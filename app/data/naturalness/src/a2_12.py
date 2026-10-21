"""A2, блок 12: слова 441–480 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («X ist voll/trocken») — так о вещи не говорят"
EN = "английский пример: так не говорят"
GO = "«Wir gehen ins/zum X» — тот же пример, что у Park, Theater, Strand; у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    # мой пример из блока 9 — шаблон Bauch («Mir tut der Bauch weh»), нашла новая проверка
    672: ("«Mir tut das Ohr weh» — шаблон примера Bauch (проверка шаблонов 21.10)", {**all_x(
        "Ich höre auf dem linken Ohr schlecht", "Я плохо слышу левым ухом", "Я погано чую лівим вухом",
        "I can't hear well in my left ear", "Sol kulağım iyi duymuyor", "Słabo słyszę na lewe ucho",
        "Ci sento poco dall'orecchio sinistro", "Oigo mal por el oído izquierdo", "J'entends mal de l'oreille gauche",
        "Na levé ucho slyším špatně")}),
    716: ("третий пример про поездку (träumen, Reise); fr «planifions» — канцелярски", {
        "t_ru": "планировать", "t_uk": "планувати", "t_en": "to plan", "t_tr": "planlamak", "t_pl": "planować",
        "t_it": "programmare, organizzare", "t_fr": "prévoir, organiser",
        **all_x("Was planst du fürs Wochenende?", "Что ты планируешь на выходные?", "Що плануєш на вихідні?",
                "What are you planning for the weekend?", "Hafta sonu için ne planlıyorsun?", "Co planujesz na weekend?",
                "Che cosa organizzi per il fine settimana?", "¿Qué planes tienes para el fin de semana?",
                "Qu'est-ce que tu prévois ce week-end?", "Co plánuješ na víkend?")}),
    2450: ("«Ich bin ein großer Fan» — чего? пусто", {
        "t_ru": "фанат, болельщик", "t_uk": "фанат, уболівальник", "t_en": "fan", "t_tr": "hayran, taraftar",
        "t_pl": "fan, kibic",
        **all_x("Ich bin ein großer Fan von dieser Band", "Я большой фанат этой группы", "Я великий фанат цього гурту",
                "I'm a big fan of this band", "Bu grubun büyük hayranıyım", "Jestem wielkim fanem tego zespołu",
                "Sono un grande fan di questo gruppo", "Soy muy fan de este grupo", "Je suis un grand fan de ce groupe",
                "Jsem velký fanoušek téhle kapely")}),
    6675: (LIST, {"t_ru": "высота, сумма", "t_uk": "висота, сума", "t_en": "height, amount",
                  "t_tr": "yükseklik, tutar", "t_pl": "wysokość, kwota", "t_it": "l'altezza, l'importo",
                  "t_es": "la altura, el importe", "t_fr": "la hauteur, le montant",
                  "x_ru": "На такой высоте воздух разреженный"}),
    807: ("«Ich esse gerne Schokolade» — шаблон Eis («Ich esse gern Eis»)", {
        "t_ru": "шоколад", "t_uk": "шоколад", "t_en": "chocolate",
        **all_x("Kannst du mir eine Tafel Schokolade mitbringen?", "Можешь принести мне плитку шоколада?",
                "Можеш принести мені плитку шоколаду?", "Could you bring me a bar of chocolate?",
                "Bana bir tablet çikolata getirebilir misin?", "Możesz mi przynieść tabliczkę czekolady?",
                "Mi porti una tavoletta di cioccolato?", "¿Me traes una tableta de chocolate?",
                "Tu peux me rapporter une tablette de chocolat?", "Můžeš mi přinést tabulku čokolády?")}),
    6679: ("«Справочник полезный для начинающих» — язык аннотаций; " + LIST, {
        "t_ru": "полезный", "t_uk": "корисний", "t_en": "useful", "t_tr": "faydalı, yararlı",
        "t_pl": "przydatny, pożyteczny", "t_fr": "utile", "t_cs": "užitečný",
        **all_x("Sprichst du Spanisch? Das ist im Urlaub sehr nützlich", "Ты знаешь испанский? В отпуске это очень полезно",
                "Ти знаєш іспанську? У відпустці це дуже корисно", "Do you speak Spanish? That's really useful on holiday",
                "İspanyolca biliyor musun? Tatilde çok faydalı olur", "Znasz hiszpański? Na wakacjach to bardzo przydatne",
                "Sai lo spagnolo? In vacanza è molto utile", "¿Sabes español? En vacaciones es muy útil",
                "Tu parles espagnol? En vacances, c'est très utile", "Umíš španělsky? Na dovolené je to hodně užitečné")}),
    1556: ("«Я проинформирую тебя» — канцелярски; " + LIST, {
        "t_ru": "сообщать, узнавать", "t_uk": "повідомляти, дізнаватися", "t_en": "to inform, to find out",
        "t_tr": "bilgilendirmek, bilgi almak", "t_pl": "informować, dowiadywać się", "t_it": "informare, informarsi",
        "t_es": "informar, informarse", "t_fr": "informer, se renseigner", "t_cs": "informovat, informovat se",
        **all_x("Hast du dich schon über den Kurs informiert?", "Ты уже узнал про курс?", "Ти вже дізнався про курс?",
                "Have you found out about the course yet?", "Kurs hakkında bilgi aldın mı?",
                "Dowiedziałeś się już czegoś o kursie?", "Ti sei già informato sul corso?",
                "¿Ya te has informado sobre el curso?", "Tu t'es déjà renseigné sur le cours?",
                "Už ses informoval o tom kurzu?")}),
    10260: ("uk «мороживо» — ошибка; «обещаю тебе мороженое» — неживо", {
        "t_ru": "обещать", "t_uk": "обіцяти", "t_tr": "söz vermek", "t_pl": "obiecać", "t_cs": "slíbit",
        **all_x("Versprich mir, dass du vorsichtig fährst", "Обещай мне, что будешь ехать осторожно",
                "Пообіцяй мені, що їхатимеш обережно", "Promise me you'll drive carefully",
                "Dikkatli süreceğine söz ver", "Obiecaj mi, że będziesz ostrożnie jechać",
                "Promettimi che guiderai con prudenza", "Prométeme que conducirás con cuidado",
                "Promets-moi de conduire prudemment", "Slib mi, že pojedeš opatrně")}),
    94: ("«ленивый» — другое значение; «Der Stuhl ist sehr bequem» — скелет", {
        "t_ru": "удобный", "t_uk": "зручний", "t_en": "comfortable", "t_tr": "rahat", "t_pl": "wygodny",
        **all_x("Die Schuhe sind total bequem", "Эта обувь очень удобная", "Це взуття дуже зручне",
                "These shoes are really comfortable", "Bu ayakkabılar çok rahat", "Te buty są bardzo wygodne",
                "Queste scarpe sono comodissime", "Estos zapatos son comodísimos",
                "Ces chaussures sont super confortables", "Tyhle boty jsou hrozně pohodlné")}),
    259: (LIST, {"t_ru": "праздник, вечеринка", "t_uk": "свято, вечірка", "t_tr": "kutlama, parti",
                 "t_pl": "uroczystość, impreza", "x_pl": "Impreza była super"}),
    12128: ("«Das ist mir ein Rätsel» — так слово и говорят; " + LIST, {
        "t_ru": "загадка, головоломка", "t_uk": "загадка, головоломка", "t_en": "riddle, mystery",
        "t_tr": "bilmece, gizem", "t_pl": "zagadka",
        **all_x("Das ist mir ein Rätsel", "Для меня это загадка", "Для мене це загадка", "It's a mystery to me",
                "Bu benim için bir gizem", "To dla mnie zagadka", "Per me è un enigma", "Para mí es un enigma",
                "C'est une énigme pour moi", "Je mi to záhadou")}),
    13644: (LIST + "; «Die Kette ist aus Gold» — скелет", {
        "t_ru": "цепочка, цепь", "t_uk": "ланцюжок, ланцюг", "t_en": "chain, necklace", "t_tr": "zincir, kolye",
        "t_pl": "łańcuszek, łańcuch", "t_it": "la catena, la collana", "t_es": "la cadena, el collar",
        "t_fr": "la chaîne, le collier", "t_cs": "řetěz, řetízek",
        **all_x("Die Kette hat mir meine Oma geschenkt", "Эту цепочку мне подарила бабушка",
                "Цей ланцюжок мені подарувала бабуся", "My gran gave me this necklace",
                "Bu kolyeyi bana babaannem hediye etti", "Ten łańcuszek dała mi babcia",
                "Questa collana me l'ha regalata la nonna", "Este collar me lo regaló mi abuela",
                "C'est ma grand-mère qui m'a offert ce collier", "Ten řetízek mi darovala babička")}),
    922: (SKEL, {**all_x(
        "Die Teller sind noch in der Spülmaschine", "Тарелки ещё в посудомойке", "Тарілки ще в посудомийці",
        "The plates are still in the dishwasher", "Tabaklar hâlâ bulaşık makinesinde", "Talerze są jeszcze w zmywarce",
        "I piatti sono ancora nella lavastoviglie", "Los platos todavía están en el lavavajillas",
        "Les assiettes sont encore dans le lave-vaisselle", "Talíře jsou ještě v myčce")}),
    13920: (LIST, {"t_ru": "описывать", "t_uk": "описувати", "t_en": "to describe", "t_tr": "tarif etmek, anlatmak",
                   "t_pl": "opisywać"}),
    18149: ("«Я должен сегодня постирать» — калька; " + LIST, {
        "t_ru": "бельё, стирка", "t_uk": "білизна, прання", "t_en": "laundry, washing", "t_tr": "çamaşır",
        "t_pl": "pranie, bielizna", "t_es": "la ropa, la colada",
        "x_ru": "Мне сегодня надо постирать бельё", "x_uk": "Мені сьогодні треба випрати білизну"}),
    8792: ("«Der Koch macht sehr gutes Essen» — из детской книжки", {**all_x(
        "Mein Mann ist ein super Koch", "Мой муж — отличный повар", "Мій чоловік — чудовий кухар",
        "My husband's a great cook", "Kocam harika bir aşçı", "Mój mąż jest świetnym kucharzem",
        "Mio marito è un cuoco bravissimo", "Mi marido es un cocinero estupendo", "Mon mari est un excellent cuisinier",
        "Můj manžel je skvělý kuchař")}),
    10266: ("«Это была драматическая ситуация» — язык новостей; " + LIST, {
        "t_ru": "драматичный, резкий", "t_uk": "драматичний, різкий", "t_en": "dramatic", "t_tr": "dramatik",
        "t_pl": "dramatyczny",
        **all_x("Sei nicht so dramatisch!", "Не драматизируй!", "Не драматизуй!", "Don't be so dramatic!",
                "Bu kadar dramatik olma!", "Nie dramatyzuj!", "Non drammatizzare!", "¡No te pongas tan dramático!",
                "Ne dramatise pas!", "Nedělej z toho takové drama!")}),
    6696: (LIST, {"t_ru": "мягкий, нежный", "t_uk": "м'який, ніжний", "t_en": "soft, tender", "t_tr": "yumuşak",
                  "t_pl": "miękki, delikatny", "t_es": "blando, suave", "t_fr": "mou, doux"}),
    6697: ("«Das ist wirklich notwendig» — пусто; вопрос — то, как слово говорят", {
        "t_ru": "необходимый, нужный", "t_uk": "необхідний, потрібний", "t_en": "necessary", "t_tr": "gerekli",
        "t_pl": "konieczny, potrzebny",
        **all_x("Ist das wirklich notwendig?", "Это правда так необходимо?", "Це справді так необхідно?",
                "Is that really necessary?", "Bu gerçekten gerekli mi?", "Czy to naprawdę konieczne?",
                "È proprio necessario?", "¿De verdad es necesario?", "C'est vraiment nécessaire?",
                "Je to opravdu nutné?")}),
    16017: (LIST, {"t_ru": "община, муниципалитет", "t_uk": "громада, муніципалітет",
                   "t_en": "community, municipality", "t_tr": "belediye, topluluk", "t_pl": "gmina, wspólnota",
                   "t_it": "il comune, la comunità", "t_es": "el municipio, la comunidad",
                   "t_fr": "la commune, la communauté", "t_cs": "obec, komunita"}),
    18667: (LIST + "; «мы должны понять» — калька с müssen", {
        "t_ru": "сначала, пока что", "t_uk": "спочатку, поки що", "t_en": "first, for now", "t_tr": "önce, şimdilik",
        "t_pl": "najpierw, na razie", "t_it": "prima, per ora", "t_es": "primero, de momento",
        "t_fr": "d'abord, pour l'instant", "t_cs": "nejprve, zatím",
        "x_ru": "Сначала нам надо понять, в чём проблема", "x_uk": "Спочатку нам треба зрозуміти, у чому проблема"}),
    1828: (LIST, {"t_ru": "толкать, двигать", "t_uk": "штовхати, пересувати", "t_en": "to push", "t_tr": "itmek",
                  "t_pl": "pchać, przesuwać", "x_uk": "Штовхни-но візок"}),
    192: ("шаблон zweimal («Ich war zweimal dort»)", {"t_en": "three times", **all_x(
        "Ich habe dich dreimal angerufen!", "Я тебе три раза звонил!", "Я тобі тричі дзвонив!",
        "I called you three times!", "Seni üç kez aradım!", "Dzwoniłem do ciebie trzy razy!",
        "Ti ho chiamato tre volte!", "¡Te he llamado tres veces!", "Je t'ai appelé trois fois!",
        "Volal jsem ti třikrát!")}),
    112: (GO, {**all_x(
        "Ich muss die Bücher in die Bibliothek zurückbringen", "Мне надо вернуть книги в библиотеку",
        "Мені треба повернути книжки до бібліотеки", "I need to take the books back to the library",
        "Kitapları kütüphaneye geri götürmem lazım", "Muszę oddać książki do biblioteki",
        "Devo riportare i libri in biblioteca", "Tengo que devolver los libros a la biblioteca",
        "Je dois rendre les livres à la bibliothèque", "Musím vrátit knihy do knihovny")}),
    6715: (EN + " («typical for Germany»)", {"t_tr": "tipik", "x_en": "That's typical of Germany"}),
    1651: (LIST, {"t_ru": "одалживать, брать взаймы", "t_uk": "позичати", "t_en": "to lend, to borrow",
                  "t_tr": "ödünç vermek", "t_pl": "pożyczać"}),
    960: ("«Я учусь в университете» — почти перевод самого слова", {**all_x(
        "Nach der Schule will ich an die Universität", "После школы я хочу поступить в университет",
        "Після школи я хочу вступити до університету", "After school I want to go to university",
        "Liseden sonra üniversiteye gitmek istiyorum", "Po szkole chcę iść na uniwersytet",
        "Dopo la scuola voglio andare all'università", "Después del instituto quiero ir a la universidad",
        "Après le lycée, je veux aller à l'université", "Po škole chci jít na univerzitu")}),
    929: ("«Danke für den Tipp!» — так слово и живёт; " + LIST, {
        "t_en": "tip, hint", "t_tr": "ipucu, tavsiye", "t_pl": "rada, wskazówka",
        **all_x("Danke für den Tipp!", "Спасибо за совет!", "Дякую за пораду!", "Thanks for the tip!",
                "Tavsiye için teşekkürler!", "Dzięki za radę!", "Grazie del consiglio!", "¡Gracias por el consejo!",
                "Merci pour le tuyau!", "Díky za tip!")}),
    242: ("tr «Bu yirmi euro» — без глагола цены", {"x_tr": "Bu yirmi euro tutuyor"}),
    18670: (LIST, {"t_ru": "будить, разбудить", "t_uk": "будити, розбудити", "t_en": "to wake (someone) up",
                   "t_tr": "uyandırmak", "t_pl": "budzić, obudzić"}),
    1914: ("«Ich trage Stiefel» — шаблон одежды; " + LIST, {
        "t_ru": "сапог", "t_uk": "чобіт", "t_en": "boot", "t_tr": "çizme, bot", "t_pl": "kozak, but",
        **all_x("Im Winter brauche ich warme Stiefel", "Зимой мне нужны тёплые сапоги", "Взимку мені потрібні теплі чоботи",
                "I need warm boots in winter", "Kışın sıcak botlara ihtiyacım var", "Zimą potrzebuję ciepłych kozaków",
                "D'inverno mi servono stivali caldi", "En invierno necesito botas calentitas",
                "En hiver, j'ai besoin de bottes chaudes", "V zimě potřebuju teplé vysoké boty")}),
    6726: ("it — длинно", {"x_it": "Non trovo le chiavi da nessuna parte"}),
    14413: (GO, {**all_x(
        "Montags ist das Museum geschlossen", "По понедельникам музей закрыт", "По понеділках музей зачинений",
        "The museum is closed on Mondays", "Müze pazartesileri kapalı", "W poniedziałki muzeum jest zamknięte",
        "Il lunedì il museo è chiuso", "Los lunes el museo está cerrado", "Le musée est fermé le lundi",
        "V pondělí je muzeum zavřené")}),
    12529: ("ru «Мне нужно быстро принять душ» — книжно", {"x_ru": "Мне ещё надо быстренько принять душ"}),
    943: (SKEL + "; " + LIST, {
        "t_ru": "сухой", "t_uk": "сухий", "t_en": "dry", "t_tr": "kuru", "t_pl": "suchy", "t_it": "secco, asciutto",
        **all_x("Die Wäsche ist schon trocken", "Бельё уже сухое", "Білизна вже суха", "The washing's already dry",
                "Çamaşırlar kurumuş bile", "Pranie już wyschło", "Il bucato è già asciutto", "La ropa ya está seca",
                "Le linge est déjà sec", "Prádlo už je suché")}),
    9460: ("«У тебя есть для меня ручка?» — калька; " + LIST, {
        "t_ru": "ручка, карандаш", "t_uk": "ручка, олівець", "t_en": "pen, pencil", "t_tr": "kalem",
        "t_pl": "długopis, ołówek",
        **all_x("Hast du mal einen Stift?", "У тебя не найдётся ручки?", "У тебе не знайдеться ручки?",
                "Have you got a pen?", "Kalemin var mı?", "Masz może długopis?", "Hai una penna?",
                "¿Tienes un bolígrafo?", "Tu as un stylo?", "Nemáš propisku?")}),
    1228: ("uk/tr — без «тебе»", {"t_ru": "благодарить", "t_uk": "дякувати", "t_en": "to thank", "t_pl": "dziękować",
                                  "x_uk": "Я хочу тобі подякувати", "x_tr": "Sana teşekkür etmek istiyorum"}),
    503: (GO + "; en «We go to a concert»", {**all_x(
        "Kommst du mit ins Konzert? Ich habe zwei Karten", "Пойдёшь со мной на концерт? У меня два билета",
        "Підеш зі мною на концерт? У мене два квитки", "Fancy coming to the concert? I've got two tickets",
        "Benimle konsere gelir misin? İki biletim var", "Pójdziesz ze mną na koncert? Mam dwa bilety",
        "Vieni con me al concerto? Ho due biglietti", "¿Vienes conmigo al concierto? Tengo dos entradas",
        "Tu viens au concert avec moi? J'ai deux billets", "Půjdeš se mnou na koncert? Mám dva lístky")}),
    2800: ("«Die Wäsche ist schmutzig» — скелет и шаблон Wäsche/trocken; «нечестный» — другое значение", {
        "t_ru": "грязный", "t_uk": "брудний", "t_en": "dirty", "t_tr": "kirli, pis", "t_pl": "brudny",
        **all_x("Deine Schuhe sind ganz schmutzig", "У тебя ботинки совсем грязные", "У тебе черевики зовсім брудні",
                "Your shoes are filthy", "Ayakkabıların çok kirli", "Masz strasznie brudne buty",
                "Hai le scarpe tutte sporche", "Tienes los zapatos muy sucios", "Tes chaussures sont toutes sales",
                "Máš úplně špinavé boty")}),
}

SPLIT_LATER = {}
