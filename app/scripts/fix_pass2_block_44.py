"""ВТОРОЙ ПРОХОД, блок 44 (ряды 8601–8800): 5 правок.

ПЛОТНОСТЬ ДЕФЕКТОВ ПРОДОЛЖАЕТ ПАДАТЬ, И ТЕПЕРЬ ЭТО РЯД, А НЕ СЛУЧАЙ:

    блоки 36–38   35–44 правки   18–22%
    блок 41       16 правок       8%
    блок 42       13 правок       6.5%
    блок 43        8 правок       4%
    блок 44        5 правок       2.5%

Пять блоков подряд вниз, и падение не объясняется легкостью рядов: здесь
по-прежнему C1 и C2, редкие слова, длинные фразы. Объяснение в другом —
закрытые классы больше не возвращаются. Правка матчера (блок 39) убрала
класс «показывается не то значение», примета на запятую (42) — класс
«потеряна вторая часть», гейт на строчную (43) — класс опечаток в начале
фразы.

ПОЛЬСКИХ ПРАВОК ОДНА, И ОНА МЕЛКАЯ. Две подряд чистых по польскому
блока после шести полос — это уже не случайность, а признак того, что
польские дефекты сосредоточены в определённых участках базы, а не
размазаны по ней. Участок 8601–8800 чист.

ОСТАЛОСЬ ТО, ЧТО НИ ОДНА ПРИМЕТА НЕ ВИДИТ ПО УСТРОЙСТВУ:

    Putsch (16633) de «Der Putsch war ein Fehlschlag UND hatte
                       weitreichende politische Folgen»
                   ru «НЕУДАВШИЙСЯ путч имел далеко идущие…»
                   uk «НЕВДАЛИЙ путч мав далекосяжні…»

Два сказуемых немецкого свернулись в одно определение: вместо «путч был
неудачей и имел последствия» получилось «неудавшийся путч имел
последствия». Смысл почти тот же, но ученик видит одно сказуемое там,
где в эталоне два.

`scan_pl_comma_clause` этого не поймает по устройству: в немецком здесь
НЕТ запятой, части соединены союзом «und». Предел приметы назван в ней
самой, и это ровно он.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ два сказуемых эталона свернулись в одно определение ═════
    (16633, "example_ru",
     "Неудавшийся путч имел далеко идущие политические последствия",
     "Путч был неудачей и имел далеко идущие политические последствия",
     "в эталоне два сказуемых: «war ein Fehlschlag und hatte»"),
    (16633, "example_uk",
     "Невдалий путч мав далекосяжні політичні наслідки",
     "Путч був невдачею і мав далекосяжні політичні наслідки",
     "то же"),

    # ══ добавленное слово ══════════════════════════════════════
    (15223, "example_pl",
     "Pies merdał tyłkiem z radości",
     "Pies merdał tyłkiem",
     "«z radości» в эталоне «wedelte mit dem Hinterteil» нет"),

    # ══ форма, которой в языке нет ═════════════════════════════
    (12927, "example_uk",
     "Чоловік отримав інфаркт, і його швидко доставили до лікарні",
     "У чоловіка стався інфаркт, і його швидко доставили до лікарні",
     "інфаркт не «отримують»: по-українськи «стався»"),
    (18381, "example_pl",
     "Tapeta w moim salonie zupełnie się odklejała",
     "Tapeta w moim salonie już całkiem się odkleiła",
     "незавершённый вид против «ist abgelöst»: обои уже отклеились"),
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
