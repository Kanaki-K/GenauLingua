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
from app.services.streak_service import current_streak
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import pair_label, pair_from_user
from app.services.quiz_service import (
    STRUGGLING_THRESHOLD,
    get_overall_progress,
    get_user_progress_stats,
)

router = Router()


def get_stats_keyboard(lang: str = DEFAULT_LOCALE) -> InlineKeyboardMarkup:
    """
    У экрана статистики своих кнопок нет.

    Кнопка «🏆 Мой рейтинг» отсюда убрана: рейтинг теперь отдельным пунктом
    ГЛАВНОГО меню, и второй вход в том же боте только путает. Владелец,
    увидев оба сразу: «зачем-то рейтинг отдельная кнопка и в статистике
    тоже — бред».

    Возвращается пустая разметка, а не None: вызывающий код не ветвится,
    Telegram пустую клавиатуру принимает.
    """
    return InlineKeyboardMarkup(inline_keyboard=[])


def create_progress_bar(current: int, total: int, length: int = 10) -> str:
    if total == 0:
        return "░" * length + " 0%"
    percentage = min(100, int((current / total) * 100))
    filled = int((current / total) * length)
    empty = length - filled
    return f"{'▓' * filled}{'░' * empty} {percentage}%"


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
    """
    Кнопка «📊 Статистика» открывает ДОМАШНИЙ ЭКРАН, а не эту простыню.

    Три шкалы отвечают на вопрос, с которым человек сюда и приходит, —
    «где я сейчас», — и дают кнопку заниматься. Простыня на сорок строк
    отвечает на него же, но дольше, и кончается не действием, а объяснением.

    И главное: прежде три шкалы жили только за `/start`, который набирают
    один раз в жизни. Замечание владельца дословно: «меню старт по факту
    юзер видит 1 раз, пока не введёт команду сам». Экран надо ставить туда,
    куда приходят, а приходят сюда.

    Сама статистика никуда не делась — она под кнопкой «📊 Подробнее»
    на домашнем экране.
    """
    from app.bot.handlers.quiz.home import show_home

    user = await session.get(User, message.from_user.id)

    try:
        await message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)

    if not user or not user.level:
        lang = (user.interface_language if user else None) or DEFAULT_LOCALE
        await message.answer(get_text("stats_no_level", lang))
        return

    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="")
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)

    await show_home(message, session, user)


async def build_totals(user: User, session: AsyncSession) -> tuple[int, int]:
    """
    Сколько сборок показано и сколько собрано верно — по изучаемому языку.

    Из `user_words.shown_build`/`correct_build`, то есть из тех же
    счётчиков, что ведёт учёт ответа, а не из отдельного подсчёта по
    строкам: одно число про одно и то же должно браться из одного места.
    """
    pair = pair_from_user(user)
    shown, correct = (await session.execute(
        select(
            func.coalesce(func.sum(UserWord.shown_build), 0),
            func.coalesce(func.sum(UserWord.correct_build), 0),
        ).where(
            UserWord.user_id == user.id,
            UserWord.learning_lang == pair.learning,
        )
    )).one()
    return int(shown), int(correct)


