"""Вычитка чешского, порция p009 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    1415: (T + "«rychlé … rychlé» — повтор", {"example_cs": "Na cestách často jíme rychlé občerstvení, protože nás to nezdrží"}),
    1508: (T + "«příliš» — книжно", {"example_cs": "Ten pásek je mi moc těsný"}),
    1558: (T + "«Pro integraci pomáhá» — калька", {"example_cs": "Při integraci pomůže jazyk víc než cokoli jiného"}),
    1595: (T + "«Klikám» — не тот вид", {"example_cs": "Kliknu na odkaz"}),
    1599: (T + "«své» — лишнее", {"example_cs": "Nech si ty komentáře!"}),
    1611: (T + "«Pošli … pošlu» — повтор", {"example_cs": "Pošli mi bankovní spojení a převedu ti peníze za lístek na koncert"}),
    1661: (T + "«Mažu» — не тот вид", {"example_cs": "Smažu starý soubor"}),
    1664: (T + "«úplnou výpověď, bez mezer» — коряво", {"example_cs": "Policie od něj chce výpověď o celém večeru bez mezer"}),
    1680: (T + "«dělám meditace» — калька", {"example_cs": "Každé ráno si dávám deset minut meditace"}),
    1710: (T + "«okolí» → слово карточки «sousedství»", {"example_cs": "V našem sousedství se všichni znají"}),
}

REPLACE = []

SPLIT_LATER = {}
