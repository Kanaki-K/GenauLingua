"""Вычитка чешского, порция p025 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    17159: (T + "«Převážíme» — не тот вид", {"example_cs": "Nábytek převezeme náklaďákem"}),
    17217: (T + "«beru» — не тот вид", {"example_cs": "Jako suvenýr si vezmu jen magnetku"}),
    17255: (T + "«auto potřebuje naftu» — калька", {"example_cs": "Moje auto jezdí na naftu, ne na benzín"}),
    17294: (T + "«svém» — лишнее", {"example_cs": "Jezdí do práce na starém mopedu"}),
    17368: (T + "«Ukládáme» — не тот вид", {"example_cs": "Uložíme kufry do auta"}),
    17375: (T + "«do myčky aut» — повтор", {"example_cs": "S autem jezdím pravidelně do myčky"}),
    17511: (T + "«příliš» — книжно", {"example_cs": "Kabel k televizi je moc krátký"}),
    17512: (T + "«na mé kreditní kartě» — калька", {"example_cs": "Na kreditce mi nefunguje čip"}),
    17513: (T + "«tomuto» — книжно", {"example_cs": "Nemám přístup k tomuhle souboru"}),
    17514: (T + "«příliš» — книжно", {"example_cs": "Reproduktory hrají moc nahlas"}),
    17523: (T + "«Můj profil» — калька", {"example_cs": "Profil na sociálních sítích mám soukromý"}),
    17524: (T + "«Sekám» — не тот вид", {"example_cs": "Nasekám cibuli najemno"}),
    17530: (T + "«Baterie v mé baterce» — калька", {"example_cs": "V baterce mám vybitou baterii"}),
    17549: (T + "«Pracuji» — книжно", {"example_cs": "Pracuju se dvěma monitory"}),
    17554: (T + "«disk mého počítače» — калька", {"example_cs": "V počítači mám plný pevný disk"}),
    17576: (T + "пассив — книжно", {"example_cs": "Rozbušku bomby zneškodnili"}),
    17590: (T + "«mnoho» — книжно", {"example_cs": "Platforma nabízí spoustu nových funkcí"}),
    17690: (T + "«velmi» — книжно", {"example_cs": "Píst v motoru se pohybuje hrozně rychle nahoru a dolů"}),
    17728: (T + "«Tento» — книжно", {"example_cs": "Tenhle měsíc je účet za telefon dvakrát vyšší než obvykle"}),
    17729: (T + "«Tento … běží» — калька", {"example_cs": "Tenhle televizní pořad dávají každou neděli"}),
    17784: (T + "«tomto … velmi» — книжно", {"example_cs": "V tomhle oboru je konkurence hodně silná"}),
    17805: (T + "«tomto … velmi velká» — книжно", {"example_cs": "Po tomhle výrobku je obrovská poptávka"}),
    17921: (T + "«Udělejme» — книжно", {"example_cs": "Pojďme udělat malý pokus"}),
    17928: (T + "«Tento» — книжно", {"example_cs": "Tenhle druh se už vyskytuje jen vzácně"}),
    17930: (T + "«Tento … vyrobený» — книжно", {"example_cs": "Tenhle stůl je z kovu"}),
    17946: (T + "«potřebuji» — книжно", {"example_cs": "Na koláč potřebuju tři sta gramů mouky"}),
    18168: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju měkčí polštář"}),
    18177: (T + "«Můj byt je» — калька", {"example_cs": "Bydlím ve třetím patře"}),
    18187: (T + "«velmi přátelští» — книжно", {"example_cs": "Obyvatelé domu jsou hodně milí"}),
    18190: (T + "«Zatloukám» — не тот вид", {"example_cs": "Zatluču hřebík do zdi"}),
    18200: (T + "«obývacího pokoje» — книжно", {"example_cs": "Koupil jsem nové závěsy do obýváku"}),
}

REPLACE = []

SPLIT_LATER = {}
