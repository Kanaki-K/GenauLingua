"""Вычитка польского, порция p036 (B2), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    16280: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez kolano córka dostała zwolnienie z WF-u"}),
    16303: (T + "«naszego» — лишнее", {"example_pl": "Dla kota nowe dziecko jest na razie intruzem"}),
    16309: (T + "«Mój» — лишнее", {"example_pl": "Kuzyn jest policjantem i nocami jeździ na patrol"}),
    16310: (T + "«Mój» — лишнее", {"example_pl": "Wujek był kiedyś pilotem w siłach powietrznych"}),
    16318: (T + "«mój» — лишнее", {"example_pl": "W paintballu brat jest zawsze naszym snajperem, trafia prawie każdego"}),
    16320: (T + "«Nasz … swojego» — лишнее", {"example_pl": "Kocur broni całego ogrodu jak własnego terytorium"}),
    16322: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez hałaśliwą budowę napisałem list do naszej posłanki"}),
    16327: (T + "порядок, «z powodu» → «przez»", {"example_pl": "Przez terroryzm od czasu zamachów kontrole na lotnisku są dużo surowsze"}),
    16337: (T + "«Mój» — лишнее", {"example_pl": "Wujek był w wojsku dowódcą prawie tysiąca żołnierzy"}),
    16342: (T + "«Mój» — лишнее", {"example_pl": "Wujek w Teksasie od czterdziestu lat zawsze głosuje na republikanów"}),
    16350: (T + "«mój» — лишнее", {"example_pl": "Po maturze kuzyn zaciągnął się na cztery lata do sił zbrojnych"}),
    16357: (T + "«Mój» — лишнее", {"example_pl": "Pradziadek był zagorzałym komunistą i co niedzielę kłócił się z księdzem"}),
    16362: (T + "«Jego» — лишнее", {"example_pl": "Kurator sądowy pomaga mu po wyjściu z więzienia"}),
    16367: (T + "«mój» — лишнее", {"example_pl": "Przy każdych mistrzostwach świata zwykle spokojny sąsiad staje się wielkim patriotą i wywiesza flagi"}),
    16371: (T + "«Ponieważ» — книжно", {"example_pl": "Duże firmy utworzyły kartel, więc cukier przez lata był za drogi"}),
    16372: (T + "«Nasz» — лишнее", {"example_pl": "Szczeniak to mały niszczyciel, pogryzł już trzy pary butów"}),
    16380: (T + "«Moja» — лишнее", {"example_pl": "Młodsza siostra bawi się w królową, a my musimy być jej poddanymi"}),
    16396: (T + "«Mój» — лишнее", {"example_pl": "Pradziadek służył w czasie wojny w piechocie i nigdy nie potrafił o tym mówić"}),
    16407: (T + "«Nasz» — лишнее", {"example_pl": "Sąsiad kiedyś odsiedział trzy lata, a dziś jest najmilszym człowiekiem w całym bloku"}),
    16439: (T + "«dla swojego» — коряво", {"example_pl": "Koleżanka z pracy dostała tymczasowy zakaz zbliżania się wobec agresywnego byłego"}),
    16470: (T + "«Nasi» — лишнее", {"example_pl": "Znajomi mieszkają w Indiach w wiejskim dystrykcie, gdzie do najbliższego supermarketu są dwie godziny"}),
    16510: (T + "«mój bilet był» — калька", {"example_pl": "Przy kontroli okazało się, że mam nieważny bilet, bo przez pomyłkę kupiłem złą strefę"}),
    16524: (T + "«mój» — лишнее", {"example_pl": "Od zeszłego roku mąż jest obywatelem Niemiec i wreszcie może głosować"}),
    16580: (T + "«mojej» — лишнее", {"example_pl": "W partii babci wszyscy wciąż mówią do siebie towarzyszko i towarzyszu"}),
    16632: (T + "«najlepsze, co jest zimą» — коряво", {"example_pl": "Gorące kakao uwieńczone górą bitej śmietany to dla mnie najlepsza rzecz zimą"}),
    16755: (T + "«Nasz» — лишнее", {"example_pl": "Kocur zachowuje się jak monarcha, siedzi w najlepszym fotelu i każe się obsługiwać"}),
    16769: (T + "«Mój» — лишнее", {"example_pl": "Synek salutuje za każdym razem, gdy obok przejeżdża radiowóz"}),
    16786: (T + "«nasz» — лишнее", {"example_pl": "Za nadgryziony tort głównym podejrzanym jest pies, ma jeszcze śmietanę na nosie"}),
    16787: (T + "«Mój» — лишнее", {"example_pl": "Kuzyn pracuje w MSW i nigdy nie może nam powiedzieć, nad czym pracuje"}),
    16788: (T + "«Moja» — лишнее", {"example_pl": "Przyjaciółka z Kanady nie rozumie naszego systemu prawnego: po co do wszystkiego pieczątka?"}),
    16796: (T + "«Moja» — лишнее", {"example_pl": "Ciocia z Ohio napisała list do swojego kongresmena, bo droga przed jej domem jest pełna dziur"}),
    16867: (T + "«z powodu zakłócania» — порядок", {"example_pl": "Na naszych urodzinach sąsiedzi wezwali policję za zakłócanie ciszy, o wpół do jedenastej"}),
    16926: (T + "«noszę trzy swetry» — смысл", {"example_pl": "W samolocie dopuszczalne jest tylko osiem kilo bagażu podręcznego, więc mam na sobie trzy swetry jeden na drugim"}),
    16935: (T + "«poszukuję» — книжно", {"example_pl": "Od godziny szukam pilota po całym mieszkaniu"}),
    16954: (T + "«mojej» — лишнее", {"example_pl": "Rodzina szwagierki jest szlachecka, ale mieszkają zupełnie zwyczajnie w wynajętym mieszkaniu"}),
    16964: (T + "«Z powodu» → «Przez»", {"example_pl": "Przez zamknięcie centrum na maraton mąż jedzie dziś do pracy rowerem"}),
    16979: (T + "«Mój» — лишнее", {"example_pl": "Sąsiad zasiada w radzie gminy i chce wreszcie wywalczyć światła przed szkołą"}),
    17146: (T + "«Mój wyjazd jest» — калька", {"example_pl": "Wyjazd mam jutro o siódmej rano"}),
    17154: (T + "«przyspieszyć tempo» — повтор", {"example_pl": "Możemy trochę przyspieszyć?"}),
    17158: (T + "«wkrótce» → «zaraz»", {"example_pl": "Goście powinni zaraz przybyć"}),
    17164: (T + "«w moim rowerze» — калька", {"example_pl": "Siodełko w rowerze mam o wiele za wysoko, nie sięgam stopami ziemi"}),
    17165: (T + "«cała moja praca zniknęła» — калька", {"example_pl": "Po awarii komputera przepadła mi cała praca pisemna"}),
}

REPLACE = []

SPLIT_LATER = {}
