"""Вычитка польского, порция p009 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    1450: (T + "«mój» — лишнее", {"example_pl": "Kiedy pada, pies nie chce iść na spacer"}),
    1462: (T + "«mój» — лишнее", {"example_pl": "W przeciwieństwie do mnie brat lubi wcześnie wstawać"}),
    1464: (T + "«On jest» — тяжело", {"example_pl": "To słynny skrzypek"}),
    1471: (T + "«To jest» — тяжело", {"example_pl": "Genialny pomysł!"}),
    1495: (T + "«Czy» — книжно", {"example_pl": "To prawdziwe złoto?"}),
    1506: (T + "«Mój» — лишнее", {"example_pl": "Syn chodzi do szkoły podstawowej"}),
    1511: (T + "«Moja» — лишнее", {"example_pl": "Siostra poświęca więcej czasu na pielęgnację włosów niż ja na śniadanie"}),
    1512: (T + "«moje oceny nie były» — калька", {"example_pl": "W pierwszym półroczu miałem nie najlepsze oceny"}),
    1515: (T + "«Mój» — лишнее", {"example_pl": "Mąż jest zdolny manualnie, sam wszystko naprawia w domu"}),
    1555: (T + "«mój» — лишнее", {"example_pl": "Jako informatyk brat prawie zawsze może pracować z domu"}),
    1566: (T + "«Ta … gdzieś tam» — коряво", {"example_pl": "Książka leży gdzieś tutaj"}),
    1571: (T + "«Obok studiów» — калька", {"example_pl": "W trakcie studiów dwa razy w tygodniu dorabiam w kinie"}),
    1578: (T + "«Ona» — лишнее", {"example_pl": "Ma wykształcenie handlowe"}),
    1582: (T + "«Czy możesz, proszę» — книжно", {"example_pl": "Możesz zaznaczyć błędy?"}),
    1588: (T + "«On» — лишнее", {"example_pl": "Skarży się na bóle"}),
    1625: (T + "«Czy» — книжно", {"example_pl": "Mogę zapłacić kartą kredytową?"}),
    1640: (T + "«Mój» — лишнее", {"example_pl": "Laptop znowu mi się zawiesił"}),
    1647: (T + "«On odbywa» — книжно", {"example_pl": "Uczy się zawodu elektryka"}),
    1680: (T + "«Każdego ranka» — книжно", {"example_pl": "Codziennie rano robię dziesięć minut medytacji"}),
    1692: (T + "«Mój» — лишнее", {"example_pl": "Współlokator nigdy nie zmywa"}),
    1698: (T + "«Pana» — регистр", {"example_pl": "Mam dla pana wiadomość"}),
    1702: (T + "«Moja» — лишнее", {"example_pl": "Kuzynka chce zostać projektantką mody i już szyje sobie sukienki"}),
    1724: (T + "«Mój» — лишнее", {"example_pl": "Bratanek ma pięć lat"}),
    1728: (T + "«Moja» — лишнее", {"example_pl": "Siostrzenica studiuje w Berlinie"}),
    1735: (T + "«w naszym mieście» — калька", {"example_pl": "W weekendy u nas w mieście autobusem jeździ się za darmo"}),
    1740: (T + "«mój» — лишнее", {"example_pl": "Po liceum syn chce wyjechać na rok za granicę"}),
}

REPLACE = []

SPLIT_LATER = {}
