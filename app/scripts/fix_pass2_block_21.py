"""ВТОРОЙ ПРОХОД, блок 21 (ряды 4001–4200).

ПОДМЕНЫ ИДУТ ПАЧКОЙ В ПОЛЬСКОМ — девять рядов, и все поодиночке, не
тройками, как в блоках 14–19:

    Körperverletzung (16204) pl «Został oskarżony o uszkodzenie ciała»
    verfügbar        (7179)  pl «Ten model nie jest teraz dostępny»
    Küsschen         (10532) pl «Daj mi buziaka na dobranoc»
    Bestrafung       (16206) pl «Kara za kłamstwo była surowa»
    Pakt             (16207) pl «pakt o nieagresji» — которого в эталоне нет
    zerbrechen       (7183)  pl «Uważaj bo szklanka się stłucze»
    Hausarrest       (16214) pl «Dostał tydzień aresztu domowego»
    Vanille          (11825) pl «Poproszę lody o smaku wanilii»

И турецком — четыре:

    durstig  (11732) tr «Çok susamışım, bir bardak su ver»
    rauschen (15526) tr «Rüzgâr bütün gece bacada uğuldadı» — про ВЕТЕР
    belasten (2264)  tr «Sana yük olmak istemiyorum»
    dürfen   (13522) tr третье лицо множественного вместо вежливого «вы»

Все они примерно той же длины, что эталон, — то есть
`scan_length_outlier` их видеть не может, и это ещё раз подтверждает
предел, записанный в блоке 15.

ЗАМЕР 1: ВЕЖЛИВОСТЬ ДОБАВЛЕНА. `zumachen` (7167) по-польски писал
«Zamknij drzwi, proszę» при немецком «Mach die Tür zu», где никакого
«bitte» нет. У `scan_bitte_dropped` список замкнут, значит обратное
направление измеримо тем же списком.

Первая версия замера дала **24 попадания, из них 19 польских — и все
законные.** Причина в польской грамматике: **формальный императив ТАК И
ОБРАЗУЕТСЯ** через «Proszę + инфинитив». «Biegen Sie links ab» →
«Proszę skręcić w lewo»; другого способа нет.

Отсекается правилом, а не списком: если немецкий эталон сам вежливый
(«Sie»/«Ihnen»/«Ihre»), польское «Proszę» — перевод этой формы, а не
добавка. После отсечения 8 попаданий, настоящих 2–4. Половина добавлена
в примету мягким списком, и польский формальный императив стоит в
самопроверке отдельной строкой.

И снова: слабый признак нашёл не то, что искал. Среди восьми оказалась
ПОДМЕНА — `Vanille` (11825), где «мороженое пахнет ванилью и очень
вкусное» превратилось в «мне, пожалуйста, мороженое с ванилью».

ЗАМЕР 2: РОД РАССКАЗЧИКА ЧЕРЕЗ МЕСТОИМЕНИЕ. `nähen` (1719) писал «Я шью
себе одежду САМА» при немецком «selbst», где рода нет. Половины приметы
на глагол и на прилагательное этого не видят.

Замер: ru 1 женское против 4 мужских, uk 1 против 7. Нашёлся ровно один
ряд — тот же, что глазами.

**Польский в эту половину не вошёл, и причина в языке:** «sama» значит
и «сама», и «та же». Из 9 польских попаданий восемь законные — «ta SAMA
kobieta» (та же женщина), «została sama» (она осталась одна),
«rozmawia sama ze sobą» (ОНА говорит сама с собой), «sama waży»
(муравей сам весит). Отличить без разбора подлежащего нельзя.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: подменённое предложение, польский ═════════════════
    (16204, "example_pl",
     "Został oskarżony o uszkodzenie ciała",
     "Uszkodzenie ciała było poważne i musiał iść do szpitala",
     "подмена: эталон «war ernst, und er musste ins Krankenhaus gehen»"),
    (7179, "example_pl",
     "Ten model nie jest teraz dostępny",
     "Ta książka nie jest teraz dostępna, jest wypożyczona",
     "подмена: эталон про книгу, а не про модель"),
    (10532, "example_pl",
     "Daj mi buziaka na dobranoc",
     "Na pożegnanie daje mi małego buziaka w policzek",
     "подмена: эталон «Zum Abschied gibt sie mir ein kleines Küsschen»"),
    (16206, "example_pl",
     "Kara za kłamstwo była surowa",
     "Kara za jego złe zachowanie była bardzo surowa",
     "подмена: не за ложь, а за плохое поведение"),
    (16207, "example_pl",
     "Oba kraje podpisały pakt o nieagresji",
     "Oba kraje podpisały ważny pakt",
     "«o nieagresji» в эталоне нет, зато потеряно «wichtigen»"),
    (7183, "example_pl",
     "Uważaj bo szklanka się stłucze",
     "Szklanka się stłucze, jeśli ją upuszczę",
     "подмена: эталон «wenn ich es fallen lasse»"),
    (7183, "example_uk",
     "Чашка впала й розбилася",
     "Склянка розіб'ється, якщо я її впущу",
     "то же: эталон в будущем и с условием"),
    (16214, "example_pl",
     "Dostał tydzień aresztu domowego",
     "Chłopiec ma areszt domowy",
     "подмена: никакой недели в эталоне нет"),
    (11825, "example_pl",
     "Poproszę lody o smaku wanilii",
     "Lody smakują wanilią i są bardzo pyszne",
     "подмена: эталон описывает мороженое, а не заказывает его"),

    # ══ КЛАСС: подменённое предложение, турецкий ════════════════
    (11732, "example_tr",
     "Çok susamışım, bir bardak su ver",
     "Spordan sonra çok susuyorum ve bol su içiyorum",
     "подмена: эталон «Nach dem Sport bin ich sehr durstig und trinke viel Wasser»"),
    (15526, "example_tr",
     "Rüzgâr bütün gece bacada uğuldadı",
     "Su, nehirdeki taşların üzerinden gürültüyle akıyor",
     "подмена: перевод про ВЕТЕР в трубе, а эталон про воду в реке"),
    (2264, "example_tr",
     "Sana yük olmak istemiyorum",
     "Bu bana çok yük oluyor",
     "подмена: эталон «Das belastet mich sehr»"),
    (13522, "example_tr",
     "Artık eve gidebilirler, ders bitti",
     "Artık eve gidebilirsiniz, ders bitti",
     "третье лицо множественного вместо вежливого «вы»"),

    # ══ вежливость добавлена: эталон о ней не просит ════════════
    (7167, "example_pl",
     "Zamknij drzwi, proszę",
     "Zamknij drzwi",
     "в эталоне «Mach die Tür zu» никакого «bitte» нет"),

    # ══ род рассказчика через местоимение ═══════════════════════
    (1719, "example_ru",
     "Я шью себе одежду сама",
     "Я шью себе одежду сам",
     "эталон «selbst» рода не показывает; база по умолчанию мужская"),
    (1719, "example_uk",
     "Я сама шию собі одяг",
     "Я сам шию собі одяг",
     "то же"),
    (1719, "example_pl",
     "Sama szyję sobie ubrania",
     "Sam szyję sobie ubrania",
     "то же"),

    # ══ потерянное слово ════════════════════════════════════════
    (10530, "example_pl",
     "Grzesznik żałował swoich czynów",
     "Grzesznik żałuje swoich czynów i chce się poprawić",
     "потеряно «und möchte sich bessern», и время не то"),
    (7171, "example_pl",
     "Zamek wygląda wspaniale w światłach",
     "Zamek wygląda naprawdę wspaniale we wszystkich światłach",
     "потеряно «wirklich» и «all den»"),
    (7185, "example_pl",
     "To bardzo cenny zegarek od dziadka",
     "To cenny zegarek, który zostawił mi dziadek",
     "потеряно «vermacht» — оставил в наследство; и «bardzo» добавлено"),
    (1278, "example_tr",
     "Ekran bozuk",
     "Bilgisayarın ekranı bozuk",
     "потеряно «des Computers»"),
    (8890, "example_uk",
     "Вчителька стежить за дітьми на перерві",
     "Вчителька чергує на перерві й стежить за дітьми",
     "слова ряда в примере не было: Aufsicht это «чергування»"),
    (10532, "example_uk",
     "На прощання вона дає мені поцілунок у щоку",
     "На прощання вона дає мені маленький поцілуночок у щоку",
     "потерян уменьшительный суффикс: Küsschen, а не Kuss"),
    (10533, "example_pl",
     "Czekanie na odpowiedź to prawdziwa męka",
     "Męka czekania na odpowiedź była nie do zniesienia",
     "потеряно «unerträglich», и время не то"),

    # ══ добавленное слово ═══════════════════════════════════════
    (7186, "example_pl",
     "Zapalam świeczkę na torcie",
     "Zapalam świeczkę",
     "«na torcie» в эталоне «Ich zünde eine Kerze an» нет"),

    # ══ «рано в семь часов» и прочая неловкость ═════════════════
    (17146, "example_ru",
     "Мой отъезд завтра рано в семь часов",
     "Мой отъезд завтра утром в семь часов",
     "«рано в семь часов» не по-русски: «morgen früh» это утром"),
    (17146, "example_uk",
     "Мій від'їзд завтра рано о сьомій годині",
     "Мій від'їзд завтра вранці о сьомій годині",
     "то же"),
    (17146, "example_en",
     "My departure is tomorrow early at seven o'clock",
     "My departure is tomorrow morning at seven",
     "то же"),

    # ══ слово не из своего списка и не тот регистр ══════════════
    (7165, "example_uk",
     "Це був справді гівняний день для мене",
     "Це був справді паршивий день для мене",
     "в ru выбран «паршивый», а uk взял самый грубый из четырёх"),
    (14486, "example_tr",
     "Çocuk tencereye sopalarla vuruyor",
     "Çocuk sopalarla tencerede tempo tutuyor",
     "«vurmak» это просто бить; trommeln — «tempo tutmak»"),
    (14034, "example_uk",
     "Прислів'я говорить: попередження краще за лікування",
     "Прислів'я говорить: запобігати краще, ніж лікувати",
     "«попередження» это предупреждение, а Vorbeugen — профилактика"),
    (8893, "example_ru",
     "Управляющий директор руководит компанией",
     "Директор руководит компанией",
     "«управляющий директор» калька; в списке «директор»"),
    (8893, "example_uk",
     "Генеральний директор керує компанією",
     "Директор керує компанією",
     "«генеральний» нет в списке переводов"),

    # ══ русизм в списке переводов ══════════════════════════════
    (601, "translation_ru",
     "в обед, в полдень, по полудни",
     "в обед, в полдень, после полудня",
     "«по полудни» не форма: нужно «после полудня»"),
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
