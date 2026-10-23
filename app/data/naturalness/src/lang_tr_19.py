"""Вычитка турецкого, порция p019 (B1), 23.10: чувства, еда — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    10443: (T + "«tehditkar bir durumdu» — книжно", {"example_tr": "Durum gerçekten tehlikeliydi"}),
    10448: (T + "«Yazık ki maç…» — порядок", {"example_tr": "Maçın iptal edilmesi çok yazık"}),
    10449: (T + "«O, güvenilebilecek…» — тяжело", {"example_tr": "Her zaman güvenebileceğin sadık bir dosttur"}),
    10450: (T + "«O, … tamamen aşık» — подстрочник", {"example_tr": "Sınıf arkadaşına fena halde âşık"}),
    10454: (T + "«O mütevazı bir insandır ve…» — тяжело", {"example_tr": "Mütevazı bir insandır, pek konuşmaz"}),
    10457: (T + "«Vatanıma» — пафосно; о доме «memleket»", {"example_tr": "Memleketime büyük bir özlem duyuyorum"}),
    10463: (T + "«Onun gelmeyeceğinden endişeleniyorum» — тяжело", {"example_tr": "Korkarım gelmeyecek"}),
    10465: (T + "«işkence ediyor» — слишком сильно для quälen", {"example_tr": "Bu düşünceler ona her gün eziyet ediyor"}),
    10532: (T + "«yanağa öpücük veriyor» — калька", {"example_tr": "Vedalaşırken yanağıma küçük bir öpücük konduruyor"}),
    10805: (T + "klingt — «kulağa geliyor»", {"example_tr": "Bu kulağa oldukça endişe verici geliyor"}),
    10834: (T + "«sonu ifşa etme» — книжно", {"example_tr": "Lütfen bana sonunu söyleme"}),
    10853: (T + "«Bu, senin dâhiyane bir fikrindi» — тяжело", {"example_tr": "Ne dâhiyane bir fikirdi bu!"}),
    11082: (T + "«Favori rengim» — калька", {"example_tr": "En sevdiğim renk mavi"}),
    11136: (T + "«Gündelik yaşam … telaşlı» — книжно", {"example_tr": "Şu sıralar hayatım çok telaşlı"}),
    11229: (T + "«tamamen kaçık mısın?» — подстрочник", {"example_tr": "Sen iyice kafayı mı yedin?"}),
    11266: (T + "«Onun bencilliği» — лишнее «onun»", {"example_tr": "Bencilliği başkalarını anlamasını engelliyor"}),
    11350: (T + "«O gerçek bir egoist» — подстрочник", {"example_tr": "Tam bir egoist"}),
    11352: (T + "«pek sevilmeyen biri» — калька", {"example_tr": "Yeni şefi kimse pek sevmiyor"}),
    11481: (T + "«yatmak ve … okumak çok rahat» — коряво", {"example_tr": "Sıcacık bir battaniyenin altında uzanıp kitap okumak çok keyifli"}),
    11667: (T + "«Çok nefis» — тавтология", {"example_tr": "Ne nefis kokuyor!"}),
    12024: (T + "Brathähnchen — по-турецки «piliç çevirme»", {"translation_tr": "piliç çevirme, ızgara tavuk", "example_tr": "Cumaları pazardan piliç çevirme alıyoruz"}),
}

REPLACE = []

SPLIT_LATER = {}
