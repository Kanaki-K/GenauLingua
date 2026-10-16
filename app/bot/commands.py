"""
Меню команд Telegram (кнопка «Меню» у поля ввода) — из кода, по языку телефона.

Прежде меню не ставилось нигде: что в нём лежит, решал BotFather руками, и
команды /language там быть не могло — её не было. А она нужна именно тому,
кто ошибся языком при знакомстве: такой человек не прочтёт ни настроек, ни
вступления, но кнопку «Меню» найдёт.

Подписи — на языке ТЕЛЕФОНА (`language_code` у `set_my_commands`): язык бота
у промахнувшегося как раз чужой. Без языка — английский: его поймёт больше
всего людей из тех, чей язык не наш.
"""
from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.types import BotCommand

from app.locales import get_text
from app.services.language_service import INTERFACE_LANGS

logger = logging.getLogger(__name__)

# Порядок — порядок строк в меню. /language второй: ради неё меню и ставится
COMMANDS = (
    ("start", "cmd_start"),
    ("language", "cmd_language"),
    ("settings", "cmd_settings"),
    ("help", "cmd_help"),
)

FALLBACK_LANG = "en"


def commands_for(lang: str) -> list[BotCommand]:
    return [BotCommand(command=name, description=get_text(key, lang)) for name, key in COMMANDS]


async def setup_commands(bot: Bot) -> None:
    """Поставить меню на каждый язык бота и запасное. Сбой не мешает запуску."""
    try:
        await bot.set_my_commands(commands_for(FALLBACK_LANG))
        for lang in INTERFACE_LANGS:
            await bot.set_my_commands(commands_for(lang), language_code=lang)
    except Exception:
        logger.warning("меню команд не поставлено", exc_info=True)
