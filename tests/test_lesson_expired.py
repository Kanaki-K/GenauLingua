"""
Нажатие по кнопке занятия, которого бот уже не помнит.

Живой тест владельца 14.10: бот перезапустили посреди доски, и нажатия по
ней пропадали молча — «заглючило, не даёт пары дособирать». Состояние
занятия живёт в памяти и при перезапуске стирается, так что на проде это
случится после каждой выкатки.
"""
import pytest

from app.locales import get_text
from app.testing import make_bot, make_dispatcher, press, reset_state


@pytest.mark.parametrize("data", [
    "answer_123",               # ответ кнопкой
    "next_question",            # «Дальше»
    "speech_skip",              # «Пропустить» в «Говорю»
    "mt:l:0:0",                 # доска
    "bd:t:0:77:0",              # «Собираю»: слово
    "bd:check:77:0",            # «Собираю»: «Проверить»
])
async def test_a_forgotten_lesson_says_so_and_offers_a_new_one(session, user, data):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)       # как после перезапуска: состояния нет

    await dp.feed_update(bot, press(user.id, data, message_id=500))

    alerts = [p for n, p in recorder.calls
              if n == "AnswerCallbackQuery" and p.get("show_alert")]
    assert alerts and alerts[0]["text"] == get_text("lesson_expired", "ru"), (
        f"{data}: нажатие пропало молча — {recorder.calls}"
    )
    markups = [p for n, p in recorder.calls if n == "EditMessageReplyMarkup"]
    buttons = [b["callback_data"] for p in markups
               for row in p["reply_markup"]["inline_keyboard"] for b in row]
    assert buttons == ["learn_now:again"], f"{data}: вместо мёртвых кнопок {buttons}"
