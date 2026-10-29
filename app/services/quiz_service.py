"""
Движок викторины: подбор слова по SRS, сборка вариантов ответа, учёт прогресса.

Не зависит от изучаемого языка — язык приходит в LanguagePair. Слова берутся
только канонические для изучаемого языка (см. app/services/word_groups.py),
иначе одно и то же слово встречалось бы несколько раз.
"""

import collections
import random
from datetime import datetime, timedelta
from app.core.clock import utcnow
from typing import Optional

from sqlalchemy import and_, case, func, literal_column, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.database.enums import CEFRLevel, QuizChannel, QuizMode, counted_channels
from app.database.models import (
    PartOfSpeech, QuizQuestion, QuizSession, User, UserWord, Word, WordFrequency, WordLangGroup,
)
from app.services import build_service
from app.services.word_level import level_expr, level_of
from app.services.goal_service import categories_for
from app.services.language_service import (
    LanguagePair,
    fold,
    get_language,
    pair_for_channel,
    display_text,
    main_meaning,
    meaning_variants,
    option_label,
    pair_from_user,
    word_column,
    word_text,
)

# ==================== КОНСТАНТЫ SRS ====================
MIN_ATTEMPTS_FOR_LEARNED = 3

# УЖЕ ИЗВЕСТНОЕ СЛОВО — ДВАЖДЫ, А НЕ ТРИЖДЫ (патч 2.1). Отзыв 15.10: «если
# я прохожу уровень без ошибок, мне не надо доказывать тремя проходами,
# что всё запомнил»; владелец: «если с первого раза правильно — сократить
# повтор». Новое слово, отвеченное верно при первой же встрече, начинает
# серию с двух: следующий повтор — через 3 дня, и одного верного ответа там
# хватает до «выучено». Угадывание (25% при четырёх вариантах) отсекает
# эта проверка: угаданное слово на ней чаще всего ломается и идёт заново.
# Кнопки «знаю это слово» нет — решение владельца: «случайно тыкнешь — то
# же угадывание».
FIRST_SIGHT_STREAK = 2
LEARNED_SUCCESS_RATE = 90
LEARNED_SHOW_PROBABILITY = 0.01

# Слово нельзя считать выученным в день знакомства: три угадывания подряд
# внутри одного дня — это не запоминание. Требуем, чтобы между первым
# показом и моментом «выучено» прошли сутки.
MIN_DAYS_BEFORE_LEARNED = 1

STRUGGLING_WORDS_RATIO = 0.60
NEW_WORDS_RATIO = 0.30
REVIEW_WORDS_RATIO = 0.09
LEARNED_WORDS_RATIO = 0.01

STRUGGLING_THRESHOLD = 70
REVIEW_THRESHOLD = 90

# Пауза между повторами слова в рамках одной сессии подбора
REPEAT_COOLDOWN = timedelta(hours=1)


# ============================================================================
# ИНТЕРВАЛЬНОЕ ПОВТОРЕНИЕ
# ============================================================================
#
# ЗАЧЕМ ЭТО ПОЯВИЛОСЬ. Прежде все корзины подбора ключевались на ТОЧНОСТИ:
# трудные (<70%), новые (ряда нет), на повторение (70–90%), выученные. Слово,
# отвеченное верно с первого раза, имеет точность 100% и метки «выучено» не
# имеет — то есть не попадало НИ В ОДНУ корзину и больше не показывалось.
#
# Откат в конце каскада (`get_any_word`) формально существовал, но достижим
# только когда пусты все корзины, включая новые, — а новых хватает всем: у
# самого активного человека в запасе ещё 464 слова его уровня.
#
# Замер 13 октября 2026 по рабочей копии:
#
#     слов в прогрессе                       21 306
#     НЕ ВЕРНУТСЯ НИКОГДА                    18 664  (87.6%)
#     людей задето                              193 из 199
#     в среднем недостижимо у человека          84.5% его словаря
#     слов в корзине «на повторение»               3  (на них шло 9% подбора)
#
# И следствие, которое всё объясняет: **98.2% выученных слов человек хотя бы
# раз отвечал НЕВЕРНО** (1 509 из 1 537). Чтобы выучить слово, надо было
# сперва его провалить: только ошибка роняла точность ниже 70 и возвращала
# слово в подбор. Ответил верно с первого раза — потерял слово.
#
# ПОЧЕМУ ИМЕННО ТАКИЕ СРОКИ. Выведены из поведения, а не из учебника. Замер
# разрывов между днями занятий:
#
#     через 1 день   56.6%   <-- больше половины всех возвратов
#     через 2 дня    17.2%   (накопленно 73.8%)
#     за неделю      90.5%
#
# Отсюда первая ступень — СУТКИ: назавтра возвращается большинство, и слова
# прошлого дня должны их ждать. Короче суток делать нельзя: 71% дней — это
# два круга и больше, а разрыв между ними всего 0.4 часа, то есть одно
# сидение. Слово с интервалом в четыре часа вернулось бы через двадцать
# минут — не повторение, а назойливость.
#
# Серия 0 — это промах, и час берётся не из расписания, а из
# `REPEAT_COOLDOWN`: немедленный повтор у нас делает отдельная кнопка
# «повторить ошибки», и дублировать её подбором незачем.
#
# ЧИСЛА ИНТЕРВАЛОВ — РЕШЕНИЕ ВЛАДЕЛЬЦА, а не свойство механики: её можно
# менять, не трогая ничего, кроме этой таблицы.
REVIEW_SCHEDULE: dict[int, timedelta] = {
    0: REPEAT_COOLDOWN,
    1: timedelta(days=1),
    2: timedelta(days=3),
    3: timedelta(days=7),
    4: timedelta(days=21),
}

# Серия пятая и дальше — поддержание. Слово человек знает, и возвращается оно
# редко: чтобы не забылось, а не чтобы занять место в круге.
REVIEW_SCHEDULE_TAIL = timedelta(days=60)

# Сколько НОВЫХ слов в круге из пятнадцати. Это пол, а не потолок: если
# просроченных не хватает, новые доберут остаток.
#
# Зачем пол. Повторение — то, что учит, но открытие нового — то, за чем
# приходят. Круг целиком из повторений читается как домашняя работа, и
# человек, вернувшийся после месяца с пятьюстами просроченными слов, иначе
# не увидел бы ни одного нового никогда.
NEW_WORDS_PER_ROUND = 3

# Длина круга по умолчанию — для случаев, когда подбор не знает её (прямой
# вызов из приёмки, первый вопрос до создания занятия).
DEFAULT_ROUND_LENGTH = 15

# ПЕРВОЕ ЗАНЯТИЕ КОРОЧЕ. Прод 15.10: новички уходили на втором-пятом
# вопросе из пятнадцати, не увидев ни итога, ни зачем это всё. Семь —
# короткое знакомство: итог и первая победа приходят через пару минут, а
# доска (ей нужно не меньше пяти вопросов в круге) в нём ещё помещается
FIRST_LESSON_LENGTH = 8  # знакомство: по два слова A1, A2, B1, B2 (`first_lesson`)


def in_first_lesson(user) -> bool:
    """
    Человек ещё на ПЕРВОМ УРОКЕ (патч 2.1): не закончил ни одного занятия и
    не ответил на 7 вопросов всего (`users.onboarded_at` пусто).

    ЗАЧЕМ. Прод 15.10: 21 из 32 брошенных занятий брошены на 0–2-м вопросе;
    польский новичок первым словом получил многозначное «mieć na myśli» и
    ушёл после первого ответа. Владелец: «первые 7 с лёгкими вопросами,
    чтобы юзер как можно прошёл первый круг… и получил дофамин». И: «даже
    если по какой-то причине он его сбросит — чтобы открывалась полноценная
    игра после первого круга» — поэтому отметка ставится и после 7 ответов
    в брошенных занятиях: лёгкий режим не держит вечно.
    """
    if user is None:
        return False
    if getattr(user, "onboarded_at", None) is not None:
        return False
    return not (getattr(user, "quizzes_passed", 0) or 0)


def lesson_length(user) -> int:
    """
    Сколько вопросов в занятии. Первое — короче, пока человек на первом
    уроке (`in_first_lesson`); дальше — его настройка. Одно место для всех,
    кто это число показывает: кнопки «Учить N слов», вступление, напоминание.
    """
    chosen = (getattr(user, "quiz_word_count", None) if user is not None else None) or DEFAULT_ROUND_LENGTH
    if in_first_lesson(user):
        # Короче, но не длиннее выбранного: первое занятие не растягивается
        return min(FIRST_LESSON_LENGTH, chosen)
    return chosen

# Сколько кандидатов тянуть из БД, чтобы набрать 3 различных дистрактора.
# С запасом: часть кандидатов отсеется как совпадающие по тексту.
DISTRACTOR_CANDIDATES = 16
OPTIONS_TOTAL = 4


# ============================================================================
# БАЗОВЫЙ ЗАПРОС: канонические слова с пригодными переводами
# ============================================================================

def _usable_words(pair: LanguagePair):
    """
    Слова, годные для викторины на данной паре языков.

    Условия:
      - слово каноническое для изучаемого языка (дубли схлопнуты);
      - текст есть и на изучаемом, и на языке значения — иначе карточку
        нечем показать или нечем подписать.
    """
    native_col = word_column(pair.native)
    learning_col = word_column(pair.learning)

    query = (
        select(Word)
        .join(
            WordLangGroup,
            and_(
                WordLangGroup.word_id == Word.id,
                WordLangGroup.lang == pair.learning,
                WordLangGroup.is_canonical.is_(True),
            ),
        )
        .where(
            native_col.isnot(None),
            func.btrim(native_col) != "",
            learning_col.isnot(None),
            func.btrim(learning_col) != "",
        )
    )
    return query


def _apply_quiz_mode_filter(query, user: User):
    """
    Фильтр по режиму викторины.

    LEVEL     — по user.level
    CATEGORY  — по user.quiz_category, все уровни
    ALL_WORDS — без фильтра
    DIFFICULT — обрабатывается отдельно в get_difficult_word
    """
    if user is None:
        return query

    if user.quiz_mode == QuizMode.CATEGORY:
        if user.quiz_category:
            return query.where(Word.category == user.quiz_category)
        return query.where(level_expr(user.learning_lang) == user.level)

    if user.quiz_mode == QuizMode.ALL_WORDS:
        return query

    if user.quiz_mode == QuizMode.DIFFICULT:
        return query

    # LEVEL и всё неизвестное. Уровень — В ИЗУЧАЕМОМ ЯЗЫКЕ (`word_level`)
    return query.where(level_expr(user.learning_lang) == user.level)


def _exclude(query, exclude_ids: Optional[list[int]]):
    if exclude_ids:
        return query.where(Word.id.not_in(exclude_ids))
    return query


async def _pick_one(session: AsyncSession, query) -> Optional[Word]:
    """
    Одно случайное слово. Выборка случайного делается в БД: раньше здесь
    выгружались все подходящие строки (в режиме «Все слова» — тысячи ORM-объектов
    на каждый вопрос) и random.choice применялся в Python.
    """
    result = await session.execute(query.order_by(func.random()).limit(1))
    return result.scalars().first()


# Из скольких самых ходовых невиденных слов уровня выбирать новое. Не из
# десяти: верх частотного списка — служебные слова (der, und, in, ich), и
# первое занятие новичка состояло бы из них. Сто пятьдесят смешивают их с
# Haus, Mutter, gut, fahren, а редкое экзаменационное (Familienstand,
# buchstabieren) приходит позже
COMMON_POOL = 150
# Первый урок: из 60 самых частых — однословные существительные, глаголы,
# прилагательные не длиннее 10 букв (`get_new_words`)
EASY_POOL = 60
EASY_MAX_LETTERS = 10


# На сколько служебное слово «реже» в очереди новых: der, von, zwischen, but
# занимали половину первого занятия (замер 15.10: bei, von, zwischen, nun,
# mal из 15). Они не пропадают — просто содержательные идут чаще раньше
#
# Второй замер, после уровней по языкам (15.10): у английского, польского,
# украинского уровень A1 стал частотным, и первое занятие снова состояло из
# you, a, the, with it / na, ten, do / з, для, в. Штраф поднят: служебные —
# на 2.5, наречия — на 1.0; в начале — существительные, глаголы, признаки
FUNCTION_WORD_PENALTY = 2.5
ADVERB_PENALTY = 1.0
EASY_POS = (PartOfSpeech.NOUN, PartOfSpeech.VERB, PartOfSpeech.ADJECTIVE)
_FUNCTION_POS = (PartOfSpeech.PRONOUN, PartOfSpeech.PREPOSITION,
                 PartOfSpeech.CONJUNCTION, PartOfSpeech.OTHER)


def _function_word_penalty():
    return case(
        (Word.pos.in_(_FUNCTION_POS), FUNCTION_WORD_PENALTY),
        (Word.pos == PartOfSpeech.ADVERB, ADVERB_PENALTY),
        else_=0.0,
    )


async def _pick_common(session: AsyncSession, query, lang: str,
                       pool: Optional[int] = None) -> Optional[Word]:
    """
    Новое слово — случайное среди самых ходовых на изучаемом языке.

    Прежде — случайное из всего уровня: новичок A1 получал Strumpf (22 385-е
    по частоте) раньше Haus. Прод 15.10: новички уходили после первых
    слов, отвечая на всё верно. Частота — по ИЗУЧАЕМОМУ языку
    (`WordFrequency`); слово без частоты идёт последним, но не пропадает.
    """
    pool = (
        query.outerjoin(
            WordFrequency,
            and_(WordFrequency.word_id == Word.id, WordFrequency.lang == lang),
        )
        .order_by((WordFrequency.zipf - _function_word_penalty()).desc().nulls_last(), Word.id)
        .limit(pool or COMMON_POOL)
        .subquery()
    )
    picked = aliased(Word, pool)
    result = await session.execute(select(picked).order_by(func.random()).limit(1))
    return result.scalars().first()


# ============================================================================
# SRS: ВЫБОР СЛОВА ПО ПРИОРИТЕТУ
# ============================================================================

