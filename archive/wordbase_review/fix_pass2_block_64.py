"""ВТОРОЙ ПРОХОД, блок 64 (ряды 12601–12800): 4 правки.

Весь блок — один слой: безранговый хвост, уровень B1, лексика взрослой
жизни в Германии. Авиация (`Bordkarte`-окружение: `Fluggast`, `Gate`,
`Gepäckband`, `Passkontrolle`, `Pilotenstreik`), страхование
(`Haftpflicht`, `Kaskoversicherung`, `Personenschaden`, `Sachschaden`),
почта и возвраты (`Nachnahme`, `Retoure`, `Retourenschein`,
`Rücksendung`, `Porto`), экология (`Abgas`, `Schadstoff`, `Sondermüll`,
`Sperrmüll`, `Klimawandel`), история (`Nachkriegszeit`,
`Nationalsozialismus`, `Staatsgründung`). Немецкие эталоны чистые,
подмен целиком нет, формальных замечаний извлекателя — НОЛЬ из 200.

ЧЕТЫРЕ ПРАВКИ, и три из них — в ячейке СПИСКА, а не примера. Это редкий
расклад: обычно блок даёт правки примеров. Здесь примеры в порядке, а
подвели три перевода-списка.

 • `Kommunikationsstärke` (2616) en «important IN WORK» — не по-английски
   и не по норме базы. Пять других рядов пишут «at work» (`gefordert`
   7499, `managen` 9229, `Schikane` 11515, `Belästigung` 16295,
   `Diskriminierung` 16773); 2616 — единственный выброс.
 • `kommunikativ` (2617) en список «communicative, TO BE COMMUNICATIVE,
   outgoing, sociable» — второй вариант пересказывает первый, добавляя
   связку. В остальных четырёх языках ровно три РАЗНЫХ прилагательных.
   На карточке человек видел одно слово дважды.
 • `Gemüsehändler/in` (2513) pl список «sprzedawca warzyw, WARZYWNIAK».
   `warzywniak` по-польски — ЛАВКА (или огород), а не человек. Ряд о
   человеке, и четыре языка называют человека дважды («greengrocer,
   vegetable seller», «торговец овощами, зеленщик», «продавець овочів,
   зеленяр», «manav, sebze satıcısı»).
 • `Spieler/in` (2836) ru список «игрок, игрок в команде,
   МУЗЫКАНТ-ИСПОЛНИТЕЛЬ». У немецкого `Spieler` значения «музыкант» без
   композита нет; зато есть «играющий на деньги», и его назвали ТРИ
   языка согласно: en «gambler», tr «kumarbaz», pl «hazardzista».
   Правило 1ае в чистом виде: согласие ДОБАВЛЯЕТ, значит список неполон
   и третий вариант занят чужим смыслом.

════════════════════════════════════════════════════════════════════════
ЧЕТЫРЕ ЗАМЕРА, ТРИ ОТМЕНИЛИ КЛАСС (второй блок подряд)
════════════════════════════════════════════════════════════════════════

1. «to ...» В СПИСКЕ НЕГЛАГОЛЬНОГО РЯДА. Увидев `kommunikativ` с «to be
   communicative», я замерил по базе: 54 попадания. И почти все
   законные, потому что примета названа неверно: «to» в них —
   ПРЕДЛОГ, а не частица инфинитива («to me», «to the left», «to that
   place», «to one's advantage»), плюс ряды PHRASE, где «to walk the
   dog» — ровно то, что нужно. Настоящих среди 54 — один, 2617, и он
   дефектен не из-за «to», а потому что ПЕРЕСКАЗЫВАЕТ первый вариант.

   Обратный замер (глагольный ряд, но не все варианты на «to ») дал 25
   попаданий, и все законные: у английских модальных инфинитива нет
   вовсе («may», «can», «will», «should»), а причастия стоят отдельными
   значениями («experienced», «deserted»). База права.

2. ВАРИАНТ ОКАНЧИВАЕТСЯ ДРУГИМ ВАРИАНТОМ ТОГО ЖЕ СПИСКА. Уточнённая
   примета после первого провала: 1508 попаданий («с» ⊂ «начиная с»,
   «training» ⊂ «vocational training», «грудь» ⊂ «женская грудь»). Тот
   же приём базы, что и префиксный вариант из блока 63 (1620), только с
   другим порядком слов. Класса нет — и это, кстати, подтверждает, что
   правка 2836 («игрок» → «азартный игрок») пишется В стиле базы.

3. ОДИН ЯЗЫК ДОБАВИЛ УСИЛИТЕЛЬ, КОТОРОГО НЕТ В НЕМЕЦКОМ. Повод —
   `Gegner/in` (2508) uk «Суперник ДУЖЕ сильний» при «Der Gegner ist
   stark». Замер: 204 ряда, и примерно 120 из них — ТУРЕЦКОЕ «çok».

       de Das Café ist gemütlich        tr Kafe ÇOK rahat
       de Der Kassierer ist freundlich  tr Kasiyer ÇOK nazik
       de Deine Stimme ist schön        tr Sesin ÇOK güzel

   **Турецкий слой вставляет «çok» системно** — это его повадка, а не
   дефект; польский так же поступает с «bardzo» (десятки рядов).
   Украинский ряд 2508 — одиночка в том же приёме, и выделять его было
   бы непоследовательно. Класс отменён, повадка записана в HANDOVER,
   чтобы следующий читатель не «открыл» её заново и не внёс 120 правок.

ОТДЕЛЬНО ОТМЕЧЕНО, НО НЕ ПРАВЛЕНО: uk-список `Spieler/in` (2836) —
«гравець, гравчиня», то есть второй вариант это женская форма первого, а
значения «играющий на деньги» нет вовсе. Это НЕДОСТАЧА, а не поломка:
длина списков по базе разная (en 2, ru 3, pl 3), и дополнять их — не
работа прохода по дефектам.

ПРОВЕРКА `chosen_index` ДО ЗАПИСИ (правило 1ао). Три из четырёх правок
меняют САМ СПИСОК, то есть то, из чего карточка выбирает, — здесь
проверка нужнее всего:

    2616 en  0 -> 0     2617 en  0 -> 0  (список 4 варианта -> 3)
    2513 pl  0 -> 0     2836 ru  0 -> 0
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (2616, "example_en",
     "Good communication skills are important in work",
     "Good communication skills are important at work",
     "«in work» не по-английски; норма базы — «at work», пять рядов"),
    (2617, "translation_en",
     "communicative, to be communicative, outgoing, sociable",
     "communicative, outgoing, sociable",
     "второй вариант пересказывает первый со связкой; в остальных "
     "четырёх языках ровно три разных прилагательных"),
    (2513, "translation_pl",
     "sprzedawca warzyw, warzywniak",
     "sprzedawca warzyw, handlarz warzywami",
     "`warzywniak` — лавка, а не человек; ряд о человеке, и четыре "
     "языка называют человека дважды"),
    (2836, "translation_ru",
     "игрок, игрок в команде, музыкант-исполнитель",
     "игрок, игрок в команде, азартный игрок",
     "у `Spieler` значения «музыкант» нет; значение «играющий на "
     "деньги» согласно назвали en, tr и pl"),
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
