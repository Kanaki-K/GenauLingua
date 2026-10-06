"""
Правка по примете scan_de_zu_infinitive: лишнее `zu` в инфинитиве
после модального глагола.

Примета прочла 12902 примера и дала сверх блока 59 один ряд — и он
оказался сломан глубже, чем на одно `zu`:

    de  Ich konnte die Kraft nicht herzubringen, um weiter zu gehen
    en  Bring the chairs over here, please
    ru  Я не смог собраться с силами, чтобы идти дальше
    uk  Принеси сюди ще один стілець
    tr  Devam etmek için gücü toparlamadım
    pl  Przynieś tutaj te krzesła z kuchni

`herbringen` значит «принести сюда». В эталоне он поставлен в значении
«собраться с силами» — а это `aufbringen`, другой глагол. Английский,
украинский и польский перевели правильное значение, русский и турецкий
пошли за эталоном.

То есть два дефекта в одном ряду: лишнее `zu` и подменённый глагол. И
снова тот же расклад — эталон сломан, переводы разошлись трое против
двух.

    python -m app.scripts.fix_de_zu_infinitive            # показать
    python -m app.scripts.fix_de_zu_infinitive --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    (7967, "example_de",
     "Ich konnte die Kraft nicht herzubringen, um weiter zu gehen",
     "Bring die Stühle bitte her",
     "лишнее «zu» после модального, и «herbringen» не значит "
     "«собраться с силами»"),
    (7967, "example_ru",
     "Я не смог собраться с силами, чтобы идти дальше",
     "Принеси, пожалуйста, стулья сюда",
     "перевод пошёл за сломанным эталоном"),
    (7967, "example_uk", "Принеси сюди ще один стілець",
     "Принеси сюди, будь ласка, стільці",
     "вслед за исправленным эталоном"),
    (7967, "example_tr", "Devam etmek için gücü toparlamadım",
     "Sandalyeleri lütfen buraya getir",
     "перевод пошёл за сломанным эталоном"),
    (7967, "example_pl", "Przynieś tutaj te krzesła z kuchni",
     "Przynieś tutaj, proszę, te krzesła",
     "«z kuchni» в эталоне нет"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
