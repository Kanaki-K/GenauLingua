"""Вычитка польского, порция p035 (B2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    15137: (T + "«W piłce dostał piłką» — повтор", {"example_pl": "Na meczu dostał piłką prosto w jądra i przez dziesięć minut leżał na murawie"}),
    15173: (T + "«moich dziadków» — лишнее", {"example_pl": "Dla dziadków dziewictwo przed ślubem było jeszcze bardzo ważne, dla moich dzieci to w ogóle nie temat"}),
    15224: (T + "«Mój» — лишнее", {"example_pl": "Syn to mały dżentelmen, w supermarkecie przytrzymuje drzwi każdej starszej pani"}),
    15228: (T + "«każdego ranka» → «co rano»", {"example_pl": "„No i co, złotko, znowu zaspałeś?” — pyta piekarka syna co rano"}),
    15229: (T + "«rozebrać górną część ciała» — коряво", {"example_pl": "U lekarza do osłuchania muszę odsłonić górną część ciała"}),
    15253: (T + "«Moja» — лишнее", {"example_pl": "Świadkowa zapomniała obrączek w urzędzie, więc wzięliśmy dwa żelki"}),
    15254: (T + "«Nasza» — лишнее", {"example_pl": "Nawigacja mówi u nas niskim męskim głosem, dzieci nazywają go panem Müllerem"}),
    15288: (T + "«Przy jego … brat» — коряво", {"example_pl": "Przy takiej krzepkiej posturze nikt nie wierzy, że brat tańczy balet"}),
    15307: (T + "«naszym» — лишнее", {"example_pl": "Z pierworodnym synem byliśmy dużo surowsi, mała dziś może prawie wszystko"}),
    15313: (T + "«Moja … ciemnowłosa, a ja jestem» — коряво", {"example_pl": "Siostra jest szatynką, a ja blondynką"}),
    15316: (T + "«swoim» — лишнее", {"example_pl": "Siostra co wieczór rozmawia z nienarodzonym dzieckiem i puszcza mu muzykę"}),
    15321: (T + "«utrzymuje go w młodości» — калька", {"example_pl": "Dziadek twierdzi, że mały flirt z piekarką co rano utrzymuje go w formie"}),
    15509: (T + "«przeszedł» → «przepełzł»", {"example_pl": "Po stole przepełzł czarny chrząszcz"}),
    15517: (T + "«Moje buty» — калька", {"example_pl": "Buty ugrzęzły mi w błocie"}),
    15523: (T + "«wiele … które pływają w wodzie» — коряво", {"example_pl": "W gospodarstwie jest dużo gęsi, pływają w stawie"}),
    15528: (T + "«Mój» — лишнее", {"example_pl": "Syn zna nazwy ponad pięćdziesięciu dinozaurów, ja znam tylko trzy"}),
    15544: (T + "«pozostanie mokre» — книжно", {"example_pl": "Drewno zgnije, jeśli będzie stale mokre"}),
    15548: (T + "«wiele» → «dużo»", {"example_pl": "W stawie pływa dużo kaczek"}),
    15570: (T + "«Nasz» — лишнее", {"example_pl": "Nowy kotek to takie małe, słodkie stworzenie"}),
    15591: (T + "идиома «wróble ćwierkają na dachach»", {"example_pl": "Wróble na dachach ćwierkają, że się pobierają"}),
    15655: (T + "«naszego» — лишнее", {"example_pl": "Weterynarz znalazł u psa pasożyty w jelitach, teraz dostaje kurację"}),
    15760: (T + "«Moi» — лишнее", {"example_pl": "Dziadkowie mieszkają na północnym zachodzie Niemiec, tuż przy Morzu Północnym"}),
    15775: (T + "«przesypia sen zimowy» — коряво", {"example_pl": "Żółw zapada w piwnicy w sen zimowy, a syn codziennie sprawdza, czy jeszcze oddycha"}),
    15777: (T + "«Długo moi przyjaciele» — порядок", {"example_pl": "Przyjaciele długo myśleli, że są bezpłodni, a teraz będą mieli bliźniaki"}),
    15883: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez orkan jutro odwołują wszystkie pociągi, a dzieci cieszą się na dzień w domu"}),
    16147: (T + "«Każdego lata» — калька", {"example_pl": "Co roku latem nad jeziorem jest prawdziwa inwazja komarów"}),
    16151: (T + "«nasz» — лишнее", {"example_pl": "Podczas burzy pies uciekł pod łóżko"}),
    16153: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez starą bombę z czasów wojny wczoraj ewakuowali całą dzielnicę"}),
    16173: (T + "«zdecydowała przeciw» — коряво", {"example_pl": "W głosowaniu większość była przeciw propozycji"}),
    16177: (T + "«każdego wieczoru» → «co wieczór»", {"example_pl": "W filmie porywacze co wieczór o ósmej dzwonią do rodziny"}),
    16180: (T + "«uderzył głową piłkę» — коряво", {"example_pl": "W ostatniej minucie nasz napastnik uderzeniem głową wpakował piłkę do bramki"}),
    16181: (T + "«naszego» — лишнее", {"example_pl": "Na czas urlopu pies jest na przechowaniu u sąsiadki"}),
    16182: (T + "порядок слов", {"example_pl": "Tu musisz podpisać umowę"}),
    16188: (T + "«Mój» — лишнее", {"example_pl": "Dziadek przez dwa lata służył w wojsku i ciągle o tym opowiada"}),
    16198: (T + "«i policja go znalazła» — коряво", {"example_pl": "Paszport okazał się podróbką"}),
    16206: (T + "«Kara za jego … była» — книжно", {"example_pl": "Za złe zachowanie dostał bardzo surową karę"}),
    16214: (T + "«mój» — лишнее", {"example_pl": "Przez złą ocenę syn ma tydzień szlabanu"}),
    16225: (T + "«Mój» — лишнее", {"example_pl": "Młodszy brat najbardziej lubi bawić się w policjanta i bandytę, i zawsze jest bandytą"}),
    16246: (T + "«Mój» — лишнее", {"example_pl": "Wujek od trzydziestu lat pracuje w wymiarze sprawiedliwości, najpierw jako sędzia, teraz jako prokurator"}),
    16247: (T + "«nasze … naszą» — повтор", {"example_pl": "Przy wędrówkach po Alpach naszą bazą jest mała chatka"}),
    16258: (T + "«Mój» — лишнее", {"example_pl": "Pradziadek służył w tym samym pułku co jego ojciec"}),
    16272: (T + "«nie zostanie sprzedany» — книжно", {"example_pl": "To wybrakowany towar, nie idzie do sprzedaży"}),
}

REPLACE = []

SPLIT_LATER = {}
