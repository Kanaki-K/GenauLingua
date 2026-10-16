"""ПРИМЕТА: два ряда с РАЗНЫМИ словами и одинаковыми переводами.

ОТКУДА ВЗЯЛАСЬ. В блоке 44 попался `entfliehen` (16640), в блоке 45 —
`entkommen` (8103). Заголовки разные, немецкие эталоны разные, а
переводы совпадают СЛОВО В СЛОВО в ru, uk и pl: «Заключённые сбежали из
тюрьмы».

`scan_same_headword` этого не видит: она сравнивает заголовки.
`scan_inflected_twin` тоже: там нужна общая основа. А здесь два
совершенно разных немецких слова дают одну и ту же карточку.

Признак структурный — равенство строк, — поэтому по правилу из блока 42
примета написана сразу.

ЗАМЕР: 223 пары рядов, у которых совпал пример хотя бы в одном языке.
Порог «не меньше трёх языков» оставляет 86 пар, и они делятся по тому,
совпадает ли ТАКЖЕ немецкий эталон:

    30 пар — немецкий эталон тоже совпадает;
    56 пар — немецкий эталон разный (55 из них и заголовки разные).

ПЕРВЫЕ 30 — ЗАКОННЫ, И ЭТО РЕШЕНИЕ БАЗЫ, А НЕ ОПЛОШНОСТЬ. Одна немецкая
фраза нарочно обслуживает несколько рядов, каждый из которых учит своё
слово этой фразы:

    «Das Bild hängt an der Wand»  → `an` (19), `hängen` (419), `Wand` (1001)
    «Wir spielen Fußball»         → `Fußball` (300), `spielen` (861)
    «Ich höre gern Musik»         → `hören` (421), `Musik` (618)
    «Ich trinke Wasser»           → `trinken` (942), `Wasser` (1010)

Для A1 это разумно: ученик видит знакомую фразу и учит в ней новое слово.
Сюда же попадают известные полные дубли заголовков (`Dunkelheit`, `grob`,
`aufrichtig`, `platzen`) — они уже в списке решений владельца.

ВТОРЫЕ 56 — НАСТОЯЩИЙ КЛАСС, И ОН О СИНОНИМАХ:

    herrlich (1531)   ~ wunderbar (2109)    «Погода чудесная»
    schrecklich(1843) ~ furchtbar (2494)
                      ~ miserabel (10878)   «Погода ужасная» — ТРОЙКА
    Toilette (932)    ~ WC (1011)
                      ~ Klo (18139)         «Где туалет?»   — ТРОЙКА
    Beil (7919)       ~ Axt (18193)         «Он взял топор…»
    entkommen (8103)  ~ entfliehen (16640)  «Заключённые сбежали…»
    Gegenmittel(12650)~ Gegengift (12782)
    Stockwerk (18248) ~ Geschoss (18401)
    dreist (10924)    ~ unverschämt (11601)
    herstellen (2559) ~ produzieren (2733)
    ... и ещё около сорока пар

ПЕРВОЕ, ЧТО Я ПРОВЕРИЛ — НЕ ЛОМАЕТ ЛИ ЭТО ТЕСТ. Если `herrlich` и
`wunderbar` дают один перевод, то вопрос про `herrlich` с дистрактором
`wunderbar` имеет ДВА верных ответа. Это ровно та беда, которую HANDOVER
называет главной для многозначных ячеек.

**Код уже защищён, и проверено это прямо в нём.** `get_distractors`
(`app/services/quiz_service.py`) отбрасывает кандидата, чьи значения
пересекаются с верным ответом хотя бы по одному:

    if not variants or variants & taken:
        continue

Сравнение идёт по `meaning_variants`, то есть по каждому значению
отдельно, а не по строке целиком. Значит все 56 пар для теста безвредны.

Это первый случай за проход, когда замер нашёл класс, а продакшн-код
оказался к нему уже готов. Вывод для будущих замеров: **прежде чем
считать класс дефектом, посмотри, не обрабатывает ли его код.**

ЧТО ОСТАЁТСЯ ВЛАДЕЛЬЦУ. Два ряда всё равно учат одному и тому же: одна
фраза, один перевод, разные немецкие слова. Ученик встречает по сути одну
карточку дважды. Это то же решение, что по 175 парам одинаковых
заголовков (`scan_same_headword`), и оно о составе базы, а не о дефекте:
удалять ряд нельзя — меняется размер базы и связи `user_words`.

Разумный вариант для владельца: у синонимичных пар РАЗВЕСТИ примеры, а не
удалять ряды. Тогда `Beil` останется про топорик, а `Axt` про колун, и
обе карточки начнут учить разному.

ПРЕДЕЛ ПРИМЕТЫ. Она сравнивает строки целиком, поэтому пары, где перевод
отличается одним словом, не видит. Порог «три языка» выбран замером: на
двух языках пар 47, и среди них много случайных совпадений коротких фраз.
"""

