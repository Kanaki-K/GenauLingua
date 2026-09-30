# -*- coding: utf-8 -*-
"""
Заглавная I и İ в турецких переводах.

Правило нетривиальное и ломается тихо: если список дотless-основ разъедется с
турецкой орфографией, «Işık» (свет) превратится в «İşık» — другое слово, — и
заметить это можно будет только на слух в озвучке.

Слова в тестах взяты из настоящей базы: именно они попались на первом прогоне.
"""
import pytest

from app.scripts.fix_turkish_i import classify, fix

# Пишутся через дотless ı — заглавная I правильная, трогать нельзя.
# Все эти слова в базе есть.
DOTLESS = [
    "Işık",        # свет
    "Işığı",       # свет с притяжательным
    "Işın",        # луч
    "Islak",       # мокрый
    "Islık",       # свист
    "Isıtma",      # отопление
    "Isırmak",     # кусать
    "Isınma",      # разогрев
    "Izgara",      # решётка, гриль
    "Irkçı",       # расист
    "Irmak",       # река
    "Ilık",        # тёплый
    "Ihlamur",     # липа
    "Ispanak",     # шпинат
    "Istakoz",     # лобстер
    "Issız",       # безлюдный
    "Ismarlamak",  # заказывать
]

# Пишутся через İ — заглавная I здесь ошибка
DOTTED = [
    "Iyi",         # хороший
    "Iyimser",     # оптимист
    "Iyilik",      # добро
    "Iş",          # работа — против «Işık»
    "Işe",
    "Işlem",
    "Işaret",
    "Isim",        # имя — против «Isıtma»
    "Isyan",       # бунт
    "Istemek",     # хотеть
    "Iskele",      # пристань
    "Izin",        # разрешение
    "Izlemek",     # смотреть
    "Ilik",        # костный мозг — против «Ilık»
    "Itiraf",      # признание — против «Itır»
    "Insan",       # человек
    "Iç",          # внутренний
    "Ikinci",      # второй
    "Ihlal",       # нарушение
]

# Иностранные слова и аббревиатуры: турецкая орфография на них не
# распространяется
FOREIGN = ["IBAN", "IT", "DVD", "Intercity", "Inline"]


@pytest.mark.parametrize("word", DOTLESS)
def test_dotless_stays(word):
    """Слова с настоящей ı не трогаются."""
    assert classify(word[1:]) == "dotless"
    assert fix(word) == word


@pytest.mark.parametrize("word", DOTTED)
def test_dotted_gets_fixed(word):
    assert classify(word[1:]) == "dotted"
    assert fix(word) == "İ" + word[1:]


@pytest.mark.parametrize("word", FOREIGN)
def test_foreign_untouched(word):
    assert fix(word) == word


def test_vowel_harmony_separates_lookalikes():
    """
    Пары, которые различает только гармония гласных.

    Именно на них держится всё правило: «ısı-» и «isi-» отличаются второй
    буквой, а не смыслом, который скрипт знать не может.
    """
    assert fix("Isıtma") == "Isıtma"      # ısıtma — отопление
    assert fix("Isim") == "İsim"          # isim — имя
    assert fix("Ilık") == "Ilık"          # ılık — тёплый
    assert fix("Ilik") == "İlik"          # ilik — костный мозг
    assert fix("Işık") == "Işık"          # ışık — свет
    assert fix("Işitme") == "İşitme"      # işitme — слух


def test_only_word_start():
    """Заглавная I внутри слова не начало — её правило не касается."""
    assert fix("beIyi") == "beIyi"


def test_whole_phrase():
    """В фразе правится каждое слово по отдельности."""
    assert fix("Iyi Işık") == "İyi Işık"
    assert fix("Iki insan") == "İki insan"


def test_lowercase_untouched():
    """
    Строчные буквы не трогаются.

    Скрипт правит только заглавную I: у строчной «i» и «ı» уже различимы, и
    догадываться не о чем. Ошибки в строчных, если они есть, — другая задача.
    """
    assert fix("daha iyi") == "daha iyi"
    assert fix("en iyi") == "en iyi"
    assert fix("ışık") == "ışık"


def test_idempotent():
    """Повторный прогон ничего не меняет."""
    for word in DOTLESS + DOTTED + FOREIGN:
        once = fix(word)
        assert fix(once) == once
