"""B1, блок 29: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2070: (LIST, {"t_ru": "заходить, заглядывать", "t_uk": "заходити, забігати", "t_en": "to drop by, to come past",
                  "t_tr": "uğramak", "t_pl": "wpadać, zaglądać"}),
    11670: (EN, {"x_en": "He likes a whisky in the evening"}),
    6781: (LIST + "; en «You can't determine everything» — так не говорят", {
        "t_ru": "решать, определять", "t_uk": "вирішувати, визначати", "t_en": "to decide, to determine",
        "t_tr": "karar vermek, belirlemek", "t_pl": "decydować, określać", "t_it": "decidere, determinare",
        "t_es": "decidir, mandar", "x_en": "You can't decide everything"}),
    16033: ("«Das ist eine verdächtige Person» — протокол; " + LIST, {
        "t_ru": "подозрительный", "t_uk": "підозрілий", "t_en": "suspicious", "t_tr": "şüpheli", "t_pl": "podejrzany",
        **all_x("Das kommt mir verdächtig vor", "Мне это кажется подозрительным", "Мені це здається підозрілим",
                "That looks suspicious to me", "Bu bana şüpheli geliyor", "To wydaje mi się podejrzane",
                "Mi sembra sospetto", "Me parece sospechoso", "Ça me paraît suspect", "Připadá mi to podezřelé")}),
    12141: (LIST, {"t_en": "spectator, viewer"}),
    6782: ("«Das war ein seltsamer Vorfall» — шаблон «Das war ein …»; " + LIST, {
        "t_ru": "происшествие, случай", "t_uk": "випадок, інцидент", "t_en": "incident", "t_pl": "zdarzenie, incydent",
        "t_it": "l'episodio, l'incidente", "t_cs": "příhoda, incident",
        **all_x("Über den Vorfall reden wir später", "Об этом случае поговорим позже", "Про цей випадок поговоримо пізніше",
                "We'll talk about the incident later", "Olay hakkında sonra konuşuruz",
                "O tym zdarzeniu porozmawiamy później", "Dell'episodio parliamo dopo", "Del incidente hablamos luego",
                "On parlera de l'incident plus tard", "O té příhodě si promluvíme později")}),
    6783: ("«Er muss etwas Großes vorhaben» — живее «Was hast du vor?»; " + LIST, {
        "t_ru": "собираться, планировать", "t_uk": "збиратися, планувати", "t_en": "to plan, to be up to",
        "t_tr": "planlamak, niyetinde olmak", "t_pl": "zamierzać, planować", "t_it": "avere in mente, progettare",
        "t_es": "planear, tener pensado", "t_fr": "avoir en tête, prévoir", "t_cs": "chystat, plánovat",
        **all_x("Was hast du heute Abend vor?", "Какие у тебя планы на вечер?", "Які в тебе плани на вечір?",
                "What are you up to tonight?", "Bu akşam ne planlıyorsun?", "Co planujesz dziś wieczorem?",
                "Cos'hai in mente per stasera?", "¿Qué tienes pensado para esta noche?", "Tu as prévu quoi ce soir?",
                "Co chystáš na dnešní večer?")}),
    11671: (LIST, {"t_it": "il panino, il tramezzino"}),
    6784: ("«Ich setze alle Mittel ein» — книжно; " + LIST + " (было шесть значений)", {
        "t_ru": "использовать, задействовать", "t_uk": "використовувати, залучати", "t_en": "to use, to deploy",
        "t_tr": "kullanmak, devreye sokmak", "t_pl": "stosować, angażować", "t_it": "impiegare, usare",
        "t_es": "emplear, usar", "t_fr": "employer, utiliser", "t_cs": "použít, nasadit",
        **all_x("Wir müssen mehr Personal einsetzen", "Нам нужно задействовать больше персонала",
                "Нам треба залучити більше персоналу", "We need to deploy more staff",
                "Daha fazla personel kullanmamız lazım", "Musimy zaangażować więcej personelu",
                "Dobbiamo impiegare più personale", "Tenemos que emplear a más personal",
                "Il faut employer plus de personnel", "Musíme nasadit víc personálu")}),
    14422: ("«Kinder lieben Märchen» — пусто; " + LIST, {
        "t_ru": "сказка, выдумка", "t_uk": "казка, вигадка", "t_en": "fairy tale, tall tale", "t_pl": "bajka, baśń",
        **all_x("Erzähl mir keine Märchen!", "Не рассказывай мне сказки!", "Не розповідай мені казок!",
                "Don't tell me fairy tales!", "Bana masal anlatma!", "Nie opowiadaj mi bajek!", "Non raccontarmi favole!",
                "¡No me cuentes cuentos!", "Ne me raconte pas de contes!", "Nevykládej mi pohádky!")}),
    13937: (LIST, {"t_ru": "кстати, к слову", "t_uk": "до речі, до слова", "t_en": "by the way, speaking of which",
                   "t_tr": "bu arada, laf açılmışken", "t_pl": "a propos, przy okazji"}),
    6785: (LIST + "; ru «ненадолго прервать» — канцелярит", {
        "t_ru": "прерывать, перебивать", "t_uk": "перебивати, перервати", "t_en": "to interrupt, to break off",
        "t_tr": "sözünü kesmek, kesmek", "t_pl": "przerywać, wstrzymywać",
        "x_ru": "Извини, можно тебя на секунду перебить?", "x_en": "Sorry, can I interrupt you for a second?"}),
    10312: (LIST, {"t_ru": "увлекательный, захватывающий", "t_uk": "захопливий, неймовірний",
                   "t_en": "fascinating, captivating", "t_tr": "büyüleyici, çok ilginç", "t_pl": "fascynujący, porywający"}),
    12535: ("«Sie wurde ohnmächtig und fiel um» — претерит; " + LIST, {
        "t_ru": "без сознания, в обмороке", "t_uk": "непритомний, безсилий", "t_en": "unconscious, passed out",
        "t_tr": "baygın, güçsüz", "t_pl": "omdlały, bezsilny", "t_it": "svenuto, impotente",
        "t_es": "desmayado, impotente", "t_cs": "omdlelý, bezmocný",
        **all_x("Mir war so heiß, ich bin fast ohnmächtig geworden", "Мне было так жарко, что я чуть не упал в обморок",
                "Мені було так спекотно, що я мало не знепритомнів", "I was so hot I nearly passed out",
                "O kadar sıcaktı ki neredeyse bayılıyordum", "Było mi tak gorąco, że prawie zemdlałem",
                "Avevo così caldo che sono quasi svenuto", "Tenía tanto calor que casi me desmayo",
                "J'avais tellement chaud que j'ai failli m'évanouir", "Bylo mi takové horko, že jsem skoro omdlel")}),
    16034: (LIST, {"t_ru": "алиби, отговорка", "t_uk": "алібі, відмовка", "t_tr": "mazeret, bahane",
                   "t_pl": "alibi, wymówka"}),
    6786: (LIST + "; ru «находится в тяжёлом кризисе» — канцелярит", {
        "t_ru": "кризис", "t_uk": "криза", "t_en": "crisis", "t_tr": "kriz, buhran", "t_pl": "kryzys",
        "x_ru": "У фирмы серьёзный кризис"}),
    8806: (EN, {"x_en": "My brother is in the navy"}),
    12536: (LIST, {"t_ru": "кома", "t_uk": "кома", "t_pl": "śpiączka"}),
    1548: ("«Er ist sehr höflich» — пусто", {"t_tr": "nazik, kibar", "t_it": "educato, gentile", **all_x(
        "Sei bitte höflich zu den Gästen", "Будь, пожалуйста, вежлив с гостями", "Будь, будь ласка, ввічливим із гостями",
        "Please be polite to the guests", "Lütfen misafirlere karşı kibar ol", "Bądź, proszę, uprzejmy dla gości",
        "Sii gentile con gli ospiti, per favore", "Sé educado con los invitados, por favor",
        "Sois poli avec les invités, s'il te plaît", "Buď prosím k hostům zdvořilý")}),
    17922: ("«Die Rakete fliegt zum Mond» — детский; " + LIST, {
        "t_ru": "ракета", "t_uk": "ракета", "t_en": "rocket", "t_tr": "roket, havai fişek", "t_pl": "rakieta",
        **all_x("An Silvester schießen wir Raketen ab", "На Новый год мы запускаем ракеты", "На Новий рік ми запускаємо ракети",
                "We set off rockets on New Year's Eve", "Yılbaşında havai fişek atıyoruz", "W sylwestra puszczamy rakiety",
                "A Capodanno lanciamo i razzi", "En Nochevieja tiramos cohetes", "Au Nouvel An, on tire des fusées",
                "Na Silvestra pouštíme rakety")}),
    10314: (LIST, {"t_ru": "верность, преданность", "t_uk": "вірність, відданість", "t_en": "loyalty",
                   "t_tr": "sadakat, bağlılık", "t_pl": "lojalność, wierność"}),
    16036: ("«Der Täter machte ein volles Geständnis» — претерит, протокол; " + LIST, {
        "t_ru": "признание", "t_uk": "зізнання, визнання вини", "t_en": "confession", "t_tr": "itiraf",
        "t_pl": "przyznanie się, wyznanie",
        **all_x("Ich muss dir ein Geständnis machen", "У меня к тебе признание", "Мушу тобі в дечому зізнатися",
                "I have a confession to make", "Sana bir itirafım var", "Muszę ci się do czegoś przyznać",
                "Devo farti una confessione", "Tengo que hacerte una confesión", "J'ai un aveu à te faire",
                "Musím se ti k něčemu přiznat")}),
    10315: ("«Lautes Gelächter kam aus dem Zimmer» — претерит", {**all_x(
        "Aus dem Zimmer hört man lautes Gelächter", "Из комнаты слышен громкий смех", "З кімнати чути гучний сміх",
        "You can hear loud laughter from the room", "Odadan yüksek kahkahalar geliyor", "Z pokoju słychać głośny śmiech",
        "Dalla stanza si sentono forti risate", "Desde la habitación se oyen risas fuertes",
        "On entend de grands éclats de rire dans la pièce", "Z pokoje je slyšet hlasitý smích")}),
    2949: (LIST, {"t_ru": "проходить, заблудиться", "t_uk": "проходити, заблукати", "t_en": "to go, to get lost",
                  "t_tr": "geçmek, yolunu kaybetmek", "t_pl": "przebiegać, zgubić się", "t_it": "andare, perdersi",
                  "t_es": "salir, perderse", "t_fr": "se passer, se perdre", "t_cs": "proběhnout, zabloudit"}),
    14425: (LIST, {"t_ru": "пение, вокал", "t_uk": "спів, вокал", "t_en": "singing, vocals", "t_tr": "şarkı söyleme, vokal",
                   "t_pl": "śpiew, wokal"}),
    12537: (LIST, {"t_ru": "психиатр", "t_uk": "психіатр", "t_tr": "psikiyatrist", "t_pl": "psychiatra"}),
    1709: (LIST, {"t_ru": "образец, узор", "t_uk": "зразок, узор", "t_en": "sample, pattern", "t_tr": "numune, desen",
                  "t_pl": "wzór, próbka", "t_it": "il campione, il motivo", "t_es": "la muestra, el estampado",
                  "t_fr": "l'échantillon, le motif"}),
    6789: ("«Kannst du das Geschirr wegnehmen?» — так не говорят (abräumen); " + LIST, {
        "t_ru": "забирать, отбирать", "t_uk": "забирати, відбирати", "t_en": "to take away, to remove",
        "t_tr": "almak, elinden almak", "t_pl": "zabierać, odbierać",
        **all_x("Nimm ihm bitte die Schere weg!", "Забери у него, пожалуйста, ножницы!", "Забери в нього, будь ласка, ножиці!",
                "Please take the scissors away from him!", "Lütfen makası elinden al!", "Zabierz mu, proszę, nożyczki!",
                "Togligli le forbici, per favore!", "¡Quítale las tijeras, por favor!", "Enlève-lui les ciseaux, s'il te plaît!",
                "Vezmi mu prosím ty nůžky!")}),
    17099: ("«Das Fahrzeug steht vor der Tür» — пусто; " + LIST, {
        "t_ru": "транспортное средство, машина", "t_uk": "транспортний засіб, машина", "t_tr": "araç, taşıt",
        "t_pl": "pojazd",
        **all_x("Wem gehört das Fahrzeug da vorne?", "Чья это машина впереди?", "Чия це машина попереду?",
                "Whose vehicle is that up ahead?", "Şuradaki araç kimin?", "Do kogo należy ten pojazd z przodu?",
                "Di chi è quel veicolo lì davanti?", "¿De quién es ese vehículo de ahí delante?",
                "À qui est le véhicule là-devant?", "Čí je to vozidlo tamhle vpředu?")}),
    12538: ("«Ohne Essen werden wir verhungern» — пусто; живое — «Ich verhungere!»", {
        "t_ru": "умереть с голоду", "t_uk": "померти з голоду", "t_en": "to starve",
        **all_x("Wann gibt's Essen? Ich verhungere!", "Когда будет еда? Я умираю с голоду!",
                "Коли буде їжа? Я помираю з голоду!", "When's dinner? I'm starving!",
                "Yemek ne zaman? Açlıktan ölüyorum!", "Kiedy jedzenie? Umieram z głodu!",
                "Quando si mangia? Sto morendo di fame!", "¿Cuándo se come? ¡Me muero de hambre!",
                "On mange quand? Je meurs de faim!", "Kdy bude jídlo? Umírám hlady!")}),
    10316: (LIST, {"t_ru": "клясться, присягать", "t_uk": "клястися, присягати", "t_en": "to swear, to vow",
                   "t_tr": "yemin etmek, and içmek", "t_pl": "przysięgać, poprzysiąc"}),
    6790: (LIST + "; «разорванный» — другое слово (reißen)", {
        "t_ru": "хитрый, пронырливый", "t_uk": "хитрий, спритний", "t_en": "cunning, crafty", "t_tr": "kurnaz, açıkgöz",
        "t_pl": "przebiegły, cwany", "t_it": "scaltro, furbo", "t_es": "astuto, pillo", "t_fr": "rusé, malin",
        "t_cs": "mazaný, vychytralý"}),
    9755: ("«Die Summe beträgt 100 Euro» — квитанция; " + LIST, {
        "t_ru": "сумма, итог", "t_uk": "сума, підсумок", "t_en": "sum, amount", "t_tr": "meblağ, toplam",
        "t_pl": "suma, kwota", "t_it": "la somma, l'importo", "t_es": "la suma, el importe", "t_fr": "la somme, le montant",
        "t_cs": "suma, částka",
        **all_x("Das ist eine ganz schöne Summe!", "Это кругленькая сумма!", "Це чимала сума!", "That's quite a sum!",
                "Bu epey yüklü bir meblağ!", "To niezła suma!", "È una bella somma!", "¡Es una buena suma!",
                "C'est une jolie somme!", "To je pěkná suma!")}),
    2485: ("«Die Demonstration war friedlich» — хроника; " + LIST, {
        "t_ru": "мирный, спокойный", "t_uk": "мирний, спокійний", "t_en": "peaceful, calm", "t_tr": "barışçıl, huzurlu",
        "t_pl": "pokojowy, spokojny", "t_cs": "pokojný, klidný",
        **all_x("Bei uns im Dorf ist es sehr friedlich", "У нас в деревне очень спокойно", "У нас у селі дуже спокійно",
                "It's very peaceful in our village", "Köyümüz çok huzurlu", "U nas na wsi jest bardzo spokojnie",
                "Nel nostro paese è molto tranquillo", "En nuestro pueblo se vive muy tranquilo",
                "Dans notre village, c'est très paisible", "U nás na vesnici je velký klid")}),
    14426: (LIST, {"t_ru": "режиссёр", "t_uk": "режисер", "t_en": "director", "t_tr": "yönetmen"}),
    6791: (LIST, {"t_ru": "наполнять, заполнять", "t_uk": "наповнювати, заповнювати", "t_en": "to fill, to stuff",
                  "t_pl": "napełniać, wypełniać"}),
    12539: ("«Die Patientin wartet in Zimmer 5» — шаблон Patient («Der Patient wartet»)", {
        "t_ru": "пациентка", "t_uk": "пацієнтка", "t_en": "patient", "t_tr": "hasta", "t_pl": "pacjentka",
        **all_x("Die Patientin darf morgen nach Hause", "Пациентку завтра отпускают домой", "Пацієнтку завтра відпускають додому",
                "The patient can go home tomorrow", "Hasta yarın eve gidebilir", "Pacjentka może jutro wrócić do domu",
                "La paziente domani può tornare a casa", "La paciente puede irse a casa mañana",
                "La patiente peut rentrer chez elle demain", "Pacientka může zítra domů")}),
    18164: (EN + " («basement» — американское)", {"x_en": "Please fetch the bucket from the cellar",
                                                "t_es": "el cubo, el balde"}),
    1679: (LIST, {"t_ru": "мышь", "t_uk": "миша", "t_en": "mouse", "t_tr": "fare", "t_pl": "mysz"}),
}

SPLIT_LATER = {
    6784: ["sich einsetzen für = заступаться; einsetzen = начинаться (Der Regen setzt ein)"],
    6790: ["gerissen = разорванный (Partizip от reißen)"],
}
