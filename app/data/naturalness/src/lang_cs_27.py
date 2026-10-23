"""Вычитка чешского, порция p027 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    7118: (T + "«V šíři stepi nevidíte» — калька", {"example_cs": "V širé stepi neuvidíš celé hodiny jediný dům"}),
    7120: (T + "«Moji rodiče» — книжно", {"example_cs": "Rodiče neschvalují moje rozhodnutí"}),
    7134: (T + "«velmi … v této noci» — книжно", {"example_cs": "Hvězdy dneska v noci krásně jasně svítí"}),
    7135: (T + "«jde za svým pudem» — калька", {"example_cs": "Náš kocour poslouchá pud a každou noc loví na zahradě myši"}),
    7139: (T + "«Moje staré tričko» — калька", {"example_cs": "Staré tričko mám úplně roztrhané"}),
    7150: (T + "«můj mobil by byl» — порядок", {"example_cs": "Bez obalu by byl mobil dávno rozbitý, pořád mi padá"}),
    7189: (T + "«můj syn» — лишнее", {"example_cs": "V noci se syn plíží do kuchyně a jí čokoládu"}),
    7199: (T + "«Věnuji svůj» — книжно", {"example_cs": "Čas věnuju rodině"}),
    7201: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju prací prášek"}),
    7202: (T + "«tohoto» — книжно", {"example_cs": "Do toho projektu nejsem zapojený"}),
    7232: (T + "«velmi» — книжно", {"example_cs": "Vysvětluje úkol hodně přesně"}),
    7260: (T + "«Opírám» — не тот вид", {"example_cs": "Opřu žebřík o zeď"}),
    7261: (T + "«spíše» — книжно", {"example_cs": "Není líný, je spíš úplně vyčerpaný z noční směny"}),
    7277: (T + "«velmi» — книжно", {"example_cs": "Obraz je dokonale ostrý, udělaný hodně profesionálně"}),
    7303: (T + "«mnoha lidem» — книжно", {"example_cs": "Nový zákon umožňuje spoustě lidí studovat"}),
    7306: (T + "«velmi» — книжно", {"example_cs": "Jeho odpověď byla hodně vágní"}),
    7308: (T + "«ještě více posiluje mé» — тяжело", {"example_cs": "To mé podezření ještě posiluje"}),
    7344: (T + "«svou vrtačku» — тяжело", {"example_cs": "Kdy můžu mít vrtačku zpátky? Potřebuju ji o víkendu"}),
    7351: (T + "«se svým platem» — калька", {"example_cs": "S platem vyjdu"}),
    7359: (T + "«svůj» — лишнее", {"example_cs": "Chceme rozšířit podnik a otevřít nové obchody"}),
    7363: (T + "«Můj pes je … můj» — повтор", {"example_cs": "Pes je svým způsobem můj nejlepší kamarád"}),
    7371: (T + "«Moje miminko» — калька", {"example_cs": "Miminko občas pláče úplně bezdůvodně a nevím, co dělat"}),
    7387: (T + "«lépe» — книжно", {"example_cs": "Nastražuje uši, aby líp slyšel"}),
    7390: (T + "«Téměř» — книжно", {"example_cs": "Skoro všechny moje kamarádky už mají děti"}),
    7393: (T + "«Můj poukaz» — калька", {"example_cs": "Poukaz mi na konci měsíce propadne, musím ho rychle uplatnit"}),
    7455: (T + "«velmi» — книжно", {"example_cs": "Na svatbu si teta bere hodně nápadný růžový klobouk"}),
}

REPLACE = []

SPLIT_LATER = {}
