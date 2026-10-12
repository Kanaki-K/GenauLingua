"""
Домашний экран: три шкалы и прямой вход одним каналом.

Главное, что тут держится, — ЧИСЛИТЕЛЬ И ЗНАМЕНАТЕЛЬ ПРИХОДЯТ ИЗ ОДНОГО
НАБОРА СЛОВ. Это ровно та форма дефекта, которую проект ловил семь раз
(`ROADMAP.md` §6): проверка смотрит на одно поле, а меняется соседнее. Здесь
соседние — два множества слов: освоенные считаются по прогрессу, а полоса
рисуется от числа слов текущего режима. Разойдись они, и у всякого, кто
сменил уровень, полоса ушла бы за край: «342 из 300».

Второе — ПОРОГ ДОПУСКА НЕ ОБХОДИТСЯ прямым входом. Кнопка «🎧» не имеет
права выдать новичку вопросы о словах, которых он ни разу не видел: узнать
на слух то, чего не видел, нельзя, и остаётся жать наугад.
"""

import pytest

from app.bot.handlers.quiz.home import BAR_LENGTH, _bar
from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import UserWord
from app.services.language_service import pair_from_user
from app.services.quiz_service import (
    CHANNEL_MASTERY,
    CHANNEL_UNLOCK,
    get_channel_progress,
    get_user_progress_stats,
    pick_channel,
)
from tests.conftest import build_groups, make_word


# ============================================================================
# ПОЛОСА
# ============================================================================

def test_empty_bar_when_nothing_is_counted():
    assert _bar(0, 100) == "░" * BAR_LENGTH


def test_full_bar_when_everything_is_counted():
    assert _bar(100, 100) == "▓" * BAR_LENGTH


def test_bar_without_words_does_not_divide_by_zero():
    """
    Знаменатель бывает нулём: категория без слов на этой паре языков, режим
    «сложные» у человека без ошибок. Экран обязан нарисоваться пустым, а не
    упасть.
    """
    assert _bar(0, 0) == "░" * BAR_LENGTH


def test_bar_never_runs_past_its_length():
    """
    Страховка на случай, если числитель всё-таки обгонит знаменатель. Полоса
    длиннее остальных сломала бы выравнивание всего блока, а причину искали
    бы в подписях.
    """
    assert len(_bar(500, 100)) == BAR_LENGTH


# ============================================================================
# ТРИ ШКАЛЫ СЧИТАЮТСЯ ПО НАБОРУ СЛОВ ЗАНЯТИЯ
# ============================================================================

async def _seed(session, user, *, words_a1=3, words_b1=2):
    """Слова двух уровней: по ним и видно, держится ли ограничение."""
    for i in range(words_a1):
        session.add(make_word(f"Alpha{i}", level=CEFRLevel.A1))
    for i in range(words_b1):
        session.add(make_word(f"Beta{i}", level=CEFRLevel.B1))
    await build_groups(session, ["de"])


def _progress(user_id: int, word_id: int, **counters) -> UserWord:
    base = dict(
        user_id=user_id, word_id=word_id, learning_lang="de", correct_streak=0,
        times_shown=0, times_correct=0, learned=False,
        shown_audio=0, correct_audio=0, shown_speech=0, correct_speech=0,
    )
    base.update(counters)
    return UserWord(**base)


@pytest.mark.asyncio
async def test_scales_are_counted_inside_the_level_not_across_the_language(session, user):
    """
    Освоенное на ДРУГОМ уровне в шкалу текущего не попадает.

    Это и есть тот самый дефект, от которого тест поставлен: первая редакция
    считала все ряды `UserWord` по изучаемому языку, а полосу рисовала от
    числа слов уровня. Человек, пришедший с B1 на A1, получал бы пять
    освоенных слов из трёх.
    """
    # Слов на чужом уровне НАРОЧНО больше, чем на своём: тогда прежняя
    # формула не просто завышала счёт, а выдавала «4 из 2» — полосу за краем.
    # Замерено на этом самом посеве: прежняя формула 4, новая 1.
    await _seed(session, user, words_a1=2, words_b1=3)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL

    from sqlalchemy import select
    from app.database.models import Word

    rows = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    a1 = [w for w in rows if w.level == CEFRLevel.A1]
    b1 = [w for w in rows if w.level == CEFRLevel.B1]

    # Одно слово A1 освоено глазами, и ВСЕ слова B1 тоже
    session.add(_progress(user.id, a1[0].id, times_shown=5, times_correct=CHANNEL_MASTERY))
    for w in b1:
        session.add(_progress(user.id, w.id, times_shown=9, times_correct=CHANNEL_MASTERY))
    await session.commit()

    pair = pair_from_user(user)
    progress = await get_channel_progress(user.id, session, pair, level=CEFRLevel.A1)
    stats = await get_user_progress_stats(user.id, session, pair, level=CEFRLevel.A1)

    assert progress["text"] == 1, "B1 не имеет права попасть в шкалу A1"
    assert progress["text"] <= stats["total_words"], "полоса ушла за край"


