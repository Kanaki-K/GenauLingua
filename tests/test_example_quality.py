"""
Показывает ли пример само слово.

Проверка по подстроке даёт 30% срабатываний на базе, и большинство из них —
словоизменение: «рыба» стоит в примере как «рыбу». Настоящий дефект — это
пример про другое слово: «подсобить» → «иногда нужно помочь удаче». Тесты
держат границу между тем и другим.
"""

import pytest

from app.scripts.example_quality import fold, word_in_example


def found(word: str, example: str, lang: str) -> bool:
    return word_in_example(word, example, lang)[0]


class TestInflectionIsNotADefect:
    """Слово в другой форме — пример годен."""

    @pytest.mark.parametrize("word,example", [
        ("Рыба", "Я люблю рыбу"),
        ("Лыжи", "Он катается на лыжах"),
        ("Таблица", "Заполните таблицу"),
        ("Сортировать", "Я сортирую бумаги"),
        ("Книга", "Я читаю интересную книгу"),
        ("Работать", "Она работает в офисе"),
    ])
    def test_russian(self, word, example):
        assert found(word, example, "ru")

    @pytest.mark.parametrize("word,example", [
        ("книга", "Я читаю книгу"),
        ("робити", "Що ти робиш"),
    ])
    def test_ukrainian(self, word, example):
        assert found(word, example, "uk")

    @pytest.mark.parametrize("word,example", [
        ("książka", "Czytam ciekawą książkę"),
        ("robić", "Co ty robisz"),
        ("dom", "Idę do domu"),
    ])
    def test_polish(self, word, example):
        assert found(word, example, "pl")

    @pytest.mark.parametrize("word,example", [
        ("Haus", "Das Haus ist groß"),
        ("Haus", "Die Häuser sind alt"),       # умлаут в множественном числе
        ("Fuß", "Meine Füße tun weh"),         # ß и умлаут вместе
        ("gehen", "Wir wollen weggehen"),      # корень внутри составного
    ])
    def test_german(self, word, example):
        assert found(word, example, "de")

    @pytest.mark.parametrize("word,example", [
        ("to read", "She reads every day"),
        ("to run", "He is running fast"),
    ])
    def test_english_particle(self, word, example):
        assert found(word, example, "en")


class TestGermanSeparableVerbs:
    """
    Отделяемая приставка уходит в конец предложения. Без учёта этого целый
    класс немецких глаголов попадал бы в дефекты.
    """

    @pytest.mark.parametrize("word,example", [
        ("aufstehen", "Ich stehe früh auf"),
        ("anrufen", "Ich rufe dich morgen an"),
        ("einkaufen", "Wir kaufen im Supermarkt ein"),
        ("mitkommen", "Kommst du mit"),
        ("zurückgeben", "Ich gebe das Buch zurück"),
    ])
    def test_detached_prefix(self, word, example):
        assert found(word, example, "de")

    def test_unseparated_form_also_works(self):
        assert found("aufstehen", "Ich muss früh aufstehen", "de")


class TestCompoundHeadwords:
    """
    У заголовочного слова из нескольких частей достаточно, чтобы нашлась
    любая содержательная часть.
    """

    def test_any_part_counts(self):
        assert found("Консервная банка", "Банка пустая", "ru")

    def test_longest_part_counts(self):
        assert found("Офисное помещение", "Помещение светлое", "ru")


class TestRealDefects:
    """Пример про другое слово — это дефект, и он должен находиться."""

    @pytest.mark.parametrize("word,example,lang", [
        ("Подсобить", "Иногда нужно помочь удаче", "ru"),
        ("Величественный", "Величие этих гор меня впечатлило", "ru"),
        ("Двойник", "Это копия оригинала", "ru"),
        ("Buch", "Ich lese eine Zeitung", "de"),
        ("Fahrkarte", "Der Zug ist pünktlich", "de"),
    ])
    def test_flagged(self, word, example, lang):
        assert not found(word, example, lang)

    def test_different_word_with_shared_start_is_a_defect(self):
        """
        «Fräulein» и «Frau» — разные слова с общими четырьмя буквами.

        На доле основы в половину слова это совпадало, и пример проходил как
        годный. Поймано проверкой озвучки распознаванием: клип
        «das Fräulein … Entschuldigung, Frau» был опознан как не содержащий
        слова — и оказался прав. Отсюда доля основы стала своей на язык: в
        немецком и английском слово почти не меняется, и половины мало.
        """
        assert not found("Fräulein", "Entschuldigung, Frau", "de")
        # При этом само «Frau» в том же примере находиться должно
        assert found("Frau", "Entschuldigung, Frau", "de")

    def test_empty_example_is_a_defect(self):
        assert not found("Рыба", "", "ru")

    def test_empty_word_is_a_defect(self):
        assert not found("", "Я люблю рыбу", "ru")


class TestFold:
    """Сравнение основ без диакритики — иначе Haus и Häuser разойдутся."""

    def test_umlauts_removed(self):
        assert fold("Häuser") == "hauser"
        assert fold("Müller") == "muller"

    def test_eszett_expands(self):
        assert fold("Fuß") == "fuss"

    def test_polish_diacritics_removed(self):
        assert fold("książkę") == "ksiazke"
        assert fold("żółty") == "zolty"

    def test_case_removed(self):
        assert fold("РЫБА") == fold("рыба")


class TestKnownLimits:
    """
    Чередование в основе этим способом не берётся — нужен морфологический
    разбор. Такие слова попадают в список дефектов ложно; это признанный
    предел отсева, а не скрытая ошибка, и разбирать их приходится дальше.
    """

    def test_stem_alternation_is_missed(self):
        # «нуждаться» и «нужна» расходятся на четвёртой букве
        assert not found("Нуждаться", "Мне срочно нужна помощь", "ru")
