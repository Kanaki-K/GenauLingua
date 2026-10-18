# -*- coding: utf-8 -*-
"""Медленные нажатия пишутся видом действия, без текста и номеров (патч 2.1)."""
from app.bot.slow_log import describe
from app.testing import press, text_update, voice_update


def test_button_without_ids():
    assert describe(press(1, "answer_12345")) == "кнопка answer"
    assert describe(press(1, "learn_now:day2")) == "кнопка learn_now"
    assert describe(press(1, "bd:t:3:17:2")) == "кнопка bd"
    assert describe(press(1, "next_question")) == "кнопка next_question"


def test_messages_without_text():
    assert describe(text_update(1, "Моё личное сообщение")) == "сообщение"
    assert describe(text_update(1, "/start")) == "команда"
    assert describe(voice_update(1)) == "голосовое"
