"""B1, блок 64: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    11780: ("«Der See war völlig eingefroren» — претерит; " + LIST, {
        "t_ru": "замороженный, замёрзший", "t_uk": "заморожений, замерзлий", "t_en": "frozen", "t_tr": "donmuş, dondurulmuş",
        **all_x("Das Fleisch ist noch eingefroren", "Мясо ещё замороженное", "М'ясо ще заморожене", "The meat is still frozen",
                "Et hâlâ donmuş", "Mięso jest jeszcze zamrożone", "La carne è ancora congelata", "La carne aún está congelada",
                "La viande est encore congelée", "Maso je ještě zmrazené")}),
    16343: ("«женщина-судья», «female judge» — лишнее", {"t_ru": "судья", "t_uk": "суддя", "t_en": "judge",
                                                       "t_tr": "hâkim, yargıç", "t_pl": "sędzia"}),
    16345: ("«Die Studenten besetzen den Hörsaal …» — хроника; " + LIST, {
        "t_ru": "занимать, оккупировать", "t_uk": "займати, окупувати", "t_en": "to occupy, to save (a seat)",
        "t_tr": "işgal etmek, yer tutmak", "t_pl": "zajmować, okupować", "t_fr": "occuper, pourvoir", "t_cs": "obsadit, okupovat",
        **all_x("Kannst du mir einen Platz besetzen?", "Можешь занять мне место?", "Можеш зайняти мені місце?",
                "Can you save me a seat?", "Bana bir yer tutar mısın?", "Zajmiesz mi miejsce?", "Mi occupi un posto?",
                "¿Me ocupas un sitio?", "Tu peux m'occuper une place?", "Obsadíš mi místo?")}),
    8962: ("«… ist sehr streng» — шаблон Lehrerin («Unsere Lehrerin ist sehr streng»)", {"t_en": "headmistress, principal", **all_x(
        "Die Direktorin will mit deinen Eltern sprechen", "Директриса хочет поговорить с твоими родителями",
        "Директорка хоче поговорити з твоїми батьками", "The headmistress wants to speak to your parents",
        "Müdire anne babanla konuşmak istiyor", "Dyrektorka chce porozmawiać z twoimi rodzicami",
        "La preside vuole parlare con i tuoi genitori", "La directora quiere hablar con tus padres",
        "La directrice veut parler à tes parents", "Ředitelka chce mluvit s tvými rodiči")}),
    17198: ("«Auf der Autobahn war ein riesiger Stau» — претерит", {**all_x(
        "Ich stehe im Stau und komme zu spät", "Я стою в пробке и опоздаю", "Я стою в заторі й запізнюся",
        "I'm stuck in a traffic jam and I'll be late", "Trafik sıkışıklığındayım, geç kalacağım", "Stoję w korku i się spóźnię",
        "Sono bloccato nell'ingorgo e arriverò tardi", "Estoy en un atasco y voy a llegar tarde",
        "Je suis dans les bouchons, je vais être en retard", "Stojím v zácpě a přijdu pozdě")}),
    589: ("«Ich gehe zum Metzger …» — шаблон «gehen»", {**all_x(
        "Beim Metzger gibt es heute frische Würste", "У мясника сегодня свежие колбаски", "У м'ясника сьогодні свіжі ковбаски",
        "The butcher's has fresh sausages today", "Kasapta bugün taze sosis var", "U rzeźnika są dziś świeże kiełbaski",
        "Dal macellaio oggi ci sono salsicce fresche", "En la carnicería hoy hay salchichas frescas",
        "Chez le boucher, il y a des saucisses fraîches aujourd'hui", "U řezníka mají dnes čerstvé klobásy")}),
    16346: ("«Ich möchte einen Pass beantragen» — шаблон Konsulat", {**all_x(
        "Hast du schon Urlaub beantragt?", "Ты уже подал заявление на отпуск?", "Ти вже подав заяву на відпустку?",
        "Have you applied for leave yet?", "İzin başvurusu yaptın mı?", "Złożyłeś już wniosek o urlop?",
        "Hai già richiesto le ferie?", "¿Ya has solicitado las vacaciones?", "Tu as déjà demandé tes congés?",
        "Už sis zažádal o dovolenou?")}),
    1353: ("«Die Einfahrt ist verboten» — табличка", {**all_x(
        "Der Nachbar parkt schon wieder in unserer Einfahrt", "Сосед опять паркуется у нас на въезде",
        "Сусід знову паркується на нашому в'їзді", "The neighbour is parking in our driveway again",
        "Komşu yine giriş yolumuza park etmiş", "Sąsiad znowu parkuje na naszym wjeździe",
        "Il vicino parcheggia di nuovo nel nostro passo carraio", "El vecino vuelve a aparcar en nuestra entrada",
        "Le voisin se gare encore devant notre entrée", "Soused zase parkuje u našeho vjezdu")}),
    844: ("«Wo ist meine Socke?» — шаблон Kamm («Wo ist mein Kamm?»)", {**all_x(
        "In der Waschmaschine verschwindet immer eine Socke", "В стиральной машине всегда пропадает один носок",
        "У пральній машині завжди зникає одна шкарпетка", "One sock always disappears in the washing machine",
        "Çamaşır makinesinde hep bir çorap kayboluyor", "W pralce zawsze ginie jedna skarpetka",
        "In lavatrice sparisce sempre un calzino", "En la lavadora siempre desaparece un calcetín",
        "Il y a toujours une chaussette qui disparaît dans la machine", "V pračce vždycky zmizí jedna ponožka")}),
    2734: ("«Es gibt einen großen Protest …» — шаблон «Es gibt …»", {**all_x(
        "Aus Protest ist er nicht gekommen", "В знак протеста он не пришёл", "На знак протесту він не прийшов",
        "He didn't come, as a protest", "Protesto olarak gelmedi", "Na znak protestu nie przyszedł",
        "Per protesta non è venuto", "En señal de protesta no vino", "Il n'est pas venu, par protestation", "Na protest nepřišel")}),
    2995: ("«Viele Wanderer sind hier» — пусто", {**all_x(
        "Auf dem Gipfel treffen sich viele Wanderer", "На вершине собирается много туристов", "На вершині збирається багато туристів",
        "Lots of hikers meet up at the top", "Zirvede birçok yürüyüşçü buluşuyor", "Na szczycie spotyka się wielu turystów",
        "In cima si incontrano tanti escursionisti", "En la cima se juntan muchos senderistas",
        "Beaucoup de randonneurs se retrouvent au sommet", "Na vrcholu se schází spousta turistů")}),
    10752: ("«Seine Versuche waren vergeblich» — книжно", {**all_x(
        "Ich habe vergeblich auf dich gewartet", "Я напрасно тебя ждал", "Я марно тебе чекав", "I waited for you in vain",
        "Seni boşuna bekledim", "Na próżno na ciebie czekałem", "Ti ho aspettato invano", "Te esperé en vano",
        "Je t'ai attendu en vain", "Marně jsem na tebe čekal")}),
    2236: ("«Ich stelle ein Zeugnis aus» — пусто; " + LIST, {
        "t_ru": "выдавать, выставлять", "t_uk": "видавати, виставляти", "t_en": "to issue, to exhibit",
        "t_tr": "belge vermek, sergilemek", "t_pl": "wystawiać, wyłączać", "t_it": "rilasciare, esporre",
        "t_es": "expedir, exponer", "t_fr": "délivrer, exposer", "t_cs": "vystavit, vypnout",
        **all_x("Können Sie mir eine Quittung ausstellen?", "Можете выдать мне квитанцию?", "Можете видати мені квитанцію?",
                "Could you issue me a receipt?", "Bana fiş verebilir misiniz?", "Może mi Pan wystawić paragon?",
                "Mi può rilasciare una ricevuta?", "¿Me puede expedir un recibo?", "Vous pouvez me délivrer un reçu?",
                "Můžete mi vystavit účtenku?")}),
    12224: ("«Der Sportler trainiert jeden Tag» — шаблон Turner", {**all_x(
        "Für einen Sportler isst er ziemlich ungesund", "Для спортсмена он питается довольно нездорово",
        "Як для спортсмена, він харчується досить нездорово", "For an athlete he eats pretty unhealthily",
        "Bir sporcu için oldukça sağlıksız besleniyor", "Jak na sportowca je dość niezdrowo",
        "Per essere uno sportivo mangia piuttosto male", "Para ser deportista come bastante mal",
        "Pour un sportif, il mange plutôt mal", "Na sportovce jí dost nezdravě")}),
    2076: ("«Die Vorlesung beginnt um 10 Uhr» — шаблон «beginnt um …»", {**all_x(
        "In der Vorlesung schlafe ich immer fast ein", "На лекции я всегда чуть не засыпаю", "На лекції я завжди мало не засинаю",
        "I always nearly fall asleep in the lecture", "Derste hep neredeyse uyuyakalıyorum", "Na wykładzie zawsze prawie zasypiam",
        "A lezione mi addormento quasi sempre", "En clase casi siempre me duermo", "En cours, je m'endors presque toujours",
        "Na přednášce vždycky skoro usnu")}),
    1756: ("«Die Pfanne ist sehr heiß» — пусто", {**all_x(
        "Gib noch etwas Öl in die Pfanne", "Добавь ещё немного масла на сковородку", "Додай ще трохи олії на сковорідку",
        "Put a bit more oil in the pan", "Tavaya biraz daha yağ koy", "Dodaj jeszcze trochę oleju na patelnię",
        "Metti ancora un po' d'olio nella padella", "Echa un poco más de aceite en la sartén",
        "Mets encore un peu d'huile dans la poêle", "Dej do pánve ještě trochu oleje")}),
    12718: ("«Mir ist kalt, wir werden frieren» — так не говорят", {**all_x(
        "Im Winter friere ich immer an den Füßen", "Зимой у меня всегда мёрзнут ноги", "Узимку в мене завжди мерзнуть ноги",
        "In winter my feet are always cold", "Kışın ayaklarım hep üşür", "Zimą zawsze marzną mi stopy",
        "D'inverno ho sempre freddo ai piedi", "En invierno siempre tengo frío en los pies",
        "En hiver, j'ai toujours froid aux pieds", "V zimě mi vždycky mrznou nohy")}),
    9832: ("«Es gibt heute einen Rabatt …» — шаблон «Es gibt …»", {**all_x(
        "Bekomme ich als Student Rabatt?", "А студентам есть скидка?", "Чи є знижка для студентів?",
        "Do I get a student discount?", "Öğrenci olarak indirim alabilir miyim?", "Czy jako student dostanę zniżkę?",
        "Come studente ho diritto a uno sconto?", "¿Tengo descuento como estudiante?",
        "J'ai droit à une réduction en tant qu'étudiant?", "Dostanu jako student slevu?")}),
    2553: ("ru «Меня мучает тоска» — книжно", {"x_ru": "У меня тоска по дому, по семье", "x_en": "I'm homesick for my family"}),
    12720: ("«Die Sehne … tut weh» — шаблон «tut weh»", {**all_x(
        "Beim Fußball habe ich mir eine Sehne gerissen", "На футболе я порвал сухожилие", "На футболі я порвав сухожилля",
        "I tore a tendon playing football", "Futbol oynarken tendonum koptu", "Na piłce zerwałem ścięgno",
        "Giocando a calcio mi sono rotto un tendine", "Jugando al fútbol me rompí un tendón",
        "Au foot, je me suis déchiré un tendon", "Při fotbale jsem si přetrhl šlachu")}),
    9833: ("«Das Hotel ist ausgebucht» — шаблон ausverkauft", {**all_x(
        "Für Silvester ist schon alles ausgebucht", "На Новый год всё уже забронировано", "На Новий рік уже все заброньовано",
        "Everything's already booked up for New Year's Eve", "Yılbaşı için her yer çoktan dolu",
        "Na sylwestra wszystko jest już zarezerwowane", "Per Capodanno è già tutto al completo",
        "Para Nochevieja ya está todo completo", "Pour le Nouvel An, tout est déjà complet",
        "Na Silvestra je už všechno plně obsazené")}),
    16355: ("«Der Streifenwagen … fuhr schnell vorbei» — претерит", {**all_x(
        "Vor dem Haus steht ein Streifenwagen", "Перед домом стоит патрульная машина", "Перед будинком стоїть патрульна машина",
        "There's a patrol car outside the house", "Evin önünde bir devriye arabası var", "Przed domem stoi radiowóz",
        "Davanti a casa c'è una volante", "Delante de la casa hay un coche patrulla",
        "Il y a une voiture de police devant la maison", "Před domem stojí policejní auto")}),
    17204: ("«Vergiss nicht, dich anzuschnallen …» — шаблон Helm («Vergiss nicht, … aufzusetzen»)", {**all_x(
        "Im Bus muss man sich nicht anschnallen", "В автобусе не нужно пристёгиваться", "В автобусі не треба пристібатися",
        "You don't have to buckle up on the bus", "Otobüste emniyet kemeri takmak zorunlu değil",
        "W autobusie nie trzeba zapinać pasów", "In autobus non bisogna allacciarsi la cintura",
        "En el autobús no hace falta abrocharse el cinturón", "Dans le bus, pas besoin d'attacher sa ceinture",
        "V autobuse se nemusíš připoutat")}),
    7462: (EN + " («vacation»)", {"x_en": "The money won't be enough for the holiday"}),
    1492: ("«Er hat eine Glatze» — шаблон Bart («Er hat einen langen Bart»); убрать пометку (colloq.)", {
        "t_it": "la testa calva, la calvizie",
        **all_x("Mit 30 hatte er schon eine Glatze", "В 30 у него уже была лысина", "У 30 у нього вже була лисина",
                "He already had a bald head at 30", "30 yaşında zaten keldi", "W wieku 30 lat miał już łysinę",
                "A 30 anni aveva già la testa calva", "A los 30 ya tenía calva", "À 30 ans, il avait déjà le crâne chauve",
                "Ve třiceti už měl pleš")}),
}

SPLIT_LATER = {}
