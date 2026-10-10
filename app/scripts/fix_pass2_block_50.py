"""ВТОРОЙ ПРОХОД, блок 50 (ряды 9801–10000): 10 правок.

ПОЛОВИНА БАЗЫ ПРОЙДЕНА. Блок дал ещё один сквозной класс — «вариант
списка, добавляющий только пустое местоимение» (23 ячейки,
`fix_empty_placeholder_variant.py`), найденный на `gegenüberstehen`.

ОДИН РЯД ПРОТИВ СВОЕГО БЛИЗНЕЦА — ТОТ ЖЕ ПРИЁМ, ЧТО В БЛОКЕ 49:

    verschonen (8271)  de «Bitte verschon mich VON deinen Kommentaren»
    verschonen (10649) de «Verschone mich MIT deinen Kritiken»

Два ряда с одним заголовком (класс повторов, 175 пар), и управление у них
разное. По Дудену «jemanden MIT etwas verschonen» — предлог «mit». То
есть прав второй ряд, а первый дал «von» вслед за русским «избавить ОТ».
Это не стиль, а предлог при глаголе, и близнец в базе показывает норму.

ПОДМЕНА, КОТОРАЯ ПОВТОРИЛАСЬ ДВАЖДЫ ОДНОЙ ФРАЗОЙ:

    Quacksalber (13017) pl «Ten lekarz to ZWYKŁY znachor»
    Scharlatan  (11425) pl «Ten lekarz to ZWYKŁY szarlatan»   ← блок 49

Два разных немецких заголовка получили одну польскую заготовку, в которой
меняется только последнее слово. `Scharlatan` правлен в блоке 49 (там
немецкий говорит «Der Mann», а не «Arzt»); здесь немецкий как раз про
врача, поэтому убирается только добавленное «zwykły». Это прямое
подтверждение гипотезы о польских примерах, СОЧИНЁННЫХ по заготовке.

ОСТАЛЬНЫЕ ВОСЕМЬ:

 • `ehelichen` (15271) pl «Chce poślubić swoją dziewczynę latem» —
   подмена целиком: своя девушка и лето вместо «sie ehelichen und eine
   Familie gründen».
 • `Herzversagen` (13018) pl «Dziadek zmarł nagle» (дедушка внезапно)
   вместо «Der Patient starb» (пациент умер).
 • `Kronleuchter` (18421) uk и tr добавили «кришталева»/«kristal», чего
   в «Der prächtige Kronleuchter» нет. Побочный след: из-за этого
   карточка показывала второй вариант списка («кришталева люстра»)
   вместо того, что стоит в эталоне.
 • `zuordnen` (8270) pl потеряно «klaren» (чёткой).
 • `abkratzen` (8280) pl «Muszę zeskrobać» (должен) при немецком «Ich
   kratze ... ab» — настоящее время без долженствования, как в четырёх
   других языках.
 • `kaltmachen` (8292) pl «W filmie» без «tym» при «In diesem Film»;
   указание есть во всех пяти остальных языках.
 • `Odyssee` (14734) tr «birçok maceralı, gerçek bir destansı serüvendi»
   — «birçok maceralı» рассыпается: «birçok» требует существительного,
   а не прилагательного. Нормальная форма «birçok macerayla dolu».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ предлог при глаголе; близнец в базе показывает норму ════
    (8271, "example_de",
     "Bitte verschon mich von deinen Kommentaren",
     "Bitte verschon mich mit deinen Kommentaren",
     "«verschonen» управляет «mit»; близнец 10649 так и написан"),

    # ══ польская заготовка, повторённая в двух рядах ════════════
    (13017, "example_pl",
     "Ten lekarz to zwykły znachor",
     "Ten lekarz to znachor",
     "«zwykły» в «Dieser Arzt ist ein Quacksalber» нет; та же заготовка, "
     "что в Scharlatan (11425)"),

    # ══ подмены целиком ════════════════════════════════════════
    (15271, "example_pl",
     "Chce poślubić swoją dziewczynę latem",
     "Chce ją poślubić i założyć rodzinę",
     "своя девушка и лето вместо «sie ehelichen und eine Familie gründen»"),
    (13018, "example_pl",
     "Dziadek zmarł nagle na niewydolność serca",
     "Pacjent zmarł na niewydolność serca",
     "«дедушка внезапно» вместо «Der Patient starb»"),

    # ══ добавлено то, чего в эталоне нет ═══════════════════════
    (18421, "example_uk",
     "Розкішна кришталева люстра висить у центрі бальної зали",
     "Розкішна люстра висить у центрі бальної зали",
     "«кришталева» в «Der prächtige Kronleuchter» нет"),
    (18421, "example_tr",
     "Görkemli kristal avize balo salonunun merkezinde asılı",
     "Görkemli avize balo salonunun merkezinde asılı",
     "«kristal» в эталоне нет"),

    # ══ потеряно то, что есть в эталоне ════════════════════════
    (8270, "example_pl",
     "Nie umiem przyporządkować tego do żadnej kategorii",
     "Nie umiem przyporządkować tego do żadnej jasnej kategorii",
     "потеряно «klaren»"),
    (8292, "example_pl",
     "W filmie gangster chce sprzątnąć rywala",
     "W tym filmie gangster chce sprzątnąć rywala",
     "потеряно «diesem»; указание есть во всех пяти остальных языках"),

    # ══ время и долженствование ════════════════════════════════
    (8280, "example_pl",
     "Muszę zeskrobać starą naklejkę ze słoika",
     "Zeskrobuję starą naklejkę ze słoika",
     "«должен» при немецком «Ich kratze ... ab»"),

    # ══ рассыпавшаяся турецкая конструкция ═════════════════════
    (14734, "example_tr",
     "Afrika'daki yolculuğu birçok maceralı, gerçek bir destansı serüvendi",
     "Afrika'daki yolculuğu birçok macerayla dolu gerçek bir destansı serüvendi",
     "«birçok» требует существительного, а не прилагательного «maceralı»"),
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
