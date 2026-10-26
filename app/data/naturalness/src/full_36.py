"""Полная вычитка, порция 36: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    16320: (T + "ru/uk/en/it/es/fr «волки защищают территорию» — везде «кот защищает сад как свою территорию»", {"example_ru": "Наш кот защищает весь сад как свою территорию", "example_uk": "Наш кіт захищає весь сад як свою територію", "example_en": "Our tomcat defends the whole garden as his territory", "example_it": "Il nostro gatto difende tutto il giardino come suo territorio", "example_es": "Nuestro gato defiende todo el jardín como su territorio", "example_fr": "Notre chat défend tout le jardin comme son territoire"}),
    16952: (T + "ru/uk «машина незаперта» — «ключ в машине»", {"example_ru": "Оставить ключ в машине — грубая небрежность, говорит страховая, и ничего не платит", "example_uk": "Залишити ключ у машині — груба недбалість, каже страхова, і нічого не платить"}),
    17153: (T + "de/tr/pl/cs «обратный путь был дольше» — везде «на обратном пути остановились поесть»", {"example_de": "Auf dem Rückweg haben wir zum Essen angehalten", "example_ru": "На обратном пути мы остановились пообедать", "example_uk": "На зворотному шляху ми зупинилися пообідати", "example_en": "On the way back we stopped for lunch", "example_tr": "Dönüş yolunda yemek için mola verdik", "example_pl": "W drodze powrotnej zatrzymaliśmy się na obiad", "example_it": "Sulla strada del ritorno ci siamo fermati a mangiare", "example_es": "En el camino de vuelta paramos a comer", "example_fr": "Sur le chemin du retour, on s'est arrêtés manger", "example_cs": "Na cestě zpět jsme se zastavili na oběd"}),
}

REPLACE = []
SPLIT_LATER = {}
