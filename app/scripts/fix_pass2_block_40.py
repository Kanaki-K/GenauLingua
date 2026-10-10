"""ВТОРОЙ ПРОХОД, блок 40 (ряды 7801–8000): 26 правок.

`kahl` (7923) — ТОТ САМЫЙ РЯД, который примета `scan_shown_sense` назвала
в своём остатке, и он попался в этом блоке сам. Эталон «Der Berg war
völlig kahl, ohne Vegetation», пример «Гора была совсем ГОЛАЯ», а
карточка показывала «ЛЫСЫЙ» — про гору. Нужное слово «голый» в списке
ЕСТЬ, но «голый» и «голая» совпадают лишь на трёх буквах при пороге
основы четыре, и матчер его не видит.

Правлено СО СТОРОНЫ СПИСКА: порядок значений изменён так, чтобы первым
стояло то, о котором пример. Это честно и для словаря: основное значение
`kahl` — «голый, лишённый растительности», а «лысый» — частный случай про
голову. Так же в uk и pl; в en и tr пример и так совпадал.

ПОЧЕМУ НЕ ПРАВЛЕН МАТЧЕР — ЗАМЕР ОТЛОЖЕН, А НЕ ЗАБЫТ. Снизить требование
до трёх букв у коротких основ выглядело прямым продолжением правки блока
39, и улов обнадёживал: 262 ячейки, и в пробе почти везде пример написан
СОВЕРШЕННЫМ видом, а список держит оба («lesen» → «прочитать», «zahlen»
→ «zapłacić», «rutschen» → «poślizgnąć się», «wecken» → «obudzić»). Для
славянских видовых пар это был бы большой выигрыш.

Но замер не выдержал проверки, и провалился он дважды:

    · счёт завышен — условие «показывается первый вариант» выполняется и
      тогда, когда первый вариант СОВПАЛ строго, а не по промаху. То есть
      262 включают ячейки, где поблажка вообще не сработала бы («hä» en:
      «huh» совпадает точно, менять нечего);
    · нашлась порча — `aufeinander` (13511) uk: при примере «одна на
      одній» показалось бы «один за одним» вместо «один на одному»,
      потому что у короткого варианта требование ниже и он побеждает.

Правка матчера за один проход уже сделана (блок 39, 538 ячеек). Делать
вторую на замере, который сам себя не сошёлся, — ровно та поспешность,
против которой весь этот журнал. Замер записан здесь целиком, чтобы
повторить его аккуратно: считать только ячейки с ИСТИННЫМ промахом и
проверить, не затеняет ли короткий вариант длинный.

ШЕСТАЯ ПОЛЬСКАЯ ПОЛОСА ПОДРЯД, и в ней подмена целиком:

    Schluckauf (12860) de «Ich habe Schluckauf nach dem schnellen Essen»
                       pl «Mam czkawkę OD ZIMNEJ WODY»

Плюс `vorstellbar` (7918): в польском списке стояло «pomyślny w myślach»
— это не оборот вовсе («pomyślny» значит удачный), а пример был подменён
целиком. Два дефекта в одном ряду, в переводе и в примере.

ВИД КАРТОЧКИ ПОПРАВЛЕН ЕЩЁ В ПЯТИ РЯДАХ, и все пять — тот же механизм,
что замерен в блоке 39: `Lieblingsfarbe` показывала «en sevilen renk»
при примере «En sevdiğim renk», `Fünfer` — «beşlik» (пятёрка денег) при
примере о школьной оценке, `Törtchen` — «tartolet» при примере про
«kekler», `Besorgung` — «alışveriş» при примере о делах, `Umstand` — при
примере, где слова ряда не было вовсе.

`Aufpasser` (9095) — порядок значений не по делу: эталон «Der Aufpasser
passt auf die Kinder auf» о том, кто присматривает за детьми, а первым
значением стояло «надзиратель» и «наглядач», то есть тюремный. Порядок
исправлен в ru и uk.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ KAHL: ряд из остатка приметы, правлен со стороны списка ══
    (7923, "translation_ru",
     "лысый, голый, оголённый, безлистный",
     "голый, лысый, оголённый, безлистный",
     "пример «Гора была совсем голая», а показывалось «лысый»"),
    (7923, "translation_uk",
     "лисий, голий, оголений, безлистий",
     "голий, лисий, оголений, безлистий",
     "то же: пример «Гора була голою», показывалось «лисий»"),
    (7923, "translation_pl",
     "łysy, nagi, bezlistny, goły",
     "nagi, łysy, bezlistny, goły",
     "то же: пример «Góra była naga», показывалось «łysy»"),

    # ══ шестая польская полоса подряд ═══════════════════════════
    (12860, "example_pl",
     "Mam czkawkę od zimnej wody",
     "Mam czkawkę po szybkim jedzeniu",
     "подмена: от холодной воды вместо «nach dem schnellen Essen»"),
    (7918, "translation_pl",
     "wyobrażalny, możliwy do wyobrażenia, pomyślny w myślach",
     "wyobrażalny, możliwy do wyobrażenia, do pomyślenia",
     "«pomyślny w myślach» не оборот: «pomyślny» значит удачный"),
    (7918, "example_pl",
     "Taki wynik jest całkiem wyobrażalny",
     "Trudno sobie wyobrazić, że zrobił coś takiego",
     "подмена: «такой результат вполне представим» вместо эталона"),
    (7910, "example_pl",
     "Twardość tego kamienia jest niesamowita",
     "Twardość kamienia jest imponująca",
     "«niesamowita» вместо «beeindruckend», и «tego» лишнее"),
    (11874, "example_pl",
     "Kupiłem w sklepie paczkę wędzonych kiełbasek",
     "Kupiłem w supermarkecie paczkę wędzonych kiełbasek",
     "«w sklepie» вместо «im Supermarkt»"),
    (12303, "example_pl",
     "Wygląda wysportowanie i regularnie trenuje",
     "Wygląda wysportowana i regularnie trenuje",
     "«wygląda wysportowanie» не форма: нужен род"),
    (11079, "example_pl",
     "Mówił pewny siebie i przekonująco przed tłumem",
     "Mówił z pewnością siebie i przekonująco przed tłumem",
     "прилагательное на месте наречия: фраза не согласована"),

    # ══ вид карточки: слово не из своего списка ═════════════════
    (11082, "translation_tr",
     "en sevilen renk",
     "favori renk, en sevilen renk",
     "в списке было только страдательное «en sevilen», пример же о своём"),
    (11082, "example_tr",
     "En sevdiğim renk mavi",
     "Favori rengim mavi",
     "«en sevdiğim» нет в списке; «favori renk» теперь есть"),
    (9563, "example_tr",
     "Öğrenci matematik dersinden beş aldı",
     "Öğrenci matematikten zayıf aldı",
     "«beş» давало «beşlik» — пятёрку денег; «zayıf» и есть оценка"),
    (11872, "example_tr",
     "Küçük kekler lezzetli görünüyor ve bir tane yemek istiyorum",
     "Küçük pastalar lezzetli görünüyor ve bir tane yemek istiyorum",
     "«kekler» не из списка; «küçük pasta» в нём есть"),
    (9878, "example_tr",
     "Hâlâ yapacak birkaç işim var",
     "Hâlâ yapacak birkaç günlük işim var",
     "слова ряда в примере не было, показывалось «alışveriş»"),
    (7926, "example_tr",
     "Onun gelmemiş olması çok tuhaftı",
     "Onun gelmemesi durumu çok tuhaftı",
     "`Umstand` потерян целиком: «durum» стоит в списке первым"),
    (11075, "example_tr",
     "Kötü bir şey olacağını hissetmiştim",
     "Kötü bir şey olacağına dair bir önsezim vardı",
     "`Vorahnung` потерян: «önsezi» стоит в списке первым"),
    (11085, "example_uk",
     "Він не вагається відкрито висловлювати свою думку",
     "Він без жодної сором'язливості відкрито висловлює свою думку",
     "слова ряда в примере не было, показывалось «сором'язливість»"),

    # ══ порядок значений не по делу ═════════════════════════════
    (9095, "translation_ru",
     "надзиратель, надсмотрщик, присматривающий",
     "присматривающий, надзиратель, надсмотрщик",
     "эталон о том, кто присматривает за детьми, а не о тюремном"),
    (9095, "translation_uk",
     "наглядач, доглядач, опікун",
     "опікун, доглядач, наглядач",
     "то же"),
    (9095, "example_tr",
     "Gözcü çocuklara göz kulak oluyor",
     "Gözetmen çocuklara göz kulak oluyor",
     "«gözcü» это дозорный; в списке есть «gözetmen»"),

    # ══ значение, которого в списке не было ═════════════════════
    (9880, "translation_ru",
     "в долгах, задолжавший, обременённый долгами",
     "в долгах, задолжавший, обременённый долгами, произошедший по своей вине",
     "у `verschuldet` есть значение «selbst verursacht», в en оно названо"),
    (9880, "example_ru",
     "Из-за неудачных сделок он оказался обременён долгами и обанкротился",
     "Его банкротство произошло по своей вине из-за неудачных сделок",
     "эталон «Sein Bankrott war durch schlechte Geschäfte verschuldet» "
     "о причине, а не о долгах; в uk, tr и pl так и есть"),

    # ══ потерянное и не то слово ════════════════════════════════
    (11076, "example_ru",
     "Его креативность проявилась в его уникальных работах",
     "Его креативность проявилась в уникальных дизайнах",
     "«работах» вместо «Designs»; в uk «дизайнах»"),
    (11874, "example_tr",
     "Süpermarkette bir paket sosis aldım",
     "Süpermarkette bir paket füme sosis aldım",
     "потеряна копчёность: `Knacker` это füme sosis"),
    (7918, "example_tr",
     "Bunun gibi bir şey yaptığı zor tasavvur edilebilir",
     "Böyle bir şey yaptığını tasavvur etmek zor",
     "фраза не согласована: «yaptığı zor tasavvur edilebilir»"),
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
