# -*- coding: utf-8 -*-
"""
Одна команда, которая отвечает «всё ли в порядке».

    python -m app.scripts.state_report

Зачем. Состояние складывается из шести разных проверок, и запускать их по
очереди — шесть команд и шесть разных форматов вывода. Владелец спросил:
«я могу просто прийти, открыть комп, проверить, что разные языки, правильная
озвучка, правильно всё». Вот ответ на этот вопрос одной строкой на пункт.

Скрипт ТОЛЬКО ЧИТАЕТ: ничего не правит, не синтезирует, не удаляет и в
Telegram не ходит. Его безопасно запускать в любой момент.

Что НЕ проверяется здесь и почему:

  приметы и гейты   — их 48, каждая печатает свой разбор; запускать надо
                      отдельно, иначе вывод этой сводки утонет
  pytest            — то же, своя команда
  проверка слухом   — медленная, минуты на сотню клипов; запускается
                      отдельно по языку, результат лежит в asr_check_*.jsonl
                      и показывается здесь, если файлы есть
"""
from __future__ import annotations

import glob
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.config import settings  # noqa: E402

# Эталон целостности.
#
# Рядов должно быть РОВНО столько: правка текста не создаёт и не удаляет
# ряды, и любое расхождение здесь означает, что тронули не ту таблицу.
EXPECTED_ROWS = 12902

# А вот показы и верные ответы — НЕ РОВНО, а НЕ МЕНЬШЕ.
#
# Сперва здесь стояло точное равенство, и это было верно ровно до того дня,
# когда владелец сел играть в тестового бота сам: счётчики выросли на
# одиннадцать показов, и отчёт закричал «СБОЙ целостности» при совершенно
# целой базе. Ложная тревога такого рода хуже отсутствия проверки — новая
# сессия увидела бы СБОЙ и пошла искать несуществующую порчу.
#
# Смысл проверки при этом сохраняется полностью: счётчики могут только
# РАСТИ. Если они упали — значит кто-то переписал или потерял user_words, а
# это ровно та беда, от которой гейт и поставлен.
BASELINE_SHOWN = 29742
BASELINE_CORRECT = 26133

OK = "ОК  "
BAD = "СБОЙ"


def line(status: str, title: str, detail: str = "") -> None:
    print(f"  [{status}] {title}" + (f" — {detail}" if detail else ""))


def check_base(engine) -> bool:
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT COUNT(*) FROM words")).scalar()
        shown, correct = conn.execute(
            text("SELECT SUM(times_shown), SUM(times_correct) FROM user_words")
        ).first()

    shown = shown or 0
    correct = correct or 0
    good = (rows == EXPECTED_ROWS
            and shown >= BASELINE_SHOWN
            and correct >= BASELINE_CORRECT)

    played = shown - BASELINE_SHOWN
    tail = f", наиграно с эталона +{played}" if played else ""
    line(OK if good else BAD, "целостность базы",
         f"рядов {rows}, показов {shown}, верных {correct}{tail}")

    if rows != EXPECTED_ROWS:
        line(BAD, "   рядов не столько",
             f"{rows} против {EXPECTED_ROWS} — тронули не ту таблицу")
    if shown < BASELINE_SHOWN or correct < BASELINE_CORRECT:
        line(BAD, "   счётчики УПАЛИ",
             f"показов {shown} (было не меньше {BASELINE_SHOWN}), "
             f"верных {correct} (не меньше {BASELINE_CORRECT}) — "
             f"user_words переписан или потерян")
    return good


def check_card(engine) -> bool:
    """Карточка: одно значение, и оно же озвучено и стоит в названии клипа."""
    from app.database.models import Word
    from app.services.audio_service import KIND_WORD, audio_title, spoken_for
    from app.services.language_service import (
        SUPPORTED_LANGS, example_text, get_language, main_meaning,
        option_label, upper_first,
    )

    pairs = shown_bad = spoken_bad = title_bad = list_bad = 0
    with Session(engine) as s:
        ids = s.execute(text("SELECT id FROM words ORDER BY id")).scalars().all()
        for i in ids:
            w = s.get(Word, i)
            for lang in SUPPORTED_LANGS:
                chosen = main_meaning(w, lang)
                if not chosen:
                    continue
                pairs += 1
                shown = option_label(w, lang)
                want = (chosen if get_language(lang).uses_article
                        else upper_first(chosen, lang))
                if shown != want:
                    shown_bad += 1
                if "," in shown:
                    list_bad += 1
                if (spoken_for(w, lang, KIND_WORD) or "").strip() != chosen.strip():
                    spoken_bad += 1
                if not audio_title(chosen, example_text(w, lang)).startswith(chosen):
                    title_bad += 1

    good = not (shown_bad or spoken_bad or title_bad or list_bad)
    line(OK if good else BAD, "карточка", f"проверено пар «ряд × язык» {pairs}")
    for name, count in (("на кнопке список, а не одно слово", list_bad),
                        ("показано не выбранное значение", shown_bad),
                        ("озвучено не выбранное значение", spoken_bad),
                        ("название клипа не с того слова", title_bad)):
        if count:
            line(BAD, f"   {name}", str(count))
    return good


