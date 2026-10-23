"""Вычитка польского, порция p039 (C1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    7762: (T + "«w najbardziej przednim rzędzie» — коряво", {"example_pl": "W kinie córka zawsze chce siedzieć w przednich rzędach, a potem boli ją kark"}),
    7763: (T + "«nasz» — лишнее", {"example_pl": "Po myjni stary samochód znowu lśni jak nowy, do pierwszego deszczu"}),
    7769: (T + "«Nasz» — лишнее", {"example_pl": "Pies nas przechytrzył: szczeka przy drzwiach, a kiedy idziemy zobaczyć, kradnie chleb ze stołu"}),
    7805: (T + "«częściowo … częściowo» — книжно", {"example_pl": "Dzieci w klasie syna mają po części sześć, po części już osiem lat"}),
    7824: (T + "«moich» — лишнее", {"example_pl": "We wsi rodziców widać przemianę: tam, gdzie dawniej był rzeźnik, jest teraz wegańska kawiarnia"}),
    7841: (T + "«nasz … swoim» — лишнее", {"example_pl": "Odkąd jest dziecko, pies nie jest już w centrum uwagi i dąsa się w koszyku"}),
    7844: (T + "«Nasz» — лишнее", {"example_pl": "Kot jest bardzo wymagający w jedzeniu i je tylko jeden rodzaj karmy z łososiem"}),
    7845: (T + "«Moja» — лишнее", {"example_pl": "Pierwsza próba z ciastem drożdżowym była zupełnie spaprana, ciasto po prostu nie wyrosło"}),
    7870: (T + "«swojego» — лишнее", {"example_pl": "Syn jest kopią dziadka, nawet kicha z tym samym dźwiękiem"}),
    7895: (T + "«Nasza» — лишнее", {"example_pl": "Mała wkłada wszystko do szczeliny odtwarzacza DVD, wczoraj był to plasterek sera"}),
    7906: (T + "«Nasza» — лишнее", {"example_pl": "Nowa pediatra jest młoda i dynamiczna i wszystko tłumaczy dzieciom przy pomocy pluszaka"}),
    7910: (T + "«nasz» — лишнее", {"example_pl": "Przez twardość wody czajnik ciągle zarasta tu kamieniem"}),
    7928: (T + "«jego … naszego» — коряво", {"example_pl": "Przy takiej szybkości nikt w parku nie złapie psa"}),
    7940: (T + "«nasz» — лишнее", {"example_pl": "Na dźwięk psiego szczekania kot od razu chowa się pod kanapę"}),
    7953: (T + "«Moja łacina» — калька", {"example_pl": "Łacinę ze szkoły mam całkiem zardzewiałą"}),
    7960: (T + "«Nasze» — лишнее", {"example_pl": "Mieszkanie niestety nie nadaje się dla dużego psa"}),
    7965: (T + "«Mój … spóźnia się dziesięć» — коряво", {"example_pl": "Kolega stale spóźnia się o dziesięć minut"}),
    7967: (T + "порядок слов", {"example_pl": "Przynieś, proszę, te krzesła tutaj"}),
    7987: (T + "«mój dzień pracy jest» — калька", {"example_pl": "Przez masę spotkań dzień pracy mam kompletnie poszatkowany"}),
    7999: (T + "«Z powodu … ruch pociągów» — книжно", {"example_pl": "Przez roboty w weekend pociągi jeżdżą w ograniczonym zakresie"}),
    8009: (T + "«Mój» — лишнее", {"example_pl": "Wniosek wrócił do mnie, bo był niekompletny"}),
    8051: (T + "«Nasza … imituje» — книжно", {"example_pl": "Papuga perfekcyjnie imituje teraz dzwonek mojego telefonu"}),
    8617: (T + "«mojej» — лишнее", {"example_pl": "Sernik cioci nie ma sobie równych"}),
    8941: (T + "«swojego» — лишнее", {"example_pl": "Na karnawał syn przebiera się za łowcę nagród z ulubionego serialu"}),
    8992: (T + "«Moja» — лишнее", {"example_pl": "Ciocia jest porucznikiem marynarki i przyjdzie na ślub syna w mundurze"}),
    8993: (T + "«Moja» — лишнее", {"example_pl": "Dziesięcioletnia córka jest teraz znawczynią ptaków i poprawia nawet przewodnika w muzeum"}),
    9004: (T + "«Ponieważ» — книжно", {"example_pl": "Zmywarka się zepsuła, więc przez tydzień zmywamy ręcznie, a dzieci kłócą się o wycieranie"}),
    9008: (T + "«swoją» — лишнее", {"example_pl": "Po trzydziestu latach jako trener drużyny dziecięcej tata ogłosił rezygnację"}),
    9012: (T + "«Mój» — лишнее", {"example_pl": "Dziadek był tylko starszym szeregowym, ale opowiada historie, jakby dowodził całą armią"}),
    9026: (T + "«z mojego biura» — лишнее", {"example_pl": "W dzień wypłaty koledzy z biura zawsze idą razem na kebaba"}),
    9046: (T + "«mojej» — лишнее", {"example_pl": "Dziadek przyjaciółki był bankierem w Zurychu i nauczył ją zapisywać każdy cent"}),
    9056: (T + "«operatora dźwigu» — повтор", {"example_pl": "Przed naszym oknem od miesięcy stoi ogromny dźwig, a syn co rano macha do operatora"}),
    9077: (T + "«swoją» — лишнее", {"example_pl": "Na karnawał syn przebiera się za policjanta i z dumą pokazuje każdemu gościowi tekturową odznakę"}),
}

REPLACE = []

SPLIT_LATER = {}
