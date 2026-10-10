"""ВТОРОЙ ПРОХОД, блок 54 (ряды 10601–10800): 13 правок.

ПЛОТНОСТЬ 6.5% ПРОТИВ 12% В БЛОКЕ 53. Участок подмен кончился, и это
видно по характеру правок: ни одной подмены целиком, ни одной
сочинённой фразы. Осталась мелочь двух видов.

ПЕРВЫЙ ВИД — СЛОВО В ПРИМЕРЕ НЕ ИЗ СВОЕГО СПИСКА, и карточка поэтому
показывает не то, что человек читает. Четыре таких ряда:

    indiskret    (11441) uk «неделікатно» при списке «нетактовний, ...»
    splitternackt(13766) tr «tamamen çıplak» при «çırılçıplak»
    erheblich     (8464) tr «ciddi» при «önemli, hatırı sayılır, büyük»
    multipel      (8449) pl «wielokrotne problemy» — по-польски так не
                         говорят; «liczne» стоит в том же списке третьим

Это тот остаток, который примета `scan_shown_sense` и назвала: без знания
языка его не увидеть, потому что структурно всё на месте.

ВТОРОЙ ВИД — ДОБАВЛЕНО ИЛИ ПОТЕРЯНО ОДНО СЛОВО:

    Ärgernis     (11439) pl потеряно «ständige» (постоянный), добавлено
                         «prawdziwe» — а «постоянный шум» есть во всех
                         четырёх остальных языках
    Zehenspitze  (15297) pl «na czubkach palców» без «stóp»: по-польски
                         это кончики ПАЛЬЦЕВ РУК, а речь о пальцах ног
    Drogerie      (9930) en «next door» при «um die Ecke» (за углом)
    beaufsichtigen(9238) uk «на майданчику» без «дитячому»: Spielplatz
                         это детская площадка, а «майданчик» — просто
                         площадка
    Genialität   (11448) en «is remarkable» при «ist wirklich
                         beeindruckend»: потеряно «wirklich»
    unsinnig      (8445) pl добавлено «zupełnie»
    Sketch       (14776) pl «naprawdę» (действительно) вместо «sehr»
    Luftunterstützung (16842) pl «Żołnierze» (солдаты) вместо «Die
                         Truppen» (войска)
    Jurastudium   (9615) pl «Kończy» (заканчивает) вместо «absolviert»

ЧТО Я СОЗНАТЕЛЬНО НЕ ТРОНУЛ, хотя заметил:

 • `Dienstboten` (9239) de «In älteren Zeiten» — не идиоматично,
   нормальное немецкое «In früheren Zeiten», и четыре перевода говорят
   именно «в прежние времена». Но правило 1y требует, чтобы переводы
   расходились с эталоном в сторону ДОБАВЛЕНИЯ; здесь они просто
   естественнее, а эталон не неверен. Не повод править эталон.
 • `bereinigen` (8457) de «Nach dem bereinigten Konflikt» — неловкое
   причастие вместо «nach der Bereinigung des Konflikts». Та же причина:
   неловко, но не ошибка.
 • `Insassin` (16841) ru и uk потеряли «des Gefängnisses». Немецкому оно
   нужно, потому что «Insassin» значит и заключённую, и пассажирку; в
   русском «заключённая» однозначна, и уточнение лишнее. Это НОРМА
   языка, а не потеря.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ слово в примере не из своего списка ═════════════════════
    (11441, "example_uk",
     "Було неделікатно з її боку це говорити",
     "Було нетактовно з її боку це говорити",
     "«неделікатно» не из списка; «нетактовний» в нём первый"),
    (13766, "example_tr",
     "Bahçede tamamen çıplak duruyordu",
     "Bahçede çırılçıplak duruyordu",
     "«tamamen çıplak» не из списка; «çırılçıplak» в нём первый"),
    (8464, "example_tr",
     "Proje ciddi maliyetlere neden oluyor",
     "Proje önemli maliyetlere neden oluyor",
     "«ciddi» не из списка; «önemli» в нём первое"),
    (8449, "example_pl",
     "Ma wielokrotne problemy w swoim życiu",
     "Ma liczne problemy w swoim życiu",
     "«wielokrotne problemy» по-польски не говорят; «liczne» в списке третье"),

    # ══ потеряно слово, которое есть в эталоне ══════════════════
    (11439, "example_pl",
     "Ten hałas to prawdziwe utrapienie dla sąsiadów",
     "Ciągły hałas to utrapienie dla sąsiadów",
     "потеряно «ständige», добавлено «prawdziwe»"),
    (15297, "example_pl",
     "Tańczyła na czubkach palców",
     "Tańczyła na czubkach palców stóp",
     "без «stóp» это кончики пальцев РУК, а речь о пальцах ног"),
    (9930, "example_en",
     "I buy my toothpaste at the drugstore next door",
     "I buy my toothpaste at the drugstore around the corner",
     "«next door» при «um die Ecke»"),
    (9238, "example_uk",
     "Мати доглядає за дітьми на майданчику",
     "Мати доглядає за дітьми на дитячому майданчику",
     "Spielplatz — детская площадка, «майданчик» просто площадка"),
    (11448, "example_en",
     "The genius of his invention is remarkable",
     "The genius of his invention is really impressive",
     "потеряно «wirklich beeindruckend»"),

    # ══ добавлено лишнее или не то слово ═══════════════════════
    (8445, "example_pl",
     "To zupełnie bezsensowny pomysł",
     "To bezsensowny pomysł",
     "«zupełnie» в «Das ist eine unsinnige Idee» нет"),
    (14776, "example_pl",
     "Ten skecz był naprawdę śmieszny",
     "Ten skecz był bardzo śmieszny",
     "«naprawdę» (действительно) вместо «sehr» (очень)"),
    (16842, "example_pl",
     "Żołnierze poprosili o wsparcie lotnicze",
     "Wojska poprosiły o wsparcie lotnicze",
     "«Żołnierze» (солдаты) вместо «Die Truppen» (войска)"),
    (9615, "example_pl",
     "Kończy studia prawnicze na uniwersytecie",
     "Odbywa studia prawnicze na uniwersytecie",
     "«Kończy» (заканчивает) вместо «absolviert»"),
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
