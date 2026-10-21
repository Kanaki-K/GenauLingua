"""B1, блок 28: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    17096: (LIST + "; «бумажный платок» (марка Tempo) — другое значение", {
        "t_ru": "темп, скорость", "t_uk": "темп, швидкість", "t_en": "pace, speed", "t_tr": "tempo, hız",
        "t_pl": "tempo, szybkość", "t_fr": "le rythme, la vitesse"}),
    6766: (LIST, {"t_ru": "учитывать, обдумывать", "t_uk": "враховувати, обдумувати", "t_en": "to consider, to bear in mind",
                  "t_tr": "hesaba katmak, düşünmek", "t_pl": "brać pod uwagę, przemyśleć",
                  "t_fr": "prendre en compte, réfléchir à"}),
    18678: ("ru «Нам нужно сначала подождать» — калька; " + LIST, {
        "t_ru": "подождать, переждать", "t_uk": "зачекати, перечекати", "t_en": "to wait and see, to wait",
        "t_pl": "poczekać, odczekać", "x_ru": "Надо пока подождать", "x_uk": "Треба поки почекати",
        "x_en": "We'll just have to wait and see"}),
    16029: (LIST, {"t_ru": "следить, наблюдать", "t_uk": "стежити, спостерігати", "t_en": "to monitor, to watch over",
                   "t_tr": "izlemek, denetlemek", "t_pl": "nadzorować, monitorować", "t_it": "sorvegliare, controllare",
                   "t_cs": "hlídat, sledovat"}),
    8803: ("«Der Wächter kontrolliert die Eingänge» — инструкция; " + LIST, {
        "t_ru": "сторож, охранник", "t_uk": "сторож, охоронець", "t_en": "guard, watchman", "t_tr": "bekçi, gardiyan",
        "t_pl": "strażnik, ochroniarz", "t_es": "el vigilante, el guardia", "t_fr": "le gardien, le vigile",
        "t_cs": "hlídač, strážný",
        **all_x("Der Wächter lässt nachts niemanden rein", "Ночью сторож никого не пускает", "Уночі сторож нікого не пускає",
                "The guard doesn't let anyone in at night", "Bekçi gece kimseyi içeri almıyor",
                "Strażnik w nocy nikogo nie wpuszcza", "Di notte il guardiano non fa entrare nessuno",
                "Por la noche el vigilante no deja entrar a nadie", "La nuit, le gardien ne laisse entrer personne",
                "Hlídač v noci nikoho nepustí dovnitř")}),
    1775: (EN + " («I write the protocol»)", {"t_en": "minutes, record", "x_en": "I'm taking the minutes",
                                             "x_ru": "Я веду протокол"}),
    15444: ("ru «Мы хотим сажать» — несовершенный вид", {"x_ru": "Мы хотим посадить помидоры"}),
    14991: (EN + " («neighbor» — американское)", {"x_en": "My neighbour is a widow"}),
    6767: (LIST, {"t_ru": "упасть, рухнуть", "t_uk": "впасти, звалитися", "t_en": "to fall, to plunge",
                  "t_tr": "düşmek, yıkılmak", "t_pl": "upaść, runąć", "t_it": "cadere, precipitare",
                  "t_es": "caerse, precipitarse", "t_fr": "tomber, chuter", "t_cs": "upadnout, spadnout",
                  "x_ru": "Смотри не упади"}),
    8805: (LIST + " (было «приём у врача или терапевта»)", {
        "t_ru": "заседание, сеанс", "t_uk": "засідання, сеанс", "t_en": "meeting, session", "t_tr": "toplantı, seans",
        "t_pl": "posiedzenie, sesja", "t_it": "la seduta, la riunione", "t_fr": "la séance, la réunion",
        "t_cs": "schůze, sezení"}),
    2976: (LIST, {"t_ru": "переносить, ладить", "t_uk": "переносити, ладити", "t_en": "to tolerate, to get along",
                  "t_tr": "kaldırmak, iyi geçinmek", "t_pl": "znosić, dogadywać się", "t_it": "tollerare, andare d'accordo",
                  "t_es": "tolerar, llevarse bien", "t_fr": "supporter, s'entendre", "t_cs": "snášet, vycházet"}),
    6769: ("«Der Wind bläst heute stark» — снова погода; " + LIST, {
        "t_ru": "дуть, надувать", "t_uk": "дути, надувати", "t_en": "to blow", "t_tr": "üflemek, esmek",
        "t_pl": "dmuchać, wiać",
        **all_x("Blas mal auf die Suppe, die ist heiß", "Подуй на суп, он горячий", "Подуй на суп, він гарячий",
                "Blow on the soup, it's hot", "Çorbayı üfle, sıcak", "Podmuchaj na zupę, jest gorąca",
                "Soffia sulla minestra, è calda", "Sopla la sopa, que está caliente", "Souffle sur la soupe, elle est chaude",
                "Foukni do polévky, je horká")}),
    1531: ("«Das Wetter ist herrlich» — снова погода; " + LIST, {
        "t_ru": "чудесный, великолепный", "t_uk": "чудовий, прекрасний", "t_en": "wonderful, glorious",
        "t_tr": "harika, muhteşem", "t_pl": "wspaniały, cudowny", "t_it": "splendido, meraviglioso",
        **all_x("Das war ein herrlicher Urlaub", "Это был чудесный отпуск", "Це була чудова відпустка",
                "That was a wonderful holiday", "Harika bir tatildi", "To był wspaniały urlop",
                "È stata una vacanza splendida", "Fueron unas vacaciones maravillosas",
                "C'étaient des vacances magnifiques", "Byla to nádherná dovolená")}),
    2972: (LIST + "; en «I have sympathy for that» — так не говорят", {
        "t_ru": "понимание, сочувствие", "t_uk": "розуміння, співчуття", "t_en": "understanding, sympathy",
        "t_tr": "anlayış, hoşgörü", "x_en": "I can understand that"}),
    13934: (LIST, {"t_ru": "будь любезен", "t_uk": "будь ласкавий", "t_en": "kindly", "t_tr": "lütfen",
                   "t_it": "una buona volta"}),
    12139: (LIST, {"t_en": "coach, trainer", "t_tr": "antrenör, koç"}),
    15445: ("«Das Tal ist wunderschön» — пусто", {"t_ru": "долина", "t_uk": "долина", "t_en": "valley", **all_x(
        "Im Tal ist es oft neblig", "В долине часто туман", "У долині часто туман", "It's often foggy in the valley",
        "Vadide sık sık sis oluyor", "W dolinie często jest mgła", "Nella valle c'è spesso nebbia",
        "En el valle suele haber niebla", "Dans la vallée, il y a souvent du brouillard", "V údolí bývá často mlha")}),
    14421: ("«Das ist eine alte Tradition» — пусто", {**all_x(
        "Bei uns ist das Tradition", "У нас это традиция", "У нас це традиція", "It's a tradition with us",
        "Bizde bu bir gelenek", "U nas to tradycja", "Da noi è una tradizione", "En casa es una tradición",
        "Chez nous, c'est une tradition", "U nás je to tradice")}),
    1661: (EN + " (потеряно «old»); " + LIST, {
        "t_ru": "удалять, тушить", "t_uk": "видаляти, гасити", "t_en": "to delete, to put out", "t_pl": "usuwać, gasić",
        "t_fr": "supprimer, éteindre", "t_cs": "smazat, hasit", "x_en": "I'm deleting the old file"}),
    1126: ("ru «сходить в учреждение» — так не говорят", {
        "t_ru": "госучреждение, должность", "t_uk": "установа, посада", "t_en": "authorities, office",
        **all_x("Ich muss morgen aufs Amt", "Завтра мне надо в госучреждение", "Завтра мені треба в установу",
                "Tomorrow I have to go to the authorities", "Yarın resmi daireye gitmem lazım", "Jutro muszę iść do urzędu",
                "Domani devo andare in un ufficio pubblico", "Mañana tengo que ir a una oficina pública",
                "Demain, je dois aller à l'administration", "Zítra musím na úřad")}),
    2887: ("«Das Wasser tropft» — пусто", {"t_ru": "капать", "t_uk": "капати", **all_x(
        "Der Wasserhahn tropft schon seit Tagen", "Кран капает уже несколько дней", "Кран капає вже кілька днів",
        "The tap's been dripping for days", "Musluk günlerdir damlıyor", "Kran kapie już od kilku dni",
        "Il rubinetto gocciola da giorni", "El grifo lleva días goteando", "Le robinet goutte depuis des jours",
        "Kohoutek kape už několik dní")}),
    18680: (EN + " («movie» — американское)", {"t_es": "el comienzo, el principio",
                                             "x_en": "The start of the film was boring"}),
    115: ("«Sie bildet sich weiter» — это weiterbilden, а не bilden; " + LIST, {
        "t_ru": "образовывать, составлять", "t_uk": "утворювати, складати", "t_en": "to form, to make up",
        "t_tr": "oluşturmak, kurmak", "t_pl": "tworzyć, formować", "t_it": "formare, costituire",
        "t_es": "formar, constituir", "t_fr": "former, constituer", "t_cs": "tvořit, utvářet",
        **all_x("Bildet bitte zwei Gruppen!", "Образуйте, пожалуйста, две группы!", "Утворіть, будь ласка, дві групи!",
                "Please form two groups!", "Lütfen iki grup oluşturun!", "Utwórzcie, proszę, dwie grupy!",
                "Formate due gruppi, per favore!", "¡Formad dos grupos, por favor!",
                "Formez deux groupes, s'il vous plaît!", "Vytvořte prosím dvě skupiny!")}),
    10308: (LIST, {"t_ru": "застенчивый, робкий", "t_uk": "сором'язливий, несміливий", "t_en": "shy, timid",
                   "t_tr": "utangaç, çekingen"}),
    2612: ("«Der Kofferraum ist voll» — пусто", {"t_en": "boot, trunk", "t_es": "el maletero", **all_x(
        "Pack die Taschen in den Kofferraum", "Положи сумки в багажник", "Поклади сумки в багажник",
        "Put the bags in the boot", "Çantaları bagaja koy", "Włóż torby do bagażnika", "Metti le borse nel bagagliaio",
        "Mete las bolsas en el maletero", "Mets les sacs dans le coffre", "Dej tašky do kufru")}),
    13935: ("«Das war nur ein Missverständnis» — шаблон Versehen («Das war ein Versehen von mir»)", {**all_x(
        "Moment, das ist ein Missverständnis!", "Подожди, это недоразумение!", "Зачекай, це непорозуміння!",
        "Hang on, that's a misunderstanding!", "Bir dakika, bu bir yanlış anlama!", "Chwileczkę, to nieporozumienie!",
        "Aspetta, è un malinteso!", "¡Espera, es un malentendido!", "Attends, c'est un malentendu!",
        "Počkej, to je nedorozumění!")}),
    17921: ("«Das Experiment war erfolgreich» — отчёт", {**all_x(
        "Lass uns ein kleines Experiment machen", "Давай проведём небольшой эксперимент",
        "Давай проведемо невеликий експеримент", "Let's do a little experiment", "Küçük bir deney yapalım",
        "Zróbmy mały eksperyment", "Facciamo un piccolo esperimento", "Hagamos un pequeño experimento",
        "Faisons une petite expérience", "Udělejme malý experiment")}),
    16031: ("«Der Betrüger wurde verhaftet» — хроника; " + LIST, {
        "t_ru": "мошенник, жулик", "t_uk": "шахрай, обманщик", "t_en": "scammer, fraudster", "t_tr": "dolandırıcı, sahtekâr",
        "t_pl": "oszust, naciągacz", "t_es": "el estafador, el timador", "t_fr": "l'escroc, l'arnaqueur",
        **all_x("Vorsicht, am Telefon gibt es viele Betrüger", "Осторожно, по телефону звонит много мошенников",
                "Обережно, телефоном дзвонить багато шахраїв", "Watch out, there are lots of scammers on the phone",
                "Dikkat, telefonda çok dolandırıcı var", "Uważaj, przez telefon dzwoni wielu oszustów",
                "Attento, al telefono ci sono tanti truffatori", "Cuidado, por teléfono hay muchos estafadores",
                "Attention, il y a beaucoup d'escrocs au téléphone", "Pozor, po telefonu volá spousta podvodníků")}),
    2217: ("«Sei aufmerksam im Unterricht» — команда учителя; " + LIST, {
        "t_ru": "внимательный, заботливый", "t_uk": "уважний, дбайливий", "t_en": "attentive, thoughtful",
        "t_tr": "dikkatli, düşünceli", "t_pl": "uważny, troskliwy",
        **all_x("Er hört immer aufmerksam zu", "Он всегда внимательно слушает", "Він завжди уважно слухає",
                "He always listens attentively", "Hep dikkatle dinler", "Zawsze uważnie słucha",
                "Ascolta sempre con attenzione", "Siempre escucha con atención", "Il écoute toujours attentivement",
                "Vždycky pozorně poslouchá")}),
    13936: (LIST, {"t_ru": "болтовня, сплетни", "t_uk": "балаканина, плітки", "t_en": "talk, gossip",
                   "t_tr": "boş laf, dedikodu", "t_pl": "gadanie, plotki", "t_fr": "les bavardages, les ragots",
                   "t_cs": "řeči, pomluvy"}),
    2446: ("«Das ist eine wichtige Fähigkeit» — пусто; " + LIST, {
        "t_ru": "способность, умение", "t_uk": "здатність, уміння",
        **all_x("Sie hat die Fähigkeit, jeden zum Lachen zu bringen", "У неё есть способность рассмешить любого",
                "Вона має здатність розсмішити будь-кого", "She has the ability to make anyone laugh",
                "Herkesi güldürme yeteneği var", "Ma zdolność rozśmieszania każdego",
                "Ha la capacità di far ridere chiunque", "Tiene la capacidad de hacer reír a cualquiera",
                "Elle a la capacité de faire rire n'importe qui", "Má schopnost rozesmát kohokoli")}),
    6773: (LIST, {"t_ru": "уровень, этаж", "t_uk": "рівень, поверх", "t_en": "level, floor", "t_tr": "seviye, kat",
                  "t_pl": "poziom, kondygnacja", "t_it": "il livello, il piano", "t_es": "el nivel, la planta",
                  "t_fr": "le niveau, l'étage", "t_cs": "úroveň, patro"}),
    18162: (LIST, {"t_it": "il recinto, la recinzione"}),
    14992: ("снова Technologie", {**all_x(
        "In unserer Familie leben drei Generationen unter einem Dach",
        "В нашей семье под одной крышей живут три поколения", "У нашій родині під одним дахом живуть три покоління",
        "Three generations live under one roof in our family", "Ailemizde üç nesil aynı çatı altında yaşıyor",
        "W naszej rodzinie pod jednym dachem mieszkają trzy pokolenia",
        "Nella nostra famiglia tre generazioni vivono sotto lo stesso tetto",
        "En nuestra familia viven tres generaciones bajo el mismo techo",
        "Dans notre famille, trois générations vivent sous le même toit",
        "V naší rodině žijí tři generace pod jednou střechou")}),
    10311: ("ru «Ты не можешь меня обмануть» — калька; " + LIST, {
        "t_ru": "обманывать, ошибаться", "t_uk": "обманювати, помилятися", "t_en": "to deceive, to be mistaken",
        "t_tr": "aldatmak, yanılmak", "t_pl": "oszukiwać, mylić się", "t_it": "ingannare, sbagliarsi",
        "t_cs": "oklamat, mýlit se", "x_ru": "Меня не обманешь", "x_uk": "Мене не обманеш", "x_en": "You can't fool me"}),
    6774: (LIST, {"t_ru": "удерживать, проводить", "t_uk": "утримувати, проводити", "t_en": "to keep from, to hold",
                  "t_tr": "alıkoymak, düzenlemek", "t_pl": "powstrzymywać, odbywać", "t_it": "impedire, tenere",
                  "t_es": "impedir, celebrar", "t_fr": "empêcher, tenir", "t_cs": "zabránit, pořádat"}),
    6775: (LIST, {"t_ru": "хлопок, грохот", "t_uk": "гуркіт, ляск", "t_en": "bang, pop", "t_tr": "patlama sesi, çat sesi",
                  "t_pl": "huk, trzask", "t_es": "el estallido, el estruendo", "t_fr": "la détonation, le claquement"}),
    2586: ("«Irgendwer wird mir helfen?» — так не говорят", {**all_x(
        "Irgendwer klingelt an der Tür", "Кто-то звонит в дверь", "Хтось дзвонить у двері",
        "Someone's ringing the doorbell", "Biri kapıyı çalıyor", "Ktoś dzwoni do drzwi", "Qualcuno suona alla porta",
        "Alguien llama a la puerta", "Quelqu'un sonne à la porte", "Někdo zvoní u dveří")}),
    6777: (LIST + "; ru «сильная ссора» — калька", {
        "t_ru": "сильный, бурный", "t_uk": "сильний, бурхливий", "t_en": "intense, fierce", "t_tr": "şiddetli, sert",
        "t_pl": "gwałtowny, silny", "t_it": "violento, forte", "t_es": "fuerte, violento", "t_fr": "violent, vif",
        "t_cs": "prudký, silný", "x_ru": "Это была бурная ссора", "x_en": "That was a fierce argument"}),
    6778: (LIST, {"t_ru": "понимать, осознавать", "t_uk": "розуміти, усвідомлювати", "t_en": "to understand, to grasp",
                  "t_tr": "anlamak, kavramak", "t_pl": "pojmować, rozumieć"}),
}

SPLIT_LATER = {
    17096: ["das Tempo (разг.) = бумажный платок; Tempo 30 = ограничение скорости"],
    6775: ["einen Knall haben = быть чокнутым"],
}
