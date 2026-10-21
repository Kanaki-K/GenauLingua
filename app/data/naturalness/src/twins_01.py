"""Почти-повторы примеров, внесённые вычиткой в блоках 02–23 (проверка `near_twins` 21.10)."""

WHY = "мой новый пример почти повторял пример другого слова (проверка near_twins 21.10)"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    362: (WHY + " — Ansicht («… eine gute Idee»)", {**all_x(
        "Du sprichst schon gut Deutsch!", "Ты уже хорошо говоришь по-немецки!", "Ти вже добре говориш німецькою!",
        "You already speak good German!", "Zaten iyi Almanca konuşuyorsun!", "Już dobrze mówisz po niemiecku!",
        "Parli già bene il tedesco!", "¡Ya hablas bien alemán!", "Tu parles déjà bien allemand!",
        "Už mluvíš dobře německy!")}),
    251: (WHY + " — zusammenkommen («Am Sonntag … die ganze Familie zusammen»)", {**all_x(
        "Meine Familie wohnt in Polen", "Моя семья живёт в Польше", "Моя родина живе в Польщі",
        "My family lives in Poland", "Ailem Polonya'da yaşıyor", "Moja rodzina mieszka w Polsce",
        "La mia famiglia vive in Polonia", "Mi familia vive en Polonia", "Ma famille habite en Pologne",
        "Moje rodina bydlí v Polsku")}),
    1534: (WHY + " — Dank («Vielen Dank…»)", {**all_x(
        "Sie hat uns herzlich begrüßt", "Она тепло нас встретила", "Вона тепло нас привітала",
        "She greeted us warmly", "Bizi sıcak karşıladı", "Serdecznie nas przywitała", "Ci ha accolti calorosamente",
        "Nos recibió con mucho cariño", "Elle nous a accueillis chaleureusement", "Srdečně nás přivítala")}),
    942: (WHY + " — etwas («Möchtest du etwas trinken?»)", {**all_x(
        "Du musst mehr Wasser trinken", "Тебе нужно пить больше воды", "Тобі треба пити більше води",
        "You need to drink more water", "Daha fazla su içmelisin", "Musisz pić więcej wody", "Devi bere più acqua",
        "Tienes que beber más agua", "Tu dois boire plus d'eau", "Musíš pít víc vody")}),
    6296: (WHY + " — anmachen («Mach bitte das Licht an»)", {**all_x(
        "Hier ist zu wenig Licht zum Lesen", "Здесь слишком мало света для чтения", "Тут замало світла для читання",
        "There isn't enough light here to read", "Burada okumak için yeterince ışık yok",
        "Jest tu za mało światła do czytania", "Qui c'è poca luce per leggere", "Aquí hay poca luz para leer",
        "Il n'y a pas assez de lumière ici pour lire", "Je tu málo světla na čtení")}),
    497: (WHY + " — Topf («Ich koche Suppe…»)", {**all_x(
        "Wer kocht heute?", "Кто сегодня готовит?", "Хто сьогодні готує?", "Who's cooking today?",
        "Bugün yemeği kim yapıyor?", "Kto dziś gotuje?", "Chi cucina oggi?", "¿Quién cocina hoy?",
        "Qui fait la cuisine aujourd'hui?", "Kdo dnes vaří?")}),
    695: (WHY + " — Blatt («Gib mir ein Blatt Papier»)", {**all_x(
        "Der Drucker hat kein Papier mehr", "В принтере закончилась бумага", "У принтері закінчився папір",
        "The printer is out of paper", "Yazıcıda kağıt kalmadı", "W drukarce skończył się papier",
        "La stampante è senza carta", "La impresora se ha quedado sin papel", "L'imprimante n'a plus de papier",
        "V tiskárně došel papír")}),
    965: (WHY + " — ausfallen («Der Unterricht fällt heute aus»: та же фраза)", {**all_x(
        "Der Unterricht macht mir Spaß", "Мне нравятся занятия", "Мені подобаються заняття", "I enjoy the lessons",
        "Dersler hoşuma gidiyor", "Lekcje sprawiają mi przyjemność", "Le lezioni mi piacciono", "Me gustan las clases",
        "J'aime bien les cours", "Výuka mě baví")}),
    398: (WHY + " — abfallen («Die Blätter fallen jetzt im Herbst ab»)", {**all_x(
        "Im Herbst gehen wir gern in den Wald", "Осенью мы любим ходить в лес", "Восени ми любимо ходити до лісу",
        "In autumn we like going to the forest", "Sonbaharda ormana gitmeyi severiz", "Jesienią lubimy chodzić do lasu",
        "In autunno ci piace andare nel bosco", "En otoño nos gusta ir al bosque", "En automne, on aime aller en forêt",
        "Na podzim rádi chodíme do lesa")}),
    753: (WHY + " — zuweilen («… regnet es den ganzen Tag»)", {**all_x(
        "Nimm einen Schirm mit, es regnet", "Возьми зонт, идёт дождь", "Візьми парасольку, йде дощ",
        "Take an umbrella, it's raining", "Şemsiye al, yağmur yağıyor", "Weź parasol, pada deszcz",
        "Prendi l'ombrello, piove", "Llévate un paraguas, que llueve", "Prends un parapluie, il pleut",
        "Vezmi si deštník, prší")}),
    539: (WHY + " — erstmal («Lass mich erstmal in Ruhe…»)", {**all_x(
        "Lass die Tür bitte offen", "Оставь, пожалуйста, дверь открытой", "Залиш, будь ласка, двері відчиненими",
        "Leave the door open, please", "Kapıyı açık bırak lütfen", "Zostaw, proszę, otwarte drzwi",
        "Lascia la porta aperta, per favore", "Deja la puerta abierta, por favor",
        "Laisse la porte ouverte, s'il te plaît", "Nech prosím dveře otevřené")}),
}
