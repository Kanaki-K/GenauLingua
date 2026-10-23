"""Вычитка чешского, порция p022 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    14008: (T + "«velmi» — книжно", {"example_cs": "Má hodně úhledné písmo"}),
    14013: (T + "«svou» — лишнее", {"example_cs": "Autor brzy vydá novou knihu"}),
    14041: (T + "«vzrušující novinku» — калька", {"example_cs": "Mám pro tebe skvělou novinku"}),
    14100: (T + "«spot běží» — калька", {"example_cs": "Ten spot dávají každý večer před zprávami"}),
    14213: (T + "«raději» — книжно", {"example_cs": "Můžeme si tykat, nebo si radši budeme vykat?"}),
    14231: (T + "«Moje výslovnost» — калька", {"example_cs": "Výslovnost v angličtině se mi pořád zlepšuje"}),
    14239: (T + "«svůj» — лишнее", {"example_cs": "Dostal jsem výzvu, abych zaplatil příspěvek"}),
    14276: (T + "«Své» — лишнее", {"example_cs": "Kontakty jsem si uložil do adresáře"}),
    14376: (T + "«pro mého tátu» — тяжело", {"example_cs": "Pro tátu je neděle svatá, to se nepracuje"}),
    14377: (T + "«bezpodmínečně» — книжно", {"example_cs": "Syn chce na masopust za každou cenu jít za prince"}),
    14403: (T + "«Právě … svůj» — книжно", {"example_cs": "Zrovna píše první román"}),
    14432: (T + "«tomto» — книжно", {"example_cs": "V tomhle hororu bojuje s podivnými stvořeními"}),
    14433: (T + "«Tento» — книжно", {"example_cs": "Tenhle film má hodně akce"}),
    14446: (T + "«velmi» — книжно", {"example_cs": "Obřad byl moc pěkný"}),
    14450: (T + "«velmi» — книжно", {"example_cs": "Náš pastor je ve vesnici hodně oblíbený"}),
    14452: (T + "«mnoho» — книжно", {"example_cs": "V mytologii je spousta bohyň"}),
    14461: (T + "«tohoto» — книжно", {"example_cs": "Režii toho filmu měl Tarantino"}),
    14466: (T + "«velmi» — книжно", {"example_cs": "Vypravěč toho příběhu je hodně talentovaný"}),
    14482: (T + "«velmi» — книжно", {"example_cs": "Poslední číslo časopisu bylo hodně zajímavé"}),
    14485: (T + "«Miluji» — книжно", {"example_cs": "Miluju německou literaturu"}),
    14500: (T + "«daroval» — книжно", {"example_cs": "Syn mi dal kresbu"}),
    14568: (T + "«velmi» — книжно", {"example_cs": "Ztvárnění hlavní postavy bylo hodně přesvědčivé"}),
    14738: (T + "«velmi» — книжно", {"example_cs": "Hraje moc dobře na banjo a často vystupuje"}),
    14936: (T + "«Dříve» — книжно", {"example_cs": "Dřív se mladým ženám říkalo slečno"}),
    14939: (T + "«Dala mu polibek» — книжно", {"example_cs": "Dala mu pusu"}),
    14953: (T + "«přátelství je velmi důležité» — книжно", {"example_cs": "Na našem přátelství mi hodně záleží"}),
    14959: (T + "«Můj bratr» — книжно", {"example_cs": "Brácha je gay"}),
    14967: (T + "«svou» — лишнее", {"example_cs": "Má poměr s kolegyní"}),
    14976: (T + "«velmi» — книжно", {"example_cs": "Je to skutečný gentleman a hodně zdvořilý"}),
    14977: (T + "«V mém mládí» — калька", {"example_cs": "Za mého mládí bylo všechno jinak"}),
    15011: (T + "«velmi» — книжно", {"example_cs": "Rozchod byl pro oba hodně těžký"}),
    15022: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju doprovod k lékaři"}),
    15024: (T + "«Svůj … tají» — книжно", {"example_cs": "Soukromý život si přísně hlídá"}),
    15025: (T + "«s mým starým přítelem» — тяжело", {"example_cs": "Setkání se starým kamarádem bylo opravdu krásné"}),
    15030: (T + "«své dítě» — книжно", {"example_cs": "Matka kojí miminko v čekárně"}),
    15089: (T + "«mnoho» — книжно", {"example_cs": "Má ve městě spoustu ctitelů"}),
}

REPLACE = []

SPLIT_LATER = {}
