"""Вычитка польского, порция p044 (C1), 23.10: лишние местоимения и кальки → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    16564: (T + "«Mój» — лишнее", {"example_pl": "Pradziadek był w czasie wojny dezerterem, długo nikt w rodzinie o tym nie mówił"}),
    16570: (T + "«swoim … swojego» — повтор", {"example_pl": "Najmłodszy namalował na ścianie w pokoju herb ulubionego klubu piłkarskiego"}),
    16571: (T + "«Mój» — лишнее", {"example_pl": "Młodszy brat to prawdziwy węszyciel, po kryjomu czyta mój pamiętnik"}),
    16586: (T + "«Nasz» — лишнее", {"example_pl": "Pies to mały porywacz, każdą skarpetkę ciągnie do swojego posłania"}),
    16593: (T + "«Nasz» — лишнее", {"example_pl": "Chomik tej nocy znowu podjął próbę ucieczki"}),
    16605: (T + "«Mój» — лишнее", {"example_pl": "Mały siostrzeniec to prawdziwy szantażysta: bez lodów nie założy kurtki"}),
    16612: (T + "«nasza» — лишнее", {"example_pl": "Przy podkradaniu ciastek z puszki kotka jest moją wspólniczką"}),
    16988: (T + "«Mój» — лишнее", {"example_pl": "Dziadek nigdy nie miał wielkiego szacunku dla władzy, nawet dla proboszcza"}),
    17248: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez burzę przestrzeń powietrzna nad lotniskiem była zamknięta i przez dwie godziny krążyliśmy nad górami"}),
    17279: (T + "«mój» — лишнее", {"example_pl": "W klubie wioślarskim siostrzeniec jest sternikiem, bo jest najlżejszy"}),
    17289: (T + "«nasza» — лишнее", {"example_pl": "Zimą kotka najchętniej śpi na ciepłej masce samochodu"}),
    17292: (T + "«Nasza» — лишнее", {"example_pl": "Nowa hybryda w mieście jeździ prawie tylko na prądzie"}),
    17602: (T + "«Mój» — лишнее", {"example_pl": "Nowy laptop ma tylko dwa porty i ciągle potrzebuję jakiejś przejściówki"}),
    17633: (T + "«Ponieważ» — книжно", {"example_pl": "Lampki zamokły, więc w Wigilię było zwarcie i jedliśmy przy świecach"}),
    17653: (T + "«Z powodu … nasze» — коряво", {"example_pl": "Przez akcję przywoławczą auto musi w przyszłym tygodniu jechać do warsztatu"}),
    17704: (T + "«mój» — лишнее", {"example_pl": "W biurze laptop automatycznie podłącza się do dużego monitora"}),
    18003: (T + "«nasz» — лишнее", {"example_pl": "Przy każdej detonacji petard w sylwestra pies wczołguje się głębiej pod łóżko"}),
    18022: (T + "«Mój» — лишнее", {"example_pl": "Fryzjer lubi eksperymentować, dlatego mam teraz niebieskie włosy"}),
    18335: (T + "«Mój» — лишнее", {"example_pl": "Ulubiony sweter był w suszarce tylko dziesięć minut i teraz pasuje na córkę"}),
    18350: (T + "«Nasz» — лишнее", {"example_pl": "Kot najbardziej lubi leżeć na wąskim parapecie nad kaloryferem i patrzeć na ptaki"}),
    18356: (T + "«Moja» — лишнее", {"example_pl": "Butelka na wodę jest nieszczelna i teraz wszystkie zeszyty w plecaku są mokre"}),
    18365: (T + "«Na mojej szafce» — калька", {"example_pl": "Na szafce nocnej piętrzy mi się pięć zaczętych książek"}),
    18794: (T + "«mojej» — лишнее", {"example_pl": "Styl życia sąsiadki to dla mnie zagadka: pracuje w nocy, a biega o drugiej po południu"}),
}

REPLACE = []

SPLIT_LATER = {}
