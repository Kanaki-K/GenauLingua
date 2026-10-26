"""Полная вычитка, порция 32: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    11791: (T + "ru «в качестве провизии», uk «як провіант» — книжно", {"example_ru": "Для похода в горы я беру провизию: бутерброды, яблоки и шоколад", "example_uk": "Для походу в гори я беру провіант: бутерброди, яблука й шоколад"}),
    12186: (T + "fr «a fait mouche, un vrai coup dans le mille» — повтор", {"example_fr": "Le cadeau, c'était dans le mille : ma fille était ravie"}),
    12188: (T + "смысл разошёлся (de/tr/pl/cs «клуб вышел во вторую лигу») — везде «по воскресеньям играет в любительской лиге»", {"example_de": "Sonntags spielt er in einer Amateurliga", "example_ru": "По воскресеньям он играет в любительской лиге", "example_uk": "По неділях він грає в аматорській лізі", "example_en": "On Sundays he plays in an amateur league", "example_tr": "Pazarları amatör bir ligde oynuyor", "example_pl": "W niedziele gra w amatorskiej lidze", "example_it": "La domenica gioca in una lega amatoriale", "example_es": "Los domingos juega en una liga de aficionados", "example_fr": "Il joue dans une ligue amateur le dimanche", "example_cs": "V neděli hraje v amatérské lize"}),
    12234: (T + "ru/uk «джакузи было расслабляющим» — калька", {"example_ru": "В джакузи в отеле было так приятно расслабиться", "example_uk": "У джакузі в готелі було так приємно розслабитися"}),
    12268: (T + "uk «оголосив мені мат» — так не говорят", {"example_uk": "Після трьох ходів він поставив мені мат"}),
    12356: (T + "ru/uk «решилась на уход из офиса» — неуклюже", {"example_ru": "В пятьдесят тётя наконец ушла из офиса и теперь открывает маленькую гостиницу", "example_uk": "У п'ятдесят тітка нарешті пішла з офісу й тепер відкриває маленький готель"}),
    12410: (T + "fr «au-dessous de la ceinture» — устойчиво «en dessous»", {"example_fr": "Les blagues de mon frère sur mon ex sont parfois vraiment en dessous de la ceinture"}),
    12596: (T + "it «dolori… dolorosi» — тавтология", {"example_it": "L'indolenzimento dopo il primo allenamento era davvero doloroso"}),
    12656: (T + "ru/uk «небольшое вмешательство» — книжно", {"example_ru": "Это всего лишь небольшая операция, через час сможешь пойти домой", "example_uk": "Це лише невелика операція, за годину зможеш піти додому"}),
    12674: (T + "it «in un respiro», es «de un solo aliento» — так не говорят", {"example_it": "Ha bevuto tutto il bicchiere d'acqua d'un fiato", "example_es": "Se bebió el vaso de agua entero de un trago"}),
    12683: (T + "ru/uk «невосприимчив к ней всю жизнь» — книжно", {"example_ru": "Кто уже переболел ветрянкой, у того обычно иммунитет на всю жизнь", "example_uk": "Хто вже перехворів на вітрянку, у того зазвичай імунітет на все життя"}),
    12713: (T + "en «slept off his drunkenness» — так не говорят", {"example_en": "After the wedding my uncle slept it off until midday"}),
    12728: (T + "en «more comfortable» — не то", {"example_en": "I feel better now that I've said it"}),
    12740: (T + "ru/uk «гормоны сходят с ума» — калька", {"example_ru": "В переходном возрасте у сына гормоны бушуют вовсю", "example_uk": "У перехідному віці в сина гормони вирують на повну"}),
}

REPLACE = []
SPLIT_LATER = {}
