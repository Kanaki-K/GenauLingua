# -*- coding: utf-8 -*-
"""Медленные нажатия пишутся видом действия, без текста и номеров (патч 2.1)."""
from app.bot.slow_log import describe
from app.locales import get_text
from app.testing import press, text_update, voice_update


def test_button_without_ids():
    assert describe(press(1, "answer_12345")) == "кнопка answer"
    assert describe(press(1, "learn_now:day2")) == "кнопка learn_now"
    assert describe(press(1, "bd:t:3:17:2")) == "кнопка bd"
    assert describe(press(1, "next_question")) == "кнопка next_question"


def test_messages_without_text():
    assert describe(text_update(1, "Моё личное сообщение")) == "сообщение"
    assert describe(voice_update(1)) == "голосовое"


def test_command_by_name_without_arguments():
    # 2.2.1: разбор 18.10 не отличал /start от /language
    assert describe(text_update(1, "/start")) == "команда /start"
    assert describe(text_update(1, "/start ref_секрет")) == "команда /start"
    assert describe(text_update(1, "/Language@GenauLingua_bot")) == "команда /language"


def test_menu_buttons_by_key_on_any_language():
    # Кнопки меню приходят текстом — прежде все писались «сообщение»
    for lang in ("ru", "uk", "en", "it", "cs"):
        assert describe(text_update(1, get_text("btn_learn_words", lang))) == "меню learn_words"
        assert describe(text_update(1, get_text("btn_rating", lang))) == "меню rating"
    assert describe(text_update(1, "📚 Учить слова")) == "меню learn_words"   # прежняя надпись
