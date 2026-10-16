"""
Названия языков в той форме, какой их требует фраза вступления.

«Вы учите НЕМЕЦКИЙ с переводом на РУССКИЙ» (решение владельца 16.10) —
по-русски обе формы совпадают с названием строчными, а по-украински,
по-чешски, по-немецки уже нет: «вивчаєте німецьку з перекладом
українською», «učíte se němčinu s překladem do ruštiny». Собрать такую
фразу из `langname_*` нельзя, а склонять кодом — гадать.

Поэтому формы выписаны таблицей: локаль → место во фразе → язык.
  * `learn` — что человек учит (дополнение к «учите»);
  * `into` — на какой язык перевод (то, что встаёт после предлога или
    падежного окончания в `intro_pair`).

Полнота таблицы проверяется тестом: локаль × все языки реестра. Новый язык
без строки здесь — красный тест, а не «[MISSING]» во вступлении.
"""

FORMS: dict[str, dict[str, dict[str, str]]] = {
    "ru": {
        "learn": {
            "de": "немецкий", "en": "английский", "ru": "русский", "uk": "украинский",
            "tr": "турецкий", "pl": "польский", "it": "итальянский", "es": "испанский",
            "fr": "французский", "cs": "чешский",
        },
        "into": {
            "de": "немецкий", "en": "английский", "ru": "русский", "uk": "украинский",
            "tr": "турецкий", "pl": "польский", "it": "итальянский", "es": "испанский",
            "fr": "французский", "cs": "чешский",
        },
    },
    "uk": {
        "learn": {
            "de": "німецьку", "en": "англійську", "ru": "російську", "uk": "українську",
            "tr": "турецьку", "pl": "польську", "it": "італійську", "es": "іспанську",
            "fr": "французьку", "cs": "чеську",
        },
        "into": {
            "de": "німецькою", "en": "англійською", "ru": "російською", "uk": "українською",
            "tr": "турецькою", "pl": "польською", "it": "італійською", "es": "іспанською",
            "fr": "французькою", "cs": "чеською",
        },
    },
    "en": {
        "learn": {
            "de": "German", "en": "English", "ru": "Russian", "uk": "Ukrainian",
            "tr": "Turkish", "pl": "Polish", "it": "Italian", "es": "Spanish",
            "fr": "French", "cs": "Czech",
        },
        "into": {
            "de": "German", "en": "English", "ru": "Russian", "uk": "Ukrainian",
            "tr": "Turkish", "pl": "Polish", "it": "Italian", "es": "Spanish",
            "fr": "French", "cs": "Czech",
        },
    },
    "de": {
        "learn": {
            "de": "Deutsch", "en": "Englisch", "ru": "Russisch", "uk": "Ukrainisch",
            "tr": "Türkisch", "pl": "Polnisch", "it": "Italienisch", "es": "Spanisch",
            "fr": "Französisch", "cs": "Tschechisch",
        },
        # «mit Übersetzung ins Russische»
        "into": {
            "de": "Deutsche", "en": "Englische", "ru": "Russische", "uk": "Ukrainische",
            "tr": "Türkische", "pl": "Polnische", "it": "Italienische", "es": "Spanische",
            "fr": "Französische", "cs": "Tschechische",
        },
    },
    "pl": {
        # «Nauka: niemiecki, tłumaczenie na rosyjski» — польская локаль
        # обходится без «Pan/Pani», поэтому фраза безличная
        "learn": {
            "de": "niemiecki", "en": "angielski", "ru": "rosyjski", "uk": "ukraiński",
            "tr": "turecki", "pl": "polski", "it": "włoski", "es": "hiszpański",
            "fr": "francuski", "cs": "czeski",
        },
        "into": {
            "de": "niemiecki", "en": "angielski", "ru": "rosyjski", "uk": "ukraiński",
            "tr": "turecki", "pl": "polski", "it": "włoski", "es": "hiszpański",
            "fr": "francuski", "cs": "czeski",
        },
    },
    "cs": {
        "learn": {
            "de": "němčinu", "en": "angličtinu", "ru": "ruštinu", "uk": "ukrajinštinu",
            "tr": "turečtinu", "pl": "polštinu", "it": "italštinu", "es": "španělštinu",
            "fr": "francouzštinu", "cs": "češtinu",
        },
        "into": {
            "de": "němčiny", "en": "angličtiny", "ru": "ruštiny", "uk": "ukrajinštiny",
            "tr": "turečtiny", "pl": "polštiny", "it": "italštiny", "es": "španělštiny",
            "fr": "francouzštiny", "cs": "češtiny",
        },
    },
    "es": {
        "learn": {
            "de": "alemán", "en": "inglés", "ru": "ruso", "uk": "ucraniano",
            "tr": "turco", "pl": "polaco", "it": "italiano", "es": "español",
            "fr": "francés", "cs": "checo",
        },
        "into": {
            "de": "alemán", "en": "inglés", "ru": "ruso", "uk": "ucraniano",
            "tr": "turco", "pl": "polaco", "it": "italiano", "es": "español",
            "fr": "francés", "cs": "checo",
        },
    },
    "fr": {
        # Артикль — часть формы: «l'allemand», но «le russe»
        "learn": {
            "de": "l’allemand", "en": "l’anglais", "ru": "le russe", "uk": "l’ukrainien",
            "tr": "le turc", "pl": "le polonais", "it": "l’italien", "es": "l’espagnol",
            "fr": "le français", "cs": "le tchèque",
        },
        "into": {
            "de": "allemand", "en": "anglais", "ru": "russe", "uk": "ukrainien",
            "tr": "turc", "pl": "polonais", "it": "italien", "es": "espagnol",
            "fr": "français", "cs": "tchèque",
        },
    },
    "it": {
        "learn": {
            "de": "tedesco", "en": "inglese", "ru": "russo", "uk": "ucraino",
            "tr": "turco", "pl": "polacco", "it": "italiano", "es": "spagnolo",
            "fr": "francese", "cs": "ceco",
        },
        "into": {
            "de": "tedesco", "en": "inglese", "ru": "russo", "uk": "ucraino",
            "tr": "turco", "pl": "polacco", "it": "italiano", "es": "spagnolo",
            "fr": "francese", "cs": "ceco",
        },
    },
    "tr": {
        "learn": {
            "de": "Almanca", "en": "İngilizce", "ru": "Rusça", "uk": "Ukraynaca",
            "tr": "Türkçe", "pl": "Lehçe", "it": "İtalyanca", "es": "İspanyolca",
            "fr": "Fransızca", "cs": "Çekçe",
        },
        "into": {
            "de": "Almanca", "en": "İngilizce", "ru": "Rusça", "uk": "Ukraynaca",
            "tr": "Türkçe", "pl": "Lehçe", "it": "İtalyanca", "es": "İspanyolca",
            "fr": "Fransızca", "cs": "Çekçe",
        },
    },
}


def language_form(locale: str, place: str, code: str) -> str:
    """Форма названия `code` для места `place` во фразе на языке `locale`."""
    from app.locales import DEFAULT_LOCALE

    table = FORMS.get(locale) or FORMS[DEFAULT_LOCALE]
    return table[place].get(code, code)
