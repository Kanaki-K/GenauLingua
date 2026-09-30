# -*- coding: utf-8 -*-
"""
Проверка карточки с озвучкой на живом Telegram — боевым кодом, не макетом.

Дёргает тот самый show_card из app/bot/handlers/quiz/card.py и тот самый
audio_service, что работают в викторине. Проверяется то, что юнит-тестами
не поймать: переходы между видами карточки в настоящем API.

Что именно проверяется:
  1. вопрос      — звук слова, подпись, четыре варианта одним сообщением
  2. разбор      — на том же сообщении звук меняется на «слово и пример»
  3. новый вопрос — снова слово, на том же сообщении
  4. кэш         — второй показ того же слова идёт по file_id, без синтеза
  5. деградация  — при отказе озвучки карточка пересоздаётся текстовой
  6. гетероним   — в вопрос уходит клип с примером, а не изолированное слово

    python -m app.scripts.tts_verify_card
"""
from __future__ import annotations

import asyncio
import logging
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import delete, select

from app.bot.handlers.quiz.card import (
    STATE_CARD_HAS_AUDIO,
    STATE_CARD_ID,
    show_card,
)
from app.bot.keyboards import get_answer_keyboard
from app.config import settings
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import User, Word, WordAudio
from app.database.session import AsyncSessionLocal
from app.services.audio_service import (
    KIND_FULL,
    KIND_WORD,
    clip_for_user,
    clip_kind_for_question,
)
from app.services.language_service import LanguagePair, word_text
from app.services.quiz_service import generate_question

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)

DEMO_USER_ID = -777003
LANG, NATIVE = "de", "ru"

bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()

passed: list[str] = []
failed: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    (passed if ok else failed).append(name)
    print(f"  {'OK  ' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))
    return ok


def new_state() -> FSMContext:
    return FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, chat_id=settings.ADMIN_USER, user_id=settings.ADMIN_USER),
    )


async def demo_user(session) -> User:
    await session.merge(
        User(
            id=DEMO_USER_ID, first_name="verify", interface_language=NATIVE,
            learning_lang=LANG, native_lang=NATIVE, reverse_mode=False,
            level=CEFRLevel.A1, quiz_mode=QuizMode.LEVEL, audio_enabled=True,
        )
    )
    await session.commit()
    return await session.get(User, DEMO_USER_ID)


async def pick_question(session, user, pair, exclude):
    for _ in range(30):
        q = await generate_question(session, user, exclude_ids=exclude, pair=pair)
        if q:
            return q
    return None


