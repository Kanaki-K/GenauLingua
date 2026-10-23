"""Вычитка польского, порция p021 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    13002: (T + "«na toalecie» — коряво", {"example_pl": "Na telefonie jest więcej zarazków niż na desce klozetowej"}),
    13057: (T + "«Jego dziąsła krwawią» — калька", {"example_pl": "Krwawią mu dziąsła przy myciu zębów"}),
    13060: (T + "«jego głos był» — калька", {"example_pl": "Po koncercie w Monachium był zachrypnięty"}),
    13061: (T + "«Mój» — лишнее", {"example_pl": "Wujek jest cukrzykiem i musi uważać na dietę"}),
    13140: (T + "«Moja» — лишнее", {"example_pl": "Babcia ma reumatyzm i trudno jej chodzić"}),
    13175: (T + "«Moja … swojego» — лишнее", {"example_pl": "Żona ma wizytę u ginekologa"}),
    13444: (T + "«Czy ktoś» — книжно", {"example_pl": "Dzwonił ktoś?"}),
    13497: (T + "«Czy ktoś» — книжно", {"example_pl": "Widział ktoś z was mój telefon?"}),
    13570: (T + "«sporo razy» — коряво", {"example_pl": "Dzwoniłem do ciebie już kilka razy"}),
    13599: (T + "«Nasz» — лишнее", {"example_pl": "Syn ma teraz cztery i pół roku"}),
    13631: (T + "«potrzebuje ubrania» — калька", {"example_pl": "Dziecko jest gołe, trzeba je ubrać"}),
    13746: (T + "«swoje» — лишнее", {"example_pl": "Rano najpierw wkładam kapcie"}),
    13749: (T + "«swój» — лишнее", {"example_pl": "Pożyczysz mi czerwony lakier do paznokci?"}),
    13767: (T + "«Nosi swoje … związane» — тяжело", {"example_pl": "Długie włosy wiąże w kucyk"}),
    13911: (T + "«Oto … dla ciebie» — книжно", {"example_pl": "Mam dla ciebie ważną wskazówkę"}),
    13930: (T + "«On» — лишнее", {"example_pl": "Jest tu, że tak powiem, szefem"}),
    13934: (T + "порядок слов", {"example_pl": "Łaskawie przestań!"}),
    13944: (T + "порядок слов", {"example_pl": "Możesz się jutro ze mną skontaktować?"}),
    13949: (T + "«Mój» — лишнее", {"example_pl": "Dziadek pali fajkę"}),
    13964: (T + "«moja» — лишнее", {"example_pl": "Na ślub babcia dostała jeszcze telegram"}),
    13986: (T + "«On» — лишнее", {"example_pl": "Zaprzecza wszystkiemu, co mówię"}),
    13987: (T + "«Chętnie czytam» — калька gern", {"example_pl": "Lubię czytać to czasopismo"}),
}

REPLACE = []

SPLIT_LATER = {}
