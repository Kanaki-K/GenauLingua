"""Шаг 2, cs, порция 36: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    16275: (T + "в примере policejní šéf, не šéf policie", {"x_cs": "Šéf policie mluví s médii o nových opatřeních"}),
    16305: (T + "в примере нет místo pro svědky", {"x_cs": "Zítra musí sousedka u soudu na místo pro svědky, viděla tu nehodu"}),
    16326: (T + "в примере только technici", {"x_cs": "V detektivkách kriminalističtí technici vždycky někde najdou vlas"}),
    16574: (T + "в примере глагол vybral", {"t_cs": "vyvolený, vybraný, (sich erwählen) vybrat si"}),
    16853: (T + "в примере просто cela", {"t_cs": "cela předběžného zadržení, cela"}),
    16899: (T + "в примере просто krádeže", {"x_cs": "V našem supermarketu teď všude visí kamery, protože je tam tolik krádeží v obchodě"}),
}

REPLACE = []
SPLIT_LATER = {}