def check_audio(engine) -> bool:
    """Хранилище клипов: сколько есть и сколько не хватает."""
    from app.database.models import Word
    from app.services import audio_store
    from app.services.audio_service import KIND_FULL, KIND_WORD, spoken_for
    from app.services.language_service import SUPPORTED_LANGS
    from app.services.tts_voices import default_voice

    # Клип нужен не каждому ряду, а каждому КАНОНИЧЕСКОМУ в своём языке:
    # ряды, которые для этого языка дают одно и то же слово, схлопнуты в
    # группу и делят один клип. Считать по всем рядам — значит насчитать
    # десятки тысяч несуществующих пропаж.
    missing = total = 0
    seen: set[tuple[str, str, str]] = set()
    with Session(engine) as s:
        for lang in SUPPORTED_LANGS:
            voice = default_voice(lang)
            ids = s.execute(text("""
                SELECT w.id FROM words w
                JOIN word_lang_groups g
                  ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
                ORDER BY w.id
            """), {"lang": lang}).scalars().all()
            for i in ids:
                w = s.get(Word, i)
                for kind in (KIND_WORD, KIND_FULL):
                    spoken = spoken_for(w, lang, kind)
                    if not spoken or (lang, kind, spoken) in seen:
                        continue
                    seen.add((lang, kind, spoken))
                    total += 1
                    if audio_store.read(lang, voice, kind, spoken) is None:
                        missing += 1

    root = pathlib.Path("tts")
    on_disk = sum(1 for _ in root.rglob("*.mp3")) if root.exists() else 0
    size_gb = (sum(f.stat().st_size for f in root.rglob("*.mp3")) / 2**30
               if root.exists() else 0)

    line(OK if not missing else BAD, "озвучка",
         f"на диске {on_disk} клипов, {size_gb:.2f} ГБ; "
         f"нужно {total}, не хватает {missing}")
    return not missing


def check_pairs(engine) -> bool:
    """
    Языковые пары: на каждой ли есть чем играть.

    Пар тридцать — шесть изучаемых языков на пять языков значения. Если в
    какой-то паре рядов мало, викторина по ней выйдет куцей, и заметить это
    иначе как счётом нельзя.
    """
    from app.services.language_service import LANGUAGES, LEARNABLE_LANGS

    worst = None
    with engine.connect() as conn:
        for learn in LEARNABLE_LANGS:
            la = LANGUAGES[learn]
            for native in LEARNABLE_LANGS:
                if learn == native:
                    continue
                na = LANGUAGES[native]
                n = conn.execute(text(f"""
                    SELECT COUNT(*) FROM words w
                    JOIN word_lang_groups g
                      ON g.word_id = w.id AND g.lang = :l AND g.is_canonical
                    WHERE w.{la.word_attr} IS NOT NULL
                      AND btrim(w.{la.word_attr}) <> ''
                      AND w.{na.word_attr} IS NOT NULL
                      AND btrim(w.{na.word_attr}) <> ''
                      AND w.{la.example_attr} IS NOT NULL
                      AND w.{na.example_attr} IS NOT NULL
                """), {"l": learn}).scalar()
                if worst is None or n < worst[0]:
                    worst = (n, f"{learn}->{native}")

    good = worst is not None and worst[0] >= 5000
    line(OK if good else BAD, "языковые пары",
         f"все 30 покрыты, самая бедная {worst[1]} — {worst[0]} рядов")
    return good


def check_asr() -> None:
    """Проверка слухом — если её запускали, показать результат."""
    files = sorted(glob.glob("asr_check*.jsonl"))
    if not files:
        line("—   ", "проверка слухом", "не запускалась")
        return
    for path in files:
        rows = [json.loads(x) for x in open(path, encoding="utf-8") if x.strip()]
        if not rows:
            continue
        ok = sum(1 for r in rows if r.get("verdict") == "совпало")
        lang = pathlib.Path(path).stem.replace("asr_check", "").lstrip("_") or "?"
        share = 100 * ok / len(rows)
        line(OK if share >= 99 else BAD, f"   слухом {lang}",
             f"{ok} из {len(rows)} ({share:.1f}%)")


def main() -> int:
    engine = create_engine(settings.DATABASE_URL_SYNC)
    print("\n=== СОСТОЯНИЕ ===\n")
    results = [check_base(engine), check_pairs(engine),
               check_card(engine), check_audio(engine)]
    check_asr()
    print()
    if all(results):
        print("  Всё в порядке. Отдельно прогнать: приметы, pytest, verify_wordbase.\n")
        return 0
    print("  Есть сбои — см. строки СБОЙ выше.\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
