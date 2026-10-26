"""Полная вычитка, порция 49: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    16932: (T + "de/tr/pl/cs книжное «нужен пересмотр результатов» — везде «адвокат требует пересмотра дела»", {"example_de": "Der Anwalt fordert eine Revision des Urteils", "example_ru": "Адвокат требует пересмотра дела", "example_uk": "Адвокат вимагає перегляду справи", "example_en": "The lawyer is asking for a review of the case", "example_tr": "Avukat davanın yeniden incelenmesini istiyor", "example_pl": "Adwokat domaga się rewizji wyroku", "example_it": "L'avvocato chiede la revisione del processo", "example_es": "El abogado pide la revisión del juicio", "example_fr": "L'avocat demande une révision du procès", "example_cs": "Advokát žádá revizi rozsudku"}),
    16934: (T + "ru/uk «телефон» — «ключ от машины»", {"example_ru": "Сын спрятал мой ключ от машины и пишет требование выкупа: три мармеладных мишки", "example_uk": "Син сховав мій ключ від машини й пише вимогу викупу: три желейні ведмедики"}),
    17680: (T + "de/tr/pl/cs «датчик движения включает свет» — везде «датчик дождя сам включает дворники»", {"example_de": "Der Sensor schaltet bei Regen die Scheibenwischer von selbst ein", "example_ru": "Датчик дождя сам включает дворники", "example_uk": "Датчик дощу сам вмикає двірники", "example_en": "The rain sensor switches the wipers on by itself", "example_tr": "Sensör yağmur yağınca silecekleri kendiliğinden çalıştırıyor", "example_pl": "Czujnik deszczu sam włącza wycieraczki", "example_it": "Il sensore di pioggia accende da solo i tergicristalli", "example_es": "El sensor de lluvia enciende solo los limpiaparabrisas", "example_fr": "Le capteur de pluie allume les essuie-glaces tout seul", "example_cs": "Senzor deště sám zapíná stěrače"}),
    17726: (T + "de/tr/pl/cs «каждый вечер новости» — везде «канал показывает одни сериалы»", {"example_de": "Dieser Fernsehsender zeigt nur Serien", "example_ru": "Этот телеканал показывает одни сериалы", "example_uk": "Цей телеканал показує лише серіали", "example_en": "This TV channel only shows series", "example_tr": "Bu televizyon kanalı sadece dizi gösteriyor", "example_pl": "Ta stacja telewizyjna pokazuje same seriale", "example_it": "Questo canale televisivo trasmette solo serie", "example_es": "Este canal de televisión solo pone series", "example_fr": "Cette chaîne de télévision ne passe que des séries", "example_cs": "Tahle televizní stanice dává jen seriály"}),
}

REPLACE = []
SPLIT_LATER = {}
