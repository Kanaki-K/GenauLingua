#!/usr/bin/env python3
"""
Прогон всех пользовательских сценариев бота на реальных данных.

Проверяет то, что нельзя проверить ни статикой, ни юнит-тестами: каждый
обработчик вызывается в своём настоящем контексте, с FSM-состоянием,
которое к этому моменту накопилось. Одиночный вызов обработчика
не поймал бы, например, что «повтор ошибок» читает данные,
положенные завершением викторины.

Usage:
  python -m app.scripts.verify_all_flows
  python -m app.scripts.verify_all_flows --pair en ru --level B1

Код возврата 1, если хоть один шаг упал.
"""
from __future__ import annotations

import argparse
import asyncio
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import delete, select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel
from app.database.models import (
    MonthlyQuizEvent, MonthlyStats, QuizQuestion, QuizSession, TranslationReport,
    User, UserWord,
)
from app.database.session import AsyncSessionLocal

PROBE_ID = -9001


# ============================================================================
# ЗАГЛУШКИ AIOGRAM
# ============================================================================

class StubAudio:
    """Аудио в ответе Telegram: из него берётся file_id для кэша озвучки."""

    def __init__(self, index: int):
        self.file_id = f"stub-file-id-{index}"
        self.duration = 2
        self.file_size = 20000


class StubBot:
    def __init__(self):
        self.sent = []
        self.audio_sent = []

    async def send_message(self, chat_id=None, text=None, **kw):
        self.sent.append(text or kw.get("text", ""))
        return StubMessage(self)

    async def send_audio(self, chat_id=None, audio=None, caption=None, **kw):
        """
        Карточка с озвучкой: звук, подпись и кнопки одним сообщением.

        Подпись попадает в общий список отправленного — проверки текста
        карточки должны видеть её независимо от того, со звуком карточка
        или без.
        """
        self.audio_sent.append(caption or "")
        self.sent.append(caption or "")
        message = StubMessage(self, text=caption or "")
        message.audio = StubAudio(len(self.audio_sent))
        return message

    async def send_voice(self, chat_id=None, voice=None, caption=None, **kw):
        return await self.send_audio(chat_id=chat_id, audio=voice, caption=caption, **kw)

    async def edit_message_reply_markup(self, **kw):
        pass

    async def edit_message_text(self, **kw):
        pass

    async def edit_message_caption(self, **kw):
        pass

    async def edit_message_media(self, **kw):
        pass

    async def delete_message(self, **kw):
        pass


class StubUser:
    def __init__(self, uid):
        self.id = uid
        self.username = "probe"
        self.first_name = "Probe"
        self.last_name = None


class StubChat:
    def __init__(self, uid):
        self.id = uid


class StubMessage:
    def __init__(self, bot=None, text="", uid=PROBE_ID):
        self.bot = bot or StubBot()
        self.chat = StubChat(uid)
        self.from_user = StubUser(uid)
        self.message_id = 500
        self.text = text
        self.sent = []
        self.markups = []
        # Карточка со звуком: заполняется только там, где отправлено аудио
        self.audio = None

    async def answer(self, text=None, reply_markup=None, **kw):
        self.sent.append(text or "")
        self.markups.append(reply_markup)
        return StubMessage(self.bot, uid=self.from_user.id)

    async def answer_document(self, **kw):
        return StubMessage(self.bot, uid=self.from_user.id)

    async def edit_text(self, text=None, reply_markup=None, **kw):
        self.sent.append(text or "")
        self.markups.append(reply_markup)
        return self

    async def edit_reply_markup(self, reply_markup=None, **kw):
        self.markups.append(reply_markup)
        return self

    async def edit_media(self, media=None, reply_markup=None, **kw):
        """
        Правка медийной карточки: так вопрос превращается в разбор.

        Подпись из media уходит в тот же список, что и текст обычной
        правки, — проверки не должны зависеть от того, медийная карточка
        или нет.
        """
        caption = getattr(media, "caption", None)
        self.sent.append(caption or "")
        self.markups.append(reply_markup)
        self.bot.sent.append(caption or "")
        self.audio = StubAudio(0)
        return self

    async def edit_caption(self, caption=None, reply_markup=None, **kw):
        self.sent.append(caption or "")
        self.markups.append(reply_markup)
        return self

    async def delete(self):
        pass


