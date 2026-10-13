"""
Общие утилиты для хендлеров бота
"""

import asyncio
import logging

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards import get_main_menu_keyboard
from app.database.models import User
# DEFAULT_LOCALE ниже читается в ensure_anchor, а импорта не было: строка
# `user.interface_language or DEFAULT_LOCALE` стоит ВНЕ try, поэтому у
# человека с пустым языком интерфейса якорь падал бы NameError, а не терялся
# тихо. Выживало это лишь потому, что язык ставится раньше уровня и `or`
# почти всегда замыкается на первом операнде.
from app.locales import DEFAULT_LOCALE

logger = logging.getLogger(__name__)


# Telegram ограничивает бота примерно 30 сообщениями в секунду. Удаляем
# порциями с паузой, иначе большой разрыв в id упирается в лимит и получаем 429.
DELETE_CHUNK_SIZE = 20
DELETE_CHUNK_PAUSE = 0.35
# Разрыв больше этого означает, что пользователь давно не заходил: вычищать
# сотни чужих сообщений бессмысленно и дорого
MAX_DELETE_RANGE = 100

# Название в якоре пишется ОДИНАКОВО на всех языках: это имя, а не слово.
BOT_NAME = "GenauLingua"

# Со скольких дней серия попадает в якорь. Один день — не серия.
ANCHOR_STREAK_MIN = 2


async def delete_messages_fast(bot, chat_id: int, start_id: int, end_id: int):
    """Массовое удаление сообщений между start_id и end_id"""
    if end_id <= start_id:
        return

    first_id = max(start_id, end_id - MAX_DELETE_RANGE)
    message_ids = list(range(first_id, end_id))

    deleted = 0
    for offset in range(0, len(message_ids), DELETE_CHUNK_SIZE):
        chunk = message_ids[offset:offset + DELETE_CHUNK_SIZE]
        results = await asyncio.gather(
            *(bot.delete_message(chat_id=chat_id, message_id=mid) for mid in chunk),
            return_exceptions=True,
        )
        deleted += sum(1 for r in results if not isinstance(r, Exception))

        if offset + DELETE_CHUNK_SIZE < len(message_ids):
            await asyncio.sleep(DELETE_CHUNK_PAUSE)

    logger.debug("Удалено %d/%d сообщений", deleted, len(message_ids))


def anchor_text(user: User) -> str:
    """
    Строка состояния для якоря: что учу, на каком уровне, сколько дней.

    ЧТО ТАКОЕ ЯКОРЬ. Сообщение, на котором живёт нижняя клавиатура, и у
    него три работы, все несущие: держит клавиатуру (она живёт НА
    сообщении, удалили — нажимать нечего), служит закладкой для зачистки
    переписки, и не даёт чату опустеть — у пустого чата Telegram показывает
    кнопку START, то есть бот «закрывается».

    ЧТО МЕНЯЕТСЯ. Механика не трогается, только ТЕКСТ. Прежде это был один
    значок раздела — `🤖`, `📚`, `📊`, `🦾`. Ограничение Telegram одно:
    текст непустой, и одиночный значок тут не обязателен.

    Якорь пересоздаётся при каждом переходе, значит он всегда свежий, и это
    ЕДИНСТВЕННЫЙ постоянный элемент во всём боте. Поэтому он и отвечает на
    вопрос, который иначе требует отдельного экрана: что я учу, на каком
    уровне, сколько дней подряд.

    Значок раздела теряется — честная потеря: раздел называет сам экран под
    якорем. Серия показывается с двух дней: один день — не серия, и писать
    про него значило бы повторять ту ложь, из-за которой домашний экран
    хвалил за восемь месяцев молчания.
    """
    from app.services.language_service import language_word, pair_from_user
    from app.services.streak_service import current_streak

    lang = user.interface_language or DEFAULT_LOCALE
    parts = [BOT_NAME]

    pair = pair_from_user(user)
    learning = language_word(pair.learning, lang)
    native = language_word(pair.native, lang)
    if learning and native:
        parts.append(f"{learning} → {native}")
    elif learning:
        parts.append(learning)

    if user.level:
        parts.append(user.level.value)

    streak = current_streak(user)
    if streak >= ANCHOR_STREAK_MIN:
        from app.locales import get_text

        parts.append(get_text("anchor_streak", lang, days=streak))

    return " · ".join(parts)


async def ensure_anchor(message: Message, session: AsyncSession, user: User,
                        emoji: str = "") -> tuple:
    """
    Создать новое якорное сообщение с главным меню.

    `emoji` остался в подписи ради вызывающих, которые его ещё передают:
    значение игнорируется, текст собирается из состояния человека. Удалять
    параметр заодно с правкой текста значило бы ронять семь мест разом.
    """
    old_anchor_id = user.anchor_message_id
    lang = user.interface_language or DEFAULT_LOCALE
    try:
        sent = await message.answer(
            anchor_text(user), reply_markup=get_main_menu_keyboard(lang)
        )
        new_anchor_id = sent.message_id
        user.anchor_message_id = new_anchor_id
        await session.commit()
        logger.debug(f"Создан новый якорь {new_anchor_id}")
        return old_anchor_id, new_anchor_id
    except Exception as e:
        logger.error(f"Ошибка создания якоря: {e}")
        return old_anchor_id, None