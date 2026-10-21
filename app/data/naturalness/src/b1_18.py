"""B1, блок 18: следующие 40 по частоте. Вычитано вручную 21.10."""


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    10229: ("«Er muss vor Schmerzen stöhnen» — неживо", {**all_x(
        "Der Patient hat die ganze Nacht gestöhnt", "Пациент стонал всю ночь", "Пацієнт стогнав усю ніч",
        "The patient groaned all night", "Hasta bütün gece inledi", "Pacjent jęczał całą noc",
        "Il paziente ha gemuto tutta la notte", "El paciente gimió toda la noche", "Le patient a gémi toute la nuit",
        "Pacient celou noc sténal")}),
    10230: ("«Ich bin das gewohnt» — шаблон gewöhnt («Ich bin daran schon gewöhnt»)", {**all_x(
        "Alles läuft wie gewohnt", "Всё идёт как обычно", "Усе йде як звичайно",
        "Everything's going on as usual", "Her şey her zamanki gibi gidiyor", "Wszystko idzie jak zwykle",
        "Tutto va come al solito", "Todo va como es habitual", "Tout se passe comme d'habitude",
        "Všechno běží jako obvykle")}),
    10231: ("«Ты должен меня отпустить» — калька с musst", {**all_x(
        "Lass mich los!", "Отпусти меня!", "Відпусти мене!", "Let go of me!", "Bırak beni!", "Puść mnie!",
        "Lasciami!", "¡Suéltame!", "Lâche-moi!", "Pusť mě!")}),
    10233: ("«Ich fürchte das Gewitter» — книжно; в речи — «Ich fürchte, …»", {**all_x(
        "Ich fürchte, das klappt nicht", "Боюсь, ничего не получится", "Боюся, нічого не вийде",
        "I'm afraid it won't work", "Korkarım bu olmayacak", "Obawiam się, że to się nie uda",
        "Temo che non funzionerà", "Me temo que no va a funcionar", "Je crains que ça ne marche pas",
        "Obávám se, že to nevyjde")}),
    17918: ("«Ich interessiere mich für …» — пятый такой пример", {**all_x(
        "Das ist eine Wissenschaft für sich", "Это целая наука", "Це ціла наука", "That's a science in itself",
        "Bu başlı başına bir bilim", "To cała nauka", "È una scienza a sé", "Es toda una ciencia",
        "C'est une science à part entière", "To je věda sama o sobě")}),
    1148: ("«Ich muss einen Antrag stellen» — канцелярия; второе живое значение — предложение руки", {**all_x(
        "Er hat ihr einen Antrag gemacht", "Он сделал ей предложение", "Він зробив їй пропозицію",
        "He made her a proposal of marriage", "Ona evlenme teklif etti", "Oświadczył się jej",
        "Le ha fatto la proposta di matrimonio", "Le hizo una propuesta de matrimonio",
        "Il l'a demandée en mariage", "Požádal ji o ruku")}),
    13476: ("«Das Buch kostet hundert Euro» — шаблон fünfzig, tausend", {**all_x(
        "Auf der Party waren hundert Leute", "На вечеринке было сто человек", "На вечірці було сто людей",
        "There were a hundred people at the party", "Partide yüz kişi vardı", "Na imprezie było sto osób",
        "Alla festa c'erano cento persone", "En la fiesta había cien personas", "Il y avait cent personnes à la fête",
        "Na večírku bylo sto lidí")}),
    8781: ("«Der Bauer arbeitet auf dem Feld» — шаблон Feld, из букваря", {**all_x(
        "Wir kaufen Eier direkt beim Bauern", "Мы покупаем яйца прямо у фермера", "Ми купуємо яйця просто у фермера",
        "We buy eggs straight from the farmer", "Yumurtaları doğrudan çiftçiden alıyoruz",
        "Kupujemy jajka prosto od rolnika", "Compriamo le uova direttamente dal contadino",
        "Compramos los huevos directamente al agricultor", "On achète les œufs directement chez le paysan",
        "Vajíčka kupujeme přímo od zemědělce")}),
    10235: ("«Das ist doch totaler Schwachsinn» — шаблон Unsinn («Das ist totaler Unsinn»)", {**all_x(
        "So ein Schwachsinn, das glaube ich nicht", "Какой бред, я в это не верю", "Яка нісенітниця, я в це не вірю",
        "What rubbish, I don't believe that", "Ne saçmalık, buna inanmıyorum", "Co za bzdura, nie wierzę w to",
        "Che stupidaggine, non ci credo", "¡Qué tontería, no me lo creo!", "Quelle bêtise, je n'y crois pas",
        "Takový nesmysl, tomu nevěřím")}),
    14398: ("«Probe für das Konzert» — снова Konzert", {**all_x(
        "Ich habe heute Probe im Chor", "У меня сегодня репетиция в хоре", "У мене сьогодні репетиція в хорі",
        "I've got choir rehearsal today", "Bugün koroda provam var", "Mam dziś próbę chóru",
        "Oggi ho le prove del coro", "Hoy tengo ensayo con el coro", "J'ai répétition de chorale aujourd'hui",
        "Dneska mám zkoušku sboru")}),
    1401: ("«Die Polizei hat ihn erwischt» — десятый пример с Polizei", {**all_x(
        "Ich habe den Bus gerade noch erwischt", "Я едва успел на автобус", "Я ледве встиг на автобус",
        "I only just caught the bus", "Otobüse son anda yetiştim", "Ledwo zdążyłem na autobus",
        "Ho preso l'autobus per un pelo", "Pillé el autobús por los pelos", "J'ai attrapé le bus de justesse",
        "Autobus jsem tak tak stihl")}),
    10241: ("«Du bist sehr mutig» — пусто", {**all_x(
        "Die Kinder sind mutig ins kalte Wasser gesprungen", "Дети смело прыгнули в холодную воду",
        "Діти сміливо стрибнули в холодну воду", "The children bravely jumped into the cold water",
        "Çocuklar cesurca soğuk suya atladı", "Dzieci odważnie wskoczyły do zimnej wody",
        "I bambini si sono tuffati coraggiosamente nell'acqua fredda", "Los niños se tiraron valientes al agua fría",
        "Les enfants ont courageusement sauté dans l'eau froide", "Děti odvážně skočily do studené vody")}),
}

SPLIT_LATER = {}
