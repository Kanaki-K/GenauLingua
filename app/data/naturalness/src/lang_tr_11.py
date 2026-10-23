"""Вычитка турецкого, порция p011 (B1), 23.10: кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    2150: (T + "«koyma yeri» — так не говорят", {"translation_tr": "eşya koyacak yer, park yeri", "example_tr": "Bodrumda bisiklet ve bebek arabası koymak için bir yer var"}),
    2169: (T + "«artık resmî mi?» — подстрочник", {"example_tr": "Taşınmanız artık resmîleşti mi?"}),
    2185: (T + "«varsayımından hareket ediyorum» — канцелярит", {"example_tr": "Geleceğini varsayıyorum"}),
    2225: (T + "«aile tarihini ele alıyor» — канцелярит", {"example_tr": "Babasının ölümünden beri aile geçmişiyle çok uğraşıyor"}),
    2254: (T + "«dinozorlar konusunda heyecanlı» — подстрочник", {"example_tr": "Oğlum dinozorlara bayılıyor"}),
    2264: (T + "«bana yük oluyor» — о чувствах «yıpratıyor»", {"example_tr": "Bu beni çok yıpratıyor"}),
    2293: (T + "«Bunu değerlendiremiyorum» — неестественно", {"example_tr": "Bunu değerlendirecek durumda değilim"}),
    2320: (T + "«tükenmez kalemler yok» — тяжело", {"example_tr": "Biri hep ofis malzemesini eve götürüyor, yine bütün tükenmezler kaybolmuş"}),
    2361: (T + "«sadece matematikte değil» = «не только в математике» — смысл наоборот", {"example_tr": "Notlarım matematik hariç sınıf ortalamasının üstünde"}),
    2378: (T + "в примере потерялась школа", {"example_tr": "Okul seneden itibaren bilgisayar dersi getiriyor"}),
    2445: (T + "«O bu alanda uzman» — лишнее «O»", {"example_tr": "Bu alanda uzman"}),
}

REPLACE = []

SPLIT_LATER = {}
