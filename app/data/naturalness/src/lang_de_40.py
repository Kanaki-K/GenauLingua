"""Вычитка немецкого, порция p040 (C1), 23.10: заглушка → бытовая"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    9887: (W + "; «Seine Integrität» — книжно", ex("Echte Freundschaft ist nicht käuflich",
        "Настоящую дружбу не купишь", "Справжню дружбу не купиш",
        "Real friendship can't be bought", "Gerçek dostluk satın alınamaz",
        "Prawdziwej przyjaźni nie da się kupić", "La vera amicizia non si compra",
        "La amistad de verdad no se compra", "La vraie amitié ne s'achète pas",
        "Opravdové přátelství se nedá koupit")),
}

REPLACE = []

SPLIT_LATER = {}