@pytest.mark.asyncio
async def test_three_channels_are_counted_apart(session, user):
    """
    Три шкалы — три разных навыка. Слово, освоенное на слух, в текстовую
    шкалу не попадает, и наоборот.
    """
    await _seed(session, user, words_a1=3, words_b1=0)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL

    from sqlalchemy import select
    from app.database.models import Word

    words = (await session.execute(select(Word).order_by(Word.id))).scalars().all()

    # Первое — только глазами, второе — только на слух, третье — только вслух.
    # Итог всегда включает канальные попадания, поэтому times_correct равен
    # им: текстовый канал считается вычитанием.
    session.add(_progress(user.id, words[0].id, times_shown=4, times_correct=CHANNEL_MASTERY))
    session.add(_progress(
        user.id, words[1].id, times_shown=4, times_correct=CHANNEL_MASTERY,
        shown_audio=4, correct_audio=CHANNEL_MASTERY,
    ))
    session.add(_progress(
        user.id, words[2].id, times_shown=4, times_correct=CHANNEL_MASTERY,
        shown_speech=4, correct_speech=CHANNEL_MASTERY,
    ))
    await session.commit()

    progress = await get_channel_progress(
        user.id, session, pair_from_user(user), level=CEFRLevel.A1
    )

    assert progress["text"] == 1
    assert progress["audio"] == 1
    assert progress["speech"] == 1


@pytest.mark.asyncio
async def test_unlock_count_uses_its_own_threshold_not_mastery(session, user):
    """
    «Допущено к каналу» и «освоено каналом» — разные числа с разными порогами.

    Домашний экран спрашивает первое, прежде чем запускать занятие одним
    каналом. Спроси он второе — прямой вход открывался бы много позже, чем
    слова на самом деле готовы.
    """
    await _seed(session, user, words_a1=2, words_b1=0)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL

    from sqlalchemy import select
    from app.database.models import Word

    words = (await session.execute(select(Word).order_by(Word.id))).scalars().all()

    # Один верный ответ: к слуху допущено, освоением ещё не считается
    for w in words:
        session.add(_progress(
            user.id, w.id, times_shown=1,
            times_correct=CHANNEL_UNLOCK[QuizChannel.AUDIO],
        ))
    await session.commit()

    progress = await get_channel_progress(
        user.id, session, pair_from_user(user), level=CEFRLevel.A1
    )

    assert progress["ready_audio"] == 2, "оба слова допущены к слуху"
    assert progress["audio"] == 0, "но ни одно не освоено на слух"


# ============================================================================
# ПРЯМОЙ ВХОД ОДНИМ КАНАЛОМ УВАЖАЕТ ПОРОГ ДОПУСКА
# ============================================================================

@pytest.mark.asyncio
async def test_preferred_channel_waits_for_the_unlock(session, user):
    """
    Слово, которое человек ни разу не отвечал верно, не придёт на слух даже
    по прямому входу. Иначе кнопка «🎧» на свежем счёте выдала бы пятнадцать
    загадок подряд.
    """
    await _seed(session, user, words_a1=1, words_b1=0)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.audio_enabled = True
    user.quiz_channels = "t"       # состав занятия тут ни при чём
    await session.commit()

    from sqlalchemy import select
    from app.database.models import Word

    word = (await session.execute(select(Word))).scalars().first()

    channel = await pick_channel(
        session, user, word, "de", prefer=QuizChannel.AUDIO
    )
    assert channel is QuizChannel.TEXT, "порог допуска обойдён"


@pytest.mark.asyncio
async def test_preferred_channel_wins_once_the_word_is_unlocked(session, user):
    """А вот допущенное слово приходит именно запрошенным каналом."""
    await _seed(session, user, words_a1=1, words_b1=0)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.audio_enabled = True
    user.quiz_channels = "t"

    from sqlalchemy import select
    from app.database.models import Word

    word = (await session.execute(select(Word))).scalars().first()
    session.add(_progress(
        user.id, word.id, times_shown=3,
        times_correct=CHANNEL_UNLOCK[QuizChannel.AUDIO],
    ))
    await session.commit()

    channel = await pick_channel(
        session, user, word, "de", prefer=QuizChannel.AUDIO
    )
    assert channel is QuizChannel.AUDIO


