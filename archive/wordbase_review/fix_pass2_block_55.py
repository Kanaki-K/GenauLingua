"""ВТОРОЙ ПРОХОД, блок 55 (ряды 10801–11000): 10 правок.

ПЛОТНОСТЬ 5%, И РАЗБОР ТОТ ЖЕ, ЧТО В БЛОКЕ 54: подмен целиком нет ни
одной, остались слово не из списка и потеря одного слова. Второй блок
подряд после участка — класс работы устойчив, а не случаен.

СЛОВО В ПРИМЕРЕ НЕ ИЗ СВОЕГО СПИСКА, три ряда:

    Ganove   (16852) tr «Hırsız» (вор) при списке «dolandırıcı, haydut,
                     gangster»
    erpicht  (11465) uk «палко бажає» при «охочий, спраглий, падкий»
    vorsehen  (8495) en «to allow for» при «to provide for, to
                     stipulate, to plan»

Во всех трёх карточка показывала первый вариант списка, а человек читал
в примере другое слово.

ГРАММАТИКА ТУРЕЦКОГО, два ряда:

    Überläufer (16855) tr «arkadaşlarını düşmana IHANET etti» —
                       «ihanet etmek» требует датива того, кого предали:
                       «arkadaşlarına ihanet etti». Но тогда теряется
                       «кому выдал». Правильный оборот для «verraten an»
                       — «ele vermek»: «arkadaşlarını düşmana ele verdi».
    Sättigung  (11979) tr «başka bir şey YEMEDIM» (не ел) при немецком
                       «konnte nichts mehr essen» (не мог есть) —
                       потерян модальный глагол: «yiyemedim».

ОСТАЛЬНЫЕ ПЯТЬ — потеря или сдвиг одного слова:

    Einleitung  (9618) pl «Wstęp tej powieści» — по-польски нужно
                       «Wstęp DO tej powieści»; украинский так и говорит
                       («Вступ ДО роману»)
    Gefährt    (17379) pl «już nie jeździ» (настоящее) при «war schon
                       lange nicht mehr zu fahren»
    hellsehen  (14784) pl потерян сам заголовок: немецкий говорит
                       «hellsehen UND die Zukunft vorhersagen», польский
                       оставил только второе, хотя «jasnowidzieć» стоит
                       в его списке первым
    Mopp       (18459) pl «Wezmę ... umyję» (будущее) при немецком
                       «Ich hole ... und wische» (настоящее)
    einschreiten (16859) tr «çatışma» (столкновение) при «Streit»
                       (ссора); ru, uk, pl, en все четыре говорят
                       «ссора»

ЧТО НЕ ТРОНУТО НАРОЧНО — и причина та же, что в правиле 1аб:

 • `Haferflocken` (11981) de «esse ich IMMER», а ru, uk, pl и en «immer»
   потеряли (только tr держит «her zaman»). Четыре языка СОГЛАСНЫ в
   ПОТЕРЕ, а это по правилу 1аб ничего не доказывает против эталона. И
   отдельно: в русском настоящее время само несёт привычность, так что
   потери смысла нет.
 • `gutmütig` (11471) ru потеряло «Mensch», хотя uk и pl держат
   «людиною»/«człowiekiem». «Был очень добродушным» по-русски полно.
 • `Sterblichkeit` (13092) de «Die SterblichkeitsRATE» — заголовок
   внутри композита. Это та же терпимость, что к `Blutgerinnsel` при
   заголовке `Gerinnsel`: слово в примере есть, и все пять переводов
   согласно говорят «уровень смертности».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ слово в примере не из своего списка ═════════════════════
    (16852, "example_tr",
     "Hırsız, aylarca mağazaları soyduktan sonra nihayet tutuklandı",
     "Haydut, aylarca mağazaları soyduktan sonra nihayet tutuklandı",
     "«Hırsız» (вор) не из списка; «haydut» в нём второе"),
    (11465, "example_uk",
     "Він палко бажає поїхати за кордон і познайомитися з новими культурами",
     "Він охочий поїхати за кордон і познайомитися з новими культурами",
     "«палко бажає» не из списка; «охочий» в нём первый"),
    (8495, "example_en",
     "We have to allow for a short break",
     "We have to provide for a short break",
     "«to allow for» не из списка; «to provide for» в нём первое"),

    # ══ грамматика турецкого ═══════════════════════════════════
    (16855, "example_tr",
     "Saf değiştiren, silah arkadaşlarını düşmana ihanet etti",
     "Saf değiştiren, silah arkadaşlarını düşmana ele verdi",
     "«ihanet etmek» требует датива преданного; для «verraten an» — «ele vermek»"),
    (11979, "example_tr",
     "Yemekten sonra çabuk tok hissettim ve başka bir şey yemedim",
     "Yemekten sonra çabuk tok hissettim ve başka bir şey yiyemedim",
     "потерян модальный: «konnte nichts mehr essen» — не МОГ есть"),

    # ══ потеря или сдвиг одного слова ══════════════════════════
    (9618, "example_pl",
     "Wstęp tej powieści był naprawdę wciągający",
     "Wstęp do tej powieści był naprawdę wciągający",
     "по-польски нужно «Wstęp DO»; украинский так и говорит"),
    (17379, "example_pl",
     "Jego stary pojazd już nie jeździ",
     "Jego stary pojazd już dawno nie nadawał się do jazdy",
     "настоящее при «war schon lange nicht mehr zu fahren»"),
    (14784, "example_pl",
     "Niektórzy twierdzą, że potrafią przewidywać przyszłość",
     "Niektórzy twierdzą, że potrafią jasnowidzieć i przewidywać przyszłość",
     "потерян сам заголовок: «hellsehen UND vorhersagen», «jasnowidzieć» в списке первое"),
    (18459, "example_pl",
     "Wezmę mop i szybko umyję podłogę",
     "Biorę mop i szybko myję podłogę",
     "будущее при немецком настоящем «Ich hole ... und wische»"),
    (16859, "example_tr",
     "Polis çatışmayı bitirmek için müdahale etmek zorunda kaldı",
     "Polis kavgayı bitirmek için müdahale etmek zorunda kaldı",
     "«çatışma» (столкновение) при «Streit» (ссора); так в четырёх языках"),
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
