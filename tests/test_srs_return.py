"""
Слово возвращается. Главный дефект продукта и его лечение.

ЧТО БЫЛО. Подбор слова шёл по четырём корзинам, и все ключевались на
ТОЧНОСТИ: трудные (<70%), новые (ряда нет), на повторение (70–90%),
выученные. Слово, отвеченное верно с первого раза, имеет точность 100% и
метки «выучено» не имеет — то есть не попадало НИ В ОДНУ корзину.

Замер по рабочей копии 13 октября 2026:

    слов в прогрессе                       21 306
    НЕ ВЕРНУТСЯ НИКОГДА                    18 664  (87.6%)
    людей задето                              193 из 199
    в среднем недостижимо у человека          84.5% его словаря
    слов в корзине «на повторение»               3  (на них шло 9% подбора)

И следствие, которое всё объясняет: **98.2% выученных слов человек хотя бы
раз отвечал НЕВЕРНО** — 1 509 из 1 537. Чтобы выучить слово, надо было
сперва его провалить: только ошибка роняла точность ниже 70 и возвращала
слово в подбор.

ЧТО СТАЛО. Корзины ключуются на ВРЕМЕНИ: у каждой длины серии свой срок
(`REVIEW_SCHEDULE`). Сроки выведены из поведения — 56.6% возвратов
приходятся на следующий день, поэтому первая ступень сутки; короче нельзя,
потому что 71% дней это два круга и больше с разрывом 0.4 часа.

Замер того же дня: доступных к показу знакомых слов 1 105 → 21 240, людей
без материала для повторения 37 → 0.
"""

from datetime import timedelta

import pytest
from sqlalchemy import delete, select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import User, UserWord, Word
from app.services.language_service import pair_from_user
from app.services.quiz_service import (
    CHANNEL_MASTERY,
    DEFAULT_ROUND_LENGTH,
    NEW_WORDS_PER_ROUND,
    REVIEW_SCHEDULE,
    REVIEW_SCHEDULE_TAIL,
    count_due_words,
    get_due_words,
    select_word_by_priority,
    wants_new_word,
)
from tests.conftest import build_groups, make_word

# Модульной пометки asyncio здесь НЕТ: в pytest.ini стоит
# `asyncio_mode = auto`, и на синхронных проверках состава круга она даёт
# предупреждение. То же замечание записано в `tests/test_quiz_flow.py`.

WORDS = 40


async def _ready(session, user, *, count: int = 15) -> list[Word]:
    for i in range(WORDS):
        session.add(make_word(f"Wort{i:03d}", level=CEFRLevel.A1))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = count
    user.quiz_channels = "t"
    user.audio_enabled = False
    await session.commit()

    return list((await session.execute(select(Word).order_by(Word.id))).scalars().all())


async def _seen(session, user, word, *, streak: int, ago: timedelta) -> None:
    await session.execute(
        delete(UserWord).where(
            UserWord.user_id == user.id, UserWord.word_id == word.id
        )
    )
    session.add(UserWord(
        user_id=user.id, word_id=word.id, learning_lang="de",
        times_shown=max(1, streak), times_correct=streak,
        correct_streak=streak, learned=streak >= 3,
        last_seen_at=utcnow() - ago,
    ))
    await session.commit()


# ============================================================================
# СЛОВО ВОЗВРАЩАЕТСЯ
# ============================================================================

async def test_a_word_answered_right_comes_back(session, user):
    """
    Самая важная проверка во всём наборе.

    Прежде этот случай означал потерю слова навсегда: точность 100%, метки
    «выучено» нет, ни одна корзина не берёт.
    """
    words = await _ready(session, user)
    pair = pair_from_user(user)
    word = words[0]

    await _seen(session, user, word, streak=1, ago=timedelta(days=2))

    due = await get_due_words(user.id, session, pair, [], user=user)
    assert due is not None, "слово, отвеченное верно, не вернулось"
    assert due.id == word.id


