"""
Уровень сам предлагает подняться — когда стал лёгким.

ПОЧЕМУ ПРИЗНАК НЕ ТОТ, ЧТО БЫЛ ЗАПИСАН В ДОРОЖНОЙ КАРТЕ

`ROADMAP.md` §3.5 обещал: «если 90% слов уровня освоены — предложить
следующий». Замер по всей базе показал, что это правило не сработало бы НИ
РАЗУ: лучший человек освоил 9.5% своего уровня (117 слов из 1235), а выше
десяти процентов нет никого. В A1 тысяча двести слов, и дойти до девятисот
— это сотни кругов.

Вопрос ведь не «прошёл ли человек уровень», а «не стал ли уровень лёгким».
На него отвечает ТОЧНОСТЬ: на A1 тридцать пять человек из шестидесяти двух
отвечают верно в девяти случаях из десяти. Их видно сегодня.

Эти тесты держат три вещи: что порог различает, что отказ помнится, и что
бот СПРАШИВАЕТ, а не переключает молча.
"""

import pytest

from app.database.enums import CEFRLevel
from app.database.models import QuizQuestion, QuizSession, User, Word
from app.services.level_service import (
    EASY_ACCURACY,
    LEVEL_ORDER,
    MIN_ANSWERS,
    NEWCOMER_LESSONS,
    NEWCOMER_MIN_ANSWERS,
    RECENT_ANSWERS,
    decline_level,
    next_level,
    raise_level,
    recent_accuracy,
    should_offer_next_level,
)
from tests.conftest import build_groups, make_word


# ============================================================================
# ЛЕСТНИЦА УРОВНЕЙ
# ============================================================================

def test_levels_go_up_one_step_at_a_time():
    assert next_level(CEFRLevel.A1) is CEFRLevel.A2
    assert next_level(CEFRLevel.B1) is CEFRLevel.B2


def test_there_is_nothing_above_the_top():
    """С верхнего уровня подниматься некуда, и предлагать нечего."""
    assert next_level(LEVEL_ORDER[-1]) is None


def test_no_level_means_no_offer():
    assert next_level(None) is None


# ============================================================================
# КОГДА ПРЕДЛАГАТЬ
# ============================================================================

async def _answers(session, user: User, correct: int, wrong: int) -> None:
    """
    Проставить человеку ответы на его текущем уровне.

    Слово заводится один раз на тест: у `words` уникальность по паре
    (слово, уровень), и второй вызов помощника падал бы на ней, а не на
    том, что проверяется.
    """
    from sqlalchemy import select

    word = (await session.execute(select(Word))).scalars().first()
    if word is None:
        session.add(make_word("Haus", level=user.level))
        await build_groups(session, ["de"])
        word = (await session.execute(select(Word))).scalars().first()
    quiz = QuizSession(
        user_id=user.id, learning_lang=user.learning_lang, level=user.level,
        total_questions=correct + wrong,
    )
    session.add(quiz)
    await session.commit()

    # Время ответа нарастает, и отсчёт ведётся от ЧИСЛА УЖЕ ЗАПИСАННЫХ
    # вопросов, а не от «сейчас». Второй вызов помощника иначе лёг бы на
    # секунды РАНЬШЕ хвоста первого: `utcnow()` между вызовами сдвигается на
    # микросекунды, а внутри вызова шаг — целая секунда.
    from datetime import timedelta
    from sqlalchemy import func as sa_func

    from app.core.clock import utcnow

    already = int((await session.execute(
        select(sa_func.count()).select_from(QuizQuestion)
    )).scalar() or 0)

    start = utcnow()
    for i in range(correct + wrong):
        session.add(QuizQuestion(
            session_id=quiz.id, word_id=word.id, is_correct=i < correct,
            answered_at=start + timedelta(seconds=already + i),
        ))
    await session.commit()


@pytest.mark.asyncio
async def test_too_few_answers_to_judge(session, user):
    """
    При малом числе ответов одна ошибка двигает точность на пять пунктов, и
    предложение превращается в лотерею.
    """
    user.quizzes_passed = NEWCOMER_LESSONS + 1  # обычное правило — два занятия
    user.level = CEFRLevel.A1
    await _answers(session, user, correct=MIN_ANSWERS - 1, wrong=0)

    assert await should_offer_next_level(user, session) is None


@pytest.mark.asyncio
async def test_offered_when_the_level_got_easy(session, user):
    user.level = CEFRLevel.A1
    await _answers(session, user, correct=MIN_ANSWERS, wrong=0)

    assert await should_offer_next_level(user, session) is CEFRLevel.A2


