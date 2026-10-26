"""Полная вычитка, порция 31: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    10755: (T + "ru/uk/en/it/es/fr «доверяй интуиции» — везде «интуиция говорит, что что-то не так»", {"example_ru": "Интуиция подсказывает мне, что что-то не так", "example_uk": "Інтуїція підказує мені, що щось не так", "example_en": "My intuition tells me something's not right", "example_it": "La mia intuizione mi dice che qualcosa non va", "example_es": "Mi intuición me dice que algo no va bien", "example_fr": "Mon intuition me dit que quelque chose ne va pas"}),
    10772: (T + "it/fr «погода в выходные» — «кофе в офисе ужасный»", {"example_it": "Il caffè dell'ufficio ha un sapore orribile, ora me lo porto da casa", "example_fr": "Le café du bureau est épouvantable, maintenant j'apporte le mien"}),
    10816: (T + "en/it/es/fr «восприятие времени» — «восприятие цветов»", {"example_en": "Everyone's perception of colour is different", "example_it": "La percezione dei colori è diversa da persona a persona", "example_es": "La percepción de los colores es distinta en cada persona", "example_fr": "La perception des couleurs est différente chez chacun"}),
    11277: (T + "ru/uk «теряет очки» — «не может найти ключи»", {"example_ru": "У брата острый ум, но он вечно не может найти ключи", "example_uk": "У брата гострий розум, але він вічно не може знайти ключі"}),
    11569: (T + "ru «соседка поливает цветы» — «трижды проверяю плиту»", {"example_ru": "Для душевного покоя я перед отпуском трижды проверяю, выключена ли плита"}),
    11716: (T + "de/tr/pl/cs «мы едим» — везде «американцы едят»", {"example_de": "An Thanksgiving essen die Amerikaner Truthahn", "example_ru": "Американцы на День благодарения едят индейку", "example_uk": "Американці на День подяки їдять індика", "example_en": "Americans eat turkey for Thanksgiving", "example_tr": "Amerikalılar Şükran Günü'nde hindi yer", "example_pl": "Amerykanie jedzą indyka na Święto Dziękczynienia", "example_it": "Per il Ringraziamento gli americani mangiano il tacchino", "example_es": "En Acción de Gracias los estadounidenses comen pavo", "example_fr": "Pour Thanksgiving, les Américains mangent de la dinde", "example_cs": "Američané jedí na Den díkůvzdání krocana"}),
    11728: (T + "de/tr/pl/cs учебниковое «дорогой морепродукт» — везде «на годовщину побаловали себя омаром»", {"example_de": "Zum Hochzeitstag haben wir uns einen Hummer gegönnt", "example_ru": "На годовщину мы побаловали себя омаром", "example_uk": "На річницю ми побалували себе омаром", "example_en": "For our anniversary we treated ourselves to lobster", "example_tr": "Yıl dönümümüzde kendimize bir ıstakoz ısmarladık", "example_pl": "Na rocznicę zafundowaliśmy sobie homara", "example_it": "Per l'anniversario ci siamo regalati un astice", "example_es": "Por nuestro aniversario nos dimos el capricho de un bogavante", "example_fr": "Pour notre anniversaire de mariage, on s'est offert un homard", "example_cs": "K výročí jsme si dopřáli humra"}),
}

REPLACE = []
SPLIT_LATER = {}
