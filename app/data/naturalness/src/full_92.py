"""Полная вычитка, порция 92: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    13888: (T + "двойник с 1698 «у меня для вас сообщение» — везде «послание фильма простое»", {"example_de": "Die Botschaft des Films ist ganz einfach", "example_ru": "Послание фильма очень простое", "example_uk": "Послання фільму дуже просте", "example_en": "The film's message is very simple", "example_tr": "Filmin mesajı çok basit", "example_pl": "Przesłanie filmu jest bardzo proste", "example_it": "Il messaggio del film è molto semplice", "example_es": "El mensaje de la película es muy sencillo", "example_fr": "Le message du film est très simple", "example_cs": "Poselství filmu je úplně jednoduché"}),
    18315: (T + "двойник с 1545 «дети во дворе» и 473 «велосипеды в подвале» — везде «соседка вешает бельё на заднем дворе»", {"example_de": "Im Hinterhof hängt die Nachbarin ihre Wäsche auf", "example_ru": "Соседка развешивает бельё на заднем дворе", "example_uk": "Сусідка розвішує білизну на задньому дворі", "example_en": "The neighbour hangs her washing out in the back courtyard", "example_tr": "Komşu kadın çamaşırlarını arka avluya asıyor", "example_pl": "Sąsiadka wiesza pranie na podwórku za domem", "example_it": "La vicina stende il bucato nel cortile interno", "example_es": "La vecina tiende la ropa en el patio interior", "example_fr": "La voisine étend son linge dans l'arrière-cour", "example_cs": "Sousedka věší prádlo na dvorku za domem"}),
    18736: (T + "двойник с 18607 «пока всё шло хорошо» — везде «никто не откликнулся на объявление»", {"example_de": "Bislang hat sich niemand auf die Anzeige gemeldet", "example_ru": "Пока что на объявление никто не откликнулся", "example_uk": "Поки що на оголошення ніхто не відгукнувся", "example_en": "So far nobody has answered the ad", "example_tr": "Şimdiye kadar ilana kimse dönmedi", "example_pl": "Jak dotąd nikt nie odpowiedział na ogłoszenie", "example_it": "Finora nessuno ha risposto all'annuncio", "example_es": "Hasta ahora nadie ha respondido al anuncio", "example_fr": "Jusqu'ici, personne n'a répondu à l'annonce", "example_cs": "Zatím se na inzerát nikdo neozval"}),
}

REPLACE = []
SPLIT_LATER = {}