@pytest.mark.asyncio
async def test_disabled_audio_cancels_the_preferred_channel(session, user):
    """
    Выключенная озвучка отменяет слух и речь, что бы ни просил прямой вход:
    у вопроса на слух самого слова на экране нет, его заменяет клип.
    """
    await _seed(session, user, words_a1=1, words_b1=0)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.audio_enabled = False

    from sqlalchemy import select
    from app.database.models import Word

    word = (await session.execute(select(Word))).scalars().first()
    session.add(_progress(user.id, word.id, times_shown=9, times_correct=9))
    await session.commit()

    for channel in (QuizChannel.AUDIO, QuizChannel.SPEECH):
        picked = await pick_channel(session, user, word, "de", prefer=channel)
        assert picked is QuizChannel.TEXT, f"{channel} прошёл без озвучки"


# ============================================================================
# СБОРКА ЭКРАНА
# ============================================================================

@pytest.mark.asyncio
async def test_home_renders_on_an_empty_account(session, user):
    """
    Человек без единого ответа тоже должен увидеть экран: три пустые полосы,
    а не ошибку. Это первый экран после онбординга.
    """
    from app.bot.handlers.quiz.home import build_home

    await _seed(session, user, words_a1=2, words_b1=0)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    text, keyboard = await build_home(user, session)

    assert "░" in text, "полос нет вовсе"
    assert "▓" not in text, "на пустом счёте нечему быть закрашенным"
    assert len(keyboard.inline_keyboard[1]) == 3, "три прямых входа по каналам"


@pytest.mark.asyncio
async def test_home_labels_are_padded_to_one_width(session, user):
    """
    Подписи выравниваются по самой длинной из трёх — иначе полосы разъезжаются
    лестницей, и шкалы перестают сравниваться взглядом, а в этом весь смысл.

    Одна шкала нарочно ЗАКРАШЕНА, а две пусты. Пустой счёт эту проверку не
    держит: у него все три полосы начинаются с «░», и выравнивание сошлось бы
    даже при разной длине подписей. Приёмка на живых людях на этом и
    попалась — искала начало полосы по первому пустому знаку, а у закрашенной
    перед ним стоят «▓».
    """
    from app.bot.handlers.quiz.home import build_home

    await _seed(session, user, words_a1=2, words_b1=0)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL

    from sqlalchemy import select
    from app.database.models import Word

    word = (await session.execute(select(Word))).scalars().first()
    session.add(_progress(
        user.id, word.id, times_shown=5, times_correct=CHANNEL_MASTERY
    ))
    await session.commit()

    text, _ = await build_home(user, session)
    block = text.split("<code>")[1].split("</code>")[0]
    lines = block.splitlines()
    starts = [min(i for i, ch in enumerate(line) if ch in "▓░") for line in lines]

    assert "▓" in block, "ни одна полоса не закрашена — проверка вхолостую"
    assert len(set(starts)) == 1, f"полосы начинаются в разных местах: {starts}"


@pytest.mark.asyncio
async def test_every_button_has_a_handler_that_answers_it(session, user):
    """
    У каждой кнопки экрана есть обработчик, который её ловит.

    Дефект, от которого стоит этот тест, в проекте уже случался дважды и оба
    раза выглядел одинаково: кнопка есть, нажатие уходит в пустоту, бот
    молчит. Один раз надпись реплай-кнопки вписали в фильтр руками и только
    по-русски; другой раз обработчик перехватывал событие и ничего не делал.
    Проверка сверяет не текст, а СОПОСТАВЛЕНИЕ: каждое `callback_data`
    клавиатуры должно пройти фильтры хотя бы одного зарегистрированного
    обработчика.
    """
    from app.bot.handlers.quiz.home import build_home, router

    await _seed(session, user, words_a1=2, words_b1=0)
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    _, keyboard = await build_home(user, session)
    data = [b.callback_data for row in keyboard.inline_keyboard for b in row]
    assert len(data) == 4, f"кнопок стало {len(data)}, проверка устарела"

    # Фильтры aiogram — вызываемые объекты над объектом события. Полноценный
    # CallbackQuery тут не нужен: все фильтры экрана смотрят только на .data
    class _Probe:
        def __init__(self, value: str) -> None:
            self.data = value

    handlers = router.callback_query.handlers
    assert handlers, "у экрана нет ни одного обработчика нажатий"

    for value in data:
        probe = _Probe(value)
        matched = any(
            all(f.callback(probe) for f in handler.filters)
            for handler in handlers
        )
        assert matched, f"нажатие {value!r} не ловит ни один обработчик"
