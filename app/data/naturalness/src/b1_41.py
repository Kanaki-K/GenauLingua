"""B1, блок 41: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    16081: ("«Die Gräfin war sehr elegant gekleidet» — роман", {**all_x(
        "Seine Oma war eine echte Gräfin", "Его бабушка была настоящей графиней", "Його бабуся була справжньою графинею",
        "His gran was a real countess", "Büyükannesi gerçek bir kontesti", "Jego babcia była prawdziwą hrabiną",
        "Sua nonna era una vera contessa", "Su abuela era una condesa de verdad", "Sa grand-mère était une vraie comtesse",
        "Jeho babička byla skutečná hraběnka")}),
    15012: ("«Die Gemeinschaft hilft sich gegenseitig» — газета; " + LIST, {
        "t_ru": "сообщество, община", "t_uk": "спільнота, громада", "t_en": "community", "t_tr": "topluluk, cemaat",
        "t_pl": "wspólnota, społeczność",
        **all_x("Wir sind eine kleine Gemeinschaft, hier hilft jeder jedem", "Мы небольшая община, здесь все помогают друг другу",
                "Ми невелика громада, тут усі допомагають одне одному", "We're a small community, everyone helps each other here",
                "Küçük bir topluluğuz, burada herkes birbirine yardım eder",
                "Jesteśmy małą społecznością, tu każdy pomaga każdemu", "Siamo una piccola comunità, qui tutti si aiutano",
                "Somos una pequeña comunidad, aquí todos se ayudan", "On est une petite communauté, ici tout le monde s'entraide",
                "Jsme malá komunita, tady pomáhá každý každému")}),
    6927: (LIST, {"t_ru": "замена, заменитель", "t_uk": "заміна, замінник", "t_tr": "yedek, ikame",
                  "t_pl": "zastępstwo, zamiennik"}),
    17519: ("«Aktiviere die Zwei-Faktor-Authentifizierung» — инструкция", {**all_x(
        "Hast du Bluetooth aktiviert?", "Ты включил блютус?", "Ти увімкнув блютуз?", "Have you turned on Bluetooth?",
        "Bluetooth'u açtın mı?", "Włączyłeś Bluetooth?", "Hai attivato il Bluetooth?", "¿Has activado el Bluetooth?",
        "Tu as activé le Bluetooth?", "Zapnul jsi Bluetooth?")}),
    3061: ("«Ich lasse meine Tasche im Café zurück» — так не говорят", {**all_x(
        "Wir mussten das Auto zurücklassen und zu Fuß gehen", "Нам пришлось бросить машину и идти пешком",
        "Нам довелося кинути машину й іти пішки", "We had to leave the car behind and walk",
        "Arabayı geride bırakıp yürümek zorunda kaldık", "Musieliśmy zostawić samochód i iść pieszo",
        "Abbiamo dovuto lasciare la macchina e andare a piedi", "Tuvimos que dejar el coche y seguir a pie",
        "On a dû laisser la voiture et continuer à pied", "Museli jsme nechat auto a jít pěšky")}),
    6931: (LIST, {"t_ru": "переводить, перемещать", "t_uk": "переводити, переміщувати", "t_en": "to transfer, to move",
                  "t_tr": "nakletmek, başka yere almak", "t_pl": "przenieść, przesunąć"}),
    16084: (LIST, {"t_ru": "перекрыть, заблокировать", "t_uk": "перекрити, заблокувати", "t_en": "to block, to close off",
                   "t_tr": "kapatmak, bloke etmek", "t_pl": "zablokować, zamknąć"}),
    16086: ("ru «королевское обращение с нами» — калька; " + LIST, {
        "t_ru": "королевский, роскошный", "t_uk": "королівський, розкішний", "t_en": "royal, regal",
        "t_tr": "kraliyete ait, görkemli", "t_pl": "królewski, wystawny",
        "x_ru": "Нас приняли по-королевски", "x_uk": "Нас прийняли по-королівськи"}),
    6932: (LIST, {"t_ru": "отвлекать, отклонять", "t_uk": "відволікати, відхиляти", "t_en": "to distract, to take one's mind off",
                  "t_tr": "dikkatini dağıtmak, oyalamak", "t_pl": "rozpraszać, odwracać uwagę"}),
    15473: ("ru «Утка плывёт» — так не говорят", {"x_ru": "Утка плавает по озеру"}),
    15013: (EN, {"x_en": "We're related"}),
    15474: ("«Die Welle im Meer war heute echt groß» — снова погода", {**all_x(
        "Die Wellen sind heute zu hoch zum Schwimmen", "Сегодня волны слишком высокие, чтобы купаться",
        "Сьогодні хвилі надто високі, щоб купатися", "The waves are too high for swimming today",
        "Dalgalar bugün yüzmek için fazla yüksek", "Fale są dziś za wysokie, żeby pływać",
        "Oggi le onde sono troppo alte per nuotare", "Hoy las olas están demasiado altas para nadar",
        "Aujourd'hui, les vagues sont trop hautes pour se baigner", "Vlny jsou dnes moc vysoké na plavání")}),
    10386: (EN + " («embraces»)", {"x_en": "My mum hugs me every morning"}),
    17932: (EN + " («math» — американское)", {"x_en": "I found division in maths hard"}),
    10387: (LIST, {"t_ru": "неуверенный, небезопасный", "t_uk": "невпевнений, небезпечний", "t_en": "unsure, unsafe",
                   "t_tr": "emin olmayan, güvensiz", "t_pl": "niepewny, niebezpieczny"}),
    6937: (LIST, {"t_ru": "оказаться, оказывать", "t_uk": "виявитися, виявляти", "t_en": "to turn out, to show",
                  "t_tr": "çıkmak, göstermek", "t_pl": "okazać się, wyświadczyć"}),
    6938: (LIST, {"t_ru": "организовать, устроить", "t_uk": "організувати, влаштувати", "t_en": "to arrange, to organise",
                  "t_tr": "ayarlamak, düzenlemek", "t_pl": "zorganizować, umówić"}),
    1616: ("«Die Äpfel sind im Korb» — пусто", {"t_ru": "корзина, корзинка", "t_uk": "кошик", "t_en": "basket",
                                               "t_tr": "sepet", "t_pl": "koszyk, kosz",
                                               **all_x("Leg das Brot in den Korb", "Положи хлеб в корзинку", "Поклади хліб у кошик",
                                                       "Put the bread in the basket", "Ekmeği sepete koy", "Włóż chleb do koszyka",
                                                       "Metti il pane nel cestino", "Pon el pan en la cesta",
                                                       "Mets le pain dans le panier", "Dej chleba do košíku")}),
    8832: ("шаблон Assistentin («Die Assistentin hilft dem Chef …»)", {**all_x(
        "Ich suche einen Assistenten für mein Büro", "Я ищу ассистента в свой офис", "Я шукаю асистента в офіс",
        "I'm looking for an assistant for my office", "Ofisim için bir asistan arıyorum", "Szukam asystenta do biura",
        "Cerco un assistente per il mio ufficio", "Busco un asistente para mi oficina",
        "Je cherche un assistant pour mon bureau", "Hledám asistenta do kanceláře")}),
    1856: (LIST + "; ru «идём под парусом» — книжно", {
        "t_ru": "ходить под парусом, парить", "t_uk": "ходити під вітрилом, плавати на яхті",
        "x_ru": "На выходных мы ходим под парусом", "x_en": "We're going sailing at the weekend"}),
    17120: ("«Der Transport der Güter dauerte drei Tage» — претерит, накладная", {**all_x(
        "Der Transport ist im Preis inbegriffen", "Перевозка включена в цену", "Перевезення включене в ціну",
        "Transport is included in the price", "Nakliye fiyata dahil", "Transport jest wliczony w cenę",
        "Il trasporto è incluso nel prezzo", "El transporte está incluido en el precio",
        "Le transport est compris dans le prix", "Doprava je v ceně")}),
    12564: (EN + " («emergency room» — американское); " + LIST, {
        "t_ru": "приёмный покой, неотложка", "t_uk": "приймальне відділення, невідкладна допомога",
        "t_en": "A&E, emergency department", "x_ru": "Мне пришлось везти отца в приёмный покой",
        "x_uk": "Мені довелося везти батька в приймальне відділення", "x_en": "I had to take my dad to A&E"}),
    11687: (LIST, {"t_ru": "мешать, растрогать", "t_uk": "помішувати, зворушувати", "t_en": "to stir, to move",
                   "t_tr": "karıştırmak, duygulandırmak", "t_pl": "mieszać, wzruszać"}),
    2197: ("«Die Arbeit ist sehr anstrengend» — пусто", {**all_x(
        "Mit kleinen Kindern ist jeder Tag anstrengend", "С маленькими детьми каждый день утомительный",
        "З маленькими дітьми кожен день виснажливий", "With small children every day is exhausting",
        "Küçük çocuklarla her gün yorucu", "Z małymi dziećmi każdy dzień jest męczący",
        "Con i bambini piccoli ogni giorno è faticoso", "Con niños pequeños cada día es agotador",
        "Avec des tout-petits, chaque journée est fatigante", "S malými dětmi je každý den únavný")}),
}

REPLACE = [{"id": 8831, "by": 1804, "lang": "de", "why": "Ruhestand — книжный вариант Rente (in Rente gehen)"}]

SPLIT_LATER = {
    1616: ["jemandem einen Korb geben = отказать (в ухаживании)"],
    6931: ["jemanden versetzen = не прийти на встречу, продинамить"],
}
