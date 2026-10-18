"""
Медленные нажатия — в журнал с видом действия (патч 2.1).

ЗАЧЕМ. 15.10 на проде 7 нажатий шли по 2–11 секунд у одного человека, и
понять, ЧТО это было, не удалось: aiogram пишет только общее время
обработки. Теперь нажатие дольше `SLOW_MS` пишется с видом действия:
«answer», «next_question», «learn_now», «voice»… — по нему видно, какая
часть бота тормозит.

ТЕКСТ ЛЮДЕЙ НЕ ПИШЕТСЯ: у сообщения — только вид (text / voice), у кнопки —
её действие без номеров слов и людей.
"""
from __future__ import annotations

import logging
import re
import time

SLOW_MS = 1500

# Номера (слов, сообщений, версий) и хвосты после них — не вид действия
_TAIL = re.compile(r"[:_]?\d.*$")


def describe(update) -> str:
    """Вид действия по обновлению Telegram — без личных данных."""
    callback = getattr(update, "callback_query", None)
    if callback is not None and callback.data:
        head = callback.data.split(":")[0]
        return "кнопка " + (_TAIL.sub("", head) or head)
    message = getattr(update, "message", None)
    if message is not None:
        if getattr(message, "voice", None) is not None:
            return "голосовое"
        text = getattr(message, "text", None)
        if text:
            # КОМАНДА — С ИМЕНЕМ, КНОПКА МЕНЮ — СВОИМ КЛЮЧОМ (2.2.1). Прежде
            # и то и другое писалось общим словом, и разбор 18.10 не мог
            # отличить «/start» от «/language», а «Учить» от «Рейтинга»:
            # кнопки меню приходят текстом. Аргументы команды не пишутся
            if text.startswith("/"):
                name = text.split()[0].split("@")[0].lower()[:24]
                return f"команда {name}"
            key = _menu_key(text)
            return f"меню {key}" if key else "сообщение"
        return "сообщение (другое)"
    if getattr(update, "my_chat_member", None) is not None:
        return "статус бота"
    return "другое"


def _menu_key(text: str):
    """Ключ кнопки главного меню по надписи на любом языке (и прежним), иначе None."""
    from app.bot.buttons import (
        BTN_HELP, BTN_LEARN_WORDS, BTN_RATING, BTN_SETTINGS, BTN_STATS, button_texts,
    )

    for key in (BTN_LEARN_WORDS, BTN_STATS, BTN_RATING, BTN_SETTINGS, BTN_HELP):
        if text in button_texts(key):
            return key.removeprefix("btn_")
    return None


logger = logging.getLogger("app.main")


async def slow_update_log(handler, event, data):
    started = time.perf_counter()
    try:
        return await handler(event, data)
    finally:
        spent = (time.perf_counter() - started) * 1000
        if spent >= SLOW_MS:
            logger.warning("медленно %d мс: %s", spent, describe(event))


def install_slow_log(dp) -> None:
    """
    Журнал — ПЕРВЫМ среди внешних middleware, снаружи замка очереди.

    Dispatcher при создании сам вешает FSMContextMiddleware, и с ним —
    замок `SimpleEventIsolation`: нажатия человека идут по очереди. Журнал,
    повешенный обычным `outer_middleware()`, вставал ПОСЛЕ него и не видел
    ожидания в очереди — а «нажатия по 2–11 с», ради которых журнал заведён,
    именно ожиданием и бывают, пока распознаётся голосовое (аудит 2.1).
    """
    dp.update.outer_middleware._middlewares.insert(0, slow_update_log)
