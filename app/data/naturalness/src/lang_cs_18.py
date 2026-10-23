"""Вычитка чешского, порция p018 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    10021: (T + "«Pošli … pošlu» — повтор", {"example_cs": "Pošli mi svůj IBAN a převedu ti peníze za lístek na koncert"}),
    10076: (T + "mit den Händen — потеряно", {"example_cs": "Má hodně šikovné ruce"}),
    10107: (T + "«velmi» — книжно", {"example_cs": "Jsem hodně překvapený"}),
    10138: (T + "«velmi» — книжно", {"example_cs": "Jsem ti moc vděčný"}),
    10179: (T + "«svou» — лишнее", {"example_cs": "Je žárlivá na sestru"}),
    10186: (T + "«velmi» — книжно", {"example_cs": "Před zkouškou jsem hrozně nervózní"}),
    10195: (T + "«svou» — лишнее", {"example_cs": "Nechci riskovat práci"}),
    10218: (T + "«lépe» — книжно", {"example_cs": "Máš se chovat líp"}),
    10220: (T + "«Dítě … velmi» — книжно", {"example_cs": "Malý je dneska moc hodný"}),
    10240: (T + "«svůj» — лишнее", {"example_cs": "Rád bych si splnil sen"}),
    10243: (T + "«Obětuji svůj» — книжно", {"example_cs": "Obětuju práci všechen volný čas"}),
    10246: (T + "«velmi» — книжно", {"example_cs": "Jeho reakce byla hodně pozitivní"}),
    10280: (T + "«za své chování» — калька", {"example_cs": "Měl by ses stydět za to, jak se chováš"}),
    10298: (T + "«vizi svého života» — калька", {"example_cs": "Mám jasnou vizi, co chci v životě dělat"}),
    10302: (T + "«stále» — книжно", {"example_cs": "Rodina je pořád v hlubokém smutku"}),
    10308: (T + "«velmi» — книжно", {"example_cs": "Moje dcera je hodně plachá"}),
    10318: (T + "«Rozdělme» — книжно", {"example_cs": "Rozdělíme dort spravedlivě"}),
    10324: (T + "«Jakou máš starost» — калька", {"example_cs": "Copak máš za starost?"}),
    10327: (T + "«svou» — лишнее", {"example_cs": "Prosí o odpuštění za tu velkou chybu"}),
    10348: (T + "«opravdu velmi» — книжно", {"example_cs": "Je opravdu moc okouzlující"}),
    10365: (T + "«velmi» — книжно", {"example_cs": "Je to hodně zapálená učitelka"}),
    10374: (T + "«svou» — лишнее", {"example_cs": "Přestaň obtěžovat sestru"}),
    10376: (T + "«ovlivňuje» — не тот вид", {"example_cs": "To ovlivní moje rozhodnutí"}),
    10383: (T + "«Velmi lituji» — книжно", {"example_cs": "Hrozně lituju, že jsem nemohl přijít"}),
    10389: (T + "«velmi» — книжно", {"example_cs": "Tvůj výkon na mě hodně zapůsobil"}),
    10405: (T + "«velmi» — книжно", {"example_cs": "Pracuje hodně soustředěně"}),
    10409: (T + "«kvůli mé nové práci» — калька", {"example_cs": "Je závistivá, že mám novou práci"}),
    10415: (T + "«ubohým způsobem» — тяжело", {"example_cs": "Choval se uboze"}),
    10417: (T + "«Můj otec je můj» — повтор", {"example_cs": "Táta je můj velký vzor"}),
    10418: (T + "«od svých problémů» — тяжело", {"example_cs": "Potřebuju trochu rozptýlení od problémů"}),
    10427: (T + "«svou vděčnost» — калька", {"example_cs": "Nevím, jak ti dát najevo vděčnost"}),
    10430: (T + "«mnoho» — книжно", {"example_cs": "Žárlivost ničí spoustu vztahů"}),
}

REPLACE = []

SPLIT_LATER = {}
