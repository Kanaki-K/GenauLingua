"""
Показ карточки викторины.

Главное требование: без озвучки карточка должна быть в точности такой, какой
была до её внедрения. Озвучка — добавка, а не переделка; когда её нет, ни
текст, ни кнопки не должны отличаться ни на символ.
"""

import pytest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.handlers.quiz.card import (
    STATE_CARD_HAS_AUDIO,
    STATE_CARD_ID,
    show_card,
)
from app.services.audio_service import AudioClip

CHAT_ID = 12345
WORD_ID = 777
TEXT = "Вопрос 1 из 25\n\n🇩🇪 <b>die Fahrkarte</b>\n\n📝 Ich kaufe eine Fahrkarte\n\nВыбери перевод:"
KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Билет", callback_data="answer_777")],
    [InlineKeyboardButton(text="Ошибка", callback_data="answer_778")],
])


class FakeSession:
    """Сессия-заглушка: карточка не должна ничего писать в базу без звука."""

    def __init__(self):
        self.added = []
        self.commits = 0

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        pass

    async def commit(self):
        self.commits += 1

    async def rollback(self):
        pass


class FakeState:
    def __init__(self, data=None):
        self._data = dict(data or {})

    async def get_data(self):
        return dict(self._data)

    async def update_data(self, **kwargs):
        self._data.update(kwargs)
        return dict(self._data)


class SentMessage:
    def __init__(self, message_id=555, audio=None):
        self.message_id = message_id
        self.audio = audio


class FakeBot:
    def __init__(self):
        self.calls = []

    async def send_message(self, chat_id, text, reply_markup=None, **kwargs):
        self.calls.append(("send_message", {
            "chat_id": chat_id, "text": text,
            "reply_markup": reply_markup, **kwargs,
        }))
        return SentMessage()

    async def send_audio(self, chat_id, media, caption=None, reply_markup=None,
                         title=None, **kwargs):
        self.calls.append(("send_audio", {
            "chat_id": chat_id, "caption": caption,
            "reply_markup": reply_markup, "title": title, **kwargs,
        }))
        return SentMessage(audio=FakeAudio())


class FakeAudio:
    file_id = "AgACAgIAAxkDAAI-fake"
    duration = 3


class FakeMessage:
    """Прежняя карточка: запоминает, как её правили."""

    def __init__(self, message_id=555):
        self.message_id = message_id
        self.edits = []
        self.deleted = False

    async def edit_text(self, text, reply_markup=None, **kwargs):
        self.edits.append(("edit_text", {
            "text": text, "reply_markup": reply_markup, **kwargs,
        }))
        return SentMessage(self.message_id)

    async def edit_media(self, media, reply_markup=None, **kwargs):
        self.edits.append(("edit_media", {
            "media": media, "reply_markup": reply_markup, **kwargs,
        }))
        return SentMessage(self.message_id, audio=FakeAudio())

    async def delete(self):
        self.deleted = True


def make_clip(with_file_id=False):
    return AudioClip(
        kind="word", voice="de-DE-KatjaNeural", spoken_text="die Fahrkarte",
        title="die Fahrkarte", filename="die Fahrkarte.mp3",
        file_id="cached-file-id" if with_file_id else None,
        data=None if with_file_id else b"x" * 2000,
    )


class TestWithoutAudio:
    """
    Без озвучки — в точности прежняя карточка.

    До внедрения озвучки первый вопрос отправлялся как send_message(текст,
    клавиатура), а следующий правился как edit_text(текст, клавиатура).
    Ровно это и должно происходить, когда звука нет.
    """

    async def test_new_card_is_plain_send_message(self):
        bot, state, session = FakeBot(), FakeState(), FakeSession()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=None,
            word_id=WORD_ID, lang="de",
        )

        assert len(bot.calls) == 1
        method, kwargs = bot.calls[0]
        assert method == "send_message"
        assert kwargs["text"] == TEXT
        assert kwargs["reply_markup"] is KEYBOARD

    async def test_text_is_passed_through_untouched(self):
        bot, state, session = FakeBot(), FakeState(), FakeSession()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=None,
            word_id=WORD_ID, lang="de",
        )

        sent = bot.calls[0][1]["text"]
        # Ни приписки про озвучку, ни пометки — ни одного лишнего символа
        assert sent == TEXT
        assert "озвучк" not in sent.lower()
        assert "🔊" not in sent

    async def test_keyboard_gets_no_extra_buttons(self):
        bot, state, session = FakeBot(), FakeState(), FakeSession()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=None,
            word_id=WORD_ID, lang="de",
        )

        keyboard = bot.calls[0][1]["reply_markup"]
        assert keyboard.inline_keyboard == KEYBOARD.inline_keyboard
        flat = [b.text for row in keyboard.inline_keyboard for b in row]
        assert not any("🔊" in t for t in flat)

    async def test_existing_card_is_edited_with_plain_edit_text(self):
        bot, session = FakeBot(), FakeSession()
        state = FakeState({STATE_CARD_HAS_AUDIO: False, STATE_CARD_ID: 555})
        message = FakeMessage()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=None,
            word_id=WORD_ID, lang="de", message=message,
        )

        assert len(message.edits) == 1
        method, kwargs = message.edits[0]
        assert method == "edit_text"
        assert kwargs["text"] == TEXT
        assert kwargs["reply_markup"] is KEYBOARD
        # Ничего нового не отправлялось и прежнее не удалялось
        assert bot.calls == []
        assert message.deleted is False

    async def test_nothing_written_to_database(self):
        bot, state, session = FakeBot(), FakeState(), FakeSession()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=None,
            word_id=WORD_ID, lang="de",
        )

        assert session.added == []
        assert session.commits == 0


