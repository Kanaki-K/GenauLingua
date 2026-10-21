"""B1, блок 35: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    13949: ("«Der Schiedsrichter blies in die Pfeife» — претерит; " + LIST, {
        "t_ru": "трубка, свисток", "t_uk": "люлька, свисток", "t_en": "pipe, whistle", "t_tr": "pipo, düdük",
        "t_pl": "fajka, gwizdek", "t_it": "la pipa, il fischietto", "t_es": "la pipa, el silbato",
        "t_fr": "la pipe, le sifflet", "t_cs": "dýmka, píšťalka",
        **all_x("Mein Opa raucht Pfeife", "Мой дед курит трубку", "Мій дід курить люльку", "My grandad smokes a pipe",
                "Dedem pipo içiyor", "Mój dziadek pali fajkę", "Mio nonno fuma la pipa", "Mi abuelo fuma en pipa",
                "Mon grand-père fume la pipe", "Děda kouří dýmku")}),
    2281: ("«Das Paket kam beschädigt an» — претерит", {"t_ru": "повреждённый, битый", **all_x(
        "Das Paket ist beschädigt angekommen", "Посылка пришла повреждённой", "Посилка прийшла пошкоджена",
        "The parcel arrived damaged", "Paket hasarlı geldi", "Paczka przyszła uszkodzona",
        "Il pacco è arrivato danneggiato", "El paquete ha llegado dañado", "Le colis est arrivé abîmé",
        "Balík přišel poškozený")}),
    10347: ("«So ein Abschaum will ich …» — грамматика; убрать пометку (fam.); " + LIST, {
        "t_ru": "подонок, отбросы общества", "t_uk": "покидьок, мерзотник", "t_en": "scum, lowlife",
        "t_tr": "pislik, alçak", "t_pl": "szumowina, kanalia", "t_fr": "la racaille, la lie de la société",
        **all_x("Das ist doch der letzte Abschaum!", "Это же последние подонки!", "Це ж останні покидьки!",
                "They're absolute scum!", "Bunlar tam bir pislik!", "To ostatnie szumowiny!", "Sono proprio feccia!",
                "¡Son pura escoria!", "C'est vraiment la racaille!", "To je ta nejhorší spodina!")}),
    8813: ("«female assistant», «секретарь» — лишнее", {
        "t_ru": "ассистентка, помощница", "t_en": "assistant", "t_tr": "asistan, yardımcı"}),
    6869: (LIST + " (было шесть значений)", {
        "t_ru": "коробка, колонка", "t_uk": "коробка, колонка", "t_en": "box, speaker", "t_tr": "kutu, hoparlör",
        "t_pl": "pudło, kolumna głośnikowa"}),
    2370: (LIST, {"t_ru": "собственность, имущество", "t_tr": "mülk, mal", "t_pl": "własność, mienie"}),
    15459: (LIST, {"t_ru": "свинья, свиноматка", "t_uk": "свиня, свиноматка", "t_en": "sow, pig", "t_tr": "dişi domuz, domuz",
                   "t_pl": "świnia, locha"}),
    10348: (LIST, {"t_ru": "обаятельный, очаровательный", "t_uk": "чарівний, милий", "t_tr": "çekici, sevimli",
                   "t_pl": "czarujący, uroczy"}),
    2348: ("«Die Diskussion war interessant» — пусто; " + LIST, {
        "t_ru": "дискуссия, спор", "t_uk": "дискусія, суперечка", "t_en": "discussion, argument", "t_tr": "tartışma",
        "t_pl": "dyskusja, spór",
        **all_x("Keine Diskussion, du gehst jetzt ins Bett!", "Никаких дискуссий, марш спать!", "Жодних дискусій, марш спати!",
                "No discussion, you're going to bed now!", "Tartışma yok, şimdi yatıyorsun!",
                "Żadnej dyskusji, idziesz teraz spać!", "Niente discussioni, adesso vai a letto!",
                "¡Sin discusión, ahora te vas a la cama!", "Pas de discussion, tu vas au lit!", "Žádná diskuse, jdeš spát!")}),
    16056: (LIST + " (было семь значений)", {
        "t_ru": "взрывать, поливать", "t_uk": "підривати, поливати", "t_en": "to blow up, to sprinkle",
        "t_tr": "patlatmak, sulamak", "t_pl": "wysadzić, skropić", "t_it": "far saltare, annaffiare",
        "t_es": "volar, regar", "t_fr": "faire sauter, arroser", "t_cs": "odstřelit, kropit"}),
    6871: ("«Das ist ein interessantes Objekt» — пусто; " + LIST, {
        "t_ru": "объект, предмет", "t_uk": "об'єкт, предмет", "t_en": "object, property", "t_tr": "nesne, yapı",
        "t_pl": "obiekt, przedmiot", "t_cs": "objekt, předmět",
        **all_x("Das Objekt da am Himmel – ist das ein Flugzeug?", "Этот объект в небе — это самолёт?",
                "Цей об'єкт у небі — це літак?", "That object in the sky – is it a plane?",
                "Gökyüzündeki şu nesne uçak mı?", "Ten obiekt na niebie to samolot?", "Quell'oggetto nel cielo è un aereo?",
                "Ese objeto en el cielo, ¿es un avión?", "Cet objet dans le ciel, c'est un avion?",
                "Ten objekt na nebi – je to letadlo?")}),
    6872: (LIST + " (было семь значений)", {
        "t_ru": "собирать, строить", "t_uk": "збирати, будувати", "t_en": "to set up, to build up", "t_tr": "kurmak, geliştirmek",
        "t_pl": "rozstawić, zbudować", "t_it": "montare, costruire", "t_es": "montar, construir", "t_fr": "monter, construire",
        "t_cs": "postavit, sestavit", "x_ru": "Мы снова ставим палатку", "x_en": "We're putting the tent up again"}),
    10349: ("«Gemeinsam sind wir stark und vereint» — лозунг", {**all_x(
        "An Weihnachten ist die ganze Familie wieder vereint", "На Рождество вся семья снова воссоединяется",
        "На Різдво вся родина знову об'єднана", "At Christmas the whole family is reunited",
        "Noel'de bütün aile yeniden bir arada", "W święta cała rodzina jest znów połączona",
        "A Natale tutta la famiglia è di nuovo unita", "En Navidad toda la familia vuelve a estar unida",
        "À Noël, toute la famille est de nouveau réunie", "O Vánocích je celá rodina zase spojená")}),
    12551: ("«Der Unfall war leider tödlich» — хроника; " + LIST, {
        "t_ru": "смертельный, смертоносный", "t_uk": "смертельний, смертоносний", "t_en": "deadly, fatal",
        "t_tr": "ölümcül, öldürücü", "t_pl": "śmiertelny, zabójczy",
        **all_x("Dieser Pilz ist tödlich", "Этот гриб смертельно ядовит", "Цей гриб смертельно отруйний",
                "This mushroom is deadly", "Bu mantar ölümcül", "Ten grzyb jest śmiertelnie trujący",
                "Questo fungo è mortale", "Esta seta es mortal", "Ce champignon est mortel",
                "Tahle houba je smrtelně jedovatá")}),
    17925: ("«Diese Krankheit wird durch Gene übertragen» — учебник", {**all_x(
        "Das liegt bei uns in den Genen", "Это у нас в генах", "Це в нас у генах", "It's in our genes",
        "Bu bizim genlerimizde var", "To mamy w genach", "Ce l'abbiamo nei geni", "Lo llevamos en los genes",
        "C'est dans nos gènes", "To máme v genech")}),
    18686: (LIST, {"t_ru": "повод, случай", "t_uk": "привід, нагода", "t_en": "occasion, reason", "t_tr": "vesile, sebep",
                   "t_pl": "okazja, powód", "t_fr": "l'occasion, le motif"}),
    16057: ("«Nach der Niederlage begannen sie den Rückzug» — претерит, война; " + LIST, {
        "t_ru": "отступление, уход", "t_uk": "відступ, вихід", "t_en": "retreat, withdrawal", "t_tr": "geri çekilme, çekilme",
        "t_pl": "odwrót, wycofanie się", "t_fr": "la retraite, le retrait",
        **all_x("Für mich ist das kein Rückzug, sondern eine Pause", "Для меня это не уход, а пауза",
                "Для мене це не вихід, а пауза", "For me it's not a withdrawal, it's a break",
                "Benim için bu bir geri çekilme değil, bir mola", "Dla mnie to nie wycofanie się, tylko przerwa",
                "Per me non è un ritiro, ma una pausa", "Para mí no es una retirada, sino una pausa",
                "Pour moi, ce n'est pas un retrait, mais une pause", "Pro mě to není ústup, ale pauza")}),
    8814: ("пример про Nachtschicht, а не про Schicht; " + LIST, {
        "t_ru": "смена, слой", "t_uk": "зміна, шар", "t_en": "shift, layer", "t_tr": "vardiya, katman",
        "t_pl": "zmiana, warstwa", "t_fr": "le poste, la couche",
        **all_x("Meine Schicht fängt um sechs an", "Моя смена начинается в шесть", "Моя зміна починається о шостій",
                "My shift starts at six", "Vardiyam altıda başlıyor", "Moja zmiana zaczyna się o szóstej",
                "Il mio turno inizia alle sei", "Mi turno empieza a las seis", "Mon poste commence à six heures",
                "Moje směna začíná v šest")}),
    13951: (LIST, {"t_ru": "с другой стороны, зато", "t_uk": "з іншого боку, зате"}),
    13497: (EN + " («Has anyone of you»)", {"t_ru": "кто-нибудь, какой-нибудь", "t_uk": "хтось, якийсь",
                                           "t_en": "anyone, someone", "t_tr": "birisi, herhangi biri",
                                           "t_pl": "ktoś, któryś", "x_en": "Has any of you seen my phone?"}),
    16058: (EN + " («You can't command me!»); " + LIST, {
        "t_ru": "приказывать, велеть", "t_uk": "наказувати, веліти", "t_en": "to order, to command",
        "t_tr": "emretmek, emir vermek", "t_pl": "rozkazywać, kazać", "t_cs": "rozkazovat, poroučet",
        "x_en": "You can't order me around!"}),
    10351: ("ru «Я уже предчувствую, что случилось» — так не говорят; " + LIST, {
        "t_ru": "догадываться, предчувствовать", "t_uk": "здогадуватися, передчувати", "t_en": "to guess, to sense",
        "t_tr": "tahmin etmek, sezmek", "t_pl": "domyślać się, przeczuwać", "t_it": "intuire, immaginare",
        "t_es": "imaginarse, intuir", "t_fr": "se douter, deviner",
        "x_ru": "Я уже догадываюсь, что случилось", "x_en": "I can already guess what's happened"}),
    12154: (LIST, {"t_ru": "целиться", "t_uk": "цілитися", "t_en": "to aim", "t_tr": "nişan almak, hedeflemek",
                   "t_pl": "celować, mierzyć"}),
    6873: ("ru «Спустись вниз» — масло масляное", {"x_ru": "Спустись, пожалуйста, в гостиную!"}),
    6876: (EN, {"x_en": "We're going down the stairs"}),
    14436: ("шаблон Staffel («Die neue Staffel läuft …»); " + LIST, {
        "t_ru": "серия, эпизод", "t_uk": "серія, епізод", "t_en": "episode, incident", "t_tr": "bölüm, olay",
        "t_pl": "odcinek, epizod",
        **all_x("Ich schaue nur noch eine Episode, dann gehe ich schlafen", "Посмотрю ещё одну серию — и спать",
                "Подивлюся ще одну серію — і спати", "Just one more episode, then I'm off to bed",
                "Bir bölüm daha izleyip yatacağım", "Obejrzę jeszcze jeden odcinek i idę spać",
                "Guardo ancora un episodio e poi vado a dormire", "Veo un episodio más y me voy a dormir",
                "Je regarde encore un épisode et je vais me coucher", "Dám si ještě jeden díl a jdu spát")}),
    10352: ("«Nach dem Tor brach großer Jubel aus» — претерит; " + LIST, {
        "t_ru": "ликование, восторг", "t_uk": "радісні вигуки, тріумфування", "t_en": "cheering, jubilation",
        "t_tr": "coşku, tezahürat", "t_pl": "wiwaty, euforia", "t_fr": "la liesse, les acclamations",
        **all_x("Nach dem Tor gibt es im Stadion großen Jubel", "После гола на стадионе всеобщее ликование",
                "Після голу стадіон вибухає радісними вигуками", "After the goal there's huge cheering in the stadium",
                "Golden sonra stadyumda büyük bir coşku var", "Po golu na stadionie są wielkie wiwaty",
                "Dopo il gol nello stadio c'è grande esultanza", "Tras el gol hay un gran júbilo en el estadio",
                "Après le but, c'est la liesse dans le stade", "Po gólu je na stadionu velký jásot")}),
    6877: ("снова Projekt; " + LIST, {
        "t_ru": "довести до конца, провернуть", "t_uk": "довести до кінця, здійснити", "t_en": "to see through, to go through with",
        "t_tr": "sonuna kadar götürmek, tamamlamak", "t_pl": "doprowadzić do końca, przeprowadzić",
        **all_x("Wenn ich etwas anfange, ziehe ich es auch durch", "Если я что-то начинаю, то довожу до конца",
                "Якщо я щось починаю, то доводжу до кінця", "When I start something, I see it through",
                "Bir şeye başlarsam sonuna kadar götürürüm", "Jak coś zaczynam, to doprowadzam to do końca",
                "Quando inizio una cosa, la porto a termine", "Cuando empiezo algo, lo llevo a cabo",
                "Quand je commence quelque chose, je vais jusqu'au bout", "Když něco začnu, tak to i dotáhnu")}),
    9761: (LIST, {"t_ru": "жертвовать, сдавать (кровь)", "t_uk": "жертвувати, здавати (кров)",
                  "t_en": "to donate, to give (blood)", "t_tr": "bağışlamak, kan vermek", "t_pl": "ofiarować, oddać (krew)"}),
    1710: ("«Die Nachbarschaft ist freundlich» — пусто; en «neighborhood» — американское; " + LIST, {
        "t_ru": "соседство, район", "t_uk": "сусідство, район", "t_en": "neighbourhood, neighbours",
        "t_tr": "mahalle, komşuluk", "t_pl": "sąsiedztwo, okolica", "t_es": "el vecindario, el barrio",
        "t_cs": "sousedství, okolí",
        **all_x("In unserer Nachbarschaft kennt jeder jeden", "У нас в районе все друг друга знают",
                "У нашому районі всі одне одного знають", "In our neighbourhood everyone knows everyone",
                "Mahallemizde herkes birbirini tanır", "W naszej okolicy wszyscy się znają",
                "Nel nostro quartiere si conoscono tutti", "En nuestro barrio todo el mundo se conoce",
                "Dans notre quartier, tout le monde se connaît", "V našem okolí se všichni znají")}),
    16059: ("«Die Soldaten trugen grüne Tarnung» — претерит, война; " + LIST, {
        "t_ru": "маскировка, прикрытие", "t_uk": "маскування, прикриття", "t_en": "camouflage, cover",
        "t_tr": "kamuflaj, paravan", "t_pl": "kamuflaż, przykrywka", "t_it": "il camuffamento, la copertura",
        "t_cs": "maskování, krytí",
        **all_x("Der Job als Kellner war nur Tarnung", "Работа официантом была лишь прикрытием",
                "Робота офіціантом була лише прикриттям", "The waiter job was just a cover",
                "Garsonluk işi sadece bir paravandı", "Praca kelnera była tylko przykrywką",
                "Il lavoro da cameriere era solo una copertura", "El trabajo de camarero era solo una tapadera",
                "Le boulot de serveur n'était qu'une couverture", "Práce číšníka byla jen krytí")}),
    10354: ("«Er zeigte viel Mitgefühl …» — претерит; " + LIST, {
        "t_en": "sympathy, compassion", "t_tr": "merhamet, şefkat", "t_pl": "współczucie, empatia",
        **all_x("Du hast null Mitgefühl!", "У тебя ноль сочувствия!", "У тебе нуль співчуття!", "You've got zero sympathy!",
                "Sende hiç merhamet yok!", "Nie masz za grosz współczucia!", "Non hai un briciolo di compassione!",
                "¡No tienes ni pizca de compasión!", "Tu n'as aucune compassion!", "Nemáš ani špetku soucitu!")}),
}

SPLIT_LATER = {
    12551: ["tödlich langweilig = смертельно скучно"],
}
