"""Вычитка немецкого, порция p042 (C1), 23.10: заглушка → бытовая"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    14118: (W + "; «zwischen den Parteien» — суд", ex("Meine Tante hat mir den Job im Hotel vermittelt",
        "Тётя помогла мне устроиться на работу в отель", "Тітка допомогла мені влаштуватися на роботу в готель",
        "My aunt got me the job at the hotel", "Teyzem otelde iş bulmama aracı oldu",
        "Ciocia załatwiła mi pracę w hotelu", "Mia zia mi ha procurato il lavoro in albergo",
        "Mi tía me consiguió el trabajo en el hotel", "Ma tante m'a trouvé le boulot à l'hôtel",
        "Teta mi zprostředkovala práci v hotelu")),
}

REPLACE = []

SPLIT_LATER = {}
