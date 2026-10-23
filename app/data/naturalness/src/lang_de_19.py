"""Вычитка немецкого, порция p019 (B1), 23.10: заглушки → живые бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    10545: (W, ex("Aus Überzeugung esse ich seit Jahren kein Fleisch",
        "По убеждению я уже много лет не ем мяса", "З переконання я вже багато років не їм м'яса",
        "Out of conviction I haven't eaten meat for years", "İnancım gereği yıllardır et yemiyorum",
        "Z przekonania od lat nie jem mięsa", "Per convinzione non mangio carne da anni",
        "Por convicción llevo años sin comer carne", "Par conviction, je ne mange plus de viande depuis des années",
        "Z přesvědčení už roky nejím maso")),
    11588: (W + "; «völlig unbegründet» — книжно", ex("Meine Befürchtung war richtig: Der Zug ist ausgefallen",
        "Мои опасения подтвердились: поезд отменили", "Мої побоювання справдилися: потяг скасували",
        "My fear was right: the train has been cancelled", "Endişem doğruymuş: tren iptal oldu",
        "Moje obawy się potwierdziły: pociąg odwołano", "Il mio timore era giusto: il treno è stato cancellato",
        "Mi temor era cierto: han cancelado el tren", "Ma crainte était fondée : le train a été annulé",
        "Moje obava byla správná: vlak zrušili")),
    11673: (W, ex("Im Winter finden die Vögel kaum Nahrung",
        "Зимой птицы почти не находят корма", "Узимку птахи майже не знаходять корму",
        "In winter the birds can hardly find any food", "Kışın kuşlar neredeyse hiç yiyecek bulamıyor",
        "Zimą ptaki prawie nie znajdują pożywienia", "D'inverno gli uccelli trovano poco cibo",
        "En invierno los pájaros apenas encuentran comida", "En hiver, les oiseaux ne trouvent presque pas de nourriture",
        "V zimě ptáci skoro nenajdou potravu")),
    11719: (W, ex("Früher hat man auf dem Dorf zu Weihnachten eine Gans geschlachtet",
        "Раньше в деревне на Рождество резали гуся", "Раніше в селі на Різдво різали гусака",
        "In the old days people in the village slaughtered a goose for Christmas", "Eskiden köyde Noel'de bir kaz keserlerdi",
        "Dawniej na wsi na święta zabijało się gęś", "Una volta in campagna a Natale si ammazzava un'oca",
        "Antes en el pueblo se mataba un ganso en Navidad", "Autrefois, au village, on tuait une oie pour Noël",
        "Dřív se na vesnici na Vánoce zabíjela husa")),
}

REPLACE = []

SPLIT_LATER = {}
