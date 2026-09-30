"""
Показ карточки викторины: текст, кнопки и озвучка одним сообщением.

Зачем отдельный модуль. Карточка ведётся одним сообщением от вопроса к
разбору и дальше к следующему вопросу — так было и до озвучки. Но со звуком
появляется переход, которого раньше не было: текстовое сообщение нельзя
отредактировать в медийное и наоборот. А синтез может не удаться на отдельном
слове, то есть карточка то со звуком, то без. Все четыре случая перехода
собраны здесь, чтобы три места показа в game.py выглядели одинаково и не
разъезжались.

Озвучка нигде не обязательна: нет звука — карточка выходит текстовой, как
раньше. Потерять звук допустимо, потерять викторину нет.
"""

from __future__ import annotations

import logging
from typing import Optional

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InlineKeyboardMarkup, InputMediaAudio, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.audio_service import AudioClip, remember

logger = logging.getLogger(__name__)

# Ключи состояния: по ним следующий показ понимает, что правит
STATE_CARD_ID = "card_message_id"
STATE_CARD_HAS_AUDIO = "card_has_audio"


async def _send_new(
    bot: Bot,
    chat_id: int,
    text: str,
    keyboard: InlineKeyboardMarkup,
    clip: Optional[AudioClip],
) -> Message:
    if clip is None:
        return await bot.send_message(chat_id, text, reply_markup=keyboard)

    media = (
        clip.file_id if clip.file_id
        else BufferedInputFile(clip.data, filename=clip.filename)
    )
    return await bot.send_audio(
        chat_id, media, caption=text, reply_markup=keyboard, title=clip.title,
    )


async def _edit_media(message: Message, text: str, keyboard: InlineKeyboardMarkup,
                      clip: AudioClip) -> Message:
    media = (
        clip.file_id if clip.file_id
        else BufferedInputFile(clip.data, filename=clip.filename)
    )
    return await message.edit_media(
        InputMediaAudio(
            media=media, caption=text, parse_mode=ParseMode.HTML, title=clip.title,
        ),
        reply_markup=keyboard,
    )


def _extract_file_id(message: Message) -> tuple[Optional[str], Optional[int]]:
    audio = getattr(message, "audio", None)
    if audio is None:
        return None, None
    return audio.file_id, getattr(audio, "duration", None)


async def show_card(
    bot: Bot,
    chat_id: int,
    state: FSMContext,
    session: AsyncSession,
    *,
    text: str,
    keyboard: InlineKeyboardMarkup,
    clip: Optional[AudioClip],
    word_id: int,
    lang: str,
    message: Optional[Message] = None,
) -> None:
    """
    Показать карточку: новую или на месте прежней.

    message — сообщение прежней карточки, если её нужно переиспользовать.
    Когда медийность меняется, правка невозможна: сообщение пересоздаётся.
    """
    data = await state.get_data()
    had_audio = bool(data.get(STATE_CARD_HAS_AUDIO))
    wants_audio = clip is not None

    sent: Optional[Message] = None

    if message is not None and had_audio == wants_audio:
        try:
            if wants_audio:
                sent = await _edit_media(message, text, keyboard, clip)
            else:
                sent = await message.edit_text(text, reply_markup=keyboard)
        except Exception:
            # Правка не удалась — карточка всё равно должна появиться
            logger.debug("правка карточки не удалась, пересоздаю", exc_info=True)
            sent = None

    if sent is None:
        if message is not None:
            try:
                await message.delete()
            except Exception:
                logger.debug("прежняя карточка не удалилась", exc_info=True)
        sent = await _send_new(bot, chat_id, text, keyboard, clip)

    await state.update_data(**{
        STATE_CARD_ID: sent.message_id,
        STATE_CARD_HAS_AUDIO: wants_audio,
    })

    # Клип, синтезированный только что, теперь лежит в Telegram — запоминаем
    # его file_id, чтобы больше никогда не синтезировать это слово
    if clip is not None and clip.needs_remembering:
        file_id, duration = _extract_file_id(sent)
        if file_id:
            await remember(session, word_id, lang, clip, file_id, duration)
            await session.commit()
