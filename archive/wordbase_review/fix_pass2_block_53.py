"""ВТОРОЙ ПРОХОД, блок 53 (ряды 10401–10600): 32 правки в 24 рядах.

САМЫЙ ПЛОТНЫЙ БЛОК ЗА ДВЕНАДЦАТЬ БЛОКОВ — 12% против полосы 2.5–5%,
в которой проход шёл с блока 48. И это прямое подтверждение правила,
записанного в блоке 46: **дефекты сидят участками, и падение плотности
нельзя читать как «осталось меньше работы».**

Участок польско-украинских подмен, и подмены здесь не мелкие: в десяти
рядах польская или украинская фраза не перевод, а самостоятельное
предложение с тем же словом.

    Punktzahl   (12370) uk «Я НАБРАВ НАЙБІЛЬШЕ ОЧОК У ГРІ»
                     de «Die Punktzahl bei diesem Spiel war sehr niedrig»
    anstehen     (8417) uk «ЗАВТРА ОЧІКУЄТЬСЯ СИЛЬНИЙ ВІТЕР»
                     de «Es stehen wichtige Entscheidungen an»
    Camping      (1303) uk «КЕМПІНГ БУВ ЧУДОВИМ, МИ ПРОВЕЛИ БАГАТО ЧАСУ...»
                     de «Im Sommer machen wir Camping in Italien»
    nachforschen (8413) pl «TRUDNO DOJŚĆ, KTO MIAŁ RACJĘ»
                     de «Der Detektiv musste nachforschen, wer der Täter war»
    Kürzung     (17880) pl «W BUDŻECIE SZKOŁY ZNOWU SĄ CIĘCIA»
                     de «Die Kürzungen im Budget waren unvermeidlich»

ЧЕТЫРЕ ЯЗЫКА ПРОТИВ ЭТАЛОНА — И ПРАВ ОКАЗАЛСЯ НЕ ЭТАЛОН:

    Karawane (17362) de «Die Karawane zog durch die Wüste»
                     en «...through the desert TO EGYPT»
                     ru «...через пустыню В ЕГИПЕТ»
                     uk «...через пустелю В ЄГИПЕТ»
                     tr «...çölün içinden MISIR'A gitti»
                     pl «...przez pustynię»            ← как в немецком

Четыре независимых перевода держат Египет, которого в эталоне нет. Это не
четыре одинаковые ошибки — это след того, что немецкую фразу обрезали.
Поэтому правится НЕМЕЦКИЙ (и польский вслед за ним), а не четыре перевода:
две ячейки вместо четырёх, и версия, которую подтверждают четыре языка.

Это первый случай за проход, когда эталон исправляется ПО переводам, а не
наоборот. Условие, при котором так можно: переводы согласны между собой и
расходятся с эталоном в сторону ДОБАВЛЕНИЯ, а не пропуска.

ОДИН РЯД ПРОТИВ СВОЕГО ЖЕ АРТИКЛЯ (пятый блок подряд этот приём):

    Karnickel (15810) article='das', а пример «DER Karnickel sitzt...»

Девятый гейт этого не поймал, и у него было СЛЕПОЕ ПЯТНО: проверка «der X»
не делалась вовсе, потому что «der» бывает женским дативом. Замер показал,
что при артикле ряда 'die' таких попаданий 137 и все законны («in der
Garage», «an der Wand»), а при артикле 'das' — ровно два, и один из них
законный плюрал-генитив («Die Geschichte der Arbeitslager»). После
ограничения на начало фразы остаётся один дефект. Гейт дополнен.

ТРИ СЛОВА, КОТОРЫХ НЕТ:

 • `Muttersöhnchen` (15290) uk «мамалюбко» — такого слова нет; в списке
   «мамій, мамин синочок».
 • `Duo` (14765) tr «sahnede çıkacak» — направление требует датива,
   «sahneye çıkacak».
 • `voreinander` (8403) uk «один одного» и pl «siebie wzajemnie» —
   взаимное местоимение вместо предложного оборота, который и есть
   заголовок; из-за этого карточка показывала «один перед одним» при
   примере без этих слов.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ эталон правится ПО четырём согласным переводам ═══════════
    (17362, "example_de",
     "Die Karawane zog durch die Wüste",
     "Die Karawane zog durch die Wüste nach Ägypten",
     "en, ru, uk, tr держат Египет — немецкую фразу обрезали"),
    (17362, "example_pl",
     "Karawana ciągnęła przez pustynię",
     "Karawana ciągnęła przez pustynię do Egiptu",
     "вслед за восстановленным эталоном"),

    # ══ артикль примера против артикля ряда ═════════════════════
    (15810, "example_de",
     "Der Karnickel sitzt in seinem Käfig und frisst Karotten",
     "Das Karnickel sitzt in seinem Käfig und frisst Karotten",
     "article='das', а пример говорил «Der»"),

    # ══ подмены целиком ════════════════════════════════════════
    (12370, "example_uk",
     "Я набрав найбільше очок у грі",
     "Кількість очок у цій грі була дуже низькою",
     "«я набрал больше всех» вместо «счёт был очень низким»"),
    (8417, "example_uk",
     "Завтра очікується сильний вітер",
     "Очікуються важливі рішення",
     "ветер вместо «Es stehen wichtige Entscheidungen an»"),
    (8413, "example_pl",
     "Trudno dojść, kto miał rację",
     "Detektyw musiał dochodzić, kto był sprawcą",
     "«трудно выяснить, кто был прав» вместо детектива и преступника"),
    (17880, "example_pl",
     "W budżecie szkoły znowu są cięcia",
     "Cięcia w budżecie były nieuniknione",
     "школьный бюджет вместо «waren unvermeidlich»"),
    (14294, "example_pl",
     "Uroczyście przyrzekł poprawę",
     "Przyrzekł, że nigdy więcej nie skłamie",
     "«обещал исправиться» вместо «nie wieder zu lügen»"),
    (8405, "example_pl",
     "Nie powinieneś odrzucać takiej oferty",
     "Chciał odrzucić tę ofertę",
     "повеление вместо «Er wollte das Angebot ausschlagen»"),
    (8415, "example_tr",
     "Partiden çıkıyor çünkü artık katılmıyor",
     "Dernekten ayrılmak istiyorum",
     "«он выходит из партии, потому что не согласен» вместо «Ich will aus "
     "dem Verein austreten»"),

    # ══ подмена одного слова или части фразы ════════════════════
    (16825, "example_uk",
     "Між кордонами лежала нічия земля",
     "Прикордонний регіон був нічиєю землею між двома країнами",
     "«между границами» вместо «Die Grenzregion ... zwischen den zwei Ländern»"),
    (16825, "example_pl",
     "Między okopami była ziemia niczyja",
     "Region przygraniczny był ziemią niczyją między dwoma krajami",
     "«между окопами» вместо пограничного региона"),
    (8410, "example_pl",
     "Woda w studni była nieczysta",
     "Woda była nieczysta i nie można jej było pić",
     "колодец вместо потерянной второй части «man konnte es nicht trinken»"),
    (8411, "example_pl",
     "Ten stary telefon jest już bezużyteczny",
     "Stare urządzenie stało się całkowicie bezużyteczne",
     "телефон вместо «Das alte Gerät»"),
    (11426, "example_pl",
     "Była zachwycona widokiem z okna",
     "Była zachwycona pięknem krajobrazu",
     "вид из окна вместо «der Schönheit der Landschaft»"),
    (14296, "example_pl",
     "Popieram ten nowy pomysł",
     "Całkowicie popieram tę nową politykę",
     "«идея» вместо «Politik», потеряно «vollständig»"),
    (17878, "example_pl",
     "Na to mieszkanie było wielu zainteresowanych",
     "Na ten dom było wielu zainteresowanych",
     "«mieszkanie» (квартира) вместо «das Haus»"),
    (15290, "example_tr",
     "O tam bir ana kuzusu, çayını bile annesi koyuyor",
     "O tam bir ana kuzusu ve hiçbir şeyi kendi başına yapamıyor",
     "«даже чай ему мама наливает» вместо «kann nichts selbst machen»"),
    (15290, "example_pl",
     "Ten maminsynek nie umie sam gotować",
     "To prawdziwy maminsynek i nie umie nic zrobić sam",
     "«не умеет сам готовить» вместо «nichts selbst machen»"),
    (2889, "example_en",
     "There was a tsunami",
     "The tsunami destroyed the coastal town",
     "фраза обрезана до «there was a tsunami»"),
    (2889, "example_tr",
     "Bir tsunami oldu",
     "Tsunami kıyı kasabasını yıktı",
     "то же обрезание в турецком"),
    (1303, "example_en",
     "We're going camping this weekend",
     "In summer we go camping in Italy",
     "«на этих выходных» вместо «Im Sommer ... in Italien»"),
    (1303, "example_uk",
     "Кемпінг був чудовим, ми провели багато часу на свіжому повітрі",
     "Влітку ми їдемо в кемпінг до Італії",
     "подмена целиком"),
    (1303, "example_tr",
     "Bu hafta sonu kampa gidiyoruz",
     "Yazın İtalya'da kamp yapıyoruz",
     "«на этих выходных» вместо лета и Италии"),

    # ══ слово не из своего списка / выдуманное ══════════════════
    (15290, "example_uk",
     "Він справжній мамалюбко і не може нічого робити самостійно",
     "Він справжній мамій і не може нічого робити самостійно",
     "«мамалюбко» — такого слова нет; в списке «мамій»"),
    (8403, "example_uk",
     "Вони боялися один одного",
     "Вони відчували страх один перед одним",
     "взаимное «один одного» вместо предложного оборота заголовка"),
    (8403, "example_pl",
     "Bali się siebie wzajemnie",
     "Czuli strach jeden przed drugim",
     "«siebie wzajemnie» вместо предложного оборота заголовка"),

    # ══ грамматика и время ═════════════════════════════════════
    (14765, "example_tr",
     "Ünlü düet yarın sahnede çıkacak",
     "Ünlü düet yarın sahneye çıkacak",
     "направление требует датива: «sahneye»"),
    (14297, "example_uk",
     "Він мовчки покидав кімнату",
     "Він мовчки покинув кімнату",
     "незавершённый вид при немецком «verließ»"),
    (8416, "example_pl",
     "Pijany mężczyzna chwiał się na nogach",
     "Pijany mężczyzna chwieje się i ledwo stoi",
     "прошедшее при немецком настоящем и потеряно «kann kaum stehen»"),
    (13060, "example_pl",
     "Mam zachrypnięty głos po koncercie",
     "Po koncercie jego głos był zachrypnięty",
     "«у меня» при немецком «seine Stimme»"),

    # ══ добавлено лишнее ═══════════════════════════════════════
    (8412, "example_pl",
     "Możesz pokroić ten papier na pół?",
     "Możesz pokroić ten papier?",
     "«na pół» (пополам) в эталоне нет"),
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
