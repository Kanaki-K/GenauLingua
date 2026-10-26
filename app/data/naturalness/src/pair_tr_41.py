"""Шаг 2, tr, порция 41: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    11157: (T + "word in example", {"t_tr": "defne, zafer (mecazi), (sich auf Lorbeeren ausruhen) başarısının üstüne yatmak"}),
    11602: (T + "word in example", {"t_tr": "dehşet, nefret edilen şey, (ein Gräuel sein) kâbus gibi olmak"}),
    12506: (T + "word in example", {"t_tr": "surat (kaba), (halt die Fresse) çeneni kapa"}),
    12800: (T + "word in example", {"t_tr": "sarhoşluk, (Trunkenheit am Steuer) alkollü araç kullanma"}),
}

REPLACE = []
SPLIT_LATER = {}
