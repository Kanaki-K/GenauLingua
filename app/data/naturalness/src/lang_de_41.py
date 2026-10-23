"""Вычитка немецкого, порция p041 (C1), 23.10: заглушка → бытовая"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    11077: (W + "; второе значение: сладкое вино", ex("Der Wein ist mir zu lieblich, ich trinke lieber trockenen",
        "Это вино для меня слишком сладкое, я предпочитаю сухое", "Це вино для мене занадто солодке, я волію сухе",
        "This wine is too sweet for me, I prefer dry", "Bu şarap bana fazla tatlı, sek olanı tercih ederim",
        "To wino jest dla mnie za słodkie, wolę wytrawne", "Questo vino per me è troppo amabile, preferisco quello secco",
        "Este vino es demasiado dulce para mí, prefiero el seco", "Ce vin est trop doux pour moi, je préfère le sec",
        "To víno je na mě moc sladké, radši piju suché")),
}

REPLACE = []

SPLIT_LATER = {}