class StubCallback:
    def __init__(self, data, uid=PROBE_ID, bot=None):
        self.bot = bot or StubBot()
        self.data = data
        self.from_user = StubUser(uid)
        self.message = StubMessage(self.bot, uid=uid)
        self.alerts = []

    async def answer(self, text=None, show_alert=False, **kw):
        if text:
            self.alerts.append(text)


class StubState:
    """FSMContext: держит состояние между шагами сценария."""

    def __init__(self):
        self.data: dict = {}
        self.state = None

    async def get_data(self):
        return dict(self.data)

    async def update_data(self, **kw):
        self.data.update(kw)
        return dict(self.data)

    async def set_state(self, state):
        self.state = state

    async def get_state(self):
        return self.state

    async def clear(self):
        self.data = {}
        self.state = None


# ============================================================================
# УЧЁТ РЕЗУЛЬТАТОВ
# ============================================================================

class Report:
    def __init__(self):
        self.rows: list[tuple[str, str, str]] = []

    async def step(self, name, coro_factory, *, expect_text=True):
        try:
            result = await coro_factory()
        except Exception as exc:
            self.rows.append((name, "ПАДАЕТ", f"{type(exc).__name__}: {exc}"))
            traceback.print_exc(limit=6)
            return None

        detail = ""
        if isinstance(result, (StubMessage, StubCallback)):
            msg = result if isinstance(result, StubMessage) else result.message
            # Часть обработчиков отвечает через bot.send_message, а не через
            # message.answer — учитываем оба канала, иначе рабочий шаг
            # выглядит как «ничего не отправил»
            body = "\n".join(msg.sent + msg.bot.sent)
            if expect_text and not body.strip():
                self.rows.append((name, "ПУСТОЙ ОТВЕТ", "обработчик ничего не отправил"))
                return result
            detail = f"{len(body)} символов"
            for marker in ("[MISSING:", "[ERROR:"):
                if marker in body:
                    self.rows.append((name, "СЛОМАН ТЕКСТ", f"в ответе есть {marker}"))
                    return result
        self.rows.append((name, "ок", detail))
        return result

    @property
    def failures(self):
        return [r for r in self.rows if r[1] != "ок"]

    def print(self):
        print(f"\n{'шаг':46} {'статус':14} детали")
        print("-" * 92)
        for name, status, detail in self.rows:
            mark = "  " if status == "ок" else "!!"
            print(f"{mark} {name:44} {status:14} {detail}")
        print()
        print(f"шагов: {len(self.rows)}, проблем: {len(self.failures)}")


# ============================================================================
# СЦЕНАРИИ
# ============================================================================

async def cleanup(s):
    ids = (await s.execute(select(QuizSession.id).where(QuizSession.user_id == PROBE_ID))).scalars().all()
    await s.execute(delete(MonthlyQuizEvent).where(MonthlyQuizEvent.user_id == PROBE_ID))
    await s.execute(delete(MonthlyStats).where(MonthlyStats.user_id == PROBE_ID))
    await s.execute(delete(TranslationReport).where(TranslationReport.user_id == PROBE_ID))
    await s.execute(delete(UserWord).where(UserWord.user_id == PROBE_ID))
    if ids:
        await s.execute(delete(QuizQuestion).where(QuizQuestion.session_id.in_(ids)))
    await s.execute(delete(QuizSession).where(QuizSession.user_id == PROBE_ID))
    await s.execute(delete(User).where(User.id == PROBE_ID))
    await s.commit()


async def flow_onboarding(rep, s, state):
    from app.bot.handlers import start

    await rep.step("/start (новый юзер)",
                   lambda: _msg_flow(start.cmd_start, s, state, text="/start"))
    await rep.step("выбор языка интерфейса",
                   lambda: _cb_flow(start.select_language, s, state, "select_lang_ru"))
    await rep.step("выбор уровня",
                   lambda: _cb_flow(start.select_level, s, state, "start_level_A1"))
    await rep.step("/start (уже есть юзер)",
                   lambda: _msg_flow(start.cmd_start, s, state, text="/start"))


