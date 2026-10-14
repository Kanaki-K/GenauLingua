"""
Показ карточки викторины: текст, кнопки и озвучка одним сообщением.

Зачем отдельный модуль. Карточка ведётся одним сообщением от вопроса к
разбору и дальше к следующему вопросу — так было и до озвучки. Но со звуком
появляется переход, которого раньше не было: текстовое сообщение нельзя
отредактировать в медийное и наоборот. А синтез может не удаться на отдельном
слове, то есть карточка то со звуком, то без. Все четыре случая перехода
собраны здесь, чтобы места показа в lesson.py и speech.py выглядели одинаково и не
разъезжались.

Озвучка нигде не обязательна: нет звука — карточка выходит текстовой, как
раньше. Потерять звук допустимо, потерять викторину нет.
"""

from __future__ import annotations

import logging
from typing import Awaitable, Callable, Optional

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InlineKeyboardMarkup, InputMediaAudio, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.audio_service import (
    AudioClip, forget, reobtain, remember,
)

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
    lang: str,
) -> Message:
    if clip is None:
        return await bot.send_message(chat_id, text, reply_markup=keyboard)

    media = (
        clip.file_id if clip.file_id
        else BufferedInputFile(clip.data, filename=clip.filename)
    )
    # Исполнитель не передаётся нарочно: см. audio_service — подпись,
    # одинаковая у всех клипов, не несёт ничего
    return await bot.send_audio(
        chat_id, media, caption=text, reply_markup=keyboard, title=clip.title,
    )


async def _edit_media(message: Message, text: str, keyboard: InlineKeyboardMarkup,
                      clip: AudioClip, lang: str) -> Message:
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
    without_audio: Optional[
        Callable[[], Awaitable[Optional[tuple[str, InlineKeyboardMarkup]]]]
    ] = None,
) -> None:
    """
    Показать карточку: новую или на месте прежней.

    message — сообщение прежней карточки, если её нужно переиспользовать.
    Когда медийность меняется, правка невозможна: сообщение пересоздаётся.

    without_audio — как пересобрать карточку, если звук пропал уже при
    отправке. Нужен вопросу на слух: там звук и есть вопрос, и без него
    текст «Послушай и выбери» над четырьмя вариантами — вопрос без вопроса.
    """
    data = await state.get_data()
    had_audio = bool(data.get(STATE_CARD_HAS_AUDIO))
    wants_audio = clip is not None

    sent: Optional[Message] = None

    if message is not None and had_audio == wants_audio:
        try:
            if wants_audio:
                sent = await _edit_media(message, text, keyboard, clip, lang)
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
        try:
            sent = await _send_new(bot, chat_id, text, keyboard, clip, lang)
        except TelegramBadRequest:
            # МЁРТВАЯ ССЫЛКА НА КЛИП НЕ ИМЕЕТ ПРАВА ОБРЫВАТЬ КРУГ.
            #
            # Так и случилось у живого человека: Telegram ответил «wrong
            # remote file identifier: Wrong padding in the string», ошибка
            # ушла наружу, вопрос не появился, и занятие встало на третьем
            # вопросе. Правка медиа выше свой отказ ловила — а пересоздание
            # отправляло ТОТ ЖЕ негодный file_id и падало окончательно.
            #
            # Что делаем: запись кэша выбрасываем (её file_id мёртв), звук
            # берём заново — с диска, иначе синтезом, — и отправляем им.
            # Не вышло и это: карточка выходит ТЕКСТОВОЙ. Вопрос без звука
            # хуже вопроса со звуком, но несравнимо лучше оборванного круга.
            if clip is None or not clip.file_id:
                raise
            logger.warning(
                "Telegram отклонил file_id клипа (слово %s %s) — переделываю",
                word_id, lang, exc_info=True,
            )
            await forget(session, word_id, lang, clip.kind, clip.voice)
            fresh = await reobtain(clip, lang)
            if fresh is not None:
                try:
                    sent = await _send_new(bot, chat_id, text, keyboard, fresh, lang)
                    clip = fresh
                except TelegramBadRequest:
                    # И свежий клип отвергнут — дальше только без звука.
                    # Прежде эта ошибка уходила наружу, и человек оставался
                    # вовсе без экрана
                    logger.warning("свежий клип тоже отвергнут (слово %s %s)",
                                   word_id, lang, exc_info=True)
                    fresh = None
            if fresh is None:
                clip = None
                if without_audio is not None:
                    rebuilt = await without_audio()
                    if rebuilt is not None:
                        text, keyboard = rebuilt
                sent = await _send_new(bot, chat_id, text, keyboard, None, lang)
            wants_audio = clip is not None

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
