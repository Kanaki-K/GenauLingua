"""ВТОРОЙ ПРОХОД, блок 42 (ряды 8201–8400): 13 правок.

ПОЛЬСКАЯ ПОЛОСА ВЕРНУЛАСЬ ПОСЛЕ ОДНОГО ЧИСТОГО БЛОКА — восемь из
тринадцати правок польские, и пять из них подмены. Но вид подмен другой,
и он важнее их числа.

ПОЛЬСКИЙ ПРИМЕР НЕ ОБРЕЗАННЫЙ ПЕРЕВОД, А ДРУГОЕ ПРЕДЛОЖЕНИЕ С ТЕМ ЖЕ
СЛОВОМ:

    Zimt      (11887) de «Ich mag Zimt im Kaffee»
                      pl «DODAJ TROCHĘ cynamonu DO CIASTA»
    Nachttisch(18365) de «Auf meinem Nachttisch liegt ein Buch»
                      pl «OKULARY leżą na szafce nocnej»
    furzen    (15203) de «Er furzte so laut, dass alle lachten»
                      pl «KTO TU pierdział W WINDZIE»
    Diplomat   (9118) de «Der Diplomat verhandelt mit der Regierung»
                      pl «Dyplomata ROZMAWIAŁ Z MINISTREM»
    Turnschuh (13738) de «Ich brauche neue Turnschuhe»
                      pl «KUPIŁEM nowe buty sportowe»

Во всех пяти польская фраза грамматична, уместна и содержит слово ряда —
но она не перевод немецкой. Это уточняет гипотезу о польском: дело не
только в отдельном прогоне, а в том, что **часть польских примеров
СОЧИНЯЛИ по заголовку, не глядя на немецкую фразу**.

ИЗ ЭТОГО ВЫШЛА ПРИМЕТА `scan_pl_comma_clause`, И ОНА НАШЛА ДЕФЕКТ В
БЛОКЕ, КОТОРЫЙ Я УЖЕ ЗАКРЫЛ. Признак структурный, по пунктуации: в
немецком примере есть запятая (значит он из двух частей), а в переводе
запятой нет вовсе. Ограничена ru, uk и pl, потому что у английского и
турецкого отсутствие запятой — норма языка (818 и 843 ряда).

Замер: 16 рядов, половина законна (польский соединяет союзом «i»/«ani»
то, что немецкий делит запятой), восемь дефектов — исправлены сквозной
правкой `fix_pl_comma_clause.py`. Среди них `sinnlos` (11122) — это ряд
8103, блок 41. Я прочёл его глазами и потерю второй части не увидел.

**Вывод, который стоит дороже восьми правок:** структурную примету надо
писать, как только класс УГАДАН, а не когда он наберёт пять случаев.
Глаз пропускает потерю второй части, потому что первая часть переведена
верно и фраза читается гладко.

ОДНА ПОЛНАЯ ПОДМЕНА ВНЕ ПОЛЬСКОГО: `verkörpert` (7979) pl держал «On
uosabia spokój i rozsądek» при эталоне о роли детектива — то есть и в
этом ряду польский сочинил своё.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ польский сочинил своё предложение ═══════════════════════
    (7979, "example_pl",
     "On uosabia spokój i rozsądek",
     "Doskonale wciela się w rolę detektywa w filmie",
     "подмена целиком: эталон о роли детектива в фильме"),
    (11887, "example_pl",
     "Dodaj trochę cynamonu do ciasta",
     "Lubię cynamon w kawie",
     "подмена: «добавь корицы в тесто» вместо «Ich mag Zimt im Kaffee»"),
    (18365, "example_pl",
     "Okulary leżą na szafce nocnej",
     "Na mojej szafce nocnej leży książka",
     "подмена: очки вместо книги, и потеряно «meinem»"),
    (15203, "example_pl",
     "Kto tu pierdział w windzie",
     "Pierdnął tak głośno, że wszyscy się roześmiali",
     "подмена целиком: вопрос про лифт вместо «so laut, dass alle lachten»"),
    (9118, "example_pl",
     "Dyplomata rozmawiał z ministrem",
     "Dyplomata negocjuje z rządem",
     "подмена: разговаривал с министром вместо «verhandelt mit der Regierung»"),
    (13738, "example_pl",
     "Kupiłem nowe buty sportowe do biegania",
     "Potrzebuję nowych butów sportowych do biegania",
     "«купил» вместо «Ich brauche»"),
    (18364, "example_pl",
     "Zostałem na zewnątrz, drzwi się zatrzasnęły",
     "Zostałem zatrzaśnięty na zewnątrz, zapomniałem klucza",
     "потерян ключ: эталон «hab meinen Schlüssel vergessen»"),
    (11167, "example_pl",
     "Przepraszam nie chciałem cię obrazić",
     "Nie chciałem cię obrazić",
     "«Przepraszam» в эталоне нет, и запятой при нём не стояло"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (9567, "example_pl",
     "Uczennica nosi uniform",
     "Uczennica nosi mundurek",
     "«uniform» по-польски военная форма; школьная — «mundurek»"),
    (18365, "example_tr",
     "Gece masasının üzerinde bir kitap var",
     "Başucu masamın üzerinde bir kitap var",
     "«gece masası» не из списка; «başucu masası» в нём есть"),

    # ══ форма, которой в языке нет ══════════════════════════════
    (12898, "example_uk",
     "Стоматолог зробив мені знеболення перед сверлінням",
     "Стоматолог зробив мені знеболення перед свердлінням",
     "«сверління» русский корень; по-украински «свердління»"),
    (14667, "example_tr",
     "O, görgülü tarzı ve iyi davranışa sahiptir",
     "Görgülü tavırları ve iyi davranışları var",
     "«görgülü tarzı ... sahiptir» не согласовано; `Manieren` — «tavırlar»"),
    (8002, "example_tr",
     "Çocuğun davranışı garip ve bizi hepimizi şaşırttı",
     "Çocuğun davranışı garipti ve hepimizi şaşırttı",
     "«bizi hepimizi» удвоение дополнения"),
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
