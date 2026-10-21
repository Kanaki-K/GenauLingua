"""A2, блок 13: слова 481–520 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («X leuchtet», «Das war romantisch») — пусто"
EN = "английский пример: так не говорят"
GO = "«Wir gehen in den X» — тот же пример, что у Park, Museum, Theater"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2769: (SKEL, {"t_ru": "романтичный", **all_x(
        "Wir hatten ein romantisches Abendessen bei Kerzenlicht", "У нас был романтический ужин при свечах",
        "У нас була романтична вечеря при свічках", "We had a romantic candlelit dinner",
        "Mum ışığında romantik bir akşam yemeği yedik", "Zjedliśmy romantyczną kolację przy świecach",
        "Abbiamo fatto una cena romantica a lume di candela", "Tuvimos una cena romántica a la luz de las velas",
        "On a fait un dîner romantique aux chandelles", "Měli jsme romantickou večeři při svíčkách")}),
    1334: (EN + " («We discuss the problem»); " + LIST, {
        "t_ru": "обсуждать, спорить", "t_uk": "обговорювати, сперечатися", "t_en": "to discuss, to argue",
        "t_tr": "tartışmak", "t_pl": "dyskutować, omawiać",
        **all_x("Mit ihm kann man nicht diskutieren", "С ним невозможно спорить", "З ним неможливо сперечатися",
                "There's no arguing with him", "Onunla tartışılmaz", "Z nim nie da się dyskutować",
                "Con lui non si può discutere", "Con él no se puede discutir", "Avec lui, on ne peut pas discuter",
                "S ním se nedá diskutovat")}),
    57: (LIST, {"t_ru": "профессиональное обучение, образование", "t_uk": "професійне навчання, освіта",
                "t_en": "vocational training, apprenticeship", "t_tr": "mesleki eğitim",
                "t_pl": "nauka zawodu, wykształcenie", "t_it": "la formazione", "t_es": "la formación",
                "t_fr": "la formation", "t_cs": "vyučení, vzdělání"}),
    13931: (EN, {"t_tr": "röportaj, mülakat", "t_pl": "wywiad, rozmowa kwalifikacyjna",
                 "x_en": "She's giving an interview"}),
    14419: ("«каждый день по часу» — порядок слов; " + LIST, {
        "t_ru": "пианино, фортепиано", "t_uk": "піаніно, фортепіано",
        "x_ru": "Я каждый день по часу играю на пианино", "x_uk": "Я щодня по годині граю на піаніно"}),
    6753: (LIST, {"t_ru": "получаться, удаваться", "t_uk": "вдаватися, виходити", "t_en": "to work out",
                  "t_tr": "yolunda gitmek", "t_pl": "udać się, wyjść", "t_cs": "vyjít, klapnout",
                  "x_ru": "Со встречей всё получилось?"}),
    2704: ("uk «прибула» — так о посылке не говорят; " + LIST, {
        "t_ru": "посылка, пакет", "t_uk": "посилка, пакет", "t_en": "parcel, package", "t_tr": "paket, koli",
        "t_pl": "paczka", "x_uk": "Посилка прийшла сьогодні", "x_en": "The parcel arrived today"}),
    1058: (EN + " («We sit in the living room»); " + LIST, {
        "t_ru": "гостиная", "t_uk": "вітальня", "t_en": "living room", "t_tr": "oturma odası, salon",
        "t_pl": "salon, pokój dzienny",
        **all_x("Komm ins Wohnzimmer, der Film fängt an", "Иди в гостиную, фильм начинается",
                "Іди до вітальні, фільм починається", "Come into the living room, the film's starting",
                "Oturma odasına gel, film başlıyor", "Chodź do salonu, film się zaczyna",
                "Vieni in soggiorno, il film sta cominciando", "Ven al salón, que empieza la película",
                "Viens au salon, le film commence", "Pojď do obýváku, film začíná")}),
    2268: (LIST, {"t_ru": "популярный, любимый", "t_uk": "популярний, улюблений", "t_en": "popular",
                  "t_tr": "popüler, sevilen", "t_pl": "popularny, lubiany"}),
    1962: ("«Ich trainiere jeden Tag» — пусто, как täglich; " + LIST, {
        "t_ru": "тренироваться, тренировать", "t_uk": "тренуватися, тренувати", "t_en": "to train, to work out",
        "t_tr": "antrenman yapmak", "t_pl": "trenować",
        **all_x("Ich trainiere dreimal pro Woche im Fitnessstudio", "Я тренируюсь в спортзале три раза в неделю",
                "Я тренуюся в спортзалі тричі на тиждень", "I work out at the gym three times a week",
                "Haftada üç kez spor salonunda antrenman yapıyorum", "Trenuję na siłowni trzy razy w tygodniu",
                "Mi alleno in palestra tre volte alla settimana", "Entreno en el gimnasio tres veces por semana",
                "Je m'entraîne à la salle trois fois par semaine", "Trénuji v posilovně třikrát týdně")}),
    12138: (EN + " («Finally it's holidays»)", {"t_en": "holidays", "t_tr": "tatil", "t_pl": "wakacje, ferie",
                                               "x_en": "The holidays are here at last!"}),
    17505: (SKEL + " («Der Apparat ist kaputt»); " + LIST, {
        "t_ru": "аппарат, телефон", "t_uk": "апарат, телефон", "t_en": "device, phone", "t_tr": "cihaz, telefon",
        "t_pl": "aparat, urządzenie", "t_it": "l'apparecchio, il telefono", "t_es": "el aparato",
        "t_fr": "l'appareil", "t_cs": "přístroj, telefon",
        **all_x("Der Apparat macht komische Geräusche", "Аппарат издаёт странные звуки", "Апарат видає дивні звуки",
                "The machine is making strange noises", "Cihaz garip sesler çıkarıyor",
                "To urządzenie wydaje dziwne dźwięki", "L'apparecchio fa dei rumori strani",
                "El aparato hace ruidos raros", "L'appareil fait des bruits bizarres", "Ten přístroj vydává divné zvuky")}),
    12140: (LIST, {"t_ru": "цирк, балаган", "t_uk": "цирк, балаган", "t_en": "circus, fuss", "t_tr": "sirk, curcuna",
                   "t_pl": "cyrk, zamieszanie"}),
    747: ("«Ich rechne schnell» — пусто; " + LIST, {
        "t_ru": "считать, рассчитывать на", "t_uk": "рахувати, розраховувати на", "t_en": "to calculate, to count on",
        "t_tr": "hesaplamak, beklemek", "t_pl": "liczyć, liczyć na coś", "t_it": "calcolare, contare su",
        "t_es": "calcular, contar con", "t_fr": "calculer, compter sur",
        **all_x("Kannst du das schnell im Kopf rechnen?", "Можешь быстро посчитать это в уме?",
                "Можеш швидко порахувати це в голові?", "Can you quickly calculate that in your head?",
                "Bunu kafandan hızlıca hesaplayabilir misin?", "Możesz to szybko policzyć w pamięci?",
                "Puoi calcolarlo velocemente a mente?", "¿Puedes calcularlo rápido de cabeza?",
                "Tu peux le calculer vite de tête?", "Můžeš to rychle spočítat z hlavy?")}),
    677: ("«Она покупает в интернете» — без дополнения так не говорят; " + LIST, {
        "t_ru": "онлайн, в интернете", "t_uk": "онлайн, в інтернеті", "t_tr": "internetten, online",
        "t_pl": "online, przez internet", "t_es": "por internet, en línea",
        "x_ru": "Она делает покупки в интернете", "x_uk": "Вона робить покупки онлайн"}),
    16035: (LIST, {"t_ru": "партия, сторона", "t_uk": "партія, сторона", "t_en": "party, side", "t_tr": "parti, taraf",
                   "t_pl": "partia, strona"}),
    1803: ("«закон божий как школьный предмет» — пояснение, не перевод; «Religion ist ein wichtiges Fach» — плакат", {
        "t_ru": "религия, вера", "t_uk": "релігія, віра", "t_en": "religion, faith", "t_tr": "din, inanç",
        "t_pl": "religia, wiara",
        **all_x("In der Schule haben wir zweimal pro Woche Religion", "В школе у нас два раза в неделю урок религии",
                "У школі в нас двічі на тиждень урок релігії", "At school we have religion twice a week",
                "Okulda haftada iki kez din dersimiz var", "W szkole mamy religię dwa razy w tygodniu",
                "A scuola abbiamo religione due volte alla settimana", "En el colegio tenemos religión dos veces por semana",
                "À l'école, on a cours de religion deux fois par semaine", "Ve škole máme náboženství dvakrát týdně")}),
    1670: ("«Ich male gern» — пусто; " + LIST, {
        "t_ru": "рисовать (красками), красить", "t_uk": "малювати, фарбувати", "t_en": "to paint",
        "t_tr": "resim yapmak, boyamak", "t_pl": "malować", "t_it": "dipingere, disegnare", "t_es": "pintar",
        "t_fr": "peindre, dessiner", "t_cs": "malovat",
        **all_x("Meine Tochter malt gern Tiere", "Моя дочь любит рисовать животных", "Моя донька любить малювати тварин",
                "My daughter loves painting animals", "Kızım hayvan resmi yapmayı seviyor",
                "Moja córka lubi malować zwierzęta", "A mia figlia piace disegnare gli animali",
                "A mi hija le gusta pintar animales", "Ma fille adore dessiner des animaux",
                "Moje dcera ráda maluje zvířata")}),
    13492: ("«как только» — это sobald; sowie — слово списков и объявлений, «Brot sowie Milch» так не говорят", {
        "t_ru": "а также, и", "t_uk": "а також, і", "t_en": "as well as, and", "t_tr": "ve ayrıca",
        "t_pl": "oraz, a także", "t_it": "nonché, e anche", "t_es": "así como, y también", "t_fr": "ainsi que, et",
        "t_cs": "a také, jakož i",
        **all_x("Bitte bringen Sie Ihren Pass sowie ein Foto mit", "Пожалуйста, возьмите с собой паспорт, а также фото",
                "Будь ласка, візьміть із собою паспорт, а також фото", "Please bring your passport as well as a photo",
                "Lütfen pasaportunuzu ve ayrıca bir fotoğraf getirin", "Proszę zabrać paszport oraz zdjęcie",
                "Porti con sé il passaporto e anche una foto", "Traiga su pasaporte así como una foto, por favor",
                "Apportez votre passeport ainsi qu'une photo, s'il vous plaît", "Přineste si prosím pas a také fotku")}),
    12142: (LIST, {"t_ru": "команда, сборная", "t_uk": "команда, збірна", "t_en": "team, crew", "t_tr": "takım",
                   "t_pl": "drużyna, załoga"}),
    14427: ("«Der Autor schreibt gerade ein neues Buch» — пусто", {**all_x(
        "Wer ist der Autor von diesem Buch?", "Кто автор этой книги?", "Хто автор цієї книжки?",
        "Who's the author of this book?", "Bu kitabın yazarı kim?", "Kto jest autorem tej książki?",
        "Chi è l'autore di questo libro?", "¿Quién es el autor de este libro?", "Qui est l'auteur de ce livre?",
        "Kdo je autorem téhle knihy?")}),
    3043: (EN + " («We sleep in the tent»); " + LIST, {
        "t_ru": "палатка", "t_uk": "намет", "t_en": "tent", "t_tr": "çadır", "t_pl": "namiot",
        "t_es": "la tienda de campaña",
        **all_x("Hilfst du mir, das Zelt aufzubauen?", "Поможешь мне поставить палатку?", "Допоможеш мені поставити намет?",
                "Can you help me put up the tent?", "Çadırı kurmama yardım eder misin?", "Pomożesz mi rozbić namiot?",
                "Mi aiuti a montare la tenda?", "¿Me ayudas a montar la tienda?", "Tu m'aides à monter la tente?",
                "Pomůžeš mi postavit stan?")}),
    1771: (LIST, {"t_ru": "личный, частный", "t_uk": "особистий, приватний", "t_en": "private", "t_tr": "özel",
                  "t_pl": "prywatny"}),
    175: ("«немецкий как школьный предмет» — пояснение, не перевод", {
        "t_ru": "немецкий язык", "t_uk": "німецька мова", "t_en": "German", "t_tr": "Almanca", "t_pl": "niemiecki",
        "x_uk": "Вона вивчає німецьку вже рік"}),
    738: ("«Ich putze die Küche» — скелет; " + LIST, {
        "t_ru": "убирать, чистить", "t_uk": "прибирати, чистити", "t_en": "to clean, to brush",
        "t_tr": "temizlemek, fırçalamak", "t_pl": "sprzątać, myć", "t_it": "pulire, lavarsi",
        "t_es": "limpiar, cepillarse", "t_fr": "nettoyer, se brosser", "t_cs": "uklízet, čistit",
        **all_x("Hast du dir die Zähne geputzt?", "Ты почистил зубы?", "Ти почистив зуби?",
                "Have you brushed your teeth?", "Dişlerini fırçaladın mı?", "Umyłeś zęby?", "Ti sei lavato i denti?",
                "¿Te has cepillado los dientes?", "Tu t'es brossé les dents?", "Vyčistil sis zuby?")}),
    14428: ("третий пример «интересуюсь …» (interessieren, Interesse)", {**all_x(
        "Ich mag die italienische Kultur", "Мне нравится итальянская культура", "Мені подобається італійська культура",
        "I love Italian culture", "İtalyan kültürünü seviyorum", "Lubię kulturę włoską", "Mi piace la cultura italiana",
        "Me gusta la cultura italiana", "J'aime la culture italienne", "Mám rád italskou kulturu")}),
    1184: (LIST, {"t_ru": "тратить, угощать", "t_uk": "витрачати, пригощати", "t_en": "to spend, to buy (a round)",
                  "t_tr": "harcamak, ısmarlamak", "t_pl": "wydawać, postawić", "t_it": "spendere, offrire",
                  "t_es": "gastar, invitar", "t_fr": "dépenser, payer (une tournée)", "t_cs": "utrácet, vydávat"}),
    2057: ("«Поезд идёт с опозданием», «має запізнення» — книжно/калька", {
        "x_ru": "Поезд опаздывает", "x_uk": "Поїзд запізнюється"}),
    # Мой пример у Flug (блок 7) — шаблон этого: «Mein Flug hat Verspätung»
    2467: ("мой пример «Mein Flug hat Verspätung» — шаблон Verspätung («Der Zug hat Verspätung»)", {**all_x(
        "Wir haben den Flug nach Rom gebucht", "Мы забронировали рейс в Рим", "Ми забронювали рейс до Риму",
        "We've booked the flight to Rome", "Roma uçuşunu ayırttık", "Zarezerwowaliśmy lot do Rzymu",
        "Abbiamo prenotato il volo per Roma", "Hemos reservado el vuelo a Roma", "On a réservé le vol pour Rome",
        "Zarezervovali jsme let do Říma")}),
    762: ("«Ich koche nach dem Rezept» — пусто; " + LIST, {
        "t_ru": "рецепт", "t_uk": "рецепт", "t_en": "recipe, prescription", "t_tr": "tarif, reçete",
        "t_pl": "przepis, recepta",
        **all_x("Kannst du mir das Rezept für den Kuchen geben?", "Дашь мне рецепт этого пирога?",
                "Даси мені рецепт цього пирога?", "Can you give me the recipe for the cake?",
                "Bana pastanın tarifini verir misin?", "Dasz mi przepis na to ciasto?", "Mi dai la ricetta della torta?",
                "¿Me das la receta del pastel?", "Tu me donnes la recette du gâteau?", "Dáš mi recept na ten koláč?")}),
    10328: (LIST, {"t_ru": "умный", "t_uk": "розумний", "t_en": "intelligent, clever", "t_tr": "zeki",
                   "t_pl": "inteligentny, bystry"}),
    1073: (EN + " («to the center to shop»); " + LIST, {
        "t_ru": "центр", "t_uk": "центр", "t_en": "centre, city centre", "t_tr": "merkez", "t_pl": "centrum",
        "x_en": "We're going to the centre to do some shopping"}),
    1074: ("«Я пишу записку для тебя» — калька; " + LIST, {
        "t_ru": "записка, бумажка", "t_uk": "записка, папірець", "t_en": "note, slip of paper", "t_tr": "not kağıdı",
        "t_pl": "kartka, karteczka",
        **all_x("Schreib es dir auf einen Zettel", "Запиши это на бумажке", "Запиши це на папірці",
                "Write it down on a piece of paper", "Bunu bir kağıda yaz", "Zapisz to na karteczce",
                "Scrivilo su un foglietto", "Apúntalo en un papelito", "Note-le sur un bout de papier",
                "Napiš si to na lístek")}),
    2961: (EN + " («We are postponing»); " + LIST, {
        "t_ru": "переносить, отложить", "t_uk": "переносити, відкладати", "t_en": "to postpone, to move",
        "t_tr": "ertelemek", "t_pl": "przesunąć, przełożyć",
        **all_x("Können wir den Termin verschieben?", "Можем перенести встречу?", "Можемо перенести зустріч?",
                "Can we move the appointment?", "Randevuyu erteleyebilir miyiz?", "Możemy przesunąć termin?",
                "Possiamo spostare l'appuntamento?", "¿Podemos cambiar la cita?", "On peut reporter le rendez-vous?",
                "Můžeme posunout termín?")}),
    2123: (GO, {**all_x(
        "Die Kinder wollen unbedingt in den Zoo", "Дети очень хотят в зоопарк", "Діти дуже хочуть до зоопарку",
        "The kids are desperate to go to the zoo", "Çocuklar ille de hayvanat bahçesine gitmek istiyor",
        "Dzieci koniecznie chcą iść do zoo", "I bambini vogliono assolutamente andare allo zoo",
        "Los niños quieren ir al zoo como sea", "Les enfants veulent absolument aller au zoo",
        "Děti chtějí za každou cenu do zoo")}),
    533: (SKEL + "; " + LIST, {
        "t_ru": "лампа", "t_uk": "лампа", "t_en": "lamp", "t_tr": "lamba", "t_pl": "lampa",
        **all_x("Kannst du die Lampe anmachen?", "Можешь включить лампу?", "Можеш увімкнути лампу?",
                "Can you switch the lamp on?", "Lambayı açabilir misin?", "Możesz włączyć lampę?",
                "Puoi accendere la lampada?", "¿Puedes encender la lámpara?", "Tu peux allumer la lampe?",
                "Můžeš rozsvítit lampu?")}),
    2458: ("«Это толстая кошка» — пусто; fett — прежде всего о еде", {
        "t_ru": "жирный, толстый", "t_uk": "жирний, товстий", "t_en": "fatty, fat", "t_tr": "yağlı, şişman",
        "t_pl": "tłusty, gruby", "t_it": "grasso", "t_es": "graso, gordo", "t_fr": "gras, gros", "t_cs": "tlustý, mastný",
        **all_x("Das Essen ist mir zu fett", "Для меня эта еда слишком жирная", "Ця їжа для мене надто жирна",
                "The food is too fatty for me", "Bu yemek bana çok yağlı", "To jedzenie jest dla mnie za tłuste",
                "Questo cibo è troppo grasso per me", "Esta comida es demasiado grasa para mí",
                "Ce plat est trop gras pour moi", "To jídlo je na mě moc mastné")}),
    1067: ("«Der Zahn tut weh» — шаблон Bauch, Bein, Ohr", {**all_x(
        "Mein Sohn hat seinen ersten Zahn verloren", "У моего сына выпал первый зуб", "У мого сина випав перший зуб",
        "My son has lost his first tooth", "Oğlumun ilk dişi düştü", "Mojemu synowi wypadł pierwszy ząb",
        "A mio figlio è caduto il primo dente", "A mi hijo se le ha caído el primer diente",
        "Mon fils a perdu sa première dent", "Synovi vypadl první zub")}),
    17781: ("«ausgezeichnet» — книжно; " + LIST, {
        "t_ru": "обслуживание, сервис", "t_uk": "обслуговування, сервіс", "t_en": "service", "t_tr": "servis, hizmet",
        "t_pl": "obsługa, serwis",
        **all_x("Der Service war leider schlecht", "Обслуживание, к сожалению, было плохим",
                "Обслуговування, на жаль, було поганим", "Unfortunately the service was poor", "Maalesef servis kötüydü",
                "Obsługa niestety była słaba", "Purtroppo il servizio era pessimo", "Por desgracia, el servicio fue malo",
                "Malheureusement, le service était mauvais", "Obsluha byla bohužel špatná")}),
}

SPLIT_LATER = {}
