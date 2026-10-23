"""Вычитка чешского, порция p032 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    11748: (T + "«Moje babička» — книжно", {"example_cs": "Babička peče každý rok na Vánoce výborné cukroví"}),
    11756: (T + "«mnoho» — книжно", {"example_cs": "Za války musela spousta lidí hladovět"}),
    11762: (T + "«příliš» — книжно", {"example_cs": "Maso bylo moc tuhé na jídlo"}),
    11785: (T + "«nesnáší» — двусмысленно", {"example_cs": "Sestra nemůže jíst pšenici, proto peču chleba ze špaldy"}),
    11979: (T + "«Můj lékař» — книжно", {"example_cs": "Lékař říká, že se má jíst pomalu, protože pocit sytosti přijde až po dvaceti minutách"}),
    12184: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju si dát pauzu od stresu"}),
    12227: (T + "«když se stalo» — смысл", {"example_cs": "Finále jsme sledovali s celou ulicí a nakonec bylo Německo mistrem světa"}),
    12350: (T + "«Ve hře mého syna» — тяжело", {"example_cs": "V synově hře je trpaslík nejsilnější v boji zblízka, z dálky nic netrefí"}),
    12611: (T + "«nadechuji» — книжно", {"example_cs": "Zhluboka se nadechnu"}),
    12612: (T + "«Můj táta» — лишнее", {"example_cs": "Táta má problémy s ledvinou a musí hodně pít"}),
    12621: (T + "«Můj bratr» — книжно", {"example_cs": "Brácha je ještě dva týdny v karanténě"}),
    12645: (T + "«této» — книжно", {"example_cs": "V téhle situaci se cítím nesvůj"}),
    12664: (T + "«Natahuji» — книжно", {"example_cs": "Natáhnu ruce nahoru"}),
    12672: (T + "«velmi» — книжно", {"example_cs": "Dřív se lidé hrozně báli epidemií, jako byl mor"}),
    12732: (T + "«Moje … s mými» — калька", {"example_cs": "Terapeutka mi s problémy opravdu pomáhá"}),
    12758: (T + "«mého syna» — тяжело", {"example_cs": "Ve školce, kam chodí syn, je teď malá epidemie vší"}),
    12768: (T + "«moje duševní zdraví» — калька", {"example_cs": "Stres se mi podepsal na duševním zdraví"}),
}

REPLACE = []

SPLIT_LATER = {}
