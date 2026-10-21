"""A2, блок 8: слова 281–320 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («X ist breit/dick») — так о вещи не говорят"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
FILM = "третий пример подряд про фильм (fantastisch, spannend, langweilig) — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    413: ("«Она носит брюки» — о том, что на ней сейчас, так не говорят", {
        "x_ru": "На ней синие брюки", "x_uk": "На ній сині штани", "x_en": "She's wearing blue trousers"}),
    15394: (EN, {"t_ru": "птица", "t_es": "el pájaro", "x_en": "The bird is singing in the tree"}),
    6449: (LIST, {"t_ru": "срочно, настоятельно", "t_tr": "acilen", "t_pl": "pilnie"}),
    1432: (SKEL + "; «поток» — другое слово", {
        "t_ru": "река", "t_uk": "річка", "t_en": "river", "t_tr": "nehir", "t_pl": "rzeka",
        **all_x("Wir schwimmen im Fluss", "Мы купаемся в реке", "Ми купаємося в річці", "We're swimming in the river",
                "Nehirde yüzüyoruz", "Kąpiemy się w rzece", "Facciamo il bagno nel fiume", "Nos bañamos en el río",
                "On se baigne dans la rivière", "Koupeme se v řece")}),
    2853: (LIST + "; «Störe ich?» — то, что говорят каждый день", {
        "t_ru": "мешать, беспокоить", "t_uk": "заважати, турбувати", "t_en": "to disturb, to bother",
        "t_tr": "rahatsız etmek", "t_pl": "przeszkadzać",
        **all_x("Entschuldigung, störe ich?", "Извините, я не помешаю?", "Вибачте, я не заважаю?",
                "Sorry, am I disturbing you?", "Pardon, rahatsız ediyor muyum?", "Przepraszam, nie przeszkadzam?",
                "Scusi, disturbo?", "Perdone, ¿molesto?", "Excusez-moi, je dérange?", "Promiňte, neruším?")}),
    644: (SKEL + "; " + LIST, {
        "t_ru": "природа, характер", "t_uk": "природа, вдача", "t_en": "nature", "t_tr": "doğa",
        "t_pl": "przyroda, natura",
        **all_x("Am Wochenende sind wir gern in der Natur", "По выходным мы любим бывать на природе",
                "На вихідних ми любимо бувати на природі", "At the weekend we like to get out into nature",
                "Hafta sonları doğada olmayı severiz", "W weekendy lubimy spędzać czas na łonie przyrody",
                "Nel fine settimana ci piace stare nella natura", "Los fines de semana nos gusta estar en la naturaleza",
                "Le week-end, on aime être dans la nature", "O víkendu jsme rádi v přírodě")}),
    6456: (TWO + " («правый» и «довольно, прав» — разные слова)", {
        "t_ru": "правый", "t_uk": "правий", "t_en": "right", "t_tr": "sağ", "t_pl": "prawy", "t_it": "destro",
        "t_es": "derecho", "t_fr": "droit", "t_cs": "pravý",
        "x_ru": "У меня болит правая рука", "x_uk": "У мене болить права рука"}),
    2754: (LIST, {"t_ru": "ряд, очередь", "t_uk": "ряд, черга", "t_en": "row, turn", "t_tr": "sıra",
                  "t_pl": "rząd, kolejka", "t_it": "la fila, il turno", "t_es": "la fila, el turno",
                  "t_fr": "le rang, le tour"}),
    615: ("«Morgens ist es kühl» — пусто, как nachts", {
        "t_en": "in the morning", "t_tr": "sabahları", "t_pl": "rano",
        **all_x("Ich trinke morgens immer Kaffee", "По утрам я всегда пью кофе", "Вранці я завжди п'ю каву",
                "I always have coffee in the morning", "Sabahları hep kahve içerim", "Rano zawsze piję kawę",
                "La mattina bevo sempre il caffè", "Por las mañanas siempre tomo café",
                "Le matin, je bois toujours un café", "Ráno vždycky piju kávu")}),
    884: (SKEL + "; en «We go» — так не говорят", {
        "t_ru": "пляж", "t_uk": "пляж", "t_en": "beach",
        **all_x("Wir liegen den ganzen Tag am Strand", "Мы весь день лежим на пляже", "Ми цілий день лежимо на пляжі",
                "We spend all day lying on the beach", "Bütün gün plajda yatıyoruz", "Cały dzień leżymy na plaży",
                "Stiamo tutto il giorno in spiaggia", "Nos pasamos el día tumbados en la playa",
                "On reste toute la journée à la plage", "Celý den ležíme na pláži")}),
    6461: (LIST + "; «Це триває», «Ça dure» — о будущем так не говорят", {
        "t_ru": "как минимум, хотя бы", "t_uk": "щонайменше, принаймні", "t_en": "at least", "t_tr": "en az",
        "t_pl": "co najmniej, przynajmniej", "t_it": "almeno", "t_es": "al menos, por lo menos", "t_fr": "au moins",
        "t_cs": "nejméně, alespoň",
        "x_uk": "Це займе щонайменше дві години", "x_es": "Eso tarda al menos dos horas",
        "x_fr": "Ça prend au moins deux heures", "x_cs": "To potrvá nejméně dvě hodiny"}),
    742: (LIST, {"t_ru": "радио", "t_uk": "радіо"}),
    815: ("«нелегальный» — другое слово (schwarzarbeiten); «Die Hose ist schwarz» — скелет", {
        "t_ru": "чёрный", "t_uk": "чорний", "t_en": "black", "t_tr": "siyah", "t_pl": "czarny", "t_it": "nero",
        "t_es": "negro", "t_fr": "noir", "t_cs": "černý",
        **all_x("Hast du meine schwarze Jacke gesehen?", "Ты не видел мою чёрную куртку?", "Ти не бачив мою чорну куртку?",
                "Have you seen my black jacket?", "Siyah ceketimi gördün mü?", "Widziałeś moją czarną kurtkę?",
                "Hai visto la mia giacca nera?", "¿Has visto mi chaqueta negra?", "Tu as vu ma veste noire?",
                "Neviděl jsi moji černou bundu?")}),
    2111: (LIST + "; «У меня есть желание» — калька", {
        "t_ru": "желание, просьба", "t_uk": "бажання, побажання", "t_en": "wish, request", "t_tr": "dilek, istek",
        "t_pl": "życzenie, prośba", "t_it": "il desiderio, l'augurio", "t_es": "el deseo, la petición",
        "t_fr": "le souhait, le vœu", "t_cs": "přání",
        "x_ru": "У меня одно желание", "x_uk": "У мене одне бажання", "x_en": "I have one wish"}),
    6465: ("«Der Ort ist zu fern» — по-немецки так не говорят (zu weit)", {
        "t_ru": "далеко, далёкий", "t_uk": "далеко, далекий", "t_en": "far, away", "t_tr": "uzak",
        "t_pl": "daleko, z daleka",
        **all_x("Halt dich von ihm fern!", "Держись от него подальше!", "Тримайся від нього подалі!",
                "Stay away from him!", "Ondan uzak dur!", "Trzymaj się od niego z daleka!", "Stai lontano da lui!",
                "¡Mantente lejos de él!", "Reste loin de lui!", "Drž se od něj dál!")}),
    6468: (LIST + "; «Мы должны» — калька с müssen", {
        "t_ru": "договориться, прийти к согласию", "t_uk": "домовитися, дійти згоди",
        "t_en": "to agree, to come to an agreement", "t_tr": "anlaşmak", "t_pl": "dogadać się, porozumieć się",
        "t_it": "mettersi d'accordo", "t_es": "ponerse de acuerdo", "t_fr": "se mettre d'accord", "t_cs": "dohodnout se",
        "x_ru": "Нам надо договориться", "x_uk": "Нам треба домовитися"}),
    1119: (LIST, {"t_ru": "похожий, подобный", "t_uk": "схожий, подібний", "t_en": "similar, alike",
                  "t_tr": "benzer", "t_pl": "podobny", "t_fr": "semblable, pareil"}),
    6473: ("«Was geschah gestern?» — претерит, так говорят только в книге", {
        "t_ru": "происходить, случаться", "t_uk": "відбуватися, траплятися", "t_en": "to happen, to occur",
        "t_tr": "olmak, meydana gelmek", "t_pl": "dziać się, zdarzać się", "t_es": "pasar, ocurrir",
        "t_fr": "se passer, arriver",
        **all_x("Keine Sorge, es ist nichts Schlimmes geschehen", "Не волнуйся, ничего страшного не случилось",
                "Не хвилюйся, нічого страшного не сталося", "Don't worry, nothing bad happened",
                "Merak etme, kötü bir şey olmadı", "Spokojnie, nic złego się nie stało",
                "Tranquillo, non è successo niente di grave", "Tranquilo, no ha pasado nada grave",
                "Ne t'inquiète pas, il ne s'est rien passé de grave", "Neboj, nic hrozného se nestalo")}),
    15954: (LIST, {"t_uk": "договір, контракт", "t_en": "contract, agreement", "t_tr": "sözleşme",
                   "t_it": "il contratto", "t_es": "el contrato", "t_fr": "le contrat"}),
    538: (FILM, {**all_x(
        "Mir ist langweilig", "Мне скучно", "Мені нудно", "I'm bored", "Canım sıkılıyor", "Nudzi mi się",
        "Mi annoio", "Me aburro", "Je m'ennuie", "Nudím se")}),
    36: ("«Er trägt einen … Anzug» — тот же пример, что Hose и Kleid", {**all_x(
        "Zur Hochzeit ziehe ich einen Anzug an", "На свадьбу я надену костюм", "На весілля я вдягну костюм",
        "I'll wear a suit to the wedding", "Düğüne takım elbise giyeceğim", "Na wesele założę garnitur",
        "Al matrimonio metto un completo", "Para la boda me pongo traje", "Pour le mariage, je mets un costume",
        "Na svatbu si vezmu oblek")}),
    1086: ("tr «bulundum» — книжно", {"x_ru": "Я был там два раза", "x_tr": "Oraya iki kez gittim"}),
    8759: (LIST, {"t_ru": "директор", "t_uk": "директор", "t_en": "director, head", "t_tr": "müdür",
                  "t_pl": "dyrektor", "x_en": "The director isn't in today"}),
    10157: (FILM + "; " + LIST, {
        "t_ru": "захватывающий, интересный", "t_uk": "захопливий, цікавий", "t_en": "exciting, thrilling",
        "t_tr": "heyecanlı, sürükleyici", "t_pl": "emocjonujący, wciągający", "t_it": "emozionante, avvincente",
        "t_es": "emocionante, apasionante", "t_fr": "passionnant, palpitant",
        **all_x("Das Spiel war bis zum Schluss spannend", "Матч был захватывающим до самого конца",
                "Матч був захопливим до самого кінця", "The match was exciting right to the end",
                "Maç sonuna kadar heyecanlıydı", "Mecz był emocjonujący do samego końca",
                "La partita è stata emozionante fino alla fine", "El partido fue emocionante hasta el final",
                "Le match était palpitant jusqu'à la fin", "Zápas byl napínavý až do konce")}),
    13446: (LIST, {"t_ru": "благодаря этому, из-за этого", "t_uk": "завдяки цьому, через це",
                   "t_en": "because of that, that way", "t_tr": "bu sayede, bu yüzden", "t_pl": "dzięki temu, przez to",
                   "t_it": "grazie a questo, così", "t_es": "gracias a eso, por eso", "t_fr": "grâce à cela, ainsi",
                   "t_cs": "díky tomu, kvůli tomu", "x_en": "I learned a lot from that"}),
    2610: (LIST, {"t_ru": "умный, разумный", "t_uk": "розумний, мудрий", "t_en": "clever, smart",
                  "t_tr": "akıllı, zeki", "t_pl": "mądry, sprytny", "t_it": "intelligente, saggio",
                  "t_es": "listo, inteligente", "t_fr": "intelligent, malin", "t_cs": "chytrý, moudrý"}),
    6482: (LIST + "; «чувствую себя сегодня слабым» — калька", {
        "t_ru": "слабый", "t_uk": "слабкий", "t_en": "weak", "t_tr": "güçsüz, zayıf", "t_pl": "słaby",
        "x_ru": "Сегодня я чувствую слабость", "x_uk": "Сьогодні я почуваюся слабким", "x_en": "I feel weak today",
        "x_tr": "Bugün kendimi güçsüz hissediyorum"}),
    658: ("«Berlin liegt im Norden» — неверно по сути и как у Ort/Stadt", {**all_x(
        "Ich komme aus dem Norden", "Я с севера", "Я з півночі", "I'm from the north", "Ben kuzeyliyim",
        "Jestem z północy", "Vengo dal nord", "Soy del norte", "Je viens du nord", "Jsem ze severu")}),
    280: ("«Die Form sieht richtig aus» — смысла нет", {
        "t_ru": "форма, вид", "t_uk": "форма, вигляд", "t_tr": "şekil, form", "t_pl": "forma, kształt",
        "t_it": "la forma", "t_es": "la forma", "t_cs": "tvar, forma",
        **all_x("Ich bin gerade nicht in Form", "Я сейчас не в форме", "Я зараз не у формі", "I'm out of form right now",
                "Şu an formda değilim", "Nie jestem teraz w formie", "Adesso non sono in forma",
                "Ahora no estoy en forma", "Je ne suis pas en forme en ce moment", "Teď nejsem ve formě")}),
    1003: ("«горячий» — это heiß; «Das Wasser ist warm» — скелет", {
        "t_ru": "тёплый", "t_uk": "теплий", "t_en": "warm", "t_tr": "sıcak, ılık", "t_pl": "ciepły",
        "t_es": "cálido, templado",
        **all_x("Zieh dich warm an, es ist kalt", "Оденься потеплее, холодно", "Вдягнися тепліше, холодно",
                "Wrap up warm, it's cold", "Üstüne sıcak bir şey giy, hava soğuk", "Ubierz się ciepło, jest zimno",
                "Mettiti qualcosa di caldo, fa freddo", "Ponte algo calentito, hace frío",
                "Habille-toi chaudement, il fait froid", "Obleč se teple, je zima")}),
    10163: ("«Ich erzähle dir keine Geheimnisse mehr» — неживо", {
        "t_ru": "секрет, тайна", "t_uk": "таємниця, секрет",
        **all_x("Kannst du ein Geheimnis für dich behalten?", "Умеешь хранить секреты?", "Умієш зберігати таємниці?",
                "Can you keep a secret?", "Sır tutabilir misin?", "Umiesz dochować tajemnicy?",
                "Sai mantenere un segreto?", "¿Sabes guardar un secreto?", "Tu sais garder un secret?",
                "Umíš udržet tajemství?")}),
    1329: (SKEL + "; " + LIST, {
        "t_ru": "толстый, густой", "t_uk": "товстий, густий", "t_en": "thick, fat", "t_tr": "kalın, şişman",
        "t_pl": "gruby", "t_it": "spesso, grasso", "t_es": "grueso, gordo", "t_fr": "épais, gros",
        "t_cs": "tlustý, silný",
        **all_x("Die Wände sind hier sehr dick", "Здесь очень толстые стены", "Тут дуже товсті стіни",
                "The walls are really thick here", "Buradaki duvarlar çok kalın", "Tutaj ściany są bardzo grube",
                "Qui i muri sono molto spessi", "Aquí las paredes son muy gruesas", "Ici, les murs sont très épais",
                "Tady jsou hodně silné zdi")}),
    6496: (LIST + "; cs «Copak si nevšimneš» — неестественно", {
        "t_ru": "замечать, запоминать", "t_uk": "помічати, запам'ятовувати", "t_en": "to notice, to remember",
        "t_tr": "fark etmek, aklında tutmak", "t_pl": "zauważać, zapamiętywać", "t_it": "accorgersi, ricordare",
        "t_fr": "remarquer, retenir", "t_cs": "všimnout si, zapamatovat si", "x_cs": "Nevšimneš si, že lže?"}),
    17483: (LIST, {"t_ru": "видео", "t_uk": "відео", "t_en": "video", "t_tr": "video", "t_pl": "wideo, filmik",
                   "x_it": "Guarda un po' questo video"}),
    1612: (LIST, {"t_ru": "проверять, контролировать", "t_uk": "перевіряти, контролювати",
                  "t_en": "to check, to control", "t_tr": "kontrol etmek", "t_pl": "sprawdzać, kontrolować",
                  "t_es": "revisar, comprobar", "t_cs": "kontrolovat",
                  "x_ru": "Проверь, пожалуйста, счёт"}),
    6499: ("перевод — список из восьми слов; en «on deployment» — так не говорят", {
        "t_ru": "выезд, использование", "t_uk": "виїзд, застосування", "t_en": "operation, use",
        "t_tr": "görev, kullanım", "t_pl": "akcja, użycie", "t_it": "l'intervento, l'impiego",
        "t_es": "la intervención, el uso", "t_fr": "l'intervention, l'utilisation", "t_cs": "zásah, nasazení",
        "x_ru": "Пожарные на выезде", "x_en": "The fire brigade is out on a call"}),
    1635: (LIST, {"t_ru": "искусство, умение", "t_uk": "мистецтво, вміння", "t_en": "art, skill", "t_tr": "sanat",
                  "t_pl": "sztuka", "t_it": "l'arte", "t_es": "el arte", "t_fr": "l'art", "t_cs": "umění",
                  "x_pl": "Lubię sztukę współczesną"}),
    13449: ("пример повторял trotzdem («Es regnet, aber ich gehe trotzdem»); " + LIST, {
        "t_ru": "всё же, тем не менее", "t_uk": "все ж таки, проте", "t_en": "still, nevertheless",
        "t_tr": "yine de", "t_pl": "jednak, mimo to", "t_it": "comunque, tuttavia", "t_es": "aun así, sin embargo",
        "t_fr": "quand même, pourtant", "t_cs": "přesto",
        **all_x("Er war krank, ist aber dennoch gekommen", "Он был болен, но всё же пришёл",
                "Він був хворий, але все ж таки прийшов", "He was ill, but he still came", "Hastaydı ama yine de geldi",
                "Był chory, a jednak przyszedł", "Era malato, ma è venuto comunque", "Estaba enfermo, pero aun así vino",
                "Il était malade, mais il est quand même venu", "Byl nemocný, ale přesto přišel")}),
    743: ("«Wer kann das richtig raten?» — как из викторины", {
        "t_ru": "угадывать, советовать", "t_uk": "вгадувати, радити", "t_en": "to guess, to advise",
        "t_tr": "tahmin etmek, tavsiye etmek", "t_pl": "zgadywać, radzić", "t_cs": "hádat, radit",
        **all_x("Rate mal, wen ich getroffen habe!", "Угадай, кого я встретил!", "Вгадай, кого я зустрів!",
                "Guess who I ran into!", "Tahmin et kimi gördüm!", "Zgadnij, kogo spotkałem!",
                "Indovina chi ho incontrato!", "¡Adivina a quién me he encontrado!", "Devine qui j'ai croisé!",
                "Hádej, koho jsem potkal!")}),
}

# dennoch — в речи «trotzdem»; немцу учить разговорное
REPLACE = [{"id": 13449, "by": 1972, "lang": "de",
            "why": "dennoch — письменное, в речи trotzdem"}]

SPLIT_LATER = {
    6456: ["recht = довольно (recht gut)", "Recht haben = быть правым"],
}