async def main() -> int:
    await bot.send_message(
        settings.ADMIN_USER,
        "🔬 <b>Проверка карточки боевым кодом</b>\n\n"
        "Ниже карточка пройдёт весь цикл: вопрос → разбор → новый вопрос, "
        "всё на одном сообщении. Кнопки не активны — это проверка, не игра.",
    )

    pair = LanguagePair(learning=LANG, native=NATIVE)
    state = new_state()
    await state.clear()

    async with AsyncSessionLocal() as session:
        user = await demo_user(session)

        print("\n=== 1. Вопрос: звук слова, подпись и кнопки одним сообщением ===")
        q1 = await pick_question(session, user, pair, [])
        if q1 is None:
            print("не удалось собрать вопрос — база пуста?")
            return 1
        w1 = q1["correct_word"]
        spoken1 = word_text(w1, LANG)

        clip1 = await clip_for_user(session, user, w1, LANG, KIND_WORD)
        check("клип слова синтезирован", clip1 is not None and clip1.data is not None,
              f"{len(clip1.data) if clip1 and clip1.data else 0} Б, {spoken1!r}")

        await show_card(
            bot, settings.ADMIN_USER, state, session,
            text=f"Вопрос 1 из 3\n\n🇩🇪 <b>{spoken1}</b>\n\nВыбери перевод:",
            keyboard=get_answer_keyboard(q1["options"]),
            clip=clip1, word_id=w1.id, lang=LANG,
        )
        data = await state.get_data()
        card_id = data.get(STATE_CARD_ID)
        check("карточка отправлена, id запомнен", bool(card_id), f"message_id={card_id}")
        check("состояние помнит, что карточка со звуком",
              data.get(STATE_CARD_HAS_AUDIO) is True)

        cached = await session.scalar(
            select(WordAudio).where(
                WordAudio.word_id == w1.id, WordAudio.lang == LANG,
                WordAudio.kind == KIND_WORD,
            )
        )
        check("file_id попал в кэш после отправки", cached is not None,
              f"{cached.file_id[:22]}…, {cached.duration_seconds} с" if cached else "")

        print("\n=== 2. Кэш: второй раз без синтеза ===")
        clip1b = await clip_for_user(session, user, w1, LANG, KIND_WORD)
        check("второй раз отдан file_id, а не байты",
              clip1b is not None and clip1b.file_id is not None and clip1b.data is None,
              "синтеза не было")

        print("\n=== 3. Разбор: на том же сообщении звук меняется на слово с примером ===")
        clip_full = await clip_for_user(session, user, w1, LANG, KIND_FULL)
        check("клип «слово и пример» синтезирован",
              clip_full is not None and clip_full.data is not None)
        if clip_full and clip1:
            check("это другой клип, длиннее",
                  len(clip_full.data or b"") > len(clip1.data or b""),
                  f"{len(clip1.data)} Б → {len(clip_full.data)} Б")
            check("в названии слово и начало примера", " — " in clip_full.title,
                  clip_full.title)

        # Тот же объект сообщения, что был бы у callback.message
        from aiogram.types import Chat, Message
        stub = Message.model_construct(
            message_id=card_id,
            chat=Chat(id=settings.ADMIN_USER, type="private"),
            date=None,
        ).as_(bot)

        await show_card(
            bot, settings.ADMIN_USER, state, session,
            text=f"✅ <b>Правильно!</b>\n\n🇩🇪 <b>{spoken1}</b>\n\n"
                 f"🇩🇪 {clip_full.spoken_text.split('…')[-1].strip() if clip_full else ''}",
            keyboard=get_answer_keyboard(q1["options"][:1]),
            clip=clip_full, word_id=w1.id, lang=LANG, message=stub,
        )
        data = await state.get_data()
        check("разбор остался тем же сообщением",
              data.get(STATE_CARD_ID) == card_id,
              f"было {card_id}, стало {data.get(STATE_CARD_ID)}")

        print("\n=== 4. Новый вопрос на том же сообщении ===")
        q2 = await pick_question(session, user, pair, [w1.id])
        w2 = q2["correct_word"]
        clip2 = await clip_for_user(session, user, w2, LANG, KIND_WORD)
        stub2 = Message.model_construct(
            message_id=data.get(STATE_CARD_ID),
            chat=Chat(id=settings.ADMIN_USER, type="private"), date=None,
        ).as_(bot)
        await show_card(
            bot, settings.ADMIN_USER, state, session,
            text=f"Вопрос 2 из 3\n\n🇩🇪 <b>{word_text(w2, LANG)}</b>\n\nВыбери перевод:",
            keyboard=get_answer_keyboard(q2["options"]),
            clip=clip2, word_id=w2.id, lang=LANG, message=stub2,
        )
        after = await state.get_data()
        check("новый вопрос на том же сообщении",
              after.get(STATE_CARD_ID) == card_id,
              f"message_id={after.get(STATE_CARD_ID)}")

        print("\n=== 5. Деградация: карточка без звука ===")
        stub3 = Message.model_construct(
            message_id=after.get(STATE_CARD_ID),
            chat=Chat(id=settings.ADMIN_USER, type="private"), date=None,
        ).as_(bot)
        await show_card(
            bot, settings.ADMIN_USER, state, session,
            text="Вопрос 3 из 3\n\n🇩🇪 <b>без озвучки</b>\n\n"
                 "<i>Так карточка выглядит, если синтез не удался или "
                 "озвучка выключена в настройках.</i>",
            keyboard=get_answer_keyboard(q2["options"]),
            clip=None, word_id=w2.id, lang=LANG, message=stub3,
        )
        degraded = await state.get_data()
        check("медийная карточка пересоздана текстовой",
              degraded.get(STATE_CARD_ID) != card_id,
              f"{card_id} → {degraded.get(STATE_CARD_ID)}")
        check("состояние помнит, что звука теперь нет",
              degraded.get(STATE_CARD_HAS_AUDIO) is False)

        print("\n=== 6. Гетероним: в вопрос идёт клип с примером ===")
        hetero = await session.scalar(
            select(Word).where(Word.word_de.in_(["modern", "umfahren", "übersetzen"]))
        )
        if hetero is None:
            print("  (в базе нет ни одного слова из списка гетеронимов — пропущено)")
        else:
            kind = clip_kind_for_question(hetero, LANG)
            check(f"для {hetero.word_de!r} выбран клип с контекстом",
                  kind == KIND_FULL, f"вид клипа: {kind}")

        ordinary = await session.scalar(select(Word).where(Word.word_de == "Haus"))
        if ordinary is not None:
            check("для обычного слова клип только со словом",
                  clip_kind_for_question(ordinary, LANG) == KIND_WORD)

        await session.execute(delete(User).where(User.id == DEMO_USER_ID))
        await session.commit()

    print(f"\n=== ИТОГ: прошло {len(passed)}, провалилось {len(failed)} ===")
    for name in failed:
        print(f"  ПРОВАЛ: {name}")

    await bot.send_message(
        settings.ADMIN_USER,
        f"{'✅' if not failed else '❌'} Проверка карточки: "
        f"прошло {len(passed)}, провалилось {len(failed)}."
        + ("\n\n" + "\n".join(f"• {n}" for n in failed) if failed else ""),
    )
    await bot.session.close()
    return 1 if failed else 0


sys.exit(asyncio.run(main()))
