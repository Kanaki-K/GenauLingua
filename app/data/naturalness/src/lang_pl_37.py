"""Вычитка польского, порция p037 (B2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    17197: (T + "«Nasz» — лишнее", {"example_pl": "Pies to mieszaniec, skrzyżowano pudla z labradorem"}),
    17206: (T + "«każdego wieczoru» → «co wieczór»", {"example_pl": "Na rejsie co wieczór ktoś inny musiał pisać dziennik pokładowy"}),
    17229: (T + "«żeby odwiedzić rodzinę» — повтор", {"example_pl": "Często jeżdżę do rodzinnego miasta odwiedzić bliskich"}),
    17260: (T + "«swoim» — лишнее", {"example_pl": "W weekendy jeździ kabrioletem nad jezioro"}),
    17305: (T + "«Mój lot … jest» — калька", {"example_pl": "Lot powrotny mam w przyszły wtorek o czternastej"}),
    17313: (T + "«W moim» — лишнее", {"example_pl": "W starym motorowerze znowu zatkał mi się gaźnik"}),
    17326: (T + "«Moja» — лишнее", {"example_pl": "Koja na statku jest bardzo mała, ale przytulna"}),
    17349: (T + "«Mój niemiecki był» — калька", {"example_pl": "Na początku mówiłem po niemiecku tak nieporadnie, że piekarz zawsze odpowiadał mi po angielsku"}),
    17354: (T + "«nasz» — лишнее", {"example_pl": "Po warkocie silnika pies już z daleka poznaje, że tata wraca do domu"}),
    17387: (T + "«naszego» — лишнее", {"example_pl": "Po dwóch godzinach szukania znaleźliśmy wreszcie w lesie miejsce upadku drona"}),
    17408: (T + "«swój» — лишнее", {"example_pl": "W każdą niedzielę sąsiad poleruje zabytkowy samochód i potem objeżdża dokładnie raz osiedle"}),
    17538: (T + "«Strona mojej firmy jest» — калька", {"example_pl": "Nasza firma ma zupełnie nową stronę internetową, wygląda świetnie"}),
    17548: (T + "«swoim» — лишнее", {"example_pl": "Na weselu kolega zrobił dronem świetne zdjęcia z góry"}),
    17550: (T + "«w naszym domu» — лишнее", {"example_pl": "Bez elektryczności w domu nic nie działa, nawet ogrzewanie"}),
    17551: (T + "«Nasz» — лишнее", {"example_pl": "Sąsiad na kempingu ma głośny agregat, który chodzi całą noc"}),
    17561: (T + "«Moja» — лишнее", {"example_pl": "Babcia ma jeszcze w piwnicy starą maszynę do pisania"}),
    17571: (T + "«Jak mogę» — калька", {"example_pl": "Jak wyłączyć powiadomienia w telefonie?"}),
    17581: (T + "«awarii uległ» — книжно", {"example_pl": "Na lotnisku padł system bezpieczeństwa i wszystkie loty miały opóźnienie"}),
    17610: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez usterkę czujnik dymu zapiszczał w środku nocy"}),
    17635: (T + "«spróbuj ponownie» — книжно", {"example_pl": "System jest offline, spróbuj później jeszcze raz"}),
    17643: (T + "«mój» — лишнее", {"example_pl": "Mechanizm zabezpieczenia przed dziećmi jest tak skomplikowany, że szafkę otwiera tylko syn"}),
    17666: (T + "«mojego» — лишнее", {"example_pl": "W grze wideo syna co drugi wróg ma miotacz ognia"}),
    17678: (T + "«mojego serwisu» — лишнее", {"example_pl": "Algorytm serwisu wideo zna już mój gust lepiej niż ja sam"}),
    17744: (T + "«Nasz» — лишнее", {"example_pl": "System alarmowy prawie co wieczór zgłasza włamywacza, ale to zawsze tylko kot w oknie"}),
    17797: (T + "«naszym» — лишнее", {"example_pl": "Instalacja solarna na dachu latem wytwarza więcej prądu, niż potrzebujemy"}),
    17807: (T + "«Giełda wzrosła» — калька", {"example_pl": "Na giełdzie dziś mocne wzrosty"}),
    17813: (T + "«mojej» — лишнее", {"example_pl": "Po pandemii biuro podróży cioci zbankrutowało"}),
    17814: (T + "«dobrze wnieść swoje» — коряво", {"example_pl": "W nowej firmie mogę dużo wnieść dzięki doświadczeniu z zagranicy"}),
    17816: (T + "«moja droga» — калька", {"example_pl": "Od przeprowadzki droga do pracy mi się podwoiła, teraz jadę godzinę"}),
    17817: (T + "«moich» — лишнее", {"example_pl": "Dla dziadków własny samochód był wtedy oznaką zamożności"}),
    17857: (T + "«Mój wspólnik prowadzi ze mną» — коряво", {"example_pl": "Prowadzę firmę razem ze wspólnikiem"}),
    17863: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez inwentaryzację market budowlany jest w sobotę zamknięty, akurat kiedy potrzebuję farby"}),
    17871: (T + "«Moja» — лишнее", {"example_pl": "Pierwsza próba z chlebem na zakwasie to była klapa, był twardy jak kamień"}),
    17962: (T + "«Mój» — лишнее", {"example_pl": "Syn studiuje psychologię na uniwersytecie"}),
    17967: (T + "«przyszło spostrzeżenie» — калька", {"example_pl": "Po wypaleniu doszedłem do wniosku, że zdrowie jest ważniejsze niż kariera"}),
    17973: (T + "«moich» — лишнее", {"example_pl": "Dla dziadków mieszkanie z obcymi ludźmi to bardzo dziwny styl życia"}),
    17974: (T + "«Mój» — лишнее", {"example_pl": "Dziadek służył w czasie wojny w artylerii i od tamtej pory słabo słyszy"}),
    18010: (T + "«mój» — лишнее", {"example_pl": "Przy każdym nowym przepisie mąż musi być królikiem doświadczalnym"}),
    18210: (T + "«Mój … mój» — лишнее", {"example_pl": "Współlokator ciągle wyjada mi jogurt z lodówki"}),
    18252: (T + "«Moja» — лишнее", {"example_pl": "Współlokatorka co niedzielę gotuje dla całego mieszkania"}),
    18253: (T + "«Nasz» — лишнее", {"example_pl": "Pies chowa się pod łóżko, gdy tylko zaczynam odkurzać"}),
    18257: (T + "«Nasz» — лишнее", {"example_pl": "Odkurzacz jest tak głośny, że pies za każdym razem ucieka pod łóżko"}),
    18270: (T + "«Ona» — лишнее", {"example_pl": "Mieszka w penthousie w centrum"}),
}

REPLACE = []

SPLIT_LATER = {}