from __future__ import annotations

import sys
from collections import defaultdict

from sqlalchemy import create_engine, text

from app.config import settings

LANGS = ("en", "ru", "uk", "tr", "pl")
# Новые языки считаются ОТДЕЛЬНО, и замер старых от них не меняется: числа
# 30 и 56 выше — про пять старых языков. Для новых интересно другое: пара,
# где немецкие фразы разные, старые языки их РАЗЛИЧАЮТ, а новые переводят
# одной строкой. Синонимы (`herrlich` ~ `wunderbar`) старые языки уже
# склеили, и это известный класс; а склейка только в новых — похоже на
# пример, переписанный из соседнего ряда.
NEW_LANGS = ("it", "es", "fr", "cs")
MIN_LANGS = 3
EXPECTED_SAME_DE = 30
EXPECTED_DIFF_DE = 56


def coinciding(rows, langs) -> dict[tuple[int, int], set[str]]:
    """Пары рядов и языки, в которых их примеры совпали строка в строку."""
    pair_langs: dict[tuple[int, int], set[str]] = defaultdict(set)
    for lang in langs:
        by_text: dict[str, list[int]] = defaultdict(list)
        for row in rows:
            example = (row[f"example_{lang}"] or "").strip()
            if example:
                by_text[example].append(row["id"])
        for ids in by_text.values():
            if len(ids) < 2:
                continue
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    pair_langs[(ids[i], ids[j])].add(lang)
    return pair_langs


def main() -> None:
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, level, example_de, "
            + ", ".join(f"example_{lang}" for lang in LANGS + NEW_LANGS)
            + " FROM words ORDER BY id"
        )).mappings().all()
    by_id = {r["id"]: r for r in rows}

    pair_langs = coinciding(rows, LANGS)

    same_de = []
    diff_de = []
    for (first, second), langs in pair_langs.items():
        if len(langs) < MIN_LANGS:
            continue
        a, b = by_id[first], by_id[second]
        target = same_de if (a["example_de"] or "").strip() == (b["example_de"] or "").strip() else diff_de
        target.append((a, b, langs))

    print("=== немецкий эталон РАЗНЫЙ — настоящий класс ===")
    for a, b, langs in sorted(diff_de, key=lambda x: -len(x[2])):
        print(f"{a['word_de']} ({a['id']}, {a['level']})  ~  "
              f"{b['word_de']} ({b['id']}, {b['level']})   {len(langs)} яз.")
        print(f"    de A: {a['example_de']}")
        print(f"    de B: {b['example_de']}")
        print(f"    ru  : {a['example_ru']}")

    print("\n=== немецкий эталон ТОЖЕ совпадает — одна фраза на несколько рядов ===")
    for a, b, langs in sorted(same_de, key=lambda x: -len(x[2])):
        print(f"{a['word_de']} ({a['id']}) ~ {b['word_de']} ({b['id']})   "
              f"{len(langs)} яз.   {a['example_de']}")

    print(f"\nпар с совпавшим переводом в ≥{MIN_LANGS} языках: {len(same_de) + len(diff_de)}")
    print(f"   немецкий эталон тоже совпадает: {len(same_de)} (ожидаем {EXPECTED_SAME_DE})")
    print(f"   немецкий эталон разный:         {len(diff_de)} (ожидаем {EXPECTED_DIFF_DE})")
    print("для теста безвредно: get_distractors отбрасывает пересечение значений")

    new_pairs = coinciding(rows, NEW_LANGS)
    only_new = []
    for (first, second), langs in new_pairs.items():
        if len(langs) < MIN_LANGS:
            continue
        a, b = by_id[first], by_id[second]
        if (a["example_de"] or "").strip() == (b["example_de"] or "").strip():
            continue
        if len(pair_langs.get((first, second), ())) >= MIN_LANGS:
            continue                      # старые языки склеили тоже — синонимы
        only_new.append((a, b, langs))
    if new_pairs:
        print(f"\n=== it/es/fr/cs: немецкий разный, старые языки различают, "
              f"новые (≥{MIN_LANGS}) склеили: {len(only_new)} ===")
        for a, b, langs in only_new:
            print(f"{a['word_de']} ({a['id']})  ~  {b['word_de']} ({b['id']})   "
                  f"{','.join(sorted(langs))}")
            print(f"    de A: {a['example_de']}")
            print(f"    de B: {b['example_de']}")
            for lang in NEW_LANGS:
                print(f"    {lang}  : {a[f'example_{lang}']}")
    if len(same_de) != EXPECTED_SAME_DE or len(diff_de) != EXPECTED_DIFF_DE:
        print("ВНИМАНИЕ: остаток изменился — разбери и обнови docstring")
        sys.exit(1)


if __name__ == "__main__":
    main()
