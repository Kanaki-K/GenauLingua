"""B1, блок 23: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2451: ("«Das ist reine Fantasie» — пусто", {**all_x(
        "Du hast aber viel Fantasie!", "Ну и фантазия у тебя!", "Ну й фантазія в тебе!", "You've got some imagination!",
        "Ne hayal gücün var!", "Ale masz wyobraźnię!", "Che fantasia che hai!", "¡Qué imaginación tienes!",
        "Tu as de l'imagination!", "Ty máš ale fantazii!")}),
    10269: ("«… sehr unhöflich von dir» — шаблон «… von dir»", {**all_x(
        "Es ist unhöflich, mit vollem Mund zu sprechen", "Невежливо разговаривать с полным ртом",
        "Нечемно розмовляти з повним ротом", "It's rude to talk with your mouth full", "Ağzı dolu konuşmak kabalıktır",
        "Mówienie z pełnymi ustami jest niegrzeczne", "È maleducato parlare con la bocca piena",
        "Es de maleducados hablar con la boca llena", "C'est impoli de parler la bouche pleine",
        "Je nezdvořilé mluvit s plnou pusou")}),
    14409: ("«Wir gehen heute ins Studio» — пусто; " + LIST, {
        "t_ru": "студия, спортзал", "t_uk": "студія, спортзал", "t_en": "studio, gym", "t_tr": "stüdyo, spor salonu",
        "t_pl": "studio, siłownia", "t_it": "lo studio, la palestra", "t_es": "el estudio, el gimnasio",
        "t_fr": "le studio, la salle de sport", "t_cs": "studio, posilovna",
        **all_x("Die Band nimmt im Studio ein neues Album auf", "Группа записывает в студии новый альбом",
                "Гурт записує в студії новий альбом", "The band is recording a new album in the studio",
                "Grup stüdyoda yeni bir albüm kaydediyor", "Zespół nagrywa w studiu nowy album",
                "La band registra un nuovo album in studio", "El grupo graba un nuevo disco en el estudio",
                "Le groupe enregistre un nouvel album en studio", "Kapela nahrává ve studiu nové album")}),
    9746: ("«Der König trägt eine goldene Krone» — шаблон одежды", {**all_x(
        "Ich brauche eine neue Krone für meinen Zahn", "Мне нужна новая коронка на зуб", "Мені потрібна нова коронка на зуб",
        "I need a new crown on my tooth", "Dişim için yeni bir kron lazım", "Potrzebuję nowej korony na ząb",
        "Mi serve una nuova corona per il dente", "Necesito una corona nueva para la muela",
        "J'ai besoin d'une nouvelle couronne pour ma dent", "Potřebuju novou korunku na zub")}),
    13483: ("«keinerlei Interesse an Sport» — шаблон Interesse", {**all_x(
        "Es gibt keinerlei Probleme", "Никаких проблем нет", "Жодних проблем немає", "There are no problems at all",
        "Hiçbir sorun yok", "Nie ma żadnych problemów", "Non c'è nessun problema", "No hay ningún problema",
        "Il n'y a aucun problème", "Nejsou vůbec žádné problémy")}),
    6703: ("«Das Essen war hervorragend» — шаблон prima, ausgezeichnet", {**all_x(
        "Sie spricht hervorragend Englisch", "Она превосходно говорит по-английски", "Вона чудово розмовляє англійською",
        "She speaks excellent English", "Mükemmel İngilizce konuşuyor", "Znakomicie mówi po angielsku",
        "Parla un inglese eccellente", "Habla un inglés excelente", "Elle parle un anglais excellent",
        "Výborně mluví anglicky")}),
    2052: ("«Ich habe eine Versicherung» — пусто; «Die Versicherung zahlt …» — у Schaden", {**all_x(
        "Ohne Versicherung fahre ich nicht ins Ausland", "Без страховки я за границу не поеду",
        "Без страховки я за кордон не поїду", "I don't travel abroad without insurance", "Sigortasız yurt dışına çıkmam",
        "Bez ubezpieczenia nie jadę za granicę", "Senza assicurazione non vado all'estero",
        "Sin seguro no viajo al extranjero", "Je ne pars pas à l'étranger sans assurance",
        "Bez pojištění do zahraničí nejedu")}),
    6705: ("«Komm mal her» — шаблон hierher («Komm mal hierher!»)", {**all_x(
        "Hilf mir mal kurz!", "Помоги-ка мне на минутку!", "Допоможи-но мені на хвилинку!",
        "Can you just help me for a second?", "Bir saniye yardım eder misin?", "Pomóż mi no na chwilę!",
        "Mi aiuti un attimo?", "¿Me ayudas un momento?", "Tu peux m'aider un peu?", "Pomůžeš mi na chvilku?")}),
    16020: ("«Die Bomben haben die Stadt zerstört» — хроника; шаблон zerstören", {**all_x(
        "Die Nachricht ist wie eine Bombe eingeschlagen", "Новость произвела эффект разорвавшейся бомбы",
        "Новина вибухнула, як бомба", "The news came as a bombshell", "Haber bomba gibi düştü",
        "Wiadomość spadła jak bomba", "La notizia è scoppiata come una bomba", "La noticia cayó como una bomba",
        "La nouvelle a fait l'effet d'une bombe", "Zpráva zapůsobila jako bomba")}),
    12524: ("«Meine Kehle tut weh» — шаблон «tut weh»", {**all_x(
        "Ich habe eine trockene Kehle", "У меня пересохло в горле", "У мене пересохло в горлі", "My throat is dry",
        "Boğazım kurudu", "Zaschło mi w gardle", "Ho la gola secca", "Tengo la garganta seca", "J'ai la gorge sèche",
        "Mám vyschlo v krku")}),
    772: ("ru «убирает» / es «vaciar» — разные значения в одном примере", {**all_x(
        "Bis Freitag müssen wir die Wohnung räumen", "До пятницы нам нужно освободить квартиру",
        "До п'ятниці нам треба звільнити квартиру", "We have to vacate the flat by Friday",
        "Daireyi cumaya kadar boşaltmamız lazım", "Do piątku musimy opróżnić mieszkanie",
        "Entro venerdì dobbiamo liberare l'appartamento", "Tenemos que vaciar el piso antes del viernes",
        "On doit libérer l'appartement d'ici vendredi", "Do pátku musíme vyklidit byt")}),
    2885: ("«Mein Hund ist treu» — пусто", {**all_x(
        "Er ist seiner Frau immer treu geblieben", "Он всегда был верен своей жене", "Він завжди був вірний своїй дружині",
        "He's always been faithful to his wife", "Karısına hep sadık kaldı", "Zawsze był wierny swojej żonie",
        "È sempre rimasto fedele a sua moglie", "Siempre le ha sido fiel a su mujer",
        "Il est toujours resté fidèle à sa femme", "Své ženě zůstal vždycky věrný")}),
    1977: ("«Es gab einen Überfall» — пусто", {**all_x(
        "Gestern gab es einen Überfall auf die Bank", "Вчера был налёт на банк", "Учора був наліт на банк",
        "There was a robbery at the bank yesterday", "Dün bankaya bir soygun yapıldı", "Wczoraj był napad na bank",
        "Ieri c'è stata una rapina in banca", "Ayer hubo un atraco al banco", "Hier, il y a eu un braquage à la banque",
        "Včera došlo k přepadení banky")}),
    6710: ("«Pack deinen Kram zusammen» — тот же пример, что у Zeug", {**all_x(
        "Ich habe keine Lust auf den ganzen Kram", "Неохота мне возиться со всей этой ерундой",
        "Не хочеться мені возитися з усією цією морокою", "I can't be bothered with all that stuff",
        "Bu işlerle uğraşmaya hiç hevesim yok", "Nie chce mi się zajmować tym całym bałaganem",
        "Non ho voglia di tutta questa roba", "No tengo ganas de todo ese rollo",
        "J'ai pas envie de tout ce bazar", "Nemám chuť na ty všechny krámy")}),
    12526: ("«Er ist angeschossen» — пусто; ru «ранен выстрелом» — канцелярит", {**all_x(
        "Der Jäger hat ein Reh angeschossen", "Охотник подстрелил косулю", "Мисливець підстрелив козулю",
        "The hunter wounded a deer", "Avcı bir karacayı yaraladı", "Myśliwy postrzelił sarnę",
        "Il cacciatore ha ferito un capriolo", "El cazador hirió a un corzo", "Le chasseur a blessé un chevreuil",
        "Myslivec postřelil srnu")}),
    16022: ("«Die bewaffneten Männer sind gefährlich» — пусто", {**all_x(
        "Der Täter ist bewaffnet", "Преступник вооружён", "Злочинець озброєний", "The suspect is armed",
        "Fail silahlı", "Sprawca jest uzbrojony", "Il colpevole è armato", "El autor está armado",
        "L'auteur est armé", "Pachatel je ozbrojený")}),
    2724: ("«Das Hotel hat einen Pool» — пусто", {**all_x(
        "Die Kinder sind den ganzen Tag im Pool", "Дети целый день в бассейне", "Діти цілий день у басейні",
        "The kids are in the pool all day", "Çocuklar bütün gün havuzda", "Dzieci cały dzień siedzą w basenie",
        "I bambini stanno tutto il giorno in piscina", "Los niños se pasan el día en la piscina",
        "Les enfants sont dans la piscine toute la journée", "Děti jsou celý den v bazénu")}),
    12525: ("«Nach dem Lauf fehlte mir der Atem» — претерит", {**all_x(
        "Ich bin völlig außer Atem", "Я совсем запыхался", "Я зовсім захекався", "I'm completely out of breath",
        "Nefes nefese kaldım", "Jestem zupełnie zdyszany", "Sono senza fiato", "Estoy sin aliento",
        "Je suis complètement essoufflé", "Jsem úplně bez dechu")}),
    18666: ("en «Let me think in peace first» — так не говорят", {**all_x(
        "Jetzt essen wir erstmal, dann sehen wir weiter", "Сначала поедим, а там видно будет",
        "Спершу поїмо, а там видно буде", "Let's eat first, then we'll see", "Önce bir yiyelim, sonra bakarız",
        "Najpierw zjedzmy, potem się zobaczy", "Prima mangiamo, poi vediamo", "Primero comemos y luego ya veremos",
        "D'abord on mange, après on verra", "Nejdřív se najíme a pak se uvidí")}),
    14983: ("«Das Mädel ist wirklich nett» — пусто; разговорное слово", {**all_x(
        "Na, Mädels, wie geht's?", "Ну что, девчонки, как дела?", "Ну що, дівчата, як справи?",
        "Hey girls, how's it going?", "Eee kızlar, nasılsınız?", "No i jak, dziewczyny?", "Allora, ragazze, come va?",
        "¿Qué tal, chicas?", "Alors, les filles, ça va?", "Tak co, holky, jak to jde?")}),
    6708: ("«Der Schnee kann … verwandeln» — открытка", {**all_x(
        "Im Winter verwandelt sich der See in eine Eisbahn", "Зимой озеро превращается в каток",
        "Узимку озеро перетворюється на ковзанку", "In winter the lake turns into an ice rink",
        "Kışın göl buz pistine dönüşüyor", "Zimą jezioro zamienia się w lodowisko",
        "D'inverno il lago si trasforma in una pista di pattinaggio", "En invierno el lago se convierte en una pista de hielo",
        "En hiver, le lac se transforme en patinoire", "V zimě se jezero mění v kluziště")}),
}

SPLIT_LATER = {}