async def test_it_does_not_come_back_before_its_time(session, user):
    """
    Срок — это не украшение. Слово, показанное час назад, не должно
    возвращаться: 71% дней это два круга подряд с разрывом 0.4 часа, и
    человек получил бы то же слово через двадцать минут.
    """
    words = await _ready(session, user)
    pair = pair_from_user(user)

    await _seen(session, user, words[0], streak=1, ago=timedelta(hours=3))

    due = await get_due_words(user.id, session, pair, [], user=user)
    assert due is None, f"вернулось раньше срока: {due.word_de if due else ''}"


@pytest.mark.parametrize("streak", sorted(REVIEW_SCHEDULE))
async def test_every_step_of_the_ladder_works(session, user, streak):
    """Каждая ступень расписания: не раньше срока, но после — да."""
    words = await _ready(session, user)
    pair = pair_from_user(user)
    delay = REVIEW_SCHEDULE[streak]
    word = words[0]

    await _seen(session, user, word, streak=streak, ago=delay / 2)
    assert await get_due_words(user.id, session, pair, [], user=user) is None, (
        f"серия {streak}: вернулось вдвое раньше срока {delay}"
    )

    await _seen(session, user, word, streak=streak, ago=delay + timedelta(minutes=1))
    due = await get_due_words(user.id, session, pair, [], user=user)
    assert due is not None and due.id == word.id, (
        f"серия {streak}: не вернулось после срока {delay}"
    )


async def test_a_long_streak_falls_into_the_tail(session, user):
    """Серия длиннее последней ступени — поддержание раз в два месяца."""
    words = await _ready(session, user)
    pair = pair_from_user(user)
    long_streak = max(REVIEW_SCHEDULE) + 3

    await _seen(session, user, words[0], streak=long_streak,
                ago=REVIEW_SCHEDULE_TAIL / 2)
    assert await get_due_words(user.id, session, pair, [], user=user) is None

    await _seen(session, user, words[0], streak=long_streak,
                ago=REVIEW_SCHEDULE_TAIL + timedelta(days=1))
    assert await get_due_words(user.id, session, pair, [], user=user) is not None


async def test_a_learned_word_still_comes_back(session, user):
    """
    Выученное не исчезает из жизни: оно возвращается на поддержание.

    Прежде выученному доставался один процент подбора — то есть оно
    забывалось тихо.
    """
    words = await _ready(session, user)
    pair = pair_from_user(user)

    await _seen(session, user, words[0], streak=4, ago=timedelta(days=22))

    due = await get_due_words(user.id, session, pair, [], user=user)
    assert due is not None and due.id == words[0].id
    assert await count_due_words(user.id, session, pair, user=user) == 1


async def test_the_oldest_debt_comes_first(session, user):
    """
    Долг разбирается с самого залежавшегося, а не наугад.

    Иначе у человека, вернувшегося после месяца, часть слов висела бы
    просроченной годами — пока жребий до них не дойдёт.
    """
    words = await _ready(session, user)
    pair = pair_from_user(user)
    ages = (timedelta(days=30), timedelta(days=10), timedelta(days=2))
    for word, ago in zip(words[:3], ages):
        await _seen(session, user, word, streak=1, ago=ago)

    order, taken = [], []
    for _ in range(3):
        word = await get_due_words(user.id, session, pair, taken, user=user)
        assert word is not None
        order.append(word.id)
        taken.append(word.id)

    assert order == [w.id for w in words[:3]], "порядок не от старого к свежему"


# ============================================================================
# СОСТАВ КРУГА
# ============================================================================

def test_new_words_are_spread_through_the_round():
    """
    Новые раскладываются по кругу, а не кучей в конце: открытие должно
    встречаться каждые несколько вопросов.
    """
    places = [i + 1 for i in range(15) if wants_new_word(i, 15)]
    assert places == [5, 10, 15]
    assert len(places) == NEW_WORDS_PER_ROUND


def test_a_short_round_still_gets_new_words():
    """У круга из пяти вопросов новые тоже есть — пол соблюдается."""
    places = [i + 1 for i in range(5) if wants_new_word(i, 5)]
    assert places, "в коротком круге не осталось ни одного нового слова"


