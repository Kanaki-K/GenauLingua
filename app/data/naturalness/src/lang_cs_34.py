"""Вычитка чешского, порция p034 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    14257: (T + "«Moje děti» — лишнее", {"example_cs": "Děti už vůbec nevědí, jak se používá telefonní automat, je to pro ně muzejní exponát"}),
    14280: (T + "«své» — лишнее", {"example_cs": "Babička mi diktuje recepty, protože už nedokáže dobře psát"}),
    14463: (T + "«svůj» — лишнее", {"example_cs": "Fotbalista mi dal autogram"}),
    14467: (T + "«Moje prateta» — книжно", {"example_cs": "Prateta byla jeptiška a pracovala v nemocnici"}),
    14491: (T + "«Můj bratr» — книжно", {"example_cs": "Brácha není dobrý tanečník, na svatbách vždycky sedí u stolu"}),
    14494: (T + "«Moji sousedé» — книжно", {"example_cs": "Sousedé jsou věřící křesťané a každou neděli chodí do kostela"}),
    14498: (T + "«Můj děda» — книжно", {"example_cs": "Děda celý život psal poezii, ale nikdy nic nevydal"}),
    14508: (T + "«mnoho» — книжно", {"example_cs": "Mýtus o Atlantidě fascinuje spoustu lidí"}),
    14519: (T + "«Mnoho» — книжно", {"example_cs": "Spousta rodičů neví, jak brzy dnes děti vidí na internetu porno"}),
    14535: (T + "«Mnoho» — книжно", {"example_cs": "Spousta lidí sní o nesmrtelnosti"}),
    14536: (T + "«této» — книжно", {"example_cs": "To téma je v téhle rodině tabu"}),
    14538: (T + "«Tato» — книжно", {"example_cs": "Ta metafora přirovnává život k cestě"}),
    14541: (T + "«Moje věřící rodina … mnoho» — калька", {"example_cs": "Rodina je věřící a během roku slaví spoustu svátků"}),
    14558: (T + "«svého» — лишнее", {"example_cs": "Na každou zkoušku si dcera bere malého plyšového medvídka jako talisman"}),
    14649: (T + "«V mém snubním prstenu» — калька", {"example_cs": "Ve snubním prstenu mám zevnitř nápis s datem naší svatby"}),
    14664: (T + "«Můj … mou … příliš» — книжно", {"example_cs": "Učitel němčiny považuje moji interpretaci básně za moc volnou"}),
    14775: (T + "«moje rodina» — «naše»", {"example_cs": "U narozeninových písní zná naše rodina vždycky jen první sloku, pak všichni broukají"}),
    15042: (T + "«velmi» — книжно", {"example_cs": "Pohřeb byl pro rodinu hodně emotivní"}),
    15043: (T + "«Můj snoubenec a já» — калька", {"example_cs": "Se snoubencem se příští měsíc bereme"}),
    15045: (T + "«Moje … velmi» — калька", {"example_cs": "Naše adoptované dítě je u nás moc šťastné"}),
    15058: (T + "«jeho pes jeho» — повтор", {"example_cs": "Od té doby, co je děda sám, je pes jeho nejvěrnější společník"}),
    15080: (T + "«své» — лишнее", {"example_cs": "Vychovává děti sama"}),
    15091: (T + "«velmi» — книжно", {"example_cs": "Mámě je šedesát, ale pořád vypadá hodně mladistvě"}),
    15096: (T + "«Můj bratr» — книжно", {"example_cs": "Brácha mi šel za svědka na svatbě"}),
    15098: (T + "«Moje tchyně» — книжно", {"example_cs": "Tchyně k nám zítra přijede na návštěvu"}),
}

REPLACE = []

SPLIT_LATER = {}
