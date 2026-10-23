"""Вычитка польского, порция p012 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    2448: (T + "«To nie jest uczciwe» — тяжело", {"example_pl": "To nieuczciwe"}),
    2460: (T + "«mój» — лишнее", {"example_pl": "W finansach dobrze się zarabia, ale brat prawie nie ma wolnego czasu"}),
    2466: (T + "«Moja» — лишнее", {"example_pl": "Sąsiadka pomaga uchodźcom w nauce niemieckiego"}),
    2468: (T + "«Moja … jako» — тяжело", {"example_pl": "Kuzynka jest stewardesą i co tydzień jest w innym mieście"}),
    2475: (T + "«Pan» — регистр", {"example_pl": "Nie musi pan być taki formalny, mówmy sobie po imieniu"}),
    2477: (T + "«Mój» — лишнее", {"example_pl": "Wujek jest leśniczym i zna każdą ścieżkę w lesie"}),
    2483: (T + "«W moim» — лишнее", {"example_pl": "W gronie przyjaciół jestem jedyną osobą bez dzieci"}),
    2490: (T + "нет слова карточки", {"example_pl": "Po kłótni czułem straszną frustrację"}),
    2495: (T + "«Mój» — лишнее", {"example_pl": "Tata od pięćdziesięciu lat jest członkiem tego samego klubu piłkarskiego"}),
    2499: (T + "«Mój» — лишнее", {"example_pl": "Dziadek przyjechał w latach sześćdziesiątych z Turcji do Kolonii jako gastarbeiter"}),
    2507: (T + "«wynosiła» — книжно", {"example_pl": "Kupujący chciał zapłacić tylko 3000 euro, moja kontrpropozycja to 3500"}),
    2530: (T + "«Moja» — лишнее", {"example_pl": "Córka nie toleruje glutenu, więc na jej urodziny piekę bezglutenowo"}),
    2533: (T + "«Mój» — лишнее", {"example_pl": "Brat z dwoma przyjaciółmi założył małą firmę"}),
    2553: (T + "«Czuję tęsknotę» — калька", {"example_pl": "Dopada mnie tęsknota za rodziną"}),
    2575: (T + "«W naszym mieście» — калька", {"example_pl": "U nas w mieście większość ludzi pracuje w przemyśle"}),
    2589: (T + "«Ten dom pochodzi» — книжно", {"example_pl": "Dom jest z XVIII wieku"}),
    2592: (T + "«Moja» — лишнее", {"example_pl": "Sąsiadka jest Żydówką i zaprosiła nas na Chanukę"}),
    2608: (T + "«panuje dobry klimat» — книжно", {"example_pl": "W zespole mamy dobry klimat"}),
    2618: (T + "«Chętnie oglądam» — калька gern", {"example_pl": "Lubię oglądać komedie"}),
    2626: (T + "«To jest poprawne» — тяжело", {"example_pl": "To poprawna odpowiedź"}),
    2628: (T + "«Na zewnątrz» — книжно", {"example_pl": "Na dworze właśnie głośno huknęło"}),
    2633: (T + "«Moje» — лишнее", {"example_pl": "Dziecko chodzi do żłobka"}),
    2651: (T + "«nowego toru» — смысл", {"example_pl": "Komunikat przez głośniki na dworcu był tak niewyraźny, że nikt nie zrozumiał, z którego toru"}),
    2660: (T + "«mojego» — лишнее", {"example_pl": "Ulubione zajęcie syna to zbieranie kamieni i malowanie ich"}),
    2679: (T + "«Mój» — лишнее", {"example_pl": "Kuzyn jest żołnierzem i przez rok pracuje w NATO w Brukseli"}),
    2700: (T + "«Moja» — лишнее", {"example_pl": "Siostra ma mały sklep internetowy z czapkami robionymi na drutach"}),
    2701: (T + "«naszego miasta» — тяжело", {"example_pl": "Odkąd są zakupy online, u nas w centrum wiele sklepów stoi pustych"}),
    2713: (T + "«mój paszport traci ważność» — книжно", {"example_pl": "Na kontroli paszportowej urzędnik zauważył, że paszport traci mi ważność w przyszłym tygodniu"}),
    2741: (T + "«mój» — лишнее", {"example_pl": "W teleturnieju dziadek zna każdą odpowiedź przed uczestnikami"}),
    2743: (T + "«mojej» — лишнее", {"example_pl": "W rankingu szkół w naszym mieście podstawówka córki jest na samej górze"}),
}

REPLACE = []

SPLIT_LATER = {}
