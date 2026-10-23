"""Вычитка польского, порция p034 (B2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    14257: (T + "«Moje» — лишнее", {"example_pl": "Dzieci nie wiedzą już, jak się korzysta z automatu telefonicznego, dla nich to eksponat muzealny"}),
    14258: (T + "«w mediach … w telewizji» — повтор", {"example_pl": "W relacjach z nawałnicy w telewizji pokazali nawet naszą ulicę"}),
    14273: (T + "«swoim» — лишнее", {"example_pl": "Na demonstracji klimatycznej córka sama napisała hasła na transparencie"}),
    14280: (T + "«swoje … nie pisze dobrze» — коряво", {"example_pl": "Babcia dyktuje mi przepisy, bo sama już słabo pisze"}),
    14296: (T + "«wychodzić z nim będzie, proszę» — коряво", {"example_pl": "Popieram pomysł z psem, ale na spacery niech wtedy chodzi ktoś inny"}),
    14326: (T + "«naszego» — лишнее", {"example_pl": "Interakcja psa z robotem sprzątającym to najzabawniejsza rzecz, jaką kiedykolwiek widzieliśmy"}),
    14327: (T + "«Nasz» — лишнее", {"example_pl": "Router wysyła tak słaby sygnał, że do pokoju dzieci internet nie dociera"}),
    14331: (T + "«Nasz» — лишнее", {"example_pl": "Pies przy jedzeniu ciągle szuka kontaktu wzrokowego, licząc na kawałek kiełbasy"}),
    14464: (T + "«cały mój rytm» — калька", {"example_pl": "Po trzech tygodniach nocnych zmian mam kompletnie rozregulowany rytm"}),
    14467: (T + "«Moja» — лишнее", {"example_pl": "Cioteczna babcia była zakonnicą i pracowała w szpitalu"}),
    14491: (T + "«Mój … nie jest dobrym» — калька", {"example_pl": "Brat to kiepski tancerz, na weselach zawsze siedzi przy stole"}),
    14494: (T + "«Moi» — лишнее", {"example_pl": "Sąsiedzi są wierzącymi chrześcijanami i co niedzielę chodzą do kościoła"}),
    14498: (T + "«Mój» — лишнее", {"example_pl": "Dziadek całe życie pisał poezję, ale nigdy nic nie wydał"}),
    14509: (T + "«Ona» — лишнее", {"example_pl": "Pięknie gra na skrzypcach"}),
    14513: (T + "порядок «nas»", {"example_pl": "Komik na scenie nas rozśmieszył"}),
    14524: (T + "«Moja» — лишнее", {"example_pl": "Siostra śpiewa bosko, w chórze zawsze dostaje solówki"}),
    14541: (T + "«Moja religijna rodzina» — калька", {"example_pl": "Rodzina jest bardzo religijna i obchodzi wiele świąt w roku"}),
    14549: (T + "«Pierwszy raz zjeść … to było» — коряво", {"example_pl": "Kiedy pierwszy raz zjadłem naprawdę dobry francuski chleb, to było dla mnie objawienie"}),
    14558: (T + "«swojego» — лишнее", {"example_pl": "Na każdy egzamin córka zabiera małego pluszowego misia jako talizman"}),
    14585: (T + "«swojego» — лишнее", {"example_pl": "Za trasą koncertową ulubionego zespołu córka jeździła do trzech miast"}),
    14595: (T + "«Moja» — лишнее", {"example_pl": "Przyjaciółka wierzy w reinkarnację i mówi, że w poprzednim życiu była kotem"}),
    14649: (T + "«W mojej obrączce jest napis» — калька", {"example_pl": "W obrączce mam od środka grawer z datą naszego ślubu"}),
    14664: (T + "«Mój» — лишнее", {"example_pl": "Nauczyciel niemieckiego uważa, że moja interpretacja wiersza jest zbyt swobodna"}),
    14677: (T + "«nasze» — лишнее", {"example_pl": "Do zasypiania dziecko najbardziej lubi spokojną muzykę orkiestrową"}),
    14720: (T + "«mojego» — лишнее", {"example_pl": "Dla syna bramkarz Bayernu to coś w rodzaju bóstwa, nawet śpi w jego koszulce"}),
    14751: (T + "«mojego» — лишнее", {"example_pl": "Na komunię siostrzeńca przyjeżdża cała rodzina z Polski i potrzebujemy trzech stołów więcej"}),
    14761: (T + "«mojego … swoją» — лишнее", {"example_pl": "Zespół siostrzeńca wysłał piosenkę do dwudziestu wytwórni płytowych, ale żadna nie odpowiedziała"}),
    14775: (T + "«moja rodzina zna» — калька", {"example_pl": "Z piosenek urodzinowych u nas w rodzinie zawsze zna się tylko pierwszą zwrotkę, potem wszyscy nucą"}),
    14812: (T + "«nasz» — лишнее", {"example_pl": "Babcia wierzy, że kot ma nadprzyrodzone moce, bo przed każdą burzą znika pod kanapą"}),
    14842: (T + "«Nasz» — лишнее", {"example_pl": "Szkolny wieczór teatralny był czystą improwizacją, bo połowa dzieci zapomniała tekstu"}),
    15042: (T + "«wzruszający dla rodziny» — коряво", {"example_pl": "Pogrzeb był dla rodziny bardzo przejmujący"}),
    15043: (T + "«Mój narzeczony i ja» — калька", {"example_pl": "Z narzeczonym bierzemy ślub w przyszłym miesiącu"}),
    15045: (T + "«Moje adoptowane dziecko» — коряво", {"example_pl": "Adoptowany synek jest u nas bardzo szczęśliwy"}),
    15056: (T + "«wkrótce wróci do domu» — книжно", {"example_pl": "Tatuś zaraz wróci"}),
    15058: (T + "«jego pies jest jego» — повтор", {"example_pl": "Odkąd dziadek jest sam, pies jest jego najwierniejszym towarzyszem"}),
    15061: (T + "«Moja» — лишнее", {"example_pl": "Przyjaciółka jest lesbijką"}),
    15063: (T + "«czuje się jak z obrońcą» — коряво", {"example_pl": "Odkąd mamy dużego psa, córeczka czuje się bezpieczna, jakby miała obrońcę"}),
    15064: (T + "«pomocników do pomocy» — повтор", {"example_pl": "Na festyn miejski szukamy jeszcze chętnych pomocników do rozstawiania stoisk"}),
    15075: (T + "«Nasz» — лишнее", {"example_pl": "Zięć pomógł nam przy przeprowadzce i sam złożył wszystkie szafy"}),
    15080: (T + "«swoje» — лишнее", {"example_pl": "Sama wychowuje dzieci"}),
    15092: (T + "«mojego» — лишнее", {"example_pl": "Na chrzciny bratanka cała rodzina ubrała się na biało"}),
    15096: (T + "«Mój brat był moim» — калька", {"example_pl": "Świadkiem na moim weselu był brat"}),
    15098: (T + "«Moja» — лишнее", {"example_pl": "Teściowa przyjeżdża jutro z wizytą"}),
    15099: (T + "«swoim» — лишнее", {"example_pl": "Przed supermarketem codziennie siedzi ten sam żebrak z psem"}),
}

REPLACE = []

SPLIT_LATER = {}
