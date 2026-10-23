"""Вычитка польского, порция p018 (B1), 23.10: кальки и лишние местоимения → разговорный польский"""

T = "вычитка польского: "

FIXES = {
    10084: (T + "«On to» — лишнее", {"example_pl": "To dobra dusza"}),
    10092: (T + "«jest uznawany za» — канцелярит", {"example_pl": "Od wczoraj zaginiony jest chłopiec z naszej wsi"}),
    10093: (T + "«To jest» — тяжело", {"example_pl": "To naprawdę dziwne"}),
    10108: (T + "«On … pozostaje» — книжно", {"example_pl": "Zawsze jest spokojny"}),
    10111: (T + "«Mój» — лишнее", {"example_pl": "Syn boi się potworów pod łóżkiem"}),
    10118: (T + "«Czy możesz» — книжно", {"example_pl": "Wybaczysz mi?"}),
    10125: (T + "«zupełnie śmieszne» — смысл", {"example_pl": "To jest po prostu żałosne"}),
    10135: (T + "«To jest» — тяжело", {"example_pl": "To duża odpowiedzialność"}),
    10150: (T + "«On» — лишнее", {"example_pl": "Chce zemsty za wszystko"}),
    10166: (T + "«wybuchł … wybuchła» — повтор", {"example_pl": "Kiedy zaczął się pożar, wybuchła panika"}),
    10173: (T + "«To nie był mój zamiar» — калька", {"example_pl": "Nie miałem takiego zamiaru"}),
    10181: (T + "«on» — лишнее", {"example_pl": "To dziwne, nigdy się nie spóźnia"}),
    10190: (T + "«każdego wieczoru» — книжно", {"example_pl": "Co wieczór przed kolacją się modlimy"}),
    10194: (T + "«Jestem zdezorientowany zadaniem» — калька", {"example_pl": "To zadanie zupełnie mnie zdezorientowało"}),
    10197: (T + "«Pana» — регистр", {"example_pl": "Jestem bardzo rad, że mogę pana poznać"}),
    10201: (T + "«Mój» — лишнее", {"example_pl": "Syn to prawdziwy geniusz z matematyki"}),
    10202: (T + "«Ona» — лишнее", {"example_pl": "Ma wielki talent do muzyki"}),
    10222: (T + "«Ona» — лишнее", {"example_pl": "Jest zdolna do wszystkiego"}),
    10227: (T + "«Nastrój jest świetny» — калька", {"example_pl": "Jest tu świetna atmosfera"}),
    10238: (T + "«On» — лишнее", {"example_pl": "Ma na mnie duży wpływ"}),
    10239: (T + "«To jest» — тяжело", {"example_pl": "To naprawdę zdumiewające"}),
    10256: (T + "«Ja, głupek,» — калька", {"example_pl": "Ale ze mnie głupek, zostawiłem włączone światło"}),
    10264: (T + "«Mój» — лишнее", {"example_pl": "Brat się zemścił i schował wszystkie moje skarpetki"}),
    10282: (T + "«Ona» — лишнее", {"example_pl": "Ma uroczą małą córeczkę"}),
    10308: (T + "«Moja» — лишнее", {"example_pl": "Córka jest bardzo nieśmiała"}),
    10319: (T + "«On» — лишнее", {"example_pl": "Ma silny charakter"}),
    10346: (T + "«To jest zupełnie» — тяжело", {"example_pl": "To kompletnie absurdalne"}),
    10348: (T + "«On jest … bardzo» — тяжело", {"example_pl": "Jest naprawdę czarujący"}),
    10357: (T + "«Ona» — лишнее", {"example_pl": "Ma naprawdę silną osobowość"}),
    10361: (T + "«Panu» — регистр", {"example_pl": "Czy mogę panu w czymś pomóc?"}),
    10370: (T + "«nędznie» — книжно", {"example_pl": "Czuję się dziś fatalnie"}),
    10374: (T + "«swojej» — лишнее", {"example_pl": "Przestań dokuczać siostrze"}),
    10381: (T + "«odwołano jego pociąg» — книжно", {"example_pl": "Był dość wzburzony, bo odwołali mu pociąg"}),
    10386: (T + "«każdego ranka» — книжно", {"example_pl": "Mama przytula mnie co rano"}),
    10387: (T + "«to jest słuszne» — тяжело", {"example_pl": "Jestem niepewny, czy to słuszne"}),
    10405: (T + "«Pracuje bardzo skupiony» — грамматика", {"example_pl": "Przy pracy jest bardzo skupiony"}),
    10409: (T + "«Ona» — лишнее", {"example_pl": "Jest zazdrosna o moją nową pracę"}),
    10410: (T + "«Ona jest» — тяжело", {"example_pl": "To kłamczucha, nie można jej wierzyć ani w jedno słowo"}),
    10416: (T + "«On» — лишнее", {"example_pl": "Ma w sobie dużo uroku"}),
    10417: (T + "«Mój» — лишнее", {"example_pl": "Tata jest dla mnie wielkim wzorem"}),
    10418: (T + "«moich» — лишнее", {"example_pl": "Potrzebuję oderwania się od problemów"}),
    10421: (T + "«Moja skóra jest» — калька", {"example_pl": "Mam wrażliwą skórę"}),
}

REPLACE = []

SPLIT_LATER = {}
