"""Вычитка чешского, порция p006 (A2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    6326: (T + "«příliš» — книжно", {"example_cs": "To je moc nebezpečné"}),
    6329: (T + "«On» — лишнее", {"example_cs": "Opravdu vyhrál!"}),
    6401: (T + "«Jsi jako» — слово карточки «podobat se»", {"example_cs": "Strašně se podobáš mámě"}),
    6496: (T + "«Nevšímáš si» — не тот вид", {"example_cs": "Copak sis nevšiml, že lže?"}),
    6657: (T + "«slavný svým» — коряво", {"example_cs": "Strýc je v celé vesnici známý svým jablečným koláčem"}),
    6675: (T + "«V této» — книжно", {"example_cs": "V takové výšce je vzduch řidší"}),
    6696: (T + "«velmi» — книжно", {"example_cs": "Ta postel je hrozně měkká"}),
    6715: (T + "«Typický Max» — калька", {"example_cs": "Typické pro Maxe, zase jde pozdě"}),
    7143: (T + "«regionu» — книжно", {"example_cs": "Z jakého jsi kraje?"}),
    8980: (T + "«svoji» — лишнее", {"example_cs": "Zítra odešlu žádost o místo"}),
    10095: (T + "«pro mě» — калька", {"example_cs": "Ten chleba je mi moc kyselý"}),
    10102: (T + "«velmi» — книжно", {"example_cs": "Ten film je hrozně vtipný"}),
    10182: (T + "noch = всё ещё", {"example_cs": "Ten šroub je pořád volný"}),
    12334: (T + "«uděláme okruh» — калька", {"example_cs": "Po jídle si uděláme malé kolečko po starém městě"}),
    13430: (T + "«zůstávám» — не тот вид", {"example_cs": "Prší, proto zůstanu doma"}),
    13644: (T + "«darovala» — книжно", {"example_cs": "Ten řetízek mi dala babička"}),
    13843: (T + "«Tvůj hlas je» — калька", {"example_cs": "Máš krásný hlas"}),
    14035: (T + "«Tady je tvoje káva» — калька", {"example_cs": "Tady máš kávu, prosím"}),
    15048: (T + "«sladká» о ребёнке — калька", {"example_cs": "Moje vnučka má tři roky a je moc roztomilá"}),
    15391: (T + "«Daroval» — книжно", {"example_cs": "Dal jí červené růže"}),
    15518: (T + "«na chladné místo» — тяжело", {"example_cs": "Dej prosím pivo do chladu"}),
    17488: (T + "«Motor mého auta» — калька", {"example_cs": "Mám v autě rozbitý motor"}),
}

REPLACE = []

SPLIT_LATER = {}
