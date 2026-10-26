"""Шаг 2, tr, порция 32: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    11752: (T + "word in example", {"t_tr": "servis etmek, zarar vermek, (Chaos anrichten) kargaşa çıkarmak"}),
    12232: (T + "word in example", {"t_tr": "mücadele etmek, güreşmek, (nach Luft ringen) nefes nefese kalmak"}),
    12337: (T + "word in example", {"t_tr": "kafa yormak, düşünüp durmak"}),
    12356: (T + "word in example", {"t_tr": "ayrılma, atlayış, (den Absprung schaffen) bırakmayı başarmak"}),
    12642: (T + "word in example", {"t_tr": "işitme, kulak"}),
    12709: (T + "word in example", {"t_tr": "hafifletmek, dindirmek, iyi gelmek"}),
    12713: (T + "word in example", {"t_tr": "sarhoşluk, (Rausch ausschlafen) uyuyup ayılmak"}),
    12737: (T + "word in example", {"t_tr": "bakım, tedarik, hizmet"}),
    12768: (T + "word in example", {"t_tr": "ruhsal, psikolojik, ruh (sağlığı)"}),
}

REPLACE = []
SPLIT_LATER = {}
