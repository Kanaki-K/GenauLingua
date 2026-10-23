"""Вычитка немецкого, порция p049 (C2), 23.10: заглушка → бытовая"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    16858: (W + "; отчёт", ex("Die Steuerbehörde will noch Belege für mein Arbeitszimmer sehen",
        "Налоговая хочет ещё увидеть чеки на мой рабочий кабинет", "Податкова хоче ще побачити чеки за мій робочий кабінет",
        "The tax office still wants to see receipts for my home office", "Vergi dairesi çalışma odam için belgeleri de görmek istiyor",
        "Urząd skarbowy chce jeszcze zobaczyć rachunki za mój gabinet", "L'ufficio delle imposte vuole vedere ancora le ricevute per il mio studio",
        "Hacienda todavía quiere ver los justificantes de mi despacho", "Le fisc veut encore voir les justificatifs pour mon bureau",
        "Finanční úřad chce ještě vidět doklady k mé pracovně")),
}

REPLACE = []

SPLIT_LATER = {}
