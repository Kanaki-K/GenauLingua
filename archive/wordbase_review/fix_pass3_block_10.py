"""ТРЕТИЙ ПРОХОД, блок 10 (ряды 1801–2000): 36 ячеек в 7 рядах по всей базе.

РОД В НЕМЕЦКОМ — ЭТО ЗНАЧЕНИЕ, А В СПИСКАХ СТОЯЛИ ЗНАЧЕНИЯ ЧУЖОГО РОДА.

Зацепка — ряд 1819, `das Schild` (1829):

    das Schild
        ru  табличка, вывеска, дорожный знак, ЩИТ

«das Schild» — табличка, вывеска, дорожный знак. А щит — это «DER
Schild», другое слово с тем же написанием. Ученик видит артикль «das» и
четвёртым значением «щит»; выучив это, он скажет «das Schild» про щит, и
будет неправ. Для немецкого это хуже опечатки: род несёт значение.

════════════════════════════════════════════════════════════════════════
ПОЧЕМУ ЗДЕСЬ СПИСОК СЛОВ, А НЕ ПРАВИЛО (ИСКЛЮЧЕНИЕ ИЗ ПРАВИЛА 1бв)
════════════════════════════════════════════════════════════════════════

Правило 1бв велит выбирать правило, а не список: «список кончается там,
где кончилось твоё воображение». Здесь — обратный случай, и его стоит
понимать как границу того правила.

Род-различающие омографы — ЗАКРЫТЫЙ лексический список немецкого языка,
он кончается не в моём воображении, а в словаре: `der/das Schild`,
`die/das Band`, `der/die Kiefer`, `die/das Steuer`, `der/das Erbe`,
`der/das Verdienst`, `der/das Bund`, `der/die Leiter`, `der/das Gehalt`,
`der/die Kunde`, `der/das Moment`, `der/die Heide`, `der/die Mangel`,
`der/das Tor`, `der/die Weise`, `der/das Teil`, `der/das Golf`,
`der/das Bauer`. Никакое структурное правило этого знать не может:
написание у пары одинаковое, а разводит их только словарь.

Поэтому инструмент — именно перечисление, и замер сделан по нему:
36 заголовков проверено, 7 рядов с чужим родом в списке, 11 чистых.

ОДИННАДЦАТЬ ЧИСТЫХ, И ЭТО НЕ СЛУЧАЙНОСТЬ. База почти всегда берёт ОДИН
род и не мешает значения:

    die Leiter   (8775)  «лестница, стремянка» — вождя («der Leiter») нет
    das Gehalt   (2509)  «зарплата» — содержания («der Gehalt») нет
    der Kunde    (9753)  «клиент» — вести («die Kunde») нет
    der Moment    (608)  «момент» — фактора («das Moment») нет
    die Heide  (15756)   «пустошь» — язычника («der Heide») нет
    der Mangel  (7030)   «нехватка» — катка для белья («die Mangel») нет
    das Tor    (12106)   «гол, ворота» — глупца («der Tor») нет
    der Bauer   (8781)   «крестьянин, пешка» — клетки («das Bauer») нет

И отдельно `die Weise` (3007) «способ, манера, мелодия»: похоже на
смешение, но НЕТ — «мелодия» тоже женского рода («eine alte Weise»), а
мужское «der Weise» значит «мудрец» и в списке не стоит. Ложная тревога,
разобранная чтением словаря, а не глазом.

════════════════════════════════════════════════════════════════════════
СЕМЬ РЯДОВ, И В ШЕСТИ НЕПРАВ СПИСОК, А В ОДНОМ — АРТИКЛЬ
════════════════════════════════════════════════════════════════════════

В шести рядах пример учит ровно тому роду, что в артикле, значит прав
артикль с примером, а лишние значения надо убрать (правило 1аь):

    das Schild (1829)  «Das Schild ist groß» — вывеска
        убрано: щит / shield / kalkan / tarcza  (= der Schild)
    die Band   (1212)  «Ich spiele in einer Band» — музыкальная группа
        убрано: лента, тесьма, бинт / ribbon, tape, bandage  (= das Band)
    der Kiefer (12638) «Der Zahnarzt untersuchte meinen Kiefer» — челюсть
        убрано: сосна / pine tree  (= die Kiefer)
    die Steuer (1913)  «Ich muss Steuern zahlen» — налог
        убрано: руль, штурвал / steering wheel, helm  (= das Steuer)
    das Erbe   (16042) «Das Erbe ist sehr wertvoll» — наследство
        убрано: наследник / heir  (= der Erbe)
    der Bund   (16249) «Der Bund hat neue Gesetze verabschiedet» — федерация
        убрано: пучок / bunch / demet / pęk  (= das Bund)
        «пояс брюк» ОСТАВЛЕН: «der Hosenbund» мужского рода, это свой

СЕДЬМОЙ РЯД УСТРОЕН НАОБОРОТ. `der Verdienst` (9176, C2):

    de  Seine Verdienste wurden endlich anerkannt     — заслуги
    ru  заслуга, заработок        uk  заслуга, заробіток
    en  merit, earnings           pl  zasługa, zarobek

По Дудену «das Verdienst» — заслуга, «der Verdienst» — заработок. Пример
про заслуги, и ПЕРВЫМ значением заслуга стоит во всех пяти языках —
то есть за средний род голосуют и пример, и шесть списков, а за мужской
только поле `article`. Правится артикль: «der» → «das», и заработок
убирается как чужой род.

ЧТО ЗНАТЬ ВЛАДЕЛЬЦУ. Убранные значения в базе больше НИГДЕ не живут:
ряда `der Schild`, `das Band`, `die Kiefer`, `das Steuer`, `der Erbe`,
`der Verdienst`, `das Bund` нет. То есть база этих слов теперь не учит
вовсе — и это лучше, чем учить их с неверным родом. Если они нужны, им
нужны СВОИ ряды со своим артиклем; добавление рядов — решение владельца.

ЧТО ЕЩЁ ПРОВЕРЕНО В БЛОКЕ И ОСТАВЛЕНО. `Ewigkeit` (18657): турецкий
пример «Seni asırlardır bekliyorum» — «жду тебя веками», а в турецком
списке стоят «sonsuzluk, ebediyet». Слова примера в списке нет, но это
не дефект: немецкое «eine Ewigkeit warten» — идиома, и турецкий берёт
свою идиому вместо калькирования. Английский и польский делают то же
(«ages», «całe wieki»), только у них идиома попала ещё и в список.

В КУЧУ ВЛАДЕЛЬЦА: `steck` (6681) — заголовок в повелительной форме при
pos VERB, словарная форма «stecken»; `die Hunderte` (13479) — пара к
ряду 13476 `hundert`, тот же вид, что `tausend` / `Tausende` из блока 8.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

W_SCHILD = "щит — это «der Schild», другое слово"
W_BAND = "лента и бинт — это «das Band», другое слово"
W_KIEFER = "сосна — это «die Kiefer», другое слово"
W_STEUER = "руль и штурвал — это «das Steuer», другое слово"
W_ERBE = "наследник — это «der Erbe», другое слово"
W_BUND = "пучок — это «das Bund», другое слово; пояс брюк оставлен"
W_VERDIENST = "заслуга — это «das Verdienst»; заработок — «der», и он убран"

FIXES: list[tuple[int, str, str, str, str]] = [
    # --- das Schild (1829): щит принадлежит «der Schild»
    (1829, "translation_en", "sign, signboard, road sign, shield",
     "sign, signboard, road sign", W_SCHILD),
    (1829, "translation_ru", "табличка, вывеска, дорожный знак, щит",
     "табличка, вывеска, дорожный знак", W_SCHILD),
    (1829, "translation_uk", "табличка, вивіска, дорожній знак, щит",
     "табличка, вивіска, дорожній знак", W_SCHILD),
    (1829, "translation_tr", "tabela, levha, trafik işareti, kalkan",
     "tabela, levha, trafik işareti", W_SCHILD),
    (1829, "translation_pl", "tabliczka, szyld, znak drogowy, tarcza",
     "tabliczka, szyld, znak drogowy", W_SCHILD),
    # --- die Band (1212): лента, тесьма, бинт принадлежат «das Band»
    (1212, "translation_en", "band, music group, ribbon, tape, bandage",
     "band, music group", W_BAND),
    (1212, "translation_ru", "группа, музыкальная группа, лента, тесьма, бинт",
     "группа, музыкальная группа", W_BAND),
    (1212, "translation_uk", "гурт, музичний гурт, стрічка, тасьма, бинт",
     "гурт, музичний гурт", W_BAND),
    (1212, "translation_tr", "müzik grubu, kurdele, bant, sargı",
     "müzik grubu", W_BAND),
    (1212, "translation_pl", "zespół, zespół muzyczny, wstążka, taśma",
     "zespół, zespół muzyczny", W_BAND),
    # --- der Kiefer (12638): сосна принадлежит «die Kiefer»
    (12638, "translation_en", "jaw, pine tree", "jaw", W_KIEFER),
    (12638, "translation_ru", "челюсть, сосна", "челюсть", W_KIEFER),
    (12638, "translation_uk", "щелепа, сосна", "щелепа", W_KIEFER),
    (12638, "translation_tr", "çene, çam ağacı", "çene", W_KIEFER),
    (12638, "translation_pl", "szczęka, sosna", "szczęka", W_KIEFER),
    # --- die Steuer (1913): руль и штурвал принадлежат «das Steuer»
    (1913, "translation_en", "tax, steering wheel, helm", "tax", W_STEUER),
    (1913, "translation_ru", "налог, руль, штурвал", "налог", W_STEUER),
    (1913, "translation_uk", "податок, кермо, штурвал", "податок", W_STEUER),
    (1913, "translation_tr", "vergi, direksiyon, dümen", "vergi", W_STEUER),
    (1913, "translation_pl", "podatek, kierownica, ster", "podatek", W_STEUER),
    # --- das Erbe (16042): наследник принадлежит «der Erbe»
    (16042, "translation_en", "inheritance, heritage, heir",
     "inheritance, heritage", W_ERBE),
    (16042, "translation_ru", "наследство, наследие, наследник",
     "наследство, наследие", W_ERBE),
    (16042, "translation_uk", "спадок, спадщина, спадкоємець",
     "спадок, спадщина", W_ERBE),
    (16042, "translation_tr", "miras, kültürel miras, mirasçı",
     "miras, kültürel miras", W_ERBE),
    (16042, "translation_pl", "spadek, dziedzictwo, spadkobierca",
     "spadek, dziedzictwo", W_ERBE),
    # --- der Bund (16249): пучок принадлежит «das Bund»
    (16249, "translation_en",
     "federal government, federation, alliance, bunch, waistband",
     "federal government, federation, alliance, waistband", W_BUND),
    (16249, "translation_ru",
     "федерация, федеральное правительство, союз, пучок, пояс брюк",
     "федерация, федеральное правительство, союз, пояс брюк", W_BUND),
    (16249, "translation_uk",
     "федерація, федеральний уряд, союз, пучок, пояс штанів",
     "федерація, федеральний уряд, союз, пояс штанів", W_BUND),
    (16249, "translation_tr",
     "federasyon, federal hükümet, birlik, demet, pantolon kemeri",
     "federasyon, federal hükümet, birlik, pantolon kemeri", W_BUND),
    (16249, "translation_pl",
     "federacja, rząd federalny, związek, pęk, pasek u spodni",
     "federacja, rząd federalny, związek, pasek u spodni", W_BUND),
    # --- der Verdienst (9176): неправ АРТИКЛЬ, а не список
    (9176, "article", "der", "das", W_VERDIENST),
    (9176, "translation_en", "merit, earnings", "merit", W_VERDIENST),
    (9176, "translation_ru", "заслуга, заработок", "заслуга", W_VERDIENST),
    (9176, "translation_uk", "заслуга, заробіток", "заслуга", W_VERDIENST),
    (9176, "translation_tr", "hizmet, katkı, kazanç", "hizmet, katkı",
     W_VERDIENST),
    (9176, "translation_pl", "zasługa, zarobek", "zasługa", W_VERDIENST),
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
