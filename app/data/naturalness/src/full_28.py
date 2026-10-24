"""Полная вычитка, порция 28: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    7476: (T + "смысл разошёлся (премия/заслуга/спасибо) — везде «ему за это полагается большое спасибо»", {"example_ru": "Ему за это полагается большое спасибо", "example_uk": "Йому за це належить велика подяка", "example_en": "He deserves a big thank-you for this", "example_tr": "Bunun için ona büyük bir teşekkür borçluyuz", "example_it": "Gli spetta un grande ringraziamento per questo", "example_es": "Se merece un gran agradecimiento por esto", "example_fr": "Il mérite un grand merci pour ça"}),
    7509: (T + "en/it/es/fr «его слова причинили боль» — «не хочу никому причинять боль»", {"example_en": "I don't want to cause anyone pain", "example_it": "Non voglio causare dolore a nessuno", "example_es": "No quiero causarle dolor a nadie", "example_fr": "Je ne veux causer de peine à personne"}),
    7692: (T + "ru «запер дверь» — «выключил плиту»", {"example_ru": "Я не стопроцентно уверен, что выключил плиту"}),
    8113: (T + "смысл разошёлся — везде «по телефону изменил голос, чтобы меня разыграть»", {"example_de": "Am Telefon hat er seine Stimme verstellt, um mich reinzulegen", "example_ru": "По телефону он изменил голос, чтобы меня разыграть", "example_uk": "По телефону він змінив голос, щоб мене розіграти", "example_en": "On the phone he disguised his voice to play a joke on me", "example_tr": "Telefonda bana şaka yapmak için sesini değiştirdi", "example_pl": "Przez telefon zmienił głos, żeby zrobić mi kawał", "example_it": "Al telefono ha camuffato la voce per farmi uno scherzo", "example_es": "Al teléfono disfrazó la voz para gastarme una broma", "example_fr": "Au téléphone, il a déguisé sa voix pour me faire une blague", "example_cs": "Do telefonu změnil hlas, aby si ze mě vystřelil"}),
    8116: (T + "en/it/es/fr «в их ссору» — «влип в это не по своей вине»", {"example_en": "I got mixed up in it through no fault of my own", "example_it": "Ci sono finito dentro senza nessuna colpa", "example_es": "Acabé metido en esto sin tener ninguna culpa", "example_fr": "Je me suis retrouvé mêlé à ça sans y être pour rien"}),
    8530: (T + "ru/uk «кто-то перерыл ящики» — «перерыл квартиру, а ключ был в кармане»", {"example_ru": "Я перерыл всю квартиру, а ключ от машины в итоге был в кармане куртки", "example_uk": "Я перерив усю квартиру, а ключ від машини зрештою був у кишені куртки"}),
}

REPLACE = []
SPLIT_LATER = {}
