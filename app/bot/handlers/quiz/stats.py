"""
Статистика и прогресс пользователя — по текущему режиму викторины
"""

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

import logging

logger = logging.getLogger(__name__)

from app.bot.buttons import BTN_STATS, pressed
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.database.models import User, QuizSession, Word, UserWord
from app.database.enums import QuizMode
from app.locales import get_text
from app.services.language_service import pair_flags, pair_from_user
from app.services.quiz_service import (
    STRUGGLING_THRESHOLD,
    get_overall_progress,
    get_user_progress_stats,
)

router = Router()


def get_stats_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=get_text("stats_btn_rating", lang),
                callback_data="show_my_rating"
            )]
        ]
    )


def create_progress_bar(current: int, total: int, length: int = 10) -> str:
    if total == 0:
        return "░" * length + " 0%"
    percentage = min(100, int((current / total) * 100))
    filled = int((current / total) * length)
    empty = length - filled
    return f"{'▓' * filled}{'░' * empty} {percentage}%"


def get_achievement_emoji(percentage: float) -> str:
    if percentage >= 95: return "🏆"
    elif percentage >= 85: return "🥇"
    elif percentage >= 75: return "🥈"
    elif percentage >= 60: return "🥉"
    return "📝"


# ============================================================================
# ПРОГРЕСС ПО ТЕКУЩЕМУ РЕЖИМУ
# ============================================================================

async def get_mode_progress(user: User, session: AsyncSession) -> dict:
    """
    Прогресс по текущему режиму викторины.

    Считается по изучаемому языку и только по словам, доступным на текущей
    языковой паре: прогресс по немецкому не влияет на английский, а слово без
    перевода на язык значения в базу доступного не входит.
    """
    pair = pair_from_user(user)

    if user.quiz_mode == QuizMode.CATEGORY and user.quiz_category:
        return await get_user_progress_stats(user.id, session, pair, category=user.quiz_category)

    if user.quiz_mode == QuizMode.ALL_WORDS:
        return await get_user_progress_stats(user.id, session, pair)

    if user.quiz_mode == QuizMode.DIFFICULT:
        return await _progress_difficult(user, session)

    return await get_user_progress_stats(user.id, session, pair, level=user.level)


async def _progress_difficult(user: User, session: AsyncSession) -> dict:
    """Прогресс по сложным словам — в рамках изучаемого языка"""
    learning_lang = pair_from_user(user).learning

    struggling_result = await session.execute(
        select(func.count())
        .select_from(UserWord)
        .where(
            UserWord.user_id == user.id,
            UserWord.learning_lang == learning_lang,
            UserWord.learned == False,
            UserWord.times_shown >= 2,
            (UserWord.times_correct * 100.0 / UserWord.times_shown) < STRUGGLING_THRESHOLD
        )
    )
    struggling_words = struggling_result.scalar() or 0

    # Сколько бывших сложных теперь выучены
    recovered_result = await session.execute(
        select(func.count())
        .select_from(UserWord)
        .where(
            UserWord.user_id == user.id,
            UserWord.learning_lang == learning_lang,
            UserWord.learned == True,
            UserWord.times_shown >= 3
        )
    )
    recovered = recovered_result.scalar() or 0

    return {
        'total_words': struggling_words + recovered,
        'seen_words': struggling_words + recovered,
        'learned_words': recovered,
        'struggling_words': struggling_words,
        'new_words': 0,
    }


# ============================================================================
# НАЗВАНИЕ РЕЖИМА ДЛЯ СТАТИСТИКИ
# ============================================================================

def _get_mode_title(user: User, lang: str) -> str:
    """Заголовок текущего режима для статистики"""
    from app.bot.handlers.quiz.settings import get_category_display

    if user.quiz_mode == QuizMode.LEVEL:
        return f"{user.level.value}"
    elif user.quiz_mode == QuizMode.CATEGORY:
        cat = user.quiz_category or "—"
        return get_category_display(cat, lang)
    elif user.quiz_mode == QuizMode.ALL_WORDS:
        return get_text("qmode_all_short", lang)
    elif user.quiz_mode == QuizMode.DIFFICULT:
        return get_text("qmode_difficult_short", lang)
    return "—"


# ============================================================================
# ОСНОВНОЙ ХЕНДЛЕР
# ============================================================================

