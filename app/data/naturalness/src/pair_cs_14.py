"""Шаг 2, cs, порция 14: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    6366: (T + "в примере nádherně", {"t_cs": "nádherný, překrásný, nádherně"}),
    6369: (T + "в примере odsud", {"t_cs": "vzdálený, (zehn Minuten entfernt) deset minut odsud"}),
    6398: (T + "в примере nesouhlasí", {"t_cs": "sedět, souhlasit, hlasovat"}),
    6417: (T + "в примере prolomí se", {"t_cs": "zlomit, porušit, (Eis) prolomit se"}),
    6506: (T + "в примере snaž se", {"t_cs": "úsilí, námaha, (sich Mühe geben) snažit se"}),
    6527: (T + "в примере kompletně", {"t_cs": "úplně, kompletní, kompletně"}),
    6606: (T + "в примере vytvořila", {"t_cs": "stvořit, vytvořit"}),
    6638: (T + "в примере přináší radost", {"t_cs": "působit, připravit, (Freude bereiten) přinášet radost"}),
    6645: (T + "в примере нет centrální", {"x_cs": "Byt má centrální polohu"}),
    6703: (T + "в примере výborně", {"t_cs": "vynikající, skvělý, výborně"}),
    6707: (T + "в примере mohutná", {"t_cs": "mocný, mohutný, velmi"}),
    6708: (T + "в примере mění, а не proměnit", {"x_cs": "V zimě se jezero promění v kluziště"}),
    6736: (T + "в примере ne zas tak", {"t_cs": "příliš, moc, (nicht allzu) ne zas tak"}),
    6805: (T + "в примере zapnout řetízek", {"t_cs": "nasadit, investovat, (Schmuck) zapnout"}),
}

REPLACE = []
SPLIT_LATER = {}
