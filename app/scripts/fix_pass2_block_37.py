"""ВТОРОЙ ПРОХОД, блок 37 (ряды 7201–7400): 35 правок.

ГЛАВНОЕ В БЛОКЕ — НЕ ПРАВКИ, А НОВАЯ ПРИМЕТА. Ряды 7252 `heiter` (10716)
и 7355 `heiterem` (11008) — один заголовок в двух формах. Повтор, которого
`scan_same_headword` не видит: она сравнивает `word_de` строка в строку.
Замер вышел в `scan_inflected_twin.py`: 83 пары «форма + окончание», из
них 13 с полностью одинаковым списком ru. То есть 375 заголовков прямой
приметы — это НИЖНЯЯ граница класса.

И замер связал два списка решений владельца в один: почти в каждой паре
один участник — голая словоформа (`heiterem`, `bezaubernde`, `dritt`,
`lenk`, `mittler`), то есть ряд из списка «заголовок не в словарной
форме». Голая форма ВСЕГДА дубль своей леммы, значит оба списка — один
класс с двух сторон, и решать их надо одним правилом.

ОТМЕНЁННЫЙ ВАРИАНТ ПРИМЕТЫ, ЗАМЕРЕННЫЙ ДО КОНЦА: сравнивать заголовки
без учёта регистра даёт 400 групп вместо 375, то есть ещё 29. Прочитаны
все 29 — ВСЕ законны: в немецком большая буква отличает существительное
от глагола и прилагательного (`Essen`/`essen`, `Morgen`/`morgen`,
`Arm`/`arm`, `Wagen`/`wagen`, `Sie`/`sie`). Ни одного дефекта. Вариант
отменён, а чувствительность к регистру в прямой примете подтверждена.

ТРЕТЬЯ ПОЛЬСКАЯ ПОЛОСА ПОДРЯД — 14 ячеек. Приём держится третий блок:

    Hackbraten (11848) «pyszny» вместо «den besten», и «Mama» вместо «Moja mama»
    besagen    (14168) «ceny» (цены) вместо «die Zahlen» (показатели)
    empört     (11009) «tym, co usłyszał» вместо «die unfaire Behandlung»
    Kraut      (11854) потеряно «immer selbst» и «kwaszona»
    Marathon   (12288) потеряно «nächsten» и «in Berlin»
    Turbulenz  (17256) потерян «Flugzeug», добавлено «silne»
    Genitale   (12831) потеряно «während der Routineuntersuchung»
    Milz       (12830) «mi» вместо «des Patienten»

НО ОДНОВРЕМЕННО — И ТУРЕЦКАЯ ПОЛОСА, 10 ЯЧЕЕК. Такого за проход ещё не
было: две полосы разных языков в одном блоке.

    aufgedreht (11007) «uyarılı» — слова нет в списке и значит не то
    grenzen     (7818) «varıyor» вместо «yaklaşmak» из своего списка
    Einmischung(14172) «müdahale görmek» — не оборот
    Diesel     (17255) «Arabam dizel gerekli» — фраза не согласована
    Schachtel  (18329) «Hediyeli kutular» — не оборот
    Pupillen   (12835) «daralmıştır» — не то время
    derartig   (13566) «birşey» вместо «bir şey»

ВИД КАРТОЧКИ СЛОМАН ТРИЖДЫ, И ВСЕ ТРИ РАЗА ОДИНАКОВО: в примере стоит
слово, которого нет в своём списке, поэтому `main_meaning` не находит
совпадения и показывает ПЕРВЫЙ вариант — не тот, о котором фраза.

    überführen (16514) ru «ИЗОБЛИЧИТЬ» при списке «перевезти, УЛИЧИТЬ…»
                       → карточка показывала «перевезти» на фразу о суде
    grenzen     (7818) tr «varıyor» при списке «sınır olmak, …»
                       → карточка показывала «sınır olmak» на «граничит с безумием»
    Zehner      (9868) tr «On avro» при списке «onluk, …»

Это тот же механизм, что в `Schiene` и `Messe` (блок 33), только там
виновата была поблажка матчера, а здесь — само слово в примере.

ЗАКОННЫЙ ПОДСЛУЧАЙ КЛАССА «ЧИСЛО СЛОВАМИ», НАЙДЕННЫЙ СРАЗУ: `Bahnsteig`
(1211) — de «von Bahnsteig 3», ru «с третьей платформы», uk «з третього
перону», pl «z peronu trzeciego». Три языка пишут число словом против
цифры, и это НЕ дефект: порядковый номер платформы по-людски называют
словом, «с платформы 3» — канцелярит. Правило из блока 36 относится к
ИЗМЕРЕНИЯМ («5 Zentimeter», «30 Prozent»), а не к порядковым номерам.
Граница класса названа, ряды не тронуты.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: вид карточки — слово не из своего списка ══════════
    (16514, "example_ru",
     "Полиция смогла изобличить преступника",
     "Полиция смогла уличить преступника",
     "«изобличить» не из списка: матчер молчал и карточка показывала «перевезти»"),
    (7818, "example_tr",
     "Yaptığın şey çılgınlığa varıyor",
     "Yaptığın şey çılgınlığa yaklaşıyor",
     "«varıyor» не из списка; в нём «-e yaklaşmak», иначе показывалось «sınır olmak»"),
    (9868, "example_tr",
     "On avro yeterli değil, daha fazla paraya ihtiyacım var",
     "Bir onluk yeterli değil, daha fazla paraya ihtiyacım var",
     "эталон «Ein Zehner», и «onluk» стоит в списке первым"),
    (12825, "example_uk",
     "Моя бабуся тепер живе в будинку для людей похилого віку",
     "Моя бабуся тепер живе в будинку для літніх людей",
     "в примере оборот, которого нет в списке «будинок для літніх людей»"),
    (9549, "example_tr",
     "Mezuniyet partisi gelecek hafta yapılacak",
     "Mezuniyet töreni gelecek hafta yapılacak",
     "эталон `Abschlussfeier` как торжество; «töreni» стоит в списке первым"),

    # ══ третья польская полоса подряд ═══════════════════════════
    (11848, "example_pl",
     "Mama robi pyszny klops na obiad",
     "Moja mama robi najlepszy klops na obiad",
     "«pyszny» вместо «den besten», и потеряно «Meine»"),
    (14168, "example_pl",
     "Raport mówi, że ceny wzrosły",
     "Raport mówi, że liczby wzrosły",
     "подмена: цены вместо «die Zahlen gestiegen sind»"),
    (11009, "example_pl",
     "Był oburzony tym, co usłyszał",
     "Był oburzony niesprawiedliwym traktowaniem",
     "подмена: «тем, что услышал» вместо «über die unfaire Behandlung»"),
    (11854, "example_pl",
     "Babcia robi kapustę do kiełbasek",
     "Moja babcia zawsze sama robi kapustę kwaszoną do kiełbasek",
     "потеряно «immer selbst» и квашеность: эталон о кислой капусте"),
    (12288, "example_pl",
     "W niedzielę biegnę swój pierwszy maraton",
     "W następną niedzielę biegnę swój pierwszy maraton w Berlinie",
     "потеряно «nächsten» и «in Berlin»"),
    (17256, "example_pl",
     "Podczas lotu były silne turbulencje",
     "Samolot miał turbulencje podczas lotu",
     "потерян «Flugzeug», добавлено «silne»"),
    (12831, "example_pl",
     "Lekarz zbadał narządy płciowe pacjenta",
     "Lekarz zbadał narządy płciowe podczas rutynowego badania",
     "потеряно «während der Routineuntersuchung», добавлен «pacjent»"),
    (12830, "example_pl",
     "Lekarz zbadał mi śledzionę",
     "Lekarz zbadał śledzionę pacjenta",
     "«mi» вместо «des Patienten»"),
    (9552, "example_pl",
     "Badam ten temat do prezentacji",
     "Właśnie badam ten temat do mojej prezentacji",
     "потеряно «gerade» и «meine»"),
    (12284, "example_pl",
     "Mój kumpel trenuje ze mną na siłowni",
     "Mój kumpel i ja trenujemy razem na siłowni",
     "эталон «Mein Sportsfreund UND ICH trainieren ZUSAMMEN»"),
    (18326, "example_pl",
     "Ten pokój jest zimny i nieprzytulny",
     "Ten pokój jest nieprzytulny i zimny",
     "порядок перевёрнут против «ungemütlich und kalt»"),
    (14636, "example_pl",
     "W tej bajce mieszka złośliwy skrzat",
     "W tej opowieści jest zły skrzat",
     "«bajka» вместо «Geschichte», «złośliwy» вместо «bös»"),
    (17835, "example_pl",
     "Konkurenci twardo walczyli o pierwsze miejsce",
     "Konkurenci zacięcie walczyli o pierwsze miejsce",
     "«twardo» калька с «hart»; по-польски «zacięcie»"),
    (12834, "translation_pl",
     "psychiatra, lekarz psychiatra",
     "psychiatra, kobieta psychiatra",
     "`Psychiaterin` женского рода: в en, ru, uk и tr женский род назван"),
    (12834, "example_pl",
     "Pracuje jako psychiatra w dużym szpitalu",
     "Ona pracuje jako psychiatra w dużym szpitalu",
     "потеряно «Sie»: без него фраза не о женщине"),

    # ══ турецкая полоса в том же блоке ══════════════════════════
    (11007, "example_tr",
     "Çocuklar tüm gün uyarılıydı ve oturamıyorlardı",
     "Çocuklar tüm gün heyecanlıydı ve yerinde duramıyorlardı",
     "«uyarılı» не из списка и значит другое; `stillsitzen` — «yerinde durmak»"),
    (14172, "example_tr",
     "Kişisel işlerime müdahale görmek istemem",
     "Kişisel işlerime müdahale edilmesine tahammül etmem",
     "«müdahale görmek» не оборот, и потеряно «dulden»"),
    (17255, "example_tr",
     "Arabam dizel gerekli, benzin değil",
     "Arabama dizel gerekiyor, benzin değil",
     "фраза не согласована: нужен датив «arabama»"),
    (18329, "example_tr",
     "Hediyeli kutular ağacın altında duruyordu",
     "Hediyelerin bulunduğu kutular ağacın altında duruyordu",
     "«hediyeli kutu» не оборот: это коробки С подарками внутри"),
    (12835, "example_tr",
     "Işık daha parlak olunca göz bebekleri daralmıştır",
     "Işık daha parlak olunca gözbebekleri daraldı",
     "«daralmıştır» не то время, и «gözbebeği» в списке одним словом"),
    (13566, "example_tr",
     "Hiç böyle birşey yapacağını düşünmemiştim",
     "Hiç böyle bir şey yapacağını düşünmemiştim",
     "«birşey» пишется раздельно"),
    (12287, "example_tr",
     "Babam her Cumartesi golf sahasında golf oynuyor",
     "Babam her Cumartesi golf sahasında oynuyor",
     "«golf» дважды в одной фразе"),

    # ══ подмена и потеря в прочих языках ════════════════════════
    (13566, "example_en",
     "I never expected he would do something like that",
     "I never expected you would do something like that",
     "эталон «dass DU etwas Derartiges machst»: в ru, uk, tr обращение к тебе"),
    (13566, "example_pl",
     "Czegoś takiego się nie spodziewałem",
     "Nie spodziewałem się, że zrobisz coś takiego",
     "потеряно обращение «du» целиком"),
    (11002, "example_uk",
     "Він завжди готовий до співпраці",
     "Він дуже готовий до співпраці й завжди охоче допомагає",
     "потеряна вторая половина эталона «und hilft immer gerne»"),
    (12287, "example_uk",
     "Мій батько грає в гольф кожну суботу",
     "Мій батько щосуботи грає на полі для гольфу",
     "потерян сам `Golfplatz`: эталон «auf dem Golfplatz»"),

    # ══ калька и форма, которой в языке нет ═════════════════════
    (7813, "example_uk",
     "Попіл був збережений в урні",
     "Попіл зберігали в урні",
     "«був збережений» калька с немецкого пассива"),
    (14636, "example_uk",
     "У історії є злий кобольд",
     "У цій історії є злий кобольд",
     "«У історії» без «цій» теряет «In der Geschichte» и звучит обрубком"),
    (7802, "example_ru",
     "Воротник крахмалят, чтобы сделать его жёстким",
     "Воротнику придают жёсткость крахмалом",
     "цели «чтобы сделать жёстким» в эталоне нет: «Man steift … mit Stärke»"),
    (7802, "example_uk",
     "Комірець крохмалять, щоб зробити його жорстким",
     "Комірцю надають жорсткості крохмалем",
     "то же"),
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