@pytest.mark.asyncio
async def test_not_offered_while_the_level_still_bites(session, user):
    """
    Порог обязан РАЗЛИЧАТЬ. Проверка на точности заведомо ниже порога: если
    и она пройдёт, правило метит во всех подряд, а не в тех, кому легко.
    """
    user.quizzes_passed = NEWCOMER_LESSONS + 1  # обычное правило — два занятия
    user.level = CEFRLevel.A1
    wrong = max(1, int(MIN_ANSWERS * (1 - EASY_ACCURACY)) + 2)
    await _answers(session, user, correct=MIN_ANSWERS, wrong=wrong)

    answered, accuracy = await recent_accuracy(user, session)
    assert accuracy < EASY_ACCURACY, "посев не ниже порога — проверка вхолостую"
    assert await should_offer_next_level(user, session) is None


@pytest.mark.asyncio
async def test_nothing_is_offered_from_the_top_level(session, user):
    user.level = LEVEL_ORDER[-1]
    await _answers(session, user, correct=MIN_ANSWERS, wrong=0)

    assert await should_offer_next_level(user, session) is None


@pytest.mark.asyncio
async def test_only_recent_answers_count(session, user):
    """
    Человек учится, и точность первых кругов к сегодняшнему дню отношения
    не имеет. Старые промахи не должны мешать предложению: за всю жизнь они
    усредняются и оно приходит с опозданием на месяцы.
    """
    user.level = CEFRLevel.A1
    # Сперва много промахов, потом ровно столько верных, сколько помещается
    # в окно последних ответов
    await _answers(session, user, correct=0, wrong=RECENT_ANSWERS)
    await _answers(session, user, correct=RECENT_ANSWERS, wrong=0)

    answered, accuracy = await recent_accuracy(user, session)
    assert answered == RECENT_ANSWERS, "окно последних ответов не соблюдено"
    assert await should_offer_next_level(user, session) is CEFRLevel.A2


# ============================================================================
# ОТКАЗ ПОМНИТСЯ
# ============================================================================

@pytest.mark.asyncio
async def test_refusal_is_remembered(session, user):
    """
    Не запомни отказ — и предложение вернётся после следующего же круга, и
    так после каждого, пока человек не уйдёт.
    """
    user.level = CEFRLevel.A1
    await _answers(session, user, correct=MIN_ANSWERS, wrong=0)
    assert await should_offer_next_level(user, session) is CEFRLevel.A2

    await decline_level(user, session)

    assert await should_offer_next_level(user, session) is None


@pytest.mark.asyncio
async def test_refusal_applies_to_that_level_only(session, user):
    """
    «Не хочу с A1 на A2» не значит «никогда ничего не предлагай».
    Поднявшись своей волей, человек снова услышит предложение.
    """
    user.level = CEFRLevel.A1
    await _answers(session, user, correct=MIN_ANSWERS, wrong=0)
    await decline_level(user, session)

    # Перешёл сам, руками, через настройки
    user.level = CEFRLevel.A2
    await session.commit()
    await _answers(session, user, correct=MIN_ANSWERS, wrong=0)

    assert await should_offer_next_level(user, session) is CEFRLevel.B1


@pytest.mark.asyncio
async def test_agreeing_raises_the_level_and_clears_the_old_refusal(session, user):
    user.level = CEFRLevel.A1
    user.level_offer_declined = CEFRLevel.A1.value
    await session.commit()

    await raise_level(user, session, CEFRLevel.A2)

    assert user.level is CEFRLevel.A2
    assert user.level_offer_declined is None, "отказ от прежнего уровня пережил переход"


# ============================================================================
# СОГЛАСИЕ: ОДИН ЭКРАН, ЧАТ ЧИСТ
#
# Живой тест владельца 14 октября: после «да» в чате остались итог круга,
# голое «Уровень A2. Слова будут потруднее.» без кнопок и новый якорь под
# ними. «Должно быть всегда одно меню». Якорь — закладка зачистки, и при
# переезде вниз он обязан забрать с собой всё, что было между.
# ============================================================================

async def test_agreeing_leaves_one_clean_screen(session, user):
    from app.locales import get_text
    from app.testing import make_bot, make_dispatcher, press, reset_state

    user.level = CEFRLevel.A1
    user.anchor_message_id = 990          # якорь над итогом круга
    await session.commit()

    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)

    # Предложение пришло сообщением 995, под итогом круга
    await dp.feed_update(bot, press(user.id, "level_up_A2", message_id=995))

    await session.refresh(user)
    assert user.level == CEFRLevel.A2
    new_anchor = user.anchor_message_id
    assert new_anchor and new_anchor != 990

    deleted = {p["message_id"] for n, p in recorder.calls if n == "DeleteMessage"}
    # Прежний якорь, итог круга и само предложение — всё между ними ушло
    assert {990, 993, 995} <= deleted, sorted(deleted)
    assert new_anchor not in deleted

    # Под якорем — ровно один экран, с кнопками и подтверждением сверху
    sent = [p for n, p in recorder.calls if n == "SendMessage"]
    screens = [p for p in sent if p.get("reply_markup", {}).get("inline_keyboard")]
    assert len(screens) == 1, [p.get("text", "")[:40] for p in sent]
    done = get_text("level_offer_done", user.interface_language or "ru", following="A2")
    assert screens[0]["text"].startswith(done)


