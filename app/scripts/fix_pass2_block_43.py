"""ВТОРОЙ ПРОХОД, блок 43 (ряды 8401–8600): 8 правок.

САМЫЙ ЧИСТЫЙ БЛОК ЗА ПРОХОД — 8 правок на 200 рядов, 4%. Польских правок
НИ ОДНОЙ: полоса оборвалась второй раз за три блока.

СЕДЬМОЙ ГЕЙТ, НАПИСАННЫЙ В ТОТ ЖЕ ЧАС. Ряд `Bewunderer` (11188) держал
турецкий пример «**d**ünyanın her yerinde birçok hayranı var» — со
строчной буквы. Опечатка, которой не видит ни одна другая примета:
грамматика цела, слово ряда на месте, смысл верен.

По правилу из блока 42 («признак не требует знания языка — пиши примету
сразу») замер сделан немедленно, а не после второго случая. Вышел
`scan_lowercase_start.py` — ГЕЙТ, потому что ни один из шести языков не
начинает предложение со строчной, то есть законного остатка у правила нет
вовсе.

**Первое правило было слишком широким, и замер это показал.** «Первая
БУКВЕННАЯ литера строчная» даёт 22 попадания, из них 21 законно: фраза
начинается с ЦИФРЫ, и следующее слово строчное по правилам языка («5.
sınıftayım», «50 euro za pizzę? To kompletnie przesadzone»). Во всех этих
рядах и немецкий эталон начинается с цифры. Правило сужено до «ПЕРВЫЙ
символ — строчная буква», остаток стал ровно 1.

ЗАМЕР, КОТОРЫЙ ОТМЕНЁН, НО ДАЛ ТРИ ПРАВКИ. Я проверял признак «немецкий
эталон от первого лица, а перевод — нет»: 3901 ряд с первым лицом в
немецком, промахов pl 1205, tr 1081, uk 133, ru 117, en 33.

Правило мерит НЕ БАЗУ, А МОЙ ЖЕ РЕГЕКСП: польский и турецкий бросают
местоимение, потому что лицо держится в окончании глагола («Wyjmuję
pranie», «başvurumu onayladı»), и это норма, а не потеря. Выписать все
личные окончания двух языков — то самое перечисление, которое за проход
шесть раз покрывало только себя. Правило отменено.

Но при чтении его улова нашлись **три украинские подмены целиком**,
которых не видит ни одна примета, потому что слово ряда в них стоит:

    überkommen (8570) de «Mich überkam plötzlich große Angst»
                      uk «ХВИЛЯ СМУТКУ охопила ЇЇ, коли вона почула
                          цю новину»
    benötigen  (2269) de «Ich benötige dringend Hilfe»
                      uk «ДІТИ потребують УВАГИ БАТЬКІВ»
    pingelig  (11424) de «Mein Chef ist echt pingelig, wenn es um die
                          Formatierung geht»
                      uk «ВІН дуже привередливий У ЇЖІ»

Это первый случай за проход, когда подмены целиком нашлись в УКРАИНСКОМ
россыпью. До сих пор украинский являлся в тройках en+uk+tr, а подмены
целиком были польской чертой. Записано как наблюдение; если повторится,
нужен замер по украинскому отдельно.

Плюс «привередливий» в том же ряду — русизм, по-украински «вибагливий»,
и оно стоит в списке ряда вторым.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ строчная буква в начале фразы — новый гейт ══════════════
    (11188, "example_tr",
     "dünyanın her yerinde birçok hayranı var",
     "Dünyanın her yerinde birçok hayranı var",
     "предложение не может начинаться со строчной"),

    # ══ украинские подмены целиком, из отменённого замера ═══════
    (8570, "example_uk",
     "Хвиля смутку охопила її, коли вона почула цю новину",
     "Мене раптом охопив великий страх",
     "подмена целиком: волна грусти у неё вместо «Mich überkam … Angst»"),
    (2269, "example_uk",
     "Діти потребують уваги батьків",
     "Я терміново потребую допомоги",
     "подмена целиком: дети и внимание вместо «Ich benötige dringend Hilfe»"),
    (11424, "example_uk",
     "Він дуже привередливий у їжі",
     "Мій начальник дуже вибагливий, коли йдеться про форматування",
     "подмена целиком, и «привередливий» русизм: в списке «вибагливий»"),

    # ══ слово не из своего списка ══════════════════════════════
    (8027, "example_uk",
     "Курс для тих, хто вже має підготовку",
     "Курс для тих, хто має високий рівень",
     "слова ряда в примере не было, показывалось «поглиблений»"),
    (8034, "example_tr",
     "Köyü bir veba kasıp kavurdu",
     "Köyü bir veba felakete uğrattı",
     "«kasıp kavurmak» не из списка; «felakete uğratmak» в нём есть"),

    # ══ форма, которой в языке нет ═════════════════════════════
    (17294, "example_tr",
     "O eski mopedi ile işe gidiyor",
     "Eski mopediyle işe gidiyor",
     "«mopedi ile» без притяжательного суффикса не согласовано"),
    (14675, "example_uk",
     "З барабанним дробом директор цирку оголосив наступний номер",
     "Під барабанний дріб директор цирку оголосив наступний номер",
     "«з барабанним дробом» не оборот: «під барабанний дріб»"),
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
