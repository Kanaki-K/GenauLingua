"""
Н3 (16.10): артикли новых языков при проверке речи.

Прежде снимались только der/die/das/the/a/an: «il libro», сказанное как
«libro», могло не засчитаться, а «l'uomo» после снятия знаков становилось
«l uomo» и не совпадало ни с чем.
"""
import pytest

from app.services import speech_check as sc


@pytest.mark.parametrize("lang,target,bare", [
    ("it", "il libro", "libro"),
    ("it", "l'uomo", "uomo"),
    ("it", "gli amici", "amici"),
    ("es", "la casa", "casa"),
    ("es", "los libros", "libros"),
    ("fr", "le livre", "livre"),
    ("fr", "l'homme", "homme"),
    ("de", "der Krieg", "krieg"),
    ("en", "the house", "house"),
])
def test_leading_article_is_dropped(lang, target, bare):
    assert sc._strip_article(sc._normalize(target, lang), lang) == bare


def test_glued_elided_article_is_recognised():
    """Распознаватель пишет «luomo» слитно — как «Derstreit» у немецкого."""
    want = sc._strip_article(sc._normalize("l'uomo", "it"), "it")
    assert sc._similarity(want, sc._normalize("luomo", "it"), "it") == 1.0


def test_czech_has_no_articles_to_drop():
    assert sc._strip_article(sc._normalize("dobrý den", "cs"), "cs") == "dobry den"
