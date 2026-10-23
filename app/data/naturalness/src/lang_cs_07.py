"""Вычитка чешского, порция p007 (A2–B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    17783: (T + "«je jen online» — оборвано", {"example_cs": "Tenhle výrobek se prodává jen online"}),
    18369: (T + "«Naše majitelka bytu» — тяжело", {"example_cs": "Naše bytná bydlí v přízemí"}),
    35: (T + "«oblékám» — не тот вид", {"example_cs": "Rychle se obléknu"}),
    147: (T + "Anmeldung — регистрация адреса, не «trvalý pobyt»", {"example_cs": "Jdu na úřad pro občany přehlásit adresu"}),
    377: (T + "«mrazivo» — книжно", {"example_cs": "Vezmi si rukavice, venku je mráz"}),
    485: (T + "«svoje» — лишнее", {"example_cs": "Uklízím si oblečení"}),
    502: (T + "время: история в прошлом", {"example_cs": "Při kontrole v autobuse jsem měl naštěstí u sebe měsíční jízdenku"}),
    592: (T + "«nesnáší» — двусмысленно", {"example_cs": "Moje kamarádka nemůže jíst mléčné výrobky"}),
    736: (T + "«s mlékem» — калька", {"example_cs": "Vařím pudink na mléce"}),
}

REPLACE = []

SPLIT_LATER = {}
