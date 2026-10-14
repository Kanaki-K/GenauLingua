"""ВТОРОЙ ПРОХОД, блок 48 (ряды 9401–9600): 10 правок в 5 рядах.

БЛОК ДАЛ ДВА СКВОЗНЫХ КЛАССА, И ОБА НАЙДЕНЫ НА ОДНОЙ ЯЧЕЙКЕ КАЖДЫЙ:

 1. `Wertsachen` (9906) «in dem Safe» вместо «im Safe» → замер по всей
    базе, 50 попаданий, 23 дефекта. Правлено `fix_de_uncontracted.py`,
    остаток держит `scan_de_uncontracted` (27 законных списком).
 2. `Verstärker` (17679) — вопрос на конце фразы без знака вопроса →
    ВОСЬМОЙ ГЕЙТ `scan_de_tail_question`. Замер: 9 фраз с
    вопросительным зачином без знака на конце, 8 из них законны (знак
    стоит внутри фразы), дефект один. Правится здесь, во всех шести
    языках сразу.

Знак вопроса здесь не придирка: близнец того же ряда, `Lautstärke`
(17683), его имеет — «Die Lautstärke ist zu hoch, kannst du sie
runterdrehen?». Норма внутри базы задана, и ряд из неё выпадал.

ОСТАЛЬНЫЕ ЧЕТЫРЕ ПРАВКИ — обычный разбор:

 • `Rind` (17864) uk «воловина» — слово есть, но говяжье мясо в
   украинском «яловичина»; «воловина» это мясо вола и в словарях стоит
   с пометой. Польское «wołowina» верно, и украинское, похоже,
   списано с него.
 • `Schwergewicht` (12345) pl «To prawdziwa waga ciężka w swojej
   branży» — подлежащее подменено: «To» (это) вместо «Er» (он). Из-за
   этого «swojej» повисает: возвратное притяжательное требует личного
   подлежащего, и фраза рассыпается грамматически.
 • `Waschraum` (3000) tr «yıkama odası» (комната для мытья ЧЕГО-ТО) при
   «yıkanma odası» (мыться самому) в списке; в примере «yıkanabilirsin»
   — именно мыться самому.
 • `vollziehen` (8199) pl «Zmiany dokonują się bardzo powoli» — время
   настоящее при немецком будущем «wird sich vollziehen», плюс
   добавленное «bardzo» (очень), которого нет ни в эталоне, ни в
   четырёх других языках.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ вопрос на конце без знака: все шесть языков ═════════════
    (17679, "example_de",
     "Der Gitarrenverstärker ist zu laut, kannst du ihn leiser stellen",
     "Der Gitarrenverstärker ist zu laut, kannst du ihn leiser stellen?",
     "фраза кончается вопросом, знака нет (гейт scan_de_tail_question)"),
    (17679, "example_en",
     "The guitar amplifier is too loud, can you turn it down",
     "The guitar amplifier is too loud, can you turn it down?",
     "то же в переводе"),
    (17679, "example_ru",
     "Гитарный усилитель слишком громкий, можешь сделать тише",
     "Гитарный усилитель слишком громкий, можешь сделать тише?",
     "то же в переводе"),
    (17679, "example_uk",
     "Гітарний підсилювач занадто гучний, можеш зробити тихіше",
     "Гітарний підсилювач занадто гучний, можеш зробити тихіше?",
     "то же в переводе"),
    (17679, "example_tr",
     "Gitar amplifikatörü çok yüksek, sesini kısabilir misin",
     "Gitar amplifikatörü çok yüksek, sesini kısabilir misin?",
     "то же в переводе"),
    (17679, "example_pl",
     "Wzmacniacz gitarowy jest za głośny, możesz go przyciszyć",
     "Wzmacniacz gitarowy jest za głośny, możesz go przyciszyć?",
     "то же в переводе"),

    # ══ слово не того языка ════════════════════════════════════
    (17864, "translation_uk",
     "корова, бик, велика рогата худоба, воловина",
     "корова, бик, велика рогата худоба, яловичина",
     "говяжье мясо по-украински «яловичина»; «воловина» — мясо вола"),

    # ══ подмена подлежащего, ломающая грамматику ═══════════════
    (12345, "example_pl",
     "To prawdziwa waga ciężka w swojej branży",
     "On jest wagą ciężką w swojej branży",
     "«To» вместо «Er»; при «To» возвратное «swojej» повисает"),

    # ══ вид карточки: слово не из своего списка ═════════════════
    (3000, "example_tr",
     "Soyunma odasının yanındaki yıkama odasında yıkanabilirsin",
     "Soyunma odasının yanındaki yıkanma odasında yıkanabilirsin",
     "в списке «yıkanma odası» (мыться самому), в примере «yıkama»"),

    # ══ время и добавленное слово ══════════════════════════════
    (8199, "example_pl",
     "Zmiany dokonują się bardzo powoli",
     "Zmiany będą dokonywać się powoli",
     "настоящее при немецком будущем «wird sich vollziehen»; «bardzo» лишнее"),
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
