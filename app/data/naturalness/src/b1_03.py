"""B1, блок 3: слова 81–120 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Das ist ein Wunder», «Ich bin wütend») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    13394: ("«Komm mal rüber zu mir» — шаблон hierher («Komm mal hierher!»)", {**all_x(
        "Ich geh mal kurz rüber zum Nachbarn", "Я на минутку схожу к соседу", "Я на хвилинку зайду до сусіда",
        "I'm just popping over to the neighbour's", "Bir dakika karşı komşuya gidiyorum", "Skoczę na chwilę do sąsiada",
        "Faccio un salto dal vicino", "Voy un momento a casa del vecino", "Je passe un instant chez le voisin",
        "Skočím na chvilku k sousedovi")}),
    2797: (LIST, {"t_ru": "стрелять, забивать (гол)", "t_uk": "стріляти, забивати (гол)", "t_en": "to shoot, to score",
                  "t_tr": "ateş etmek, gol atmak", "t_pl": "strzelać", "t_it": "sparare, segnare",
                  "t_es": "disparar, marcar", "t_fr": "tirer, marquer", "t_cs": "střílet, vstřelit"}),
    609: ("«Der März ist ein Monat» — смысла нет; уровень: Monat — A1", {
        "level": "A1",
        **all_x("Ich bin seit einem Monat in Deutschland", "Я уже месяц в Германии", "Я вже місяць у Німеччині",
                "I've been in Germany for a month", "Bir aydır Almanya'dayım", "Jestem w Niemczech od miesiąca",
                "Sono in Germania da un mese", "Llevo un mes en Alemania", "Je suis en Allemagne depuis un mois",
                "Jsem v Německu už měsíc")}),
    13396: ("uk/en/pl — подлежащее не то («перш ніж піти» = «прежде чем ты уйдёшь»)", {
        "x_uk": "Подзвони мені, перш ніж я піду", "x_en": "Call me before I go", "x_pl": "Zadzwoń, zanim wyjdę"}),
    13397: ("«Во всяком случае, я участвую» — канцелярски", {
        "x_ru": "Во всяком случае, я в деле", "x_uk": "У будь-якому разі я з вами"}),
    18113: ("«Ich bleibe heute zuhause» — шаблон zu Hause («Bleib heute lieber zu Hause»)", {**all_x(
        "Am Wochenende bin ich meistens zuhause", "На выходных я обычно дома", "На вихідних я здебільшого вдома",
        "I'm usually at home at the weekend", "Hafta sonları genelde evdeyim", "W weekendy zwykle jestem w domu",
        "Nel fine settimana di solito sono a casa", "Los fines de semana suelo estar en casa",
        "Le week-end, je suis généralement à la maison", "O víkendu jsem většinou doma")}),
    10084: (LIST + "; «человек с добрым сердцем» — пояснение", {
        "t_ru": "душа", "t_uk": "душа", "t_en": "soul", "t_tr": "ruh, can", "t_pl": "dusza"}),
    18605: ("«Irgendwann kommt die Zeit» — пусто; en «Sometime the time will come» — так не говорят", {**all_x(
        "Irgendwann musst du es ihm sagen", "Когда-нибудь тебе придётся ему сказать", "Колись тобі доведеться йому сказати",
        "At some point you'll have to tell him", "Bir gün ona söylemek zorunda kalacaksın",
        "Kiedyś będziesz musiał mu powiedzieć", "Prima o poi glielo devi dire", "En algún momento tendrás que decírselo",
        "Un jour, il faudra que tu le lui dises", "Jednou mu to budeš muset říct")}),
    1832: (LIST, {"t_ru": "бить, биться", "t_uk": "бити, битися", "t_en": "to hit, to beat", "t_tr": "vurmak, atmak",
                  "t_pl": "bić, uderzać", "t_it": "battere, colpire", "t_es": "golpear, latir", "t_fr": "battre, frapper",
                  "t_cs": "bít, tlouct"}),
    13399: ("«Wir denken dasselbe» — шаблон genauso («Ich denke genauso wie du»)", {**all_x(
        "Ich nehme dasselbe wie du", "Мне то же самое, что и тебе", "Мені те саме, що й тобі",
        "I'll have the same as you", "Ben de seninle aynısını alayım", "Poproszę to samo co ty",
        "Prendo lo stesso che prendi tu", "Yo tomo lo mismo que tú", "Je prends la même chose que toi",
        "Dám si totéž co ty")}),
    1551: ("снова Kleid — у пяти слов пример про платье; " + LIST, {
        "t_ru": "красивый, симпатичный", "t_uk": "гарний, симпатичний", "t_en": "pretty", "t_tr": "güzel, hoş",
        "t_pl": "ładny, śliczny", "t_it": "carino, bello", "t_es": "bonito, mono", "t_fr": "joli", "t_cs": "hezký",
        **all_x("Deine Tochter ist echt hübsch", "Твоя дочь очень красивая", "Твоя донька дуже гарна",
                "Your daughter is really pretty", "Kızın çok güzel", "Twoja córka jest naprawdę ładna",
                "Tua figlia è proprio carina", "Tu hija es muy mona", "Ta fille est vraiment jolie",
                "Tvoje dcera je fakt hezká")}),
    17055: (EN + " («We go by boat»)", {**all_x(
        "Wir fahren mit dem Boot auf die Insel", "Мы поплывём на остров на лодке", "Ми попливемо на острів човном",
        "We're taking the boat to the island", "Adaya tekneyle gidiyoruz", "Płyniemy łódką na wyspę",
        "Andiamo sull'isola in barca", "Vamos a la isla en barca", "On va sur l'île en bateau",
        "Pojedeme na ostrov loďkou")}),
    15938: ("«Армия марширует по Берлину» — кадр из хроники", {**all_x(
        "Mein Opa war in der Armee", "Мой дедушка служил в армии", "Мій дідусь служив в армії",
        "My grandad was in the army", "Dedem orduda görev yaptı", "Mój dziadek służył w wojsku",
        "Mio nonno era nell'esercito", "Mi abuelo estuvo en el ejército", "Mon grand-père était dans l'armée",
        "Můj děda byl v armádě")}),
    3032: ("ru «Я злой» — это о характере, а не о сейчас; " + LIST, {
        "t_ru": "злой, в ярости", "t_uk": "злий, розлючений", "t_en": "angry, furious", "t_tr": "öfkeli, kızgın",
        "t_pl": "wściekły, zły",
        **all_x("Warum bist du so wütend?", "Почему ты так злишься?", "Чому ти так злишся?", "Why are you so angry?",
                "Neden bu kadar öfkelisin?", "Czemu jesteś taki wściekły?", "Perché sei così arrabbiato?",
                "¿Por qué estás tan enfadado?", "Pourquoi tu es si en colère?", "Proč jsi tak naštvaný?")}),
    6354: (SKEL, {**all_x(
        "Es ist ein Wunder, dass niemand verletzt wurde", "Чудо, что никто не пострадал", "Диво, що ніхто не постраждав",
        "It's a miracle nobody was hurt", "Kimsenin yaralanmaması bir mucize", "To cud, że nikt nie został ranny",
        "È un miracolo che nessuno si sia fatto male", "Es un milagro que nadie haya resultado herido",
        "C'est un miracle que personne n'ait été blessé", "Je zázrak, že se nikomu nic nestalo")}),
    2031: ("перевод — список из семи; " + LIST, {
        "t_ru": "связь, соединение", "t_uk": "зв'язок, з'єднання", "t_en": "connection, link", "t_tr": "bağlantı",
        "t_pl": "połączenie, łączność", "t_it": "la connessione, il collegamento", "t_es": "la conexión, la comunicación",
        "t_fr": "la connexion, la liaison", "t_cs": "spojení"}),
    6360: ("«Das Geld ist versteckt» — скелет и шаблон verstecken", {**all_x(
        "Im Garten gibt es einen versteckten Eingang", "В саду есть скрытый вход", "У саду є прихований вхід",
        "There's a hidden entrance in the garden", "Bahçede gizli bir giriş var", "W ogrodzie jest ukryte wejście",
        "In giardino c'è un ingresso nascosto", "En el jardín hay una entrada escondida",
        "Il y a une entrée cachée dans le jardin", "V zahradě je skrytý vchod")}),
    2484: ("«Ich wünsche mir Frieden» — плакат; в речи — «Lass mich in Frieden!»", {**all_x(
        "Lass mich in Frieden!", "Оставь меня в покое!", "Дай мені спокій!", "Leave me in peace!", "Beni rahat bırak!",
        "Daj mi spokój!", "Lasciami in pace!", "¡Déjame en paz!", "Laisse-moi en paix!", "Nech mě v klidu!")}),
    1525: ("«Meine Haut ist trocken» — шаблон Creme («… für trockene Haut»)", {**all_x(
        "Ich habe sehr empfindliche Haut", "У меня очень чувствительная кожа", "У мене дуже чутлива шкіра",
        "I have very sensitive skin", "Cildim çok hassas", "Mam bardzo wrażliwą skórę", "Ho la pelle molto sensibile",
        "Tengo la piel muy sensible", "J'ai la peau très sensible", "Mám velmi citlivou pleť")}),
    1495: ("«Der Ring ist aus Gold» — шаблон Kette («… aus Gold»)", {**all_x(
        "Ist das echtes Gold?", "Это настоящее золото?", "Це справжнє золото?", "Is that real gold?",
        "Bu gerçek altın mı?", "Czy to prawdziwe złoto?", "È oro vero?", "¿Es oro de verdad?",
        "C'est de l'or véritable?", "Je to pravé zlato?")}),
    12097: (EN + " («We make a bet»)", {**all_x(
        "Ich habe die Wette gewonnen", "Я выиграл пари", "Я виграв парі", "I won the bet", "Bahsi kazandım",
        "Wygrałem zakład", "Ho vinto la scommessa", "He ganado la apuesta", "J'ai gagné le pari", "Vyhrál jsem sázku")}),
    1400: ("«Ich erwarte einen Anruf» — книжно; «Wir erwarten ein Baby» — то, как слово живёт", {
        "t_ru": "ожидать, ждать", "t_uk": "очікувати, чекати", "t_en": "to expect", "t_tr": "beklemek",
        "t_pl": "oczekiwać, spodziewać się",
        **all_x("Wir erwarten ein Baby", "Мы ждём ребёнка", "Ми чекаємо дитину", "We're expecting a baby",
                "Bebek bekliyoruz", "Spodziewamy się dziecka", "Aspettiamo un bambino", "Esperamos un bebé",
                "Nous attendons un bébé", "Čekáme miminko")}),
    10092: ("«Mein Hund ist vermisst» — по-немецки так не говорят", {**all_x(
        "Seit gestern wird ein Junge vermisst", "Со вчерашнего дня пропал мальчик", "Від учора зник хлопчик",
        "A boy has been missing since yesterday", "Dünden beri bir çocuk kayıp", "Od wczoraj zaginął chłopiec",
        "Da ieri è scomparso un ragazzo", "Desde ayer hay un niño desaparecido", "Un garçon a disparu depuis hier",
        "Od včerejška se pohřešuje chlapec")}),
    642: ("«У клоуна красный нос» — из детской книжки", {**all_x(
        "Meine Nase läuft", "У меня течёт из носа", "У мене тече з носа", "My nose is running", "Burnum akıyor",
        "Leci mi z nosa", "Mi cola il naso", "Me gotea la nariz", "J'ai le nez qui coule", "Teče mi z nosu")}),
    # Ring (блок 6) — скелет «Der Ring ist sehr teuer»
    13625: ("«Der Ring ist sehr teuer» — скелет", {**all_x(
        "Er hat ihr einen Ring gekauft", "Он купил ей кольцо", "Він купив їй каблучку", "He bought her a ring",
        "Ona bir yüzük aldı", "Kupił jej pierścionek", "Le ha comprato un anello", "Le ha comprado un anillo",
        "Il lui a acheté une bague", "Koupil jí prsten")}),
}

# ehe — книжное; говорят bevor. zuhause — то же слово, что zu Hause
REPLACE = [
    {"id": 13396, "by": 108, "lang": "de", "why": "ehe — книжное, в речи bevor"},
    {"id": 18113, "by": 1079, "lang": "de", "why": "zuhause — написание того же zu Hause"},
]

SPLIT_LATER = {}
