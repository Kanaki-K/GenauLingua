"""Вычитка чешского, порция p033 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    12887: (T + "«kouří příliš mnoho trávy» — калька", {"example_cs": "Brácha moc hulí a dělá mi to starosti"}),
    12947: (T + "слово карточки «zdravý jako řípa»", {"example_cs": "Dítě je zdravé jako řípa a plné energie"}),
    13108: (T + "«mé dcery» — тяжело", {"example_cs": "V dceřině nové učebnici biologie obrázek konečně správně ukazuje i klitoris"}),
    13516: (T + "«Moje žena» — книжно", {"example_cs": "Žena se o tom nesmí dozvědět, je to překvapení"}),
    13544: (T + "«Můj pes» — лишнее", {"example_cs": "Pes se bojí bouřek, kvůli němu zůstáváme na Silvestra doma"}),
    13545: (T + "«jsou dva a půl» — без «roku» коряво", {"example_cs": "Dceři jsou teď dva a půl roku a na všechno říká ne"}),
    13552: (T + "«potřebuji» — книжно", {"example_cs": "Na cestu potřebuju hodinu a půl"}),
    13666: (T + "«Rukávy mého svetru» — калька", {"example_cs": "Svetr má moc dlouhé rukávy"}),
    13679: (T + "«je možné prát» — канцелярит", {"example_cs": "Hedvábná halenka se smí prát jen v ruce ve studené vodě"}),
    13682: (T + "«Oblékám» — не тот вид", {"example_cs": "Obléknu si teplý svetr, protože je zima"}),
    13690: (T + "«na mých botách … příliš» — калька", {"example_cs": "Ty boty mají moc vysoké podpatky"}),
    13694: (T + "«Můj nový účes» — калька", {"example_cs": "Nový účes vypadá fakt dobře"}),
    14016: (T + "«stavím» — не тот вид", {"example_cs": "Sklenice cinkne, když ji postavím na stůl"}),
    14019: (T + "«velmi nečitelný» — книжно", {"example_cs": "Jeho rukopis se skoro nedá přečíst"}),
    14058: (T + "«tento» — книжно", {"example_cs": "Šéf tenhle týden není k zastižení"}),
    14236: (T + "«příliš» — книжно", {"example_cs": "Při odhalení nového pomníku měl starosta strašně dlouhý projev"}),
}

REPLACE = []

SPLIT_LATER = {}
