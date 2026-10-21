"""B1, блок 1: слова 1–40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Papa arbeitet», «Die Erde ist rund») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    10022: (LIST, {"t_ru": "жаль, надоело", "t_uk": "шкода, набридло", "t_en": "sorry, fed up", "t_tr": "üzgün, bıkmış",
                   "t_pl": "przykro, mieć dość", "t_it": "mi dispiace", "t_es": "lo siento"}),
    13309: (LIST, {"t_ru": "другой, остальной", "t_uk": "інший, решта", "t_en": "other, different", "t_tr": "başka, diğer",
                   "t_pl": "inny, pozostały", "x_en": "The others are already here"}),
    13817: (LIST, {"t_ru": "чёрт, проклятый", "t_uk": "чорт, проклятий", "t_en": "damn, damned",
                   "t_tr": "lanet olsun, kahretsin", "t_pl": "cholera, przeklęty"}),
    13821: (LIST + "; «Что ты, собственно, делаешь?» — книжно", {
        "t_ru": "вообще-то, на самом деле", "t_uk": "взагалі-то, насправді", "t_en": "actually, really",
        "t_tr": "aslında", "t_pl": "właściwie, tak naprawdę", "t_it": "in realtà, veramente",
        "t_es": "en realidad, realmente", "t_fr": "en fait, au fond", "t_cs": "vlastně",
        "x_ru": "Что ты вообще делаешь?", "x_uk": "Що ти взагалі робиш?"}),
    6226: ("«Убивать муху — нехорошо» — так не говорят", {**all_x(
        "Ich könnte ihn töten!", "Я бы его убил!", "Я б його вбив!", "I could kill him!", "Onu öldürebilirim!",
        "Mógłbym go zabić!", "Lo ammazzerei!", "¡Lo mataría!", "Je pourrais le tuer!", "Já bych ho zabil!")}),
    13340: (LIST, {"t_ru": "на очереди, моя очередь", "t_uk": "на черзі", "t_en": "one's turn", "t_tr": "sıra (bende)",
                   "t_pl": "kolej (na kogoś)", "t_it": "toccare a", "t_es": "tocar a", "t_fr": "c'est à (qqn)",
                   "t_cs": "na řadě"}),
    2049: ("«Das ist ja verrückt» — шаблон irre («Das ist ja irre»); " + LIST, {
        "t_ru": "сумасшедший, безумный", "t_uk": "божевільний, шалений", "t_en": "crazy, mad", "t_tr": "çılgın, deli",
        "t_pl": "szalony, zwariowany",
        **all_x("Bist du verrückt geworden?", "Ты с ума сошёл?", "Ти що, збожеволів?", "Have you gone crazy?",
                "Çıldırdın mı?", "Zwariowałeś?", "Sei impazzito?", "¿Te has vuelto loco?", "Tu es devenu fou?",
                "Zbláznil ses?")}),
    10035: ("en «What the devil» — устар.; tr «şeytan mı dürttü» — другой смысл", {
        "x_en": "What the hell are you doing there?", "x_tr": "Orada ne halt ediyorsun?"}),
    14895: ("«Der Kerl ist nett» / «Парень милый» — неживо", {**all_x(
        "Er ist ein netter Kerl", "Он хороший парень", "Він хороший хлопець", "He's a nice guy", "İyi bir adam",
        "To fajny facet", "È un tipo simpatico", "Es un buen tipo", "C'est un type sympa", "Je to fajn chlap")}),
    14896: ("«Mama kocht das Essen» — из букваря", {"t_en": "mum, mom", **all_x(
        "Mama, wo sind meine Socken?", "Мам, где мои носки?", "Мамо, де мої шкарпетки?", "Mum, where are my socks?",
        "Anne, çoraplarım nerede?", "Mamo, gdzie są moje skarpetki?", "Mamma, dove sono i miei calzini?",
        "Mamá, ¿dónde están mis calcetines?", "Maman, où sont mes chaussettes?", "Mami, kde mám ponožky?")}),
    786: ("«Ты моё сокровище» — так зовут, а не говорят; " + LIST, {
        "t_ru": "сокровище, милый", "t_uk": "скарб, коханий", "t_en": "treasure, darling", "t_tr": "hazine, canım",
        "t_pl": "skarb, kochanie",
        **all_x("Schatz, kannst du mir helfen?", "Милый, можешь мне помочь?", "Коханий, можеш мені допомогти?",
                "Darling, can you help me?", "Canım, bana yardım edebilir misin?", "Kochanie, możesz mi pomóc?",
                "Amore, mi puoi aiutare?", "Cariño, ¿me puedes ayudar?", "Chéri, tu peux m'aider?",
                "Miláčku, můžeš mi pomoct?")}),
    10040: ("«Das ist die Wahrheit» — пусто", {**all_x(
        "Sag mir die Wahrheit!", "Скажи мне правду!", "Скажи мені правду!", "Tell me the truth!", "Bana gerçeği söyle!",
        "Powiedz mi prawdę!", "Dimmi la verità!", "¡Dime la verdad!", "Dis-moi la vérité!", "Řekni mi pravdu!")}),
    10041: ("«не осмеливаюсь на это» — книжно; " + LIST, {
        "t_ru": "осмелиться, решиться", "t_uk": "наважитися, ризикнути", "t_en": "to dare",
        "t_tr": "cesaret etmek, göze almak", "t_pl": "odważyć się",
        "x_ru": "Я просто не решаюсь", "x_uk": "Я просто не наважуюся", "x_en": "I just don't dare"}),
    2948: ("«Ich verlasse die Stadt» — пусто; «полагаться» — это sich verlassen auf", {
        "t_ru": "покидать, оставлять", "t_uk": "покидати, залишати", "t_en": "to leave, to abandon",
        "t_tr": "terk etmek, ayrılmak", "t_pl": "opuszczać, zostawiać",
        **all_x("Sie hat ihn nach zehn Jahren verlassen", "Она ушла от него через десять лет",
                "Вона залишила його через десять років", "She left him after ten years", "On yıl sonra onu terk etti",
                "Zostawiła go po dziesięciu latach", "L'ha lasciato dopo dieci anni", "Lo dejó después de diez años",
                "Elle l'a quitté après dix ans", "Po deseti letech ho opustila")}),
    2307: ("«голый» — другое значение (bloße Hände); " + LIST, {
        "t_ru": "только, просто", "t_uk": "лише, просто", "t_en": "just, only", "t_tr": "sadece", "t_pl": "tylko, po prostu",
        "t_it": "solo, semplicemente", "t_es": "solo, simplemente", "t_fr": "juste, seulement", "t_cs": "jen, prostě"}),
    12464: ("«Da ist Blut an der Hand» — сцена из детектива", {**all_x(
        "Beim Arzt nehmen sie mir morgen Blut ab", "Завтра у врача у меня возьмут кровь",
        "Завтра в лікаря в мене візьмуть кров", "They're taking blood at the doctor's tomorrow",
        "Yarın doktorda kanımı alacaklar", "Jutro u lekarza pobiorą mi krew",
        "Domani dal medico mi fanno il prelievo di sangue", "Mañana me sacan sangre en el médico",
        "Demain, on me fait une prise de sang chez le médecin", "Zítra mi u doktora vezmou krev")}),
    2828: (LIST, {"t_ru": "беспокойство, забота", "t_uk": "занепокоєння, турбота", "t_en": "worry, care",
                  "t_tr": "endişe, kaygı", "t_pl": "zmartwienie, troska", "t_it": "la preoccupazione",
                  "t_es": "la preocupación", "t_fr": "le souci", "t_cs": "starost, obava"}),
    10048: ("«Sei ehrlich zu mir» — повтор Wahrheit; живёт слово в «ehrlich gesagt»", {
        "t_ru": "честный, искренний", "t_uk": "чесний, щирий", "t_en": "honest", "t_tr": "dürüst, samimi",
        "t_pl": "szczery, uczciwy",
        **all_x("Ehrlich gesagt habe ich keine Lust", "Честно говоря, мне не хочется", "Чесно кажучи, мені не хочеться",
                "To be honest, I don't feel like it", "Dürüst olmak gerekirse canım istemiyor",
                "Szczerze mówiąc, nie mam ochoty", "Sinceramente non ne ho voglia", "Sinceramente, no me apetece",
                "Honnêtement, je n'ai pas envie", "Upřímně řečeno se mi nechce")}),
    694: (SKEL + "; " + LIST, {
        "t_ru": "папа", "t_uk": "тато", "t_en": "dad", "t_tr": "baba", "t_pl": "tata",
        **all_x("Papa holt uns heute von der Schule ab", "Сегодня папа заберёт нас из школы", "Сьогодні тато забере нас зі школи",
                "Dad's picking us up from school today", "Bugün babam bizi okuldan alacak", "Dziś tata odbierze nas ze szkoły",
                "Oggi papà ci viene a prendere a scuola", "Hoy papá nos recoge del colegio",
                "Aujourd'hui, papa vient nous chercher à l'école", "Dneska nás táta vyzvedne ze školy")}),
    6274: ("«Wie bist du hierher gekommen?» — почти слово в слово пример herkommen", {**all_x(
        "Komm mal hierher!", "Иди-ка сюда!", "Іди-но сюди!", "Come over here!", "Buraya gel!", "Chodź tutaj!",
        "Vieni qua!", "¡Ven aquí!", "Viens ici!", "Pojď sem!")}),
    2767: ("«Ich rette das Kind» — неживо", {**all_x(
        "Du hast mir das Leben gerettet!", "Ты спас мне жизнь!", "Ти врятував мені життя!", "You saved my life!",
        "Hayatımı kurtardın!", "Uratowałeś mi życie!", "Mi hai salvato la vita!", "¡Me has salvado la vida!",
        "Tu m'as sauvé la vie!", "Zachránil jsi mi život!")}),
    10051: ("«Das ist die Hölle» — пусто", {**all_x(
        "Im Büro ist heute die Hölle los", "В офисе сегодня сущий ад", "В офісі сьогодні справжнє пекло",
        "It's hell at the office today", "Bugün ofis cehennem gibi", "W biurze jest dziś piekło",
        "Oggi in ufficio è un inferno", "Hoy en la oficina es un infierno", "Aujourd'hui, c'est l'enfer au bureau",
        "V kanceláři je dnes peklo")}),
    1630: ("«Das ist mein Kumpel» — пусто", {**all_x(
        "Ich gehe mit meinen Kumpels Fußball spielen", "Я иду играть в футбол с приятелями",
        "Я йду грати у футбол із приятелями", "I'm going to play football with my mates",
        "Arkadaşlarımla futbol oynamaya gidiyorum", "Idę grać w piłkę z kumplami", "Vado a giocare a calcio con gli amici",
        "Voy a jugar al fútbol con los colegas", "Je vais jouer au foot avec mes potes", "Jdu hrát fotbal s kámoši")}),
    1566: (EN, {"x_uk": "Книжка десь валяється", "x_en": "The book's lying around somewhere"}),
    2418: ("«Die Erde ist rund» — школьный факт; " + LIST, {
        "t_ru": "земля, почва", "t_uk": "земля, ґрунт", "t_en": "earth, soil", "t_tr": "dünya, toprak",
        "t_pl": "ziemia, gleba",
        **all_x("Die Pflanze braucht frische Erde", "Растению нужна свежая земля", "Рослині потрібна свіжа земля",
                "The plant needs fresh soil", "Bitkinin taze toprağa ihtiyacı var", "Roślina potrzebuje świeżej ziemi",
                "La pianta ha bisogno di terra fresca", "La planta necesita tierra nueva",
                "La plante a besoin de terre fraîche", "Rostlina potřebuje novou půdu")}),
    10060: (LIST, {"t_ru": "чёрт, ерунда", "t_uk": "чорт, дурниця", "t_en": "damn, rubbish", "t_tr": "lanet, saçmalık",
                   "t_pl": "cholera, bzdura", "t_it": "accidenti, la schifezza", "t_es": "vaya, la porquería",
                   "t_fr": "zut, la cochonnerie", "t_cs": "sakra, nesmysl"}),
}

SPLIT_LATER = {}
