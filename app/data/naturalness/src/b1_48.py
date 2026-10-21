"""B1, блок 48: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1640: ("«Mein Laptop ist neu» — пусто", {**all_x(
        "Mein Laptop ist schon wieder abgestürzt", "У меня опять завис ноутбук", "У мене знову завис ноутбук",
        "My laptop has crashed again", "Laptopum yine çöktü", "Mój laptop znowu się zawiesił",
        "Il mio portatile si è bloccato di nuovo", "Se me ha vuelto a colgar el portátil",
        "Mon ordinateur portable a encore planté", "Notebook mi zase spadl")}),
    15488: ("«Die Spinne spinnt ihr Netz» — масло масляное; в речи spinnen — «сходить с ума»", {
        "t_ru": "сходить с ума, прясть", "t_uk": "бути несповна розуму, прясти", "t_en": "to be crazy, to spin",
        "t_tr": "kafayı yemek, eğirmek", "t_pl": "mieć nierówno pod sufitem, prząść", "t_it": "essere matto, filare",
        "t_es": "estar loco, hilar", "t_fr": "être fou, filer", "t_cs": "bláznit, příst",
        **all_x("Du spinnst wohl!", "Ты что, с ума сошёл?", "Ти що, несповна розуму?", "Are you crazy?",
                "Kafayı mı yedin?", "Masz nierówno pod sufitem?", "Ma sei matto?", "¿Estás loco?", "T'es fou ou quoi?",
                "Blázníš?")}),
    12579: ("«Er verlor das Gleichgewicht und fiel hin» — претерит", {**all_x(
        "Halt dich fest, sonst verlierst du das Gleichgewicht", "Держись, а то потеряешь равновесие",
        "Тримайся, бо втратиш рівновагу", "Hold on or you'll lose your balance", "Sıkı tutun, yoksa dengeni kaybedersin",
        "Trzymaj się, bo stracisz równowagę", "Tieniti, sennò perdi l'equilibrio",
        "Agárrate, que si no pierdes el equilibrio", "Tiens-toi, sinon tu vas perdre l'équilibre",
        "Drž se, jinak ztratíš rovnováhu")}),
    10427: ("«Sie zeigte ihre Dankbarkeit …» — претерит", {**all_x(
        "Ich weiß nicht, wie ich meine Dankbarkeit zeigen soll", "Не знаю, как выразить свою благодарность",
        "Не знаю, як висловити свою вдячність", "I don't know how to show my gratitude",
        "Minnettarlığımı nasıl göstereceğimi bilmiyorum", "Nie wiem, jak okazać swoją wdzięczność",
        "Non so come mostrare la mia gratitudine", "No sé cómo mostrar mi gratitud",
        "Je ne sais pas comment montrer ma gratitude", "Nevím, jak vyjádřit svou vděčnost")}),
    16123: ("«Die Hinrichtung war ein schreckliches Ereignis» — претерит, пусто", {**all_x(
        "In vielen Ländern gibt es noch Hinrichtungen", "Во многих странах до сих пор есть казни",
        "У багатьох країнах досі є страти", "Executions still take place in many countries", "Birçok ülkede hâlâ idam var",
        "W wielu krajach wciąż wykonuje się egzekucje", "In molti paesi ci sono ancora esecuzioni",
        "En muchos países todavía hay ejecuciones", "Dans beaucoup de pays, il y a encore des exécutions",
        "V mnoha zemích se stále vykonávají popravy")}),
    7018: (LIST, {"t_ru": "неправильный, наизнанку", "t_uk": "неправильний, навиворіт", "t_en": "wrong, inside out",
                  "t_tr": "yanlış, ters", "t_pl": "zły, na lewą stronę", "t_it": "sbagliato, al rovescio",
                  "t_es": "equivocado, al revés", "t_fr": "mauvais, à l'envers", "t_cs": "špatný, naruby",
                  **all_x("Du hast den Pulli verkehrt herum an", "Ты надел свитер наизнанку", "Ти вдягнув светр навиворіт",
                          "You've got your jumper on inside out", "Kazağını ters giymişsin",
                          "Masz sweter założony na lewą stronę", "Hai la maglia al rovescio", "Llevas el jersey al revés",
                          "Tu as mis ton pull à l'envers", "Máš svetr naruby")}),
    1104: (LIST + " (было шесть значений)", {
        "t_ru": "сдавать (экзамен), снимать", "t_uk": "складати (іспит), знімати", "t_en": "to take (an exam), to take off",
        "t_tr": "sınava girmek, çıkarmak", "t_pl": "zdawać (egzamin), zdjąć", "t_it": "sostenere (un esame), togliersi",
        "t_es": "presentarse a (un examen), quitarse", "t_fr": "passer (un examen), enlever",
        "t_cs": "složit (zkoušku), sundat si"}),
    10429: ("«Das war nur eine Illusion, keine Realität» — масло масляное", {**all_x(
        "Mach dir keine Illusionen", "Не питай иллюзий", "Не плекай ілюзій", "Don't have any illusions",
        "Boş hayallere kapılma", "Nie rób sobie złudzeń", "Non farti illusioni", "No te hagas ilusiones",
        "Ne te fais pas d'illusions", "Nedělej si iluze")}),
    7021: ("ru «Это не должно от меня ускользнуть» — калька; живое — «Das lasse ich mir nicht entgehen»", {
        "t_ru": "упустить, ускользнуть", "t_uk": "пропустити, уникнути", "t_en": "to miss out on, to escape",
        "t_tr": "kaçırmak, gözden kaçmak", "t_pl": "umknąć, uniknąć",
        **all_x("Das lasse ich mir nicht entgehen!", "Такое я не упущу!", "Я цього не пропущу!",
                "I'm not going to miss out on that!", "Bunu kaçırmam!", "Nie pozwolę, żeby mi to umknęło!",
                "Non me lo perdo!", "¡No me lo pierdo!", "Je ne vais pas rater ça!", "To si nenechám ujít!")}),
    16125: ("«Das Verhör dauerte drei Stunden» — претерит", {**all_x(
        "Er wird gerade zum Verhör gebracht", "Его сейчас ведут на допрос", "Його зараз ведуть на допит",
        "He's being taken for questioning", "Şu an sorguya götürülüyor", "Właśnie prowadzą go na przesłuchanie",
        "Lo stanno portando all'interrogatorio", "Lo están llevando al interrogatorio", "On l'emmène à l'interrogatoire",
        "Právě ho vedou k výslechu")}),
    17937: ("«Der Weltraum ist unendlich groß» — учебник", {**all_x(
        "Ich würde gern mal in den Weltraum fliegen", "Я бы хотел когда-нибудь полететь в космос",
        "Я б хотів колись полетіти в космос", "I'd love to fly into space one day", "Bir gün uzaya gitmek isterdim",
        "Chciałbym kiedyś polecieć w kosmos", "Mi piacerebbe volare nello spazio un giorno",
        "Me gustaría volar al espacio algún día", "J'aimerais aller dans l'espace un jour",
        "Jednou bych rád letěl do vesmíru")}),
    7026: ("«Der Hund knurrt, wenn er wütend ist» — учебник; живое — «Mir knurrt der Magen»", {**all_x(
        "Mir knurrt der Magen", "У меня бурчит в животе", "У мене бурчить у животі", "My stomach is rumbling",
        "Midem guruldıyor", "Burczy mi w brzuchu", "Mi brontola lo stomaco", "Me gruñen las tripas",
        "J'ai le ventre qui gronde", "Kručí mi v břiše")}),
    10432: ("ru «Я должен преодолеть» — калька", {"x_ru": "Мне надо преодолеть свой страх",
                                                 "x_uk": "Мені треба подолати свій страх"}),
    1668: ("«Sie trägt Make-up» — шаблон одежды", {"t_en": "make-up", **all_x(
        "Ohne Make-up gehe ich nicht aus dem Haus", "Без макияжа я из дома не выхожу", "Без макіяжу я з дому не виходжу",
        "I don't leave the house without make-up", "Makyajsız evden çıkmam", "Bez makijażu nie wychodzę z domu",
        "Senza trucco non esco di casa", "Sin maquillaje no salgo de casa", "Je ne sors pas sans maquillage",
        "Bez make-upu nevycházím z domu")}),
    16126: ("шаблон Diebstahl («… bei der Polizei anzeigen»); " + LIST, {
        "t_ru": "показывать, заявить в полицию", "t_uk": "показувати, заявити в поліцію", "t_en": "to show, to report to the police",
        "t_tr": "göstermek, polise şikâyet etmek", "t_pl": "pokazywać, zgłosić na policję", "t_it": "indicare, denunciare",
        "t_es": "indicar, denunciar", "t_fr": "afficher, porter plainte", "t_cs": "ukazovat, nahlásit",
        **all_x("Das Handy zeigt keinen Empfang an", "Телефон не показывает сигнал", "Телефон не показує сигналу",
                "The phone isn't showing any signal", "Telefon çekim göstermiyor", "Telefon nie pokazuje zasięgu",
                "Il telefono non indica campo", "El móvil no indica cobertura", "Le téléphone n'affiche pas de réseau",
                "Mobil neukazuje signál")}),
    2980: ("ru «Судья его осуждает» — не тот смысл", {**all_x(
        "Er ist zu drei Jahren Haft verurteilt worden", "Его приговорили к трём годам тюрьмы", "Його засудили до трьох років в'язниці",
        "He was sentenced to three years in prison", "Üç yıl hapse mahkûm edildi", "Został skazany na trzy lata więzienia",
        "È stato condannato a tre anni di carcere", "Lo condenaron a tres años de cárcel",
        "Il a été condamné à trois ans de prison", "Byl odsouzen ke třem letům vězení")}),
    560: ("«Ein Liter Milch» — обрывок", {"t_en": "litre", **all_x(
        "Ich trinke jeden Tag zwei Liter Wasser", "Я каждый день пью два литра воды", "Я щодня п'ю два літри води",
        "I drink two litres of water every day", "Her gün iki litre su içiyorum", "Codziennie piję dwa litry wody",
        "Bevo due litri d'acqua al giorno", "Bebo dos litros de agua al día", "Je bois deux litres d'eau par jour",
        "Každý den piju dva litry vody")}),
    13988: ("«ans Problem rangehen» — так не говорят; " + LIST, {
        "t_ru": "взяться за дело, ответить на звонок", "t_uk": "взятися до справи, відповісти на дзвінок",
        "t_en": "to tackle, to answer the phone", "t_tr": "bir işe koyulmak, telefona bakmak",
        "t_pl": "zabrać się do czegoś, odebrać telefon", "t_it": "affrontare, rispondere al telefono",
        "t_es": "ponerse con, contestar el teléfono", "t_fr": "s'attaquer à, répondre au téléphone",
        "t_cs": "pustit se do, zvednout telefon",
        **all_x("Geh doch mal ran, dein Handy klingelt!", "Ответь, у тебя телефон звонит!", "Відповідай, у тебе телефон дзвонить!",
                "Answer it, your phone's ringing!", "Telefona baksana, çalıyor!", "Odbierz, dzwoni ci telefon!",
                "Rispondi, ti suona il telefono!", "¡Contesta, te suena el móvil!", "Réponds, ton téléphone sonne!",
                "Zvedni to, zvoní ti mobil!")}),
    7028: ("«Wir müssen die Eindringlinge vertreiben» — война; " + LIST, {
        "t_ru": "прогнать, скоротать (время)", "t_uk": "прогнати, згаяти (час)", "t_en": "to drive away, to pass (the time)",
        "t_tr": "kovmak, zaman geçirmek", "t_pl": "wypędzić, zabić (czas)", "t_it": "cacciare, far passare",
        "t_es": "echar, pasar (el tiempo)", "t_fr": "chasser, faire passer", "t_cs": "vyhnat, krátit si",
        **all_x("Wir spielen Karten, um uns die Zeit zu vertreiben", "Мы играем в карты, чтобы скоротать время",
                "Ми граємо в карти, щоб згаяти час", "We play cards to pass the time", "Zaman geçirmek için kart oynuyoruz",
                "Gramy w karty, żeby zabić czas", "Giochiamo a carte per far passare il tempo",
                "Jugamos a las cartas para pasar el tiempo", "On joue aux cartes pour faire passer le temps",
                "Hrajeme karty, abychom si krátili čas")}),
}

SPLIT_LATER = {}