async def test_the_round_holds_its_composition(session, user):
    """
    Круг из пятнадцати при достатке просроченных: ровно столько новых,
    сколько обещано, и ни одного повтора.

    Прежде состав бросался жребием на каждый вопрос, и при тридцати
    процентах новых их выходило от нуля до девяти.
    """
    words = await _ready(session, user)
    pair = pair_from_user(user)
    for word in words[:20]:
        await _seen(session, user, word, streak=1, ago=timedelta(days=2))

    known = {w.id for w in words[:20]}
    picked: list[int] = []
    fresh = 0
    for _ in range(DEFAULT_ROUND_LENGTH):
        word = await select_word_by_priority(
            user.id, session, pair, picked, user=user,
            round_length=DEFAULT_ROUND_LENGTH,
        )
        assert word is not None, f"круг оборвался на {len(picked)}-м вопросе"
        picked.append(word.id)
        if word.id not in known:
            fresh += 1

    assert len(picked) == DEFAULT_ROUND_LENGTH
    assert len(set(picked)) == len(picked), "слово повторилось внутри круга"
    assert fresh == NEW_WORDS_PER_ROUND, f"новых вышло {fresh}"


async def test_the_second_day_is_built_from_the_first(session, user):
    """
    САМЫЙ ДОРОГОЙ СЛУЧАЙ. 56.6% возвратов приходятся на следующий день, а
    112 человек из 199 занимались ровно один день — второй день и решает
    всё.

    Прежде он выглядел так же, как первый: слова первого дня были
    недостижимы, и человек получал пятнадцать новых.
    """
    words = await _ready(session, user)
    pair = pair_from_user(user)
    yesterday = words[:15]
    for index, word in enumerate(yesterday):
        await _seen(session, user, word, streak=0 if index < 3 else 1,
                    ago=timedelta(days=1, hours=2))

    known = {w.id for w in yesterday}
    picked: list[int] = []
    repeats = 0
    for _ in range(DEFAULT_ROUND_LENGTH):
        word = await select_word_by_priority(
            user.id, session, pair, picked, user=user,
            round_length=DEFAULT_ROUND_LENGTH,
        )
        assert word is not None
        picked.append(word.id)
        if word.id in known:
            repeats += 1

    assert repeats == DEFAULT_ROUND_LENGTH - NEW_WORDS_PER_ROUND, (
        f"слов первого дня в круге {repeats}, а должно "
        f"{DEFAULT_ROUND_LENGTH - NEW_WORDS_PER_ROUND}"
    )


async def test_a_fresh_person_gets_a_full_round_of_new_words(session, user):
    """Первый день: повторять нечего, и круг всё равно собирается целиком."""
    await _ready(session, user)
    pair = pair_from_user(user)

    picked: list[int] = []
    for _ in range(DEFAULT_ROUND_LENGTH):
        word = await select_word_by_priority(
            user.id, session, pair, picked, user=user,
            round_length=DEFAULT_ROUND_LENGTH,
        )
        assert word is not None, f"круг новичка оборвался на {len(picked)}-м"
        picked.append(word.id)

    assert len(set(picked)) == DEFAULT_ROUND_LENGTH


# ============================================================================
# ШКАЛА ДВИЖЕТСЯ
# ============================================================================

async def test_one_correct_answer_moves_the_scale(session, user):
    """
    Шкала «узнаю» должна сдвинуться с первого верного ответа этим способом.

    Прежде требовалось три верных именно этим каналом: у 154 человек из 199
    нет ни одного слова с тремя верными вообще.
    """
    from app.services.quiz_service import get_channel_progress

    words = await _ready(session, user)
    pair = pair_from_user(user)

    session.add(UserWord(
        user_id=user.id, word_id=words[0].id, learning_lang="de",
        times_shown=1, times_correct=1, correct_streak=1,
        shown_audio=1, correct_audio=1, last_seen_at=utcnow(),
    ))
    await session.commit()

    progress = await get_channel_progress(
        user.id, session, pair, level=CEFRLevel.A1
    )
    assert CHANNEL_MASTERY == 1
    assert progress["audio"] == 1, (
        f"после верного ответа на слух шкала показывает {progress['audio']}"
    )
