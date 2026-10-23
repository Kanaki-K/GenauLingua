"""Вычитка чешского, порция p003 (A1–A2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    1776: (T + "порядок слов", {"example_cs": "Ta zkouška je zítra?"}),
    2093: (T + "«Zůstávám» — не тот вид", {"example_cs": "Zůstanu doma, protože jsem nemocný"}),
    2539: (T + "«Rezervujeme» — книжно", {"example_cs": "Bereme si polopenzi"}),
    6228: (T + "«velmi daleko» — книжно", {"example_cs": "To je strašně daleko"}),
    6396: (T + "«připomíná tebe» — порядок", {"example_cs": "To mi tě připomíná"}),
    6897: (T + "«tuto» — книжно", {"example_cs": "Tuhle restauraci ti doporučuju"}),
    9712: (T + "«svoje auto» — лишнее", {"example_cs": "Chci prodat auto"}),
    10438: (T + "«k tvému úspěchu» — тяжело", {"example_cs": "Gratuluju ti k úspěchu"}),
    11744: (T + "«příliš hořká» — книжно", {"example_cs": "Ta káva je moc hořká"}),
    12253: (T + "«Dnes v noci» — калька", {"example_cs": "Dneska večer jdeme tancovat na diskotéku"}),
    12505: (T + "«velmi příjemně» — книжно", {"example_cs": "Ty květiny krásně voní"}),
    13317: (T + "«Tímto» — книжно", {"example_cs": "Tímhle autem pojedeme na dovolenou"}),
    13475: (T + "«hodin v noci» — калька", {"example_cs": "Už je jedenáct večer"}),
    15029: (T + "«Moje partnerka a já» — калька", {"example_cs": "S partnerkou máme velké plány do budoucna"}),
    15084: (T + "«domácnosti … domácnost» — повтор", {"example_cs": "Moje máma je žena v domácnosti a stará se o celý dům"}),
    15370: (T + "«Rozdělejme» — книжно", {"example_cs": "Pojďme rozdělat oheň"}),
    15384: (T + "«Vítr je silný» — калька", {"example_cs": "Fouká silný vítr"}),
    16032: (T + "«Připojte podpis» — канцелярит", {"example_cs": "Sem prosím Váš podpis"}),
    17563: (T + "«stojí hodně» — оборвано", {"example_cs": "Ta oprava stojí hodně peněz"}),
    3: (T + "порядок слов", {"example_cs": "Po večerech se učím německy"}),
}

REPLACE = []

SPLIT_LATER = {}
