# -*- coding: utf-8 -*-
"""
Живое демо карточки с озвучкой — так, как это должно работать в боте.

Одна карточка на вопрос:
  вопрос  — звук «слово», подпись из _question_text, 4 варианта ответа
  разбор  — на том же сообщении звук меняется на «слово … пример»,
            подпись на _answer_text, кнопка «следующее слово»

Тексты и клавиатуры берутся из настоящего кода бота, не переписываются.
Запускать при остановленном основном боте: один токен — один опрос.

    python -m app.scripts.tts_demo_card
"""
import asyncio
import logging
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

import edge_tts
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, FSInputFile, InputMediaAudio, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.quiz.game import (
    _answer_text,
    _question_text,
    get_next_question_keyboard,
)
from app.bot.keyboards import get_answer_keyboard
from app.config import settings
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import User
from app.database.session import AsyncSessionLocal
from app.services.language_service import LanguagePair, example_text, word_text
from app.services.quiz_service import generate_question

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logger = logging.getLogger("demo")

# Один регион на язык: немецкий — Германия, английский — Британия.
VOICES = {
    "de": "de-DE-KatjaNeural",
    "en": "en-GB-SoniaNeural",
    "ru": "ru-RU-SvetlanaNeural",
    "uk": "uk-UA-PolinaNeural",
    "tr": "tr-TR-EmelNeural",
}
PAUSE = " … "          # пауза между словом и примером
RATE = "-10%"          # чуть медленнее: на слух разборчивее, для A1 важно
CACHE = pathlib.Path("tts_samples/cache")
TOTAL = 5

# Сколько слов примера попадает в название. Примеры разной длины, а карточки
# должны выглядеть одинаково, поэтому пример всегда обрезается до трёх слов.
TITLE_EXAMPLE_WORDS = 3


def audio_title(word: str, example: str | None = None) -> str:
    """
    Название аудио — ровно то, что в нём звучит, и ничего лишнего.

    Для клипа со словом это само слово. Для клипа с примером — слово и
    начало примера: полный пример сделал бы названия разной длины и карточки
    выглядели бы неряшливо.
    """
    if not example:
        return word

    parts = example.split()
    head = " ".join(parts[:TITLE_EXAMPLE_WORDS]).rstrip(",.;:!?—–-")
    if len(parts) > TITLE_EXAMPLE_WORDS:
        head += "…"
    return f"{word} — {head}"


def audio_filename(title: str) -> str:
    """Имя файла из названия: Telegram показывает его, если плеер без тегов."""
    safe = "".join(c if (c.isalnum() or c in " -_—…") else "" for c in title).strip()
    return f"{safe or 'audio'}.mp3"

bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


async def synth(payload: str, lang: str, tag: str) -> pathlib.Path:
    """Озвучить и положить в кэш. Повторный запрос берётся с диска."""
    CACHE.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() else "_" for c in payload)[:60]
    path = CACHE / f"{lang}_{tag}_{safe}.mp3"
    if path.exists() and path.stat().st_size > 0:
        return path
    data = b""
    async for chunk in edge_tts.Communicate(payload, VOICES[lang], rate=RATE).stream():
        if chunk["type"] == "audio":
            data += chunk["data"]
    path.write_bytes(data)
    return path


async def demo_user(session, learning="de", native="ru") -> User:
    """Временный профиль, чтобы движок отдавал настоящие вопросы."""
    await session.merge(
        User(
            id=-777002, first_name="demo", interface_language=native,
            learning_lang=learning, native_lang=native, reverse_mode=False,
            level=CEFRLevel.A1, quiz_mode=QuizMode.LEVEL,
        )
    )
    await session.commit()
    return await session.get(User, -777002)