async def flow_settings(rep, s, state, learning, native):
    from app.bot.handlers.quiz import settings as st

    await rep.step("Настройки: главный экран", lambda: _msg(st.show_settings, s, text="🦾 Настройки"))
    await rep.step("Настройки: какой язык учить", lambda: _cb(st.show_learning_lang, s, "settings_learning"))
    await rep.step(f"Настройки: выбрать {learning}", lambda: _cb(st.set_learning_lang, s, f"set_learning_{learning}"))
    await rep.step("Настройки: режим перевода", lambda: _cb(st.change_translation_mode, s, "settings_mode"))
    await rep.step("Настройки: обратное направление", lambda: _cb(st.set_translation_direction, s, "set_dir_reverse"))
    await rep.step("Настройки: прямое направление", lambda: _cb(st.set_translation_direction, s, "set_dir_forward"))
    await rep.step("Настройки: режим викторины", lambda: _cb(st.show_quiz_mode, s, "settings_quiz_mode"))
    await rep.step("Настройки: выбор уровня", lambda: _cb(st.show_level_selection, s, "qmode_level"))
    await rep.step("Настройки: уровень B1", lambda: _cb(st.set_quiz_mode_level, s, "qmode_set_level_B1"))
    await rep.step("Настройки: категории стр.1", lambda: _cb(st.show_category_page, s, "qmode_category_page_1"))
    await rep.step("Настройки: категории стр.2", lambda: _cb(st.show_category_page, s, "qmode_category_page_2"))
    await rep.step("Настройки: выбрать категорию", lambda: _cb(st.set_quiz_mode_category, s, "qmode_set_cat_ESSEN_TRINKEN"))
    await rep.step("Настройки: все слова", lambda: _cb(st.set_quiz_mode_all, s, "qmode_all"))
    await rep.step("Настройки: сложные слова", lambda: _cb(st.set_quiz_mode_difficult, s, "qmode_difficult"))
    await rep.step("Настройки: назад к уровню", lambda: _cb(st.set_quiz_mode_level, s, "qmode_set_level_A1"))
    await rep.step("Настройки: язык интерфейса", lambda: _cb(st.change_interface_language, s, "settings_language"))
    await rep.step("Настройки: интерфейс uk", lambda: _cb(st.set_interface_language, s, "iface_lang_uk"))
    await rep.step("Настройки: интерфейс ru", lambda: _cb(st.set_interface_language, s, "iface_lang_ru"))
    await rep.step("Настройки: назад", lambda: _cb(st.back_to_settings, s, "back_to_settings"))
    # валидация: язык значения не должен совпасть с изучаемым
    await rep.step(f"Настройки: учить {native} (коллизия пары)",
                   lambda: _cb(st.set_learning_lang, s, f"set_learning_{native}"))
    await rep.step(f"Настройки: вернуть {learning}",
                   lambda: _cb(st.set_learning_lang, s, f"set_learning_{learning}"))


async def flow_quiz(rep, s, state, questions=4):
    from app.bot.handlers.quiz import game

    bot = StubBot()

    async def start():
        msg = StubMessage(bot, text="📚 Учить слова")
        await game.start_quiz(msg, state, s)
        return msg

    result = await rep.step("Викторина: старт", start)
    if result is None or not state.data.get("correct_word_id"):
        rep.rows.append(("Викторина: не стартовала", "ПАДАЕТ", "нет correct_word_id в состоянии"))
        return

    # укоротим викторину, чтобы пройти её до конца
    state.data["total_questions"] = questions

    for i in range(questions):
        word_id = state.data["correct_word_id"]

        async def answer():
            cb = StubCallback(f"answer_{word_id}", bot=bot)
            await game.process_answer(cb, state, s)
            return cb

        await rep.step(f"Викторина: ответ {i + 1}", answer)

        async def nxt():
            cb = StubCallback("next_question", bot=bot)
            await game.show_next_question(cb, state, s)
            return cb

        await rep.step(f"Викторина: далее {i + 1}", nxt, expect_text=(i < questions - 1))

    # после завершения в состоянии должны лежать данные для репорта
    if not state.data.get("report_word_ids"):
        rep.rows.append(("Викторина: итоги", "ПАДАЕТ", "нет report_word_ids после завершения"))
    else:
        rep.rows.append(("Викторина: итоги", "ок",
                         f"{len(state.data['report_word_ids'])} слов для репорта"))


