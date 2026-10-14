"""
Второй проход по разговорному усечению в НЕМЕЦКОМ ЭТАЛОНЕ: 15 ячеек.

Первый проход (`fix_de_colloquial`, 88 ячеек) закрыл только то, что
ловила первая версия приметы: `Ich <основа>` и `ne` перед заглавной
буквой. Блок 28 показал две дырки — инверсия (`Morgen fahr ich weg`) и
`ne` перед строчной (`echt ne miese Tour`). Примета расширена, и на
расширенной нашлось ещё 15 ячеек: четырнадцать `hab ich` / `geh ich` и
пять усечённых артиклей.

Отдельно важное: примета показала ряд 13435, где слово базы — это само
`ne`, а пример `Das ist gut, ne?` ровно этому и учит. Его чинить
нельзя, поэтому в скане появился список `LEGIT_HEADWORDS`. Это тот же
случай, что `Bürger/in` в `scan_word_in_example`: примета верна, а
строка — нет.

    python -m app.scripts.fix_de_colloquial_2            # показать
    python -m app.scripts.fix_de_colloquial_2 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, слово ряда)
FIXES: list[tuple[int, str, str, str, str]] = [
    (1834, "example_de", "Schließlich hab ich es geschafft",
     "Schließlich habe ich es geschafft", "schließlich"),
    (11836, "example_de",
     "Zum Kaffee hab ich frisches Gebäck vom Bäcker mitgebracht",
     "Zum Kaffee habe ich frisches Gebäck vom Bäcker mitgebracht", "Gebäck"),
    (12311, "example_de",
     "In der Schule hab ich fechten mit dem Säbel gelernt",
     "In der Schule habe ich fechten mit dem Säbel gelernt", "fechten"),
    (12395, "example_de", "Am Wochenende geh ich oft golfen",
     "Am Wochenende gehe ich oft golfen", "golfen"),
    (13651, "example_de", "Für Halloween hab ich mir ein Vampir-Kostüm gekauft",
     "Für Halloween habe ich mir ein Vampir-Kostüm gekauft", "Kostüm"),
    (13811, "example_de", "Ach Gott, hab ich das vergessen",
     "Ach Gott, habe ich das vergessen", "Gott"),
    (14253, "example_de",
     "Nach einer kurzen Unterredung mit dem Chef hab ich die Stelle bekommen",
     "Nach einer kurzen Unterredung mit dem Chef habe ich die Stelle bekommen",
     "Unterredung"),
    (15714, "example_de", "Am Strand hab ich eine schöne Muschel gefunden",
     "Am Strand habe ich eine schöne Muschel gefunden", "Muschel"),
    (18613, "example_de", "Das hab ich zuvor nie gesehen",
     "Das habe ich zuvor nie gesehen", "zuvor"),
    (18690, "example_de", "Heute hab ich keine Zeit, vielleicht ein andermal",
     "Heute habe ich keine Zeit, vielleicht ein andermal", "andermal"),
    (7043, "example_de", "Das ist ne coole neue App",
     "Das ist eine coole neue App", "cool"),
    (8316, "example_de", "Das ist ne indirekte Frage, keine direkte",
     "Das ist eine indirekte Frage, keine direkte", "indirekt"),
    (10474, "example_de",
     "Das war 'ne tragische Geschichte mit traurigem Ende",
     "Das war eine tragische Geschichte mit traurigem Ende", "tragisch"),
    (10565, "example_de", "Das ist ne geile neue Gitarre",
     "Das ist eine geile neue Gitarre", "geil"),
    (18787, "example_de", "Das ist ne dauerhafte Lösung",
     "Das ist eine dauerhafte Lösung", "dauerhaft"),
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
