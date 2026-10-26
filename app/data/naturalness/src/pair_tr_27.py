"""Шаг 2, tr, порция 27: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    7102: (T + "word in example", {"t_tr": "hakkı olmak, yaklaşmak, (auf jemanden zukommen) beklemek"}),
    7108: (T + "word in example", {"t_tr": "vermek, tanımak, (Rabatt) yapmak"}),
    7129: (T + "word in example", {"t_tr": "atlatmak, geçmek, (ayı) çıkarmak"}),
    7145: (T + "word in example", {"t_tr": "geri çekilmek, yol vermek, (nicht weichen) ayrılmamak"}),
    7159: (T + "word in example", {"x_tr": "Yalan söylediğine ne işaret ediyor?"}),
    7176: (T + "word in example", {"t_tr": "neden olmak, sağlamak, (Wunder) yaratmak"}),
    7189: (T + "word in example", {"t_tr": "sinsice yürümek, gizlice girmek"}),
    7196: (T + "word in example", {"t_tr": "birleştirmek, bir araya getirmek"}),
    7212: (T + "word in example", {"t_tr": "parlaklık, ışıltı, ihtişam"}),
    7217: (T + "word in example", {"t_tr": "uyum sağlamak, uyarlamak, (giysiyi) daraltmak"}),
    7282: (T + "word in example", {"t_tr": "değiş tokuş etmek, paylaşmak"}),
    7404: (T + "word in example", {"t_tr": "elinden almak, geri almak, el koymak"}),
}

REPLACE = []
SPLIT_LATER = {}
