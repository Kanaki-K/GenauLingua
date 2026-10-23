"""Вычитка чешского, порция p014 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    3066: (T + "«spolu spolupracujeme» — повтор", {"example_cs": "Už roky dobře spolupracujeme"}),
    3078: (T + "«nemají přístup» — калька", {"example_cs": "Dětem je sem vstup zakázán"}),
    6312: (T + "«svoje věci» — не разговорно, как Zeug", {"example_cs": "Ukliď si ty krámy"}),
    6411: (T + "«nestačí do» — коряво", {"example_cs": "Peníze mi do konce měsíce nevystačí"}),
    6477: (T + "«příliš mnoho» — книжно", {"example_cs": "Požadují moc peněz"}),
    6519: (T + "«do krytu pod mostem» — коряво", {"example_cs": "Při krupobití jsme se ukryli pod mostem"}),
    6520: (T + "«pokračujme» — книжно", {"example_cs": "Pojďme prostě pokračovat"}),
    6560: (T + "«Můj mobil je» — калька", {"example_cs": "Mobil mám připojený k wifi"}),
    6590: (T + "meiner Tochter — «mé», не «naší»", {"example_cs": "Se psem je největší přání mé dcery konečně splněné"}),
    6615: (T + "«tohoto» — книжно", {"example_cs": "Jaký má tenhle přístroj účel?"}),
    6622: (T + "«zůstávám» — не тот вид", {"example_cs": "Nejdu do kina, místo toho zůstanu doma"}),
    6638: (T + "«působí radost» — калька", {"example_cs": "Práce mi přináší velkou radost"}),
    6653: (T + "«dar pro hudbu» — порядок", {"example_cs": "Naše malá má pro hudbu dar, každou písničku hned zazpívá"}),
    6665: (T + "«Vytahuji» — не тот вид", {"example_cs": "Vytáhnu auto z garáže"}),
    6669: (T + "«velmi» — книжно", {"example_cs": "To zní moc dobře"}),
    6707: (T + "mächtig — разговорное усиление", {"example_cs": "Je na syna pořádně pyšný"}),
    6710: (T + "«chuť na krámy» — калька", {"example_cs": "Nechce se mi do všech těch krámů"}),
    6714: (T + "«příliš» — книжно", {"example_cs": "To je pro nás možná moc drahé"}),
    6727: (T + "«kvůli klíči» — коряво", {"example_cs": "Prohledal jsem celý byt, abych našel klíč"}),
    6736: (T + "«příliš» — книжно", {"example_cs": "Není to zas tak těžké"}),
}

REPLACE = []

SPLIT_LATER = {}
