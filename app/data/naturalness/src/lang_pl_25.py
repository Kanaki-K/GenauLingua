"""Вычитка польского, порция p025 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    17214: (T + "«Tego lata» → «W te wakacje»", {"example_pl": "W te wakacje jedziemy kamperem do Norwegii"}),
    17226: (T + "«Mój» — лишнее", {"example_pl": "Syn jeździ hulajnogą do szkoły"}),
    17242: (T + "«Czy» — лишнее", {"example_pl": "Jest jeszcze wolne miejsce w Państwa przedziale?"}),
    17255: (T + "«potrzebuje diesla» — калька", {"example_pl": "Moje auto jeździ na dieslu, nie na benzynie"}),
    17274: (T + "fährt LKW — профессия", {"example_pl": "Brat jeździ na ciężarówce"}),
    17294: (T + "«swoim» — лишнее", {"example_pl": "Jeździ do pracy starym motorowerem"}),
    17474: (T + "«każdego ranka» → «co rano»", {"example_pl": "Przez remont torów do Wielkanocy jeździ komunikacja zastępcza i co rano jadę pół godziny dłużej"}),
    17485: (T + "порядок слов", {"example_pl": "Słaby tu sygnał"}),
    17504: (T + "«Mój» — лишнее", {"example_pl": "Syn buduje z Lego statek kosmiczny"}),
    17520: (T + "«Moja» — лишнее", {"example_pl": "Zepsuła mi się krótkofalówka"}),
    17523: (T + "«Mój profil … jest» — калька", {"example_pl": "Mam prywatny profil w mediach społecznościowych"}),
    17526: (T + "«To jest» → «To»", {"example_pl": "To problem techniczny"}),
    17530: (T + "«bateria … jest pusta» — калька", {"example_pl": "W latarce padła bateria"}),
    17554: (T + "«w moim komputerze» — лишнее", {"example_pl": "Mam pełny dysk twardy w komputerze"}),
    17576: (T + "пассив → актив", {"example_pl": "Saperzy rozbroili zapalnik bomby"}),
    17578: (T + "«jest zepsuta» → «nie działa»", {"example_pl": "Winda nie działa, musimy iść po schodach"}),
    17587: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez awarię się spóźnimy"}),
    17619: (T + "«swój» — лишнее", {"example_pl": "Dasz mi numer komórki?"}),
    17627: (T + "«Mój» — лишнее", {"example_pl": "Komputer ciągle mi się zawiesza"}),
    17683: (T + "«ją» — лишнее", {"example_pl": "Głośność jest za duża, możesz przyciszyć?"}),
    17700: (T + "«stacja gra» — калька", {"example_pl": "W mojej ulubionej stacji radiowej zawsze leci dobra muzyka"}),
    17742: (T + "«Twój» — лишнее", {"example_pl": "Telefon ci wibruje, ktoś dzwoni"}),
    17775: (T + "«ma mały handel» — калька", {"example_pl": "Wujek zajmuje się drobnym handlem używanymi rowerami"}),
    17779: (T + "«dba o swoje» — лишнее", {"example_pl": "Rolnik codziennie zajmuje się bydłem"}),
    17784: (T + "«jest bardzo silna» — калька", {"example_pl": "W tej branży jest duża konkurencja"}),
    17810: (T + "«jest w przyszłym» → «będzie»", {"example_pl": "Otwarcie nowej restauracji będzie w przyszłym tygodniu"}),
    17928: (T + "«występuje już tylko rzadko» — книжно", {"example_pl": "Ten gatunek jest już rzadko spotykany"}),
    17930: (T + "«zrobiony z» — лишнее", {"example_pl": "Ten stół jest z metalu"}),
    17941: (T + "«Logika … jest błędna» — калька", {"example_pl": "W twoim argumencie nie ma logiki"}),
    18081: (T + "«Mój» — лишнее", {"example_pl": "Siostrzeniec chce kiedyś zostać odkrywcą i pojechać do dżungli"}),
    18177: (T + "«Moje mieszkanie jest» — калька", {"example_pl": "Mieszkam na trzecim piętrze"}),
}

REPLACE = []

SPLIT_LATER = {}
