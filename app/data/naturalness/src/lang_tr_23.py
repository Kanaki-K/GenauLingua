"""Вычитка турецкого, порция p023 (B1), 23.10: семья, природа, животные — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    15186: (T + "младенец не «bağırıyor», а плачет", {"example_tr": "Gündüzleri küçük bir melek, ama geceleri bağıra bağıra ağlıyor"}),
    15243: (T + "«Daha bu kadar küçük bir ufaklık» — тяжело", {"example_tr": "Bu kadar ufacık ama ne kadar da yaramaz!"}),
    15443: (T + "«yumurta yumurtluyor» — тавтология", {"example_tr": "Tavuk her gün bir yumurta yapıyor"}),
    15470: (T + "«kalındır» — книжно", {"example_tr": "Ağacın gövdesi çok kalın"}),
    15475: (T + "«Bu geceki don çok şiddetliydi» — калька", {"example_tr": "Dün gece çok sert don vardı"}),
    15628: (T + "Brötchen — не «sandviç»", {"example_tr": "Bir martı gagasıyla ekmeğimi kaptı"}),
    15727: (T + "птица «ötüyor», не «şarkı söylüyor»", {"example_tr": "İspinoz sabahları güzel ötüyor"}),
    15743: (T + "«tuzlu suyu duşta yıkıyorum» — коряво", {"example_tr": "Denizden çıkınca duş alıp tuzlu suyu üzerimden atıyorum"}),
    15770: (T + "«yosunlar büyür ve suyu yeşil yapar» — подстрочник", {"example_tr": "Gölde yosun çoğalıyor, su yemyeşil oluyor"}),
    15859: (T + "канарейка «ötüyor»", {"example_tr": "Kanarya her sabah yüksek sesle ötüyor"}),
}

REPLACE = []

SPLIT_LATER = {}
