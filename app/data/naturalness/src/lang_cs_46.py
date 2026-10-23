"""Вычитка чешского, порция p046 (C2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    8669: (T + "«Holeň mé vysoké boty» — тяжело", {"example_cs": "Na botě mám roztrženou holeň"}),
    8704: (T + "«potřebuji» → «potřebuju»", {"example_cs": "V zásadě jsem pro, ale ještě potřebuju čas na rozmyšlenou"}),
    9176: (T + "«zásluha mé sestry» — тяжело", {"example_cs": "To, že oslava byla tak krásná, je hlavně sestřina zásluha"}),
    9183: (T + "«své» — лишнее", {"example_cs": "Majitel obchodu zná skoro všechny stálé zákazníky"}),
    9188: (T + "«své» — лишнее", {"example_cs": "Na stipendium potřebuje dcera doporučující dopis od učitelky"}),
    9193: (T + "«pro mou profesní budoucnost» — книжно", {"example_cs": "Poradkyně mi dala užitečné tipy, co dělat dál v práci"}),
    9194: (T + "«své» — лишнее", {"example_cs": "Tchán v dílně vyrábí dřevěné hračky pro vnoučata"}),
    9200: (T + "«Moje máma» — лишнее", {"example_cs": "Máma je podnikatelka a pořád cestuje"}),
    9205: (T + "«svou vlastní» — лишнее", {"example_cs": "Mám pocit, že nový kolega sleduje vlastní agendu"}),
    9222: (T + "«jeho» — лишнее", {"example_cs": "Děda pochází z dělnické třídy a je hrdý, že všechna vnoučata vystudovala"}),
    9226: (T + "род: «byla … komorník»", {"example_cs": "Manžel se ke mně občas chová jako ke komorníkovi"}),
    9249: (T + "«nazývá … útulným» — книжно", {"example_cs": "Náš realitní makléř tvrdí, že malinký byt je útulný a hluk z ulice živý"}),
    9257: (T + "«Můj» — лишнее", {"example_cs": "Praděda strávil po válce tři roky v pracovním táboře na Sibiři"}),
    9640: (T + "«Naše … svou» — лишнее", {"example_cs": "Sousedka byla s obří dýní na titulní straně místních novin"}),
    9644: (T + "«Můj» — лишнее", {"example_cs": "Švagr si rád hraje na intelektuála a u grilu cituje Nietzscheho"}),
    10708: (T + "«můj» — лишнее", {"example_cs": "S kopečkem čokoládové zmrzliny v ruce je syn blažený"}),
    11213: (T + "«velmi» — книжно", {"example_cs": "Babička je hodně zbožná, před každým jídlem se krátce pomodlí"}),
    11214: (T + "«můj» — лишнее", {"example_cs": "Po roce v Londýně mluví bratranec o našem městečku dost povýšeně"}),
    11215: (T + "«Moje lékařka považuje» — калька", {"example_cs": "Podle doktorky mám znepokojivě vysoký tlak"}),
    11218: (T + "«své» — лишнее", {"example_cs": "Děda je do malé vnučky úplně zblázněný a každý týden jí koupí hračku"}),
    11220: (T + "«svého syna» — тяжело", {"example_cs": "Jako rozhodčí na synově zápase jsem samozřejmě trochu zaujatý"}),
    11222: (T + "«Moje» — лишнее", {"example_cs": "Děti milují vzrušení na strašidelné dráze, já si radši zakryju oči"}),
    11224: (T + "«Můj … aniž by» — книжно", {"example_cs": "Brácha nemá žádné skrupule sníst poslední kousek koláče bez zeptání"}),
    11247: (T + "«nepociťuji» → «nepociťuju»", {"example_cs": "Po dovolené nepociťuju sebemenší chuť jít do kanceláře"}),
    11290: (T + "«vyprošuji» → «vyprošuju»", {"example_cs": "Tuhle urážku si okamžitě vyprošuju"}),
    11293: (T + "«slibuji» → «slibuju»", {"example_cs": "Od nové práce si slibuju hlavně milejší kolegy"}),
    11300: (T + "«můj» — лишнее", {"example_cs": "Ženichova řeč byla tak dojemná, že se rozplakal i táta"}),
    11312: (T + "«považuje za» — книжно", {"example_cs": "Synovi přijde sushi nechutné, i když ho nikdy neochutnal"}),
    11323: (T + "«považuje za příliš» — книжно", {"example_cs": "Babičce přijde reklama na spodní prádlo na zastávce moc erotická"}),
    11356: (T + "«běží filmy» — калька", {"example_cs": "Když dávají filmy o zvířatech, sedí syn před televizí jako přikovaný"}),
    11357: (T + "«svém» — лишнее", {"example_cs": "Stát po dvaceti letech zase v dětském pokoji je úplně neskutečný pocit"}),
    11360: (T + "«Můj strach» — калька", {"example_cs": "Strach z pavouků mám úplně iracionální, vždyť mi nic nedělají"}),
    11373: (T + "«považuje za» — книжно", {"example_cs": "Babičce přijde sprosté žvýkat při mluvení žvýkačku"}),
    11380: (T + "«svém» — лишнее", {"example_cs": "Bratr posměšně zvedne obočí, když vyprávím o novém cvičebním plánu"}),
    11384: (T + "«jejího … moje» — тяжело", {"example_cs": "Při každém gólu svého klubu se jinak klidná babička dostane do extáze"}),
    11399: (T + "«moje bavorská» — лишнее", {"example_cs": "„Pán Bůh zaplať!“ říká babička z Bavorska, když jí někdo nese nákup"}),
    11408: (T + "«Můj» — лишнее", {"example_cs": "Budík každé ráno neúprosně zvoní v šest"}),
    11424: (T + "«Můj … opravdu» — книжно", {"example_cs": "Šéf je fakt puntičkářský, když jde o formátování"}),
    11440: (T + "«Můj» — лишнее", {"example_cs": "Děda je starý lakomec a nikdy neutratí peníze"}),
    11443: (T + "«svým» — лишнее", {"example_cs": "Po třech zavržených návrzích je dcera s plakátem konečně spokojená"}),
    11473: (T + "«Můj» — лишнее", {"example_cs": "Švagr je chytrák, opravuje dokonce i navigaci"}),
    11477: (T + "«velmi» — книжно", {"example_cs": "Je to hodně disciplinovaný sportovec a trénuje každý den"}),
    11482: (T + "«velmi» — книжно", {"example_cs": "Jeho netaktní poznámka ji hodně zranila a rozzlobila"}),
}

REPLACE = []

SPLIT_LATER = {}
