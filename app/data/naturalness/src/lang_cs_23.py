"""Вычитка чешского, порция p023 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    15163: (T + "«Balím» — не тот вид", {"example_cs": "Zabalím dárek do barevného papíru"}),
    15171: (T + "«naléhavě» — книжно", {"example_cs": "Klub nutně hledá dorost"}),
    15239: (T + "«Velmi» — книжно", {"example_cs": "Hrozně se mu stýská po rodném domě"}),
    15242: (T + "«Moje matka» — книжно", {"example_cs": "Máma se po škole stará o děti"}),
    15407: (T + "«velmi» — книжно", {"example_cs": "Děti jsou dneska hrozně divoké"}),
    15453: (T + "«příliš» — книжно", {"example_cs": "Terén je na turistiku moc strmý"}),
    15455: (T + "«velmi» — книжно", {"example_cs": "Je tu hodně útulná atmosféra"}),
    15459: (T + "«svině» — грубо, слово карточки «prasnice»", {"example_cs": "Na statku měla prasnice dvanáct selat"}),
    15467: (T + "«velmi» — книжно", {"example_cs": "Můj králíček je hrozně roztomilý"}),
    15470: (T + "«velmi» — книжно", {"example_cs": "Kmen stromu je hodně silný"}),
    15472: (T + "«chutnají sladce» — калька", {"example_cs": "Banány jsou teď zralé a sladké"}),
    15475: (T + "«Té noci … velmi» — книжно", {"example_cs": "Tu noc byl hodně silný mráz"}),
    15568: (T + "«Do mého pokoje» — калька", {"example_cs": "Do pokoje mi vletěla včela"}),
    15663: (T + "«Můj … svém» — лишнее", {"example_cs": "Křeček každou noc běhá v kolečku"}),
    15679: (T + "«miluje skákání» — калька", {"example_cs": "Můj pudl hrozně rád skáče do vody"}),
    15773: (T + "«svá» — лишнее", {"example_cs": "Páv v zoo hrdě roztahuje pera"}),
    15789: (T + "man — «ty»", {"example_cs": "S trochou štěstí tu z lodi uvidíš delfíny"}),
    15811: (T + "«na mém balkoně» — калька", {"example_cs": "Na balkoně mi nádherně kvete červená orchidej"}),
    15835: (T + "«velmi» — книжно", {"example_cs": "Šimpanz v zoo byl hodně hravý a inteligentní"}),
}

REPLACE = []

SPLIT_LATER = {}
