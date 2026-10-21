"""B1, блок 12: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    15966: ("«Der Soldat trägt ein Gewehr» — шаблон одежды и Soldat", {**all_x(
        "Der Jäger hat sein Gewehr im Auto", "У охотника ружьё в машине", "У мисливця рушниця в машині",
        "The hunter keeps his rifle in the car", "Avcının tüfeği arabada", "Myśliwy ma strzelbę w samochodzie",
        "Il cacciatore tiene il fucile in macchina", "El cazador lleva la escopeta en el coche",
        "Le chasseur a son fusil dans la voiture", "Myslivec má pušku v autě")}),
    1605: ("«Das ist kompliziert» — пусто", {**all_x(
        "Die Anleitung ist total kompliziert", "Инструкция ужасно запутанная", "Інструкція страшенно заплутана",
        "The instructions are really complicated", "Kullanım kılavuzu çok karmaşık", "Instrukcja jest strasznie skomplikowana",
        "Le istruzioni sono complicatissime", "Las instrucciones son complicadísimas", "Le mode d'emploi est super compliqué",
        "Návod je strašně složitý")}),
    2127: ("«Der Zugang ist gesperrt» — табличка", {**all_x(
        "Hast du Zugang zum Internet?", "У тебя есть доступ к интернету?", "У тебе є доступ до інтернету?",
        "Do you have internet access?", "İnternete erişimin var mı?", "Masz dostęp do internetu?",
        "Hai accesso a internet?", "¿Tienes acceso a internet?", "Tu as accès à internet?", "Máš přístup k internetu?")}),
    6548: (LIST, {"t_ru": "ящик, коробка", "t_uk": "ящик, коробка", "t_en": "box, crate", "t_tr": "kutu, sandık",
                  "t_pl": "skrzynka, pudło"}),
    140: ("«Der Schmerz ist in der Brust» — калька, шаблон Schmerz", {**all_x(
        "Die Mutter drückt das Kind an die Brust", "Мать прижимает ребёнка к груди", "Мати пригортає дитину до грудей",
        "The mother holds the child to her chest", "Anne çocuğu göğsüne bastırıyor", "Matka przytula dziecko do piersi",
        "La madre stringe il bambino al petto", "La madre aprieta al niño contra el pecho",
        "La mère serre l'enfant contre sa poitrine", "Matka tiskne dítě k hrudi")}),
    2583: ("«Inzwischen ist viel passiert» — шаблон seitdem («Seitdem ist viel passiert»)", {**all_x(
        "Ich koche, und du deckst inzwischen den Tisch", "Я готовлю, а ты тем временем накрой на стол",
        "Я готую, а ти тим часом накрий на стіл", "I'll cook, and meanwhile you set the table",
        "Ben yemek yapıyorum, sen de bu arada sofrayı kur", "Ja gotuję, a ty tymczasem nakryj do stołu",
        "Io cucino, e tu nel frattempo apparecchi la tavola", "Yo cocino y tú, mientras tanto, pones la mesa",
        "Je cuisine, et toi, entre-temps, tu mets la table", "Já vařím a ty mezitím prostři stůl")}),
    14388: ("«Der Sänger steht auf der Bühne» — шаблон Sänger", {**all_x(
        "Ich habe Angst, auf der Bühne zu stehen", "Я боюсь выходить на сцену", "Я боюся виходити на сцену",
        "I'm scared of being on stage", "Sahneye çıkmaktan korkuyorum", "Boję się występować na scenie",
        "Ho paura di salire sul palco", "Me da miedo subir al escenario", "J'ai peur de monter sur scène",
        "Bojím se stát na pódiu")}),
    6554: ("«Ich will dich nicht hauen» — неживо; hauen — слово детских жалоб", {**all_x(
        "Er hat mich gehauen!", "Он меня ударил!", "Він мене вдарив!", "He hit me!", "Bana vurdu!",
        "On mnie uderzył!", "Mi ha picchiato!", "¡Me ha pegado!", "Il m'a tapé!", "Praštil mě!")}),
    14389: ("«Die Musik hat einen schönen Ton» — неживо", {**all_x(
        "Nicht in diesem Ton, bitte!", "Не таким тоном, пожалуйста!", "Не таким тоном, будь ласка!",
        "Not in that tone, please!", "Bu ses tonuyla değil, lütfen!", "Nie takim tonem, proszę!",
        "Non con questo tono, per favore!", "¡No en ese tono, por favor!", "Pas sur ce ton, s'il te plaît!",
        "Ne tímhle tónem, prosím!")}),
    15409: (LIST, {"t_ru": "территория, область", "t_uk": "територія, галузь", "t_en": "area, field",
                   "t_tr": "bölge, alan", "t_pl": "obszar, dziedzina", "t_it": "la zona, il campo",
                   "t_es": "la zona, el campo", "t_fr": "la zone, le domaine", "t_cs": "oblast, obor"}),
    2911: ("«Ich gehe damit um» — так не говорят; " + LIST, {
        "t_ru": "обращаться (с чем-то), обходить", "t_uk": "поводитися, обходити", "t_en": "to handle, to bypass",
        "t_tr": "davranmak, atlatmak", "t_pl": "obchodzić się, omijać", "t_it": "trattare, aggirare",
        "t_es": "tratar, eludir", "t_fr": "gérer, contourner", "t_cs": "zacházet, obejít",
        **all_x("Er kann gut mit Kindern umgehen", "Он умеет обращаться с детьми", "Він уміє поводитися з дітьми",
                "He knows how to handle children", "Çocuklara nasıl davranılacağını biliyor",
                "Potrafi obchodzić się z dziećmi", "Sa trattare bene i bambini", "Sabe tratar a los niños",
                "Il sait bien gérer les enfants", "Umí zacházet s dětmi")}),
    1917: ("«Я получил штраф» / it «punizione» — разные слова в одном примере", {**all_x(
        "Ich musste 30 Euro Strafe zahlen", "Мне пришлось заплатить штраф 30 евро", "Мені довелося заплатити штраф 30 євро",
        "I had to pay a 30-euro fine", "30 euro ceza ödemek zorunda kaldım", "Musiałem zapłacić 30 euro mandatu",
        "Ho dovuto pagare una multa di 30 euro", "Tuve que pagar una multa de 30 euros",
        "J'ai dû payer une amende de 30 euros", "Musel jsem zaplatit pokutu 30 eur")}),
    15411: ("«Das Gras … ist sehr grün» — скелет", {**all_x(
        "Im Sommer liegen wir gern im Gras", "Летом мы любим лежать на траве", "Улітку ми любимо лежати на траві",
        "In summer we like lying in the grass", "Yazın çimenlerde uzanmayı severiz", "Latem lubimy leżeć na trawie",
        "D'estate ci piace stare sdraiati sull'erba", "En verano nos gusta tumbarnos en la hierba",
        "En été, on aime s'allonger dans l'herbe", "V létě rádi ležíme v trávě")}),
    10198: ("«Der Film macht einen guten Eindruck» — снова Film", {**all_x(
        "Beim ersten Treffen hat sie einen guten Eindruck gemacht", "На первой встрече она произвела хорошее впечатление",
        "На першій зустрічі вона справила гарне враження", "She made a good impression at the first meeting",
        "İlk buluşmada iyi bir izlenim bıraktı", "Na pierwszym spotkaniu zrobiła dobre wrażenie",
        "Al primo incontro ha fatto una buona impressione", "En la primera cita causó buena impresión",
        "Au premier rendez-vous, elle a fait bonne impression", "Na první schůzce udělala dobrý dojem")}),
}

SPLIT_LATER = {}
