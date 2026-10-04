"""
Класс: в украинской колонке апостроф U+02BC вместо обычного U+0027.

«компʼютер», «курʼєр», «інʼєкція», «мʼякий» — выглядят правильно, и
глазами их не отличить от «комп'ютер», «кур'єр». Но это другой символ:
U+02BC MODIFIER LETTER APOSTROPHE вместо U+0027 APOSTROPHE. В базе 781
украинская ячейка с обычным апострофом и 26 — с этим. Разнобой бьёт по
двум местам: поиск по слову не находит вторую форму, а синтез озвучки
читает её иначе, потому что это буква, а не знак препинания.

Нашлось при вычитке блока 21: у `vorfahren` в значениях стоял «підʼїхати»
с U+02BC, а в примере «підїхати» вообще без апострофа. Сплошной поиск по
символу показал 26 ячеек, все в значениях, в примерах ни одной.

ПОЧЕМУ ЗДЕСЬ НЕТ ЛИТЕРАЛА «было». Во всех прочих скриптах правок «было»
записано строкой и сверяется посимвольно — это защита от правки по чужой
строке. Здесь так нельзя: «компʼютер» и «комп'ютер» в исходнике выглядят
одинаково, и ошибку в литерале не увидел бы ни я, ни тот, кто будет
читать. Поэтому сверка другая, но не слабее: id перечислены поимённо,
ячейка обязана содержать U+02BC, замена механическая — только этот
символ на U+0027, остальной текст не трогается. Если в ячейке уже всё
исправлено, она пропускается.

    python -m app.scripts.fix_uk_apostrophe            # показать
    python -m app.scripts.fix_uk_apostrophe --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

MODIFIER = "ʼ"   # ʼ — буква-модификатор, попала по ошибке
PLAIN = "'"           # ' — обычный апостроф, им ведётся вся база

# id ячеек, найденных сплошным поиском по U+02BC (все — translation_uk)
IDS = [
    1565, 2080, 2705, 2706, 2714, 2715, 6848, 7739, 7888, 8401, 8661,
    8686, 8911, 8931, 9136, 10816, 11186, 11391, 11725, 12555, 12836,
    12928, 13019, 13944, 14124, 17106,
]

# В ячейке 11725 замечена ещё и опечатка «брискати» вместо «бризкати».
# Она правится в fix_block_0021, а не здесь: этот скрипт меняет ровно один
# символ и ничего больше, иначе «было» перестанет быть проверяемым.


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    plan, skipped = [], []
    with engine.connect() as conn:
        for wid in IDS:
            cur = conn.execute(
                text("SELECT translation_uk FROM words WHERE id = :i"),
                {"i": wid},
            ).scalar()
            if not cur or MODIFIER not in cur:
                skipped.append((wid, cur))
                continue
            plan.append((wid, cur, cur.replace(MODIFIER, PLAIN)))

    print(f"=== ячеек {len(IDS)}, с U+02BC {len(plan)}, пропущено {len(skipped)} ===\n")
    for wid, was, now in plan:
        print(f"  {wid} translation_uk — апостроф U+02BC → обычный")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, _, now in plan:
            conn.execute(
                text("UPDATE words SET translation_uk = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(plan)}")

    with engine.connect() as conn:
        bad = 0
        for wid, _, now in plan:
            cur = conn.execute(
                text("SELECT translation_uk FROM words WHERE id = :i"),
                {"i": wid},
            ).scalar()
            if cur != now or MODIFIER in (cur or ""):
                print(f"  ТРЕВОГА: {wid} не записалось")
                bad += 1
        left = conn.execute(text(
            "SELECT count(*) FROM words WHERE translation_uk LIKE :p "
            "OR example_uk LIKE :p"
        ), {"p": f"%{MODIFIER}%"}).scalar()
        print(f"самопроверка: не записалось {bad}, осталось в базе {left}")


if __name__ == "__main__":
    main()
