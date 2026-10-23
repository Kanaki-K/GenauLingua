"""Вычитка турецкого, порция p014 (B1), 23.10: опечатки, кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    3066: (T + "«iyi bir şekilde birlikte çalışıyoruz» — подстрочник", {"example_tr": "Yıllardır çok iyi anlaşarak birlikte çalışıyoruz"}),
    3067: (T + "«birlikte yaşamak uyumlu» — коряво", {"example_tr": "Anne babamla birlikte yaşamak hiç sorun değil, çok uyumluyuz"}),
    6226: (T + "«öldürebilirim» — «могу убить», а это крик в сердцах", {"example_tr": "Onu öldürürüm!"}),
    6353: (T + "опечатка «Bereğini» — правильно «Bereni»", {"example_tr": "Bereni tak, bu bir emir!"}),
    6383: (T + "«Hâlâ pasta kaldı» — подстрочник", {"example_tr": "Pastadan biraz daha kaldı"}),
    6418: (T + "«kavrayamıyorum» — книжно для «не могу поверить»", {"example_tr": "Aklım almıyor"}),
    6475: (T + "«korunmaya ihtiyacımız var» — канцелярит", {"example_tr": "Yağmurdan korunacak bir yer lazım"}),
    6520: (T + "«Hadi sadece devam edelim» — подстрочник «einfach»", {"example_tr": "Boş ver, devam edelim"}),
    6525: (T + "«kocaman bir problem» — по-турецки «büyük sorun»", {"example_tr": "Bu çok büyük bir sorun"}),
    6570: (T + "«mükemmel şekilde işe yaradı» — подстрочник", {"example_tr": "Her şey harika gitti"}),
    6571: (T + "«O şehirde…» — двусмысленно («тот город»)", {"example_tr": "Şehirde saygın bir doktordur"}),
    6625: (T + "sicherlich — «herhalde», не «kesinlikle»", {"example_tr": "Yolculuktan sonra herhalde acıkmışsındır"}),
    6687: (T + "«Görev» — служебное задание", {"example_tr": "Bu iş sadece görünüşte kolay"}),
    6718: (T + "genauer erklären — «подробнее»", {"example_tr": "Bunu daha ayrıntılı açıklayabilir misin?"}),
    6729: (T + "«Onun mesajlarını» — лишнее «onun»", {"example_tr": "Mesajlarını gizlice okudu"}),
    6741: (T + "«benim yanlışlığımdı» — коряво", {"example_tr": "Yanlışlıkla oldu, benim hatam"}),
    6751: (T + "«kendin değiştirebilir misin?» — «man» обобщённое", {"example_tr": "Pil kendi başına değiştirilebiliyor mu?"}),
    6758: (T + "«oldukça mümkün» — калька", {"example_tr": "Bu pekâlâ mümkün"}),
    6762: (T + "«Yine görün bize!» — «arada bir»", {"example_tr": "Arada bir görün bize!"}),
    6773: (T + "в паркинге Ebene — этаж", {"example_tr": "Otoparkın üçüncü katında buluşalım"}),
    6784: (T + "«ek trenler koyuyor» — по-турецки «sefer»", {"example_tr": "Bayram boyunca demiryolu ek seferler koyuyor"}),
    6785: (T + "«sözünü kısaca kesebilir miyim» — подстрочник", {"example_tr": "Pardon, bir saniye sözünü kesebilir miyim?"}),
    6790: (T + "«O kurnaz bir iş adamı» — лишнее «O»", {"example_tr": "Kurnaz bir iş adamıdır"}),
}

REPLACE = []

SPLIT_LATER = {}