@router.message(Command("stats"))
@router.message(pressed(BTN_STATS))
async def show_statistics(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    user = await session.get(User, user_id)

    try:
        await message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)

    if not user or not user.level:
        lang = user.interface_language if user else "ru"
        await message.answer(get_text("stats_no_level", lang))
        return

    lang = user.interface_language or "ru"
    pair = pair_from_user(user)

    # Прогресс по текущему режиму
    progress = await get_mode_progress(user, session)
    # Общий прогресс — по всей базе, доступной на текущей языковой паре
    overall = await get_overall_progress(user_id, session, pair)

    mode_title = _get_mode_title(user, lang)
    mode_arrow = pair_flags(pair)

    total = progress['total_words']
    learned = progress['learned_words']
    in_progress = progress['seen_words'] - learned
    new = progress['new_words']
    difficult = progress['struggling_words']
    overall_learned = overall['learned_words']
    overall_total = overall['total_words']

    # Викторины по текущему режиму и изучаемому языку
    quiz_query = select(QuizSession).where(
        QuizSession.user_id == user_id,
        QuizSession.completed_at.isnot(None),
        QuizSession.learning_lang == pair.learning,
    )

    if user.quiz_mode == QuizMode.LEVEL:
        quiz_query = quiz_query.where(QuizSession.level == user.level)
    elif user.quiz_mode == QuizMode.CATEGORY:
        quiz_query = quiz_query.where(QuizSession.quiz_category == user.quiz_category)
    elif user.quiz_mode == QuizMode.ALL_WORDS:
        quiz_query = quiz_query.where(QuizSession.quiz_mode == "all_words")

    quiz_query = quiz_query.order_by(QuizSession.started_at.desc())
    result = await session.execute(quiz_query)
    mode_sessions = result.scalars().all()

    # ========================================================================
    # ФОРМИРУЕМ ТЕКСТ
    # ========================================================================

    text = get_text("stats_header", lang) + "\n\n"

    # Режим + прогресс-бар
    bar = create_progress_bar(learned, total, length=12)
    text += f"🎯 <b>{mode_title}</b>\n"
    text += f"🔄 {mode_arrow}\n"
    text += f"{bar}\n"
    text += get_text("stats_learned_of", lang, learned=learned, total=total) + "\n\n"

    # Детализация
    text += get_text("stats_details", lang, progress=in_progress, new=new, difficult=difficult) + "\n\n"

    # Достижения
    if overall_learned >= 500: emoji = "🏆"
    elif overall_learned >= 200: emoji = "🥇"
    elif overall_learned >= 100: emoji = "🥈"
    elif overall_learned >= 50: emoji = "🥉"
    else: emoji = "⭐"

    text += f"{emoji} {get_text('stats_achievements_title', lang)}\n"
    text += get_text("stats_words_count", lang, count=overall_learned) + "\n"
    text += get_text("stats_streak_line", lang, days=user.streak_days) + "\n\n"

    # Викторины по режиму.
    # Точность считается по фактически отвеченным вопросам: плановое
    # total_questions превращало брошенные викторины в сплошные ошибки
    # и занижало точность примерно на 27 процентных пунктов.
    if mode_sessions:
        total_quizzes = len(mode_sessions)
        total_answered = sum(s.answered_questions for s in mode_sessions)
        total_correct = sum(s.correct_answers for s in mode_sessions)
        avg_percent = (total_correct / total_answered * 100) if total_answered > 0 else 0
        # max по пустой последовательности падает, а answered может быть нулём
        best_result = max((s.accuracy_percent for s in mode_sessions), default=0)

        q_emoji = get_achievement_emoji(avg_percent)
        text += f"{q_emoji} {get_text('stats_quizzes_header', lang, level=mode_title)}\n"
        text += get_text("stats_quizzes_passed_line", lang, count=total_quizzes) + "\n"
        text += get_text("stats_quizzes_avg_line", lang, percent=f"{avg_percent:.0f}") + "\n"
        text += get_text("stats_quizzes_best_line", lang, percent=f"{best_result:.0f}") + "\n\n"
    else:
        text += f"📝 {get_text('stats_quizzes_header', lang, level=mode_title)}\n"
        text += get_text("stats_quizzes_empty", lang) + "\n\n"

    # Последние викторины
    if mode_sessions:
        text += get_text("stats_recent_header", lang) + "\n"
        for s in mode_sessions[:3]:
            pct = s.accuracy_percent
            date_str = s.started_at.strftime("%d.%m")
            e = get_achievement_emoji(pct)
            text += f"{e} {date_str} — {s.correct_answers}/{s.answered_questions} ({pct:.0f}%)\n"
        text += "\n"

    # Общий прогресс
    if overall_total > 0:
        overall_bar = create_progress_bar(overall_learned, overall_total, length=12)
        text += get_text("stats_overall_header", lang) + "\n"
        text += f"{overall_bar}\n"
        text += get_text("stats_overall_learned", lang, learned=overall_learned, total=overall_total) + "\n\n"

    # Мотивация
    if learned == 0:
        text += get_text("stats_cta_start", lang)
    elif learned < total * 0.3:
        text += get_text("stats_cta_begin", lang)
    elif learned < total * 0.7:
        text += get_text("stats_cta_halfway", lang)
    else:
        text += get_text("stats_cta_almost", lang)

    text += "\n\n"
    text += get_text("stats_explanation", lang)

    # Якорь + отправка
    old_anchor_id, new_anchor_id = await ensure_anchor(message, session, user, emoji="📊")
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)

    await message.answer(text, reply_markup=get_stats_keyboard(lang))