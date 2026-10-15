"""
Обвес для сценарных проверок: НАСТОЯЩИЙ диспетчер, поддельный Telegram.

ЗАЧЕМ ЭТО НУЖНО СВЕРХ ОСТАЛЬНЫХ ПРОВЕРОК

Всё, что было до этого, проверяет части. Приёмка игр — что вопрос
СОБИРАЕТСЯ верно. Приёмка меню — что у каждой кнопки есть кому её поймать.
Тесты — что функции отвечают как задумано. Чего не проверял никто: что
нажатие доходит до нужного обработчика через настоящую цепочку роутеров и
что на экране после него оказывается то, что должно.

Разрыв этот не умозрительный, и проект на нём уже горел. Два разобранных
дефекта жили ровно там: «подсказка про голос гасила кнопки меню» (роутер
игры подключён раньше настроек, и обработчик глушил событие) и NameError в
развилке `show_next_question`, который не виден ни тестам на функции, ни
приёмке генератора, потому что живёт В ПОТОКЕ обработчика.

Поэтому здесь собирается диспетчер с тем же набором роутеров и в том же
порядке, что в `app.main`, и в него подаются обновления, как от Telegram.

ЧТО ПОДДЕЛЬНОЕ, А ЧТО НАСТОЯЩЕЕ

    настоящее   роутеры, фильтры, порядок подключения, обработчики,
                состояние FSM, база (тестовая), генератор вопросов
    поддельное  только сеть: вместо запросов к Telegram сессия ЗАПИСЫВАЕТ
                вызовы и отдаёт правдоподобные ответы

То есть подделан ровно один слой — самый внешний, и его подделка ничего не
скрывает: всё, что решает поведение бота, работает настоящее.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from aiogram import Bot, Dispatcher
from aiogram.client.session.base import BaseSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import TelegramMethod
from aiogram.types import (
    Audio, CallbackQuery, Chat, Message, Update, User as TgUser, Voice,
)

# Поддельный токен. Bot его разбирает на части, поэтому он должен быть
# правдоподобным по форме, но ни в какую сеть с ним никто не пойдёт.
FAKE_TOKEN = "42:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"


class RecordingSession(BaseSession):
    """
    Сессия, которая не ходит в сеть, а записывает, о чём её просили.

    Ответы выдаются по типу запроса, и этого достаточно: обработчики
    смотрят на результат только в двух местах — берут `message_id` у
    отправленного и `file_id` у отправленного аудио.
    """

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self._next_id = 1000
        # Проставляется в make_bot: ответные сообщения надо привязать к боту,
        # иначе обработчик не сможет вызвать на них ни .edit_text, ни .delete
        self.bot: Optional[Bot] = None

    # --- то, что требует BaseSession ---

    async def close(self) -> None:
        return None

    async def stream_content(self, *args: Any, **kwargs: Any):  # pragma: no cover
        raise NotImplementedError("сценариям не нужно скачивание файлов")

    async def make_request(
        self, bot: Bot, method: TelegramMethod, timeout: Optional[int] = None
    ) -> Any:
        name = type(method).__name__
        payload = method.model_dump(warnings=False)
        if name == "DeleteMessages":
            # Пачка записывается поштучно: проверкам важно, КАКИЕ сообщения
            # удалены, а не сколькими запросами
            for mid in payload["message_ids"]:
                self.calls.append(("DeleteMessage",
                                   {"chat_id": payload["chat_id"], "message_id": mid}))
            return True
        self.calls.append((name, payload))

        if name in ("SendMessage", "EditMessageText", "EditMessageCaption"):
            return self._message(payload)
        if name in ("SendAudio", "EditMessageMedia"):
            return self._message(payload, with_audio=True)
        # DeleteMessage, AnswerCallbackQuery, SendChatAction и прочее
        return True

    # --- вспомогательное ---

    def _message(self, payload: dict, *, with_audio: bool = False) -> Message:
        self._next_id += 1
        audio = None
        if with_audio:
            # `file_id` нужен настоящим кодом: клип, синтезированный только
            # что, запоминается по нему, чтобы больше не синтезировать.
            #
            # ЭТА СТРОКА НАРОЧНО НЕ ПОХОЖА НА НАСТОЯЩИЙ file_id, и делать её
            # похожей НЕЛЬЗЯ. Запоминание клипа складывает её в ОБЩИЙ кэш
            # озвучки — не в данные подопытного, — а значит приёмка, игравшая
            # круг поддельным ботом, травила звук всем, кто пользуется той же
            # базой. Так и случилось: 3 251 запись в рабочей копии, и живой
            # человек терял вопрос, потому что Telegram отвечал «wrong remote
            # file identifier: Wrong padding in the string».
            #
            # Теперь такую строку отсекает `audio_service.plausible_file_id`,
            # и короткое имя — её опознавательный знак.
            audio = Audio(
                file_id=f"fake-file-{self._next_id}",
                file_unique_id=f"u{self._next_id}",
                duration=2,
            )
        message = Message(
            message_id=self._next_id,
            date=datetime(2026, 10, 12, 12, 0, 0),
            chat=Chat(id=int(payload.get("chat_id") or 1), type="private"),
            text=payload.get("text") or payload.get("caption"),
            audio=audio,
        )
        # Без привязки к боту обработчик не сможет вызвать на этом сообщении
        # ни .edit_text, ни .delete — а карточка ведётся именно правками
        return message.as_(self.bot) if self.bot else message

    # --- разбор записанного ---

    def sent_texts(self) -> list[str]:
        """Все тексты, которые бот отправил или вписал правкой."""
        out = []
        for name, payload in self.calls:
            if name in ("SendMessage", "EditMessageText", "SendAudio",
                        "EditMessageCaption", "EditMessageMedia"):
                text = payload.get("text") or payload.get("caption")
                if text is None and name == "EditMessageMedia":
                    media = payload.get("media") or {}
                    text = media.get("caption")
                if text:
                    out.append(text)
        return out

    def last_text(self) -> str:
        texts = self.sent_texts()
        assert texts, "бот не отправил ни одного сообщения"
        return texts[-1]

    def alerts(self) -> list[str]:
        """
        Ответы на нажатие — то, что Telegram показывает всплывающим окном.

        Отдельно от `sent_texts`, потому что это не сообщение в переписке:
        им отвечают «нечего решать» или «отправь заново», и проверять такое
        надо именно здесь.
        """
        return [
            payload.get("text") or ""
            for name, payload in self.calls
            if name == "AnswerCallbackQuery"
        ]

    def sent_to(self) -> list[int]:
        """
        Кому бот ОТПРАВИЛ сообщение — по порядку, с повторами.

        Нужно рассылке: у неё главный вопрос не «что написано», а «кому
        ушло». Правки (`EditMessageText`) сюда не идут: они меняют уже
        показанное, а не доставляют новое.
        """
        return [
            int(payload["chat_id"])
            for name, payload in self.calls
            if name in ("SendMessage", "SendAudio", "SendDocument")
            and payload.get("chat_id") is not None
        ]

    def buttons(self) -> list[str]:
        """`callback_data` последней показанной клавиатуры."""
        for name, payload in reversed(self.calls):
            markup = payload.get("reply_markup")
            if not markup:
                continue
            rows = markup.get("inline_keyboard") if isinstance(markup, dict) else None
            if not rows:
                continue
            return [b.get("callback_data") for row in rows for b in row
                    if b.get("callback_data")]
        return []

    def all_buttons(self) -> list[str]:
        """
        `callback_data` ВСЕХ показанных клавиатур, а не только последней.

        Нужно потому, что за один шаг бот бывает присылает два сообщения:
        после круга — итог, а следом отдельное предложение напоминаний. Смотри
        только на последнее, и кнопки итога окажутся не найдены, хотя они
        есть. На этом мои же первые редакции сценариев и упали.
        """
        out = []
        for _, payload in self.calls:
            markup = payload.get("reply_markup")
            if not isinstance(markup, dict):
                continue
            for row in markup.get("inline_keyboard") or []:
                for button in row:
                    if button.get("callback_data"):
                        out.append(button["callback_data"])
        return out

    def button_texts(self) -> list[str]:
        for name, payload in reversed(self.calls):
            markup = payload.get("reply_markup")
            if not markup or not isinstance(markup, dict):
                continue
            rows = markup.get("inline_keyboard") or markup.get("keyboard")
            if not rows:
                continue
            return [b.get("text") for row in rows for b in row if b.get("text")]
        return []

    def clear(self) -> None:
        self.calls.clear()


def make_bot() -> tuple[Bot, RecordingSession]:
    session = RecordingSession()
    bot = Bot(token=FAKE_TOKEN, session=session)
    session.bot = bot
    return bot, session


# Какую сессию базы отдавать обработчикам. Держатель нужен потому, что
# роутеры — модульные одиночки и привязываются РОВНО К ОДНОМУ диспетчеру:
# собрать его заново на каждый тест нельзя, aiogram скажет «Router is
# already attached». Значит диспетчер один на весь прогон, а меняться между
# тестами должна сессия — через него.
_DB: dict[str, Any] = {"session": None}
_DISPATCHER: Optional[Dispatcher] = None


def use_session(db_session) -> None:
    """Подставить сессию базы, с которой пойдут следующие обновления."""
    _DB["session"] = db_session


def make_dispatcher(db_session=None) -> Dispatcher:
    """
    Диспетчер с тем же набором роутеров и в том же ПОРЯДКЕ, что боевой.

    Порядок здесь не формальность: он и решает, кто поймает нажатие первым,
    а один из разобранных дефектов был именно про это. Проверять набор,
    отличный от боевого, значит проверять не тот бот.

    Собирается ОДИН РАЗ и переиспользуется: см. `_DB` выше.
    """
    global _DISPATCHER

    if db_session is not None:
        use_session(db_session)
    if _DISPATCHER is not None:
        return _DISPATCHER

    # Набор и порядок берутся из `app.bot.routers` — того же места, откуда
    # их берёт боевой `app.main`. Своя копия списка здесь однажды уже
    # отстала, и сценарии проверяли бот без четвёртой игры, ничего об этом
    # не сообщая.
    from app.bot.routers import attach_routers

    # Приёмки можно гонять и на Redis (FSM_TEST_REDIS_URL) — так проверяется,
    # что всё состояние занятия переживает сериализацию в JSON
    import os

    from app.bot.fsm_storage import make_storage

    dp = attach_routers(Dispatcher(storage=make_storage(os.environ.get("FSM_TEST_REDIS_URL"))))

    @dp.update.middleware()
    async def inject_session(handler, event, data):
        session = _DB["session"]
        assert session is not None, "сессия базы не подставлена: use_session()"
        data["session"] = session
        return await handler(event, data)

    _DISPATCHER = dp
    return dp


async def reset_state(dp: Dispatcher) -> None:
    """
    Забыть состояние FSM между сценариями.

    Диспетчер один на весь прогон, значит и хранилище состояний одно. Не
    чисти его — и брошенный на середине круг предыдущего сценария утянул бы
    следующий: обработчик ответа сработал бы на чужих данных.
    """
    storage = dp.storage
    data = getattr(storage, "storage", None)
    if isinstance(data, dict):
        data.clear()
    states = getattr(storage, "states", None)
    if isinstance(states, dict):
        states.clear()
    redis = getattr(storage, "redis", None)
    if redis is not None:
        # Соединения пула привязаны к циклу событий, в котором открыты, а у
        # pytest-asyncio цикл свой на каждый тест: старое соединение падает
        # «Event loop is closed» (прогон 15.10 — 11 падений и 53 ошибки только
        # под FSM_TEST_REDIS_URL). Бросаем их, не закрывая: закрывать нечем —
        # их цикл уже мёртв.
        redis.connection_pool.reset()
        await redis.flushdb()


# ============================================================================
# ОБНОВЛЕНИЯ, КАК ОТ TELEGRAM
# ============================================================================

_counter = {"update": 1, "message": 1}


def _next(kind: str) -> int:
    _counter[kind] += 1
    return _counter[kind]


def text_update(user_id: int, text: str) -> Update:
    """Человек написал или нажал реплай-кнопку."""
    return Update(
        update_id=_next("update"),
        message=Message(
            message_id=_next("message"),
            date=datetime(2026, 10, 12, 12, 0, 0),
            chat=Chat(id=user_id, type="private"),
            from_user=TgUser(id=user_id, is_bot=False, first_name="Тестовый"),
            text=text,
        ),
    )


def voice_update(user_id: int, duration: int = 2) -> Update:
    """
    Человек записал голосовое — ответ на вопрос ВСЛУХ.

    Само содержимое записи поддельное, и этого достаточно: распознаватель
    для прогона подменяется (`check_pronunciation`), а проверяется здесь не
    то, как бот слышит, а то, как он УЧИТЫВАЕТ услышанное. Без этого
    речевой канал остаётся единственным, чья запись в круг не проверена
    ничем: нажатием его не пройти, а пропуск нарочно не засчитывается.
    """
    return Update(
        update_id=_next("update"),
        message=Message(
            message_id=_next("message"),
            date=datetime(2026, 10, 12, 12, 0, 0),
            chat=Chat(id=user_id, type="private"),
            from_user=TgUser(id=user_id, is_bot=False, first_name="Тестовый"),
            voice=Voice(
                file_id=f"fake-voice-{_counter['message']}",
                file_unique_id=f"vu{_counter['message']}",
                duration=duration,
            ),
        ),
    )


def press(user_id: int, data: str, message_id: int = 500) -> Update:
    """
    Человек нажал инлайн-кнопку.

    `from_user` у сообщения — БОТ, и это не придирка к точности: именно на
    этом ловится ошибка «искать человека по отправителю». С домашнего
    экрана занятие начинает сообщение бота, и `session.get(User,
    message.from_user.id)` вернул бы None.
    """
    return Update(
        update_id=_next("update"),
        callback_query=CallbackQuery(
            id=str(_next("update")),
            from_user=TgUser(id=user_id, is_bot=False, first_name="Тестовый"),
            chat_instance="test",
            data=data,
            message=Message(
                message_id=message_id,
                date=datetime(2026, 10, 12, 12, 0, 0),
                chat=Chat(id=user_id, type="private"),
                from_user=TgUser(id=1, is_bot=True, first_name="Бот"),
                text="прежний экран",
            ),
        ),
    )
