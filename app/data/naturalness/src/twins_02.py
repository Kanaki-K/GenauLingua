"""Примеры-шаблоны, внесённые вычиткой в блоках 02–35 (проверка шаблонов 21.10).

Проверка «отличаются одним смысловым словом» по 315 переписанным примерам
дала 32 предупреждения; живых — 18, остальное — совпадение двух общих слов
у разных по смыслу фраз (die/jammern, Leute/freundlich). Правится обычно
мой пример; там, где мой точнее, — чужой (zweiter, hängen-соседи).
"""

WHY = "пример-шаблон: та же фраза, другое одно слово (проверка шаблонов 21.10)"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    13464: (WHY + " — zweiter («Das ist mein zweiter Versuch heute»)", {**all_x(
        "Nimm die dritte Straße links", "Сверни на третью улицу налево", "Зверни на третю вулицю ліворуч",
        "Take the third street on the left", "Soldan üçüncü sokağa dön", "Skręć w trzecią ulicę w lewo",
        "Prendi la terza strada a sinistra", "Coge la tercera calle a la izquierda",
        "Prends la troisième rue à gauche", "Odboč do třetí ulice vlevo")}),
    13484: (WHY + " — zweit («Das ist schon mein zweiter Kaffee heute»)", {**all_x(
        "Beim zweiten Mal hat es geklappt", "Со второго раза получилось", "З другого разу вийшло",
        "It worked the second time", "İkinci seferde oldu", "Za drugim razem się udało",
        "La seconda volta è andata bene", "A la segunda salió bien", "Ça a marché la deuxième fois",
        "Napodruhé to vyšlo")}),
    847: (WHY + " — erwachsen («Mein Bruder ist schon erwachsen»)", {**all_x(
        "Mein Sohn geht in die erste Klasse", "Мой сын ходит в первый класс", "Мій син ходить у перший клас",
        "My son's in his first year at school", "Oğlum birinci sınıfa gidiyor", "Mój syn chodzi do pierwszej klasy",
        "Mio figlio fa la prima elementare", "Mi hijo va a primero de primaria",
        "Mon fils est en première année d'école", "Můj syn chodí do první třídy")}),
    1066: (WHY + " — bar («Kann ich bar zahlen?»)", {**all_x(
        "Wir möchten bitte zahlen", "Мы хотели бы расплатиться", "Ми б хотіли розрахуватися",
        "We'd like to pay, please", "Hesabı ödemek istiyoruz", "Chcielibyśmy zapłacić",
        "Vorremmo pagare, per favore", "Queríamos pagar, por favor", "On voudrait payer, s'il vous plaît",
        "Chtěli bychom zaplatit")}),
    90: (WHY + " — Bauch («Der Bauch tut mir weh»)", {**all_x(
        "Ich habe mir das Bein gebrochen", "Я сломал ногу", "Я зламав ногу", "I've broken my leg", "Bacağımı kırdım",
        "Złamałem nogę", "Mi sono rotto la gamba", "Me he roto la pierna", "Je me suis cassé la jambe",
        "Zlomil jsem si nohu")}),
    692: (WHY + " — Koffer («Hast du schon den Koffer gepackt?») и einpacken", {**all_x(
        "Ich habe den ganzen Abend gepackt", "Я весь вечер собирал вещи", "Я весь вечір пакував речі",
        "I spent the whole evening packing", "Bütün akşam bavul hazırladım", "Cały wieczór się pakowałem",
        "Ho passato tutta la sera a fare le valigie", "Me he pasado toda la tarde haciendo la maleta",
        "J'ai passé toute la soirée à faire ma valise", "Celý večer jsem balil")}),
    266: (WHY + " — ausmachen («Mach bitte den Fernseher aus»)", {**all_x(
        "Wir haben einen neuen Fernseher gekauft", "Мы купили новый телевизор", "Ми купили новий телевізор",
        "We've bought a new TV", "Yeni bir televizyon aldık", "Kupiliśmy nowy telewizor",
        "Abbiamo comprato un televisore nuovo", "Hemos comprado una tele nueva", "On a acheté une nouvelle télé",
        "Koupili jsme novou televizi")}),
    419: (WHY + " — über («Das Bild hängt über dem Sofa»)", {**all_x(
        "Häng deine Jacke an den Haken", "Повесь куртку на крючок", "Повісь куртку на гачок",
        "Hang your jacket on the hook", "Ceketini askıya as", "Powieś kurtkę na wieszaku",
        "Appendi la giacca all'attaccapanni", "Cuelga la chaqueta en el perchero",
        "Accroche ta veste au portemanteau", "Pověs si bundu na háček")}),
    45: (WHY + " — Finger («Er verletzt sich am Finger»)", {**all_x(
        "Sie nimmt das Baby auf den Arm", "Она берёт малыша на руки", "Вона бере малюка на руки",
        "She picks the baby up in her arms", "Bebeği kollarına alıyor", "Bierze dziecko na ręce",
        "Prende in braccio il bambino", "Coge al bebé en brazos", "Elle prend le bébé dans ses bras",
        "Bere miminko na ruce")}),
    384: (WHY + " — Schüler («Der Schüler macht Hausaufgaben»)", {**all_x(
        "Hast du deine Hausaufgaben schon gemacht?", "Ты уже сделал домашнее задание?",
        "Ти вже зробив домашнє завдання?", "Have you done your homework yet?", "Ödevini yaptın mı?",
        "Zrobiłeś już zadanie domowe?", "Hai già fatto i compiti?", "¿Ya has hecho los deberes?",
        "Tu as déjà fait tes devoirs?", "Už máš hotové úkoly?")}),
    18109: (WHY + " — Rücksitz («Die Kinder sitzen auf dem Rücksitz»)", {**all_x(
        "Mir ist der Teller auf den Boden gefallen", "У меня тарелка упала на пол", "У мене тарілка впала на підлогу",
        "I dropped the plate on the floor", "Tabak yere düştü", "Talerz spadł mi na podłogę",
        "Mi è caduto il piatto per terra", "Se me ha caído el plato al suelo",
        "J'ai fait tomber l'assiette sur le sol", "Spadl mi talíř na podlahu")}),
    249: (WHY + " — stürzen («Pass auf, dass du nicht stürzt»)", {**all_x(
        "Ich bin vom Fahrrad gefallen", "Я упал с велосипеда", "Я впав з велосипеда", "I fell off my bike",
        "Bisikletten düştüm", "Spadłem z roweru", "Sono caduto dalla bici", "Me he caído de la bici",
        "Je suis tombé de vélo", "Spadl jsem z kola")}),
    322: (WHY + " — gemeinsam B1 («Wir haben viele gemeinsame Interessen»)", {**all_x(
        "Lass uns das gemeinsam machen", "Давай сделаем это вместе", "Давай зробимо це разом", "Let's do it together",
        "Bunu birlikte yapalım", "Zróbmy to razem", "Facciamolo insieme", "Hagámoslo juntos", "Faisons-le ensemble",
        "Udělejme to společně")}),
    615: (WHY + " — immer («Ich trinke immer Kaffee am Morgen»)", {**all_x(
        "Morgens bin ich immer müde", "По утрам я всегда сонный", "Вранці я завжди сонний",
        "I'm always tired in the mornings", "Sabahları hep yorgunum", "Rano zawsze jestem zmęczony",
        "La mattina sono sempre stanco", "Por las mañanas siempre estoy cansado", "Le matin, je suis toujours fatigué",
        "Ráno jsem vždycky unavený")}),
    397: (WHY + " — bügeln («Ich muss heute noch die Hemden bügeln»)", {**all_x(
        "Zieh doch das blaue Hemd an", "Надень лучше синюю рубашку", "Вдягни краще синю сорочку",
        "Why don't you wear the blue shirt?", "Mavi gömleği giysene", "Załóż tę niebieską koszulę",
        "Mettiti la camicia blu", "Ponte la camisa azul", "Mets donc la chemise bleue", "Vezmi si tu modrou košili")}),
    222: (WHY + " — eng B2 («Die Straße ist sehr eng und dunkel»)", {**all_x(
        "Der Parkplatz ist ziemlich eng", "Парковка довольно тесная", "Парковка досить тісна",
        "The parking space is pretty tight", "Otopark oldukça dar", "Parking jest dość ciasny",
        "Il parcheggio è piuttosto stretto", "El aparcamiento es bastante estrecho",
        "La place de parking est assez étroite", "Parkoviště je dost těsné")}),
    686: (WHY + " — West («Wir fahren Richtung West»)", {**all_x(
        "Im Osten ist es im Winter sehr kalt", "На востоке зимой очень холодно", "На сході взимку дуже холодно",
        "It's very cold in the east in winter", "Doğuda kışın hava çok soğuk", "Na wschodzie zimą jest bardzo zimno",
        "A est d'inverno fa molto freddo", "En el este hace mucho frío en invierno",
        "Dans l'est, il fait très froid en hiver", "Na východě je v zimě velká zima")}),
    698: (WHY + " — Bushaltestelle («Die Bushaltestelle ist gleich um die Ecke»)", {**all_x(
        "Am Sonntag waren wir im Park spazieren", "В воскресенье мы гуляли в парке", "У неділю ми гуляли в парку",
        "On Sunday we went for a walk in the park", "Pazar günü parkta yürüyüş yaptık",
        "W niedzielę spacerowaliśmy po parku", "Domenica abbiamo fatto una passeggiata al parco",
        "El domingo dimos un paseo por el parque", "Dimanche, on s'est promenés dans le parc",
        "V neděli jsme se procházeli v parku")}),
}

SPLIT_LATER = {}
