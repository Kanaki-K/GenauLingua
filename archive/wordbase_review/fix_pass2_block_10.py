"""ВТОРОЙ ПРОХОД, блок 10 (ряды 1801–2000): правки, найденные глазами.

Снова низкая плотность — 12 ячеек, как и в блоке 9. Состав тот же:
ранги 3000–3300, конкретные вещи (`Tiger`, `Palast`, `Schokolade`,
`Garage`, `Bär`). Расхождений почти нет.

Самое важное:

    plus (13477)  uk «Два плюс три ДОРІВНЮЄ П'ЯТЬ»
        «Дорівнювати» в украинском требует давального: дорівнює
        П'ЯТИ. Та же ошибка управления, что `verzeihen` в блоке 5, и
        находится так же — только знанием языка. Русский рядом верен
        («равно пять» — там именительный законен), и калька прошла.

    steck (6681)  de «STECKE das Geld in die Tasche»
        Слово ряда — `steck`, усечённая форма, а пример написан полной.
        То есть карточка показывает одно, а читает другое. Замер блока
        4 показал, что голая форма в базе норма (111 против 45), и
        четыре ряда с `Steck` против одного со `Stecke` — так что
        править надо пример, а не слово ряда.

    betreten (2290)  tr «Odaya girmek YASAKTIR»
        Эталон «Du darfst den Raum nicht betreten» — обращение к
        ученику. Турецкий превратил его в безличную табличку
        «вход запрещён». Остальные четыре языка обращаются к человеку.

Рядом стоит ряд, который показывает ОБРАТНОЕ, и потому правке не
подлежит: `berühren` (10253), эталон «Bitte nicht berühren» — это и
есть табличка, инфинитив без лица, и вежливое «не трогайте» в ru, uk и
tr верно. Различие между этими двумя рядами — кому адресована фраза, и
формального признака у него нет.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── ошибка управления ───────────────────────────────────────
    (13477, "example_uk",
     "Два плюс три дорівнює п'ять",
     "Два плюс три дорівнює п'яти",
     "«дорівнювати» требует давального: дорівнює п'яти"),

    # ── слово ряда против примера ───────────────────────────────
    (6681, "example_de",
     "Stecke das Geld in die Tasche",
     "Steck das Geld in die Tasche",
     "слово ряда — усечённое «steck»; в базе голая форма норма, 4 ряда против 1"),

    # ── обращение: табличка вместо человека ─────────────────────
    (2290, "example_tr",
     "Odaya girmek yasaktır",
     "Odaya giremezsin",
     "эталон обращается к ученику, турецкий писал безличный запрет"),

    # ── выбор дальнего варианта ─────────────────────────────────
    (16008, "example_ru",
     "Полиция нашла патроны",
     "Полиция нашла боеприпасы",
     "«боеприпасы» стоит первым, и так в en, tr и pl"),
    (16008, "example_uk",
     "Поліція знайшла патрони",
     "Поліція знайшла боєприпаси",
     "то же"),
    (17078, "example_uk",
     "Гелікоптер летить над нами",
     "Вертоліт летить над нами",
     "«вертоліт» стоит первым, и так в русском"),
    (13914, "example_uk",
     "Радіосигнал не працює",
     "Радіозв'язок не працює",
     "«радіосигнал» нет в списке переводов вовсе"),
    (6672, "example_uk",
     "Можеш визначити чоловіка на фото?",
     "Можеш упізнати чоловіка на фото?",
     "«впізнати» стоит первым; «визначити» это про установление факта"),
    (14970, "example_tr",
     "O takımda genç oyuncu olarak oynuyor",
     "O takımda juniör olarak oynuyor",
     "«genç oyuncu» нет в списке переводов, а «juniör» есть и это слово ряда"),
    (10247, "example_tr",
     "Ev korkunç derecede karanlık",
     "Ev inanılmaz derecede karanlık",
     "«korkunç» нет в списке переводов, а «inanılmaz» есть"),

    # ── потерянное и добавленное слово ──────────────────────────
    (6659, "example_ru",
     "Иди вперёд, я за тобой",
     "Иди вперёд, я пойду за тобой",
     "потерян глагол «folge»: в uk, en, tr и pl он есть"),
    (6640, "example_pl",
     "Możesz na chwilę wyjść na dwór?",
     "Możesz na chwilę wyjść?",
     "«na dwór» в эталоне нет: «Kannst du mal rauskommen?»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
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
