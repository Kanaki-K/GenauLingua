"""Вычитка турецкого, порция p003 (A1–A2), 23.10: кальки, неверные слова → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    1385: (T + "«Affedersiniz, lütfen» — лишнее «lütfen»", {"example_tr": "Affedersiniz"}),
    1694: (T + "«Beraber geliyor musun?» — подстрочник", {"example_tr": "Sen de geliyor musun?"}),
    1946: (T + "«bir test yapıyoruz» — калька", {"example_tr": "Yarın test olacağız"}),
    2092: (T + "в анкете не спрашивают «erkek mi, kadın mı»", {"example_tr": "Lütfen işaretleyin: erkek veya kadın"}),
    2093: (T + "слово «çünkü» потерялось в примере", {"example_tr": "Evde kalıyorum çünkü hastayım"}),
    2793: (T + "выключатель — «düğme», а не «anahtar» (ключ)", {"translation_tr": "düğme, gişe", "example_tr": "Işığın düğmesi kapının yanında"}),
    6400: (T + "«Bu gerçek bir arkadaş» — о человеке «o»", {"example_tr": "O gerçek bir dost"}),
    6405: (T + "«sessizce konuş» — «тихо» о голосе = «alçak sesle»", {"translation_tr": "sessiz, alçak sesle", "example_tr": "Lütfen alçak sesle konuş"}),
    6483: (T + "в квартире «oturmak», не «yaşamak»", {"example_tr": "İkinci katta oturuyorum"}),
    8797: (T + "«Meslektaşım işte…» — книжно", {"example_tr": "İş arkadaşım bana yardım ediyor"}),
    8870: (T + "«O üç aydır işsizdir» — книжно", {"example_tr": "Üç aydır işsiz"}),
    10027: (T + "«Kahveden çok çayı» — неверная конструкция", {"example_tr": "Çayı kahveye tercih ederim"}),
    12214: (T + "«kulübündeyim» — «нахожусь в клубе»", {"example_tr": "Futbol kulübüne üyeyim"}),
    12459: (T + "«Fare ölü mü?» — неестественно", {"example_tr": "Fare ölmüş mü?"}),
    13259: (T + "«Çoktan hazırım» — fertig здесь «закончил»", {"example_tr": "Ben çoktan bitirdim"}),
    13262: (T + "«Hele buraya gel» — грубовато", {"example_tr": "Bir buraya gel"}),
    15084: (T + "слово «ev hanımı», в примере было «ev kadını»", {"example_tr": "Annem ev hanımı, evin bütün işleriyle o ilgileniyor"}),
    16112: (T + "«man» — обобщённо, не «ты»", {"example_tr": "İnsan hemen yargılamamalı"}),
    17250: (T + "«daireyi geziyoruz» — смотрим квартиру перед арендой", {"example_tr": "Bugün yeni daireyi gezip göreceğiz"}),
    17834: (T + "das Gut = имение, не «mal» (имущество)", {"translation_tr": "çiftlik, malikâne"}),
}

REPLACE = []

SPLIT_LATER = {}
