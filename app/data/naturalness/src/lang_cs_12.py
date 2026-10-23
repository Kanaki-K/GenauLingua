"""Вычитка чешского, порция p012 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    2530: (T + "«nesnáší lepek» — двусмысленно", {"example_cs": "Dcera nemůže jíst lepek, a tak jí k narozeninám peču bezlepkově"}),
    2560: (T + "время: potrvá", {"example_cs": "Výroba naší pohovky potrvá šest týdnů"}),
    2595: (T + "«Kde je můj» — калька", {"example_cs": "Kde mám hřeben?"}),
    2607: (T + "«lezu po horách» — коряво", {"example_cs": "O víkendu chodím lézt do hor"}),
    2624: (T + "«svého» — лишнее", {"example_cs": "Potřebuju kopii pasu"}),
    2628: (T + "«právě hlasitě prasklo» — коряво", {"example_cs": "Venku zrovna něco hlasitě prasklo"}),
    2651: (T + "«nepochopil nové nástupiště» — коряво", {"example_cs": "Hlášení z reproduktoru na nádraží bylo tak nesrozumitelné, že nikdo nepochytil, které je nové nástupiště"}),
    2690: (T + "«Poznávací značka auta» — калька", {"example_cs": "Auto má špinavou poznávací značku"}),
    2702: (T + "«Jsem optimistický, že» — калька", {"example_cs": "Dívám se na to optimisticky, zvládneme to"}),
    2729: (T + "«prezentuji» — книжно", {"example_cs": "Výsledky budu prezentovat zítra"}),
    2751: (T + "«Teplotu se dá» — грамматика", {"example_cs": "Teplota se dá regulovat v každém pokoji zvlášť"}),
}

REPLACE = []

SPLIT_LATER = {}