async def flow_quiz_wrong_answers(rep, s, state):
    """Отдельный прогон с неверными ответами — чтобы дошло до повтора ошибок."""
    from app.bot.handlers.quiz import game

    bot = StubBot()

    async def start():
        msg = StubMessage(bot, text="📚 Учить слова")
        await game.start_quiz(msg, state, s)
        return msg

    if await rep.step("Ошибки: старт викторины", start) is None:
        return
    state.data["total_questions"] = 2

    for i in range(2):
        # отвечаем заведомо неверно: id, которого нет среди вариантов
        async def answer():
            cb = StubCallback("answer_999999999", bot=bot)
            await game.process_answer(cb, state, s)
            return cb

        await rep.step(f"Ошибки: неверный ответ {i + 1}", answer)

        async def nxt():
            cb = StubCallback("next_question", bot=bot)
            await game.show_next_question(cb, state, s)
            return cb

        await rep.step(f"Ошибки: далее {i + 1}", nxt, expect_text=(i < 1))

    saved = state.data.get("saved_errors") or []
    if not saved:
        rep.rows.append(("Ошибки: список собран", "ПАДАЕТ", "saved_errors пуст"))
        return
    rep.rows.append(("Ошибки: список собран", "ок", f"{len(saved)} ошибок"))

    async def repeat():
        cb = StubCallback("repeat_errors", bot=bot)
        await game.repeat_errors(cb, state, s)
        return cb

    await rep.step("Ошибки: повтор", repeat, expect_text=False)


async def flow_report(rep, s, state):
    from app.bot.handlers.quiz import report

    if not state.data.get("report_word_ids"):
        rep.rows.append(("Репорт: пропущен", "ПАДАЕТ", "нет слов из викторины"))
        return

    word_id = state.data["report_word_ids"][0]

    await rep.step("Репорт: открыть список",
                   lambda: _cb_state(report.report_start, s, state, "report_translation_error"),
                   expect_text=False)
    await rep.step("Репорт: отметить слово",
                   lambda: _cb_state(report.report_toggle_word, s, state, f"report_toggle_{word_id}"),
                   expect_text=False)
    await rep.step("Репорт: страница",
                   lambda: _cb_state(report.report_change_page, s, state, "report_page_0"),
                   expect_text=False)
    await rep.step("Репорт: подтвердить",
                   lambda: _cb_state(report.report_confirm, s, state, "report_confirm"),
                   expect_text=False)
    await rep.step("Репорт: назад к списку",
                   lambda: _cb_state(report.report_back_to_select, s, state, "report_back_to_select"),
                   expect_text=False)
    # Жалоба на перевод и на произношение — разные пути и разные записи в базе
    await rep.step("Репорт: отправить как ошибку перевода",
                   lambda: _cb_state(report.report_send_text, s, state, "report_send_text"),
                   expect_text=False)

    # То же слово, но жалоба на озвучку: тройная уникальность должна это
    # разрешить, иначе новый вид репорта был бы недостижим
    second_word = state.data["report_word_ids"][1] if len(
        state.data.get("report_word_ids", [])) > 1 else word_id
    await rep.step("Репорт: отметить слово для озвучки",
                   lambda: _cb_state(report.report_toggle_word, s, state,
                                     f"report_toggle_{second_word}"),
                   expect_text=False)
    await rep.step("Репорт: отправить как ошибку произношения",
                   lambda: _cb_state(report.report_send_audio, s, state, "report_send_audio"),
                   expect_text=False)

    await rep.step("Репорт: два вида на одно слово различаются",
                   lambda: _check_report_kinds(s, word_id, second_word),
                   expect_text=False)

    await rep.step("Репорт: повторный клик по отправленному",
                   lambda: _cb(report.report_already_reported, s, f"report_already_{word_id}"),
                   expect_text=False)
    await rep.step("Репорт: отмена",
                   lambda: _cb_state(report.report_cancel, s, state, "report_cancel"),
                   expect_text=False)


