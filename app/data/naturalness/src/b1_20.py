"""B1, блок 20: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2657: ("снова Projekt; " + LIST, {
        "t_ru": "руководить, вести", "t_uk": "керувати, вести", "t_en": "to lead, to run", "t_tr": "yönetmek",
        "t_pl": "kierować, prowadzić", "t_it": "dirigere, gestire", "t_es": "dirigir, gestionar", "t_fr": "diriger, gérer",
        "t_cs": "vést, řídit",
        **all_x("Wer leitet die Firma?", "Кто руководит фирмой?", "Хто керує фірмою?", "Who runs the company?",
                "Şirketi kim yönetiyor?", "Kto kieruje firmą?", "Chi dirige l'azienda?", "¿Quién dirige la empresa?",
                "Qui dirige l'entreprise?", "Kdo vede firmu?")}),
    2023: ("ru «встреча» / uk «побачення» — разные слова в одном примере", {**all_x(
        "Ich habe heute Abend eine Verabredung", "У меня сегодня вечером свидание", "У мене сьогодні ввечері побачення",
        "I've got a date tonight", "Bu akşam bir buluşmam var", "Mam dziś wieczorem randkę",
        "Stasera ho un appuntamento", "Esta noche tengo una cita", "Ce soir, j'ai un rendez-vous",
        "Dneska večer mám rande")}),
    14402: ("«Der Zauberer macht einen Zauber» — масло масляное", {**all_x(
        "Der Ort hat einen besonderen Zauber", "У этого места особое очарование", "Це місце має особливу чарівність",
        "The place has a special charm", "Burasının özel bir cazibesi var", "To miejsce ma szczególny urok",
        "Il posto ha un fascino particolare", "El lugar tiene un encanto especial",
        "L'endroit a un charme particulier", "To místo má zvláštní kouzlo")}),
    2517: ("«Der Geruch ist unangenehm» — пусто", {**all_x(
        "Ich mag den Geruch von frischem Kaffee", "Я люблю запах свежего кофе", "Я люблю запах свіжої кави",
        "I love the smell of fresh coffee", "Taze kahve kokusunu seviyorum", "Uwielbiam zapach świeżej kawy",
        "Adoro l'odore del caffè fresco", "Me encanta el olor a café recién hecho", "J'adore l'odeur du café frais",
        "Miluju vůni čerstvé kávy")}),
    10247: ("«Das Haus ist unheimlich dunkel» — значение «жутко» потеряно; " + LIST, {
        "t_ru": "жуткий, ужасно", "t_uk": "моторошний, страшенно", "t_en": "creepy, incredibly",
        "t_tr": "ürkütücü, inanılmaz", "t_pl": "upiorny, strasznie", "t_it": "inquietante, incredibilmente",
        "t_es": "inquietante, increíblemente", "t_fr": "inquiétant, incroyablement", "t_cs": "strašidelný, strašně",
        **all_x("Nachts ist es im Wald unheimlich", "Ночью в лесу жутко", "Уночі в лісі моторошно",
                "It's creepy in the forest at night", "Gece ormanda ürkütücü", "W nocy w lesie jest upiornie",
                "Di notte nel bosco è inquietante", "De noche el bosque es inquietante",
                "La nuit, la forêt est inquiétante", "V noci je v lese strašidelně")}),
    2179: ("десятый пример про погоду", {**all_x(
        "Er hat eine angenehme Stimme", "У него приятный голос", "У нього приємний голос", "He has a pleasant voice",
        "Hoş bir sesi var", "Ma przyjemny głos", "Ha una voce piacevole", "Tiene una voz agradable",
        "Il a une voix agréable", "Má příjemný hlas")}),
    2589: ("пример — обрывок", {**all_x(
        "Das Haus ist aus dem 18. Jahrhundert", "Этот дом XVIII века", "Цей будинок вісімнадцятого століття",
        "The house dates from the 18th century", "Ev 18. yüzyıldan kalma", "Ten dom pochodzi z XVIII wieku",
        "La casa è del diciottesimo secolo", "La casa es del siglo XVIII", "La maison date du XVIIIe siècle",
        "Ten dům je z 18. století")}),
    14403: ("«Ich lese einen Roman» — пусто", {**all_x(
        "Sie schreibt gerade an ihrem ersten Roman", "Она сейчас пишет свой первый роман", "Вона зараз пише свій перший роман",
        "She's working on her first novel", "Şu sıralar ilk romanını yazıyor", "Pisze właśnie swoją pierwszą powieść",
        "Sta scrivendo il suo primo romanzo", "Está escribiendo su primera novela",
        "Elle écrit en ce moment son premier roman", "Právě píše svůj první román")}),
    12521: ("«Die Wunde tut noch weh» — шаблон «tut weh»", {**all_x(
        "Die Wunde muss genäht werden", "Рану нужно зашить", "Рану треба зашити", "The wound needs stitches",
        "Yaranın dikilmesi gerekiyor", "Ranę trzeba zszyć", "La ferita va ricucita", "Hay que coser la herida",
        "Il faut recoudre la plaie", "Ránu je potřeba sešít")}),
    8785: ("«Der Manager kommt gleich» — пусто", {**all_x(
        "Ich möchte mit dem Manager sprechen", "Я хочу поговорить с менеджером", "Я хочу поговорити з менеджером",
        "I'd like to speak to the manager", "Müdürle konuşmak istiyorum", "Chciałbym porozmawiać z menedżerem",
        "Vorrei parlare con il manager", "Quiero hablar con el gerente", "Je voudrais parler au manager",
        "Chtěl bych mluvit s manažerem")}),
    16007: ("«Jemand will mein Auto klauen» — шаблон stehlen", {**all_x(
        "Wer hat meinen Kuli geklaut?", "Кто стащил мою ручку?", "Хто стягнув мою ручку?", "Who's nicked my pen?",
        "Kalemimi kim aşırdı?", "Kto zwędził mój długopis?", "Chi mi ha fregato la penna?", "¿Quién me ha birlado el boli?",
        "Qui m'a piqué mon stylo?", "Kdo mi šlohnul propisku?")}),
    9450: ("«Die Korrektur ist fertig» — пусто", {**all_x(
        "Danke für die Korrektur!", "Спасибо за исправление!", "Дякую за виправлення!", "Thanks for the correction!",
        "Düzeltme için teşekkürler!", "Dzięki za poprawkę!", "Grazie per la correzione!", "¡Gracias por la corrección!",
        "Merci pour la correction!", "Díky za opravu!")}),
    10253: ("«Bitte nicht berühren» — табличка в музее", {**all_x(
        "Der Film hat mich sehr berührt", "Фильм меня очень растрогал", "Фільм мене дуже розчулив",
        "The film really moved me", "Film beni çok duygulandırdı", "Ten film bardzo mnie wzruszył",
        "Il film mi ha commosso molto", "La película me conmovió mucho", "Le film m'a beaucoup ému",
        "Ten film mě hodně dojal")}),
    10256: ("«Du bist ein Dummkopf» — шаблон Trottel, Idiot", {**all_x(
        "Ich Dummkopf habe das Licht angelassen", "Я, дурак, оставил свет включённым", "Я, дурень, залишив світло увімкненим",
        "Like an idiot, I left the light on", "Ben aptal ışığı açık bıraktım", "Ja, głupek, zostawiłem włączone światło",
        "Io, scemo, ho lasciato la luce accesa", "Yo, tonto de mí, me dejé la luz encendida",
        "Moi, l'idiot, j'ai laissé la lumière allumée", "Já hlupák jsem nechal rozsvícené světlo")}),
    3008: ("«Lass uns weitergehen» — шаблон weitermachen («Lass uns einfach weitermachen»)", {**all_x(
        "So kann es nicht weitergehen!", "Так дальше продолжаться не может!", "Так далі продовжуватися не може!",
        "It can't go on like this!", "Böyle devam edemez!", "Tak dalej toczyć się nie może!",
        "Così non si può andare avanti!", "¡Así no se puede seguir!", "Ça ne peut pas continuer comme ça!",
        "Takhle to dál pokračovat nemůže!")}),
}

SPLIT_LATER = {}
