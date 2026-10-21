"""B1, блок 54: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    12588: ("«Im Mittelalter gab es die Pest» — учебник истории; живое — «wie die Pest hassen»", {**all_x(
        "Ich hasse diese Mücken wie die Pest", "Ненавижу этих комаров как чуму", "Ненавиджу цих комарів як чуму",
        "I hate these mosquitoes like the plague", "Bu sivrisineklerden vebadan nefret eder gibi nefret ediyorum",
        "Nienawidzę tych komarów jak zarazy", "Odio queste zanzare come la peste", "Odio a estos mosquitos como a la peste",
        "Je déteste ces moustiques comme la peste", "Nesnáším ty komáry jako mor")}),
    2824: ("«Der Sonnenschein heute ist wunderbar» — снова погода", {**all_x(
        "Du bist mein kleiner Sonnenschein", "Ты моё солнышко", "Ти моє маленьке сонечко",
        "You're my little ray of sunshine", "Sen benim küçük güneş ışığımsın", "Jesteś moim małym słoneczkiem",
        "Sei il mio piccolo raggio di sole", "Eres mi rayito de sol", "Tu es mon petit rayon de soleil",
        "Jsi moje malé sluníčko")}),
    18714: ("«Du darfst dein Geld nicht vergeuden» — калька", {**all_x(
        "Vergeude nicht deine Zeit mit ihm!", "Не трать на него время впустую!", "Не марнуй на нього час!",
        "Don't waste your time on him!", "Onunla vaktini boşa harcama!", "Nie marnuj na niego czasu!",
        "Non sprecare il tuo tempo con lui!", "¡No malgastes tu tiempo con él!", "Ne gaspille pas ton temps avec lui!",
        "Neplýtvej s ním časem!")}),
    14001: ("«Die Glocke läutet um 8 Uhr» — шаблон Glocke", {**all_x(
        "Es läutet, die Pause ist vorbei", "Звенит звонок, перемена закончилась", "Дзвенить дзвоник, перерва закінчилася",
        "The bell is ringing, break is over", "Zil çalıyor, teneffüs bitti", "Dzwoni dzwonek, przerwa się skończyła",
        "Suona la campanella, la ricreazione è finita", "Suena el timbre, se acabó el recreo", "Ça sonne, la récré est finie",
        "Zvoní, přestávka skončila")}),
    17793: ("«Das Unternehmen macht einen großen Profit» — отчёт", {**all_x(
        "Ihm geht es nur um Profit", "Ему важна только выгода", "Йому йдеться тільки про вигоду",
        "All he cares about is profit", "Onun tek derdi kâr", "Chodzi mu tylko o zysk", "Gli interessa solo il profitto",
        "Solo le interesa el beneficio", "Il ne pense qu'au profit", "Jde mu jen o zisk")}),
    12179: ("«Wir gehen ins Casino und spielen» — шаблон «gehen»", {**all_x(
        "Er hat im Casino sein ganzes Geld verloren", "Он проиграл в казино все деньги", "Він програв у казино всі гроші",
        "He lost all his money at the casino", "Kumarhanede bütün parasını kaybetti", "Przegrał w kasynie wszystkie pieniądze",
        "Ha perso tutti i soldi al casinò", "Perdió todo su dinero en el casino", "Il a perdu tout son argent au casino",
        "V kasinu prohrál všechny peníze")}),
    8862: (EN, {"x_en": "The new client is coming to the office tomorrow"}),
    472: ("«Sie isst einen Keks» — пусто", {**all_x(
        "Willst du einen Keks zum Kaffee?", "Хочешь печенье к кофе?", "Хочеш печиво до кави?",
        "Do you want a biscuit with your coffee?", "Kahvenin yanına bisküvi ister misin?", "Chcesz ciastko do kawy?",
        "Vuoi un biscotto col caffè?", "¿Quieres una galleta con el café?", "Tu veux un biscuit avec ton café?",
        "Chceš k kafi sušenku?")}),
    542: ("«Sie kauft Lebensmittel» — пусто", {**all_x(
        "Lebensmittel sind teurer geworden", "Продукты подорожали", "Продукти подорожчали", "Food has got more expensive",
        "Gıdalar pahalandı", "Żywność podrożała", "Gli alimenti sono aumentati di prezzo", "Los alimentos se han encarecido",
        "La nourriture a augmenté", "Potraviny zdražily")}),
    16143: ("«Nach der großen Schlacht …» — претерит, война", {**all_x(
        "Nach der Party sah die Küche aus wie ein Schlachtfeld", "После вечеринки кухня выглядела как поле боя",
        "Після вечірки кухня була схожа на поле бою", "After the party the kitchen looked like a battlefield",
        "Partiden sonra mutfak savaş alanı gibiydi", "Po imprezie kuchnia wyglądała jak pole bitwy",
        "Dopo la festa la cucina sembrava un campo di battaglia",
        "Después de la fiesta la cocina parecía un campo de batalla",
        "Après la fête, la cuisine ressemblait à un champ de bataille", "Po párty vypadala kuchyně jako bojiště")}),
    10464: ("ru «Я должен ещё раз переосмыслить» — калька", {
        "x_ru": "Мне надо ещё раз обдумать твоё предложение, прежде чем согласиться"}),
    18717: ("«Die Sonne ging allmählich unter …» — претерит, погода", {**all_x(
        "Allmählich verstehe ich, was du meinst", "Постепенно я начинаю понимать, что ты имеешь в виду",
        "Поступово я починаю розуміти, що ти маєш на увазі", "I'm gradually starting to understand what you mean",
        "Yavaş yavaş ne demek istediğini anlıyorum", "Stopniowo zaczynam rozumieć, o co ci chodzi",
        "A poco a poco capisco cosa intendi", "Poco a poco entiendo lo que quieres decir",
        "Peu à peu, je comprends ce que tu veux dire", "Postupně chápu, co myslíš")}),
    16144: ("«Die Polizei hatte einen Durchsuchungsbefehl …» — претерит", {**all_x(
        "Ohne Durchsuchungsbefehl dürfen Sie hier nicht rein", "Без ордера на обыск вам сюда нельзя",
        "Без ордера на обшук вам сюди не можна", "You can't come in here without a search warrant",
        "Arama emri olmadan buraya giremezsiniz", "Bez nakazu przeszukania nie mogą Państwo tu wejść",
        "Senza mandato di perquisizione non potete entrare", "Sin orden de registro no pueden entrar",
        "Sans mandat de perquisition, vous ne pouvez pas entrer", "Bez příkazu k domovní prohlídce sem nesmíte")}),
    15500: ("«Aus dem heißen Topf stieg Dampf auf» — претерит", {**all_x(
        "Vorsicht, der Dampf ist heiß!", "Осторожно, пар горячий!", "Обережно, пара гаряча!", "Careful, the steam is hot!",
        "Dikkat, buhar sıcak!", "Uwaga, para jest gorąca!", "Attento, il vapore scotta!", "¡Cuidado, el vapor quema!",
        "Attention, la vapeur est brûlante!", "Pozor, pára je horká!")}),
    7078: ("ru «Можем ли мы отменить» — книжно", {"x_ru": "Можно отменить последнее действие?"}),
    12590: ("«Nach dem Unfall war sein Bein lahm» — хроника", {**all_x(
        "Die Party war ganz schön lahm", "Вечеринка была довольно скучной", "Вечірка була досить нудна",
        "The party was pretty boring", "Parti epey sıkıcıydı", "Impreza była dość nudna",
        "La festa è stata piuttosto noiosa", "La fiesta fue bastante aburrida", "La fête était plutôt ennuyeuse",
        "Ta párty byla dost nudná")}),
    1886: ("«Das ist speziell für dich» — пусто", {**all_x(
        "Er hat einen sehr speziellen Humor", "У него очень особый юмор", "У нього дуже особливий гумор",
        "He has a very particular sense of humour", "Çok özel bir mizah anlayışı var", "Ma bardzo szczególne poczucie humoru",
        "Ha un umorismo molto particolare", "Tiene un humor muy particular", "Il a un humour très particulier",
        "Má hodně zvláštní humor")}),
    13663: ("«Sie trug ein elegantes Kleid …» — претерит, шаблон одежды", {**all_x(
        "Das Restaurant ist sehr elegant", "Ресторан очень элегантный", "Ресторан дуже елегантний",
        "The restaurant is very elegant", "Restoran çok şık", "Restauracja jest bardzo elegancka",
        "Il ristorante è molto elegante", "El restaurante es muy elegante", "Le restaurant est très élégant",
        "Ta restaurace je velmi elegantní")}),
}

SPLIT_LATER = {
    15500: ["Dampf ablassen = выпустить пар"],
}
