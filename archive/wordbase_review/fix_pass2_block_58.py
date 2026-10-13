"""ВТОРОЙ ПРОХОД, блок 58 (ряды 11401–11600): 50 правок в 40 рядах.

ВТОРОЙ ПЛОТНЫЙ БЛОК ПОДРЯД — 20% после 21.5%. То есть участок, начавшийся
в блоке 57, не кончился, а продолжается. И первая половина блока 58 почти
чистая (5 правок на 50 рядов), а вторая дала 45 — участок имеет границу
внутри блока.

НАЙДЕН НОВЫЙ ВИД ДЕФЕКТА: ОДНА ПОДМЕНА, РАЗОШЁДШАЯСЯ ПО ЧЕТЫРЁМ ЯЗЫКАМ.

    verstreichen (18940) de «Lass die Frist nicht verstreichen!»
                         en «TIME PASSED UNNOTICED DURING THE MOVIE!»
                         ru «ВРЕМЯ ПРОШЛО НЕЗАМЕТНО ВО ВРЕМЯ ФИЛЬМА!»
                         uk то же, что ru
                         tr то же
                         pl «Nie pozwól, żeby termin upłynął!»  ← верно

Четыре языка говорят ОДНО И ТО ЖЕ, и это не немецкая фраза. До сих пор
такая картина (правило 1y, `Karawane`) значила, что обрезан ЭТАЛОН. Здесь
не так, и отличие видно сразу: в `Karawane` четыре языка ДОБАВЛЯЛИ к
эталону кусок («в Египет»), а здесь они заменяют фразу ЦЕЛИКОМ на другую.
Плюс польский держит немецкую версию — значит эталон не обрезан, а
подмена случилась ОДИН раз и была скопирована в четыре языка.

**Уточнение к правилу 1y:** согласие переводов доказывает, что эталон
неполон, только если они ДОБАВЛЯЮТ. Если они согласно говорят ДРУГОЕ —
это одна подмена, размноженная копированием, и править надо их.

Второй такой же ряд, но с тремя языками: `früh` (18941) — en, ru, uk
говорят «ранний подъём НЕОБХОДИМ», при немецком «ist ANSTRENGEND»
(утомителен). tr и pl держат «трудно/męczące», то есть верно.

ВЕРНАЯ ПРАВКА СНЯЛА МАСКУ С ДАВНЕГО ДЕФЕКТА В ДРУГОМ ЯЗЫКЕ.

Это стоит записать подробно, потому что случай поучительный. После
применения блока примета `scan_shown_sense` выросла с 71 до 72 и упала.
Новое попадание — `entbinden` (13136), язык pl.

Причина не в польском, а в турецком. Условие приметы: этот язык не
находит в примере НИ ОДНОГО варианта своего списка, а три и более других
языка нашли, и все они указали НЕ на первый вариант. До правки турецкий
пример «Doktor kadını hastanede doğurttu» указывал на вариант 1
(«doğurmak»), и условие «все указали не на первый» не выполнялось —
примета молчала. Моя правка сделала турецкий верным («doğum yaptırmak» —
вариант 2), и условие выполнилось.

То есть польский дефект был ВСЁ ВРЕМЯ: список «rodzić | odbierać poród |
zwalniać z obowiązku», пример «odebrał poród», а карточка показывала
«rodzić». Его маскировал турецкий дефект в том же ряду.

Лечение оказалось неожиданным. `chosen_index` ищет вариант по САМОМУ
ДЛИННОМУ слову — в «odbierać poród» это «odbierać», и форма «odebrał»
с ним не сходится (общее только «od»). Проверено прямым прогоном:

    «Lekarz odebrał poród ...»    -> None
    «Lekarz odbierał poród ...»   -> 1

Поэтому вид изменён на несовершенный: «odbierał». По-польски это
естественно для описания того, что врач делал, и карточка теперь
показывает «odbierać poród» — то есть ровно то, что в примере.

**Урок: правка в одном языке может открыть дефект в другом.** Примета
поэтому и гоняется после КАЖДОГО блока, а не в конце прохода.

ТУРЕЦКИЙ — ПЯТНАДЦАТЬ РЯДОВ, И ЭТО САМЫЙ ПЛОХОЙ ЯЗЫК БЛОКА:

    Empfängnis (15322) «HAMİLELİK yeni bir gebeliğin başlangıcıdır» —
                       «беременность есть начало новой беременности».
                       Заголовок `Empfängnis` это ЗАЧАТИЕ, «döllenme».
    Glückszahl (12404) «Benim şans numaraMIZ yedi» — притяжательный
                       первого лица МНОЖЕСТВЕННОГО: «наш», а не «мой».
    spotten    (11552) «ona alay ediyor» → нужно «onunla»; и «o zeki»
                       значит «он УМНЫЙ», а немецкое «nerdig» — «ботан».
    zapfen     (12014) «BARISTA fıçıdan taze bira döktü» — бариста варит
                       кофе; «Barkeeper» это «barmen».
    Rheuma     (13140) «Büyükannem romatizması var» → «Büyükannemin».
    entmutigen (11550) «cesaretinden kırmamalı» → «cesaretini kırmamalı».
    Stichwunde (13138) «Bıçak yaraması hastanede hemen tedavi edilmesi
                       gerekiyordu» — конструкция рассыпается.
    zulässig   (16926) «Bu yöntem ... izin verilmektedir» → дательный:
                       «Bu yönteme».
    Lieblingsbuch(9632) «Benim SEVİLEN kitabım» — страдательное
                       «любимый кем-то»; нужно «En sevdiğim kitap».

ПОДМЕНЫ ЦЕЛИКОМ, девять рядов: `erwirken` (16927) uk «Вона таки
домоглася свого» вместо адвоката и освобождения; `geistesgestört`
(13139) pl «Krzyczał na ulicy jak obłąkany»; `Stichwunde` (13138) pl
«Rana kłuta NA RAMIENIU mocno KRWAWIŁA»; `Brüderlichkeit` (11548) pl
«MÓWILI O braterstwie»; `Akkord` (14819) pl «Zagrał PIERWSZY akord»;
`beglückwünschen` (11549) pl «pogratulować NOWEJ PRACY» вместо успеха;
`zutreffend` (8623) в трёх языках; `vorladen` (16929) en и tr;
`schmackhaft` (12012) pl «ZUPA» вместо «Das Essen».

СЛАВЯНСКАЯ ГРАММАТИКА, шесть рядов: `Lende` (15324) uk «була біль» —
«біль» у чоловічому роді, треба «був біль»; `Versteigerung` (9947) uk
«о трьох годинах» → «о третій годині»; `unüblich` (8622) uk «зі ранку» →
«зранку»; `Pedal` (17396) uk «машина їхала» → «поїхала»; `zapfen`
(12014) uk «наливав» → «налив»; `gebührend` (8626) uk «була гідно
святкована» — неживий зворот.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ одна подмена, размноженная по четырём языкам ════════════
    (18940, "example_en",
     "Time passed unnoticed during the movie!",
     "Don't let the deadline expire!",
     "подмена целиком; польский держит немецкую версию"),
    (18940, "example_ru",
     "Время прошло незаметно во время фильма!",
     "Не дай сроку истечь!",
     "та же подмена, скопированная"),
    (18940, "example_uk",
     "Час пройшов непомітно під час фільму!",
     "Не дай терміну спливти!",
     "та же подмена, скопированная"),
    (18940, "example_tr",
     "Film sırasında zaman fark edilmeden geçti!",
     "Sürenin dolmasına izin verme!",
     "та же подмена, скопированная"),
    (18941, "example_en",
     "Early rising is necessary today",
     "Early rising is exhausting",
     "«необходим» вместо «ist anstrengend»; tr и pl держат верно"),
    (18941, "example_ru",
     "Ранний подъём сегодня необходим",
     "Ранний подъём утомителен",
     "то же"),
    (18941, "example_uk",
     "Ранній підйом необхідний сьогодні",
     "Ранній підйом утомливий",
     "то же"),

    # ══ турецкий: слово не то ══════════════════════════════════
    (15322, "example_tr",
     "Hamilelik yeni bir gebeliğin başlangıcıdır",
     "Döllenme yeni bir gebeliğin başlangıcıdır",
     "«Hamilelik» это беременность: «беременность — начало беременности»"),
    (12014, "example_tr",
     "Barista fıçıdan taze bira döktü",
     "Barmen fıçıdan taze bira doldurdu",
     "«Barista» варит кофе; «Barkeeper» это «barmen»"),
    (11552, "example_tr",
     "Çocuklar ona alay ediyor çünkü o zeki",
     "Çocuklar onunla alay ediyor çünkü o bir inek",
     "«ona alay» → «onunla»; «o zeki» значит УМНЫЙ, а «nerdig» — ботан"),
    (9632, "example_tr",
     "Benim sevilen kitabım çok heyecan verici ve onu defalarca okurum",
     "En sevdiğim kitap çok heyecan verici ve onu defalarca okurum",
     "«sevilen» страдательное; в списке «en sevdiği kitap»"),

    # ══ турецкий: грамматика ═══════════════════════════════════
    (12404, "example_tr",
     "Benim şans numaramız yedi",
     "Benim şans numaram yedi",
     "«numaramız» это НАШ номер, а не мой"),
    (13140, "example_tr",
     "Büyükannem romatizması var ve yürüyüşü zor",
     "Büyükannemin romatizması var ve yürümesi zor",
     "нужен генитив: «Büyükannemin»"),
    (11550, "example_tr",
     "Eleştirisi seni cesaretinden kırmamalı, iyi ilerliyorsun",
     "Eleştirisi cesaretini kırmamalı, iyi ilerliyorsun",
     "«cesaretinden kırmamalı» → «cesaretini kırmamalı»"),
    (13138, "example_tr",
     "Bıçak yaraması hastanede hemen tedavi edilmesi gerekiyordu",
     "Bıçak yarasının hastanede hemen tedavi edilmesi gerekiyordu",
     "нужен генитив: «yarasının»"),
    (16926, "example_tr",
     "Bu yöntem yeni kurallar altında izin verilmektedir",
     "Bu yönteme yeni kurallara göre izin verilmektedir",
     "«izin verilmek» требует датива"),
    (13136, "example_tr",
     "Doktor kadını hastanede doğurttu",
     "Doktor kadının doğumunu hastanede yaptırdı",
     "«doğurttu» неестественно; нормальное «doğum yaptırmak»"),
    (13139, "example_tr",
     "Bu adam tamamen deli",
     "Bu adam akıl hastası gibi görünüyordu ve karmakarışık konuşuyordu",
     "«совсем сумасшедший» вместо «schien geistesgestört und redete wirr»"),
    (13775, "example_tr",
     "İşe gitmeden önce her zaman saçını yaptırıyor",
     "İşe gitmeden önce sabahları saçımı yaptırıyorum",
     "третье лицо при немецком «Ich lasse mir»"),
    (1510, "example_tr",
     "Her gün jimnastik yapıyorum",
     "Her sabah jimnastik yapıyorum",
     "«каждый день» вместо «jeden Morgen»"),

    # ══ подмены целиком ════════════════════════════════════════
    (16927, "example_uk",
     "Вона таки домоглася свого",
     "Адвокат зміг домогтися звільнення свого клієнта",
     "«она добилась своего» вместо адвоката и освобождения"),
    (13139, "example_pl",
     "Krzyczał na ulicy jak obłąkany",
     "Mężczyzna wydawał się chory psychicznie i mówił bez ładu",
     "«кричал на улице как безумный» вместо «schien geistesgestört»"),
    (13138, "example_pl",
     "Rana kłuta na ramieniu mocno krwawiła",
     "Rana kłuta musiała być natychmiast opatrzona w szpitalu",
     "«на плече, сильно кровоточила» вместо лечения в больнице"),
    (11548, "example_pl",
     "Mówili o braterstwie między narodami",
     "Braterstwo między narodami jest ważne dla pokoju",
     "«они говорили о» вместо «ist wichtig für den Frieden»"),
    (14819, "example_pl",
     "Zagrał pierwszy akord na gitarze",
     "Gitarzysta zagrał piękny akord",
     "«первый аккорд» вместо «Der Gitarrist spielte einen schönen»"),
    (11549, "example_pl",
     "Chcę ci pogratulować nowej pracy",
     "Chcę ci pogratulować twojego sukcesu",
     "«новой работы» вместо «zu deinem Erfolg»"),
    (12012, "example_pl",
     "Zupa jest naprawdę smaczna",
     "Jedzenie jest bardzo smaczne",
     "«Zupa» вместо «Das Essen», «naprawdę» вместо «sehr»"),
    (13143, "example_pl",
     "Jego opis był bardzo plastyczny",
     "Plastyczny opis sprawił, że scena była bardzo żywa",
     "потеряно «machte die Szene sehr lebendig»"),
    (8623, "example_en",
     "That's an accurate description of him",
     "Your answer is not entirely accurate",
     "«точное описание его» вместо «Deine Antwort ist nicht ganz zutreffend»"),
    (8623, "example_uk",
     "Опис дуже застосовний для цієї ситуації",
     "Твоя відповідь не зовсім правильна",
     "то же в украинском"),
    (8623, "example_tr",
     "Açıklama bu durum için çok uygun",
     "Cevabın tam olarak doğru değil",
     "то же в турецком"),
    (16929, "example_en",
     "The judge summoned the witness to the court hearing",
     "The court summoned him as a witness",
     "«судья вызвал свидетеля» вместо «Das Gericht hat IHN als Zeugen»"),
    (16929, "example_tr",
     "Hakim tanığı mahkeme duruşmasına çağırdı",
     "Mahkeme onu tanık olarak çağırdı",
     "то же в турецком"),

    # ══ славянская грамматика ══════════════════════════════════
    (15324, "example_uk",
     "У нього була біль у поясниці",
     "У нього був біль у поясниці",
     "«біль» чоловічого роду: «був біль»"),
    (9947, "example_uk",
     "Аукціон починається о трьох годинах",
     "Аукціон починається о третій годині",
     "«о трьох годинах» — неправильна форма часу"),
    (8622, "example_uk",
     "Незвично пити пиво зі ранку",
     "Незвично пити пиво зранку",
     "«зі ранку» — опечатка"),
    (17396, "example_uk",
     "Я натиснув на педаль і машина їхала швидше",
     "Я натиснув на педаль і машина поїхала швидше",
     "незавершений вид при «fuhr schneller»"),
    (12014, "example_uk",
     "Бармен наливав свіже пиво з бочки",
     "Бармен налив свіже пиво з бочки",
     "незавершений вид при «zapfte»"),
    (8626, "example_uk",
     "Перемога була гідно святкована",
     "Перемогу відсвяткували належним чином",
     "неживий пасивний зворот"),
    (13139, "example_uk",
     "Чоловік здавався розумово хворим і говорив безладно",
     "Чоловік здавався психічно хворим і говорив безладно",
     "«розумово хворий» не из списка; «психічно хворий» в нём второй"),

    # ══ слово не из своего списка ══════════════════════════════
    (16930, "example_ru",
     "Соседние страны снова на боевом пути",
     "Соседние страны снова на тропе войны",
     "«боевой путь» не из списка; «тропа войны» единственный вариант"),

    # ══ потеря слова и вид ═════════════════════════════════════
    (13136, "example_pl",
     "Lekarz odebrał poród w szpitalu",
     "Lekarz odbierał poród u kobiety w szpitalu",
     "потеряно «die Frau»; вид изменён на несовершенный — см. докстринг, "
     "иначе `chosen_index` не узнаёт «odbierać poród» в форме «odebrał»"),
    (11545, "example_pl",
     "Przy muzyce zawsze się ożywia",
     "Przy muzyce naprawdę się ożywia",
     "«zawsze» вместо «richtig»"),
    (16925, "example_pl",
     "W średniowieczu przestępców często stracono publicznie",
     "W średniowieczu przestępców często tracono",
     "совершенный вид и добавленное «publicznie»"),
    (13140, "example_pl",
     "Babcia ma reumatyzm i trudno jej chodzić",
     "Moja babcia ma reumatyzm i trudno jej chodzić",
     "потеряно «Meine»"),
    (9269, "example_pl",
     "Dobra praca zespołowa jest ważna",
     "Dobra praca zespołowa jest ważna dla sukcesu",
     "потеряно «für den Erfolg»"),
    (13141, "example_pl",
     "Dziecko ma zadrapanie na kolanie",
     "Dziecko ma zadrapanie na kolanie po upadku",
     "потеряно «nach dem Sturz»"),
    (16929, "example_pl",
     "Sąd wezwał go do sądu jako świadka",
     "Sąd wezwał go jako świadka",
     "«Sąd ... do sądu» — повтор"),
    (8625, "example_uk",
     "Маленький хлопчик сидів на спині батька",
     "Маленький хлопчик сидів на плечах у батька",
     "«на спині» при немецком «auf den Schultern»"),
    (13138, "example_uk",
     "Ножова рана мала бути негайно лікована в лікарні",
     "Ножову рану довелося негайно лікувати в лікарні",
     "«мала бути лікована» — калька"),
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