class TestWithAudio:
    async def test_new_card_sends_audio_with_caption_and_keyboard(self):
        bot, state, session = FakeBot(), FakeState(), FakeSession()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=make_clip(),
            word_id=WORD_ID, lang="de",
        )

        method, kwargs = bot.calls[0]
        assert method == "send_audio"
        # Всё одним сообщением: звук, подпись и кнопки
        assert kwargs["caption"] == TEXT
        assert kwargs["reply_markup"] is KEYBOARD
        assert kwargs["title"] == "die Fahrkarte"

    async def test_fresh_clip_file_id_is_remembered(self):
        bot, state, session = FakeBot(), FakeState(), FakeSession()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=make_clip(),
            word_id=WORD_ID, lang="de",
        )

        # Синтезированный клип попадает в кэш — больше он не синтезируется
        assert len(session.added) == 1
        assert session.added[0].file_id == FakeAudio.file_id
        assert session.commits == 1

    async def test_cached_clip_is_not_remembered_again(self):
        bot, state, session = FakeBot(), FakeState(), FakeSession()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=make_clip(with_file_id=True),
            word_id=WORD_ID, lang="de",
        )

        assert session.added == []

    async def test_media_card_is_edited_in_place(self):
        bot, session = FakeBot(), FakeSession()
        state = FakeState({STATE_CARD_HAS_AUDIO: True, STATE_CARD_ID: 555})
        message = FakeMessage()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=make_clip(with_file_id=True),
            word_id=WORD_ID, lang="de", message=message,
        )

        assert [m for m, _ in message.edits] == ["edit_media"]
        assert bot.calls == []
        assert message.deleted is False


class TestMediaTransitions:
    """
    Текстовое сообщение нельзя отредактировать в медийное и наоборот —
    в таких случаях карточка пересоздаётся.
    """

    async def test_text_to_audio_recreates_card(self):
        bot, session = FakeBot(), FakeSession()
        state = FakeState({STATE_CARD_HAS_AUDIO: False, STATE_CARD_ID: 555})
        message = FakeMessage()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=make_clip(with_file_id=True),
            word_id=WORD_ID, lang="de", message=message,
        )

        assert message.edits == []
        assert message.deleted is True
        assert [m for m, _ in bot.calls] == ["send_audio"]

    async def test_audio_to_text_recreates_card(self):
        bot, session = FakeBot(), FakeSession()
        state = FakeState({STATE_CARD_HAS_AUDIO: True, STATE_CARD_ID: 555})
        message = FakeMessage()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=None,
            word_id=WORD_ID, lang="de", message=message,
        )

        assert message.edits == []
        assert message.deleted is True
        method, kwargs = bot.calls[0]
        # И пересозданная карточка тоже в точности прежняя
        assert method == "send_message"
        assert kwargs["text"] == TEXT
        assert kwargs["reply_markup"] is KEYBOARD

    async def test_state_tracks_whether_card_has_audio(self):
        bot, state, session = FakeBot(), FakeState(), FakeSession()

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=make_clip(with_file_id=True),
            word_id=WORD_ID, lang="de",
        )
        assert (await state.get_data())[STATE_CARD_HAS_AUDIO] is True

        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=None,
            word_id=WORD_ID, lang="de",
        )
        assert (await state.get_data())[STATE_CARD_HAS_AUDIO] is False


class TestFailureDegradation:
    async def test_failed_edit_falls_back_to_new_card(self):
        """Правка может не удаться — карточка всё равно должна появиться."""
        bot, session = FakeBot(), FakeSession()
        state = FakeState({STATE_CARD_HAS_AUDIO: False, STATE_CARD_ID: 555})

        class Broken(FakeMessage):
            async def edit_text(self, *args, **kwargs):
                raise RuntimeError("message is not modified")

        message = Broken()
        await show_card(
            bot, CHAT_ID, state, session,
            text=TEXT, keyboard=KEYBOARD, clip=None,
            word_id=WORD_ID, lang="de", message=message,
        )

        assert message.deleted is True
        assert [m for m, _ in bot.calls] == ["send_message"]
        assert bot.calls[0][1]["text"] == TEXT
