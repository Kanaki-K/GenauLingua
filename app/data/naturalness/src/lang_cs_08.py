"""Вычитка чешского, порция p008 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    831: (T + "«Chodím sem zřídka» — книжно", {"example_cs": "Sem chodím málokdy"}),
    887: (T + "«ve svém pokoji» — лишнее", {"example_cs": "Maluju stěnu v pokoji"}),
    1025: (T + "«daruje» — книжно", {"example_cs": "Na MDŽ mi manžel vždycky koupí květiny"}),
    1110: (T + "«mohu» — книжно", {"example_cs": "Na dovolené můžu konečně vypnout"}),
    1112: (T + "«Získal jsem diplom s výsledky» — коряво", {"example_cs": "Mám diplom s dobrými známkami"}),
    1114: (T + "«mohu» — книжно", {"example_cs": "Kde můžu zaparkovat auto?"}),
    1169: (T + "время: потрвá", {"example_cs": "Můj pobyt potrvá tři měsíce"}),
    1201: (T + "«Sundávám» — не тот вид", {"example_cs": "Sundám si bundu"}),
    1237: (T + "время: potrvá", {"example_cs": "Léčba potrvá dva týdny"}),
    1251: (T + "«Po odborném vzdělání» — оборвано", {"example_cs": "Po dokončení odborného vzdělání hned našla práci"}),
    1258: (T + "«jasné vysněné povolání» — коряво", {"example_cs": "V šestnácti člověk často ještě nemá vysněné povolání"}),
    1279: (T + "«cesta» → слово карточки «dráha»", {"example_cs": "Moje vzdělávací dráha nebyla přímočará: nejdřív učňák, pak maturita, pak vysoká"}),
    1294: (T + "«pomoci» — книжно", {"example_cs": "Můžeš mi pomoct rozřezat to prkno?"}),
    1299: (T + "«procházíme» — не тот вид", {"example_cs": "V neděli se jen tak projdeme po starém městě"}),
    1305: (T + "«V mém pokoji» — калька", {"example_cs": "V pokoji mám chaos"}),
    1353: (T + "«u našeho vjezdu» — смысл", {"example_cs": "Soused zase parkuje před naším vjezdem"}),
}

REPLACE = []

SPLIT_LATER = {}
