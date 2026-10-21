"""A2, блок 5: слова 161–200 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"
NEAR = "пример повторял пример другого слова — у каждого свой"
DULL = "пример ни о чём → фраза из жизни"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6326: (LIST, {"t_ru": "опасный", "t_uk": "небезпечний", "t_en": "dangerous", "t_tr": "tehlikeli",
                  "t_pl": "niebezpieczny"}),
    1718: (LIST, {"t_ru": "близость, окрестности", "t_uk": "близькість, околиця", "t_en": "vicinity, closeness",
                  "t_tr": "yakınlık, civar", "t_pl": "bliskość, okolica"}),
    6329: (LIST + "; " + NEAR + " (wahr: «Das ist wahr»)", {
        "t_ru": "действительно, на самом деле", "t_uk": "справді, насправді", "t_en": "actually, really",
        "t_tr": "gerçekten, aslında", "t_pl": "rzeczywiście, faktycznie",
        **all_x("Er hat tatsächlich gewonnen!", "Он действительно выиграл!", "Він справді виграв!", "He actually won!",
                "Gerçekten kazandı!", "Naprawdę wygrał!", "Ha vinto davvero!", "¡De verdad ha ganado!",
                "Il a vraiment gagné!", "On opravdu vyhrál!")}),
    10075: (LIST, {"t_ru": "глупый", "t_uk": "дурний", "t_en": "stupid", "t_tr": "aptal", "t_pl": "głupi"}),
    263: (NEAR + " (Luft: «Mach … das Fenster auf…»)", {**all_x(
        "Mach bitte das Fenster zu, es zieht", "Закрой, пожалуйста, окно, сквозит", "Зачини, будь ласка, вікно, протяг",
        "Close the window, please, there's a draught", "Pencereyi kapat lütfen, cereyan var",
        "Zamknij, proszę, okno, jest przeciąg", "Chiudi la finestra, per favore, c'è corrente",
        "Cierra la ventana, por favor, que hay corriente", "Ferme la fenêtre, s'il te plaît, il y a un courant d'air",
        "Zavři prosím okno, táhne")}),
    10077: (LIST, {"t_ru": "странный, смешной", "t_uk": "дивний, смішний", "t_en": "strange, funny", "t_tr": "garip, tuhaf",
                   "t_pl": "dziwny, śmieszny"}),
    1312: (EN, {"x_en": "I'm against it"}),
    3047: (LIST + "; «Я достигаю своей цели» — калька", {
        "t_ru": "цель", "t_uk": "мета", "t_en": "goal, destination", "t_tr": "hedef", "t_pl": "cel",
        "t_it": "l'obiettivo, la meta", "t_es": "el objetivo, la meta", "t_fr": "le but, l'objectif",
        "x_ru": "Я достигну своей цели", "x_uk": "Я досягну своєї мети", "x_en": "I'll reach my goal"}),
    98: ("канцелярский пример «жду уведомления»; Bescheid живёт во фразе «Bescheid sagen» — дать знать", {
        "t_ru": "уведомление, ответ", "t_uk": "повідомлення, відповідь", "t_en": "notice, answer",
        "t_tr": "bildirim, yanıt", "t_pl": "odpowiedź, decyzja", "t_it": "la risposta", "t_es": "la respuesta",
        "t_fr": "la réponse, l'avis", "t_cs": "odpověď, vyrozumění",
        **all_x("Sag mir bitte Bescheid, wenn du da bist", "Дай мне знать, пожалуйста, когда придёшь",
                "Дай мені знати, будь ласка, коли прийдеш", "Let me know when you're there, please",
                "Geldiğinde lütfen bana haber ver", "Daj mi znać, proszę, jak będziesz na miejscu",
                "Fammi sapere quando arrivi, per favore", "Avísame cuando llegues, por favor",
                "Préviens-moi quand tu es là, s'il te plaît", "Dej mi prosím vědět, až tam budeš")}),
    2695: (LIST + "; " + NEAR + " (lassen: «Lass die Tür bitte offen»)", {
        "t_ru": "открытый, откровенный", "t_uk": "відкритий, відвертий", "t_en": "open, frank", "t_tr": "açık",
        "t_pl": "otwarty, szczery", "t_it": "aperto, sincero", "t_es": "abierto, sincero", "t_fr": "ouvert, franc",
        "t_cs": "otevřený, upřímný",
        **all_x("Der Supermarkt hat bis 22 Uhr offen", "Супермаркет открыт до 22 часов", "Супермаркет відкритий до 22:00",
                "The supermarket is open until 10 pm", "Süpermarket saat 22'ye kadar açık", "Supermarket jest otwarty do 22",
                "Il supermercato è aperto fino alle 22", "El supermercado está abierto hasta las 22",
                "Le supermarché est ouvert jusqu'à 22 heures", "Supermarket má otevřeno do 22 hodin")}),
    1813: (LIST, {"t_ru": "роль, значение", "t_uk": "роль, значення", "t_en": "role, part", "t_tr": "rol",
                  "t_pl": "rola"}),
    12474: ("«бодрствующий» — книжно; pl «Jestem jeszcze rozbudzony» — калька", {
        "t_ru": "не спит, проснувшийся", "t_uk": "не спить, прокинувся", "t_en": "awake", "t_tr": "uyanık",
        "t_pl": "obudzony, rozbudzony", "x_pl": "Jeszcze nie śpię"}),
    459: (LIST, {"t_ru": "холодный", "t_uk": "холодний", "t_en": "cold", "t_tr": "soğuk", "t_pl": "zimny"}),
    906: (NEAR + " (Birne, Hund — «… süß»); пометка «(coloq.)»", {
        "t_es": "dulce, mono",
        **all_x("Das Baby ist so süß!", "Малыш такой милый!", "Малюк такий милий!", "The baby is so cute!",
                "Bebek çok tatlı!", "Dziecko jest takie słodkie!", "Il bambino è così carino!", "¡El bebé es tan mono!",
                "Le bébé est trop mignon!", "To miminko je tak roztomilé!")}),
    6344: (LIST, {"t_ru": "посмотреть, осмотреть", "t_uk": "подивитися, оглянути", "t_en": "to look at, to watch",
                  "t_tr": "bakmak", "t_pl": "obejrzeć"}),
    1547: (EN, {"x_en": "Hopefully he'll come"}),
    393: (NEAR + " (bitter: «Der Kaffee ist zu …»)", {
        "t_ru": "горячий, жаркий", "t_uk": "гарячий, спекотний", "t_en": "hot", "t_tr": "sıcak", "t_pl": "gorący, upalny",
        **all_x("Heute ist es richtig heiß", "Сегодня очень жарко", "Сьогодні дуже спекотно", "It's really hot today",
                "Bugün çok sıcak", "Dziś jest naprawdę gorąco", "Oggi fa davvero caldo", "Hoy hace mucho calor",
                "Il fait vraiment chaud aujourd'hui", "Dnes je pořádné horko")}),
    6345: (LIST, {"t_ru": "глубокий", "t_uk": "глибокий", "t_en": "deep", "t_tr": "derin", "t_pl": "głęboki"}),
    954: (LIST + "; «Я обязательно должен» — калька", {
        "t_ru": "обязательно, непременно", "t_uk": "обов'язково", "t_en": "definitely, absolutely",
        "t_tr": "kesinlikle, mutlaka", "t_pl": "koniecznie", "x_ru": "Мне обязательно нужно это сделать"}),
    1318: (LIST + "; «Что в нём?» — неясно", {"t_ru": "в этом, внутри", "t_uk": "у цьому, всередині",
                                             "t_en": "in it", "x_ru": "Что там внутри?"}),
    3007: ("пример — обрывок «Auf diese Weise»", {
        "t_ru": "способ", "t_uk": "спосіб", "t_en": "way, manner", "t_tr": "şekil, tarz", "t_pl": "sposób",
        **all_x("Auf diese Weise geht es schneller", "Таким способом получится быстрее", "Таким способом буде швидше",
                "It's faster this way", "Bu şekilde daha hızlı", "W ten sposób jest szybciej",
                "In questo modo è più veloce", "De esta manera es más rápido", "De cette façon, c'est plus rapide",
                "Tímto způsobem to jde rychleji")}),
    2642: (LIST, {"t_ru": "ситуация, положение", "t_uk": "ситуація, становище", "t_en": "situation, location",
                  "t_tr": "durum, konum", "t_pl": "sytuacja, położenie"}),
    773: (NEAR + " (Bauch, Bein — «… tut weh»)", {
        "t_ru": "спина", "t_uk": "спина", "t_en": "back", "t_tr": "sırt", "t_pl": "plecy",
        **all_x("Er trägt seinen Rucksack auf dem Rücken", "Он несёт рюкзак на спине", "Він несе рюкзак на спині",
                "He's carrying his backpack on his back", "Sırt çantasını sırtında taşıyor", "Niesie plecak na plecach",
                "Porta lo zaino sulla schiena", "Lleva la mochila a la espalda", "Il porte son sac à dos sur le dos",
                "Nese batoh na zádech")}),
    10086: ("«Ты не должен лгать» — книжно", {"x_ru": "Нельзя врать", "x_uk": "Не можна брехати"}),
    15376: (EN, {"x_en": "The horse is running fast"}),
    647: (EN, {"x_en": "He's sitting next to me"}),
    13403: (EN, {"x_en": "At least it's warm here"}),
    1843: (LIST, {"t_ru": "ужасный, страшный", "t_uk": "жахливий", "t_en": "terrible, awful", "t_tr": "korkunç, berbat",
                  "t_pl": "straszny, okropny"}),
    1793: (LIST, {"t_ru": "богатый", "t_uk": "багатий", "t_en": "rich", "t_tr": "zengin", "t_pl": "bogaty",
                  "x_en": "He's very rich"}),
    1859: (NEAR + " (selbst: «Ich mache das selbst»)", {
        "t_ru": "сам", "t_uk": "сам", "t_en": "myself, yourself", "t_tr": "kendi", "t_pl": "sam",
        **all_x("Das hast du selber gesagt!", "Ты сам это сказал!", "Ти сам це сказав!", "You said it yourself!",
                "Bunu sen kendin söyledin!", "Sam to powiedziałeś!", "L'hai detto tu stesso!", "¡Lo has dicho tú mismo!",
                "C'est toi-même qui l'as dit!", "Sám jsi to řekl!")}),
    1398: (LIST, {"t_ru": "достигать, связаться", "t_uk": "досягати, зв'язатися", "t_en": "to reach, to achieve",
                  "t_tr": "ulaşmak", "t_pl": "osiągnąć, skontaktować się", "t_it": "raggiungere, contattare",
                  "t_es": "alcanzar, contactar", "t_fr": "atteindre, joindre", "t_cs": "dosáhnout, zastihnout"}),
    6364: ("uk: знак препинания — «крапка», не «точка»; пример ни о чём", {
        "t_ru": "точка, пункт", "t_uk": "точка, крапка", "t_en": "point, full stop", "t_tr": "nokta, puan",
        "t_pl": "punkt, kropka",
        **all_x("Am Ende des Satzes steht ein Punkt", "В конце предложения стоит точка", "У кінці речення стоїть крапка",
                "There's a full stop at the end of the sentence", "Cümlenin sonunda nokta var",
                "Na końcu zdania jest kropka", "Alla fine della frase c'è un punto", "Al final de la frase hay un punto",
                "À la fin de la phrase, il y a un point", "Na konci věty je tečka")}),
    482: (DULL, {**all_x("Am Sonntag gehen wir in die Kirche", "В воскресенье мы ходим в церковь",
                         "У неділю ми ходимо до церкви", "We go to church on Sundays", "Pazar günleri kiliseye gideriz",
                         "W niedzielę chodzimy do kościoła", "La domenica andiamo in chiesa",
                         "Los domingos vamos a la iglesia", "Le dimanche, on va à l'église", "V neděli chodíme do kostela")}),
}