# ============================================================================
# ОТКАЗ НЕ НАВСЕГДА — через пять занятий на высокой точности спросим снова
# ============================================================================

@pytest.mark.asyncio
async def test_a_refusal_is_asked_again_after_five_lessons(session, user):
    """
    Владелец, 14 октября: «если он ещё 5 игр будет на высоком уровне —
    предлагаем перейти». Прежде отказ на этом уровне был навсегда.
    """
    from app.services.level_service import REOFFER_AFTER_ROUNDS

    user.level = CEFRLevel.A1
    user.quizzes_passed = 10
    await _answers(session, user, correct=MIN_ANSWERS, wrong=0)
    await decline_level(user, session)
    assert await should_offer_next_level(user, session) is None, "спросили сразу после отказа"

    user.quizzes_passed = 10 + REOFFER_AFTER_ROUNDS - 1
    await session.commit()
    assert await should_offer_next_level(user, session) is None, "спросили раньше пяти занятий"

    user.quizzes_passed = 10 + REOFFER_AFTER_ROUNDS
    await session.commit()
    assert await should_offer_next_level(user, session) is CEFRLevel.A2, (
        "через пять занятий на высокой точности не спросили"
    )


@pytest.mark.asyncio
async def test_a_second_refusal_restarts_the_count(session, user):
    from app.services.level_service import REOFFER_AFTER_ROUNDS

    user.level = CEFRLevel.A1
    user.quizzes_passed = 10 + REOFFER_AFTER_ROUNDS
    user.level_offer_declined = CEFRLevel.A1.value
    user.level_offer_declined_round = 10
    await session.commit()
    await _answers(session, user, correct=MIN_ANSWERS, wrong=0)

    await decline_level(user, session)
    assert await should_offer_next_level(user, session) is None


# ============================================================================
# БЫСТРЫЙ ПУТЬ НОВИЧКА (15.10)
# ============================================================================
#
# Прод 15.10: новички, знающие язык, отвечали верно на всё и уходили после
# первых слов, не дождавшись двадцати ответов. Владелец: «2 круга с высокой
# точностью — явно знает», «сделай по-умному». Первые занятия судятся по
# одному: шесть ответов, не больше одной ошибки на семь.


@pytest.mark.asyncio
async def test_newcomer_is_offered_after_one_short_lesson(session, user):
    user.level = CEFRLevel.A1
    user.quizzes_passed = 1
    await _answers(session, user, correct=NEWCOMER_MIN_ANSWERS, wrong=1)

    assert await should_offer_next_level(user, session) == CEFRLevel.A2, (
        "новичок ответил 6 из 7 — A1 ему явно легко, а предложения нет"
    )


@pytest.mark.asyncio
async def test_newcomer_with_two_mistakes_stays(session, user):
    user.level = CEFRLevel.A1
    user.quizzes_passed = 1
    await _answers(session, user, correct=NEWCOMER_MIN_ANSWERS - 1, wrong=2)

    assert await should_offer_next_level(user, session) is None, (
        "две ошибки из семи — уровень ещё по силам, предлагать рано"
    )


@pytest.mark.asyncio
async def test_regular_user_needs_two_lessons(session, user):
    """После первых занятий — правило владельца: два занятия с высокой точностью."""
    user.level = CEFRLevel.A1
    user.quizzes_passed = NEWCOMER_LESSONS + 1
    await _answers(session, user, correct=NEWCOMER_MIN_ANSWERS + 1, wrong=0)

    assert await should_offer_next_level(user, session) is None, (
        "одного короткого занятия хватило обычному человеку — быстрый путь протёк"
    )


@pytest.mark.asyncio
async def test_first_lesson_is_short():
    from app.services.quiz_service import FIRST_LESSON_LENGTH, lesson_length

    class Person:
        quizzes_passed = 0
        quiz_word_count = 15

    assert lesson_length(Person()) == FIRST_LESSON_LENGTH == 7
    Person.quizzes_passed = 1
    assert lesson_length(Person()) == 15, "второе занятие — обычной длины"
    Person.quizzes_passed, Person.quiz_word_count = 0, 5
    assert lesson_length(Person()) == 5, "первое не длиннее выбранного"
