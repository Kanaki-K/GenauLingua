"""B1, блок 6: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Der Engel ist schön», «Der Schaden ist groß») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1383: ("«entlang des Flusses» — письменный родительный; в речи «am Fluss entlang»", {**all_x(
        "Wir gehen am Fluss entlang", "Мы гуляем вдоль реки", "Ми гуляємо вздовж річки", "We're walking along the river",
        "Nehir boyunca yürüyoruz", "Spacerujemy wzdłuż rzeki", "Passeggiamo lungo il fiume",
        "Paseamos a lo largo del río", "On se promène le long de la rivière", "Procházíme se podél řeky")}),
    1250: (EN + " («I write a report»); " + LIST, {
        "t_ru": "отчёт, доклад", "t_uk": "звіт, доповідь", "t_en": "report", "t_tr": "rapor", "t_pl": "raport, sprawozdanie",
        "t_it": "il rapporto, la relazione", "t_es": "el informe", "t_fr": "le rapport, le compte rendu",
        "t_cs": "zpráva, hlášení",
        **all_x("Bis Freitag muss ich den Bericht fertig haben", "К пятнице мне нужно закончить отчёт",
                "До п'ятниці мені треба закінчити звіт", "I need to have the report finished by Friday",
                "Raporu cumaya kadar bitirmem lazım", "Do piątku muszę skończyć raport",
                "Entro venerdì devo finire il rapporto", "Tengo que terminar el informe para el viernes",
                "Je dois finir le rapport d'ici vendredi", "Do pátku musím dokončit zprávu")}),
    10122: ("«Die Kinder schreien laut» — пусто; «плакать» — другое слово", {
        "t_ru": "кричать, орать", "t_uk": "кричати, верещати", "t_en": "to scream, to shout",
        "t_tr": "bağırmak, çığlık atmak", "t_pl": "krzyczeć, wrzeszczeć",
        **all_x("Schrei nicht so, ich bin nicht taub!", "Не кричи так, я не глухой!", "Не кричи так, я не глухий!",
                "Don't shout like that, I'm not deaf!", "Bu kadar bağırma, sağır değilim!", "Nie krzycz tak, nie jestem głuchy!",
                "Non gridare così, non sono sordo!", "¡No grites así, que no estoy sordo!",
                "Ne crie pas comme ça, je ne suis pas sourd!", "Nekřič tak, nejsem hluchý!")}),
    14374: ("«Die Prinzessin trägt eine Krone» — шаблон одежды, сказка", {**all_x(
        "Sie benimmt sich wie eine Prinzessin", "Она ведёт себя как принцесса", "Вона поводиться як принцеса",
        "She behaves like a princess", "Prenses gibi davranıyor", "Zachowuje się jak księżniczka",
        "Si comporta come una principessa", "Se comporta como una princesa", "Elle se comporte comme une princesse",
        "Chová se jako princezna")}),
    14931: ("«Komm her, mein Schätzchen» — шаблон Liebling («Komm her, Liebling»); " + LIST, {
        "t_ru": "золотце, солнышко", "t_uk": "золотко, любий", "t_en": "sweetheart, darling", "t_tr": "canım, tatlım",
        "t_pl": "skarbie, złotko",
        **all_x("Na, Schätzchen, wie war's in der Schule?", "Ну что, солнышко, как в школе?", "Ну що, золотко, як у школі?",
                "So, sweetheart, how was school?", "Eee canım, okul nasıldı?", "No i jak, skarbie, w szkole?",
                "Allora, tesoro, com'è andata a scuola?", "¿Qué tal, cariño, cómo te ha ido en el cole?",
                "Alors, mon trésor, c'était comment l'école?", "Tak co, zlatíčko, jaké to bylo ve škole?")}),
    12103: ("«Die Kinder rennen im Park» — пусто", {**all_x(
        "Ich musste rennen, um den Bus zu kriegen", "Мне пришлось бежать, чтобы успеть на автобус",
        "Мені довелося бігти, щоб устигнути на автобус", "I had to run to catch the bus",
        "Otobüse yetişmek için koşmak zorunda kaldım", "Musiałem biec, żeby zdążyć na autobus",
        "Ho dovuto correre per prendere l'autobus", "Tuve que correr para coger el autobús",
        "J'ai dû courir pour attraper le bus", "Musel jsem běžet, abych stihl autobus")}),
    15385: ("«Halt dein Maul» — грубость; Maul — прежде всего пасть животного", {
        "t_ru": "пасть, морда", "t_uk": "паща, писок", "t_en": "mouth (of an animal)", "t_tr": "ağız",
        "t_pl": "pysk, paszcza", "t_it": "la bocca, il muso", "t_es": "la boca, el hocico", "t_fr": "la gueule, le museau",
        "t_cs": "tlama",
        **all_x("Der Hund hat einen Ball im Maul", "У собаки в пасти мяч", "У собаки в пащі м'яч",
                "The dog has a ball in its mouth", "Köpeğin ağzında bir top var", "Pies ma piłkę w pysku",
                "Il cane ha una palla in bocca", "El perro tiene una pelota en la boca",
                "Le chien a une balle dans la gueule", "Pes má v tlamě míček")}),
    12104: ("«Ich hörte einen lauten Schuss» — претерит, детектив", {**all_x(
        "Der Schuss ging knapp am Tor vorbei", "Удар прошёл чуть мимо ворот", "Удар пройшов трохи повз ворота",
        "The shot just missed the goal", "Şut kaleyi az farkla ıskaladı", "Strzał minął bramkę o włos",
        "Il tiro è finito di poco fuori", "El tiro pasó rozando la portería", "Le tir est passé juste à côté du but",
        "Střela šla těsně vedle branky")}),
    13626: ("«Er trägt einen schwarzen Hut» — шаблон одежды", {**all_x(
        "Nimm den Hut ab, wir sind in der Kirche", "Сними шляпу, мы в церкви", "Зніми капелюх, ми в церкві",
        "Take your hat off, we're in church", "Şapkanı çıkar, kilisedeyiz", "Zdejmij kapelusz, jesteśmy w kościele",
        "Togliti il cappello, siamo in chiesa", "Quítate el sombrero, que estamos en la iglesia",
        "Enlève ton chapeau, on est à l'église", "Sundej si klobouk, jsme v kostele")}),
    2654: ("снова «головная боль»; живёт слово в «Ich kann ihn nicht leiden»", {
        "t_ru": "страдать, терпеть", "t_uk": "страждати, терпіти", "t_en": "to suffer, to stand",
        "t_tr": "acı çekmek, hoşlanmamak", "t_pl": "cierpieć, znosić", "t_it": "soffrire, sopportare",
        "t_es": "sufrir, soportar", "t_fr": "souffrir, supporter", "t_cs": "trpět, snášet",
        **all_x("Ich kann ihn nicht leiden", "Терпеть его не могу", "Терпіти його не можу", "I can't stand him",
                "Ondan hiç hoşlanmıyorum", "Nie znoszę go", "Non lo sopporto", "No lo soporto", "Je ne le supporte pas",
                "Nesnáším ho")}),
    6410: ("«Da ist ein Loch in der Wand» — скелет", {**all_x(
        "Ich habe ein Loch in der Socke", "У меня дырка на носке", "У мене дірка на шкарпетці",
        "I've got a hole in my sock", "Çorabımda delik var", "Mam dziurę w skarpetce", "Ho un buco nel calzino",
        "Tengo un agujero en el calcetín", "J'ai un trou à ma chaussette", "Mám díru v ponožce")}),
    10126: ("«Wir ehren unsere Eltern» — из проповеди", {**all_x(
        "Sie wurde für ihre Arbeit geehrt", "Её наградили за её работу", "Її відзначили за її роботу",
        "She was honoured for her work", "Çalışmaları için onurlandırıldı", "Została uhonorowana za swoją pracę",
        "È stata onorata per il suo lavoro", "Fue honrada por su trabajo", "Elle a été honorée pour son travail",
        "Byla oceněna za svou práci")}),
    6411: ("главное значение — «хватать», а не «передать соль»; " + LIST, {
        "t_ru": "хватать, передать", "t_uk": "вистачати, подати", "t_en": "to be enough, to pass", "t_tr": "yetmek, uzatmak",
        "t_pl": "wystarczać, podać", "t_it": "bastare, passare", "t_es": "bastar, pasar", "t_fr": "suffire, passer",
        "t_cs": "stačit, podat",
        **all_x("Das Geld reicht nicht bis zum Monatsende", "Денег не хватает до конца месяца",
                "Грошей не вистачає до кінця місяця", "The money doesn't last until the end of the month",
                "Para ay sonuna kadar yetmiyor", "Pieniądze nie wystarczają do końca miesiąca",
                "I soldi non bastano fino a fine mese", "El dinero no basta hasta final de mes",
                "L'argent ne suffit pas jusqu'à la fin du mois", "Peníze nestačí do konce měsíce")}),
    1778: ("«Das ist Quatsch» — шаблон Unsinn («Das ist totaler Unsinn»)", {**all_x(
        "Red keinen Quatsch!", "Не говори ерунды!", "Не кажи дурниць!", "Don't talk nonsense!", "Saçmalama!",
        "Nie gadaj bzdur!", "Non dire sciocchezze!", "¡No digas tonterías!", "Ne dis pas de bêtises!",
        "Nemluv nesmysly!")}),
    2292: ("«Er war betrunken» — пусто", {**all_x(
        "Fahr nicht, du bist betrunken!", "Не садись за руль, ты пьян!", "Не сідай за кермо, ти п'яний!",
        "Don't drive, you're drunk!", "Araba kullanma, sarhoşsun!", "Nie prowadź, jesteś pijany!",
        "Non guidare, sei ubriaco!", "¡No conduzcas, que estás borracho!", "Ne conduis pas, tu es ivre!",
        "Neřiď, jsi opilý!")}),
    6412: (SKEL, {**all_x(
        "Du bist ein Engel, danke!", "Ты просто ангел, спасибо!", "Ти просто ангел, дякую!",
        "You're an angel, thank you!", "Sen bir meleksin, teşekkürler!", "Jesteś aniołem, dzięki!",
        "Sei un angelo, grazie!", "¡Eres un ángel, gracias!", "Tu es un ange, merci!", "Jsi anděl, díky!")}),
    6414: (SKEL + "; " + LIST, {
        "t_ru": "ущерб, вред", "t_uk": "шкода, збиток", "t_en": "damage, harm", "t_tr": "hasar, zarar",
        "t_pl": "szkoda, uszkodzenie",
        **all_x("Die Versicherung zahlt den Schaden", "Страховка покроет ущерб", "Страховка покриє збитки",
                "The insurance will pay for the damage", "Hasarı sigorta ödüyor", "Ubezpieczenie pokryje szkodę",
                "L'assicurazione paga il danno", "El seguro paga los daños", "L'assurance paie les dégâts",
                "Pojišťovna zaplatí škodu")}),
    6415: (LIST, {"t_ru": "ценить, оценивать", "t_uk": "цінувати, оцінювати", "t_en": "to appreciate, to estimate",
                  "t_tr": "takdir etmek, tahmin etmek", "t_pl": "cenić, szacować", "t_it": "apprezzare, stimare",
                  "t_es": "apreciar, calcular", "t_fr": "apprécier, estimer", "t_cs": "vážit si, odhadovat"}),
    6417: ("«Das kann brechen» — пусто", {**all_x(
        "Pass auf, das Eis bricht gleich!", "Осторожно, лёд сейчас проломится!", "Обережно, лід зараз проломиться!",
        "Careful, the ice is going to break!", "Dikkat et, buz kırılmak üzere!", "Uważaj, lód zaraz pęknie!",
        "Attento, il ghiaccio si sta rompendo!", "¡Cuidado, que el hielo se va a romper!", "Attention, la glace va casser!",
        "Pozor, led se za chvíli prolomí!")}),
    2223: (LIST, {"t_ru": "заказ, поручение", "t_uk": "замовлення, доручення", "t_en": "order, assignment",
                  "t_tr": "sipariş, görev", "t_pl": "zlecenie, zamówienie", "t_it": "l'incarico, l'ordine",
                  "t_es": "el encargo, el pedido", "t_fr": "la mission, la commande", "t_cs": "zakázka, úkol"}),
    10127: ("«У тебя много смелости» — калька", {**all_x(
        "Dazu braucht man viel Mut", "Для этого нужно много смелости", "Для цього потрібна велика сміливість",
        "That takes a lot of courage", "Bunun için çok cesaret gerekiyor", "Do tego potrzeba dużo odwagi",
        "Ci vuole molto coraggio", "Para eso hace falta mucho valor", "Il faut beaucoup de courage pour ça",
        "K tomu je potřeba hodně odvahy")}),
    6422: ("«Ein Haufen Arbeit wartet» — неживо", {**all_x(
        "Ich habe einen Haufen Arbeit", "У меня куча работы", "У мене купа роботи", "I've got a pile of work",
        "Bir yığın işim var", "Mam kupę roboty", "Ho un mucchio di lavoro", "Tengo un montón de trabajo",
        "J'ai un tas de travail", "Mám hromadu práce")}),
    17061: ("«Die Fahrt war schön» — пусто", {**all_x(
        "Die Fahrt nach Hamburg dauert drei Stunden", "Поездка до Гамбурга занимает три часа",
        "Поїздка до Гамбурга триває три години", "The drive to Hamburg takes three hours",
        "Hamburg'a yolculuk üç saat sürüyor", "Jazda do Hamburga trwa trzy godziny",
        "Il viaggio fino ad Amburgo dura tre ore", "El viaje a Hamburgo dura tres horas",
        "Le trajet jusqu'à Hambourg dure trois heures", "Cesta do Hamburku trvá tři hodiny")}),
    12106: ("«Er schießt ein Tor» — тот же пример, что у schießen", {**all_x(
        "Wer hat das Tor geschossen?", "Кто забил гол?", "Хто забив гол?", "Who scored the goal?", "Golü kim attı?",
        "Kto strzelił gola?", "Chi ha segnato il gol?", "¿Quién ha marcado el gol?", "Qui a marqué le but?",
        "Kdo dal gól?")}),
    6428: ("«Der Druck ist zu hoch» — пусто; " + LIST, {
        "t_ru": "давление, печать", "t_uk": "тиск, друк", "t_en": "pressure, print", "t_tr": "basınç, baskı",
        "t_pl": "ciśnienie, presja", "t_it": "la pressione, la stampa", "t_es": "la presión, la impresión",
        "t_fr": "la pression, l'impression", "t_cs": "tlak, tisk",
        **all_x("Bei der Arbeit stehe ich unter Druck", "На работе я под давлением", "На роботі я під тиском",
                "I'm under pressure at work", "İşte baskı altındayım", "W pracy jestem pod presją",
                "Al lavoro sono sotto pressione", "En el trabajo estoy bajo presión", "Au travail, je suis sous pression",
                "V práci jsem pod tlakem")}),
    2038: ("«Dein Verhalten ist gut» — неживо", {**all_x(
        "Ich verstehe sein Verhalten nicht", "Я не понимаю его поведения", "Я не розумію його поведінки",
        "I don't understand his behaviour", "Onun davranışını anlamıyorum", "Nie rozumiem jego zachowania",
        "Non capisco il suo comportamento", "No entiendo su comportamiento", "Je ne comprends pas son comportement",
        "Nerozumím jeho chování")}),
}

SPLIT_LATER = {}
