"""
Класс: значение с заглавной буквы — и всё, что нашлось в тех же рядах.

Нашлось через `scan_pos`. Он показывает 40 ячеек «первое значение не
глагол», и они считались ложными: модальные («должен», «можно»),
«смотри» у `siehe`, «были бы» у `wären` — там действительно всё верно.
Но в этих сорока лежали два настоящих: `zwitschern` → «Chirp» и
`versklaven` → «To enslave». Заглавная буква в середине словарной
статьи, да и глагол без «to».

Сплошной поиск по заглавной первой букве дал 332 ячейки в 156 рядах, и
почти все законные: месяцы и дни недели в английском и турецком,
этнонимы и языки («German», «Almanca»), имена собственные («Пасха»,
«Альпы», «Бог»), аббревиатуры («ДТП», «НАТО»), «Вы» и «I». Незаконных —
26 ячеек в семи рядах.

Шесть из семи рядов — одна поздняя партия переводов (ранг около 23 000,
id 14805–17389), и у неё три приметы сразу: заглавная первая буква,
пустая польская колонка и потерянная «ё». Та же партия, что дала 33
ячейки классу `fix_yo`.

**Польская колонка заполнена здесь же** — это те самые пять слов, про
которые в HANDOVER сказано «без польского перевода — 5». Чтобы они
появились в польских карточках, нужна пересборка групп: слова без
`translation_pl` в польские группы не попадают. Пересборку я не делаю,
это решение владельца — см. HANDOVER, раздел 7.

Попутно: `vergönnen` — английское «It wa's not granted», лишний
апостроф внутри слова; `Waage` — турецкий взвешивал яблоки, а немецкий
фрукты; `versklaven` — турецкое «on yıl» это десять лет, а в немецком
десятилетия.

    python -m app.scripts.fix_late_batch            # показать
    python -m app.scripts.fix_late_batch --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

_CAP = "значение с заглавной буквы"
_PL = "польская колонка была пустой"

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- заглавная буква в словарной статье -----------------------------------
    (9856, "translation_ru", "Весы", "весы, равновесие",
     "заглавная; и ряд про весы, а не про знак зодиака"),
    (11575, "translation_ru", "Неловкость", "неловкость, конфуз", _CAP),
    (11575, "translation_en", "Embarrassment, awkwardness",
     "embarrassment, awkwardness", _CAP),
    (11575, "translation_tr", "Utanç", "utanç, mahcubiyet", _CAP),
    (14805, "translation_ru", "Драгоценности короны",
     "драгоценности короны", _CAP),
    (14805, "translation_uk", "Королівські коштовності",
     "королівські коштовності", _CAP),
    (14805, "translation_en", "Crown jewels", "crown jewels", _CAP),
    (14805, "translation_tr", "Taç mücevherleri", "taç mücevherleri", _CAP),
    (15315, "translation_ru", "Веснушки", "веснушки", _CAP),
    (15315, "translation_uk", "Веснянки", "веснянки", _CAP),
    (15315, "translation_en", "Freckles", "freckles", _CAP),
    (15315, "translation_tr", "Çiller", "çiller", _CAP),
    (15852, "translation_ru", "Щебетать", "щебетать, чирикать", _CAP),
    (15852, "translation_uk", "Цвірінькати", "цвірінькати, щебетати", _CAP),
    (15852, "translation_en", "Chirp", "to chirp, to tweet",
     "заглавная, и у глагола потеряно «to»"),
    (15852, "translation_tr", "Cıvıldamak", "cıvıldamak", _CAP),
    (16898, "translation_ru", "Порабощать", "порабощать", _CAP),
    (16898, "translation_uk", "Поневолювати", "поневолювати", _CAP),
    (16898, "translation_en", "To enslave", "to enslave", _CAP),
    (16898, "translation_tr", "Köle yapmak", "köle yapmak, esir etmek", _CAP),
    (17389, "translation_ru", "Пассажирское сиденье",
     "пассажирское сиденье", _CAP),
    (17389, "translation_uk", "Пасажирське сидіння",
     "пасажирське сидіння", _CAP),
    (17389, "translation_en", "Passenger seat", "passenger seat", _CAP),
    (17389, "translation_tr", "Yolcu koltuğu", "yolcu koltuğu", _CAP),

    # --- дефекты в тех же рядах ------------------------------------------------
    (9856, "example_tr", "Terazi elmaları tartıyor",
     "Terazi meyveleri tartıyor", "в немецком фрукты, а не яблоки"),
    (16898, "example_tr",
     "Diktatörlük milyonlarca insanı on yıl boyunca köle yaptı",
     "Diktatörlük milyonlarca insanı onlarca yıl köle yaptı",
     "«on yıl» — десять лет; в немецком «für Jahrzehnte», десятилетия"),
    (17389, "example_ru",
     "Мой друг сидел на пассажирском сиденье, пока я вел",
     "Мой друг сидел на пассажирском сиденье, пока я вёл машину",
     "потерянная «ё», и «пока я вел» — вёл что?"),
    (17389, "example_uk",
     "Мій друг сидів на пасажирському сидінні, поки я водив",
     "Мій друг сидів на пасажирському сидінні, поки я вів машину",
     "«водив» — возил вообще, а в немецком вёл именно тогда"),
    (8458, "example_en",
     "It wa's not granted to me to live in this country",
     "It was not granted to me to live in this country",
     "«wa's» — апостроф внутри слова"),
    (8458, "example_pl", "Nie było mi dane tam pojechać",
     "Nie było mi dane żyć w tym kraju",
     "немецкий «in diesem Land zu leben» — жить в этой стране"),

    # --- пустая польская колонка: те самые пять слов --------------------------
    (14805, "translation_pl", "", "klejnoty koronne", _PL),
    (14805, "example_pl", "", "Klejnoty koronne są dobrze pilnowane", _PL),
    (15315, "translation_pl", "", "piegi", _PL),
    (15315, "example_pl", "", "Ma dużo piegów na twarzy", _PL),
    (15852, "translation_pl", "", "ćwierkać", _PL),
    (15852, "example_pl", "", "Ptak ćwierka o poranku", _PL),
    (16898, "translation_pl", "", "zniewalać, ujarzmiać", _PL),
    (16898, "example_pl", "",
     "Dyktatura zniewalała miliony ludzi przez dziesięciolecia", _PL),
    (17389, "translation_pl", "", "fotel pasażera", _PL),
    (17389, "example_pl", "",
     "Mój przyjaciel siedział na fotelu pasażera, kiedy prowadziłem", _PL),
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
