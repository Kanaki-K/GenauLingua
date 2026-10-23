"""Вычитка немецкого, порция p023 (B1), 23.10: природа, животные — заглушки → живые бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    15409: (W, ex("In diesem Gebiet gibt es kaum Handyempfang",
        "В этом районе почти нет связи", "У цьому районі майже немає зв'язку",
        "There's hardly any phone signal in this area", "Bu bölgede neredeyse hiç telefon çekmiyor",
        "Na tym terenie prawie nie ma zasięgu", "In questa zona il cellulare non prende quasi",
        "En esta zona casi no hay cobertura", "Dans cette région, il n'y a presque pas de réseau",
        "V téhle oblasti skoro není signál")),
    15417: (W, ex("Hinter unserem Haus beginnen gleich die Felder",
        "Сразу за нашим домом начинаются поля", "Одразу за нашим будинком починаються поля",
        "The fields start right behind our house", "Evimizin hemen arkasında tarlalar başlıyor",
        "Zaraz za naszym domem zaczynają się pola", "Subito dietro casa nostra cominciano i campi",
        "Justo detrás de nuestra casa empiezan los campos", "Juste derrière notre maison, il y a les champs",
        "Hned za naším domem začínají pole")),
    15419: (W, ex("Bei der Explosion in der Nachbarstraße haben bei uns die Fenster gewackelt",
        "От взрыва на соседней улице у нас дрожали окна", "Від вибуху на сусідній вулиці в нас тремтіли вікна",
        "When the explosion happened in the next street our windows shook", "Yan sokaktaki patlamada bizim camlar sallandı",
        "Przy wybuchu na sąsiedniej ulicy trzęsły się u nas okna", "Con l'esplosione nella strada accanto da noi tremavano i vetri",
        "Con la explosión en la calle de al lado nos temblaron las ventanas", "Lors de l'explosion dans la rue d'à côté, nos fenêtres ont tremblé",
        "Při výbuchu ve vedlejší ulici se nám třásla okna")),
    15424: (W, ex("Die Katze vom Nachbarn hält unseren Garten für ihr Revier",
        "Соседская кошка считает наш сад своей территорией", "Сусідська кішка вважає наш сад своєю територією",
        "The neighbours' cat thinks our garden is her territory", "Komşunun kedisi bahçemizi kendi bölgesi sanıyor",
        "Kot sąsiadów uważa nasz ogród za swój rewir", "La gatta dei vicini considera il nostro giardino il suo territorio",
        "La gata del vecino cree que nuestro jardín es su territorio", "La chatte des voisins considère notre jardin comme son territoire",
        "Sousedova kočka považuje naši zahradu za svůj revír")),
    15429: (W, ex("Im Herbst lassen wir mit den Kindern Drachen steigen",
        "Осенью мы с детьми запускаем воздушных змеев", "Восени ми з дітьми запускаємо повітряних зміїв",
        "In autumn we fly kites with the kids", "Sonbaharda çocuklarla uçurtma uçuruyoruz",
        "Jesienią puszczamy z dziećmi latawce", "In autunno facciamo volare gli aquiloni con i bambini",
        "En otoño volamos cometas con los niños", "En automne, on fait voler des cerfs-volants avec les enfants",
        "Na podzim pouštíme s dětmi draky")),
    15448: (W, ex("Im Kinderzimmer sieht es aus wie im Dschungel",
        "В детской как в джунглях", "У дитячій кімнаті як у джунглях",
        "The children's room looks like a jungle", "Çocuk odası balta girmemiş orman gibi",
        "W pokoju dziecięcym jest jak w dżungli", "La cameretta dei bambini sembra una giungla",
        "El cuarto de los niños parece una selva", "La chambre des enfants ressemble à une jungle",
        "V dětském pokoji to vypadá jako v džungli")),
    15454: (W, ex("Kannst du am Wochenende unsere Fische füttern?",
        "Можешь на выходных покормить наших рыбок?", "Можеш на вихідних погодувати наших рибок?",
        "Can you feed our fish at the weekend?", "Hafta sonu balıklarımızı besleyebilir misin?",
        "Możesz w weekend nakarmić nasze rybki?", "Puoi dare da mangiare ai nostri pesci nel fine settimana?",
        "¿Puedes dar de comer a nuestros peces el fin de semana?", "Tu peux nourrir nos poissons ce week-end ?",
        "Můžeš o víkendu nakrmit naše rybičky?")),
    15459: (W, ex("Auf dem Bauernhof hat die Sau zwölf Ferkel bekommen",
        "На ферме свиноматка принесла двенадцать поросят", "На фермі свиноматка привела дванадцять поросят",
        "On the farm the sow has had twelve piglets", "Çiftlikte dişi domuz on iki yavru doğurdu",
        "Na farmie maciora urodziła dwanaście prosiąt", "Alla fattoria la scrofa ha fatto dodici maialini",
        "En la granja la cerda ha tenido doce lechones", "À la ferme, la truie a eu douze porcelets",
        "Na statku měla svině dvanáct selat")),
    15925: (W, ex("Im Handgepäck darf man keine Waffen mitnehmen",
        "В ручной клади нельзя провозить оружие", "У ручній поклажі не можна провозити зброю",
        "You can't take weapons in your hand luggage", "El bagajında silah taşınamaz",
        "W bagażu podręcznym nie wolno przewozić broni", "Nel bagaglio a mano non si possono portare armi",
        "En el equipaje de mano no se pueden llevar armas", "On n'a pas le droit d'emporter des armes en bagage cabine",
        "V příručním zavazadle se nesmí vozit zbraně")),
}

REPLACE = []

SPLIT_LATER = {}
