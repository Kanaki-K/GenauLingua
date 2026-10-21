"""B1, блок 37: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6889: ("ru «каждую деталь того вечера» — калька", {"x_ru": "Расскажи мне в подробностях про тот вечер",
                                                       "x_en": "Tell me every detail of that evening"}),
    10359: ("«Du siehst heute Abend umwerfend aus» — шаблон fabelhaft («Du siehst fabelhaft aus!»); " + LIST, {
        "t_ru": "потрясающий, сногсшибательный", "t_uk": "приголомшливий, сліпучий", "t_en": "stunning, amazing",
        "t_tr": "muhteşem, göz kamaştırıcı", "t_pl": "oszałamiający, zjawiskowy",
        **all_x("Der Blick vom Gipfel ist einfach umwerfend", "Вид с вершины просто сногсшибательный",
                "Вид з вершини просто приголомшливий", "The view from the top is simply stunning",
                "Zirveden manzara tek kelimeyle muhteşem", "Widok ze szczytu jest po prostu oszałamiający",
                "La vista dalla cima è semplicemente stupenda", "La vista desde la cima es simplemente espectacular",
                "La vue du sommet est tout simplement époustouflante", "Výhled z vrcholu je prostě úžasný")}),
    8821: (LIST, {"t_ru": "эксперт, знаток", "t_uk": "експерт, знавець", "t_pl": "ekspert, znawca"}),
    16066: (LIST + "; en «vacation» — американское", {
        "t_ru": "право, претензия", "t_uk": "право, претензія", "t_en": "claim, entitlement", "t_tr": "hak, talep",
        "t_pl": "prawo, roszczenie", "t_fr": "le droit, l'exigence", "x_en": "You're entitled to two weeks' holiday"}),
    10360: ("пример многословный; живое — «ein ungutes Gefühl»", {**all_x(
        "Ich habe ein ungutes Gefühl dabei", "У меня нехорошее предчувствие", "У мене недобре передчуття",
        "I've got a bad feeling about this", "İçimde kötü bir his var", "Mam niedobre przeczucie",
        "Ho una brutta sensazione", "Tengo un mal presentimiento", "J'ai un mauvais pressentiment", "Mám z toho špatný pocit")}),
    16067: ("«Die Polizei fand Kokain …» — претерит", {**all_x(
        "Die Polizei hat Kokain in seinem Auto gefunden", "Полиция нашла кокаин в его машине",
        "Поліція знайшла кокаїн у його машині", "The police found cocaine in his car", "Polis arabasında kokain buldu",
        "Policja znalazła kokainę w jego samochodzie", "La polizia ha trovato cocaina nella sua macchina",
        "La policía ha encontrado cocaína en su coche", "La police a trouvé de la cocaïne dans sa voiture",
        "Policie mu našla v autě kokain")}),
    16068: ("ru «заключили соглашение» — канцелярит", {
        "x_ru": "У нас договорённость, кто что делает", "x_uk": "У нас домовленість, хто що робить",
        "x_en": "We've made an arrangement about who does what"}),
    10361: ("«Kann ich dir behilflich sein?» — формула вежливости, говорят на «Sie»", {**all_x(
        "Kann ich Ihnen behilflich sein?", "Могу я вам чем-нибудь помочь?", "Чи можу я вам чимось допомогти?",
        "Can I be of any help?", "Size yardımcı olabilir miyim?", "Czy mogę Panu w czymś pomóc?",
        "Posso esserLe d'aiuto?", "¿Puedo serle de ayuda?", "Je peux vous être utile?", "Mohu vám být nápomocný?")}),
    13955: ("«Den Nachrichten zufolge wird es morgen regnen» — снова погода", {**all_x(
        "Seiner Aussage zufolge war er zu Hause", "Согласно его показаниям, он был дома",
        "Згідно з його свідченнями, він був удома", "According to his statement, he was at home",
        "İfadesine göre evdeymiş", "Według jego zeznań był w domu", "Secondo la sua deposizione, era a casa",
        "Según su declaración, estaba en casa", "D'après sa déposition, il était chez lui", "Podle jeho výpovědi byl doma")}),
    8823: ("«female solicitor» — лишнее; ru «мне не нужно» — не тот смысл", {
        "t_en": "lawyer, solicitor", "t_tr": "avukat", "x_ru": "Мой адвокат сказала ничего не подписывать"}),
    13956: (EN, {"x_en": "Pardon, could you say that again?"}),
    2827: ("«Der Sonnenuntergang ist schön» — пусто", {"t_uk": "захід сонця", **all_x(
        "Lass uns den Sonnenuntergang am Strand anschauen", "Давай посмотрим закат на пляже",
        "Давай подивимося на захід сонця на пляжі", "Let's watch the sunset on the beach",
        "Gün batımını sahilde izleyelim", "Popatrzmy na zachód słońca na plaży", "Guardiamo il tramonto in spiaggia",
        "Vamos a ver la puesta de sol en la playa", "Allons regarder le coucher de soleil sur la plage",
        "Pojďme se podívat na západ slunce na pláži")}),
    16069: ("пример из полицейской хроники; " + LIST, {
        "t_ru": "похитить, угнать", "t_uk": "викрасти, захопити", "t_en": "to kidnap, to hijack", "t_tr": "kaçırmak",
        "t_pl": "porwać, uprowadzić",
        **all_x("Heute Abend entführe ich dich ins Kino!", "Сегодня вечером я похищаю тебя в кино!",
                "Сьогодні ввечері я викрадаю тебе в кіно!", "I'm kidnapping you to the cinema tonight!",
                "Bu akşam seni sinemaya kaçırıyorum!", "Dziś wieczorem porywam cię do kina!",
                "Stasera ti rapisco e ti porto al cinema!", "¡Esta noche te secuestro y te llevo al cine!",
                "Ce soir, je t'enlève et je t'emmène au cinéma!", "Dnes večer tě unesu do kina!")}),
    13502: ("«Es regnete stark, sodass wir zu Hause blieben» — претерит", {**all_x(
        "Es hat stark geregnet, sodass wir zu Hause geblieben sind", "Шёл сильный дождь, так что мы остались дома",
        "Ішов сильний дощ, так що ми залишилися вдома", "It was raining hard, so we stayed at home",
        "Çok yağmur yağdı, bu yüzden evde kaldık", "Mocno padało, tak że zostaliśmy w domu",
        "Pioveva forte, per cui siamo rimasti a casa", "Llovió mucho, así que nos quedamos en casa",
        "Il pleuvait fort, si bien que nous sommes restés à la maison", "Silně pršelo, takže jsme zůstali doma")}),
    15010: (LIST, {"t_ru": "хозяйка, госпожа", "t_uk": "господиня, пані", "t_en": "mistress, owner",
                   "t_tr": "sahibi, hanımefendi", "t_pl": "pani, właścicielka"}),
    9764: ("убрать пометку (hovor.)", {"t_cs": "spropitné, dýško", "t_en": "tip"}),
    2390: ("«Sie haben ihn eingesperrt» — пусто; " + LIST, {
        "t_ru": "запирать, сажать в тюрьму", "t_uk": "замикати, садити до в'язниці", "t_en": "to lock up, to shut in",
        "t_tr": "kilitlemek, hapsetmek", "t_pl": "zamknąć, uwięzić",
        **all_x("Sperr den Hund nicht im Auto ein!", "Не запирай собаку в машине!", "Не замикай собаку в машині!",
                "Don't lock the dog in the car!", "Köpeği arabada kilitleme!", "Nie zamykaj psa w samochodzie!",
                "Non rinchiudere il cane in macchina!", "¡No encierres al perro en el coche!",
                "N'enferme pas le chien dans la voiture!", "Nezavírej psa v autě!")}),
    8824: (LIST, {"t_ru": "предприятие, работа", "t_uk": "підприємство, робота", "t_en": "company, operation",
                  "t_tr": "işletme, faaliyet", "t_pl": "firma, zakład", "t_it": "l'azienda, il funzionamento",
                  "t_fr": "l'entreprise, le fonctionnement", "t_cs": "podnik, provoz"}),
    17111: ("«Die Autos rasen viel zu schnell» — масло масляное; " + LIST, {
        "t_ru": "гнать, мчаться", "t_uk": "гнати, мчати", "t_en": "to speed, to race", "t_tr": "hızla gitmek, çok hızlı sürmek",
        "t_pl": "pędzić, mknąć",
        **all_x("Er rast immer wie ein Verrückter", "Он всегда гоняет как сумасшедший", "Він завжди жене як навіжений",
                "He always speeds like a maniac", "Hep deli gibi hızlı sürüyor", "Zawsze pędzi jak wariat",
                "Sfreccia sempre come un pazzo", "Siempre va a toda velocidad como un loco",
                "Il fonce toujours comme un fou", "Vždycky se řítí jako blázen")}),
    17929: (EN, {"x_en": "Research into new medicines takes years"}),
    12553: ("«Der verwundete Soldat brauchte …» — претерит", {**all_x(
        "Er ist im Krieg schwer verwundet worden", "Он был тяжело ранен на войне", "Його тяжко поранило на війні",
        "He was badly wounded in the war", "Savaşta ağır yaralandı", "Został ciężko ranny na wojnie",
        "È stato ferito gravemente in guerra", "Lo hirieron gravemente en la guerra", "Il a été grièvement blessé à la guerre",
        "Ve válce byl těžce raněn")}),
    10363: ("«Deine Manieren sind wirklich schlecht» — пусто", {**all_x(
        "Wo sind denn deine Manieren?", "Где твои манеры?", "Де твої манери?", "Where are your manners?",
        "Görgün nerede?", "Gdzie twoje maniery?", "Dove sono le tue buone maniere?", "¿Dónde están tus modales?",
        "Où sont passées tes manières?", "Kde máš způsoby?")}),
    13957: ("убрать пометку (fam.)", {"t_fr": "non, nan"}),
    6891: ("«Der Pfeil flog direkt ins Ziel» — претерит; шаблон weisen («Der Pfeil weist …»); " + LIST, {
        "t_ru": "стрелка, стрела", "t_uk": "стрілка, стріла", "t_en": "arrow", "t_tr": "ok, ok işareti",
        "t_pl": "strzałka, strzała", "t_cs": "šipka, šíp",
        **all_x("Folg einfach den Pfeilen", "Просто иди по стрелкам", "Просто йди за стрілками", "Just follow the arrows",
                "Okları takip et", "Po prostu idź za strzałkami", "Segui le frecce", "Sigue las flechas",
                "Suis les flèches", "Prostě jdi podle šipek")}),
    6892: ("шаблон Fleck («… ein großer Fleck»)", {**all_x(
        "Manchmal wäre ich gern unsichtbar", "Иногда мне хотелось бы быть невидимкой", "Іноді мені хотілося б бути невидимим",
        "Sometimes I'd like to be invisible", "Bazen görünmez olmak isterdim", "Czasem chciałbym być niewidzialny",
        "A volte vorrei essere invisibile", "A veces me gustaría ser invisible", "Parfois, j'aimerais être invisible",
        "Někdy bych chtěl být neviditelný")}),
    6893: ("«Das Prinzip ist eigentlich ganz einfach zu verstehen» — многословно; живое — «Im Prinzip»", {**all_x(
        "Im Prinzip hast du recht", "В принципе, ты прав", "У принципі, ти маєш рацію", "In principle you're right",
        "Prensipte haklısın", "W zasadzie masz rację", "In linea di principio hai ragione", "En principio tienes razón",
        "En principe, tu as raison", "V principu máš pravdu")}),
}

SPLIT_LATER = {
    8824: ["in Betrieb = работает (Die Maschine ist in Betrieb); Betrieb = оживление (Hier ist viel Betrieb)"],
}
