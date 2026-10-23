"""Вычитка польского, порция p004 (A2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    67: (T + "«Moja» — лишнее", {"example_pl": "Babcia piecze wspaniałe ciasta"}),
    95: (T + "«Opowiadam … o mojej» — калька", {"example_pl": "Opowiem ci o podróży"}),
    161: (T + "«za tym» — лишнее", {"example_pl": "Jestem za"}),
    207: (T + "«pytań do umowy» — предлог", {"example_pl": "Mam jeszcze kilka pytań w sprawie umowy"}),
    336: (T + "«Ona» — лишнее", {"example_pl": "Ma piękną twarz"}),
    355: (T + "«On» — лишнее", {"example_pl": "Ma grypę"}),
    487: (T + "«To jest super» — тяжело", {"example_pl": "To super!"}),
    647: (T + "«On» — лишнее", {"example_pl": "Siedzi obok mnie"}),
    677: (T + "«Ona» — лишнее", {"example_pl": "Robi zakupy online"}),
    757: (T + "«mój tata» — лишнее", {"example_pl": "Od zeszłego roku tata jest emerytem"}),
    784: (T + "«To szkoda» — калька", {"example_pl": "Szkoda"}),
    804: (T + "«od dzisiejszego rana» — книжно", {"example_pl": "Od rana pada śnieg"}),
    814: (T + "«Ona» — лишнее", {"example_pl": "Jest w ciąży"}),
    842: (T + "«On» — лишнее", {"example_pl": "Jedzie na narty"}),
    895: (T + "«Czy» — книжно", {"example_pl": "To krzesło jest wolne?"}),
    904: (T + "«Moja» — лишнее", {"example_pl": "Babcia gotuje najlepszą zupę"}),
    1067: (T + "«Mojemu» — лишнее", {"example_pl": "Synowi wypadł pierwszy ząb"}),
    1129: (T + "«Czy … spotkania» — тяжело", {"example_pl": "Możesz zmienić termin?"}),
}

REPLACE = []

SPLIT_LATER = {}
