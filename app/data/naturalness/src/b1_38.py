"""B1, блок 38: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2312: (LIST, {"t_ru": "тормозить, сдерживать", "t_uk": "гальмувати, стримувати", "t_en": "to brake, to slow down",
                  "t_tr": "fren yapmak, yavaşlatmak", "t_pl": "hamować, zwalniać"}),
    6895: (LIST, {"t_ru": "мнение, вид", "t_uk": "думка, вид", "t_en": "opinion, view", "t_tr": "görüş, görünüm",
                  "t_pl": "zdanie, widok", "t_it": "l'opinione, la vista", "t_fr": "l'avis, la vue"}),
    6896: ("ru «совершенно безобидная» — согласование; " + LIST, {
        "t_ru": "безобидный, безвредный", "t_uk": "нешкідливий, безневинний", "t_en": "harmless", "t_tr": "zararsız, masum",
        "x_ru": "Собака с виду опасная, но совершенно безобидная",
        "x_en": "The dog looks dangerous, but it's completely harmless"}),
    13959: (LIST, {"t_ru": "конверт, обложка", "t_uk": "конверт, обкладинка", "t_en": "envelope, cover",
                   "t_tr": "zarf, kapak", "t_pl": "koperta, okładka", "t_it": "la busta, la copertina",
                   "t_fr": "l'enveloppe, la couverture", "t_cs": "obálka, obal"}),
    12554: ("«Mir tut der Nacken weh» — шаблон «tut weh»; " + LIST, {
        "t_ru": "шея, затылок", "t_uk": "шия, потилиця", "t_en": "neck, nape", "t_tr": "ense, boyun", "t_pl": "kark",
        **all_x("Ich habe einen steifen Nacken", "У меня затекла шея", "У мене затекла шия", "I've got a stiff neck",
                "Ensem tutuldu", "Mam zesztywniały kark", "Ho il collo rigido", "Tengo el cuello rígido",
                "J'ai la nuque raide", "Mám ztuhlou šíji")}),
    6898: (LIST, {"t_ru": "обеспечить, выделить", "t_uk": "забезпечити, виділити", "t_en": "to provide, to get",
                  "t_tr": "sağlamak, temin etmek", "t_pl": "zapewnić, wygospodarować"}),
    10366: ("«Das Buch kann mich total fesseln» — так не говорят; " + LIST, {
        "t_ru": "захватывать, связывать", "t_uk": "захоплювати, зв'язувати", "t_en": "to captivate, to tie up",
        "t_tr": "büyülemek, bağlamak", "t_pl": "wciągać, związywać", "t_it": "avvincere, legare", "t_es": "atrapar, atar",
        "t_fr": "captiver, ligoter", "t_cs": "upoutat, spoutat",
        **all_x("Der Film hat mich von Anfang an gefesselt", "Фильм захватил меня с самого начала",
                "Фільм захопив мене з самого початку", "The film captivated me from the start",
                "Film beni ta baştan büyüledi", "Film wciągnął mnie od początku", "Il film mi ha avvinto fin dall'inizio",
                "La película me atrapó desde el principio", "Le film m'a captivé dès le début",
                "Film mě upoutal hned od začátku")}),
    1904: ("«Ich esse gerne Steak» — пусто", {"t_ru": "стейк", "t_uk": "стейк", "t_tr": "biftek", **all_x(
        "Wie möchten Sie Ihr Steak, medium oder durch?", "Какой прожарки вам стейк — средней или полной?",
        "Як вам підсмажити стейк — середньо чи добре?", "How would you like your steak, medium or well done?",
        "Bifteğinizi nasıl istersiniz, orta mı iyi pişmiş mi?", "Jak wysmażyć stek: średnio czy dobrze?",
        "Come vuole la bistecca, media o ben cotta?", "¿Cómo quiere el filete, al punto o bien hecho?",
        "Vous voulez votre steak à point ou bien cuit?", "Jak si přejete steak, medium, nebo propečený?")}),
    2472: (LIST, {"t_ru": "требовать", "t_uk": "вимагати", "t_en": "to demand, to challenge", "t_tr": "talep etmek, zorlamak",
                  "t_pl": "żądać, wymagać", "t_it": "esigere, pretendere", "t_cs": "požadovat, vyžadovat"}),
    13960: (LIST, {"t_ru": "выражать, выдавить", "t_uk": "висловлювати, видавити", "t_en": "to express, to squeeze out",
                   "t_tr": "ifade etmek, sıkmak", "t_pl": "wyrażać, wyciskać", "t_it": "esprimere, spremere",
                   "t_es": "expresar, exprimir", "t_fr": "exprimer, presser", "t_cs": "vyjádřit, vymačkat"}),
    10367: ("ru «воспринимаю как очень расслабляющую» — калька; " + LIST, {
        "t_ru": "чувствовать, ощущать", "t_uk": "відчувати, сприймати", "t_en": "to feel, to sense",
        "t_tr": "hissetmek, algılamak", "t_pl": "odczuwać, czuć", "t_it": "provare, sentire", "t_es": "sentir, percibir",
        "t_fr": "éprouver, ressentir", "t_cs": "cítit, pociťovat",
        **all_x("Ich empfinde nichts mehr für ihn", "Я больше ничего к нему не чувствую", "Я більше нічого до нього не відчуваю",
                "I don't feel anything for him any more", "Ona karşı artık hiçbir şey hissetmiyorum",
                "Nic już do niego nie czuję", "Non provo più niente per lui", "Ya no siento nada por él",
                "Je n'éprouve plus rien pour lui", "Už k němu nic necítím")}),
    12162: ("шаблон angeln («Wir gehen am Wochenende angeln»); " + LIST, {
        "t_ru": "ловить рыбу, рыбачить", "t_uk": "ловити рибу, рибалити", "t_en": "to fish", "t_tr": "balık tutmak",
        "t_pl": "łowić ryby",
        **all_x("Im Sommer fischen wir oft im Fluss", "Летом мы часто ловим рыбу в реке", "Улітку ми часто ловимо рибу в річці",
                "In summer we often fish in the river", "Yazın sık sık nehirde balık tutuyoruz",
                "Latem często łowimy ryby w rzece", "D'estate peschiamo spesso nel fiume",
                "En verano pescamos a menudo en el río", "L'été, on pêche souvent dans la rivière",
                "V létě často chytáme ryby v řece")}),
    13961: (LIST, {"t_ru": "повесить трубку, ставить музыку", "t_uk": "покласти слухавку, ставити музику",
                   "t_en": "to hang up, to DJ", "t_tr": "telefonu kapatmak, plak çalmak",
                   "t_pl": "odłożyć słuchawkę, puszczać muzykę"}),
    16072: ("«Der Aufstand gegen die Regierung …» — претерит, хроника; живое — «Mach keinen Aufstand!»", {
        "t_ru": "восстание, шум", "t_uk": "повстання, буча", "t_en": "uprising, fuss", "t_tr": "ayaklanma, olay çıkarma",
        "t_pl": "powstanie, awantura", "t_it": "la rivolta, il putiferio", "t_es": "la revuelta, el escándalo",
        "t_fr": "la révolte, le scandale", "t_cs": "povstání, povyk",
        **all_x("Mach doch nicht so einen Aufstand!", "Не поднимай такой шум!", "Не здіймай такої бучі!",
                "Don't make such a fuss!", "Bu kadar olay çıkarma!", "Nie rób takiej awantury!",
                "Non fare tutto questo putiferio!", "¡No montes tanto escándalo!", "Ne fais pas un tel scandale!",
                "Nedělej takový povyk!")}),
    887: (LIST, {"t_ru": "красить, намазывать", "t_uk": "фарбувати, намазувати", "t_en": "to paint, to spread",
                 "t_tr": "boyamak, sürmek", "t_pl": "malować, smarować", "t_it": "dipingere, spalmare",
                 "t_es": "pintar, untar", "t_fr": "peindre, tartiner", "t_cs": "malovat, natírat"}),
    2266: ("«Er hat mich beleidigt» — пусто", {**all_x(
        "Ich wollte dich nicht beleidigen", "Я не хотел тебя обидеть", "Я не хотів тебе образити",
        "I didn't mean to offend you", "Seni kırmak istemedim", "Nie chciałem cię urazić", "Non volevo offenderti",
        "No quería ofenderte", "Je ne voulais pas te vexer", "Nechtěl jsem tě urazit")}),
    16073: ("«Der Häuptling führte den Stamm …» — претерит, сказка", {**all_x(
        "Wer ist hier eigentlich der Häuptling?", "Кто тут вообще вождь?", "Хто тут взагалі вождь?",
        "Who's the chief around here, anyway?", "Burada şef kim ki?", "Kto tu właściwie jest wodzem?",
        "Chi è il capo qui, in realtà?", "¿Quién es aquí el jefe, en realidad?", "C'est qui le chef, ici?",
        "Kdo je tady vlastně náčelník?")}),
    6902: ("ru «очень ценно для меня» — калька", {"x_ru": "Это кольцо мне очень дорого",
                                                  "x_en": "This ring means a lot to me"}),
    6903: (LIST, {"t_ru": "чрезвычайно, огромный", "t_uk": "надзвичайно, величезний", "t_en": "extremely, enormous",
                  "t_tr": "son derece, muazzam", "t_pl": "niezwykle, ogromnie"}),
    16075: ("«Der Film handelt von …» — шаблон Psychopath", {**all_x(
        "Die Mafia kontrolliert hier alles", "Здесь всё контролирует мафия", "Тут усе контролює мафія",
        "The mafia controls everything here", "Burada her şeyi mafya kontrol ediyor", "Mafia kontroluje tu wszystko",
        "Qui la mafia controlla tutto", "Aquí la mafia lo controla todo", "Ici, c'est la mafia qui contrôle tout",
        "Mafie tady ovládá všechno")}),
    6905: ("«Die Platte vom Grill» — так не говорят; " + LIST, {
        "t_ru": "пластинка, плита", "t_uk": "платівка, плита", "t_en": "record, plate", "t_tr": "plak, levha",
        "t_pl": "płyta, blat", "t_it": "il disco, la piastra", "t_es": "el disco, la placa", "t_fr": "le disque, la plaque",
        "t_cs": "deska, plotna",
        **all_x("Hast du noch die alten Platten von deinen Eltern?", "У тебя ещё есть старые пластинки родителей?",
                "У тебе ще є старі платівки батьків?", "Have you still got your parents' old records?",
                "Annenlerin eski plakları hâlâ sende mi?", "Masz jeszcze stare płyty rodziców?",
                "Hai ancora i vecchi dischi dei tuoi?", "¿Todavía tienes los discos viejos de tus padres?",
                "Tu as encore les vieux disques de tes parents?", "Máš ještě staré desky po rodičích?")}),
    2183: ("«Die technische Anlage wurde modernisiert» — отчёт; " + LIST + " (было восемь значений)", {
        "t_ru": "установка, приложение", "t_uk": "установка, додаток", "t_en": "system, attachment",
        "t_tr": "tesis, ek dosya", "t_pl": "instalacja, załącznik", "t_it": "l'impianto, l'allegato",
        "t_es": "la instalación, el anexo", "t_fr": "l'installation, la pièce jointe", "t_cs": "zařízení, příloha",
        **all_x("Die Rechnung finden Sie in der Anlage", "Счёт вы найдёте в приложении", "Рахунок ви знайдете в додатку",
                "Please find the invoice in the attachment", "Faturayı ek dosyada bulabilirsiniz",
                "Fakturę znajdzie Pan w załączniku", "Trova la fattura in allegato", "Encontrará la factura en el anexo",
                "Vous trouverez la facture en pièce jointe", "Fakturu najdete v příloze")}),
    12555: ("«Der Arzt gab mir eine Spritze» — претерит; " + LIST, {
        "t_ru": "укол, шприц", "t_uk": "укол, шприц", "t_en": "injection, syringe", "t_tr": "iğne, şırınga",
        "t_pl": "zastrzyk, strzykawka",
        **all_x("Gleich bekommst du eine Spritze", "Сейчас тебе сделают укол", "Зараз тобі зроблять укол",
                "You're about to get an injection", "Birazdan sana iğne yapacaklar", "Zaraz dostaniesz zastrzyk",
                "Tra poco ti fanno una puntura", "Ahora te van a poner una inyección", "Tu vas avoir une piqûre",
                "Hned dostaneš injekci")}),
}

SPLIT_LATER = {
    887: ["streichen = вычёркивать (Termin streichen)"],
    2183: ["Anlage: Stereoanlage, Grünanlage, Geldanlage"],
}
