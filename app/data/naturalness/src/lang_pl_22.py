"""Вычитка польского, порция p022 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    14008: (T + "«Jego pismo jest» — калька", {"example_pl": "Ma bardzo staranne pismo"}),
    14161: (T + "«Czy» — книжно", {"example_pl": "Mogę odwołać wizytę telefonicznie?"}),
    14231: (T + "«Moja wymowa jest» — калька", {"example_pl": "Mam coraz lepszą wymowę po angielsku"}),
    14246: (T + "«do mojej» — калька", {"example_pl": "Mail nie dotarł mi do skrzynki pocztowej"}),
    14276: (T + "«swoje» — лишнее", {"example_pl": "Zapisałem kontakty w książce adresowej"}),
    14317: (T + "порядок слов", {"example_pl": "Cały czas pisze do mnie esemesy"}),
    14376: (T + "«mojego» — лишнее", {"example_pl": "Niedziela jest dla taty święta, wtedy się nie pracuje"}),
    14377: (T + "«Mój» — лишнее", {"example_pl": "Syn na karnawał koniecznie chce przebrać się za księcia"}),
    14415: (T + "«Moja» — порядок", {"example_pl": "Na tym cmentarzu leży babcia"}),
    14430: (T + "«moja» — лишнее", {"example_pl": "Obraz nad kanapą namalowała babcia"}),
    14435: (T + "«Mój» — лишнее", {"example_pl": "Wujek jest znanym pisarzem"}),
    14442: (T + "«Każdego wieczoru» — книжно", {"example_pl": "Co wieczór odmawia modlitwę"}),
    14455: (T + "«moich» — лишнее", {"example_pl": "Kupię ci pamiątkę z wakacji"}),
    14502: (T + "«Moja» — лишнее", {"example_pl": "Córka lubi tańczyć balet"}),
    14691: (T + "«On» — лишнее", {"example_pl": "Gra na harmonijce ustnej w parku"}),
    14737: (T + "«Jaki jest twój» — калька", {"example_pl": "Jaki masz znak zodiaku – Baran czy Byk?"}),
    14745: (T + "«On» — лишнее", {"example_pl": "Gra na puzonie w zespole jazzowym"}),
    14799: (T + "«Moja» — лишнее", {"example_pl": "Córka od roku uczy się grać na klarnecie"}),
    14806: (T + "«u mojej» — лишнее", {"example_pl": "W kuchni u babci wisi krucyfiks"}),
    14811: (T + "«kolorują kolorami» — повтор", {"example_pl": "Dzieci kolorują obrazki"}),
    14847: (T + "«Mój» — лишнее", {"example_pl": "Brat co wieczór ćwiczy na saksofonie, sąsiedzi mają dość"}),
    14908: (T + "«ukochany» — книжно", {"example_pl": "Chodź tu, kochanie"}),
    14934: (T + "«swój» — лишнее", {"example_pl": "Rusz tyłek"}),
    14959: (T + "«Mój» — лишнее", {"example_pl": "Brat jest gejem"}),
    14974: (T + "«Ona» — лишнее", {"example_pl": "Ma szczupłą figurę"}),
    14976: (T + "«i jest» — повтор", {"example_pl": "To prawdziwy dżentelmen, bardzo uprzejmy"}),
    14991: (T + "«Moja» — лишнее", {"example_pl": "Sąsiadka jest wdową"}),
    14998: (T + "«jest twój pies» — калька", {"example_pl": "Jakiej rasy masz psa?"}),
    15006: (T + "«wasza wzajemna relacja» — книжно", {"example_pl": "Jakie macie ze sobą relacje?"}),
    15020: (T + "«Mój» — лишнее", {"example_pl": "Szwagier jest lekarzem"}),
    15021: (T + "«Moi» — лишнее", {"example_pl": "Rodzice wychowali mnie surowo"}),
    15030: (T + "«swoje» — лишнее", {"example_pl": "Matka karmi dziecko piersią w poczekalni"}),
    15089: (T + "«Ona» — лишнее", {"example_pl": "Ma w mieście wielu wielbicieli"}),
    15110: (T + "«Ona jest» — тяжело", {"example_pl": "To urodzona nauczycielka"}),
}

REPLACE = []

SPLIT_LATER = {}
