"""Вычитка турецкого, порция p020 (B1), 23.10: спорт, медицина — кальки и опечатки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    12134: (T + "«Bir gol daha, kazanırız!» — оборвано", {"example_tr": "Bir gol daha atarsak kazanırız!"}),
    12139: (T + "streng — строгий, «katı», не «sert»", {"example_tr": "Antrenörümüz çok katı"}),
    12143: (T + "«kötü bir kaybeden» — калька", {"example_tr": "Kimse kaybetmeyi bilmeyen birini sevmez"}),
    12175: (T + "«Oyuna katılmak ister misin?» — книжно", {"example_tr": "Sen de oynamak ister misin?"}),
    12243: (T + "«Hâlâ bir amatör» — подстрочник", {"example_tr": "Daha amatör ama çok yetenekli"}),
    12271: (T + "«onun büyük tutkusu» — лишнее «onun»", {"example_tr": "Video oyunları en büyük tutkusu"}),
    12318: (T + "«çoktan aldın mı?» — неестественно", {"example_tr": "Konser biletini şimdiden aldın mı?"}),
    12326: (T + "«O bir maceraperest» — подстрочник", {"example_tr": "Maceraperest biri, hiçbir yerde uzun kalmıyor"}),
    12340: (T + "«Benim favori filmim» — калька", {"example_tr": "En sevdiğim film 80'lerin bir klasiği"}),
    12364: (T + "«oynarız» — привычка, а в примере сейчас", {"example_tr": "Parkta frizbi oynuyoruz"}),
    12404: (T + "«şans numaram» — по-турецки «şanslı sayım»", {"example_tr": "Şanslı sayım yedi"}),
    12521: (T + "«doktorun onu dikmesi» — коряво", {"example_tr": "Yara derin, doktorun dikiş atması lazım"}),
    12531: (T + "«Hemen çiş yapmam lazım» — грубовато", {"example_tr": "Bir çişe gitmem lazım"}),
    12560: (T + "«Onun akciğer sorunu var» — подстрочник", {"example_tr": "Akciğerlerinde sorun var"}),
    12570: (T + "«Kazadan kaynaklanan» — канцелярит", {"example_tr": "Kazadan kalan yara izi hâlâ alnında duruyor"}),
    12588: (T + "«vebadan nefret eder gibi» — калька идиомы", {"example_tr": "Bu sivrisineklerden ölesiye nefret ediyorum"}),
    12601: (T + "«O … bağımlısıdır» — книжно", {"example_tr": "Uyuşturucu bağımlısı"}),
    12602: (T + "«Onun kalp atışı» — лишнее «onun»", {"example_tr": "Kalp atışı çok hızlı"}),
    12622: (T + "«özürlü» — устаревшее, обидное слово", {"translation_tr": "engelli"}),
    12625: (T + "«O kahveye bağımlı» — подстрочник", {"example_tr": "Tam bir kahve bağımlısı"}),
    12630: (T + "«tamamen ıslak oluyorum» — калька", {"example_tr": "Spor yaparken terliyorum ve sırılsıklam oluyorum"}),
    12641: (T + "опечатка «Anneanemin»", {"example_tr": "Anneannemin bakıma ihtiyacı var"}),
    12857: (T + "«Bir kaburga kırdım» — калька", {"example_tr": "Kaburgam kırıldı ve çok ağrıyor"}),
    12972: (T + "«cildinde güneş yanığı olur» — тяжело", {"example_tr": "Krem sür, yoksa güneşte yanarsın"}),
}

REPLACE = []

SPLIT_LATER = {}