async def _check_report_kinds(s, text_word_id: int, audio_word_id: int) -> str:
    """
    Проверить, что виды репорта действительно различаются в базе.

    Без этого проверка отправки ничего не значила бы: обработчик мог бы
    молча записывать всё как ошибку перевода.
    """
    from sqlalchemy import select

    from app.database.models import TranslationReport

    rows = (await s.execute(
        select(TranslationReport.word_id, TranslationReport.kind,
               TranslationReport.voice)
        .where(TranslationReport.user_id == PROBE_ID)
    )).all()

    kinds = {(word_id, kind) for word_id, kind, _ in rows}
    if (text_word_id, "text") not in kinds:
        raise AssertionError(f"нет жалобы на перевод слова {text_word_id}: {kinds}")
    if not any(kind == "audio" for _, kind in kinds):
        raise AssertionError(f"нет жалобы на произношение: {kinds}")

    # У жалобы на произношение должен быть записан голос, иначе её нечем
    # проверить
    audio_rows = [r for r in rows if r[1] == "audio"]
    if not all(r[2] for r in audio_rows):
        raise AssertionError(f"у жалобы на произношение не записан голос: {audio_rows}")

    return f"{len(rows)} записей, виды: {sorted({k for _, k in kinds})}"


async def flow_stats_help(rep, s):
    from app.bot.handlers.quiz import help as help_mod
    from app.bot.handlers.quiz import stats

    await rep.step("Статистика", lambda: _msg(stats.show_statistics, s, text="📊 Статистика"))
    await rep.step("Помощь", lambda: _msg(help_mod.show_help, s, text="❓ Помощь"))
    for name, handler, data in [
        ("Помощь: как пользоваться", help_mod.show_how_to_use, "help_how_to_use"),
        ("Помощь: планы", help_mod.show_roadmap, "help_roadmap"),
        ("Помощь: сообщество", help_mod.show_community, "help_community"),
        ("Помощь: о боте", help_mod.show_about, "help_about"),
        ("Помощь: назад", help_mod.back_to_help, "help_back"),
    ]:
        await rep.step(name, lambda h=handler, d=data: _cb(h, s, d))


async def flow_leaderboard(rep, s):
    from app.bot.handlers.leaderboard import alltime, leaderboard_table, monthly

    await rep.step("Рейтинг: мой", lambda: _cb(monthly.show_my_rating_callback, s, "show_my_rating"))
    await rep.step("Рейтинг: таблица (кнопка меню)",
                   lambda: _msg(monthly.show_leaderboard, s, text="🏆 Рейтинг"))
    await rep.step("Рейтинг: месячный", lambda: _cb(monthly.switch_to_monthly, s, "rating_monthly"))
    await rep.step("Рейтинг: за всё время", lambda: _cb(alltime.switch_to_alltime, s, "rating_alltime"))
    await rep.step("Таблица: месяц", lambda: _cb(leaderboard_table.show_table_monthly, s, "leaderboard_table_monthly"))
    await rep.step("Таблица: всё время", lambda: _cb(leaderboard_table.show_table_alltime, s, "leaderboard_table_alltime"))
    await rep.step("Таблица: переключить на месяц",
                   lambda: _cb(leaderboard_table.switch_table_to_monthly, s, "table_switch_monthly"))
    await rep.step("Таблица: переключить на всё время",
                   lambda: _cb(leaderboard_table.switch_table_to_alltime, s, "table_switch_alltime"))


