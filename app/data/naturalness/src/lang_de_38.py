"""Вычитка немецкого, порция p038 (B2), 23.10: заглушки → бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    18742: (W + "; «schenkt man sich Blumen» — открытка", ex("Am Valentinstag sind alle Restaurants in der Stadt ausgebucht",
        "В День святого Валентина все рестораны в городе забронированы", "У День святого Валентина всі ресторани в місті заброньовані",
        "On Valentine's Day all the restaurants in town are fully booked", "Sevgililer Günü'nde şehirdeki bütün restoranlar dolu",
        "W walentynki wszystkie restauracje w mieście są zarezerwowane", "A San Valentino tutti i ristoranti in città sono al completo",
        "En San Valentín todos los restaurantes de la ciudad están llenos", "À la Saint-Valentin, tous les restaurants de la ville sont complets",
        "Na Valentýna jsou všechny restaurace ve městě plně obsazené")),
}

REPLACE = []

SPLIT_LATER = {}
