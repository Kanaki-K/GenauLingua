"""ТРЕТИЙ ПРОХОД, блок 7 (ряды 1201–1400): 18 ячеек в 3 рядах.

ВТОРАЯ ДЫРА В ТОМ ЖЕ МЕСТЕ, И НАШЛАСЬ ОНА ПОТОМУ, ЧТО ПЕРВУЮ Я ЗАКРЫЛ
СПИСКОМ, А НАДО БЫЛО ГРАММАТИКОЙ.

В блоке 1 закрыт `Na` (13810) и `Tja` (13835): вопрос без знака вопроса,
спрятанный от приметы ведущим междометием. Я добавил в
`scan_question_mark` снятие ведущего междометия по ЗАКРЫТОМУ СПИСКУ
(«na», «ach», «tja», «also», «hey», …) и написал в докстринге, что
список расширять нельзя.

В блоке 7 попался `Herrgott` (13894, B2) «Herrgott, was ist denn hier
passiert» — тот же дефект, и список его не берёт. Потому что `Herrgott`
не междометие, а ЗВАТЕЛЬНЫЙ ОБОРОТ, и таких оборотов бесконечно много:

    Herrgott      (13894, B2) «Herrgott, was ist denn hier passiert»
    Menschenskind (15311, B2) «Menschenskind, was hast du denn getan»
    Sau           (15459, B1) «Du dumme Sau, was machst du denn da»

════════════════════════════════════════════════════════════════════════
ПОЧЕМУ НЕЛЬЗЯ ОБОБЩИТЬ «ЧТО УГОДНО + ЗАПЯТАЯ + W-СЛОВО»
════════════════════════════════════════════════════════════════════════

Первая мысль была снимать не список, а ВООБЩЕ всё до первой запятой.
Замер: **45 попаданий, и 42 из них законные** — это подчинённые клаузы,
где W-слово вводит дополнение или определение, а не вопрос:

    unklar  (7220) «Es ist unklar, WARUM er nicht gekommen ist»
    Maximum (7815) «Das ist das Maximum, WAS ich dir leihen kann»
    gespannt (10337) «Ich bin gespannt, WIE das Konzert wird»
    rätseln (12337) «Wir rätseln noch immer, WO er hingegangen ist»

Ровно поэтому восьмой гейт (`scan_de_tail_question`) W-слова и не берёт
вовсе — об этом написано в его докстринге. Обобщение превратило бы гейт
в генератор ложных тревог.

════════════════════════════════════════════════════════════════════════
ОТДЕЛЯЕТ ВОПРОС ОТ ПОДЧИНЁННОЙ КЛАУЗЫ ВОПРОСИТЕЛЬНАЯ ЧАСТИЦА
════════════════════════════════════════════════════════════════════════

Немецкие «denn», «bloß», «eigentlich» при W-слове стоят ТОЛЬКО в
настоящем вопросе. В подчинённой клаузе их там не бывает — это
грамматика, а не частотность:

    «Was ist DENN hier passiert»   вопрос
    «Es ist unklar, warum er kam»  клауза, частицы нет и быть не может

Замер по базе: 20 рядов с сочетанием «W-слово + частица», из них **17 со
знаком «?» и ровно 3 без** — и все три оказались вопросами без знака.
**Ни одного ложного попадания.**

Признак добавлен в гейт №10 второй проверкой. Он сильнее первой, потому
что не требует перечислять зачины: их может быть сколько угодно.

ВЫВОД, КОТОРЫЙ СТОИТ ЗАПИСАТЬ ОТДЕЛЬНО. Закрывая дыру в примете,
спрашивай, закрываешь ли ты КЛАСС или только найденные случаи. Список
междометий закрыл два ряда и оставил дыру того же вида; грамматический
признак закрыл её целиком. **Между списком и правилом выбирай правило —
список кончается там, где кончилось твоё воображение.**

ВОСЕМНАДЦАТЬ ЯЧЕЕК: три ряда по шесть языков. Во всех трёх вопрос без
знака во ВСЕХ шести языках сразу — немецкий эталон задал форму, и
переводы её повторили.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # --- Herrgott (13894)
    (13894, "example_de", "Herrgott, was ist denn hier passiert",
     "Herrgott, was ist denn hier passiert?", "вопрос без знака вопроса"),
    (13894, "example_en", "Good Lord, what happened here",
     "Good Lord, what happened here?", "вопрос без знака вопроса"),
    (13894, "example_ru", "Господи, что же здесь случилось",
     "Господи, что же здесь случилось?", "вопрос без знака вопроса"),
    (13894, "example_uk", "Господи, що ж тут сталося",
     "Господи, що ж тут сталося?", "вопрос без знака вопроса"),
    (13894, "example_tr", "Tanrım, burada ne oldu",
     "Tanrım, burada ne oldu?", "вопрос без знака вопроса"),
    (13894, "example_pl", "Boże, co tu się stało",
     "Boże, co tu się stało?", "вопрос без знака вопроса"),
    # --- Menschenskind (15311)
    (15311, "example_de", "Menschenskind, was hast du denn getan",
     "Menschenskind, was hast du denn getan?", "вопрос без знака вопроса"),
    (15311, "example_en", "Good grief, what have you done",
     "Good grief, what have you done?", "вопрос без знака вопроса"),
    (15311, "example_ru", "Боже мой, что ты натворил",
     "Боже мой, что ты натворил?", "вопрос без знака вопроса"),
    (15311, "example_uk", "Божечки, що ти наробив",
     "Божечки, що ти наробив?", "вопрос без знака вопроса"),
    (15311, "example_tr", "Hay Allah, ne yaptın sen",
     "Hay Allah, ne yaptın sen?", "вопрос без знака вопроса"),
    (15311, "example_pl", "Człowieku, co ty zrobiłeś",
     "Człowieku, co ty zrobiłeś?", "вопрос без знака вопроса"),
    # --- Sau (15459)
    (15459, "example_de", "Du dumme Sau, was machst du denn da",
     "Du dumme Sau, was machst du denn da?", "вопрос без знака вопроса"),
    (15459, "example_en", "You stupid pig, what are you doing there",
     "You stupid pig, what are you doing there?", "вопрос без знака вопроса"),
    (15459, "example_ru", "Ты тупая свинья, что ты там делаешь",
     "Ты тупая свинья, что ты там делаешь?", "вопрос без знака вопроса"),
    (15459, "example_uk", "Ти дурна свиня, що ти там робиш",
     "Ти дурна свиня, що ти там робиш?", "вопрос без знака вопроса"),
    (15459, "example_tr", "Seni aptal domuz, orada ne yapıyorsun",
     "Seni aptal domuz, orada ne yapıyorsun?", "вопрос без знака вопроса"),
    (15459, "example_pl", "Ty głupia świnio, co ty tam wyprawiasz",
     "Ty głupia świnio, co ty tam wyprawiasz?", "вопрос без знака вопроса"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    seen: set[tuple[int, str]] = set()
    dupes: list[tuple[int, str]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            if (wid, col) in seen:
                dupes.append((wid, col))
            seen.add((wid, col))
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
        print("\nсухой прогон. применить: --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(
                text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now:
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