def wants_new_word(position: int, round_length: int) -> bool:
    """
    Пора ли на этом месте круга дать НОВОЕ слово.

    СОСТАВ КРУГА СЧИТАЕТСЯ ПО МЕСТУ, А НЕ ЖРЕБИЕМ, и это главная перемена.
    Прежде на каждый вопрос бросался случай: 60% трудным, 30% новым, 9%
    повторению, 1% выученным. Случай не умеет держать состав: в круге из
    пятнадцати при тридцати процентах новых их выходило от нуля до девяти.

    Новые раскладываются РОВНО по круге, а не кучей в конце: человек видит
    открытие каждые несколько вопросов, и круг не делится на «скучную
    половину» и «интересную».

        круг из 15, новых 3  →  шаг 5  →  новое на 5-м, 10-м и 15-м
        круг из 10, новых 2  →  шаг 5  →  новое на 5-м и 10-м
        круг из 5,  новое 1  →  шаг 5  →  новое на 5-м

    ОДНО НОВОЕ НА ПЯТЬ ВОПРОСОВ, а не три на любой круг. Прежде короткий круг
    тоже требовал трёх новых: у круга из пяти шаг выходил 2, новые вставали
    на 2-е и 4-е места — ровно на все места отработки (каждое второе), и
    «Вспоминаю», «Слушаю», «Говорю» в такой круг не попадали никогда. На
    круге из пятнадцати не меняется ничего.

    Это ПОЛ, а не потолок: если просроченных слов не хватает, оставшиеся
    места тоже займут новые — так и выглядит первый день, когда повторять
    ещё нечего.
    """
    new_words = max(1, min(NEW_WORDS_PER_ROUND, round_length // 5))
    step = max(2, round_length // new_words)
    return (position + 1) % step == 0


async def select_word_by_priority(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
    round_length: int = DEFAULT_ROUND_LENGTH,
    position: Optional[int] = None,
) -> Optional[Word]:
    """
    Слово для вопроса: сперва то, чему ПОРА, новое — по расписанию места.

    ПОРЯДОК ПОПЫТОК

        место под новое   новое → просроченное → трудное → любое
        прочие места      просроченное → трудное → новое → любое

    Почему просроченное впереди трудного: трудное, которому пора, и так
    просрочено — корзина «трудных» тоже ждёт срока (`_due_condition`), и
    отдельной она осталась ради режима «сложные слова» и как страховка.
    Прежде это обоснование утверждало «серия у трудного нулевая», что
    неверно: серия 2 при точности 40% — обычное дело.

    Почему «любое» в конце: когда у человека кончились и новые слова, и
    просроченные, круг всё равно должен состояться. Прежде этот откат был
    единственным путём для слова, отвеченного верно с первого раза, — и
    недостижимым, потому что новые не кончаются.

    `round_length` нужен только для раскладки новых по месту; подбор от него
    больше ничем не зависит.

    `position` — номер места в круге с нуля. Не передан — берётся число
    уже заданных слов; но после доски их на четыре больше, чем вопросов
    (доска — один вопрос из пяти слов), поэтому круг передаёт номер сам.
    """
    if position is None:
        position = len(exclude_ids)

    # ОТРАБОТКА — НА КАЖДОМ ВТОРОМ МЕСТЕ, не под новые слова. Каждое второе,
    # а не все: в первом круге дня новых по-прежнему большинство (в круге из
    # 15 — девять), а со второго круга идут все игры. Отдай отработке все
    # места — и новых за круг осталось бы три: за открытием приходят.
    practice_slot = position % 2 == 1

    if wants_new_word(position, round_length):
        order = (get_new_words, get_due_words, get_struggling_words)
    elif practice_slot:
        order = (get_due_words, get_struggling_words, get_practice_words,
                 get_new_words)
    else:
        order = (get_due_words, get_struggling_words, get_new_words,
                 get_practice_words)

    for getter in order:
        word = await getter(
            user_id, session, pair, exclude_ids, user=user, level=level
        )
        if word:
            return word

    return await get_any_word(user_id, session, pair, exclude_ids, user=user, level=level)


def _scoped(query, user: Optional[User], level: Optional[CEFRLevel]):
    """Ограничить выборку режимом пользователя либо явным уровнем."""
    if user is not None:
        return _apply_quiz_mode_filter(query, user)
    if level is not None:
        return query.where(Word.level == level)
    return query


def _review_scoped(query, user: Optional[User], level: Optional[CEFRLevel]):
    """
    Ограничить выборку УЖЕ НАЧАТЫХ слов: повторение, трудные, закрепление.

    УРОВЕНЬ РЕШАЕТ, КАКИЕ НОВЫЕ СЛОВА ДАВАТЬ, — НЕ КАКИЕ ПОВТОРЯТЬ. Начатое
    слово возвращается в срок, на каком бы уровне оно ни числилось. Прежде
    повторение шло только по словам текущего уровня, и это ломало прогресс
    дважды: при подъёме уровня слова прежнего переставали возвращаться и
    забывались, а при переуровнении словаря 15.10 по спискам Goethe у 165
    человек ушло бы с уровня 4 317 слов в работе — у половины людей
    половина их слов перестала бы повторяться.

    Режим «по теме» с темой и прочие — как прежде (`_scoped`).
    """
    if user is not None and user.quiz_mode in (QuizMode.LEVEL, None):
        return query
    if user is not None and user.quiz_mode == QuizMode.CATEGORY and not user.quiz_category:
        return query
    return _scoped(query, user, level)


def _progress_join(query, user_id: int, pair: LanguagePair):
    """Присоединить прогресс пользователя по этому языку."""
    return query.join(
        UserWord,
        and_(
            UserWord.word_id == Word.id,
            UserWord.user_id == user_id,
            UserWord.learning_lang == pair.learning,
        ),
    )


def _accuracy_below(threshold: int):
    return (UserWord.times_correct * 100.0 / UserWord.times_shown) < threshold


def _cooled_down():
    cutoff = utcnow() - REPEAT_COOLDOWN
    return or_(UserWord.last_seen_at.is_(None), UserWord.last_seen_at < cutoff)


def _answered_before(user_id: int, pair: LanguagePair, cutoff: datetime):
    """
    Последний ОТВЕТ по слову был раньше `cutoff`.

    По строкам ответов (`quiz_questions.answered_at`), а не по
    `last_seen_at`, и это не одно и то же. `last_seen_at` — якорь
    расписания, и досрочный верный ответ (отработка другой игрой) его
    нарочно не двигает. Пауза отработки, построенная на нём, не работала
    вовсе: слово, отвеченное досрочно секунды назад, числилось «показанным
    позавчера» и открывало следующий круг. Проверено исполнением: шесть
    знакомых слов возвращались в каждом круге подряд.

    Не `user_words.updated_at`: его двигает любая запись ряда — правка
    учёта, пересчёт, — и после такой правки весь словарь человека на три
    минуты выпадал бы из отработки. Строка ответа пишется только ответом.
    """
    from app.database.models import QuizQuestion, QuizSession

    recent = (
        select(QuizQuestion.id)
        .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
        .where(
            QuizQuestion.word_id == Word.id,
            QuizSession.user_id == user_id,
            QuizSession.learning_lang == pair.learning,
            QuizQuestion.answered_at >= cutoff,
        )
        .exists()
    )
    return ~recent


def _due_condition():
    """
    Условие «слово пора повторить» по расписанию, а не по точности.

    Собирается из `REVIEW_SCHEDULE`: для каждой длины серии свой срок. Серия
    длиннее последней ступени попадает в хвост (`REVIEW_SCHEDULE_TAIL`).

    `last_seen_at` пустой означает «не показывалось» — такое слово пора
    всегда. Это не теория: у рядов, созданных до появления колонки, он
    пустой, и терять их нельзя.
    """
    now = utcnow()
    longest = max(REVIEW_SCHEDULE)

    clauses = [UserWord.last_seen_at.is_(None)]
    for streak, delay in REVIEW_SCHEDULE.items():
        clauses.append(
            and_(
                UserWord.correct_streak == streak,
                UserWord.last_seen_at <= now - delay,
            )
        )
    clauses.append(
        and_(
            UserWord.correct_streak > longest,
            UserWord.last_seen_at <= now - REVIEW_SCHEDULE_TAIL,
        )
    )
    return or_(*clauses)


async def get_due_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> Optional[Word]:
    """
    Слово, которому ПОРА вернуться. Самое залежавшееся вперёд.

    Это главная корзина подбора, и до 13 октября 2026 её не было вовсе —
    разбор в шапке файла у `REVIEW_SCHEDULE`.

    ПОРЯДОК НЕ СЛУЧАЙНЫЙ, в отличие от остальных корзин: берётся слово с
    самым давним показом. У человека, вернувшегося после месяца, долг
    разбирается с самого старого, а не наугад — иначе часть слов висела бы
    просроченной годами, пока жребий до них не дойдёт.
    """
    query = _progress_join(_usable_words(pair), user_id, pair).where(
        _due_condition()
    )
    query = _exclude(_review_scoped(query, user, level), exclude_ids)
    # Выученные НЕ отсеиваются: их срок — 21 и 60 дней, и возвращаются они
    # ровно затем, чтобы не забылись. Прежде выученному доставался 1%
    # подбора, то есть забывались они тихо.
    rows = await session.execute(
        query.order_by(UserWord.last_seen_at.asc().nullsfirst()).limit(1)
    )
    return rows.scalars().first()


async def count_due_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> int:
    """Сколько слов ждёт повторения. Нужно экранам и напоминаниям."""
    query = _progress_join(
        select(func.count()).select_from(Word), user_id, pair
    ).where(_due_condition())
    query = _review_scoped(query, user, level)
    return int((await session.execute(query)).scalar() or 0)


# Сколько ждать, прежде чем слово, увиденное сегодня, вернётся ДРУГОЙ игрой.
# Внутри круга повтор и так запрещён (`exclude_ids`), так что пауза нужна
# только между кругами: только что отвеченное не должно открывать следующий.
#
# Три минуты, а не десять: владелец играет круги подряд, и при десяти
# второй круг, начатый сразу за первым, не находил ни одного слова для
# отработки — снова одни карточки. Три минуты — это конец прошлого круга.
PRACTICE_GAP = timedelta(minutes=3)


async def get_practice_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> Optional[Word]:
    """
    Слово для ОТРАБОТКИ: уже узнанное, ещё не просроченное — другой игрой.

    ЗАЧЕМ. Игры открываются для каждого слова отдельно — припоминание и слух
    после одного верного ответа, речь после двух, — а возвращается слово
    только по расписанию: верно ответил — до завтра. Значит в один день круг
    собирался из одних новых слов, а у нового открыта лишь карточка. Живой
    тест владельца 14 октября: 101 ответ за день, из них 91 карточка и 10
    пар доски, НИ ОДНОГО «Вспоминаю», «Слушаю» или «Говорю» — при 70 словах,
    уже готовых к ним. «Ниразу не было режима реверса. Ниразу не предложило
    мне голосовое записать».

    Отработка — это не досрочный повтор: слово приходит другой игрой, а
    расписание при этом не двигается (см. `update_word_progress`, «досрочно»).

    Порядок — ЛЕСЕНКА: узнал → вспомнил или услышал → сказал. Первым идёт
    слово, уже готовое к речи (два верных) и ни разу не произнесённое;
    затем — с наименьшим числом показов в других играх, чтобы отработку
    получали разные слова. Без первого правила «Говорю» не наступало
    никогда: свежих слов с одним верным всегда больше, и они занимали все
    места отработки — симуляция четырёх кругов подряд дала ноль речи.
    """
    cutoff = utcnow() - PRACTICE_GAP
    query = _progress_join(_usable_words(pair), user_id, pair).where(
        UserWord.learned.is_(False),
        UserWord.times_correct >= CHANNEL_UNLOCK[QuizChannel.REVERSE],
        UserWord.last_seen_at.isnot(None),
        # Пауза — от последнего ОТВЕТА, а не от якоря расписания
        _answered_before(user_id, pair, cutoff),
        ~_due_condition(),
    )
    query = _exclude(_review_scoped(query, user, level), exclude_ids)
    # Показы ВО ВСЕХ ИГРАХ, кроме карточки, — правилом, а не списком:
    # шестая игра, забытая здесь, не считалась бы отработкой, и одно и то
    # же слово собиралось бы снова и снова
    other_games = sum(
        (getattr(UserWord, f"shown_{c.key}") for c in counted_channels()),
        start=literal_column("0"),
    )
    ready_to_speak = case(
        (and_(UserWord.times_correct >= CHANNEL_UNLOCK[QuizChannel.SPEECH],
              UserWord.shown_speech == 0), 0),
        else_=1,
    )
    rows = await session.execute(
        query.order_by(ready_to_speak, other_games.asc(), func.random()).limit(1)
    )
    return rows.scalars().first()


async def get_ready_for(
    channel: QuizChannel,
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    gap: Optional[timedelta] = None,
) -> Optional[Word]:
    """
    Слово, ДОРОСШЕЕ до этой игры: для входа одной игрой с главного экрана и
    для чередования игр в круге (`_rotation`).

    Слово, которому ПОРА на повтор, идёт первым: отработка в другой игре —
    лучший способ его повторить. `gap` — не брать только что отвеченное.

    Человек нажал 🎤 «Говорю» и ждёт речи. Прежде круг брал следующее слово
    по расписанию, а оно чаще всего новое — и приходило карточкой: порог
    речи — два верных ответа на ЭТО слово. Владелец, 14 октября: «я банально
    не могу проверить тест Говорения, потому что оно мне не попадается…
    юзер зашёл, ожидает одно, играет в другое». Теперь сперва ищется слово,
    для которого игра уже открыта, — меньше всего бывавшее в ней. Не нашлось
    — обычный подбор, и слово придёт той игрой, до которой доросло.
    """
    shown = getattr(UserWord, f"shown_{channel.key}")
    query = _progress_join(_usable_words(pair), user_id, pair).where(
        UserWord.times_correct >= CHANNEL_UNLOCK[channel],
    )
    if channel is QuizChannel.BUILD:
        # Сборке нужен пример на обоих языках; число слов в нём решает
        # `fits` ниже, уже в Python. И слово не выше уровня человека
        # (`build_level_fits`) — уже в запросе, чтобы двадцать кандидатов
        # не ушли на слова, которые сборке всё равно не годятся
        query = query.where(*build_service.sql_prefilter(pair))
        level = getattr(user, "level", None)
        if level is not None:
            query = query.where(level_expr(pair.learning).in_(
                [lv for lv in CEFRLevel if _LEVEL_RANK[lv] <= _LEVEL_RANK[level]]))
    if gap is not None:
        # Пауза — от последнего ОТВЕТА (`_answered_before`): досрочный ответ
        # `last_seen_at` не двигает, и пауза по нему не держала ничего
        query = query.where(UserWord.last_seen_at.isnot(None),
                            _answered_before(user_id, pair, utcnow() - gap))
    query = _exclude(_scoped(query, user, None), exclude_ids)
    due_first = case((_due_condition(), 0), else_=1)
    # Игре с отбором в Python — запас кандидатов: у сборки годна не каждая
    # фраза (3–10 слов), и первое по порядку слово может не подойти.
    # Остальным играм хватает одного
    limit = 1 if channel is not QuizChannel.BUILD else FIT_CANDIDATES
    # 🧱 У СБОРКИ ПЕРВОЙ ИДЁТ ФРАЗА, КОТОРУЮ ЧЕЛОВЕК ЕЩЁ НЕ СОБИРАЛ, а не та,
    # которой пора на повтор. Владелец, 27.10: «грамматика должна быть по
    # сути всегда разная… повторяется каждый раз то же самое, это очень
    # тупо». Слово повторяется карточками, сборка учит грамматике
    order = ((shown.asc(), due_first) if channel is QuizChannel.BUILD
             else (due_first, shown.asc()))
    rows = await session.execute(
        query.order_by(*order, func.random()).limit(limit)
    )
    level = getattr(user, "level", None)
    found = next((w for w in rows.scalars() if channel_fits(channel, w, pair, level)), None)
    if channel is QuizChannel.BUILD and found is not None and await _built_before(
            session, user_id, found.id, pair):
        # Свои несобранные кончились — фраза из общей базы (`_fresh_build`)
        return await _fresh_build(session, user_id, pair, exclude_ids, level) or found
    return found


async def _started(session: AsyncSession, user_id: int, word_id: int,
                   pair: LanguagePair) -> bool:
    return (await session.execute(
        select(UserWord.word_id).where(UserWord.user_id == user_id,
                                       UserWord.word_id == word_id,
                                       UserWord.learning_lang == pair.learning)
    )).first() is not None


async def _built_before(session: AsyncSession, user_id: int, word_id: int,
                        pair: LanguagePair) -> bool:
    shown = (await session.execute(
        select(UserWord.shown_build).where(UserWord.user_id == user_id,
                                           UserWord.word_id == word_id,
                                           UserWord.learning_lang == pair.learning)
    )).scalar()
    return bool(shown)


async def _fresh_build(session: AsyncSession, user_id: int, pair: LanguagePair,
                       exclude_ids: list[int],
                       level: Optional[CEFRLevel]) -> Optional[Word]:
    """
    Фраза для сборки из ОБЩЕЙ БАЗЫ: слово, которого человек не начинал, и
    чью фразу он ещё не собирал. Уровень — не выше его (`build_level_fits`).

    Только когда сборка у человека уже открыта и свои фразы собраны все
    (`get_ready_for`): порог «два верных» остаётся. Ответ на такую фразу —
    «только грамматика» (`_record_answer`), слово начатым не становится.
    """
    from app.database.models import QuizQuestion, QuizSession

    started =select(UserWord.word_id).where(UserWord.user_id == user_id,
                                             UserWord.learning_lang == pair.learning)
    built = (select(QuizQuestion.word_id)
             .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
             .where(QuizSession.user_id == user_id,
                    QuizSession.learning_lang == pair.learning,
                    QuizQuestion.grammar_only.is_(True)))
    query = (_usable_words(pair)
             .where(*build_service.sql_prefilter(pair))
             .where(Word.id.not_in(started), Word.id.not_in(built)))
    if level is not None:
        query = query.where(level_expr(pair.learning).in_(
            [lv for lv in CEFRLevel if _LEVEL_RANK[lv] <= _LEVEL_RANK[level]]))
    rows = await session.execute(
        _exclude(query, exclude_ids).order_by(func.random()).limit(FIT_CANDIDATES))
    return next((w for w in rows.scalars()
                 if channel_fits(QuizChannel.BUILD, w, pair, level)), None)


# Сколько кандидатов тянуть для игры, годность которой решается в Python.
# Замер по dev-базе 14 октября: сборке годится от 91% (турецкий, у него
# много примеров короче трёх слов) до 97% (немецкий) канонических слов, так
# что из двадцати негодными окажутся все с вероятностью меньше 10^-20
FIT_CANDIDATES = 20


def channel_fits(channel: QuizChannel, word: Word, pair: LanguagePair,
                 level: Optional[CEFRLevel] = None,
                 word_level: Optional[CEFRLevel] = None) -> bool:
    """
    Годится ли слово для этой игры ПО СВОИМ ДАННЫМ, а не по прогрессу.

    Порог допуска (`CHANNEL_UNLOCK`) спрашивает человека: доросло ли
    слово. Здесь спрашивается само слово: есть ли из чего собрать вопрос.
    Сейчас такое условие есть у одной игры — у сборки нужен пример в 3–9
    слов с переводом; остальные игры собираются из любого слова (их откат
    при неудаче — в `generate_question`).

    `level` — уровень человека: сборка берёт слова НЕ ВЫШЕ него
    (`build_level_fits`). Без уровня (приёмки) — без этого условия.
    """
    if channel is QuizChannel.BUILD:
        # Уровень СЛОВА — в изучаемом языке (`word_level`). `Word.level` —
        # немецкий (Goethe), и у учащего английский сборка сверялась с чужим
        # уровнем (аудит подбора 15.10). Не передан и язык не немецкий —
        # проверки нет: подбор (`get_ready_for`) уже отсеял по `level_expr`
        if word_level is None and pair.learning == "de":
            word_level = word.level
        return (build_level_fits(word_level, level)
                and build_service.fits(word, pair, level))
    return True


# Порядок уровней A1 → C2 — по объявлению в enum
_LEVEL_RANK = {level: rank for rank, level in enumerate(CEFRLevel)}


def build_level_fits(word_level: Optional[CEFRLevel], level: Optional[CEFRLevel]) -> bool:
    """
    Сборка — только по словам НЕ ВЫШЕ уровня человека.

    В режимах «По теме» и «Все слова» приходят слова любого уровня, и
    пример к слову C1 — фраза уровня C1. Живой тест владельца 14.10 (уровень
    A2, режим «по теме»): «Die Kritik an seinem Plan war nicht
    ungerechtfertigt» — «слишком топорный вариант, будто так не общаются, от
    этого выглядит сложным вдвойне». Узнавать такое слово — посильно,
    собирать его фразу на A2 — нет. Оно придёт остальными играми.
    """
    if level is None or word_level is None:
        return True
    return _LEVEL_RANK[word_level] <= _LEVEL_RANK[level]


def _rotation(user: User, exclude_ids: list[int],
              recent: Optional[list[str]],
              position: Optional[int] = None,
              round_length: Optional[int] = None) -> list[QuizChannel]:
    """
    Какие игры попробовать на этом месте круга, по очереди.

    ВСЕ ИГРЫ В КАЖДОМ КРУГЕ — владелец, 14 октября: «а можно чтобы каждая
    игра включала в себя все виды игр? так же веселее. Кроме понятное дело
    для новичков». Места отработки (каждое второе, не под новые слова)
    отдаются той игре, которой в круге было МЕНЬШЕ ВСЕГО, — и под неё
    ищется слово, к ней готовое. Так «Вспоминаю», «Слушаю» и «Говорю»
    чередуются, а не выпадают по жребию.

    НОВИЧКА ЭТО НЕ ТРОГАЕТ, и отдельного режима для него не нужно: игра
    открывается по слову (1 верный — припоминание и слух, 2 — речь), и пока
    готовых слов нет, круг сам выходит карточками. База набирается — игры
    подключаются по одной.

    ПРАВИЛА СОСТАВА — ТЕ ЖЕ, ЧТО У `place_in_round`, и это одно правило, а
    не копия: `_speech_closed` и «не две одинаковые подряд» спрашиваются у
    тех же функций. Прежде слово, подобранное под игру, получало её минуя
    состав, и речь приходила ТРИ раза за круг при потолке два — в 4 кругах
    из 8 (замер на продвинутом). Разница одна: там закрытая игра уступает
    лишь при наличии замены, а здесь закрытая просто не пробуется — замена
    у места отработки есть всегда, обычный подбор.

    `position` — номер места с нуля, `round_length` — длина ЭТОГО круга
    (в «сложных» она короче настройки).
    """
    if position is None:
        position = len(exclude_ids)
    if round_length is None:
        round_length = getattr(user, "quiz_word_count", None) or DEFAULT_ROUND_LENGTH
    if position % 2 == 0 or wants_new_word(position, round_length):
        return []
    history = _channel_history(recent or [])
    used = collections.Counter(history)
    # Все игры, кроме карточки, — из перечисления, а не списком руками:
    # шестая («Собираю») встаёт в чередование сама
    games = [c for c in enabled_channels(user) if c is not QuizChannel.TEXT]
    # Номер вопроса для правил состава — с единицы
    if _speech_closed(used, position + 1, round_length):
        games = [c for c in games if c is not QuizChannel.SPEECH]
    if history:
        games = [c for c in games if c is not history[-1]]
    return sorted(games, key=lambda c: (used[c], games.index(c)))


async def get_struggling_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> Optional[Word]:
    # ТРУДНОЕ ТОЖЕ ЖДЁТ СВОЕГО СРОКА. Прежде здесь стояли только точность
    # ниже 70% и часовая пауза, и корзина обходила расписание: слово с 2
    # верными из 5 и серией 2 (срок три дня), показанное два часа назад, не
    # было просроченным — и всё равно приходило на первом же месте круга,
    # потому что эта корзина идёт сразу за просроченными. Проверено
    # исполнением. Точность — накопленная, и у слова, которое человек уже
    # начал отвечать верно, она ещё долго ниже 70: оно возвращалось бы
    # каждый час, вытесняя новые.
    #
    # Режим «сложные слова» (`get_difficult_word`) срока НЕ ждёт нарочно: там
    # человек сам попросил гонять трудное.
    query = _progress_join(_usable_words(pair), user_id, pair).where(
        UserWord.learned.is_(False),
        UserWord.times_shown > 0,
        _accuracy_below(STRUGGLING_THRESHOLD),
        _cooled_down(),
        _due_condition(),
    )
    return await _pick_one(session, _exclude(_review_scoped(query, user, level), exclude_ids))


def _unseen_query(user_id: int, pair: LanguagePair, exclude_ids: list[int],
                  user: Optional[User], level: Optional[CEFRLevel]):
    """Слова, которых человек на этом языке ещё не видел (NOT EXISTS)."""
    seen = (
        select(UserWord.word_id)
        .where(
            UserWord.user_id == user_id,
            UserWord.learning_lang == pair.learning,
            UserWord.word_id == Word.id,
        )
        .exists()
    )
    return _exclude(_scoped(_usable_words(pair).where(~seen), user, level), exclude_ids)


def _easy(query, pair: LanguagePair):
    """Лёгкие: знаменательные, однословные, короткие (первый урок)."""
    first = func.split_part(word_column(pair.learning), ",", 1)
    return query.where(
        Word.pos.in_(EASY_POS),
        ~func.btrim(first).like("% %"),
        func.length(func.btrim(first)) <= EASY_MAX_LETTERS,
    )


async def easy_new_words(session: AsyncSession, user: User, pair: LanguagePair,
                         exclude_ids: list[int], limit: int = EASY_POOL) -> list[Word]:
    """
    Новые лёгкие слова, самые частые первыми, — список, а не одно.

    Нужен первому уроку (`first_lesson`): похожее на родное слово ищется
    перебором пула, а доске на три пары нужно три слова сразу.
    """
    query = _easy(_unseen_query(user.id, pair, exclude_ids, user, user.level), pair)
    rows = await session.execute(
        query.outerjoin(
            WordFrequency,
            and_(WordFrequency.word_id == Word.id, WordFrequency.lang == pair.learning),
        )
        .order_by((WordFrequency.zipf - _function_word_penalty()).desc().nulls_last(), Word.id)
        .limit(limit)
    )
    return list(rows.scalars().all())


async def get_new_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> Optional[Word]:
    """
    Слово, которое пользователь на этом языке ещё не видел.

    NOT EXISTS вместо прежнего NOT IN со списком всех виденных id: у активного
    пользователя это тысячи идентификаторов, гонявшихся в каждом из 25 запросов.
    """
    query = _unseen_query(user_id, pair, exclude_ids, user, level)

    # ПЕРВЫЙ УРОК — САМЫЕ ЛЁГКИЕ: частые, однословные, знаменательные.
    # «mieć na myśli» первым словом (прод 15.10) — ровно то, чего не надо
    categories = categories_for(getattr(user, "learning_goal", None))
    if in_first_lesson(user):
        easy = _easy(query, pair)
        # И тема, если человек её назвал: лёгкие слова — из неё же
        tries = ([easy.where(Word.category.in_(categories))] if categories else []) + [easy]
        for candidates in tries:
            picked = await _pick_common(session, candidates, pair.learning, pool=EASY_POOL)
            if picked is not None:
                return picked

    # СЛОВА ТЕМЫ ВПЕРЁД, ЕСЛИ ЧЕЛОВЕК НАЗВАЛ ЦЕЛЬ.
    #
    # Подмешивается только в НОВЫЕ слова, и это важно: повторение и трудные
    # слова темой не ограничиваются — иначе выученное в стороне от темы
    # перестало бы возвращаться и забылось.
    #
    # Тема не отменяет уровень, а стоит поверх него. Переключить режим на
    # «по категории» было бы дешевле, но тот не смотрит на уровень вовсе, и
    # новичок получал бы C1 вперемешку с A1.
    #
    # Кончились слова темы — берём любые. Пустой круг хуже нетематического,
    # и запас этот не теоретический: в «Wirtschaft» слов уровня A1 всего два.
    if categories:
        themed = await _pick_common(
            session, query.where(Word.category.in_(categories)), pair.learning
        )
        if themed is not None:
            return themed

    return await _pick_common(session, query, pair.learning)


async def get_review_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> Optional[Word]:
    query = _progress_join(_usable_words(pair), user_id, pair).where(
        UserWord.learned.is_(False),
        UserWord.times_shown > 0,
        (UserWord.times_correct * 100.0 / UserWord.times_shown) >= STRUGGLING_THRESHOLD,
        _accuracy_below(REVIEW_THRESHOLD),
        _cooled_down(),
    )
    return await _pick_one(session, _exclude(_review_scoped(query, user, level), exclude_ids))


async def get_learned_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> Optional[Word]:
    query = _progress_join(_usable_words(pair), user_id, pair).where(
        UserWord.learned.is_(True),
        UserWord.times_shown >= MIN_ATTEMPTS_FOR_LEARNED,
        (UserWord.times_correct * 100.0 / UserWord.times_shown) >= LEARNED_SUCCESS_RATE,
    )
    return await _pick_one(session, _exclude(_review_scoped(query, user, level), exclude_ids))


async def get_any_word(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> Optional[Word]:
    query = _usable_words(pair)
    return await _pick_one(session, _exclude(_scoped(query, user, level), exclude_ids))


async def get_difficult_word(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
) -> Optional[Word]:
    """Слово из личного списка сложных (режим DIFFICULT)."""
    query = _difficult_query(user_id, pair)
    return await _pick_one(session, _exclude(query, exclude_ids))


def _difficult_conditions() -> tuple:
    """Что делает слово «сложным» — одно условие для подбора, счёта и доски."""
    return (
        UserWord.learned.is_(False),
        UserWord.times_shown >= 2,
        _accuracy_below(STRUGGLING_THRESHOLD),
        _cooled_down(),
    )


def _difficult_query(user_id: int, pair: LanguagePair):
    return _progress_join(_usable_words(pair), user_id, pair).where(
        *_difficult_conditions()
    )


async def count_difficult_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
) -> int:
    """
    Сколько сложных слов можно спросить ПРЯМО СЕЙЧАС.

    ТЕМ ЖЕ ЗАПРОСОМ, ЧТО ПОДБОР (`_difficult_query`). Прежде счёт не знал
    ни часовой паузы, ни годности слова для викторины, а подбор знал, и
    длина круга назначалась по счёту: шесть сложных, три из них отвечены
    десять минут назад — круг из шести обрывался на четвёртом вопросе
    «Не удалось подготовить следующий вопрос», без итога и баллов.
    Проверено исполнением. Так выходило всякий раз, когда после круга с
    ошибками человек сразу открывал «сложные»: промахи только что получили
    свежий показ.
    """
    query = select(func.count()).select_from(
        _difficult_query(user_id, pair).subquery()
    )
    result = await session.execute(query)
    return int(result.scalar() or 0)


# ============================================================================
# ДИСТРАКТОРЫ И СБОРКА ВАРИАНТОВ
# ============================================================================

def _option_variants(word: Word, lang: str) -> frozenset[str]:
    """
    Все значения варианта ответа.

    Сравнение идёт по каждому значению отдельно, а не по строке целиком:
    перевод «сразу, одинаковый» конфликтует и со «сразу», и с «одинаковый».
    Иначе дистрактор мог бы оказаться таким же верным ответом, как правильный.
    """
    return meaning_variants(word_text(word, lang), lang)


async def get_distractors(
    correct_word: Word,
    session: AsyncSession,
    pair: LanguagePair,
    user: Optional[User] = None,
    count: int = OPTIONS_TOTAL - 1,
) -> list[Word]:
    """
    Неправильные варианты: та же часть речи, различающийся текст ответа.

    Раньше дистракторы фильтровались только по части речи и артиклю, а текст
    вариантов не проверялся. Поэтому вопрос мог содержать два одинаковых
    варианта — например die / der / den / dem все показываются как «the»,
    и правильный выбрать было невозможно. Теперь варианты гарантированно
    различаются по тексту на языке ответа.

    Подбор идёт в три захода с ослаблением условий, чтобы редкие части речи
    не оставались без вариантов.
    """
    answer_lang = pair.answer_lang
    taken: set[str] = set(_option_variants(correct_word, answer_lang))
    # ЗНАЧЕНИЯ НА ЯЗЫКЕ ПОДСКАЗКИ ТОЖЕ НЕ ДОЛЖНЫ СОВПАДАТЬ. В «Вспоминаю»
    # подсказка — значение на родном языке, а варианты — слова изучаемого,
    # и сверка шла только по ним. Слова разные (auf, an, für), а значение у
    # них общее («на»), — и вопрос «На» выходил с двумя верными ответами:
    # 13 вопросов из 1620 по словам с общим значением. В прямых играх это
    # условие отсекает дубли одного и того же слова.
    prompt_meanings = _option_variants(correct_word, pair.prompt_lang)
    picked: list[Word] = []
    excluded_ids = [correct_word.id]

    base = _usable_words(pair)

    # 1. Та же часть речи и тот же уровень (в режимах по категории и по всей
    # базе уровень не ограничиваем).
    #
    # УРОВЕНЬ — В ИЗУЧАЕМОМ ЯЗЫКЕ (`level_expr`), а не немецкий `Word.level`:
    # у учащего английский A1 все 60 вариантов из 60 приходили уровня C1
    # (аудит подбора 15.10) — та же ошибка, что была с подбором слов.
    same_level = not (user and user.quiz_mode in (QuizMode.CATEGORY, QuizMode.ALL_WORDS))
    strict = base.where(Word.pos == correct_word.pos)
    if same_level:
        own_level = await level_of(session, correct_word, pair.learning)
        strict = strict.where(level_expr(pair.learning) == own_level)

    # АРТИКЛЬ. Когда варианты — слова С АРТИКЛЕМ («Вспоминаю»: ответ на
    # изучаемом немецком), артикль у всех вариантов ТОТ ЖЕ, что у верного.
    # Прежде требовался ИНОЙ — и артикль верного ответа всегда был
    # единственным среди четырёх: стратегия «бери непохожий артикль»
    # угадывала 63–65% вместо 25% (аудит подбора 15.10). Когда варианты —
    # значения на родном языке, артикль не виден, и прежнее условие
    # безвредно: оно лишь разводит варианты.
    noun = correct_word.pos == PartOfSpeech.NOUN and correct_word.article
    article_shown = bool(noun) and get_language(answer_lang).uses_article
    same_article = []
    if article_shown:
        strict = strict.where(Word.article == correct_word.article)
        # 1б. Та же часть речи и артикль, любой уровень — прежде чем
        # ослабить артикль
        same_article = [base.where(Word.pos == correct_word.pos,
                                   Word.article == correct_word.article)]
    elif noun:
        strict = strict.where(
            or_(Word.article.is_(None), Word.article != correct_word.article)
        )

    # 2. Та же часть речи, любой уровень и артикль
    by_pos = base.where(Word.pos == correct_word.pos)

    # 3. Любое слово — лишь бы вариантов было четыре
    anything = base

    def take(candidate: Word) -> bool:
        nonlocal taken
        variants = _option_variants(candidate, answer_lang)
        # Пересечение хотя бы по одному значению делает вариант
        # неотличимо верным — такой дистрактор не годится
        if not variants or variants & taken:
            return False
        if prompt_meanings & _option_variants(candidate, pair.prompt_lang):
            return False
        taken |= variants
        picked.append(candidate)
        excluded_ids.append(candidate.id)
        return True

    # 0. ЛОВУШКИ — только знакомому слову и не больше двух (`traps`): с чем
    # путают люди, похожие на вид, из той же темы. Новое — без них
    from app.services import traps

    if count > 1 and await traps.is_familiar(session, user, correct_word, pair):
        trap_base = base
        if article_shown:
            trap_base = base.where(Word.article == correct_word.article)
        for candidate in await traps.trap_candidates(session, trap_base, correct_word, pair):
            if len(picked) >= min(traps.TRAPS_MAX, count - 1):
                break
            take(candidate)

    for stage in (strict, *same_article, by_pos, anything):
        if len(picked) >= count:
            break

        candidates = await session.execute(
            _exclude(stage, excluded_ids).order_by(func.random()).limit(DISTRACTOR_CANDIDATES)
        )
        for candidate in candidates.scalars():
            if take(candidate) and len(picked) >= count:
                break

    return picked


def build_options(
    correct_word: Word,
    distractors: list[Word],
    pair: LanguagePair,
) -> tuple[list[tuple[int, str]], int]:
    """
    Перемешанные варианты ответа и индекс правильного.

    Текст берётся на языке ответа: при прямом направлении это язык значения,
    при обратном — изучаемый язык.
    """
    answer_lang = pair.answer_lang

    # На кнопке — подпись с бюджетом по длине, а не весь перевод: после
    # правки многозначности он доходит до 133 символов и разносит карточку.
    # Полный набор значений виден в разборе сразу после ответа.
    options = [(correct_word.id, option_label(correct_word, answer_lang))]
    for d in distractors:
        options.append((d.id, option_label(d, answer_lang)))

    random.shuffle(options)
    correct_index = next(i for i, (wid, _) in enumerate(options) if wid == correct_word.id)
    return options, correct_index


# Сколько раз пробовать подобрать слово с НОВЫМ значением, прежде чем
# смириться. Пять: столкновение значений редкое (нужно, чтобы двойник
# попал в тот же круг из пятнадцати), а каждая попытка — это запрос к базе.
MEANING_RETRIES = 5


def _meaning_key(word: Word, lang: str) -> str:
    """Главное значение слова, приведённое к сравнимому виду."""
    return (main_meaning(word, lang) or "").strip().lower()


async def _meanings_asked(
    session: AsyncSession, word_ids: list[int], lang: str
) -> set[str]:
    """
    Какие значения уже спрашивали в этом круге.

    Берётся из САМИХ слов по их номерам, а не из переданного списка
    значений: номера у круга уже есть (`used_word_ids`), и второй список
    пришлось бы вести рядом — он бы и разошёлся.
    """
    if not word_ids:
        return set()
    rows = (await session.execute(
        select(Word).where(Word.id.in_(word_ids))
    )).scalars().all()
    return {k for k in (_meaning_key(w, lang) for w in rows) if k}


# DER / DIE / DAS (владелец, 29.10.2026: тренажёр должен быть труднее; артикль
# — главная боль немецкого). Карточка «Читаю» знакомого существительного
# иногда спрашивает не значение, а артикль: значение человек уже показал, а
# род слова в варианты обычной карточки не входит вовсе — его можно годами
# угадывать мимо. Только немецкий: из десяти языков артикль, меняющий слово,
# только у него (у it/es/fr род виден по самому артиклю в значении).
ARTICLES = ("der", "die", "das")
ARTICLE_SHARE = 0.35


async def wants_article(session: AsyncSession, user: Optional[User], word: Word,
                        pair: LanguagePair, channel: Optional[QuizChannel]) -> bool:
    """Спросить ли у этой карточки артикль вместо значения."""
    if channel is not QuizChannel.TEXT or pair.learning != "de" or user is None:
        return False
    if word.pos != PartOfSpeech.NOUN or word.article not in ARTICLES:
        return False
    if in_first_lesson(user):
        return False
    from app.services import traps

    if not await traps.is_familiar(session, user, word, pair):
        return False
    return random.random() < ARTICLE_SHARE


# ОТВЕТ ВВОДОМ (владелец, 29.10.2026). «Вспоминаю» выученного слова иногда
# просит написать слово самому: из четырёх вариантов знакомое узнаётся, а не
# вспоминается, и «выучено» не значило бы «могу сказать». Только выученное:
# писать слово, которое ещё учишь, — не тренировка, а угадывание по буквам.
# Засчитывается как «Вспоминаю» — схема учёта и баллов та же.
TYPED_SHARE = 0.5


async def wants_typed(session: AsyncSession, user: Optional[User], word: Word,
                      pair: LanguagePair, channel: Optional[QuizChannel]) -> bool:
    """Спросить ли это слово вводом вместо вариантов."""
    if channel is not QuizChannel.REVERSE or user is None or in_first_lesson(user):
        return False
    learned = (await session.execute(
        select(UserWord.learned).where(
            UserWord.user_id == user.id, UserWord.word_id == word.id,
            UserWord.learning_lang == pair.learning,
        )
    )).scalar()
    if not learned:
        return False
    return random.random() < TYPED_SHARE


async def generate_question(
    session: AsyncSession,
    user: User,
    exclude_ids: Optional[list[int]] = None,
    pair: Optional[LanguagePair] = None,
    recent_channels: Optional[list[str]] = None,
    channel: Optional[QuizChannel] = None,
    prefer_channel: Optional[QuizChannel] = None,
    round_length: Optional[int] = None,
    question_number: Optional[int] = None,
) -> Optional[dict]:
    """
    Вопрос викторины: слово, варианты ответа, индекс правильного, канал.

    КАНАЛ ВЫБИРАЕТСЯ ЗДЕСЬ, ПОСЛЕ СЛОВА, а не снаружи до него. Иначе и быть
    не может: правило допуска к слуху смотрит на прогресс по КОНКРЕТНОМУ
    слову, а какое слово выпадет, решает SRS.

    `recent_channels` — чем задавались предыдущие вопросы занятия; нужно
    только чтобы не ставить три одинаковых подряд.

    `channel` НАВЯЗЫВАЕТ канал, минуя правило допуска. Два применения:
    прямой вход «только слух» с домашнего экрана и приёмка
    `verify_quiz_channels`, которой иначе нечего было бы проверять — у
    подопытного пользователя нет прогресса, и обычное правило всегда
    давало бы текст. Первая редакция приёмки на этом и попалась: она
    отрапортовала «все игры собираются верно», не собрав НИ ОДНОГО вопроса
    на слух.

    `prefer_channel` — то же желание, но БЕЗ обхода порога: слово, до канала
    не доросшее, придёт текстом. Этим и пользуется домашний экран, где
    кнопки 🔤 🎧 🎤 запускают занятие одним каналом. Жёсткий `channel`
    домашнему экрану не годится: новичок, ткнувший в «🎧», получил бы
    пятнадцать вопросов о словах, которых ни разу не видел.

    `round_length` и `question_number` — длина ЭТОГО круга и номер вопроса
    в нём (с единицы). Круг передаёт их сам: в «сложных» круг короче
    настройки, а после доски слов задано на четыре больше, чем вопросов, и
    вывести номер из `exclude_ids` нельзя. Не переданы — берутся настройка
    и число заданных слов, как прежде.

    Возвращает None, если подходящих слов не осталось.
    """
    exclude_ids = exclude_ids or []
    pair = pair or pair_from_user(user)
    length = round_length or user.quiz_word_count or DEFAULT_ROUND_LENGTH
    place = (question_number - 1) if question_number else len(exclude_ids)
    # ПЕРВОЕ ЗАНЯТИЕ — ЗНАКОМСТВО С УРОВНЕМ (29.10, `first_lesson`): только
    # карточки, на каждом месте новое слово своей ступени A1…B2
    placement = channel is None and in_first_lesson(user)
    if placement:
        channel = QuizChannel.TEXT
        prefer_channel = None

    # ЗНАЧЕНИЯ, УЖЕ СПРОШЕННЫЕ В ЭТОМ КРУГЕ, — чтобы не спросить второе
    # слово с тем же переводом.
    #
    # Находка владельца: «отметил 2 слова как ошибка перевода. В 1 ошибки
    # было 2 раза слово шептать, но разное значение на немецком. Бред». Он
    # прав: «шептать» — это и `flüstern`, и `raunen`, и в разборе круга
    # одно и то же русское слово стояло ответом к двум разным немецким.
    #
    # Это не редкость, это норма словаря: у 4 144 канонических слов из
    # 12 376 (33%) главное значение совпадает с чьим-то ещё. «Отвратительный»
    # стоит за десятью словами. В словаре так и должно быть, а в ОДНОМ
    # КРУГЕ — нет: человек видит повтор и считает его ошибкой. В пятой игре
    # (спрашиваем значением) это прямо ломает вопрос: правильных ответов
    # оказывается два.
    taken_meanings = await _meanings_asked(session, exclude_ids, pair.native)

    correct_word = None
    skipped: list[int] = []

    preset: Optional[Word] = None
    if placement:
        from app.services import first_lesson

        preset = await first_lesson.placement_word(
            session, user, pair, first_lesson.placement_level(place + 1),
            exclude_ids, taken_meanings,
        )
        if preset is not None:
            correct_word = preset
    # Попыток немного: столкновение редкое, а круг важнее чистоты. Не нашли
    # за пять подборов — берём как есть: повтор значения неприятен, а
    # оборванный круг хуже.
    # Вход одной игрой: сперва слово, ДОРОСШЕЕ до неё (`get_ready_for`)
    wanted = (
        prefer_channel
        if channel is None and prefer_channel is not None
        and prefer_channel is not QuizChannel.TEXT
        and prefer_channel in enabled_channels(user)
        else None
    )

    # Обычный круг: место отработки отдаётся игре, которой было меньше всего
    rotation = (
        _rotation(user, exclude_ids, recent_channels,
                  position=place, round_length=length)
        if wanted is None and channel is None
        and user.quiz_mode != QuizMode.DIFFICULT
        else []
    )
    rotated: Optional[QuizChannel] = None

    by_wanted = False
    for _ in range(0 if preset is not None else MEANING_RETRIES):
        candidate = None
        rotated = None
        if wanted is not None:
            candidate = await get_ready_for(
                wanted, user.id, session, pair, exclude_ids + skipped, user=user,
            )
        by_wanted = candidate is not None
        for game in rotation:
            candidate = await get_ready_for(
                game, user.id, session, pair, exclude_ids + skipped,
                user=user, gap=PRACTICE_GAP,
            )
            if candidate is not None:
                rotated = game
                break
        if candidate is None and user.quiz_mode == QuizMode.DIFFICULT:
            candidate = await get_difficult_word(
                user.id, session, pair, exclude_ids + skipped
            )
        elif candidate is None:
            candidate = await select_word_by_priority(
                user_id=user.id,
                session=session,
                pair=pair,
                exclude_ids=exclude_ids + skipped,
                user=user,
                # Длина круга и место нужны подбору, чтобы разложить новые
                # слова по месту. Длина — та же, по которой круг и строится;
                # расходиться им нельзя
                round_length=length,
                position=place,
            )
        if candidate is None:
            break
        correct_word = candidate
        meaning = _meaning_key(candidate, pair.native)
        if not meaning or meaning not in taken_meanings:
            break
        # Значение уже спрашивали — пробуем другое слово
        skipped.append(candidate.id)
        correct_word = None

    if correct_word is None and skipped:
        # Все подобранные столкнулись по значению: берём первое из них —
        # вопрос лучше, чем его отсутствие
        correct_word = await session.get(Word, skipped[0])
        rotated = None
        by_wanted = False

    if not correct_word:
        return None

    # Слово подобрано ПОД игру — ею и спрашиваем
    if channel is None and rotated is not None:
        channel = rotated

    # Фраза общей базы (`_fresh_build`) взята ТОЛЬКО ради сборки: правило
    # допуска смотрит на прогресс слова, а у такого слова его нет, и оно
    # пришло бы карточкой — новым словом посреди «Собираю»
    if (channel is None and wanted is QuizChannel.BUILD and by_wanted
            and not await _started(session, user.id, correct_word.id, pair)):
        channel = QuizChannel.BUILD

    if channel is None:
        channel = await pick_channel(
            session, user, correct_word, pair.learning, recent=recent_channels,
            prefer=prefer_channel, round_length=length, position=place + 1,
        )

    # НАПРАВЛЕНИЕ СЛЕДУЕТ ЗА КАНАЛОМ, и дальше в сборке участвует только
    # оно. Пятая игра — припоминание — спрашивает значением и ждёт слова
    # изучаемого языка, то есть её пара перевёрнута; остальные каналы идут
    # в прямую сторону. Правило одно на весь проект (`pair_for_channel`),
    # потому что ту же пару спрашивают показ карточки и разбор ответа:
    # разойдись они — задание окажется на одном языке, а варианты на другом.
    pair = pair_for_channel(pair, channel)

    # 🧱 СБОРКА: вариантов нет, есть кнопки-слова. Пример не годится (меньше
    # трёх слов, больше десяти, нет перевода) — ОТКАТ на карточку, ровно
    # как у слуха без созвучных соседей ниже: слово не теряется, игра
    # просто другая. Подбор под сборку (`get_ready_for`, `pick_channel`)
    # негодное слово и так не выбирает; откат — для навязанного канала и
    # для данных, поменявшихся между подбором и сборкой.
    if channel is QuizChannel.BUILD:
        puzzle = await build_service.make_puzzle(
            session, correct_word, pair, learner_level=getattr(user, "level", None))
        if puzzle is not None:
            return {
                "correct_word": correct_word,
                # Кнопки — те же «варианты»: номер кнопки и её слово
                "options": list(enumerate(puzzle.tiles)),
                "correct_answer_index": None,
                "pair": pair,
                "channel": channel,
                "build": puzzle,
            }
        channel = QuizChannel.TEXT
        pair = pair_for_channel(pair, channel)

    # Канал решает и ЧТО подставить в варианты, и НА КАКОМ они языке.
    #
    # На слух варианты обязаны быть созвучны: смысл не звучит, звучит форма.
    # Поставь рядом с «Verspätung» слова «Haus», «gehen» и «blau» — и
    # слушать не придётся, ответ виден по одной длине.
    # Ответ вводом вместо четырёх вариантов — выученному слову в «Вспоминаю»
    # (`wants_typed`, `typed_answer`): вариантов нет, слово пишут сами
    if await wants_typed(session, user, correct_word, pair, channel):
        return {
            "correct_word": correct_word,
            "options": [],
            "correct_answer_index": -1,
            "pair": pair,
            "channel": channel,
            "typed": True,
        }

    # der / die / das вместо обычной карточки — знакомому существительному
    # (`wants_article`): у артикля три варианта, значения не нужны
    if await wants_article(session, user, correct_word, pair, channel):
        return {
            "correct_word": correct_word,
            "options": [(article, article) for article in ARTICLES],
            "correct_answer_index": ARTICLES.index(correct_word.article),
            "pair": pair,
            "channel": channel,
            "article": True,
        }

    if channel is QuizChannel.AUDIO:
        distractors = await get_soundalike_distractors(
            correct_word, session, pair, user=user
        )
        builder = build_audio_options
    else:
        distractors = await get_distractors(correct_word, session, pair, user=user)
        builder = build_options

    # Меньше четырёх различимых вариантов — вопрос был бы некорректным.
    #
    # На слух это случается чаще: созвучных соседей у редкого слова может не
    # найтись. Вместо того чтобы терять слово целиком, откатываемся на
    # текстовый вопрос — он корректен всегда.
    if len(distractors) < OPTIONS_TOTAL - 1:
        if channel is not QuizChannel.AUDIO:
            return None
        channel = QuizChannel.TEXT
        # Пара пересчитывается вместе с каналом: иначе откат со слуха на
        # текст оставил бы направление слуха, а оно у них совпадает лишь
        # пока реверса нет в составе
        pair = pair_for_channel(pair, channel)
        distractors = await get_distractors(correct_word, session, pair, user=user)
        builder = build_options
        if len(distractors) < OPTIONS_TOTAL - 1:
            return None

    options, correct_index = builder(correct_word, distractors, pair)

    return {
        "correct_word": correct_word,
        "options": options,
        "correct_answer_index": correct_index,
        "pair": pair,
        "channel": channel,
    }


# ============================================================================
# ПРОГРЕСС
# ============================================================================

async def update_word_progress(
    user_id: int,
    word_id: int,
    is_correct: bool,
    session: AsyncSession,
    learning_lang: str,
    channel: QuizChannel = QuizChannel.TEXT,
    advance_schedule: bool = True,
) -> None:
    """
    Учесть ответ. Прогресс ведётся отдельно по каждому изучаемому языку:
    выученное «das Haus» не делает выученным «house».

    КАНАЛ учитывается дважды: в общий итог и в свой счётчик. Текстовый канал
    своего счётчика не имеет — он выводится вычитанием, см. модель UserWord.

    Значение по умолчанию TEXT не ради удобства, а ради правды о прошлом: все
    29 742 показа, накопленные до появления каналов, были текстовыми, других
    вопросов в боте не было.

    СЕРИЯ И «ВЫУЧЕНО» ОСТАЮТСЯ ОБЩИМИ, И ЭТО НЕ НЕДОСМОТР. Канал меняется от
    показа к показу, а слово у человека одно: он либо помнит его, либо нет.
    Больше того, три верных ответа РАЗНЫМИ каналами — свидетельство более
    сильное, чем три одинаковыми, поэтому дробить серию по каналам значило бы
    ослабить её.
    """
    now = utcnow()

    word = await session.get(Word, word_id)
    if word:
        # Популярность слова — общая для всех языков
        word.times_shown += 1
        if is_correct:
            word.times_correct += 1

    result = await session.execute(
        select(UserWord).where(
            UserWord.user_id == user_id,
            UserWord.word_id == word_id,
            UserWord.learning_lang == learning_lang,
        )
    )
    user_word = result.scalar_one_or_none()

    if not user_word:
        user_word = UserWord(
            user_id=user_id,
            word_id=word_id,
            learning_lang=learning_lang,
            # Засчитанное по попыткам серию не начинает (см. ниже, «досрочно»).
            # С ПЕРВОГО РАЗА ВЕРНО — сразу на ступень выше (патч 2.1)
            correct_streak=(FIRST_SIGHT_STREAK if is_correct and advance_schedule else 0),
            times_shown=1,
            times_correct=1 if is_correct else 0,
            last_seen_at=now,
            learned=False,
        )
        _count_channel(user_word, channel, is_correct)
        session.add(user_word)
        await session.commit()
        return

    # ДОСРОЧНЫЙ ВЕРНЫЙ ОТВЕТ НЕ ДВИГАЕТ РАСПИСАНИЕ. Слово, которому ещё не
    # пора, приходит отработкой — другой игрой в тот же день
    # (`get_practice_words`). Засчитай такой ответ в серию — и три игры за
    # вечер превратили бы вчерашнее знакомство в «повторить через неделю»,
    # хотя ни одного дня между ответами не прошло. Ответ учитывается в
    # показах, верных и в счётчике игры (за него и баллы), но серия и
    # отметка последнего показа — якорь срока — остаются прежними. Промах
    # досрочным не бывает: забыл — значит забыл, и срок обнуляется.
    #
    # Так же учитывается ответ, засчитанный ПО ПОПЫТКАМ (`advance_schedule=
    # False`): третья запись «Говорю» верна и с баллами — решение
    # владельца, — но слово человек не произнёс, и сдвинуть ему срок
    # значило бы солгать расписанию. Проверено исполнением: три записи
    # «Katze» на чужое слово давали серию 1 → 2.
    early = is_correct and (not advance_schedule or not _is_due(user_word, now))

    user_word.times_shown += 1
    if not early:
        user_word.last_seen_at = now
    _count_channel(user_word, channel, is_correct)

    # ПРОМАХ ОБНУЛЯЕТ СЕРИЮ, а с ней и срок возврата.
    #
    # Прежде промах лишь откусывал от серии: больше трёх — минус два, но не
    # ниже двух; иначе минус один. Пока подбор смотрел на точность, это было
    # безобидно. С тех пор как серия задаёт СРОК (`REVIEW_SCHEDULE`), правило
    # стало прятать ошибки: слово с серией 7 после промаха получало серию 5 и
    # возвращалось через ШЕСТЬДЕСЯТ ДНЕЙ — проверено исполнением: через 1, 7,
    # 30 и 59 дней после промаха оно не было ни просроченным, ни «трудным».
    # Серия 3 после промаха давала 2, то есть три дня. Человек только что
    # показал, что слово забыл, — именно его и надо вернуть первым.
    #
    # Ноль — это срок «час» (`REVIEW_SCHEDULE[0]`), то есть следующий круг
    # после паузы; немедленный повтор и так делает кнопка «повторить
    # ошибки». «Выучено» при этом снимается: оно определено как три верных
    # ПОДРЯД, а подряд больше нет.
    if is_correct:
        if not early:
            user_word.correct_streak += 1
        user_word.times_correct += 1
    else:
        user_word.correct_streak = 0

    # ДАТА ПЕРЕХОДА В «ВЫУЧЕНО» — по ней месячный балл платит +3 за слово,
    # один раз. Ставится только на переходе False → True: повторение уже
    # выученного слова дату не двигает (иначе оплата повторилась бы в
    # следующем месяце, как было при счёте по last_seen_at). Промах снимает
    # отметку — и дату: выученное заново оплачивается заново, это честно,
    # слово было забыто и выучено ещё раз
    was_learned = bool(user_word.learned)
    user_word.learned = _is_learned(user_word, now)
    if user_word.learned and not was_learned:
        user_word.learned_at = now
    elif not user_word.learned:
        user_word.learned_at = None
    await session.commit()


# ПЕРЕПУТАЛ — ЗНАЧИТ, НЕ ЗНАЕШЬ ОБА (владелец, 29.10.2026: «если неугадал —
# значит слово, которое выбрал, не знает; 1 раз ладно, мисклик, но если
# несколько — не знает»). Промах по заданному слову обнуляет его серию и так;
# здесь — слово, которое человек ВЫБРАЛ вместо верного.
CONFUSIONS_TO_FORGET = 2
CONFUSION_WINDOW = timedelta(days=30)


async def note_confusion(session: AsyncSession, user_id: int, chosen_word_id: Optional[int],
                         correct_word_id: int, learning_lang: str) -> bool:
    """
    Учесть, что человек выбрал `chosen_word_id` вместо верного слова.

    Первый раз — промах, ничего не меняется. Второй раз за
    `CONFUSION_WINDOW` — слово выбранного варианта он не знает: серия
    обнуляется, «выучено» снимается, и слово возвращается первым, как после
    собственного промаха (`update_word_progress`). Слово, которого человек не
    начинал, не трогается: о нём ответ ничего не говорит.

    Строка вопроса с `chosen_word_id` уже записана к этому моменту и входит
    в счёт. True — слово снято.
    """
    if not chosen_word_id or chosen_word_id == correct_word_id:
        return False
    user_word = (await session.execute(
        select(UserWord).where(
            UserWord.user_id == user_id,
            UserWord.word_id == chosen_word_id,
            UserWord.learning_lang == learning_lang,
        )
    )).scalar_one_or_none()
    if user_word is None:
        return False
    since = utcnow() - CONFUSION_WINDOW
    confusions = (await session.execute(
        select(func.count()).select_from(QuizQuestion)
        .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
        .where(
            QuizSession.user_id == user_id,
            QuizSession.learning_lang == learning_lang,
            QuizQuestion.chosen_word_id == chosen_word_id,
            QuizQuestion.word_id != chosen_word_id,
            QuizQuestion.is_correct.is_(False),
            QuizQuestion.answered_at >= since,
        )
    )).scalar() or 0
    if confusions < CONFUSIONS_TO_FORGET:
        return False
    if not user_word.correct_streak and not user_word.learned:
        return False
    user_word.correct_streak = 0
    user_word.learned = False
    user_word.learned_at = None
    from app.services import journal

    journal.note(session, user_id, "confused", "forget", word_id=chosen_word_id,
                 instead_of=correct_word_id, times=confusions)
    await session.commit()
    return True


def _count_channel(user_word: UserWord, channel: QuizChannel, is_correct: bool) -> None:
    """
    Засчитать показ своему каналу.

    Текстовый канал не упомянут нарочно: его счётчики выводятся из итога
    вычитанием, и ничего прибавлять к ним не надо. Если когда-нибудь здесь
    появится ветка для TEXT — значит кто-то завёл ему колонку, и вместе с
    ней завёл возможность расхождения с итогом.
    """
    # Везде `or 0`, и это не перестраховка. У ТОЛЬКО ЧТО созданного объекта
    # значения по умолчанию ещё не применены — они ставятся при вставке, а
    # сюда объект приходит до неё. Первый же ответ по новому слову падал с
    # «unsupported operand type(s) for +=: NoneType and int».
    #
    # Нашла это приёмка круга на первом же прогоне с включённой речью:
    # текстовые и слуховые ответы по новым словам в неё не попадали, потому
    # что новое слово на слух не спрашивают, а тексту счётчиков нет.
    #
    # Колонки — ПО ИМЕНИ КАНАЛА (`shown_<key>`, `correct_<key>`), а не
    # веткой на каждый: прежде здесь было три ветки, и канал без ветки
    # молча уходил бы в «текст» вычитанием.
    if channel not in counted_channels():
        return
    shown, correct = f"shown_{channel.key}", f"correct_{channel.key}"
    setattr(user_word, shown, (getattr(user_word, shown) or 0) + 1)
    if is_correct:
        setattr(user_word, correct, (getattr(user_word, correct) or 0) + 1)


def _is_due(user_word: UserWord, now: datetime) -> bool:
    """Пора ли слову по расписанию — то же правило, что `_due_condition`."""
    seen = user_word.last_seen_at
    if seen is None:
        return True
    streak = user_word.correct_streak or 0
    delay = REVIEW_SCHEDULE.get(streak)
    if delay is None:
        delay = REVIEW_SCHEDULE_TAIL if streak > max(REVIEW_SCHEDULE) else REVIEW_SCHEDULE[0]
    return seen <= now - delay


def _is_learned(user_word: UserWord, now: datetime) -> bool:
    """
    Слово выучено, если серия верных ответов достигла порога и знакомство
    произошло не сегодня. Прежняя версия отмечала «выучено» за три угадывания
    подряд, которые могли уложиться в одну сессию.
    """
    if user_word.correct_streak < MIN_ATTEMPTS_FOR_LEARNED:
        return False

    first_seen = user_word.created_at
    if first_seen is None:
        return True

    return (now - first_seen) >= timedelta(days=MIN_DAYS_BEFORE_LEARNED)


# ============================================================================
# СТАТИСТИКА ПРОГРЕССА
# ============================================================================

def _canonical_count_query(pair: LanguagePair):
    """Сколько всего слов доступно для изучения на этой паре языков."""
    return select(func.count()).select_from(_usable_words(pair).subquery())


async def get_user_progress_stats(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    level: Optional[CEFRLevel] = None,
    category: Optional[str] = None,
) -> dict:
    """
    Прогресс по изучаемому языку. Фильтры уровня и категории необязательны:
    без них считается вся доступная база.
    """
    def scoped(query):
        if level is not None:
            query = query.where(level_expr(pair.learning) == level)
        if category is not None:
            query = query.where(Word.category == category)
        return query

    total_q = select(func.count()).select_from(scoped(_usable_words(pair)).subquery())
    total_words = int((await session.execute(total_q)).scalar() or 0)

    seen_base = _progress_join(scoped(_usable_words(pair)), user_id, pair)

    seen_q = select(func.count()).select_from(seen_base.subquery())
    seen_words = int((await session.execute(seen_q)).scalar() or 0)

    learned_q = select(func.count()).select_from(
        seen_base.where(UserWord.learned.is_(True)).subquery()
    )
    learned_words = int((await session.execute(learned_q)).scalar() or 0)

    struggling_q = select(func.count()).select_from(
        seen_base.where(
            UserWord.learned.is_(False),
            UserWord.times_shown > 0,
            _accuracy_below(STRUGGLING_THRESHOLD),
        ).subquery()
    )
    struggling_words = int((await session.execute(struggling_q)).scalar() or 0)

    return {
        "total_words": total_words,
        "seen_words": seen_words,
        "learned_words": learned_words,
        "struggling_words": struggling_words,
        "new_words": max(0, total_words - seen_words),
    }


async def get_overall_progress(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
) -> dict:
    """Общий прогресс по всей доступной базе изучаемого языка."""
    stats = await get_user_progress_stats(user_id, session, pair)
    return {
        "total_words": stats["total_words"],
        "learned_words": stats["learned_words"],
    }


# ============================================================================
# ТРИ ШКАЛЫ: сколько слов освоено каждым каналом
# ============================================================================

# Сколько верных ответов этим каналом считать «узнаю слово этим способом».
#
# БЫЛО ТРИ, СТАЛО ОДИН, и это не ослабление требований, а исправление
# названия. Шкала на домашнем экране называется «узнаю на слух» — и должна
# значить именно узнавание, а не владение в совершенстве.
#
# Замер 13 октября 2026 показал цену порога в три: у 154 человек из 199 нет
# НИ ОДНОГО слова с тремя верными ответами вообще, а с тремя именно нужным
# каналом — тем более. Для 78% людей шкала не могла сдвинуться по
# построению: одно слово надо встретить четыре-пять раз, и каждый раз
# нужным каналом. Человек слушал, отвечал верно — и видел на шкале ноль.
#
# Довод «один верный ответ бывает угадыванием из четырёх» верен, но
# относится к ДРУГОЙ мере: строгая — это `learned` (три подряд плюс сутки),
# и она осталась нетронутой. Две меры лучше одной: шкала показывает
# знакомство и движется с первого круга, «выучено» показывает твёрдое
# знание и остаётся редким.
CHANNEL_MASTERY = 1


async def get_channel_progress(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    level: Optional[CEFRLevel] = None,
    category: Optional[str] = None,
) -> dict[str, int]:
    """
    Сколько слов человек узнаёт глазами, вспоминает, узнаёт на слух и
    произносит.

    Это и есть шкалы домашнего экрана. Самое полезное в них — не сами
    числа, а РАЗРЫВ между ними: «342 узнаю глазами, а произношу 64» говорит
    о человеке правду, которую он сам о себе не знает, и мотивирует сильнее
    любого бейджа.

    Шкала ПРИПОМИНАНИЯ появилась вместе с пятой игрой. Без неё бот не
    отличал бы «узнаю das Metall» от «вспомню, что металл — это das
    Metall», а это и есть та разница, ради которой игру заводили.

    Текстовая шкала считается вычитанием, ровно как в модели: отдельной
    колонки у неё нет, и разойтись с итогом она не может.

    СЧИТАЕТСЯ ПО ТОМУ ЖЕ НАБОРУ СЛОВ, ЧТО И ЗНАМЕНАТЕЛЬ ШКАЛЫ — отсюда и
    `pair` с фильтрами уровня и категории, те же, что у
    `get_user_progress_stats`. Первая редакция брала все ряды `UserWord` по
    изучаемому языку, а полоса рисовалась от числа слов текущего РЕЖИМА — и
    у всякого, кто сменил уровень или пару, числитель приходил из одного
    набора, а знаменатель из другого: 342 из 300, полоса за край. Это та же
    форма, что и семь прежних дефектов (`ROADMAP.md` §6): проверка смотрит
    на одно поле, а меняется соседнее.
    """
    own = counted_channels()
    text_correct = UserWord.times_correct - sum(
        (getattr(UserWord, f"correct_{c.key}") for c in own),
        start=literal_column("0"),
    )

    def scoped(query):
        if level is not None:
            query = query.where(level_expr(pair.learning) == level)
        if category is not None:
            query = query.where(Word.category == category)
        return query

    # Признаки освоения считаются во вложенном запросе, а итоги — снаружи:
    # соединение с `UserWord` даёт по ряду на слово, и агрегировать поверх
    # него надо отдельным уровнем, иначе фильтры счётчиков легли бы на
    # условия соединения.
    inner = (
        _progress_join(scoped(_usable_words(pair)), user_id, pair)
        .with_only_columns(
            (text_correct >= CHANNEL_MASTERY).label("text"),
            *(
                (getattr(UserWord, f"correct_{c.key}") >= CHANNEL_MASTERY).label(c.key)
                for c in own
            ),
            # Допуск — не то же, что освоение, и порог у него другой: слуху
            # довольно одного верного ответа, речи и сборке двух, а
            # освоением канала считается верный ответ ИМ САМИМ. Нужно для
            # прямого входа одной игрой: есть ли вообще что слушать, прежде
            # чем запускать занятие одним каналом.
            *(
                (UserWord.times_correct >= CHANNEL_UNLOCK[c]).label(f"ready_{c.key}")
                for c in own
            ),
        )
        .subquery()
    )

    # Ключи — ИМЕНА КАНАЛОВ (`text`, `reverse`, …, `build`) и `ready_<имя>`:
    # шкалы домашнего экрана берут их по тому же имени, и канал, добавленный
    # в перечисление, появляется в обоих местах сам
    names = ["text", *(c.key for c in own), *(f"ready_{c.key}" for c in own)]
    row = await session.execute(
        select(
            *(func.count().filter(inner.c[name]) for name in names),
            func.count(),
        ).select_from(inner)
    )
    values = row.one()
    out = {name: values[i] or 0 for i, name in enumerate(names)}
    out["touched"] = values[-1] or 0
    return out


# ============================================================================
# ВОПРОС НА СЛУХ: звучит слово изучаемого языка, выбрать что услышал
# ============================================================================

# Сколько первых букв общего начала делают дистрактор созвучным. Три —
# замерено на немецком: «Ver» объединяет Verspätung / Verspannung /
# Verpflegung, и этого хватает, чтобы различать пришлось именно слухом.
# Две буквы сводят слишком многое («an», «be»), четыре — почти ничего.
SOUNDALIKE_PREFIX = 3

# Сколько созвучных тянуть из базы, чтобы выбрать из них три. С большим
# запасом: отсев идёт уже в Python, по звучащему значению, и отбрасывает
# большинство — в ячейке нужное начало может стоять не первым вариантом.
SOUNDALIKE_CANDIDATES = 120


def _bare_meaning(word: Word, lang: str) -> str:
    """
    Звучащее значение БЕЗ артикля — то, по чему и считается созвучие.

    `main_meaning` для немецкого возвращает «der Krieg» вместе с артиклем, и
    первыми тремя буквами оказывается «der». Созвучными тогда признавались
    «der Gründer · der Flieder · der Köder» — общий у них ТОЛЬКО артикль,
    который стоит во всех четырёх вариантах и потому не различает ничего.

    Артикль берётся из самого ряда, а не из списка «der/die/das»: список
    кончился бы на первом же языке, где артиклей больше.
    """
    label = main_meaning(word, lang)
    article = (word.article or "").strip()
    if article and article != "-" and label.lower().startswith(article.lower() + " "):
        return label[len(article) + 1:]
    return label


def _prefix_len(label: str) -> int:
    """
    Сколько первых букв считать общим началом — с поправкой на короткие слова.

    Для «eigentlich» три буквы в самый раз. Для «Age» и «Way» они не находят
    ничего: трёхбуквенных слов с тем же началом в базе попросту нет, и вопрос
    сваливался в обычные дистракторы — «Age · Pill · Scum · Injection», где
    слушать не надо вовсе.

    Две буквы на коротком слове дают «Age → Agent, Agenda» и «Way → Wall,
    Wait» — ровно то, что на слух и путается.
    """
    return 2 if len(label) <= 4 else SOUNDALIKE_PREFIX


async def get_soundalike_distractors(
    correct_word: Word,
    session: AsyncSession,
    pair: LanguagePair,
    user: Optional[User] = None,
    count: int = OPTIONS_TOTAL - 1,
) -> list[Word]:
    """
    Дистракторы для вопроса НА СЛУХ: похожие по звучанию, а не по смыслу.

    ПОЧЕМУ ОБЫЧНЫЕ НЕ ГОДЯТСЯ. В текстовом вопросе дистрактор обязан быть
    близким по СМЫСЛУ — иначе правильный ответ виден без знания слова. На
    слух всё наоборот: смысл не звучит, звучит форма. Поставь рядом с
    «Verspätung» слова «Haus», «gehen» и «blau» — и слушать не придётся,
    ответ виден по одной длине.

    Упражнение на слух тем и ценно, что заставляет различать близкое:

        Verspätung · Verspannung · Verpflegung · Versöhnung

    Здесь выбор требует расслышать слово целиком, а не первый слог.

    КАК ИЩЕТСЯ СОЗВУЧНОЕ. По общему началу в изучаемом языке и по близкой
    длине. Это грубая мера — настоящая фонетическая близость требует
    транскрипции, которой в базе нет, — но она дешёвая и работает: в
    германских и славянских языках общее начало почти всегда означает общее
    звучание начала.

    СКОЛЬКО СОЗВУЧНЫХ НУЖНО, ЧТОБЫ ВОПРОС СОСТОЯЛСЯ. Хотя бы один. Если не
    нашлось ни одного — возвращается пустой список, и вызывающий код задаёт
    вопрос текстом.

    Это не придирчивость, а замер: приёмка `verify_quiz_channels` на 360
    вопросах нашла 35 (≈10%), где созвучных не было вовсе и варианты
    добирались обычными. Выходило, например, «лебедь · багажная лента ·
    халат · выход» — различить можно по длине, не вслушиваясь. Такой вопрос
    не сломан, но и слухом не является.

    Добор обычными дистракторами при этом остался: если созвучный ОДИН,
    два других берутся как придётся — одной настоящей путаницы достаточно,
    чтобы прослушать пришлось целиком.
    """
    learning_col = word_column(pair.learning)

    # МЕРИТЬ НАДО ТО, ЧТО УВИДИТ УЧЕНИК, А НЕ ЯЧЕЙКУ.
    #
    # Первая версия брала начало и длину у ВСЕЙ ячейки перевода, а на кнопку
    # ставится одно выбранное значение. Расхождение видно сразу:
    #
    #     ячейка en  «way of speaking, manner of expression, diction»
    #     на кнопке  «Manner of expression»
    #
    # Поиск по «way%» находил этот ряд, а ученик видел вариант, не имеющий с
    # «Way» ничего общего — то есть созвучие, ради которого всё и затевалось,
    # пропадало. Английское «Way» так получило в соседи «Kindergarten».
    #
    # Это шестой случай одной и той же ошибки: проверка смотрит на ЯЧЕЙКУ, а
    # код работает с ВЫБРАННЫМ ЗНАЧЕНИЕМ. Поэтому здесь запрос к базе —
    # только дешёвый предварительный отсев по ячейке, а решает сверка
    # показываемой подписи уже в Python.
    # Сравнивается ЗВУЧАЩЕЕ, то есть `main_meaning` — ровно тот текст, что
    # уходит в синтез. Не `option_label`: он добавляет немецкий артикль, и
    # первыми тремя буквами «die Art» оказывалось «die». Вопрос тогда давал
    # соседей «die Diele · dienen · diesmal» — созвучен артикль, а не слово.
    own_label = _bare_meaning(correct_word, pair.learning)
    head = own_label[:_prefix_len(own_label)]
    own_len = len(own_label)

    taken: set[str] = set(_option_variants(correct_word, pair.learning))
    picked: list[Word] = []
    excluded_ids = [correct_word.id]

    if head:
        query = (
            _usable_words(pair)
            .where(
                # предварительный отсев: ячейка СОДЕРЖИТ значение с таким
                # началом. Шире, чем нужно, — лишнее отсеется ниже
                func.lower(learning_col).like("%" + head.lower() + "%"),
            )
            .order_by(func.random())
            .limit(SOUNDALIKE_CANDIDATES)
        )
        candidates = await session.execute(_exclude(query, excluded_ids))
        for candidate in candidates.scalars():
            label = _bare_meaning(candidate, pair.learning)
            # Сверяем ЗВУЧАЩЕЕ значение, а не ячейку: созвучие должно быть у
            # того, что ученик услышит и увидит на кнопке
            if not fold(label).startswith(fold(head)):
                continue
            # Близкие по длине: разница больше трети делает ответ различимым
            # без вслушивания
            if abs(len(label) - own_len) > max(2, own_len // 3):
                continue
            variants = _option_variants(candidate, pair.learning)
            if not variants or variants & taken:
                continue
            taken |= variants
            picked.append(candidate)
            excluded_ids.append(candidate.id)
            if len(picked) >= count:
                break

    # Ни одного созвучного — вопроса на слух не выйдет
    if not picked:
        return []

    if len(picked) < count:
        # Добор обычными: вопрос станет легче, но останется вопросом
        extra = await get_distractors(
            correct_word, session, pair, user=user, count=count - len(picked)
        )
        for candidate in extra:
            if candidate.id in excluded_ids:
                continue
            variants = _option_variants(candidate, pair.learning)
            if not variants or variants & taken:
                continue
            taken |= variants
            picked.append(candidate)
            excluded_ids.append(candidate.id)

    return picked[:count]


def build_audio_options(
    correct_word: Word,
    distractors: list[Word],
    pair: LanguagePair,
) -> tuple[list[tuple[int, str]], int]:
    """
    Варианты для вопроса на слух — НА ИЗУЧАЕМОМ ЯЗЫКЕ, а не на языке значения.

    Требование владельца дословно: «должно озвучивать на том языке, котором
    ответ. Чтобы человек слушал условно немецкое слово и выбирал что он
    услышал, а не перевод».

    И это верно по сути. Если звучит немецкое слово, а в вариантах стоят
    русские переводы, упражнение проверяет ПОНИМАНИЕ — то же, что и обычная
    карточка, только вход другой. А вариант на том же языке проверяет связку
    «звук → написание», и она в чужом языке ломается первой: услышать
    «Verspätung» и опознать в нём именно это написание — отдельный навык,
    которого текстовая карточка не тренирует вовсе.
    """
    options = [(correct_word.id, option_label(correct_word, pair.learning))]
    for d in distractors:
        options.append((d.id, option_label(d, pair.learning)))

    random.shuffle(options)
    correct_index = next(i for i, (wid, _) in enumerate(options) if wid == correct_word.id)
    return options, correct_index


# ============================================================================
# СОСТАВ ЗАНЯТИЯ: каким каналом задать очередной вопрос
# ============================================================================

# Сколько верных ответов ГЛАЗАМИ открывают слово для вопроса на слух.
# Один: показа мало (можно было ткнуть мимо), а трёх много — к тому
# времени ученик перерос текстовый вопрос, и слух придёт слишком поздно.
AUDIO_UNLOCK_CORRECT = 1

# Сколько верных ответов открывают слово для ПРОИЗВОДСТВА — речи и сборки.
# Два: произвести труднее, чем узнать, и требовать этого от слова, которое
# узнано один раз, значит гарантировать промах. Одно число на обе игры —
# правило, а не две копии, которые однажды разойдутся.
PRODUCTION_UNLOCK_CORRECT = 2
BUILD_UNLOCK_CORRECT = 1

# Сколько верных ответов открывают слово для каждого канала.
#
# Порог растёт вместе с трудностью: прочитать можно сразу; узнать на слух —
# после одного успеха глазами, иначе человек угадывает звук слова, которого
# ни разу не видел; произнести — после двух, потому что производство
# труднее узнавания, и требовать его от едва знакомого слова значит
# гарантировать промах.
CHANNEL_UNLOCK = {
    QuizChannel.TEXT: 0,
    # Припоминание требует того же, что и слух: одного верного ответа
    # глазами. Нельзя вспомнить слово, которое ни разу не узнал, — вопрос
    # «металл по-немецки?» о слове, которого человек не видел, это не
    # упражнение, а гадание по четырём вариантам.
    QuizChannel.REVERSE: 1,
    QuizChannel.AUDIO: AUDIO_UNLOCK_CORRECT,
    QuizChannel.SPEECH: PRODUCTION_UNLOCK_CORRECT,
    # Сборка открывается после ОДНОГО верного. Владелец, 23.10: «разморозка
    # должна быть 1 игра, а не 2». Прежде порог был общий с речью (два), и
    # грамматика приходила поздно и по узкому кругу слов. Задание сборки —
    # перевод фразы на экране, слово уже узнано один раз
    QuizChannel.BUILD: BUILD_UNLOCK_CORRECT,
}


# Каналы, которым нужна озвучка. Перечислены, а не выведены из «всё, кроме
# текста»: пятая игра — припоминание — тоже не текст, но звука не требует,
# и прежнее «не текст, значит нужен звук» отняло бы её у всех, кто звук
# выключил.
NEEDS_AUDIO = (QuizChannel.AUDIO, QuizChannel.SPEECH)


# ============================================================================
# ДОЛИ ИГР В КРУГЕ: сколько какой игры человек встретит за занятие
# ============================================================================
#
# ДОЛЯ ОБРАТНО ПРОПОРЦИОНАЛЬНА ЦЕНЕ ОТВЕТА, и это не вкус, а единственное
# место, где трудность игр уже измерена и записана числом:
# `MonthlyStats.POINTS_*` (1 : 1 : 2 : 3). Чем дороже ответ, тем он труднее,
# и тем реже его стоит просить — иначе занятие превращается в экзамен.
#
# ЗАЧЕМ ЦЕЛЬ ВООБЩЕ. Прежде доли НИКТО не задавал: канал брался по кругу от
# предыдущего в порядке перечисления `QuizChannel`, и состав занятия
# оказывался побочным следствием порядка БУКВ. Замер (40 кругов на три
# профиля) показал, чего это стоило:
#
#   у продвинутого ритм выходил строго цикличным — t r a s t r a s, чистое
#   чередование в 21 круге из 40, хотя описание правила уверяло в обратном
#   («ритм ломается сам, случайности тут нет вовсе»);
#   речь приходила ТРИ раза за круг в 15 кругах из 40 — три записи голоса,
#   чего не решал никто;
#   последним вопросом круга речь оказывалась в 10 кругах из 40, то есть
#   самое трудное стояло ровно там, где человек уже видит итог.
#
# Доли считаются по ВКЛЮЧЁННЫМ каналам, а не по открытым для слова: иначе у
# новичка, где почти всё закрыто, цель по тексту была бы 100%, и первый же
# доросший до слуха вопрос пришёл бы текстом.
def channel_targets(channels: list[QuizChannel]) -> dict[QuizChannel, float]:
    """Какую долю круга должна занять каждая игра. Сумма — единица."""
    from app.database.models import MonthlyStats

    # Цена — из того же места, где её берёт месячный балл (`points_for`):
    # таблица здесь отстала бы от той при первой новой игре
    weight = {c: 1 / max(1, MonthlyStats.points_for(c)) for c in channels}
    total = sum(weight.values()) or 1
    return {c: w / total for c, w in weight.items()}


# Сколько раз за круг человека просят ЗАПИСАТЬ ГОЛОС, самое большее.
#
# Своя граница, а не только доля: голосовой ответ — единственный, который
# нельзя дать молча. Человек в автобусе, в офисе, рядом со спящим ребёнком
# не запишет ничего, и третья просьба за круг — это не трудность, это
# причина закрыть бота на четырнадцатом вопросе и потерять баллы за
# доведённый круг. Делитель 7 даёт 2 на круг из 15 и 3 на круг из 25.
def speech_cap(round_length: int) -> int:
    return max(1, round_length // 7)


# Сколько первых вопросов идут САМОЙ ЛЁГКОЙ из открытых игр.
#
# Разогрев. Первый вопрос задаёт тон занятию, и человеку, только что
# открывшему бота, нужна победа, а не производство речи с холодного
# старта. Прежде первым всегда выходил текст — но не по правилу, а потому
# что TEXT стоит первым в перечислении: поменяй порядок букв, и круг
# начинался бы речью, причём молча.
#
# ОДИН, А НЕ ДВА. При двух круг у продвинутого начинался «t t» — два
# одинаковых подряд, против чего в этом же правиле стоит отдельный пункт.
# Одного вопроса хватает, чтобы задать тон; дальше важнее перемежение.
WARMUP_QUESTIONS = 1

# С какого вопроса круга можно просить голос (2.2.1). Прод 14–18.10: «Говорю»
# на 1–3 вопросе показан 4 раза — и 3 раза человек ушёл на нём; к четвёртому
# вопросу занятие уже идёт, и голос — разнообразие, а не порог на входе.
# Прямой вход «🎤» с главного экрана (`prefer_channel`) правило не трогает:
# там человек сам попросил говорить.
SPEECH_FROM_QUESTION = 4


def enabled_channels(user: Optional[User]) -> list[QuizChannel]:
    """
    Какие каналы включены у человека, в постоянном порядке.

    Порядок задаётся перечислением, а не строкой в базе: от перестановки букв
    в настройке состав занятия меняться не должен.

    Текст возвращается всегда, даже если его выключили. Занятие без единого
    канала — это не занятие, а пустой экран, и пустым экраном настройка
    кончаться не имеет права.

    ВЫКЛЮЧЕННАЯ ОЗВУЧКА ОТМЕНЯЕТ СЛУХ И РЕЧЬ, что бы ни стояло в составе.
    Припоминание она НЕ отменяет: оно текстовое, просто в другую сторону.
    Это не удобство, а исправление настоящего дефекта: у вопроса на слух
    самого слова на экране НЕТ — его заменяет звук. Без звука остаётся
    «Послушай и выбери» и четыре варианта, то есть вопрос без вопроса, на
    который можно только ткнуть наугад. Ученик, выключивший озвучку,
    получал бы половину круга вслепую, и это происходило бы не изредка,
    а каждый раз.
    """
    raw = (getattr(user, "quiz_channels", None) or "t").lower()
    picked = [c for c in QuizChannel if c.value in raw]
    if not getattr(user, "audio_enabled", True):
        picked = [c for c in picked if c not in NEEDS_AUDIO]
    # «ГОВОРЮ» — ПО ЖЕЛАНИЮ (2.2.1, владелец): только у согласившихся.
    # Пока не спрашивали, «не сейчас» или «убрать» — игры нет; приглашение —
    # под итогом занятия (`speech_invite`). Объект без поля (симуляции,
    # приёмки) считается согласившимся — у них проверяется сама игра
    if getattr(user, "speech_choice", SPEECH_ON) != SPEECH_ON:
        picked = [c for c in picked if c is not QuizChannel.SPEECH]
    return picked or [QuizChannel.TEXT]


SPEECH_ON, SPEECH_OFF, SPEECH_LATER = "on", "off", "later"


async def pick_channel(
    session: AsyncSession,
    user: Optional[User],
    word: Word,
    learning_lang: str,
    recent: Optional[list[str]] = None,
    prefer: Optional[QuizChannel] = None,
    round_length: Optional[int] = None,
    position: Optional[int] = None,
) -> QuizChannel:
    """
    Каким каналом задать вопрос ПРО ЭТО СЛОВО.

    `round_length` и `position` (номер вопроса с единицы) — см.
    `generate_question`; не переданы — настройка и длина истории.

    Канал следует за словом, а не за номером вопроса. Первая версия просто
    чередовала «текст, слух, текст, слух» по счётчику, и это было неверно
    по сути: **нельзя узнать на слух то, чего ни разу не видел.** Новое
    слово, пришедшее сразу звуком, — не упражнение, а загадка: ученик жмёт
    наугад, промахивается и запоминает неверный вариант.

    ПРАВИЛО ДОПУСКА К СЛУХУ: слово хотя бы раз отвечено ВЕРНО.

    Не «показано» и не «выучено», а именно один верный ответ. Показано —
    мало: можно было ткнуть мимо. Выучено (три подряд) — много: ученик к
    тому времени уже перерос текстовый вопрос, и слух пришёл бы слишком
    поздно, когда интерес к слову иссяк. Один успех глазами — ровно та
    точка, где «узнаю написанное» уже есть, а «узнаю на слух» ещё нет.

    ЧТО РЕШАЕТСЯ ЗДЕСЬ, А ЧТО НИЖЕ. Здесь — только допуск: какие игры
    открыты ДЛЯ ЭТОГО СЛОВА. Какую из открытых взять, решает
    `place_in_round`, и там же описан состав круга целиком (разогрев, доли,
    потолок речи, перемежение).

    Разделено потому, что это разные вопросы. Допуск — про слово и про
    человека, и за ним надо идти в базу. Состав — про место в круге, и
    его можно пересчитать на столе, без базы и без бота. Пока они стояли
    вместе, правило состава было написано в описании одним, а в коде
    другим: обещалось «ритм ломается сам, случайности тут нет вовсе», а
    у продвинутого ученика выходило ровное t r a s t r a s — замер на
    40 кругах показал чистое чередование в 21 из них.

    `prefer` — прямой вход одним каналом с домашнего экрана. Порог допуска
    при этом НЕ обходится, в отличие от `generate_question(channel=...)`;
    разница разобрана ниже по ходу кода.
    """
    channels = enabled_channels(user)
    # Короткий путь — только для одной КАРТОЧКИ. Прежде он срабатывал на
    # любой единственный канал и обходил порог допуска: состав из одного
    # «Вспоминаю» или «Собираю» задавал так и НОВОЕ слово — вспомнить или
    # собрать то, чего человек ни разу не видел. Приёмка круга этого не
    # видела, пока сверяла порог только у слуха и речи
    if prefer is None and channels == [QuizChannel.TEXT]:
        return channels[0]

    progress = (await session.execute(
        select(UserWord.times_correct, UserWord.last_seen_at).where(
            UserWord.user_id == (user.id if user else 0),
            UserWord.word_id == word.id,
            UserWord.learning_lang == learning_lang,
        )
    )).first()
    times_correct = (progress[0] if progress else 0) or 0
    seen_at = progress[1] if progress else None

    # ПРЯМОЙ ВХОД ОДНИМ КАНАЛОМ — с домашнего экрана. Состав занятия тут не
    # спрашивается: человек только что ткнул в «🎧», это и есть его выбор на
    # сейчас. Но ПОРОГ ДОПУСКА остаётся в силе, и это главное отличие от
    # параметра `channel`, который порог обходит. Обойти его здесь значило бы
    # выдать новичку пятнадцать загадок подряд: слова он ни разу не видел,
    # узнать их на слух не может, и остаётся жать наугад — ровно то, против
    # чего и написано правило допуска. Слово, до канала не доросшее, придёт
    # текстом, и это честный ответ, а не поломка.
    # Годность по данным слова (`channel_fits`): сборке нужен пример в 3–10
    # слов с переводом. Пара — человека: на его родном показан пример
    pair = pair_from_user(user) if user is not None else None
    word_level = await level_of(session, word, pair.learning) if pair is not None else None

    def open_for_word(channel: QuizChannel) -> bool:
        return (times_correct >= CHANNEL_UNLOCK.get(channel, 0)
                and (pair is None or channel_fits(channel, word, pair,
                                                  getattr(user, "level", None),
                                                  word_level=word_level)))

    if prefer is not None:
        # Без озвучки закрыты ТОЛЬКО слух и речь. Прежде условие было «всё,
        # кроме текста», и вход «Вспоминаю» с выключенным звуком давал круг
        # из одних карточек — при том что «Вспоминаю» звука не требует.
        if prefer in NEEDS_AUDIO and not getattr(user, "audio_enabled", True):
            return QuizChannel.TEXT
        if open_for_word(prefer):
            return prefer
        return QuizChannel.TEXT

    # Какие каналы открыты ДЛЯ ЭТОГО СЛОВА. Порог растёт вместе с
    # трудностью канала: узнать написанное можно сразу, узнать на слух —
    # после одного успеха глазами, произнести и собрать — после двух. И
    # слово должно годиться игре: без примера в 3–10 слов собирать нечего.
    unlocked = [c for c in channels if open_for_word(c)] or [QuizChannel.TEXT]

    # СЛОВО, УЖЕ ВИДЕННОЕ СЕГОДНЯ, ВОЗВРАЩАЕТСЯ ДРУГОЙ ИГРОЙ. Карточкой его
    # только что узнали; вторая карточка того же слова за день ничему не
    # учит, а «Вспоминаю», «Слушаю» и «Говорю» — учат. Так отработка
    # (`get_practice_words`) и становится видимой.
    #
    # Кроме ПЕРВОГО вопроса круга (история пуста): круг открывается
    # карточкой, начинать с того, что непонятно без звука, плохо.
    #
    # И кроме случая, когда без карточки осталась лишь та игра, что уже шла
    # два раза подряд: «не три одинаковых подряд» важнее.
    if (recent and seen_at is not None
            and utcnow() - seen_at < timedelta(days=1)
            and len(unlocked) > 1):
        others = [c for c in unlocked if c is not QuizChannel.TEXT]
        third_in_a_row = (
            len(recent) >= 2 and recent[-1] == recent[-2]
            and all(c.value == recent[-1] for c in others)
        )
        if not third_in_a_row:
            unlocked = others

    if len(unlocked) == 1:
        return unlocked[0]

    return place_in_round(
        unlocked,
        enabled=channels,
        recent=recent or [],
        round_length=(round_length
                      or getattr(user, "quiz_word_count", None)
                      or DEFAULT_ROUND_LENGTH),
        position=position,
    )


def _channel_history(recent: list[str]) -> list[QuizChannel]:
    """
    История каналов круга: только настоящие каналы. Доска (`m`) занимает
    место в круге, но игрой-каналом не является.
    """
    known = {c.value: c for c in QuizChannel}
    return [known[v] for v in recent if v in known]


def _speech_closed(used: "collections.Counter", position: int,
                   round_length: int) -> bool:
    """
    Закрыта ли речь на вопросе номер `position` (с единицы): последний
    вопрос круга голосом не задаётся, и больше `speech_cap` голосовых за
    круг не просят, и на первых вопросах тоже (`SPEECH_FROM_QUESTION`). Одно
    правило на оба пути выбора игры — `place_in_round` и места отработки
    (`_rotation`).
    """
    return (position >= round_length
            or position < SPEECH_FROM_QUESTION
            or used[QuizChannel.SPEECH] >= speech_cap(round_length))


def place_in_round(
    unlocked: list[QuizChannel],
    *,
    enabled: list[QuizChannel],
    recent: list[str],
    round_length: int,
    position: Optional[int] = None,
) -> QuizChannel:
    """
    Какой игрой задать вопрос НА ЭТОМ МЕСТЕ круга.

    `position` — номер вопроса с единицы, если круг его знает. Выведенный
    из `recent` номер верен лишь в круге без доски: доска — вопрос круга,
    но в историю каналов не пишется, и после неё «последний вопрос» по
    истории наступал на вопрос позже настоящего — речь могла прийти
    последней.

    Отделено от `pick_channel` нарочно: сюда не ходят в базу, и всё решение
    видно целиком. Правило, которое нельзя проверить без живого человека и
    пятнадцати нажатий, в этом проекте уже один раз оказалось не тем, что
    написано в его же описании.

    ЧТО ЗНАЕТ ЭТА ФУНКЦИЯ: какие игры открыты ДЛЯ ЭТОГО СЛОВА (`unlocked`,
    их решает порог допуска), какие включены У ЧЕЛОВЕКА (`enabled` — по ним
    считается цель), чем заданы предыдущие вопросы (`recent`) и сколько
    вопросов в круге. Номер вопроса круг передаёт сам (`position`); без
    него он выводится из `recent`.

    ПРАВИЛА, ПО СТАРШИНСТВУ:

      1. разогрев      первые два вопроса — самой лёгкой из открытых
      2. речь не последней   на последнем вопросе голос не просят
      3. потолок речи  не больше `speech_cap` голосовых за круг
      4. не два подряд одинаковых, если есть выбор
      5. отставание    из оставшихся берётся та игра, которой до её доли
                       не хватает БОЛЬШЕ всех

    Пятое и есть суть: доля каждой игры задана ценой ответа
    (`channel_targets`), и выбирается та, что отстала. Отсюда состав круга
    сходится к цели сам, а порядок остаётся неровным — потому что неровен
    материал: у разных слов открыты разные игры. Прежде здесь стоял
    круговой перебор от предыдущего канала, и у продвинутого ученика он
    давал ровное t r a s t r a s — предсказуемое, то есть скучное.

    Правило — ЦЕЛЬ, А НЕ СТЕНА. Если открыт один канал, он и придёт, сколько
    бы его уже ни было: пятнадцать карточек подряд у новичка — это не
    поломка состава, а правило допуска. Нельзя спросить на слух слово,
    которого человек ни разу не видел.
    """
    if len(unlocked) == 1:
        return unlocked[0]

    targets = channel_targets(enabled)
    # Из истории берутся только настоящие каналы: доска (`m`) занимает место
    # в круге, но игрой-каналом не является, и её пять подвопросов сдвинули
    # бы номер вопроса на пять
    history = _channel_history(recent)
    if position is None:
        position = len(history) + 1
    used = collections.Counter(history)

    allowed = list(unlocked)

    # 1. РАЗОГРЕВ: первый вопрос — самой лёгкой из открытых.
    #
    # «Лёгкая» берётся из ПОРЯДКА ПЕРЕЧИСЛЕНИЯ, и это единственное место,
    # где на него можно опираться: `QuizChannel` выстроен по возрастанию
    # трудности нарочно, и так и описан в `enums.py` (с замером 87.9/87.1 на
    # карточке и припоминании). Ценой ответа тут не обойтись: карточка и
    # припоминание стоят одинаково, и первая редакция этого правила
    # разрешала их ничью по БУКВЕ — «r» меньше «t», — отчего круг у
    # продвинутого начинался припоминанием в 37 случаях из 40. Ровно та
    # беда, против которой правило и писалось.
    if position <= WARMUP_QUESTIONS:
        order = list(QuizChannel)
        return min(allowed, key=order.index)

    # 2. РЕЧЬ НЕ ПОСЛЕДНЕЙ и 3. ПОТОЛОК РЕЧИ — то же правило, что у мест
    # отработки (`_rotation`)
    if QuizChannel.SPEECH in allowed and _speech_closed(used, position, round_length):
        rest = [c for c in allowed if c is not QuizChannel.SPEECH]
        if rest:
            allowed = rest

    # 4. НЕ ДВА ОДИНАКОВЫХ ПОДРЯД, если есть чем заменить. Перемежение
    # закрепляет слово прочнее, чем блок однотипных повторов, — это и было
    # главным доводом против «трёх игр тремя кнопками в меню».
    if history:
        rest = [c for c in allowed if c is not history[-1]]
        if rest:
            allowed = rest

    # 5. ОТСТАВАНИЕ ОТ ДОЛИ: берётся игра, которой до её доли не хватает
    # больше всех.
    def deficit(channel: QuizChannel) -> float:
        return targets.get(channel, 0) * position - used[channel]

    best = max(deficit(c) for c in allowed)

    # РАВНО ОТСТАВШИЕ РАВНО ПРАВИЛЬНЫ — и выбор между ними СЛУЧАЕН.
    #
    # Это единственная случайность в составе круга, и она здесь нужна.
    # Первая редакция решала ничью по букве канала, и у продвинутого ученика
    # занятие выходило ОДИНАКОВЫМ день за днём: t r a s r t r t a r t s r t a
    # в трёх кругах подряд из трёх. Отставание у него почти всегда ничейное
    # (открыто всё, цели близки), поэтому строгий порядок превращал правило
    # в расписание. Прежний круговой перебор болел тем же, только узор был
    # другой: t r a s t r a s.
    #
    # Полшага — это «меньше половины вопроса»: ближе уже не отличить, какая
    # игра отстала сильнее, и спорить тут не о чем.
    ties = [c for c in allowed if best - deficit(c) < 0.5]
    return random.choice(ties) if len(ties) > 1 else ties[0]
