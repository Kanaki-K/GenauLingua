"""ВТОРОЙ ПРОХОД, блок 51 (ряды 10001–10200): 6 правок.

БЛОК ПОТРАЧЕН НА ТРИ ЗАМЕРА, И ВСЕ ТРИ ОТМЕНИЛИ СВОЮ ГИПОТЕЗУ. Это
записано подробно в журнале; здесь короткое изложение, потому что правок
в блоке мало именно по этой причине.

ЗАМЕР 1 — ОБРАТНАЯ ПОЛОВИНА ПРАВИЛА 1n. В блоке 47 (`zurückdrehen`)
заголовок имел приставку, которой в примере не было, и это оказалось
НЕловимо структурно. Здесь нашлось обратное: `hören` (14274) de «Er hörte
aufmerksam ZU» — заголовок без приставки, а пример учит `zuhören`. Такое
ловится: взять глаголы, чей заголовок без приставки, и посмотреть, не
кончается ли пример отделяемой частицей.

    глаголов без приставки в заголовке: 1179
    из них пример кончается частицей:     44

И класс ОТМЕНИЛСЯ, потому что это НОРМА БАЗЫ, а не дефект: в каждом из 44
рядов СПИСОК уже несёт приставочное значение, и `main_meaning` именно его
и выбирает.

    rutschen (2777) ru «скользить, ПОСКОЛЬЗНУТЬСЯ, ...»  ← ausrutschen
    setzen   (1865) pl «...,  USIĄŚĆ, ...»               ← sich hinsetzen
    drehen   (1337) pl «..., ODWRACAĆ SIĘ»               ← sich umdrehen
    blasen   (7094) ru «дуть, ЗАДУВАТЬ, ...»             ← ausblasen

То есть база сознательно держит простой глагол заголовком, а приставочные
значения — вариантами списка, и пример иллюстрирует одно из них. Контракт
§8 при этом соблюдён: слово заголовка в примере ЕСТЬ, в своей форме.

Отсечённые по дороге ложные попадания стоит назвать: `zeigen` (1070) «Zeig
mir den Weg» попал в выборку потому, что последнее слово «Weg» в нижнем
регистре совпало с частицей «weg». А `murmeln` (14085) «vor sich hin» и
`summen` (15491) «um die Blumen herum» — обороты, а не приставки.

ЗАМЕР 2 — ЕДИНСТВЕННОЕ ИСКЛЮЧЕНИЕ ИЗ 44, и оно правится здесь:

    atmen (47, A1) de «Atme bitte tief EIN»
                   ru [дышать]  «ВДОХНИ, пожалуйста, глубоко»
                   uk [дихати]  «Будь ласка, глибоко ВДИХНИ»

Здесь список приставочного значения НЕ несёт, в отличие от остальных 43.
Карточка показывает «дышать», а пример говорит «Вдохни» — ровно то
расхождение, которое §8 запрещает. У tr, pl и en всё сходится
(«nefes almak» → «nefes al», «oddychać» → «oddychaj», «to breathe» →
«breathe»), поэтому правятся только два списка.

Немецкий я НЕ трогаю: «Atme bitte tief» без приставки звучит оборванно,
нормальные формы — «tief einatmen» или «tief durchatmen». Приставка в
эталоне на месте, значит дополнить надо списки.

ЗАМЕР 3 — ПРОБЕЛ, КОТОРЫЙ ОКАЗАЛСЯ НЕ ПРОБЕЛОМ. `geschmeidig` (8324) uk
показал, что примета «ни одного варианта списка в примере»
(`scan_list_vs_example`) ограничена существительными и прилагательные не
смотрит. Прогон по всей базе ПРАВИЛОМ ПРОДАКШЕНА (`_stem_tail`, а не
`_stem_in_loose`, которым я ошибся с первого раза) дал 374 ряда с тремя и
более языками — и 323 из них ГЛАГОЛЫ вида `essen`, `gehen`, `nehmen`,
`trinken`: в списке инфинитив, в примере спрягённая форма с чередованием
основы. Это ровно тот шум, из-за которого примета и ограничена
существительными. Прилагательных в остатке 16, и `geschmeidig` среди них
НЕ оказался: у него промахивается один язык, а не три. Его нашёл глаз.

ПРАВКИ БЛОКА:

 • `geschmeidig` (8324) uk «грайливо-плавний» — такого слова нет, это
   сочинённое сложение. Плюс пример говорит «граційно», а в списке
   «граційного» не было вовсе, и карточка показывала «гнучкий». Одна
   правка закрывает и выдуманное слово, и расхождение.
 • `Hitzkopf` (11387) pl «MÓJ brat» при немецком «DEIN Bruder» — подмена
   лица; «твой брат» стоит во всех пяти остальных языках. Заодно
   возвращено «echter».
 • `drohen` (16762) pl «Grozi NAM burza» — «нам» в «Ein Gewitter droht»
   нет; взято «nadciągać» из своего же списка.
 • `nachhelfen` (8326) pl потеряно «Manchmal» (иногда), которое есть во
   всех пяти остальных языках.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ выдуманное слово + расхождение вида карточки ════════════
    (8324, "translation_uk",
     "гнучкий, плавний, м'який, грайливо-плавний",
     "гнучкий, плавний, м'який, граційний",
     "«грайливо-плавний» — сочинённое сложение; пример говорит «граційно»"),

    # ══ единственное исключение из 44 рядов замера ══════════════
    (47, "translation_ru",
     "дышать",
     "дышать, вдохнуть",
     "пример говорит «Вдохни», а список нёс только «дышать»"),
    (47, "translation_uk",
     "дихати",
     "дихати, вдихнути",
     "пример говорит «вдихни», а список нёс только «дихати»"),

    # ══ подмена лица ═══════════════════════════════════════════
    (11387, "example_pl",
     "Mój brat to narwaniec, szybko się wścieka",
     "Twój brat to prawdziwy narwaniec, szybko się wścieka",
     "«Mój» при немецком «Dein Bruder»; заодно возвращено «echter»"),

    # ══ добавлено и потеряно ═══════════════════════════════════
    (16762, "example_pl",
     "Grozi nam burza",
     "Nadciąga burza",
     "«nam» в «Ein Gewitter droht» нет; «nadciągać» есть в своём списке"),
    (8326, "example_pl",
     "Musiałem trochę dopomóc szczęściu",
     "Czasem musiałem trochę dopomóc szczęściu",
     "потеряно «Manchmal»; есть во всех пяти остальных языках"),
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
