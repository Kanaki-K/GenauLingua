"""ВТОРОЙ ПРОХОД, блок 57 (ряды 11201–11400): 54 правки в 43 рядах.

САМЫЙ ПЛОТНЫЙ БЛОК ЗА ВЕСЬ ПРОХОД — 21.5% против 12% в блоке 53 и
полосы 5–6.5% в блоках 54–56. Это ВТОРОЙ участок, и он крупнее первого.

И он подтверждает правило 1аа буквально наоборот: три блока подряд (54,
55, 56) без единой подмены целиком давали повод думать, что класс
кончился. Он не кончился — он сидит участками, и участок 57 дал
ПЯТНАДЦАТЬ подмен целиком:

    Personalakte  (9259) pl «SZEF ZAJRZAŁ DO MOICH akt osobowych»
                       de «Seine Personalakte ENTHIELT alle wichtigen
                           Unterlagen aus der letzten Anstellung»
    Flüchtlingslager(16901) pl «BRAKUJE WODY» вместо «katastrophale
                           hygienische Zustände»
    Alleinsein   (11522) pl «CZASEM POTRZEBUJĘ samotności, żeby
                           ODPOCZĄĆ» вместо «Sie brauchte ..., um ihre
                           Gedanken zu ordnen»
    Gerichtsvollzieher(16903) pl «DO SĄSIADA przyszedł komornik»
    Erdnuss      (12004) pl «LUBIĘ SOLONE orzeszki DO PIWA» вместо
                           «ist sehr proteinreich»
    Intrige      (11526) pl «W TEJ FIRMIE CIĄGLE KTOŚ KNUJE intrygi»
    Fänger        (8589) pl «ŁAPACZ ZŁAPAŁ PIŁKĘ W POWIETRZU» вместо
                           «im Baseball ist eine wichtige Position»
    Kruzifix     (14806) pl «NAD ŁÓŻKIEM wisi DREWNIANY krucyfiks»
    volllaufen    (8578) uk «ЗАЛ поволі наповнюється ЛЮДЬМИ» вместо
                           «Der Keller läuft mit WASSER voll»
    städtisch     (8580) en «The municipal POOL OPENS AT EIGHT» вместо
                           «Die städtische Verwaltung kümmert sich um
                            die Parks»
    Catering     (12003) tr «DÜĞÜN için ... TUTTUK», pl «na URODZINY»
    Telefonistin  (9262) pl «przełączyła MNIE DO SZEFA»
    Sarkophag    (14803) pl «W MUZEUM STOI KAMIENNY sarkofag»
    Chat         (17724) tr «bir sohbet BAŞLATTIK» вместо «nutzen»
    überkommen    (8570) tr «HABERI DUYDUĞUNDA bir ÜZÜNTÜ dalgası»,
                       en «A STRANGE FEELING» вместо «große Angst»

РЯД, ГДЕ РАЗОШЛИСЬ ЧЕТЫРЕ ЯЗЫКА ИЗ ПЯТИ — И ПРАВИЛО 1y НЕ ПРИМЕНИМО:

    Fernsehsendung (17729) de «Diese Fernsehsendung läuft jeden Sonntag»
                           en «That show WAS BORING»
                           ru «Моя любимая телепередача НАЧИНАЕТСЯ В ВОСЕМЬ»
                           uk то же, что ru
                           tr «Televizyon programı SIKICIYDI»
                           pl «leci w każdą niedzielę»   ← как в немецком

Четыре языка расходятся с эталоном, но МЕЖДУ СОБОЙ НЕ СОГЛАСНЫ: англ. и
тур. говорят «было скучно», рус. и укр. — «начинается в восемь». Правило
1y (блок 53) требует СОГЛАСИЯ переводов, и здесь его нет — значит прав
эталон, и правятся четыре перевода, а не он. Это обратный случай к
`Karawane`, и он показывает, что отличает одно от другого.

ГРАММАТИКА ТУРЕЦКОГО — семь рядов, и шесть из них рассыпаются, а не
просто неточны:

    Befruchtung  (13120) «Yumurta hücresi dölleme» → нужен генитив:
                         «Yumurta hücresinin döllenmesi»
    Trickster    (11524) «Herkesin kandırması yapan» → «Herkesi kandıran»
    Stillschweigen(14314) «sessizlik korudu» → «sessizliğini korudu»
    Hülse         (8590) «kovalar» значит ВЁДРА; гильзы — «kovanlar»
    Spülung      (13121) «Tuvalettin» — опечатка, и «boşaltma» не из
                         списка; «Tuvaletin sifonu»
    Kinderschänder(16906) «istismarçısı» — опечатка, нужно «istismarcısı»
    Todeszelle   (16902) «Mahkum kararı verilen kişi» — конструкция
                         рассыпается; просто «Mahkûm»

НЕМЕЦКИЙ ЭТАЛОН, восьмой случай за проход:

    anal (8576) de «Der Patient hat ANAL Beschwerden» — прилагательное
                перед существительным обязано склоняться: «anale
                Beschwerden». Все пять переводов согласно дают
                прилагательное в полной форме.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ немецкий эталон ════════════════════════════════════════
    (8576, "example_de",
     "Der Patient hat anal Beschwerden",
     "Der Patient hat anale Beschwerden",
     "прилагательное перед существительным обязано склоняться"),

    # ══ подмены целиком ════════════════════════════════════════
    (14803, "example_pl",
     "W muzeum stoi kamienny sarkofag",
     "Egipski sarkofag został starannie odrestaurowany w muzeum",
     "«в музее стоит каменный саркофаг» вместо реставрации египетского"),
    (9259, "example_pl",
     "Szef zajrzał do moich akt osobowych",
     "Jego akta osobowe zawierały wszystkie ważne dokumenty z ostatniej pracy",
     "«шеф заглянул в мои дела» вместо «enthielt alle wichtigen Unterlagen»"),
    (16901, "example_pl",
     "W obozie dla uchodźców brakuje wody",
     "W obozie dla uchodźców panowały katastrofalne warunki higieniczne",
     "«не хватает воды» вместо «katastrophale hygienische Zustände»"),
    (11522, "example_pl",
     "Czasem potrzebuję samotności, żeby odpocząć",
     "Potrzebowała samotności, żeby uporządkować myśli",
     "«иногда мне нужно ... отдохнуть» вместо «Sie brauchte ..., um ihre "
     "Gedanken zu ordnen»"),
    (16903, "example_pl",
     "Do sąsiada przyszedł komornik",
     "Komornik przyszedł, żeby wyegzekwować długi",
     "«к соседу» вместо «um die Schulden einzutreiben»"),
    (12004, "example_pl",
     "Lubię solone orzeszki ziemne do piwa",
     "Orzeszki ziemne są bardzo bogate w białko",
     "солёный арахис к пиву вместо «ist sehr proteinreich»"),
    (11526, "example_pl",
     "W tej firmie ciągle ktoś knuje intrygi",
     "Polityczna intryga była skomplikowana",
     "фирма и козни вместо «Die politische Intrige war kompliziert»"),
    (8589, "example_pl",
     "Łapacz złapał piłkę w powietrzu",
     "Łapacz w baseballu to ważna pozycja",
     "поймал мяч вместо «im Baseball ist eine wichtige Position»"),
    (14806, "example_pl",
     "Nad łóżkiem wisi drewniany krucyfiks",
     "Krucyfiks wisi na ścianie",
     "«над кроватью, деревянный» вместо «hängt an der Wand»"),
    (8578, "example_uk",
     "Зал поволі наповнюється людьми",
     "Підвал наповнюється водою",
     "зал и люди вместо «Der Keller läuft mit Wasser voll»"),
    (8580, "example_en",
     "The municipal pool opens at eight",
     "The municipal administration takes care of the parks",
     "бассейн и восемь часов вместо управления и парков"),
    (12003, "example_tr",
     "Düğün için ikram hizmeti tuttuk",
     "Parti için ikram hizmeti sipariş edildi",
     "свадьба и «наняли» вместо «für die Party ist bestellt»"),
    (12003, "example_pl",
     "Zamówiliśmy katering na urodziny",
     "Katering na imprezę jest zamówiony",
     "«на день рождения» вместо «für die Party»"),
    (9262, "example_pl",
     "Telefonistka przełączyła mnie do szefa",
     "Telefonistka łączy dzwoniących dalej",
     "«переключила меня на шефа» вместо «verbindet die Anrufer weiter»"),
    (17724, "example_tr",
     "Proje hakkında bir sohbet başlattık",
     "Proje hakkında iletişim için bir sohbet kullanıyoruz",
     "«начали чат» вместо «nutzen einen Chat für die Kommunikation»"),
    (8570, "example_tr",
     "Haberi duyduğunda bir üzüntü dalgası onu bastı",
     "Aniden büyük bir korku beni bastı",
     "новость и печаль вместо «Mich überkam plötzlich große Angst»"),
    (8570, "example_en",
     "A strange feeling came over me",
     "A great fear suddenly came over me",
     "«странное чувство» вместо «große Angst»"),
    (9263, "example_pl",
     "W tej firmie hierarchia jest bardzo sztywna",
     "Hierarchia w biurze jest bardzo jasna",
     "«жёсткая в фирме» вместо «im Büro ist sehr klar»"),
    (16904, "example_pl",
     "Jego ideologia jest bardzo radykalna",
     "Jego polityczna ideologia była skrajnie prawicowa",
     "«радикальна» вместо «extrem rechts»"),
    (13126, "example_pl",
     "Lekarze wykryli u niego guz mózgu",
     "Diagnozą był guz mózgu",
     "«врачи обнаружили» вместо «Die Diagnose war»"),
    (9260, "example_pl",
     "Firma ochroniarska pilnuje tego budynku",
     "Firmie ochroniarskiej zlecono nadzór nad budynkiem",
     "«охраняет» вместо «wurde beauftragt, zu überwachen»"),
    (9261, "example_pl",
     "On zawsze ma specjalne traktowanie u szefa",
     "Szef zawsze daje mu specjalne traktowanie",
     "подлежащее перевёрнуто: «Der Chef gibt ihm»"),
    (13123, "example_uk",
     "Суд визнав його неосудним",
     "Обвинувачений був психічно неосудним",
     "«суд признал» вместо «Der Angeklagte war mental unzurechnungsfähig»"),
    (13123, "example_pl",
     "Sąd uznał go za niepoczytalnego",
     "Oskarżony był niepoczytalny",
     "то же в польском"),
    (9629, "example_tr",
     "Mektubu taahhütlü olarak gönderdim",
     "Mektubum taahhütlü olarak geldi, böylece emin oldum",
     "«я отправил» вместо «Mein Brief KAM an, damit ich Gewissheit hatte»"),
    (13128, "example_pl",
     "Lekarz musi sterylizować narzędzia",
     "Dentysta musi sterylizować swoje narzędzia",
     "«врач» вместо «Der Zahnarzt», потеряно «seine»"),

    # ══ эталон прав, четыре перевода разошлись и НЕ согласны ════
    (17729, "example_en",
     "That show was boring",
     "This TV show airs every Sunday",
     "«было скучно» вместо «läuft jeden Sonntag»"),
    (17729, "example_ru",
     "Моя любимая телепередача начинается в восемь",
     "Эта телепередача идёт каждое воскресенье",
     "«любимая, начинается в восемь» вместо «läuft jeden Sonntag»"),
    (17729, "example_uk",
     "Моя улюблена телепередача починається о восьмій",
     "Ця телепередача виходить щонеділі",
     "то же в украинском"),
    (17729, "example_tr",
     "Televizyon programı sıkıcıydı",
     "Bu televizyon programı her pazar yayınlanıyor",
     "«было скучно» вместо «läuft jeden Sonntag»"),

    # ══ грамматика турецкого ═══════════════════════════════════
    (13120, "example_tr",
     "Yumurta hücresi dölleme normalde fallop tüpünde meydana gelir",
     "Yumurta hücresinin döllenmesi normalde fallop tüpünde meydana gelir",
     "нужен генитив и отглагольное: «hücresinin döllenmesi»"),
    (11524, "example_tr",
     "Herkesin kandırması yapan bir hileci",
     "Herkesi kandıran bir hileci",
     "«Herkesin kandırması yapan» рассыпается"),
    (14314, "example_tr",
     "Hükümet skandal hakkında sessizlik korudu",
     "Hükümet skandal hakkında sessizliğini korudu",
     "нужен притяжательный: «sessizliğini»"),
    (8590, "example_tr",
     "Mermi zemine kovalar bırakıyor",
     "Mermiler zemine kovanlar bırakıyor",
     "«kova» это ВЕДРО; гильза — «kovan»"),
    (13121, "example_tr",
     "Tuvalettin boşaltma düzgün çalışmıyor",
     "Tuvaletin sifonu düzgün çalışmıyor",
     "опечатка «Tuvalettin» и «boşaltma» не из списка"),
    (16906, "example_tr",
     "Çocuk istismarçısı ömür boyu hapis cezasına çarptırıldı",
     "Çocuk istismarcısı ömür boyu hapis cezasına çarptırıldı",
     "опечатка: «istismarcısı», а не «istismarçısı»"),
    (16902, "example_tr",
     "Mahkum kararı verilen kişi son günlerini ölüm hücresinde geçirdi",
     "Mahkûm son günlerini ölüm hücresinde geçirdi",
     "«Mahkum kararı verilen kişi» рассыпается"),
    (13124, "example_tr",
     "Partiden sonra sabahtan kalan hissediyorum",
     "Partiden sonra tamamen akşamdan kalmayım",
     "«sabahtan kalan hissediyorum» рассыпается; в списке «akşamdan kalma»"),

    # ══ слово не из своего списка ══════════════════════════════
    (8565, "example_uk",
     "Встановлена компанія має хорошу репутацію в галузі",
     "Визнана компанія має хорошу репутацію в галузі",
     "«встановлена» (установленная) не из списка; «визнаний» в нём второй"),
    (8579, "example_uk",
     "Дерево закриває дорогу",
     "Дерево перегороджує дорогу",
     "«закриває» не из списка; «перегороджувати» в нём первое"),
    (9262, "example_tr",
     "Telefoncu arayanları birbirine bağlıyor",
     "Telefon operatörü arayanları bağlıyor",
     "«Telefoncu» (телефонный мастер) не из списка"),
    (17390, "example_uk",
     "Коли падав дощ, він не відкривав дах кабріолета",
     "Коли падав дощ, він не відкривав складний дах кабріолета",
     "потеряно «складний» — заголовок именно о складном верхе"),
    (17390, "example_tr",
     "Yağmur yağdığında kabriyolenin tavanını açmadı",
     "Yağmur yağdığında kabriyolenin üstü açılır tavanını açmadı",
     "потеряно «üstü açılır» — то же"),

    # ══ потеря слова и грамматика славянских ═══════════════════
    (11521, "example_pl",
     "Ten łajdak ukradł mi wszystkie pieniądze",
     "Ten łajdak ukradł mi wszystkie pieniądze i po prostu zniknął",
     "потеряно «und ist einfach verschwunden»"),
    (16902, "example_pl",
     "Spędził ostatnie dni w celi śmierci",
     "Skazany spędził swoje ostatnie dni w celi śmierci",
     "потеряно «Der Verurteilte» и «seine»"),
    (13122, "example_pl",
     "Lekarz przepisał mi penicylinę",
     "Lekarz przepisał mi penicylinę na infekcję",
     "потеряно «gegen meine Infektion»"),
    (16905, "example_pl",
     "Trybunał skazał go na pięć lat",
     "Trybunał skazał go na pięć lat więzienia",
     "потеряно «Haft»"),
    (13602, "example_en",
     "To that extent, I agree",
     "To that extent I agree, but with caution",
     "потеряно «aber mit Vorsicht»"),
    (13602, "example_tr",
     "Bu bakımdan katılıyorum",
     "Bu bakımdan katılıyorum, ama dikkatle",
     "то же в турецком"),
    (18936, "example_uk",
     "В кінець місяця ти отримуєш зарплату",
     "У кінці місяця ти отримуєш зарплату",
     "«в кінець» — напрямок; потрібен місцевий відмінок «у кінці»"),
    (18937, "example_uk",
     "Нестача часу викликає мені стрес, коли є тільки дві години",
     "Нестача часу викликає в мене стрес, коли є тільки дві години",
     "«викликає мені» — неправильне керування; «викликає в мене»"),
    (13126, "example_uk",
     "Діагноз був пухлина мозку",
     "Діагнозом була пухлина мозку",
     "потрібен орудний відмінок: «Діагнозом була»"),
    (18470, "example_tr",
     "Mum ışığında atmosfer harikadır",
     "Mum ışığında atmosfer harikaydı",
     "настоящее при немецком прошедшем «war»"),
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