async def send_question(chat_id: int, state: FSMContext, number: int):
    """Карточка вопроса: звук слова + подпись + четыре варианта, одним сообщением."""
    data = await state.get_data()
    used = data.get("used", [])

    async with AsyncSessionLocal() as session:
        user = await demo_user(session)
        pair = LanguagePair(learning="de", native="ru")

        question = None
        for _ in range(10):
            question = await generate_question(session, user, exclude_ids=used, pair=pair)
            if question:
                break
        if not question:
            await bot.send_message(chat_id, "Слова закончились.")
            return

        word = question["correct_word"]
        used.append(word.id)

        caption = _question_text(word, pair, "ru", number, TOTAL)
        keyboard = get_answer_keyboard(question["options"])

        spoken_word = word_text(word, pair.learning)
        spoken_example = example_text(word, pair.learning)

    audio = await synth(spoken_word, "de", "w")
    title = audio_title(spoken_word)

    msg = await bot.send_audio(
        chat_id,
        FSInputFile(audio, filename=audio_filename(title)),
        caption=caption,
        reply_markup=keyboard,
        title=title,
    )

    await state.update_data(
        used=used, number=number, card_id=msg.message_id,
        correct_id=question["correct_word_id"] if "correct_word_id" in question else word.id,
        word_id=word.id, spoken_word=spoken_word, spoken_example=spoken_example,
    )


@dp.message(Command("audio"))
async def start_demo(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🎧 <b>Демо карточки с озвучкой</b>\n\n"
        f"{TOTAL} вопросов, немецкий → русский, уровень A1.\n\n"
        "В вопросе звучит <b>слово</b>. После ответа на той же карточке "
        "звук меняется на <b>слово с примером</b>.\n\n"
        "Отвечай как обычно."
    )
    await send_question(message.chat.id, state, 1)


@dp.callback_query(F.data.startswith("answer_"))
async def on_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    word_id = data.get("word_id")
    if word_id is None:
        await callback.answer("Демо не запущено — набери /audio", show_alert=True)
        return

    chosen = int(callback.data.split("_")[1])
    is_correct = chosen == word_id

    async with AsyncSessionLocal() as session:
        from app.database.models import Word
        word = await session.get(Word, word_id)
        pair = LanguagePair(learning="de", native="ru")
        caption = _answer_text(word, pair, "ru", is_correct)

    # Тот же звук, но теперь со примером — подменяем медиа на этой же карточке
    spoken_word = data["spoken_word"]
    spoken_example = data.get("spoken_example")

    payload = spoken_word
    if spoken_example:
        payload = f"{spoken_word}{PAUSE}{spoken_example}"
    audio = await synth(payload, "de", "we")
    title = audio_title(spoken_word, spoken_example)

    await callback.message.edit_media(
        InputMediaAudio(
            media=FSInputFile(audio, filename=audio_filename(title)),
            caption=caption,
            parse_mode=ParseMode.HTML,
            title=title,
        ),
        reply_markup=get_next_question_keyboard("ru"),
    )
    await callback.answer("Верно!" if is_correct else "Неверно")


@dp.callback_query(F.data == "next_question")
async def on_next(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    number = data.get("number", 1) + 1

    if number > TOTAL:
        await callback.message.delete()
        kb = InlineKeyboardBuilder()
        kb.button(text="🔁 Ещё раз", callback_data="demo_again")
        await bot.send_message(
            callback.message.chat.id,
            "✅ <b>Демо закончено.</b>\n\n"
            "Так выглядит карточка с озвучкой: одно сообщение, "
            "звук слова в вопросе, слово с примером на разборе.",
            reply_markup=kb.as_markup(),
        )
        await state.clear()
        return

    await callback.message.delete()
    await send_question(callback.message.chat.id, state, number)


@dp.callback_query(F.data == "demo_again")
async def on_again(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await send_question(callback.message.chat.id, state, 1)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(
        settings.ADMIN_USER,
        "🎧 Демо готово. Отправь <b>/audio</b> — покажу карточку с озвучкой.",
    )
    logger.info("демо слушает, напиши /audio боту")
    await dp.start_polling(bot)


asyncio.run(main())
