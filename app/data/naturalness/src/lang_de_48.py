"""Вычитка немецкого, порция p048 (C2), 23.10: заглушка → бытовая"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    14310: (W, ex("Die Notrufzentrale hat sofort einen Krankenwagen geschickt",
        "Служба экстренных вызовов сразу прислала скорую", "Служба екстрених викликів одразу надіслала швидку",
        "The emergency call centre sent an ambulance straight away", "Acil çağrı merkezi hemen bir ambulans gönderdi",
        "Centrum powiadamiania ratunkowego od razu wysłało karetkę", "La centrale operativa ha mandato subito un'ambulanza",
        "La central de emergencias mandó una ambulancia enseguida", "Le centre d'appels d'urgence a tout de suite envoyé une ambulance",
        "Tísňová linka hned poslala sanitku")),
}

REPLACE = []

SPLIT_LATER = {}
