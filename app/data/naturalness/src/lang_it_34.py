"""Вычитка итальянского, порция p034 (B2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    14465: (T + 'повтор 15429 «far volare un aquilone»', {"example_it": 'Nella fiaba il cavaliere uccide il drago'}),
    14512: (T + 'повтор 12141 «gli spettatori applaudono forte»', {"example_it": 'I bambini applaudono a ogni trucco del mago'}),
    14526: (T + 'учебниково', {"example_it": "Il cappellano dell'ospedale passa a trovare i malati"}),
    14541: (T + '«La mia famiglia religiosa celebra» — калька', {"example_it": 'I miei nonni sono molto religiosi'}),
    15045: (T + '«è molto felice con noi» — коряво', {"example_it": 'Il loro figlio adottivo viene dalla Colombia'}),
    15106: (T + '«spätzle» — не итальянский быт', {"example_it": 'La mia matrigna mi ha insegnato a fare le crespelle'}),
}

REPLACE = []

SPLIT_LATER = {}
