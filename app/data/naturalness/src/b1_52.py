"""B1, блок 52: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    13996: (LIST + " (было семь значений)", {
        "t_ru": "вклад, взнос", "t_uk": "внесок, стаття", "t_en": "contribution, fee", "t_tr": "katkı, aidat",
        "t_pl": "wkład, składka", "t_it": "il contributo, la quota", "t_es": "la aportación, la cuota",
        "t_fr": "la contribution, la cotisation", "t_cs": "příspěvek"}),
    17939: ("«Die Formel ist sehr wichtig für die Mathematik» — учебник", {**all_x(
        "Kannst du dir die Formel merken?", "Ты можешь запомнить формулу?", "Ти можеш запам'ятати формулу?",
        "Can you remember the formula?", "Formülü aklında tutabiliyor musun?", "Zapamiętasz ten wzór?",
        "Riesci a ricordare la formula?", "¿Te acuerdas de la fórmula?", "Tu arrives à retenir la formule?",
        "Zapamatuješ si ten vzorec?")}),
    16134: ("«Der Raub in der Bank war spektakulär» — претерит, хроника", {**all_x(
        "Er sitzt wegen Raub im Gefängnis", "Он сидит в тюрьме за грабёж", "Він сидить у в'язниці за грабіж",
        "He's in prison for robbery", "Gasp yüzünden hapiste", "Siedzi w więzieniu za rabunek", "È in prigione per rapina",
        "Está en la cárcel por robo", "Il est en prison pour vol", "Sedí ve vězení za loupež")}),
    18713: ("снова Projekt", {**all_x(
        "Wir liegen gut im Zeitplan", "Мы хорошо укладываемся в график", "Ми добре вкладаємося в графік",
        "We're well on schedule", "Programa göre iyi gidiyoruz", "Dobrze trzymamy się harmonogramu",
        "Siamo in linea con la tabella di marcia", "Vamos bien con el calendario",
        "On est dans les temps par rapport au planning", "Jsme dobře v harmonogramu")}),
    11711: ("«Zum Frühstück esse ich gerne …» — шаблон Speck; " + LIST, {
        "t_ru": "блин, оладья", "t_uk": "млинець, оладка", "t_en": "pancake", "t_tr": "krep, pankek",
        "t_pl": "naleśnik, placek",
        **all_x("Oma macht die besten Pfannkuchen", "Бабушка печёт лучшие блины", "Бабуся пече найкращі млинці",
                "Gran makes the best pancakes", "En güzel krepleri anneannem yapar", "Babcia robi najlepsze naleśniki",
                "La nonna fa le crespelle più buone", "La abuela hace las mejores tortitas", "Mamie fait les meilleures crêpes",
                "Babička dělá nejlepší palačinky")}),
    7064: ("«Sie war total aufgelöst …» — претерит", {**all_x(
        "Sie ist völlig aufgelöst, was ist passiert?", "Она совсем расстроена, что случилось?", "Вона зовсім засмучена, що сталося?",
        "She's completely distraught – what happened?", "Çok üzgün, ne oldu?", "Jest kompletnie roztrzęsiona, co się stało?",
        "È sconvolta, cos'è successo?", "Está deshecha, ¿qué ha pasado?", "Elle est bouleversée, qu'est-ce qui s'est passé?",
        "Je úplně rozrušená, co se stalo?")}),
    1425: ("«Die Flamme flackert orange» — пусто", {**all_x(
        "Stell die Flamme kleiner", "Сделай пламя поменьше", "Зменш полум'я", "Turn the flame down", "Alevi kıs",
        "Zmniejsz płomień", "Abbassa la fiamma", "Baja la llama", "Baisse la flamme", "Ztlum plamen")}),
    16135: ("пример про Versicherungspolice, а не про Police", {**all_x(
        "Lies dir die Police genau durch", "Внимательно прочитай полис", "Уважно прочитай поліс",
        "Read the policy carefully", "Poliçeyi dikkatlice oku", "Przeczytaj dokładnie polisę",
        "Leggi attentamente la polizza", "Lee bien la póliza", "Lis bien la police d'assurance",
        "Přečti si pozorně pojistku")}),
    12585: ("«Die Überlebenden … wurden … gebracht» — претерит, хроника", {**all_x(
        "Gibt es Überlebende?", "Есть выжившие?", "Є вцілілі?", "Are there any survivors?", "Hayatta kalan var mı?",
        "Czy są ocalali?", "Ci sono sopravvissuti?", "¿Hay supervivientes?", "Il y a des survivants?",
        "Jsou nějací přeživší?")}),
    1118: ("«Der Hund ist nicht aggressiv» — шаблон harmlos (собака)", {**all_x(
        "Warum bist du heute so aggressiv?", "Почему ты сегодня такой агрессивный?", "Чому ти сьогодні такий агресивний?",
        "Why are you so aggressive today?", "Bugün neden bu kadar agresifsin?", "Czemu jesteś dziś taki agresywny?",
        "Perché oggi sei così aggressivo?", "¿Por qué estás tan agresivo hoy?", "Pourquoi tu es si agressif aujourd'hui?",
        "Proč jsi dneska tak agresivní?")}),
    17530: (EN + " («flashlight» — американское)", {"x_en": "My torch battery is flat"}),
    10456: ("убрать пометку (coloq.)", {"t_es": "terco, cabezota"}),
    16136: ("«Im Sommer herrschen hohe Temperaturen» — снова погода", {**all_x(
        "Hier herrscht ja totales Chaos!", "Тут же царит полный хаос!", "Тут панує повний хаос!", "Total chaos reigns here!",
        "Burada tam bir kaos hüküm sürüyor!", "Tu panuje totalny chaos!", "Qui regna il caos totale!",
        "¡Aquí reina el caos total!", "Ici, c'est le chaos total qui règne!", "Tady panuje totální chaos!")}),
    18201: ("«Ich muss mein Auto reinigen» — в речи «waschen»; reinigen — «в чистку»", {**all_x(
        "Den Anzug lasse ich reinigen", "Костюм я отдам в чистку", "Костюм я віддам у чистку", "I'm having the suit cleaned",
        "Takım elbiseyi temizletiyorum", "Oddam garnitur do czyszczenia", "Faccio pulire il vestito",
        "Llevo el traje a limpiar", "Je fais nettoyer le costume", "Oblek nechám vyčistit")}),
    15035: ("«Wir kümmern uns füreinander» — грамматика (umeinander)", {**all_x(
        "Wir sind immer füreinander da", "Мы всегда рядом друг для друга", "Ми завжди є одне для одного",
        "We're always there for each other", "Hep birbirimiz için varız", "Zawsze jesteśmy dla siebie",
        "Ci siamo sempre l'uno per l'altro", "Siempre estamos el uno para el otro", "On est toujours là l'un pour l'autre",
        "Vždycky jsme tu jeden pro druhého")}),
}

REPLACE = [
    {"id": 15031, "by": 18190, "lang": "de", "why": "Nägel — мн. число Nagel"},
    {"id": 13997, "by": 2891, "lang": "de", "why": "überein — часть глагола übereinstimmen"},
    {"id": 8858, "by": 3066, "lang": "de", "why": "kooperieren — книжный вариант zusammenarbeiten"},
]

SPLIT_LATER = {
    17531: ["auf Draht sein = быть начеку, соображать"],
}
