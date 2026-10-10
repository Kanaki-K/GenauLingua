"""ВТОРОЙ ПРОХОД, блок 62 (ряды 12201–12400): 3 правки.

САМЫЙ ЧИСТЫЙ БЛОК ЗА ВЕСЬ ПРОХОД — 1.5%. Безранговый хвост продолжается,
и это весь слой A2: `Biotonne`, `Brandmelder`, `Einwohnermeldeamt`,
`Girokonto`, `Glascontainer`, `Hausordnung`, `Elternabend` — учебная
лексика для жизни в Германии. Подмен целиком нет, грамматика держится,
турецкий впервые за шесть блоков почти чист.

ТРИ ПРАВКИ:

 • `divers` (1336) tr «Cinsiyet ÇEŞİTLİ» — «пол разнообразный». Ряд
   учит третьему варианту в графе «пол», и список это держит
   («cinsiyet belirtiminde üçüncü seçenek»), а пример взял первое
   значение «çeşitli» (различный) и фраза вышла бессмысленной. Остальные
   четыре языка говорят «небинарный».
 • `gesundheitlich` (1485) ru «всё НОРМАЛЬНО» при немецком «geht ihm
   gesundheitlich GUT»; украинский говорит «усе добре».
 • `Einwurfzeit` (1364) uk «Час ПОДАННЯ» не из списка («час приймання
   листів, час виймання з поштової скриньки») — карточка показывала
   «час приймання листів».

ТОТ ЖЕ КАПКАН, ЧТО В БЛОКЕ 58, И ОН ПОПАЛСЯ МНЕ ВТОРОЙ РАЗ. Первая
версия турецкой правки была «Cinsiyet OLARAK üçüncü seçenek seçildi» —
и `scan_shown_sense` после неё упала: 71 → 72. Причина та же, что у
`entbinden` (13136): **`chosen_index` ищет вариант по САМОМУ ДЛИННОМУ
слову**, а в «cinsiyet belirtiminde üçüncü seçenek» это
«belirtiminde» (12 букв) — слова, которого в моей фразе не было.

    «Cinsiyet olarak üçüncü seçenek seçildi»      -> None
    «Cinsiyet belirtiminde üçüncü seçenek seçildi» -> 2

Вывод для продолжающего: **правя пример под многословный вариант списка,
проверь, что в нём есть САМОЕ ДЛИННОЕ слово этого варианта.** Иначе
правка выглядит верной, а карточка продолжает показывать первый вариант.
Дешевле всего проверить прямым вызовом `chosen_index` до записи в базу.

ДВА ФОРМАЛЬНЫХ ЗАМЕЧАНИЯ ИЗВЛЕКАТЕЛЯ — ЛОЖНЫЕ, и это стоит записать.
Впервые за много блоков `wordbase_review_block` сам отметил два ряда:
«латиница в переводе» на «ID-карта / ID-картка» (`Personalausweis`) и
«HR-директор» (`Personalleiter`). Это законные интернационализмы, и гейт
`scan_alien_letter` их пропускает — у него есть на такое отсечка, а
подсказка извлекателя грубее. Подсказка и названа подсказкой.

════════════════════════════════════════════════════════════════════════
КЛАСС НА РЕШЕНИЕ ВЛАДЕЛЬЦА: ЗАГОЛОВОК МУЖСКОЙ, ПРИМЕР В ЖЕНСКОЙ ФОРМЕ
════════════════════════════════════════════════════════════════════════

Заметив `Enkel` → «Meine EnkelIN» и `Englischlehrer` → «Meine
EnglischlehrerIN» рядом, я замерил по всей базе. Признак: заголовок —
существительное мужского рода без слеша, а в примере стоит его форма на
-in.

    1207  Babysitter             A2  «Wir suchen eine Babysitterin»
    1208  Bäckereifachverkäufer  A2  «Sie ist Bäckereifachverkäuferin»
    1379  Englischlehrer         A2  «Meine Englischlehrerin ist nett»
    1380  Enkel                  A2  «Meine Enkelin ist drei Jahre alt»
    1498  Grafiker               A2  «Sie ist Grafikerin»
    1591  Klassenlehrer          A2  «Meine Klassenlehrerin ist nett»
    2021  Vegetarier             A2  «Ich bin Vegetarierin»

Семь рядов, ВСЕ A2, все в этом же учебном слое. И `Vegetarier` (2021)
уже лежит в куче решений владельца — то есть замер обобщил известный
единичный случай в названный класс.

ПОЧЕМУ Я ЭТО НЕ ПРАВЛЮ. Решений два, и оба мимо моей границы:

 (а) Сделать пример мужским («Wir suchen einen Babysitter»). Но в
     нескольких рядах переводы тоже женские («Моя учительница
     английского», «Моей внучке»), так что правка — 5–6 ячеек на ряд,
     около 35 всего, и она СТИРАЕТ женскую форму из слоя, который
     женские формы учит нарочно.

 (б) Переименовать заголовок в слеш-форму: `Babysitter/in`. Это РОВНО
     соглашение самого слоя — в нём десятки таких рядов
     (`Kassierer/in`, `Koch/Köchin`, `Dieb/in`, `Nachbar/in`,
     `Lehrer/in`, `Kunde/Kundin`, `Krankenpfleger/Krankenschwester`).
     Похоже, в этих семи слеш просто забыли.

Вариант (б) правильный, но это переименование ряда — состав базы, а не
текст. Поэтому класс идёт владельцу: семь рядов названы, оба варианта
описаны, рекомендация — (б), одна ячейка `word_de` на ряд.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (1336, "example_tr",
     "Cinsiyet çeşitli",
     "Cinsiyet belirtiminde üçüncü seçenek seçildi",
     "«çeşitli» (различный) вместо третьего варианта в графе «пол»; "
     "слово «belirtiminde» обязательно — см. докстринг"),
    (1485, "example_ru",
     "По здоровью у него всё нормально",
     "По здоровью у него всё хорошо",
     "«нормально» при немецком «geht ihm gesundheitlich GUT»"),
    (1364, "example_uk",
     "Час подання до 18-ї години",
     "Час приймання листів — до 18-ї години",
     "«час подання» не из списка; «час приймання листів» в нём первое"),
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
