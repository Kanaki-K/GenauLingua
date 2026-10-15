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

import re

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
        if getattr(message, "text", None):
            return "команда" if message.text.startswith("/") else "сообщение"
        return "сообщение (другое)"
    return "другое"
