"""B1, блок 63: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    14532: ("«Sie ist eine sehr kreative Person» — пусто", {**all_x(
        "Beim Kochen bin ich ziemlich kreativ", "На кухне я довольно креативен", "Коли готую, я досить креативний",
        "I'm pretty creative when I cook", "Yemek yaparken oldukça yaratıcıyım", "W kuchni jestem dość kreatywny",
        "Quando cucino sono piuttosto creativo", "Cocinando soy bastante creativo", "En cuisine, je suis plutôt créatif",
        "Při vaření jsem docela kreativní")}),
    15571: ("«Ein Ast fiel vom Baum herunter» — претерит", {**all_x(
        "Er sägt den Ast ab, auf dem er sitzt", "Он рубит сук, на котором сидит", "Він рубає гілку, на якій сидить",
        "He's sawing off the branch he's sitting on", "Oturduğu dalı kesiyor", "Podcina gałąź, na której siedzi",
        "Sega il ramo su cui è seduto", "Corta la rama en la que está sentado", "Il scie la branche sur laquelle il est assis",
        "Řeže si větev pod sebou")}),
    2212: ("«Die Atmung ist flach» — медкарта", {**all_x(
        "Achte beim Sport auf deine Atmung", "Во время спорта следи за дыханием", "Під час спорту стеж за диханням",
        "Watch your breathing when you exercise", "Spor yaparken nefes alışına dikkat et", "Podczas ćwiczeń uważaj na oddech",
        "Quando fai sport fai attenzione alla respirazione", "Cuando hagas deporte, presta atención a la respiración",
        "Pendant le sport, fais attention à ta respiration", "Při sportu dávej pozor na dýchání")}),
    17193: ("ru «Я должен быстро заправиться» — калька", {"x_ru": "Мне надо быстро заправиться перед выездом"}),
    179: ("«Sie üben einen Dialog» — урок", {**all_x(
        "Im Film gibt es kaum Dialog", "В фильме почти нет диалогов", "У фільмі майже немає діалогів",
        "There's hardly any dialogue in the film", "Filmde neredeyse hiç diyalog yok", "W filmie prawie nie ma dialogów",
        "Nel film non c'è quasi dialogo", "En la película apenas hay diálogo", "Il n'y a presque pas de dialogues dans le film",
        "Ve filmu skoro není dialog")}),
    819: ("«Der Schwiegervater hilft im Garten» — пусто", {**all_x(
        "Mein Schwiegervater kann sehr gut kochen", "Мой тесть отлично готовит", "Мій тесть чудово готує",
        "My father-in-law is a great cook", "Kayınpederim çok güzel yemek yapar", "Mój teść świetnie gotuje",
        "Mio suocero cucina benissimo", "Mi suegro cocina muy bien", "Mon beau-père cuisine très bien", "Tchán výborně vaří")}),
    12212: ("«Es gibt viele Bars …» — шаблон «Es gibt …»", {**all_x(
        "Wir treffen uns um zehn an der Bar", "Встречаемся в десять у барной стойки", "Зустрічаємося о десятій біля барної стійки",
        "Let's meet at the bar at ten", "Onda barda buluşalım", "Spotkajmy się o dziesiątej przy barze",
        "Ci vediamo alle dieci al bar", "Quedamos a las diez en el bar", "On se retrouve au bar à dix heures",
        "Sejdeme se v deset u baru")}),
    2702: ("«bezüglich der Zukunft» — канцелярит", {**all_x(
        "Ich bin optimistisch, dass wir es schaffen", "Я настроен оптимистично: мы справимся",
        "Я оптимістично налаштований, що ми впораємося", "I'm optimistic that we'll make it",
        "Başaracağımız konusunda iyimserim", "Jestem optymistycznie nastawiony, że damy radę",
        "Sono ottimista che ce la faremo", "Soy optimista, lo conseguiremos", "Je suis optimiste, on va y arriver",
        "Jsem optimistický, že to zvládneme")}),
    8947: ("«Die Journalistin schrieb …» — претерит; «female journalist» — лишнее", {
        "t_en": "journalist", "t_tr": "gazeteci",
        **all_x("Sie arbeitet als freie Journalistin", "Она работает журналисткой-фрилансером",
                "Вона працює журналісткою-фрилансеркою", "She works as a freelance journalist",
                "Serbest gazeteci olarak çalışıyor", "Pracuje jako dziennikarka na zlecenie",
                "Lavora come giornalista freelance", "Trabaja como periodista freelance",
                "Elle travaille comme journaliste indépendante", "Pracuje jako novinářka na volné noze")}),
    9510: ("«Mein Notizbuch liegt auf dem Tisch» — пусто", {**all_x(
        "Ich schreibe alles in mein Notizbuch", "Я всё записываю в свой блокнот", "Я все записую в блокнот",
        "I write everything down in my notebook", "Her şeyi not defterime yazıyorum", "Wszystko zapisuję w notesie",
        "Scrivo tutto nel mio taccuino", "Lo apunto todo en mi libreta", "J'écris tout dans mon carnet",
        "Všechno si píšu do zápisníku")}),
    2219: ("«Das ist ein Aufruf zur Hilfe» — пусто", {**all_x(
        "Achtung, letzter Aufruf für den Flug nach Rom", "Внимание, последний вызов на рейс в Рим",
        "Увага, останній виклик на рейс до Рима", "Attention, last call for the flight to Rome",
        "Dikkat, Roma uçuşu için son çağrı", "Uwaga, ostatnie wezwanie na lot do Rzymu",
        "Attenzione, ultima chiamata per il volo per Roma", "Atención, última llamada para el vuelo a Roma",
        "Attention, dernier appel pour le vol à destination de Rome", "Pozor, poslední výzva k letu do Říma")}),
    2016: ("«Ich bin unzufrieden» — пусто", {**all_x(
        "Viele Kunden sind mit dem Service unzufrieden", "Многие клиенты недовольны обслуживанием",
        "Багато клієнтів незадоволені обслуговуванням", "Many customers are unhappy with the service",
        "Birçok müşteri hizmetten memnun değil", "Wielu klientów jest niezadowolonych z obsługi",
        "Molti clienti sono insoddisfatti del servizio", "Muchos clientes están descontentos con el servicio",
        "Beaucoup de clients sont mécontents du service", "Spousta zákazníků je se službou nespokojená")}),
    2748: ("«Wir reduzieren die Kosten» — планёрка", {**all_x(
        "Ich habe den Zucker im Kaffee reduziert", "Я уменьшил сахар в кофе", "Я зменшив цукор у каві",
        "I've cut down on sugar in my coffee", "Kahvedeki şekeri azalttım", "Ograniczyłem cukier w kawie",
        "Ho ridotto lo zucchero nel caffè", "He reducido el azúcar en el café", "J'ai réduit le sucre dans mon café",
        "Omezil jsem cukr v kávě")}),
    15574: ("«Wir spielen auf der Wiese» — пусто", {**all_x(
        "Im Sommer liegen wir oft auf der Wiese im Park", "Летом мы часто лежим на газоне в парке",
        "Улітку ми часто лежимо на галявині в парку", "In summer we often lie on the lawn in the park",
        "Yazın parkta sık sık çimenlere uzanıyoruz", "Latem często leżymy na trawniku w parku",
        "D'estate stiamo spesso sdraiati sul prato del parco", "En verano solemos tumbarnos en el césped del parque",
        "L'été, on s'allonge souvent sur la pelouse du parc", "V létě často ležíme na trávníku v parku")}),
    7409: ("«Ich wähle einen Film aus» — пусто; en «movie»", {**all_x(
        "Der Computer wählt die Gewinner zufällig aus", "Компьютер выбирает победителей случайно",
        "Комп'ютер вибирає переможців випадково", "The computer selects the winners at random",
        "Bilgisayar kazananları rastgele seçiyor", "Komputer losowo wybiera zwycięzców",
        "Il computer sceglie i vincitori a caso", "El ordenador elige a los ganadores al azar",
        "L'ordinateur sélectionne les gagnants au hasard", "Počítač vybírá výherce náhodně")}),
    17194: ("ru «Ты должен повернуть» — калька", {**all_x(
        "Bieg an der nächsten Straße ab", "На следующей улице поверни", "Поверни на наступній вулиці",
        "Turn off at the next street", "Bir sonraki sokaktan dön", "Skręć w następną ulicę", "Gira alla prossima strada",
        "Gira en la próxima calle", "Tourne à la prochaine rue", "Odboč na příští ulici")}),
    17578: (EN + " («elevator» — американское)", {"t_en": "lift, ski lift",
                                                "x_en": "The lift is broken, we'll have to take the stairs"}),
    9824: ("«Ich habe mein Portemonnaie vergessen» — шаблон Zahnbürste («Ich habe meine Zahnbürste vergessen»)", {**all_x(
        "Mir ist das Portemonnaie aus der Tasche gefallen", "У меня кошелёк выпал из кармана", "У мене гаманець випав із кишені",
        "My wallet fell out of my pocket", "Cüzdanım cebimden düştü", "Wypadł mi portfel z kieszeni",
        "Mi è caduto il portafoglio dalla tasca", "Se me ha caído la cartera del bolsillo",
        "Mon portefeuille est tombé de ma poche", "Vypadla mi peněženka z kapsy")}),
    11779: ("«Pass auf, der Pfeffer ist ziemlich scharf» — пусто", {**all_x(
        "Gib mir mal Salz und Pfeffer", "Передай мне соль и перец", "Передай мені сіль і перець",
        "Pass me the salt and pepper", "Bana tuzu ve karabiberi uzatır mısın", "Podaj mi sól i pieprz",
        "Passami il sale e il pepe", "Pásame la sal y la pimienta", "Passe-moi le sel et le poivre", "Podej mi sůl a pepř")}),
}

SPLIT_LATER = {}
