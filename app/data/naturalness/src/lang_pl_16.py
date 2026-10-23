"""Вычитка польского, порция p016 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    7786: (T + "«pozostać neutralny» — падеж", {"example_pl": "Staram się być neutralny"}),
    7888: (T + "«Mój» — лишнее", {"example_pl": "Rower był przypięty łańcuchem, a i tak zniknął"}),
    7951: (T + "«swój» — лишнее", {"example_pl": "Chcę oddać stary rower"}),
    7959: (T + "«Rdza jest coraz gorsza» — калька", {"example_pl": "Rdzy na samochodzie jest coraz więcej"}),
    8075: (T + "«liczy» — книжно", {"example_pl": "Nasze miasto ma sto tysięcy mieszkańców"}),
    8098: (T + "«zaczyna grę» — лишнее", {"example_pl": "Losujemy, kto zaczyna"}),
    8146: (T + "«oni» — лишнее", {"example_pl": "Myślę, że po prostu do siebie nie pasują"}),
    8189: (T + "«Mój» — лишнее", {"example_pl": "Kolega ma egipskie korzenie"}),
    8220: (T + "«Czy» — книжно", {"example_pl": "Te spodnie da się połączyć z czerwonym swetrem?"}),
    8285: (T + "«Mój …, pracując» — книжно", {"example_pl": "Dziadek przy pracy w ogrodzie zawsze sobie pogwizduje"}),
    8404: (T + "«Moja» — лишнее", {"example_pl": "Siostra uwielbia wszystko, co retro, zwłaszcza stare meble"}),
    8554: (T + "«Nasz» — лишнее", {"example_pl": "Syn szybko zintegrował się z nową klasą"}),
    8586: (T + "«Nasz … moje» — лишнее", {"example_pl": "Kot co rano atakuje mi stopy"}),
    8589: (T + "«Mój» — лишнее", {"example_pl": "Syn gra w drużynie baseballowej jako łapacz i nosi ogromną maskę"}),
    8595: (T + "«na zewnątrz» — книжно", {"example_pl": "Dzieci chcą pobiegać na dworze"}),
    8744: (T + "«Mój» — лишнее", {"example_pl": "Dziadek był kiedyś majorem w wojsku"}),
    8758: (T + "«Moja kariera jest ważna» — калька", {"example_pl": "Zależy mi na karierze"}),
    8766: (T + "«On jest» — тяжело", {"example_pl": "To przywódca naszej grupy"}),
    8768: (T + "«Mój» — лишнее", {"example_pl": "Tata najbardziej lubi czytać powieści o agentach i szpiegach"}),
    8778: (T + "«Mój» — лишнее", {"example_pl": "Komputer stoi na biurku"}),
    8787: (T + "«On» — лишнее", {"example_pl": "Pracuje w fabryce"}),
    8801: (T + "«On jest» — тяжело", {"example_pl": "To prawdziwy wojownik, nigdy się nie poddaje"}),
    8806: (T + "«Mój» — лишнее", {"example_pl": "Brat służy w marynarce wojennej"}),
    8807: (T + "«On jest» — тяжело", {"example_pl": "To prawdziwy zawodowiec"}),
    8808: (T + "«Moja pensja przychodzi» — калька", {"example_pl": "Pensję dostaję zawsze na koniec miesiąca"}),
    8814: (T + "«Moja zmiana» — калька", {"example_pl": "Zmianę zaczynam o szóstej"}),
    8816: (T + "«Mój» — лишнее", {"example_pl": "Doradca polecił mi tę inwestycję"}),
    8821: (T + "«On jest» — лишнее", {"example_pl": "Jest ekspertem od kuchni włoskiej"}),
    8823: (T + "«Moja» — лишнее", {"example_pl": "Adwokatka powiedziała, żebym nic nie podpisywał"}),
    8828: (T + "«Moja» — лишнее", {"example_pl": "Córka bawi się w detektywa i szuka śladów z lupą"}),
    8844: (T + "«Mój» — лишнее", {"example_pl": "Szef zaproponował mi awans"}),
}

REPLACE = []

SPLIT_LATER = {}