async def flow_reminders(rep, s):
    from app.bot.handlers import reminders

    await rep.step("Напоминания: экран", lambda: _cb(reminders.show_notifications_settings, s, "settings:notifications"))
    await rep.step("Напоминания: включить", lambda: _cb(reminders.toggle_notifications, s, "notif_toggle"))
    await rep.step("Напоминания: часовой пояс", lambda: _cb(reminders.change_timezone_start, s, "notif_change_timezone"))
    await rep.step("Напоминания: больше городов", lambda: _cb(reminders.show_extended_cities, s, "tz:more_cities"))
    await rep.step("Напоминания: назад к поясам", lambda: _cb(reminders.back_to_main_timezones, s, "tz:back_to_main"))
    await rep.step("Напоминания: выбрать пояс", lambda: _cb(reminders.set_timezone, s, "tz:Europe/Berlin"))
    await rep.step("Напоминания: время", lambda: _cb(reminders.change_notification_time, s, "notif_change_time"))
    await rep.step("Напоминания: выбрать время", lambda: _cb(reminders.set_notification_time, s, "notif_time:09:00"))
    await rep.step("Напоминания: дни", lambda: _cb(reminders.change_notification_days, s, "notif_change_days"))
    await rep.step("Напоминания: переключить день", lambda: _cb(reminders.toggle_notification_day, s, "notif_day:2"))
    await rep.step("Напоминания: сохранить дни", lambda: _cb(reminders.save_notification_days, s, "notif_save"))
    await rep.step("Напоминания: выключить", lambda: _cb(reminders.toggle_notifications, s, "notif_toggle"))


async def flow_schedulers(rep, s):
    """Работы планировщика: они ходят в базу и на прод падали бы молча."""
    from app.services.monthly_leaderboard_service import (
        finalize_season, get_or_create_current_season,
    )

    async def season():
        got = await get_or_create_current_season(s)
        return None if got else None

    await rep.step("Планировщик: текущий сезон", season, expect_text=False)

    async def notifications():
        from app.schedulers.reminder_scheduler import check_and_send_notifications

        await check_and_send_notifications(StubBot())
        return None

    await rep.step("Планировщик: рассылка напоминаний", notifications, expect_text=False)


# ============================================================================
# ВСПОМОГАТЕЛЬНОЕ
# ============================================================================

async def _msg(handler, s, text=""):
    msg = StubMessage(text=text)
    await handler(msg, s)
    return msg


async def _msg_flow(handler, s, state, text=""):
    msg = StubMessage(text=text)
    await handler(msg, state, s)
    return msg


async def _cb(handler, s, data):
    cb = StubCallback(data)
    await handler(cb, s)
    return cb


async def _cb_flow(handler, s, state, data):
    cb = StubCallback(data)
    await handler(cb, state, s)
    return cb


async def _cb_state(handler, s, state, data):
    cb = StubCallback(data)
    await handler(cb, state, s)
    return cb


# ============================================================================
# MAIN
# ============================================================================

async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", nargs=2, metavar=("LEARNING", "NATIVE"), default=["en", "ru"])
    parser.add_argument("--level", default="A1")
    args = parser.parse_args()

    learning, native = args.pair
    rep = Report()

    async with AsyncSessionLocal() as s:
        await cleanup(s)

        state = StubState()
        print(f"Сценарии для пары {learning} → {native}, уровень {args.level}\n")

        await flow_onboarding(rep, s, state)

        user = await s.get(User, PROBE_ID)
        if user is None:
            print("Онбординг не создал пользователя — дальше идти нельзя.")
            rep.print()
            return 1

        user.learning_lang, user.native_lang = learning, native
        user.level = CEFRLevel(args.level)
        await s.commit()

        await flow_settings(rep, s, state, learning, native)

        # настройки могли поменять язык — вернём заданный
        user = await s.get(User, PROBE_ID)
        user.learning_lang, user.native_lang = learning, native
        user.level = CEFRLevel(args.level)
        await s.commit()

        await flow_quiz(rep, s, state)
        await flow_report(rep, s, state)

        state2 = StubState()
        await flow_quiz_wrong_answers(rep, s, state2)

        await flow_stats_help(rep, s)
        await flow_leaderboard(rep, s)
        await flow_reminders(rep, s)
        await flow_schedulers(rep, s)

        await cleanup(s)

    rep.print()
    return 1 if rep.failures else 0


sys.exit(asyncio.run(main()))
