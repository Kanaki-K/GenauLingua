# -*- coding: utf-8 -*-
"""
ПЕРЕНОС СЛОВАРЯ на прод — без единого удаления.

    # на машине разработчика: выгрузить исправленный словарь
    python -m app.scripts.wordbase_transfer export --out wordbase.json.gz

    # на сервере: сперва посмотреть, ничего не меняя
    python -m app.scripts.wordbase_transfer load --file wordbase.json.gz
    # и применить
    python -m app.scripts.wordbase_transfer load --file wordbase.json.gz --apply
    # затем ОБЯЗАТЕЛЬНО
    python -m app.scripts.rebuild_word_groups

ЗАЧЕМ ОТДЕЛЬНЫЙ СКРИПТ, А НЕ ДАМП ТАБЛИЦЫ. DEPLOY.md предлагал «обычный
дамп таблицы words с dev на прод». С миграцией `d2f4a6b80c13` прогресс,
ответы, жалобы, группы и клипы удаляются КАСКАДОМ вслед за словом: заливка
дампа через TRUNCATE или DELETE стёрла бы прогресс всех людей разом, и
выглядело бы это как обычная успешная заливка. Поэтому здесь только UPDATE
по номеру и INSERT новых номеров.

ТРИ ПРАВИЛА, КАЖДОЕ — ОСТАНОВКА, А НЕ ПРЕДУПРЕЖДЕНИЕ:

    1. ни одна строка не удаляется — ни слов, ни указаний леммы;
    2. номер слова, который есть в базе, но нет в файле, останавливает
       перенос целиком: на этот номер может ссылаться чей-то прогресс;
    3. суммы прогресса людей (показы, верные, выученные) сверяются до и
       после в той же транзакции; разошлись — откат.

ЧТО ПЕРЕНОСИТСЯ: текст слова, артикль, часть речи, уровень, переводы и
примеры на всех языках, категории, частотный ранг; указания леммы.
ЧТО НЕТ: `times_shown` и `times_correct` слова — это популярность, которую
копит сама база, и у прода она своя.

ПОЧЕМУ ПО НОМЕРУ БЕЗОПАСНО ПО СМЫСЛУ. Сверено с выгрузкой прода от
29.09.2026: все 12 902 номера совпадают; у 666 текст слова другой, и это
редакторские правки одного и того же слова — формы к словарной («kuck» →
«gucken», «Flöhe» → «Floh», «liefen» → «laufen»), пробелы и регистр.
Прогресс по «kuck» становится прогрессом по «gucken» — тем же словом.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text  # noqa: E402

from app.config import settings  # noqa: E402

# КОЛОНКИ ЯЗЫКОВ — ИЗ РЕЕСТРА, А НЕ СПИСКОМ (Н1, 16.10). Прежде список был
# вписан руками и кончался польским: перенос на прод «прошёл» бы успешно и
# привёз словарь без итальянского, испанского, французского и чешского —
# 12 902 × 8 ячеек остались бы пустыми, и ничто бы об этом не сказало.
# Теперь новый язык в реестре — новые колонки здесь сами собой.
def _language_columns() -> tuple[str, ...]:
    from app.services.language_service import LANGUAGES, SUPPORTED_LANGS

    words = tuple(LANGUAGES[code].word_attr for code in SUPPORTED_LANGS)
    examples = tuple(LANGUAGES[code].example_attr for code in SUPPORTED_LANGS)
    return words + examples


LANGUAGE_COLUMNS = _language_columns()
CONTENT = ("article", "pos", "level") + LANGUAGE_COLUMNS + (
    "categories", "category", "frequency_rank",
)

PROGRESS_SUMS = (
    "select count(*), coalesce(sum(times_shown),0), coalesce(sum(times_correct),0), "
    "count(*) filter (where learned) from user_words"
)


def _engine():
    return create_engine(settings.DATABASE_URL_SYNC)


def _open(path: str, mode: str):
    return gzip.open(path, mode + "t", encoding="utf-8") if path.endswith(".gz") \
        else open(path, mode, encoding="utf-8")


def export(out: str) -> int:
    cols = ", ".join(f"{c}::text" if c in ("pos", "level") else c for c in CONTENT)
    with _engine().connect() as c:
        words = [dict(r._mapping) for r in c.execute(
            text(f"select id, {cols} from words order by id"))]
        overrides = [dict(r._mapping) for r in c.execute(text(
            "select word_id, lemma_word_id, reason, lang from word_lemma_overrides "
            "order by word_id"))]
    body = json.dumps({"words": words, "overrides": overrides},
                      ensure_ascii=False, sort_keys=True, default=str)
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    with _open(out, "w") as f:
        f.write(json.dumps({"sha256": digest, "words": words, "overrides": overrides},
                           ensure_ascii=False, default=str))
    print(f"выгружено слов {len(words)}, указаний леммы {len(overrides)}")
    print(f"файл {out}, контрольная сумма {digest[:16]}")
    return 0


def load(path: str, apply: bool) -> int:
    with _open(path, "r") as f:
        data = json.load(f)
    words, overrides = data["words"], data["overrides"]
    body = json.dumps({"words": words, "overrides": overrides},
                      ensure_ascii=False, sort_keys=True, default=str)
    if hashlib.sha256(body.encode("utf-8")).hexdigest() != data["sha256"]:
        print("СТОП: контрольная сумма файла не сходится — файл повреждён")
        return 1

    # ФАЙЛ ОБЯЗАН НЕСТИ ВСЕ КОЛОНКИ. Выгрузка старой версией скрипта (без
    # новых языков) иначе затёрла бы их на проде пустыми значениями
    missing = missing_columns(words)
    if missing:
        print(f"СТОП: в файле нет колонок {missing} — выгружен старой версией?")
        return 1

    incoming = {w["id"]: w for w in words}
    eng = _engine()
    with eng.begin() as c:
        current = {r[0]: r for r in c.execute(text(
            f"select id, {', '.join(f'{x}::text' if x in ('pos', 'level') else x for x in CONTENT)} "
            "from words"))}

        # ПРАВИЛО 2: всё, что есть в базе, обязано быть в файле
        lost = sorted(set(current) - set(incoming))
        if lost:
            print(f"СТОП: в базе {len(lost)} слов, которых нет в файле: {lost[:10]}")
            print("на них может ссылаться прогресс людей — перенос не начат")
            return 1

        changed: dict[str, int] = {}
        to_update = []
        for wid, w in incoming.items():
            if wid not in current:
                continue
            row = current[wid]
            diff = [col for i, col in enumerate(CONTENT, start=1)
                    if _norm(row[i]) != _norm(w[col])]
            if diff:
                to_update.append(wid)
                for col in diff:
                    changed[col] = changed.get(col, 0) + 1
        new_ids = sorted(set(incoming) - set(current))

        print(f"слов в базе {len(current)}, в файле {len(incoming)}")
        print(f"  изменится {len(to_update)}, добавится {len(new_ids)}, удалится 0")
        for col, n in sorted(changed.items(), key=lambda kv: -kv[1]):
            print(f"    {col:16} {n}")
        print(f"  указаний леммы в файле {len(overrides)}")

        before = c.execute(text(PROGRESS_SUMS)).one()
        print(f"прогресс людей: строк {before[0]}, показов {before[1]}, "
              f"верных {before[2]}, выучено {before[3]}")

        if not apply:
            print("\nпросмотр: ничего не изменено. Применить — с --apply")
            return 0

        sets = ", ".join(
            f"{col} = CAST(:{col} AS {col_type})" if col_type else f"{col} = :{col}"
            for col, col_type in _cast_map(c).items()
        )
        for wid in to_update:
            c.execute(text(f"update words set {sets} where id = :id"),
                      _params(incoming[wid]))
        for wid in new_ids:
            cols = ", ".join(("id",) + CONTENT)
            vals = ", ".join([":id"] + [
                f"CAST(:{col} AS {t})" if t else f":{col}"
                for col, t in _cast_map(c).items()
            ])
            c.execute(text(
                f"insert into words ({cols}, times_shown, times_correct, created_at) "
                f"values ({vals}, 0, 0, now())"), _params(incoming[wid]))
        for o in overrides:
            c.execute(text(
                "insert into word_lemma_overrides (word_id, lemma_word_id, reason, lang, created_at) "
                "values (:word_id, :lemma_word_id, :reason, :lang, now()) "
                "on conflict (word_id) do update set lemma_word_id = excluded.lemma_word_id, "
                "reason = excluded.reason, lang = excluded.lang"),
                # Файл до 2.3 языка указаний не знал — значит, «для всех»
                {"lang": None, **o})

        # ПРАВИЛО 3: прогресс людей обязан сойтись до единицы
        after = c.execute(text(PROGRESS_SUMS)).one()
        if tuple(after) != tuple(before):
            print(f"СТОП: прогресс разошёлся {tuple(before)} → {tuple(after)} — откат")
            raise SystemExit(1)

        # ПРАВИЛО 4 (Н1): заполненных ячеек каждого языка в базе ровно
        # столько, сколько в файле, — иначе колонка доехала не целиком
        expected = filled_counts(words)
        for col in LANGUAGE_COLUMNS:
            got = c.execute(text(
                f"select count(*) from words where coalesce(btrim({col}), '') <> ''"
            )).scalar()
            print(f"    {col:16} в файле {expected[col]:6}  в базе {got:6}")
            if got != expected[col]:
                print(f"СТОП: колонка {col} доехала не целиком — откат")
                raise SystemExit(1)

    print(f"\nприменено: изменено {len(to_update)}, добавлено {len(new_ids)}; "
          "прогресс людей сошёлся до единицы")
    print("дальше ОБЯЗАТЕЛЬНО: python -m app.scripts.rebuild_word_groups")
    return 0


def missing_columns(words: list[dict]) -> list[str]:
    """Каких колонок нет в выгрузке (смотрится по всем словам, не по первому)."""
    if not words:
        return []
    present = set().union(*(w.keys() for w in words))
    return [col for col in CONTENT if col not in present]


def filled_counts(words: list[dict]) -> dict[str, int]:
    """Сколько непустых ячеек каждого языка в выгрузке."""
    return {
        col: sum(1 for w in words if (w.get(col) or "").strip())
        for col in LANGUAGE_COLUMNS
    }


def _norm(value):
    if isinstance(value, list):
        return sorted(str(v) for v in value)
    return None if value in (None, "") else str(value)


def _cast_map(c) -> dict[str, str | None]:
    """Тип для приведения: перечисления и массив приходят строкой."""
    types = dict(c.execute(text(
        "select column_name, udt_name from information_schema.columns "
        "where table_name = 'words'")).all())
    out = {}
    for col in CONTENT:
        udt = types.get(col)
        if col in ("pos", "level"):
            out[col] = udt
        elif col == "categories":
            out[col] = "text[]" if udt == "_text" else "varchar[]"
        else:
            out[col] = None
    return out


def _params(w: dict) -> dict:
    p = {k: w.get(k) for k in ("id",) + CONTENT}
    if isinstance(p.get("categories"), str):
        p["categories"] = p["categories"]
    return p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export"); e.add_argument("--out", required=True)
    ld = sub.add_parser("load"); ld.add_argument("--file", required=True)
    ld.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if args.cmd == "export":
        return export(args.out)
    return load(args.file, args.apply)


if __name__ == "__main__":
    sys.exit(main())
