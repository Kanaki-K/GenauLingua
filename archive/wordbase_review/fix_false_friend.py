"""
Правки по примете scan_false_friend: перевод построен на созвучии со
словом ряда, а не на его смысле.

Примета прочла 12902 ряда по трём языкам на латинице и дала девять
попаданий. Из них три законных и шесть настоящих.

Главная находка — ряд `die Latte` (11775). Немецкое `die Latte` это
рейка, и так говорят ВСЕ ПЯТЬ словарных статей: `batten, slat`,
`рейка, планка`, `рейка, поперечина`, `çıta`, `listwa, łata`. А эталон
написан про другое слово:

    de  Ich bestelle mir jeden Morgen einen Latte im Café

`einen Latte` — мужского рода, это заимствованный из итальянского кофе,
совсем другое слово с тем же написанием. Ряд помечен артиклем `die`.
За эталоном пошли украинский («замовляю латте в кафе») и турецкий
(«bir latte sipariş ederim»), а русский, английский и польский остались
при рейке. Снова тот же расклад, что в блоке 56: эталон сломан, а
переводы разошлись.

Прочие пять — чужое написание вместо местного там, где статья даёт
правильное: tr `tequila` при статье `tekila`, `frisbee` при `frizbi`,
`Asteroid` при `asteroit`, `bestseller` при `çok satan kitap`. И одна
правка самой статьи: `aperatif` вместо `aperitif`.

Законные три примета показала и не могла не показать:
  · `Fräulein` в английском примере — там немецкое слово и цитируется;
  · `Pfennig` в турецком — название исторической монеты;
  · `Extras` — статья переведена в единственном числе после сквозной
    правки числа, и `extras` в неё просто не попало.

    python -m app.scripts.fix_false_friend            # показать
    python -m app.scripts.fix_false_friend --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 11775 die Latte — эталон про кофе, все пять статей про рейку
    (11775, "example_de",
     "Ich bestelle mir jeden Morgen einen Latte im Café",
     "Eine Latte des Zauns ist gebrochen",
     "«einen Latte» это кофе мужского рода, а ряд — «die Latte», рейка"),
    (11775, "example_ru", "Прибей ещё одну рейку к забору",
     "Одна рейка в заборе сломалась",
     "вслед за исправленным эталоном"),
    (11775, "example_uk", "Кожного ранку я замовляю латте в кафе",
     "Одна рейка в паркані зламалася",
     "перевод пошёл за сломанным эталоном, а не за статьёй"),
    (11775, "example_tr",
     "Her sabah kafede kendime bir latte sipariş ederim",
     "Çitin bir çıtası kırılmış",
     "перевод пошёл за сломанным эталоном, а не за статьёй"),
    (11775, "example_pl", "Przybił listwę do płotu",
     "Jedna listwa w płocie jest złamana",
     "вслед за исправленным эталоном"),
    # 11722 Tequila
    (11722, "example_tr", "Partide tequila içiyoruz",
     "Partide tekila içiyoruz",
     "в статье «tekila», а в примере осталось чужое написание"),
    # 11956 Aperitif — ошибка в самой статье
    (11956, "translation_tr", "aperatif, iştah açıcı içki",
     "aperitif, iştah açıcı içki",
     "«aperatif» — не словарное написание"),
    # 12364 Frisbee
    (12364, "example_tr", "Parkta frisbee oynarız",
     "Parkta frizbi oynarız",
     "в статье «frizbi», а в примере осталось чужое написание"),
    # 14705 Bestseller
    (14705, "example_tr",
     "Donna Leon'un yeni kitabı bir bestseller",
     "Donna Leon'un yeni kitabı çok satan bir kitap",
     "в статье «çok satan kitap», а в примере чужое слово"),
    # 18065 Asteroid
    (18065, "example_tr",
     "Asteroid milyonlar yıl önce Dünyaya çarpmıştı",
     "Asteroit milyonlarca yıl önce Dünya'ya çarpmıştı",
     "в статье «asteroit», и «milyonlar yıl» без «-ca»"),
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
