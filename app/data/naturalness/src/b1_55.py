"""B1, блок 55: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2082: ("«Ich halte einen Vortrag» — пусто", {**all_x(
        "Morgen muss ich einen Vortrag halten und bin total nervös", "Завтра мне выступать с докладом, и я ужасно нервничаю",
        "Завтра мені виступати з доповіддю, і я дуже нервую", "I have to give a talk tomorrow and I'm really nervous",
        "Yarın bir sunum yapmam lazım ve çok gerginim", "Jutro mam wykład i strasznie się denerwuję",
        "Domani devo fare una presentazione e sono nervosissimo", "Mañana tengo que dar una charla y estoy muy nervioso",
        "Demain, je dois faire un exposé et je suis super stressé", "Zítra mám přednášku a jsem strašně nervózní")}),
    12593: ("«Sie sah blass aus …» — претерит", {**all_x(
        "Du bist so blass, geht's dir nicht gut?", "Ты такой бледный, тебе нехорошо?", "Ти такий блідий, тобі погано?",
        "You look so pale, are you feeling OK?", "Çok solgunsun, iyi değil misin?", "Jesteś taki blady, źle się czujesz?",
        "Sei così pallido, non stai bene?", "Estás muy pálido, ¿no te encuentras bien?", "Tu es tout pâle, ça ne va pas?",
        "Jsi tak bledý, není ti dobře?")}),
    12595: ("ru «Спорт физически утомителен» — калька", {**all_x(
        "Die Arbeit auf dem Bau ist körperlich sehr hart", "Работа на стройке физически очень тяжёлая",
        "Робота на будові фізично дуже важка", "Working on a building site is physically very hard",
        "İnşaatta çalışmak fiziksel olarak çok ağır", "Praca na budowie jest fizycznie bardzo ciężka",
        "Lavorare in cantiere è fisicamente molto duro", "Trabajar en la obra es físicamente muy duro",
        "Travailler sur un chantier, c'est physiquement très dur", "Práce na stavbě je fyzicky hodně náročná")}),
    70: ("«Sie nimmt ein Bad in der Badewanne» — масло масляное", {**all_x(
        "Die Kinder planschen in der Badewanne", "Дети плещутся в ванне", "Діти хлюпаються у ванні",
        "The kids are splashing about in the tub", "Çocuklar küvette su sıçratıyor", "Dzieci chlapią się w wannie",
        "I bambini sguazzano nella vasca", "Los niños chapotean en la bañera", "Les enfants barbotent dans la baignoire",
        "Děti se cachtají ve vaně")}),
    9480: ("ru «Как новичок, ты должен» — калька", {"x_ru": "Новичку лучше тренироваться не спеша"}),
    7091: ("убрать пометки (fam.)/(hovor.)", {"t_fr": "vérifier, capter", "t_cs": "zkontrolovat, pochopit"}),
    9785: ("«Das alte Auto ist wertlos» — шаблон Schrott («Das alte Auto ist nur noch Schrott»)", {**all_x(
        "Ohne Unterschrift ist der Vertrag wertlos", "Без подписи договор ничего не стоит", "Без підпису договір нічого не вартий",
        "Without a signature the contract is worthless", "İmzasız sözleşme değersiz", "Bez podpisu umowa jest bezwartościowa",
        "Senza firma il contratto non ha valore", "Sin firma el contrato no tiene valor",
        "Sans signature, le contrat est sans valeur", "Bez podpisu je smlouva bezcenná")}),
    7098: ("«ideales Wetter für einen Ausflug» — снова погода", {**all_x(
        "Die Wohnung ist ideal für eine Familie", "Квартира идеальна для семьи", "Квартира ідеальна для сім'ї",
        "The flat is ideal for a family", "Daire bir aile için ideal", "Mieszkanie jest idealne dla rodziny",
        "L'appartamento è ideale per una famiglia", "El piso es ideal para una familia",
        "L'appartement est idéal pour une famille", "Byt je ideální pro rodinu")}),
    9786: ("«Der Beutel ist voll» — пусто; «Brauchen Sie …?» — у Tüte", {**all_x(
        "Ich nehme immer einen Beutel zum Einkaufen mit", "Я всегда беру с собой сумку за покупками",
        "Я завжди беру з собою торбинку для покупок", "I always take a bag with me when I go shopping",
        "Alışverişe giderken hep yanıma bir torba alırım", "Zawsze biorę ze sobą torebkę na zakupy",
        "Porto sempre una borsa per la spesa", "Siempre llevo una bolsa para la compra",
        "J'emporte toujours un sac pour faire les courses", "Na nákup si vždycky beru tašku")}),
    17944: ("«Die Galaxie ist unendlich groß» — шаблон Weltraum", {**all_x(
        "Unsere Galaxie heißt Milchstraße", "Наша галактика называется Млечный Путь", "Наша галактика називається Чумацький Шлях",
        "Our galaxy is called the Milky Way", "Galaksimizin adı Samanyolu", "Nasza galaktyka nazywa się Droga Mleczna",
        "La nostra galassia si chiama Via Lattea", "Nuestra galaxia se llama Vía Láctea",
        "Notre galaxie s'appelle la Voie lactée", "Naše galaxie se jmenuje Mléčná dráha")}),
    18207: ("«Das Wasser fließt durch das Rohr» — учебник", {**all_x(
        "Das Rohr unter der Spüle ist undicht", "Труба под раковиной протекает", "Труба під раковиною протікає",
        "The pipe under the sink is leaking", "Lavabonun altındaki boru sızdırıyor", "Rura pod zlewem przecieka",
        "Il tubo sotto il lavandino perde", "El tubo de debajo del fregadero gotea", "Le tuyau sous l'évier fuit",
        "Trubka pod dřezem teče")}),
    17134: ("«Das Segel des Schiffes ist weiß» — пусто", {**all_x(
        "Wir setzen die Segel und fahren los", "Мы поднимаем паруса и отплываем", "Ми піднімаємо вітрила й вирушаємо",
        "We hoist the sails and set off", "Yelkenleri açıp yola çıkıyoruz", "Stawiamy żagle i ruszamy",
        "Issiamo le vele e partiamo", "Izamos las velas y salimos", "On hisse les voiles et on part",
        "Napneme plachty a vyrazíme")}),
    12603: ("«Diese Flüssigkeit ist sehr giftig» — пусто", {**all_x(
        "Im Handgepäck darfst du keine Flüssigkeiten mitnehmen", "В ручную кладь нельзя брать жидкости",
        "У ручну поклажу не можна брати рідини", "You can't take liquids in your hand luggage",
        "El bagajında sıvı taşıyamazsın", "W bagażu podręcznym nie wolno przewozić płynów",
        "Nel bagaglio a mano non puoi portare liquidi", "En el equipaje de mano no puedes llevar líquidos",
        "Tu ne peux pas prendre de liquides en bagage à main", "V příručním zavazadle nesmíš mít tekutiny")}),
    7100: ("«Dir auch alles Gute, gleichfalls» — масло масляное", {**all_x(
        "Schönes Wochenende! – Danke, gleichfalls!", "Хороших выходных! — Спасибо, взаимно!", "Гарних вихідних! — Дякую, взаємно!",
        "Have a nice weekend! – Thanks, likewise!", "İyi hafta sonları! – Teşekkürler, sana da!",
        "Miłego weekendu! – Dzięki, wzajemnie!", "Buon fine settimana! – Grazie, altrettanto!",
        "¡Buen fin de semana! – Gracias, igualmente", "Bon week-end! – Merci, pareillement!", "Hezký víkend! – Díky, vzájemně!")}),
    1113: (LIST + " (было шесть значений)", {
        "t_ru": "высадить, поставить", "t_uk": "висадити, поставити", "t_en": "to drop off, to put down",
        "t_tr": "bırakmak, yere koymak", "t_pl": "podrzucić, postawić", "t_it": "lasciare, posare", "t_es": "dejar, posar",
        "t_fr": "déposer, poser", "t_cs": "vysadit, položit"}),
    2658: (EN + " (потеряно «durch die Stadt»)", {"x_en": "I steer the car through town"}),
    12609: (EN + " («wrist» вместо «hand»)", {"x_en": "I'm wrapping a bandage round my hand"}),
    17945: ("«Ich studiere Philosophie» — пусто", {**all_x(
        "Das ist meine Philosophie: leben und leben lassen", "Это моя философия: живи и давай жить другим",
        "Це моя філософія: живи й дай жити іншим", "That's my philosophy: live and let live",
        "Benim felsefem bu: yaşa ve yaşat", "Taka jest moja filozofia: żyj i pozwól żyć innym",
        "Questa è la mia filosofia: vivi e lascia vivere", "Esa es mi filosofía: vive y deja vivir",
        "C'est ma philosophie: vivre et laisser vivre", "To je moje filozofie: žij a nech žít")}),
    17138: ("«Der Lastwagen war zu schwer» — претерит, пусто", {**all_x(
        "Hinter uns fährt ein riesiger Lastwagen", "За нами едет огромный грузовик", "За нами їде величезна вантажівка",
        "There's a huge lorry behind us", "Arkamızda dev bir kamyon var", "Za nami jedzie wielka ciężarówka",
        "Dietro di noi c'è un camion enorme", "Detrás de nosotros va un camión enorme",
        "Il y a un énorme camion derrière nous", "Za námi jede obrovský kamion")}),
    8872: ("«Der Wirt war sehr freundlich» — претерит, пусто", {**all_x(
        "Der Wirt gibt heute eine Runde aus", "Хозяин паба сегодня всех угощает", "Господар бару сьогодні всіх пригощає",
        "The landlord is buying everyone a round today", "Bugün meyhane sahibi herkese bir içki ısmarlıyor",
        "Gospodarz stawia dziś kolejkę", "Oggi l'oste offre un giro a tutti", "El dueño del local invita hoy a una ronda",
        "Aujourd'hui, le patron offre une tournée", "Hostinský dnes dává rundu")}),
    7106: ("«Das Tuch war sehr weich» — претерит, пусто", {**all_x(
        "Wisch den Tisch mit einem feuchten Tuch ab", "Протри стол влажной тряпкой", "Протри стіл вологою ганчіркою",
        "Wipe the table with a damp cloth", "Masayı nemli bir bezle sil", "Przetrzyj stół wilgotną szmatką",
        "Pulisci il tavolo con un panno umido", "Limpia la mesa con un paño húmedo", "Essuie la table avec un chiffon humide",
        "Otři stůl vlhkým hadrem")}),
}

SPLIT_LATER = {}
