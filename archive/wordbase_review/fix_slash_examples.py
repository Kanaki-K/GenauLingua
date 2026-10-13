"""
Примеры, в которых остались следы правки: два варианта через слеш.

Нашлось при сплошном поиске по базе после того, как второй круг вычитки
принёс третий такой случай подряд. Всего девять строк, и они двух видов.

ПЕРВЫЙ — два варианта фразы, разделённые слешем:

    de: Das Glas kippt um. / Das Glas ist umgekippt
    tr: Cüzdanım kayıp / gitti

Кто-то правил пример и оставил оба варианта. Голос прочитает это вслух
целиком, со слешем.

ВТОРОЙ, хуже — к примеру приклеился сам перевод слова:

    en: Peace / quiet - There is peace here
    en: Bandages / dressing material — There's bandaging material in the kit

Здесь «Peace / quiet» — это перевод слова Ruhe, а не часть фразы. Человек
видит на карточке мешанину из словарной статьи и примера.

Оставляю один вариант — тот, что соответствует немецкому примеру по времени
и форме; приклеенный перевод убираю целиком.

    python -m app.scripts.fix_slash_examples            # показать
    python -m app.scripts.fix_slash_examples --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [

    # --- приклеенный перевод --------------------------------------------------
    (769, "example_en",
     "Peace / quiet - There is peace here",
     "There is peace here",
     "к примеру приклеен перевод слова Ruhe"),
    (7390, "example_en",
     "Almost / nearly - That's almost impossible",
     "That's almost impossible",
     "к примеру приклеен перевод слова nahezu"),
    (13000, "example_en",
     "Bandages / dressing material — There's bandaging material in the first aid kit",
     "There's bandaging material in the first aid kit",
     "к примеру приклеен перевод слова Verbandszeug"),

    # --- два варианта через слеш ---------------------------------------------
    #
    # Немецкий пример у kippen стоял в двух временах сразу. Беру настоящее:
    # оно совпадает с английским «The glass tips over» и турецким переводом.
    (2606, "example_de",
     "Das Glas kippt um. / Das Glas ist umgekippt",
     "Das Glas kippt um",
     "два варианта и точка в конце"),
    (2606, "example_pl",
     "Szklanka się przewraca. / Szklanka się przewróciła",
     "Szklanka się przewraca",
     "два варианта и точка в конце"),
    (2817, "example_tr",
     "Bu mantıklı değil / anlamı yok",
     "Bu mantıklı değil",
     "два варианта через слеш"),
    (7854, "example_tr",
     "Cüzdanım kayıp / gitti",
     "Cüzdanım kayıp",
     "два варианта через слеш"),
    (2937, "example_tr",
     "Ben kızgınım / alınmışım",
     "Ben kızgınım",
     "два варианта через слеш"),
    (2941, "example_tr",
     "Bu uyumlu değil / bağdaşmıyor",
     "Bu uyumlu değil",
     "два варианта через слеш"),
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

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
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

    # Самопроверка: слешей-разделителей в примерах остаться не должно
    cols = ["example_de", "example_ru", "example_uk",
            "example_en", "example_tr", "example_pl"]
    with engine.connect() as conn:
        left = sum(
            conn.execute(text(f"SELECT COUNT(*) FROM words WHERE {c} LIKE '% / %'")).scalar()
            for c in cols
        )
    print(f"самопроверка: примеров со слешем-разделителем осталось {left}")


if __name__ == "__main__":
    main()
