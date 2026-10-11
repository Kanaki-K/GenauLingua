"""ТРЕТИЙ ПРОХОД, блок 9 (ряды 1601–1800): 12 заголовков по всей базе.

ГЛАЗАМИ В БЛОКЕ — НИ ОДНОЙ ПРАВКИ. ЗАМЕР ПО ОДНОМУ РЯДУ ДАЛ 16 ДЕФЕКТОВ,
И ТРИ ИЗ НИХ ЛЕЖАЛИ В КУЧЕ ВЛАДЕЛЬЦА КАК «РЕШЕНИЯ», КОТОРЫХ ТАМ НЕ БЫЛО.

Зацепка — ряд 1758, `das Folgendes` (6632). По-немецки субстантивированное
прилагательное после ОПРЕДЕЛЁННОГО артикля берёт слабое окончание «-e»:
«das Folgende», «der Angestellte». Сильное «-es»/«-er» стоит только без
артикля или при неопределённом («ein Angestellter», «Folgendes sage ich»).
То есть «das Folgendes» неграмотно в любом чтении, и ученик видит это на
карточке.

════════════════════════════════════════════════════════════════════════
ЗАМЕР, И ОШИБКА В ПЕРВОМ ПОДХОДЕ, СТОИВШАЯ 15 РЯДОВ
════════════════════════════════════════════════════════════════════════

Правило замера: взять существительные на «-es»/«-er», отсечь последнюю
букву (сильное окончание) и поискать получившуюся слабую форму В ЕГО ЖЕ
НЕМЕЦКОМ ПРИМЕРЕ при артикле. Если пример пишет «der Angestellte», а
заголовок — «der Angestellter», ряд спорит сам с собой.

**Первый прогон дал 3 попадания, и это была моя ошибка.** В регулярном
выражении я перечислил артикли строчными — «der|die|das|dem|den|des» — и
искал РЕГИСТРОЗАВИСИМО. А немецкий пример почти всегда НАЧИНАЕТСЯ с
подлежащего, то есть с «Der Angestellte…» с большой буквы. Правило
отсекало ровно те ряды, ради которых писалось.

    регистрозависимо:    3 попадания
    регистронезависимо: 18 попаданий
    прибавка:           15

Это третий случай за проходы, когда условие замера молча съедало сигнал
(ср. «только один язык промахнулся» в `scan_pl_comma_clause` и границы
слова в замере «viel zu»). **Правило: написав условие отбора, проверь его
на ряде, который ты уже знаешь как дефектный. Если известный дефект не
попал — условие неверно, а не база чиста.**

ИЗ 18 ПОПАДАНИЙ 16 ДЕФЕКТОВ И 2 СОВПАДЕНИЯ:

    Kutscher (8975)  «Der Kutscher fährt die Kutsche» — «Kutsche» это
        другое слово, а не слабая форма «Kutscher»
    Mieter  (18251)  «Der Mieter zahlt die Miete» — то же самое

Оба — пары «действующее лицо и его предмет», и правило ловит их случайно.

════════════════════════════════════════════════════════════════════════
ПОЧЕМУ ПЕРЕИМЕНОВАНО 12, А НЕ 16: РЕШИЛА СХЕМА БАЗЫ
════════════════════════════════════════════════════════════════════════

На `words` висит УНИКАЛЬНЫЙ индекс `uq_words_word_de_level (word_de,
level)`. Для пяти рядов слабая форма на их уровне УЖЕ ЗАНЯТА — то есть в
базе рядом стоит правильно написанный близнец, и база сама это говорит:

    Angeklagter   (16976, B2) ← занято 16193 der Angeklagte   B2
    Angestellter   (8946, B2) ← занято  8879 die Angestellte  B2
    Beamter        (8921, B2) ← занято  8892 der Beamte       B2
    Freiwilliger  (11130, B1) ← занято  2480 der Freiwillige  B1
    Gefangener    (16071, B1) ← занято 16018 der Gefangene    B1

Эти пять — не правка текста, а УДАЛЕНИЕ РЯДА, и удаление рядов решает
владелец: счёт 12902 держит гейт целостности, а на `words.id` ссылается
`user_words`. Они вынесены в кучу владельца отдельным списком.

**Отдельно стоит записать про `die Angestellte` (8879).** Немецкий пишет
мужскую и женскую субстантивированную форму ОДИНАКОВО: «der Angestellte»
и «die Angestellte». Уникальный индекс артикль не учитывает, поэтому
законную пару родов база физически не вмещает на одном уровне. Это не
дефект текста, а ограничение схемы, и владельцу стоит про него знать.

ТРИНАДЦАТЬ ПЕРЕИМЕНОВАНИЙ. Все — сильное окончание на слабое, и у
одиннадцати правильная форма стоит в ИХ ЖЕ немецком примере (правило 1аь:
когда заголовок и пример расходятся, сперва решают, кто прав; здесь прав
пример). Двенадцатый — `Folgendes` (6632), где пример пишет форму без
артикля, и выбор задан не примером, а собственным прецедентом базы: `das
Nützliche` (7714) — тот же разряд слова, то же слабое окончание.

Тринадцатый — `Angehöriger` (15334), и он особый: его пример «**Ein**
Angehöriger der Familie war im Krieg gefallen» ВЕРЕН, потому что после
НЕОПРЕДЕЛЁННОГО артикля сильное окончание и нужно. Спорит не пример с
заголовком, а заголовок сам с собой: «der» требует «-e», а написано
«-er». Двух выходов тут нет — неопределённого артикля в поле `article`
база не знает (все 7250 существительных стоят с der/die/das), значит
словарная форма одна: «der Angehörige».

ЧТО ЭТО МЕНЯЕТ У ПРИМЕТ. Класс ПЕРЕЕХАЛ из одного сторожа в другой:
раньше эти ряды были «словоформенными близнецами» (`scan_inflected_twin`,
связь «-er»), теперь шесть из них — ряды с ОДИНАКОВЫМ заголовком и разным
уровнем (`scan_same_headword`). Остатки обеих примет сдвинуты и разобраны
в их докстрингах.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

WHY = "сильное окончание после определённого артикля; слабая форма — в его же примере"
WHY_PRECEDENT = "сильное окончание после определённого артикля; прецедент базы — das Nützliche"
WHY_INDEFINITE = "в примере «ein Angehöriger» окончание верно; неверен артикль заголовка"

FIXES: list[tuple[int, str, str, str, str]] = [
    (16322, "word_de", "Abgeordneter", "Abgeordnete", WHY),
    (9582, "word_de", "Gelehrter", "Gelehrte", WHY),
    (16987, "word_de", "Gesandter", "Gesandte", WHY),
    (16890, "word_de", "Geschworener", "Geschworene", WHY),
    (9644, "word_de", "Intellektueller", "Intellektuelle", WHY),
    (16796, "word_de", "Kongressabgeordneter", "Kongressabgeordnete", WHY),
    (16940, "word_de", "Kriegsgefangener", "Kriegsgefangene", WHY),
    (16642, "word_de", "Polizeibeamter", "Polizeibeamte", WHY),
    (8475, "word_de", "Unmögliches", "Unmögliche", WHY),
    (16164, "word_de", "Verdächtiger", "Verdächtige", WHY),
    (8861, "word_de", "Vorsitzender", "Vorsitzende", WHY),
    (6632, "word_de", "Folgendes", "Folgende", WHY_PRECEDENT),
    (15334, "word_de", "Angehöriger", "Angehörige", WHY_INDEFINITE),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    seen: set[tuple[int, str]] = set()
    dupes: list[tuple[int, str]] = []
    clashes: list[tuple[int, str, str]] = []
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
                continue
            # уникальный индекс (word_de, level): проверяем ДО записи
            if col == "word_de":
                taken = conn.execute(text(
                    "SELECT id FROM words WHERE word_de = :w AND level = "
                    "(SELECT level FROM words WHERE id = :i) AND id <> :i"
                ), {"w": now, "i": wid}).scalar()
                if taken:
                    clashes.append((wid, now, f"занято id={taken}"))
                    continue
            ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")
    for wid, now, why in clashes:
        print(f"СТОЛКНОВЕНИЕ id={wid} -> {now!r}: {why}")

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