async def build_stats_text(user: User, session: AsyncSession) -> str:
    """
    Подробная статистика одним текстом.

    Вынесена из обработчика, чтобы её можно было показать и с кнопки
    домашнего экрана, и проверить тестом, не поднимая аиограмовского обвеса.
    """
    user_id = user.id
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    # Прогресс по текущему режиму
    progress = await get_mode_progress(user, session)
    # Общий прогресс — по всей базе, доступной на текущей языковой паре
    overall = await get_overall_progress(user_id, session, pair)

    mode_title = _get_mode_title(user, lang)
    mode_arrow = pair_label(pair, lang)

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

    # ЗАГОЛОВОК ОДНОЙ СТРОКОЙ, БЕЗ ЗНАЧКОВ. Прежде тут стояло три строки:
    # `🎯 B1`, `🔄 Німецька → Російська` и полоса, — причём мишень и
    # круговые стрелки не значили ничего, кроме «тут начинается строка», а
    # направление собиралось БЕЗ языка интерфейса и в русском боте
    # показывало украинские названия.
    text += f"<b>{mode_title}</b> · {mode_arrow}\n\n"

    # ШКАЛА СЧИТАЕТСЯ ДО БЛИЖАЙШЕГО РУБЕЖА, А НЕ ДО ВСЕГО УРОВНЯ.
    #
    # Было: «░░░░░░░░░░░░ 0% · Выучено 9 из 3132». Замер 13 октября по 199
    # людям с прогрессом: «выучено» ноль у 156 из них, а знаменатель в три
    # тысячи слов уровня даёт вечные 0% и тем, у кого не ноль. Шкала, которая
    # у всех пустая, не показывает ничего.
    #
    # Рубежи те же, что в поощрении за круг, и по тому же числу — СЛОВАМ В
    # РАБОТЕ: это единственная ступень, которая двигается каждый круг.
    from app.services.praise_service import next_milestone

    in_work = progress["seen_words"]
    target = next_milestone(in_work)
    if target:
        bar = create_progress_bar(in_work, target, length=12)
        text += f"{bar}\n"
        text += get_text(
            "stats_in_work_line", lang,
            count=in_work, target=target, left=target - in_work,
        ) + "\n\n"
    else:
        text += get_text("stats_in_work_top", lang, count=in_work) + "\n\n"

    # Детализация
    text += get_text("stats_details", lang, progress=in_progress, new=new, difficult=difficult) + "\n\n"

    # ДОСТИЖЕНИЯ БЕЗ МЕДАЛЕЙ. Значок выбирался по числу выученных — трофей,
    # золото, серебро, бронза, звезда, — то есть пять разных знаков на одно
    # и то же место. Число и так стоит строкой ниже.
    # Полужирный — в самой локали (`<b>Твои достижения</b>`); обёртка здесь
    # давала `<b><b>…</b></b>` в четырёх заголовках экрана (аудит 14 октября)
    text += f"{get_text('stats_achievements_title', lang)}\n"
    text += get_text("stats_words_count", lang, count=overall_learned) + "\n"

    # Серия — только когда она есть. «Серия: 0 дней подряд» занимает строку
    # ничем и читается как упрёк; у остановившегося она и должна молчать
    streak = current_streak(user)
    if streak:
        text += get_text("stats_streak_line", lang, days=streak) + "\n"
    best = int(getattr(user, "best_streak_days", 0) or 0)
    if best and best != streak:
        text += get_text("stats_best_streak_line", lang, days=best) + "\n"
    # 🧱 ГРАММАТИКА — верные сборки из показанных. Решение владельца: игра
    # «Собираю» проверяет грамматику (порядок слов, формы среди ловушек), и
    # это число стоит в статистике под этим именем. Как серия выше — только
    # когда есть что показать: «0 из 0» читается как упрёк за игру, до
    # которой человек ещё не дошёл (сборка открывается после двух верных)
    built, built_right = await build_totals(user, session)
    if built:
        text += get_text("stats_grammar_line", lang, correct=built_right, shown=built) + "\n"
    text += "\n"

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

        text += f"{get_text('stats_quizzes_header', lang, level=mode_title)}\n"
        text += get_text("stats_quizzes_passed_line", lang, count=total_quizzes) + "\n"
        text += get_text("stats_quizzes_avg_line", lang, percent=f"{avg_percent:.0f}") + "\n"
        text += get_text("stats_quizzes_best_line", lang, percent=f"{best_result:.0f}") + "\n\n"
    else:
        text += f"{get_text('stats_quizzes_header', lang, level=mode_title)}\n"
        text += get_text("stats_quizzes_empty", lang) + "\n\n"

    # Последние викторины
    if mode_sessions:
        text += get_text("stats_recent_header", lang) + "\n"
        for s in mode_sessions[:3]:
            pct = s.accuracy_percent
            date_str = s.started_at.strftime("%d.%m")
            # Значка перед строкой нет: он выбирался по точности и давал
            # пять разных знаков на одно место, тогда как сама точность
            # стоит в той же строке числом
            text += (f"{date_str} — {s.correct_answers}/{s.answered_questions}"
                     f" ({pct:.0f}%)\n")
        text += "\n"

    # ОБЩИЙ ПРОГРЕСС БЕЗ ШКАЛЫ. Выученных 9 от 12 376 слов базы — это ноль
    # процентов, и полоса тут пуста у ВСЕХ, включая самых усердных. Число
    # остаётся: оно честное и растёт, а рисовать по нему полосу — значит
    # каждый раз показывать человеку, что он ничего не добился
    if overall_total > 0:
        text += f"{get_text('stats_overall_header', lang)}\n"
        text += get_text(
            "stats_overall_learned", lang,
            learned=overall_learned, total=overall_total,
        ) + "\n\n"

    # ЧЕТЫРЕ ОБЩИЕ ФРАЗЫ УБРАНЫ. «Отличное начало! Продолжай в том же
    # духе!» выбиралось по доле выученных и не знало о человеке ничего —
    # тот же дефект, что был вторым блоком напоминания. Экран статистики и
    # так весь из чисел; ему нужна не похвала, а пояснение, как они считаны.
    text += f"<i>{get_text('stats_explanation', lang)}</i>"

    return text