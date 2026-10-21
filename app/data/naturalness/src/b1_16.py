"""B1, блок 16: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    15984: ("«Der Bulle verhaftet den Dieb» — неживо; Bulle — слово улицы", {**all_x(
        "Die Bullen sind schon da!", "Менты уже здесь!", "Менти вже тут!", "The cops are already here!",
        "Aynasızlar geldi bile!", "Gliny już są!", "Gli sbirri sono già qui!", "¡Ya está aquí la poli!",
        "Les flics sont déjà là!", "Poldové už jsou tady!")}),
    2599: ("«Der Kauf des Hauses war …» — книжно", {**all_x(
        "Das war ein guter Kauf", "Это была удачная покупка", "Це була вдала покупка", "That was a good buy",
        "İyi bir satın almaydı", "To był dobry zakup", "È stato un buon acquisto", "Fue una buena compra",
        "C'était un bon achat", "To byl dobrý nákup")}),
    9731: ("«Das Auto ist mein Besitz» — язык протокола", {**all_x(
        "Das Haus ist seit hundert Jahren im Besitz der Familie", "Дом уже сто лет в собственности семьи",
        "Будинок уже сто років у власності родини", "The house has been the family's property for a hundred years",
        "Ev yüz yıldır ailenin mülkü", "Dom od stu lat jest własnością rodziny",
        "La casa è di proprietà della famiglia da cento anni", "La casa es propiedad de la familia desde hace cien años",
        "La maison est la propriété de la famille depuis cent ans", "Dům je už sto let majetkem rodiny")}),
    6614: ("«Der Fisch ist noch lebend» — тот же пример, что был у lebendig", {**all_x(
        "Sie haben ihn lebend gefunden", "Его нашли живым", "Його знайшли живим", "They found him alive",
        "Onu canlı buldular", "Znaleźli go żywego", "L'hanno trovato vivo", "Lo encontraron vivo",
        "On l'a retrouvé vivant", "Našli ho živého")}),
    15986: ("«Der Ritter trägt eine schwere Rüstung» — шаблон одежды", {**all_x(
        "Im Mittelalter gab es viele Ritter", "В Средние века было много рыцарей", "У Середньовіччі було багато лицарів",
        "There were lots of knights in the Middle Ages", "Orta Çağ'da birçok şövalye vardı",
        "W średniowieczu było wielu rycerzy", "Nel Medioevo c'erano molti cavalieri",
        "En la Edad Media había muchos caballeros", "Au Moyen Âge, il y avait beaucoup de chevaliers",
        "Ve středověku bylo hodně rytířů")}),
    18139: ("«Wo ist das Klo?» — шаблон WC («Wo ist das WC?»)", {**all_x(
        "Ich muss mal aufs Klo", "Мне надо в туалет", "Мені треба в туалет", "I need the loo",
        "Tuvalete gitmem lazım", "Muszę iść do kibla", "Devo andare in bagno", "Tengo que ir al baño",
        "Il faut que j'aille aux toilettes", "Musím na záchod")}),
    2402: (EN + " («I welcome guests»)", {"x_en": "I'm receiving guests"}),
    15987: ("«Die Polizei sucht noch den Täter» — шаблон Mörder", {**all_x(
        "Der Täter ist geflohen", "Преступник сбежал", "Злочинець утік", "The offender got away", "Fail kaçtı",
        "Sprawca uciekł", "Il colpevole è fuggito", "El autor ha huido", "Le coupable s'est enfui", "Pachatel utekl")}),
    13473: ("«Solch ein schöner Tag heute» — обрывок", {**all_x(
        "Solche Leute mag ich nicht", "Таких людей я не люблю", "Таких людей я не люблю",
        "I don't like people like that", "Böyle insanları sevmem", "Nie lubię takich ludzi",
        "Persone così non mi piacciono", "No me gusta la gente así", "Je n'aime pas ce genre de personnes",
        "Takové lidi nemám rád")}),
    15421: ("«Die Blumen wachsen sehr schnell» — пусто", {**all_x(
        "Du bist aber gewachsen!", "Как ты вырос!", "Як ти виріс!", "Haven't you grown!", "Ne kadar büyümüşsün!",
        "Ale urosłeś!", "Come sei cresciuto!", "¡Cuánto has crecido!", "Comme tu as grandi!", "Ty jsi ale vyrostl!")}),
    2502: ("«Das ist ein guter Gedanke» — пусто", {**all_x(
        "Der Gedanke an die Prüfung macht mich nervös", "Мысль об экзамене меня нервирует", "Думка про іспит мене нервує",
        "The thought of the exam makes me nervous", "Sınav düşüncesi beni geriyor", "Myśl o egzaminie mnie stresuje",
        "Il pensiero dell'esame mi rende nervoso", "Pensar en el examen me pone nervioso",
        "L'idée de l'examen me rend nerveux", "Myšlenka na zkoušku mě znervózňuje")}),
    12504: ("«Er liegt noch in der Klinik» — шаблон Krankenhaus («Er liegt im Krankenhaus»)", {**all_x(
        "Sie arbeitet in einer Klinik für Kinder", "Она работает в детской клинике", "Вона працює в дитячій клініці",
        "She works at a children's clinic", "Bir çocuk kliniğinde çalışıyor", "Pracuje w klinice dla dzieci",
        "Lavora in una clinica pediatrica", "Trabaja en una clínica infantil",
        "Elle travaille dans une clinique pour enfants", "Pracuje na dětské klinice")}),
    6620: ("ru «никак не справляюсь» — другой смысл (sich zurechtfinden — ориентироваться)", {
        "t_ru": "справляться, ориентироваться", "t_uk": "давати раду, орієнтуватися",
        "x_ru": "Я тут никак не сориентируюсь", "x_uk": "Я тут ніяк не зорієнтуюся"}),
    1550: ("«Der Tisch ist aus Holz» — скелет", {**all_x(
        "Wir haben Holz für den Kamin gekauft", "Мы купили дрова для камина", "Ми купили дрова для каміна",
        "We've bought wood for the fireplace", "Şömine için odun aldık", "Kupiliśmy drewno do kominka",
        "Abbiamo comprato la legna per il camino", "Hemos comprado leña para la chimenea",
        "On a acheté du bois pour la cheminée", "Koupili jsme dřevo do krbu")}),
    15989: ("«Der Offizier trägt eine Uniform» — шаблон одежды", {**all_x(
        "Er ist Offizier bei der Marine", "Он офицер флота", "Він офіцер флоту", "He's an officer in the navy",
        "Donanmada subay", "Jest oficerem marynarki", "È ufficiale di marina", "Es oficial de la marina",
        "Il est officier de marine", "Je důstojníkem u námořnictva")}),
    12506: ("грубое слово — на C1, чтобы не попадалось новичку; в переводе — пометка", {
        "level": "C1",
        "t_ru": "морда, рожа (груб.)", "t_uk": "морда, пика (груб.)", "t_en": "gob, mug (rude)",
        "t_tr": "surat (kaba)", "t_pl": "morda, gęba", "t_it": "il muso (volg.)", "t_es": "la jeta (vulg.)",
        "t_fr": "la gueule (vulg.)", "t_cs": "huba, držka"}),
    12507: ("«Der Krankenwagen kommt schnell» — пусто", {**all_x(
        "Ruf schnell einen Krankenwagen!", "Скорее вызови скорую!", "Швидше виклич швидку!",
        "Call an ambulance, quick!", "Çabuk ambulans çağır!", "Szybko wezwij karetkę!", "Chiama subito un'ambulanza!",
        "¡Llama rápido a una ambulancia!", "Appelle vite une ambulance!", "Rychle zavolej sanitku!")}),
}

# West — то же, что Westen («Richtung West» — так не говорят)
REPLACE = [{"id": 17073, "by": 1031, "lang": "de", "why": "West — вариант Westen; «Richtung West» — так не говорят"}]

SPLIT_LATER = {}
