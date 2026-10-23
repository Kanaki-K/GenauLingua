"""Вычитка чешского, порция p031 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    10782: (T + "«velmi» — книжно", {"example_cs": "Nová kuchyně je hodně promyšlená, každá skříňka je přesně tam, kde ji člověk potřebuje"}),
    10791: (T + "«Moje dcera» — калька", {"example_cs": "Dcera je v jídle hodně vybíravá"}),
    10885: (T + "«v sedmdesáti letech můj děda» — тяжело", {"example_cs": "V sedmdesáti děda ještě zdolal Kilimandžáro"}),
    10897: (T + "«v mém» — лишнее", {"example_cs": "Fotka v novém pasu není zrovna lichotivá"}),
    11021: (T + "«velmi» — книжно", {"example_cs": "Po rozchodu byl citově hodně labilní"}),
    11226: (T + "«pro mého tátu» — книжно", {"example_cs": "Žebrat v bance o malý úvěr bylo pro tátu ponížení"}),
    11272: (T + "«velmi» — книжно", {"example_cs": "Naše kočka je vlastně plachá, ale dědovi je hodně oddaná"}),
    11320: (T + "предлог: «Ke»", {"example_cs": "Ke zdravotním sestrám, které pracují v noci a přesto zůstávají vlídné, chovám nejhlubší úctu"}),
    11338: (T + "«k jeho» — лишнее", {"example_cs": "Synova lhostejnost ke známkám mě dohání k šílenství"}),
    11371: (T + "«má svou slabost» — смысл", {"example_cs": "Pračka má jednu vadu: na konci třikrát pípne a pak ještě jednou"}),
    11422: (T + "«Stal jsem se zapomnětlivým» — книжно", {"example_cs": "Jsem teď tak zapomnětlivý, že si dokonce zapisuju, kde jsem zaparkoval auto"}),
    11427: (T + "«velmi» — книжно", {"example_cs": "Ráno před první kávou je manžel hodně mlčenlivý, radši se ho na nic neptat"}),
    11518: (T + "«Vysvědčení mého syna» — тяжело", {"example_cs": "Synovo vysvědčení je uspokojivé, ale nic víc"}),
    11541: (T + "«mého bratra» — тяжело", {"example_cs": "Bráchův samolibý úsměšek po každé výhře v šachách mě vytáčí"}),
}

REPLACE = []

SPLIT_LATER = {}
