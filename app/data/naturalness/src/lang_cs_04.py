"""Вычитка чешского, порция p004 (A2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    95: (T + "«Vyprávím ti» — не тот вид", {"example_cs": "Povyprávím ti o své cestě"}),
    222: (T + "«Parkoviště je těsné» — смысл", {"example_cs": "To parkovací místo je dost úzké"}),
    549: (T + "«poslední raz» — неграмотно", {"example_cs": "To bylo naposledy"}),
    679: (T + "«listy» — не о листве", {"example_cs": "Na podzim je listí žluté a oranžové"}),
    686: (T + "«v zimě velká zima» — повтор", {"example_cs": "Na východě bývají v zimě velké mrazy"}),
    789: (T + "«daruješ» — книжно", {"example_cs": "Co dáš mámě k narozeninám?"}),
    1011: (T + "«toaleta» — книжно, и слово карточки WC", {"example_cs": "Kde je tady WC?"}),
}

REPLACE = []

SPLIT_LATER = {}
