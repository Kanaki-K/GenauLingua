"""Вычитка итальянского, порция p008 (B1), 23.10: повторы («ho sbattuto…», «iscrivermi al corso», «al mercato la verdura»), немецкие фамилии, голые фразы"""

T = "вычитка итальянского: "

FIXES = {
    323: (T + "повтор 1050 «al mercato la verdura è più fresca»", {"example_it": "La verdura la compro dal contadino"}),
    772: (T + "нет слова карточки «sgomberare»", {"example_it": "Entro venerdì dobbiamo sgomberare l'appartamento"}),
    831: (T + "«Vengo qui raramente» — учебниково", {"example_it": "Ci vediamo sempre più raramente"}),
    870: (T + "«Müller» — не итальянская фамилия", {"example_it": "Signora Ferrari, prego, entri nell'ambulatorio"}),
    873: (T + "повтор 874 «Chi … oggi?»", {"example_it": "Lava tu i piatti, io asciugo"}),
    883: (T + "повтор 1068 «Ho sbattuto…»", {"example_it": "Hai la fronte che scotta, hai la febbre?"}),
    921: (T + "повтор 1736 «il tuo numero»", {"example_it": "Ho cambiato numero di telefono"}),
    1009: (T + "«La lavatrice sta andando» — без ситуации", {"example_it": "La lavatrice perde acqua"}),
    1199: (T + "«Scegli qualcosa!» — без ситуации", {"example_it": "Scegli tu il ristorante"}),
    1201: (T + "повтор 1104 «togliersi la giacca/il cappotto»", {"example_it": "Togliti le scarpe, per favore"}),
    1230: (T + "«Il cameriere ci serve bene» — коряво", {"example_it": "La commessa sta servendo un altro cliente"}),
    1241: (T + "повтор 26 «Vorrei iscrivermi al corso»", {"example_it": "All'università mi sono iscritta a un corso di spagnolo"}),
    1302: (T + "«signora Klein» — не итальянская фамилия", {"example_it": "Da noi dell'organizzazione dell'ufficio si occupa la signora Conti"}),
    1308: (T + "«Canto nel coro» — учебниково", {"example_it": "Mia madre canta nel coro della chiesa"}),
    1337: (T + "«Girati» — без ситуации", {"example_it": "Girati, ti sistemo il colletto"}),
    1358: (T + "«Arredo il mio appartamento» — учебниково", {"example_it": "Stiamo ancora arredando la casa nuova"}),
    1384: (T + "«Devo decidermi» — калька", {"example_it": "Non riesco a decidermi"}),
}

REPLACE = []

SPLIT_LATER = {}
