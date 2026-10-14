"""ТРЕТИЙ ПРОХОД, блок 1 (ряды 1–200): 16 ячеек в 6 рядах.

ЗАЧЕМ ТРЕТИЙ ПРОХОД И ПОЧЕМУ ТОЛЬКО 14 БЛОКОВ. Решение владельца, принятое
по замеру после второго прохода: сплошной третий не окупается (поздние
блоки дают 1,5–3%), но блоки 1–14 второго прохода читались, когда примет
было 19, а гейтов 5, тогда как последние блоки — при 47 и 9. Замер в этой
ранней зоне дал 14% рядов с замечанием. И ровно эта зона — самые частые
слова базы, потому что порядок чтения совпадает с порядком частотности.
Самое читаемое оказалось прочитано самым слабым набором правил.

Блок 1 — это первые двести слов по частоте: `ich`, `sein`, `haben`,
`nicht`, артикли, предлоги, модальные глаголы. Почти всё здесь A1, и
почти всё — служебные слова, у которых перевод не «слово за слово», а
пояснение («определённый артикль», «безличное подлежащее»). Это слой, где
ошибку видит каждый пользователь в первую неделю.

════════════════════════════════════════════════════════════════════════
ДВА РЯДА ПРОЖИЛИ ОБА ПРОХОДА: ВОПРОС БЕЗ ЗНАКА ВОПРОСА, В ШЕСТИ ЯЗЫКАХ
════════════════════════════════════════════════════════════════════════

    Na  (13810, A1)  de «Na, wie geht's dir denn»     en «Well, how are you doing»
                     ru «Ну, как дела»                uk «Ну, як справи»
                     tr «Ee, nasılsın»               pl «No, jak się masz»

    Tja (13835, A1)  de «Tja, was soll ich sagen»     en «Well, what can I say»
                     ru «Ну, что тут сказать»         uk «Ну, що мені сказати»
                     tr «Ee, ne diyeyim»             pl «No cóż, co mam powiedzieć»

Двенадцать ячеек, и все двенадцать — вопрос без знака. Норма в базе задана
и однозначна: `Moin` (14207) «Moin, wie geht's dir denn?», `hallo` (370)
«Hallo, wie geht's dir?», `wie` (1035) «Wie geht's dir?». Три ряда со
знаком против двух без.

ПОЧЕМУ ЭТО НЕ НАШЛОСЬ ЗА ДВА ПРОХОДА. Примета была — `scan_question_mark`
ищет вопросительное слово в начале немецкой фразы. Но искала она его
строго по якорю `^`, а МЕЖДОМЕТИЕ С ЗАПЯТОЙ его прятало. Дыра ровно в
одном символе шаблона, и она прожила 137 блоков чтения.

Замер перед правкой приметы: «W-слово в начале фразы, можно после
междометия, и знака нет нигде» даёт по базе 5 попаданий. Три законные:
восклицания `Zufall` (6464) «Was für ein Zufall!» и `Schweinerei` (10744),
плюс оборот «что касается» — `anbelangen` (8250) «Was die Bezahlung
anbelangt, …». **Обе отсечки в примете УЖЕ БЫЛИ.** То есть дыра была одна,
и закрылась она снятием ведущего междометия, а не новым списком.

Примета заодно сделана ГЕЙТОМ: после этой правки она чиста по всем трём
своим ведрам по всей базе, правило формальное и от языка не зависит.
Десятый гейт.

════════════════════════════════════════════════════════════════════════
ОСТАЛЬНЫЕ ЧЕТЫРЕ ПРАВКИ
════════════════════════════════════════════════════════════════════════

 • `haben` (366) tr список «sahip olmak, var olmak, -MASI VAR». Третий
   вариант не по-турецки вовсе — это обрывок аффикса, а не слово.
   Русский и украинский в том же месте дают пояснение: «вспомогательный
   глагол для прошедшего времени» / «допоміжне дієслово минулого часу».
   По-турецки это «geçmiş zaman yardımcı fiili». Ряд ранга 30.

 • `wird` (13266) pl список «stawać się, zostać» — а польский ПРИМЕР
   этого ряда «Jutro BĘDZIE zimno», и варианта «będzie» в списке нет.
   Карточка показывала «stawać się» при примере про «będzie».
   `scan_shown_sense` показывала на этот ряд всё время: он был одним из
   71 задокументированного остатка, и в других четырёх языках пример
   указывал на ВТОРОЙ вариант, который у поляка отсутствовал. Близнец
   `wirst` (13310) «będzie» в списке ИМЕЕТ — правило 1r в чистом виде.
   Остаток приметы после правки 71 → 70.

 • `davon` (13315) ru «Я купил пиццу и уже съел половину» — слова,
   которому учит ряд, в русском примере НЕТ. Остальные четыре языка его
   держат: en «half of IT», uk «з'їв З НЕЇ половину», pl «zjadłem już Z
   NIEJ połowę», tr «ONDAN yarısını». Добавлено «от неё».

 • `zwei` (13302) pl «POTRZEBUJĘ DWIE bułki» — `potrzebować` требует
   родительного падежа, а стоял винительный. Норма базы подавляющая:
   около ста сорока рядов с «potrzebuję», и все родительным — «potrzebuję
   pomocy», «potrzebuję mąki», и даже точный двойник этой конструкции,
   `Eier` (11638) «Potrzebuję TRZECH JAJEK».

   Правка написана не «Potrzebuję dwóch bułek», а «POPROSZĘ dwie bułki»,
   и причина не в грамматике. Форма «dwóch» в списке ряда отсутствует
   («dwa, dwie, dwoje»), и карточка стала бы показывать «dwa» при примере
   про «dwóch» — то есть падежная правка породила бы дефект вида
   карточки. «Poproszę dwie bułki» — это ровно то, что поляк говорит в
   булочной, винительный при «poprosić» верен, форма «dwie» остаётся на
   месте, и немецкое «Ich brauche zwei Brötchen, bitte» передано тем же
   речевым действием. Проверено: `chosen_index` остаётся на 1.

ПРОВЕРКА `chosen_index` ДО ЗАПИСИ (правило 1ао):

    13266 pl  None -> 2   (ровно то, чего добивались)
      366 tr  None -> None
    13315 ru  None -> None
    13302 pl     1 -> 1
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # --- Na (13810): вопрос без знака во всех шести языках
    (13810, "example_de", "Na, wie geht's dir denn",
     "Na, wie geht's dir denn?", "вопрос без знака вопроса"),
    (13810, "example_en", "Well, how are you doing",
     "Well, how are you doing?", "вопрос без знака вопроса"),
    (13810, "example_ru", "Ну, как дела",
     "Ну, как дела?", "вопрос без знака вопроса"),
    (13810, "example_uk", "Ну, як справи",
     "Ну, як справи?", "вопрос без знака вопроса"),
    (13810, "example_tr", "Ee, nasılsın",
     "Ee, nasılsın?", "вопрос без знака вопроса"),
    (13810, "example_pl", "No, jak się masz",
     "No, jak się masz?", "вопрос без знака вопроса"),
    # --- Tja (13835): то же
    (13835, "example_de", "Tja, was soll ich sagen",
     "Tja, was soll ich sagen?", "вопрос без знака вопроса"),
    (13835, "example_en", "Well, what can I say",
     "Well, what can I say?", "вопрос без знака вопроса"),
    (13835, "example_ru", "Ну, что тут сказать",
     "Ну, что тут сказать?", "вопрос без знака вопроса"),
    (13835, "example_uk", "Ну, що мені сказати",
     "Ну, що мені сказати?", "вопрос без знака вопроса"),
    (13835, "example_tr", "Ee, ne diyeyim",
     "Ee, ne diyeyim?", "вопрос без знака вопроса"),
    (13835, "example_pl", "No cóż, co mam powiedzieć",
     "No cóż, co mam powiedzieć?", "вопрос без знака вопроса"),
    # --- остальные четыре
    (366, "translation_tr",
     "sahip olmak, var olmak, -ması var",
     "sahip olmak, var olmak, geçmiş zaman yardımcı fiili",
     "«-ması var» не по-турецки; ru и uk в том же месте дают "
     "пояснение «вспомогательный глагол прошедшего времени»"),
    (13266, "translation_pl",
     "stawać się, zostać",
     "stawać się, zostać, będzie",
     "польский пример ряда «Jutro będzie zimno» использует вариант, "
     "которого в списке не было; близнец `wirst` (13310) его имеет"),
    (13315, "example_ru",
     "Я купил пиццу и уже съел половину",
     "Я купил пиццу и уже съел от неё половину",
     "слова ряда `davon` в русском примере нет вовсе, остальные "
     "четыре языка его держат"),
    (13302, "example_pl",
     "Potrzebuję dwie bułki, proszę",
     "Poproszę dwie bułki",
     "`potrzebować` требует родительного (норма базы — ~140 рядов); "
     "выбран «poproszę», чтобы сохранить форму «dwie» из списка"),
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
