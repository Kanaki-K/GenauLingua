"""ВТОРОЙ ПРОХОД, блок 12 (ряды 2201–2400): правки глазами и ТРЕТЬЯ
половина класса «род рассказчика» — ПОЛЬСКИЙ.

`jahrelang` (2588): pl «Czeka**ŁAM** na niego latami» при русском «Я
ждал». Польский тоже показывает род в прошедшем, а примета
`scan_speaker_gender` смотрела только русский и украинский. Класс
прожил четыре блока в третьем языке.

По базе: **19 женских форм против 307 мужских** — мужской род здесь
такое же умолчание, как в русском.

Признак у польского ЧИЩЕ русского: первое лицо прошедшего — «-łem»
мужское, «-łam» женское, без исключений. Мешает только то, что на
«-łam» кончается и настоящее время глаголов на «-łać»: `wysyłam`,
`przesyłam`, `odsyłam`, `działam`, `wołam` — это 9 из 19 попаданий.

Отделены они НЕ списком, а проверкой по самой базе: если из слова
получается инфинитив на «-łać», который в польских переводах базы
есть, значит это настоящее время. «wysyłam» → «wysyłać» ✓ отброшено,
«czekałam» → «czekałać» ✗ осталось. После этого 10 попаданий: 6
настоящих, 3 оставлены решением (платье, лак, колготки), 1 ложное —
существительное «chłam» («Ten film to kompletny chłam»).

И ОДНО ИЗ ШЕСТИ — ХУЖЕ РОДА. `Auflauf` (12016): эталон «Zum
Mittagessen kochte **SIE** einen Kartoffelauflauf» — готовила ОНА.
Русский так и написан («она приготовила»), а польский написал «**Na
obiad zrobiłam**» — я приготовила. Это расхождение по ЛИЦУ, и примета
на род нашла его попутно, потому что первое лицо выдало себя
окончанием.

Попутно закрыта недоделка блока 8: там у `verwundert` (11369) я привёл
к мужскому роду русский и украинский, а польского не посмотрел, и
«roześmiałam» осталось. Урок записан в журнал: класс надо сметать по
ВСЕМ языкам, где у него есть признак, а не по тем, с которых начал.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── КЛАСС: род рассказчика в польском ───────────────────────
    (2588, "example_pl",
     "Czekałam na niego latami",
     "Czekałem na niego latami",
     "база пишет рассказчика в мужском роде; эталон рода не показывает"),
    (7295, "example_pl",
     "Nie mogłam nawet patrzeć",
     "Nie mogłem nawet patrzeć",
     "то же; русский рядом в мужском («я не мог»)"),
    (11075, "example_pl",
     "Miałam przeczucie, że stanie się coś złego",
     "Miałem przeczucie, że stanie się coś złego",
     "то же"),
    (11369, "example_pl",
     "Spojrzał na mnie zdziwiony, kiedy nagle się roześmiałam",
     "Spojrzał na mnie zdziwiony, kiedy nagle się roześmiałem",
     "недоделка блока 8: ru и uk привёл к мужскому, польский не посмотрел"),
    (18803, "example_pl",
     "Kupiłam nowy szampon do włosów",
     "Kupiłem nowy szampon do włosów",
     "то же; эталон «Ich kaufe» рода не показывает"),

    # ── расхождение по ЛИЦУ, найденное той же приметой ──────────
    (12016, "example_pl",
     "Na obiad zrobiłam zapiekankę z ziemniaków",
     "Na obiad zrobiła zapiekankę z ziemniaków",
     "эталон «kochte SIE» — готовила она; русский так и написан"),

    # ── добавленное и потерянное слово ──────────────────────────
    (6754, "example_ru",
     "К счастью, моя работа надёжно защищена",
     "К счастью, моя работа защищена",
     "«надёжно» в эталоне нет: «ist zum Glück gesichert»"),
    (1836, "example_uk",
     "Вона носить прикраси",
     "Вона носить гарні прикраси",
     "потеряно «schönen»: в ru, en, tr и pl оно есть"),

    # ── порядок в списке переводов ──────────────────────────────
    (12531, "translation_ru",
     "писать, сходить по-маленькому, мочиться",
     "сходить по-маленькому, мочиться, писать",
     "«писать» первым двусмысленно без ударения: пи́сать или писа́ть"),
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
