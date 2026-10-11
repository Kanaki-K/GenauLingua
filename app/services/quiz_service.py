"""
Движок викторины: подбор слова по SRS, сборка вариантов ответа, учёт прогресса.

Не зависит от изучаемого языка — язык приходит в LanguagePair. Слова берутся
только канонические для изучаемого языка (см. app/services/word_groups.py),
иначе одно и то же слово встречалось бы несколько раз.
"""

import random
from datetime import datetime, timedelta
from app.core.clock import utcnow
from typing import Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import PartOfSpeech, User, UserWord, Word, WordLangGroup
from app.services.language_service import (
    LanguagePair,
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
        return query.where(Word.level == user.level)

    if user.quiz_mode == QuizMode.ALL_WORDS:
        return query

    if user.quiz_mode == QuizMode.DIFFICULT:
        return query

    # LEVEL и всё неизвестное
    return query.where(Word.level == user.level)


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


# ============================================================================
# SRS: ВЫБОР СЛОВА ПО ПРИОРИТЕТУ
# ============================================================================

async def select_word_by_priority(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
    exclude_ids: list[int],
    user: Optional[User] = None,
    level: Optional[CEFRLevel] = None,
) -> Optional[Word]:
    """
    Слово по весам: тяжёлые → новые → на повторение → выученные.
    Если выбранная корзина пуста, пробуются следующие.
    """
    buckets = [
        (STRUGGLING_WORDS_RATIO, get_struggling_words),
        (STRUGGLING_WORDS_RATIO + NEW_WORDS_RATIO, get_new_words),
        (STRUGGLING_WORDS_RATIO + NEW_WORDS_RATIO + REVIEW_WORDS_RATIO, get_review_words),
    ]

    rand = random.random()
    for threshold, getter in buckets:
        if rand < threshold:
            word = await getter(user_id, session, pair, exclude_ids, user=user, level=level)
            if word:
                return word

    word = await get_learned_words(user_id, session, pair, exclude_ids, user=user, level=level)
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


async def get_struggling_words(
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
        _accuracy_below(STRUGGLING_THRESHOLD),
        _cooled_down(),
    )
    return await _pick_one(session, _exclude(_scoped(query, user, level), exclude_ids))


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
    seen = (
        select(UserWord.word_id)
        .where(
            UserWord.user_id == user_id,
            UserWord.learning_lang == pair.learning,
            UserWord.word_id == Word.id,
        )
        .exists()
    )
    query = _usable_words(pair).where(~seen)
    return await _pick_one(session, _exclude(_scoped(query, user, level), exclude_ids))


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
    return await _pick_one(session, _exclude(_scoped(query, user, level), exclude_ids))


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
    return await _pick_one(session, _exclude(_scoped(query, user, level), exclude_ids))


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
    query = _progress_join(_usable_words(pair), user_id, pair).where(
        UserWord.learned.is_(False),
        UserWord.times_shown >= 2,
        _accuracy_below(STRUGGLING_THRESHOLD),
        _cooled_down(),
    )
    return await _pick_one(session, _exclude(query, exclude_ids))


async def count_difficult_words(
    user_id: int,
    session: AsyncSession,
    pair: LanguagePair,
) -> int:
    """Сколько сложных слов у пользователя на этом языке."""
    query = (
        select(func.count())
        .select_from(UserWord)
        .where(
            UserWord.user_id == user_id,
            UserWord.learning_lang == pair.learning,
            UserWord.learned.is_(False),
            UserWord.times_shown >= 2,
            _accuracy_below(STRUGGLING_THRESHOLD),
        )
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
    picked: list[Word] = []
    excluded_ids = [correct_word.id]

    base = _usable_words(pair)

    # 1. Та же часть речи и тот же уровень; для существительных — иной артикль
    # (в режимах по категории и по всей базе уровень не ограничиваем).
    same_level = not (user and user.quiz_mode in (QuizMode.CATEGORY, QuizMode.ALL_WORDS))
    strict = base.where(Word.pos == correct_word.pos)
    if same_level:
        strict = strict.where(Word.level == correct_word.level)
    if correct_word.pos == PartOfSpeech.NOUN and correct_word.article:
        strict = strict.where(
            or_(Word.article.is_(None), Word.article != correct_word.article)
        )

    # 2. Та же часть речи, любой уровень и артикль
    by_pos = base.where(Word.pos == correct_word.pos)

    # 3. Любое слово — лишь бы вариантов было четыре
    anything = base

    for stage in (strict, by_pos, anything):
        if len(picked) >= count:
            break

        candidates = await session.execute(
            _exclude(stage, excluded_ids).order_by(func.random()).limit(DISTRACTOR_CANDIDATES)
        )
        for candidate in candidates.scalars():
            variants = _option_variants(candidate, answer_lang)
            # Пересечение хотя бы по одному значению делает вариант
            # неотличимо верным — такой дистрактор не годится
            if not variants or variants & taken:
                continue
            taken |= variants
            picked.append(candidate)
            excluded_ids.append(candidate.id)
            if len(picked) >= count:
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


async def generate_question(
    session: AsyncSession,
    user: User,
    exclude_ids: Optional[list[int]] = None,
    pair: Optional[LanguagePair] = None,
) -> Optional[dict]:
    """
    Вопрос викторины: слово, варианты ответа, индекс правильного.

    Возвращает None, если подходящих слов не осталось.
    """
    exclude_ids = exclude_ids or []
    pair = pair or pair_from_user(user)

    if user.quiz_mode == QuizMode.DIFFICULT:
        correct_word = await get_difficult_word(user.id, session, pair, exclude_ids)
    else:
        correct_word = await select_word_by_priority(
            user_id=user.id,
            session=session,
            pair=pair,
            exclude_ids=exclude_ids,
            user=user,
        )

    if not correct_word:
        return None

    distractors = await get_distractors(correct_word, session, pair, user=user)

    # Меньше четырёх различимых вариантов — вопрос был бы некорректным
    if len(distractors) < OPTIONS_TOTAL - 1:
        return None

    options, correct_index = build_options(correct_word, distractors, pair)

    return {
        "correct_word": correct_word,
        "options": options,
        "correct_answer_index": correct_index,
        "pair": pair,
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
            correct_streak=1 if is_correct else 0,
            times_shown=1,
            times_correct=1 if is_correct else 0,
            last_seen_at=now,
            learned=False,
        )
        _count_channel(user_word, channel, is_correct)
        session.add(user_word)
        await session.commit()
        return

    user_word.times_shown += 1
    user_word.last_seen_at = now
    _count_channel(user_word, channel, is_correct)

    if is_correct:
        user_word.correct_streak += 1
        user_word.times_correct += 1
    elif user_word.correct_streak > 3:
        user_word.correct_streak = max(2, user_word.correct_streak - 2)
    else:
        user_word.correct_streak = max(0, user_word.correct_streak - 1)

    user_word.learned = _is_learned(user_word, now)
    await session.commit()


def _count_channel(user_word: UserWord, channel: QuizChannel, is_correct: bool) -> None:
    """
    Засчитать показ своему каналу.

    Текстовый канал не упомянут нарочно: его счётчики выводятся из итога
    вычитанием, и ничего прибавлять к ним не надо. Если когда-нибудь здесь
    появится ветка для TEXT — значит кто-то завёл ему колонку, и вместе с
    ней завёл возможность расхождения с итогом.
    """
    if channel is QuizChannel.AUDIO:
        user_word.shown_audio += 1
        if is_correct:
            user_word.correct_audio += 1
    elif channel is QuizChannel.SPEECH:
        user_word.shown_speech += 1
        if is_correct:
            user_word.correct_speech += 1


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
            query = query.where(Word.level == level)
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

# Сколько верных ответов этим каналом считать освоением слова. Три — то же
# число, что и в MIN_ATTEMPTS_FOR_LEARNED, и выбрано не ради красоты: один
# верный ответ бывает угадыванием из четырёх, два подряд — везением, а три
# уже требуют знания. Подряд их идти НЕ обязано: это не серия, а счёт.
CHANNEL_MASTERY = 3


async def get_channel_progress(
    user_id: int, session: AsyncSession, learning_lang: str
) -> dict[str, int]:
    """
    Сколько слов человек узнаёт глазами, на слух и произносит.

    Это и есть три шкалы домашнего экрана. Самое полезное в них — не сами
    числа, а РАЗРЫВ между ними: «342 узнаю глазами, а произношу 64» говорит
    о человеке правду, которую он сам о себе не знает, и мотивирует сильнее
    любого бейджа.

    Текстовая шкала считается вычитанием, ровно как в модели: отдельной
    колонки у неё нет, и разойтись с итогом она не может.
    """
    text_correct = (
        UserWord.times_correct - UserWord.correct_audio - UserWord.correct_speech
    )

    row = await session.execute(
        select(
            func.count().filter(text_correct >= CHANNEL_MASTERY),
            func.count().filter(UserWord.correct_audio >= CHANNEL_MASTERY),
            func.count().filter(UserWord.correct_speech >= CHANNEL_MASTERY),
            func.count(),
        ).where(
            UserWord.user_id == user_id,
            UserWord.learning_lang == learning_lang,
        )
    )
    by_text, by_audio, by_speech, touched = row.one()

    return {
        "text": by_text or 0,
        "audio": by_audio or 0,
        "speech": by_speech or 0,
        "touched": touched or 0,
    }


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

    Если созвучных не набралось (редкое слово, короткий язык), добор идёт
    обычными дистракторами: лучше более лёгкий вопрос, чем вопрос без
    вариантов.
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
            if not label.lower().startswith(head.lower()):
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
