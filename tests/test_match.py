"""
Доска сопоставления: пять слов слева, их значения справа.

ЧТО ЗДЕСЬ ГЛАВНОЕ, И ЭТО НЕ РАСКЛАДКА

Доска легче карточки: из пяти пар последняя достаётся бесплатно,
предпоследняя — монеткой. Знание несут примерно три пары из пяти. Значит
если считать её наравне с карточкой, шкала «написанное» на домашнем экране
начнёт расти дёшево — а она честное зеркало, в этом весь её смысл.

Отсюда два правила, которые тесты и держат:

    в прогресс идут ТОЛЬКО пары, сошедшиеся с первой попытки,
    и НИКОГДА последняя сошедшаяся.

И третье, из требования владельца «они стоят не очевидно друг к другу»:
правая колонка — перестановка БЕЗ неподвижных точек. Обычного
перемешивания мало: у случайной перестановки пяти элементов хотя бы один
остаётся на своём месте примерно в 63% случаев, то есть на двух досках из
трёх человек получал бы готовый ответ.
"""

import random

import pytest

from app.database.enums import CEFRLevel, QuizMode
from app.database.models import UserWord, Word
from app.services.language_service import option_label, pair_from_user
from app.services.match_service import (
    BOARD_SIZE,
    LABEL_LIMIT,
    UNLOCK_CORRECT,
    deranged_order,
    pick_words,
    scored_pairs,
)
from tests.conftest import build_groups, make_word

# pytest.ini: asyncio_mode = auto — асинхронные тесты подхватываются сами, а
# общая пометка навешивалась бы и на синхронные проверки перестановки


# ============================================================================
# ПЕРЕСТАНОВКА БЕЗ СОВПАДЕНИЙ
# ============================================================================

def test_no_pair_stands_opposite_itself():
    """
    Ни одна пара не стоит напротив себя — иначе ответ подсказан.

    Прогон на тысяче досок, а не на одной: беда тут вероятностная, и
    единственная удачная выборка ничего не доказывает.
    """
    rng = random.Random(20261012)
    for _ in range(1000):
        order = deranged_order(BOARD_SIZE, rng)
        assert sorted(order) == list(range(BOARD_SIZE)), "перестановка потеряла пары"
        assert all(position != index for position, index in enumerate(order)), (
            f"пара стоит напротив себя: {order}"
        )


def test_plain_shuffle_would_not_have_been_enough():
    """
    Проверка проверки: обычное перемешивание действительно подсказывает.

    Без этого теста предыдущий выглядел бы придиркой. Замер: у случайной
    перестановки пяти элементов совпадение случается больше чем в половине
    случаев.
    """
    rng = random.Random(20261012)
    naive = list(range(BOARD_SIZE))
    giveaways = 0
    for _ in range(1000):
        rng.shuffle(naive)
        if any(position == index for position, index in enumerate(naive)):
            giveaways += 1

    assert giveaways > 500, (
        f"обычное перемешивание подсказало лишь {giveaways} раз из 1000 — "
        f"проверка на неподвижные точки, выходит, лишняя"
    )


def test_a_single_item_board_is_left_alone():
    """Из одного элемента перестановки без совпадений не бывает."""
    assert deranged_order(1) == [0]


# ============================================================================
# УЧЁТ: ЧТО ИДЁТ В ПРОГРЕСС
# ============================================================================

def test_every_pair_matched_on_the_first_try_is_counted():
    """
    Доска — пять ПОДВОПРОСОВ, и каждый считается как обычный вопрос:
    решение владельца «за вопрос 7 можно 5 баллов получить».

    Прежняя редакция вычитала ещё и последнюю сошедшуюся пару — она
    достаётся без выбора. Довод верен, но перевешен: промах теперь СТОИТ
    балла, и перебирать невыгодно, а своё правило у доски значило бы ещё
    одно число, которое разъедется.
    """
    counted = scored_pairs(first_try={0, 1, 2, 3, 4}, matched_order=[2, 0, 3, 1, 4])

    assert counted == {0, 1, 2, 3, 4}, "безошибочная доска даёт все пять"


def test_pair_found_after_a_miss_is_not_counted():
    """Пара, найденная после промаха, — это перебор, а не узнавание."""
    counted = scored_pairs(first_try={0, 2}, matched_order=[0, 1, 2, 3])

    assert counted == {0, 2} - {3}
    assert 1 not in counted and 3 not in counted


def test_nothing_is_counted_when_nothing_matched():
    """Пустая доска — пустой зачёт, а не ошибка."""
    assert scored_pairs(first_try=set(), matched_order=[]) == set()
    assert scored_pairs(first_try={0, 1}, matched_order=[]) == set()


def test_a_miss_costs_the_point():
    """
    Пара, найденная после промаха, в зачёт не идёт — и это именно то, что
    делает доску небесплатной. Перебирать наугад становится невыгодно.
    """
    counted = scored_pairs(first_try={0, 2, 4}, matched_order=[0, 1, 2, 3, 4])

    assert counted == {0, 2, 4}
    assert 1 not in counted and 3 not in counted


# ============================================================================
# ОТБОР СЛОВ
# ============================================================================

async def _seed(session, user, *, count: int, correct: int = UNLOCK_CORRECT,
                long_label: bool = False) -> None:
    for i in range(count):
        # Короткое немецкое слово и короткий перевод — иначе отбор по длине
        # их справедливо отбросит
        name = f"Haus{i:02d}" if not long_label else f"Sehrlangeswort{i:02d}"
        ru = f"дом{i:02d}" if not long_label else f"очень длинный перевод {i:02d}"
        session.add(make_word(name, level=CEFRLevel.A1, ru=ru))
    await build_groups(session, ["de"])

    from sqlalchemy import select

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    words = (await session.execute(select(Word))).scalars().all()
    for word in words:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            correct_streak=1, times_shown=max(correct, 1), times_correct=correct,
            learned=False,
        ))
    await session.commit()


async def test_board_takes_only_familiar_words(session, user):
    """
    Новому слову исключение не учит ничему: человек найдёт пару
    вычёркиванием и не запомнит её. Поэтому порог тот же, что у слуха.
    """
    await _seed(session, user, count=10, correct=0)

    picked = await pick_words(user, session, pair_from_user(user), level=CEFRLevel.A1)

    assert picked == [], "на доску попали слова без единого верного ответа"


async def test_board_is_full_when_there_is_material(session, user):
    await _seed(session, user, count=10)

    picked = await pick_words(user, session, pair_from_user(user), level=CEFRLevel.A1)

    assert len(picked) == BOARD_SIZE


async def test_long_labels_are_left_out(session, user):
    """
    Две колонки делят ширину экрана пополам. Слово, не влезающее в кнопку,
    едет на вторую строку, и решётка разваливается — доска перестаёт
    читаться как доска.
    """
    await _seed(session, user, count=10, long_label=True)

    picked = await pick_words(user, session, pair_from_user(user), level=CEFRLevel.A1)

    assert picked == [], f"длинные подписи прошли отбор: {len(picked)}"


async def test_every_label_on_the_board_fits(session, user):
    await _seed(session, user, count=12)

    pair = pair_from_user(user)
    picked = await pick_words(user, session, pair, level=CEFRLevel.A1)

    assert picked, "доска пуста — проверка вхолостую"
    for word in picked:
        assert len(option_label(word, pair.learning)) <= LABEL_LIMIT
        assert len(option_label(word, pair.native)) <= LABEL_LIMIT


async def test_duplicate_labels_never_share_a_board(session, user):
    """
    Две одинаковые подписи справа делают доску неразрешимой: верных
    ответов два, а засчитан будет один, и человек увидит «не пара» на
    совершенно верном выборе.
    """
    for i in range(8):
        # У всех разный немецкий, но ОДИН И ТОТ ЖЕ перевод
        session.add(make_word(f"Wort{i:02d}", level=CEFRLevel.A1, ru="дом"))
    await build_groups(session, ["de"])

    from sqlalchemy import select

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    for word in (await session.execute(select(Word))).scalars().all():
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            correct_streak=1, times_shown=2, times_correct=2, learned=False,
        ))
    await session.commit()

    pair = pair_from_user(user)
    picked = await pick_words(user, session, pair, level=CEFRLevel.A1)
    labels = [option_label(w, pair.native) for w in picked]

    assert len(labels) == len(set(labels)), f"подписи повторяются: {labels}"
    assert len(picked) == 1, "из восьми слов с одним переводом годится одно"


# ============================================================================
# КЛАВИАТУРА
# ============================================================================

def test_keyboard_is_two_columns():
    from app.bot.handlers.quiz.match import board_keyboard

    left = [f"l{i}" for i in range(5)]
    right = [f"r{i}" for i in range(5)]
    order = deranged_order(5, random.Random(1))

    rows = board_keyboard(left, right, order, [], "", 0).inline_keyboard

    assert len(rows) == 5, "рядов не пять"
    assert all(len(row) == 2 for row in rows), "это не две колонки"


def test_matched_cells_get_a_dead_callback():
    """
    Telegram не умеет неактивных кнопок: нажатие по сошедшейся паре придёт
    всё равно. Если дать ему живой callback, доска обработает его повторно.
    """
    from app.bot.handlers.quiz.match import CB_SPENT, board_keyboard

    left = [f"l{i}" for i in range(5)]
    right = [f"r{i}" for i in range(5)]
    order = deranged_order(5, random.Random(2))

    rows = board_keyboard(left, right, order, [0], "", 0).inline_keyboard
    spent = [b for row in rows for b in row if b.callback_data == CB_SPENT]

    assert len(spent) == 2, "у сошедшейся пары должны умереть ОБЕ половины"


def test_selection_is_marked_and_only_once():
    from app.bot.handlers.quiz.match import MARK_PICKED, board_keyboard

    left = [f"l{i}" for i in range(5)]
    right = [f"r{i}" for i in range(5)]
    order = deranged_order(5, random.Random(3))

    rows = board_keyboard(left, right, order, [], "l:2", 0).inline_keyboard
    marked = [b.text for row in rows for b in row if b.text.startswith(MARK_PICKED)]

    assert marked == [f"{MARK_PICKED}l2"], f"выбор помечен не там: {marked}"


def test_version_travels_in_every_callback():
    """
    Номер версии защищает от нажатий, сделанных быстрее, чем пришёл ответ.
    Без него второе нажатие обработает уже изменившуюся доску — и выглядело
    бы это как «кнопка сработала сама».
    """
    from app.bot.handlers.quiz.match import board_keyboard

    rows = board_keyboard(
        [f"l{i}" for i in range(3)], [f"r{i}" for i in range(3)],
        deranged_order(3, random.Random(4)), [], "", 7,
    ).inline_keyboard
    data = [b.callback_data for row in rows for b in row]

    assert all(d.endswith(":7") for d in data), f"версия не во всех кнопках: {data}"


# ============================================================================
# НАБОР СЛОВ — ТОТ ЖЕ, ЧТО У КРУГА
#
# Решение владельца: доска берёт слова из уровня и режима, как сам круг.
# Первая редакция смотрела только на уровень, и в режиме «по категории»
# доска молча расширялась на всю базу.
# ============================================================================

async def _mixed_base(session, user) -> None:
    """Слова двух уровней и двух категорий, все знакомые человеку."""
    from sqlalchemy import select
    from app.database.enums import WordCategory

    work = WordCategory.ARBEIT_BERUF.value
    food = WordCategory.ESSEN_TRINKEN.value
    for i in range(8):
        session.add(make_word(f"Arb{i:02d}", level=CEFRLevel.A1,
                              ru=f"раб{i:02d}", category=work))
        session.add(make_word(f"Ess{i:02d}", level=CEFRLevel.B1,
                              ru=f"еда{i:02d}", category=food))
    await build_groups(session, ["de"])

    for word in (await session.execute(select(Word))).scalars().all():
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            correct_streak=1, times_shown=2, times_correct=2, learned=False,
        ))
    await session.commit()


async def test_board_respects_the_level(session, user):
    await _mixed_base(session, user)
    user.quiz_mode = QuizMode.LEVEL
    user.level = CEFRLevel.A1
    await session.commit()

    picked = await pick_words(user, session, pair_from_user(user))

    assert picked, "доска пуста — проверка вхолостую"
    assert {w.level for w in picked} == {CEFRLevel.A1}, (
        f"в доску уровня A1 попали чужие: {[w.level for w in picked]}"
    )


async def test_board_respects_the_category_mode(session, user):
    """
    В режиме «по категории» доска берёт категорию, а НЕ уровень. Первая
    редакция в этом режиме брала всю базу: уровень она читала, а режим нет.
    """
    from app.database.enums import WordCategory

    await _mixed_base(session, user)
    user.quiz_mode = QuizMode.CATEGORY
    user.quiz_category = WordCategory.ESSEN_TRINKEN.value
    user.level = CEFRLevel.A1          # нарочно ЧУЖОЙ уровень
    await session.commit()

    picked = await pick_words(user, session, pair_from_user(user))

    assert picked, "доска пуста — проверка вхолостую"
    assert {w.category for w in picked} == {WordCategory.ESSEN_TRINKEN.value}
    # И уровень при этом не ограничивает: слова категории лежат на B1
    assert {w.level for w in picked} == {CEFRLevel.B1}


async def test_board_without_limits_in_all_words_mode(session, user):
    await _mixed_base(session, user)
    user.quiz_mode = QuizMode.ALL_WORDS
    user.level = CEFRLevel.A1
    await session.commit()

    picked = await pick_words(user, session, pair_from_user(user), size=10)

    levels = {w.level for w in picked}
    assert len(levels) > 1, (
        f"режим «все слова» ограничился одним уровнем: {levels}"
    )


# ============================================================================
# КОГДА ДОСКА ПОПАДАЕТСЯ В КРУГЕ
# ============================================================================

def test_board_stands_in_the_middle_of_the_round():
    """
    Не первым и не последним. Первым — потому что 9.5% кругов закрываются
    без единого ответа, и встречать человека незнакомым экраном нельзя, да
    и правило проекта требует первый вопрос текстовым. Последним — за ним
    идёт итог.
    """
    from app.services.match_service import board_slot

    for length in (5, 10, 15, 20, 25):
        slot = board_slot(length)
        assert 1 < slot < length, f"круг {length}: доска встала на {slot}"


def test_board_is_one_question_not_five():
    """
    Поправка владельца к моей ошибке. Первая редакция отдавала доске пять
    слотов ради правила «15 вопросов = 15 слов» — и счёт перескакивал с
    пятого вопроса на одиннадцатый. «Зачем ломать юзеру порядок 6 7 8?»

    Обещано пятнадцать ВОПРОСОВ. Доска — вопрос номер семь, внутри него
    пять подвопросов, и счёт остаётся непрерывным.
    """
    from app.services.match_service import board_slot

    assert board_slot(15) == 8


def _person(**kwargs):
    from app.database.models import User as U

    person = U(id=1, interface_language="ru", learning_lang="de",
               native_lang="ru", reverse_mode=False, level=CEFRLevel.A1)
    person.match_in_round = kwargs.get("match_in_round", True)
    person.quizzes_passed = kwargs.get("quizzes_passed", 0)
    return person


def test_board_is_offered_every_other_round():
    """
    Каждый круг — треть занятия всегда одно и то же. Чётность числа
    пройденных кругов даёт «через раз» бесплатно и детерминированно.
    """
    from app.services.match_service import BOARD_SIZE, should_insert_board

    plenty = BOARD_SIZE * 2
    assert should_insert_board(_person(quizzes_passed=0), 15, plenty)
    assert not should_insert_board(_person(quizzes_passed=1), 15, plenty)
    assert should_insert_board(_person(quizzes_passed=2), 15, plenty)


def test_board_needs_twice_its_size_in_words():
    """
    Ровно пяти годных слов мало: доски пошли бы одним набором, и человек
    заучил бы расположение кнопок вместо слов.
    """
    from app.services.match_service import BOARD_SIZE, should_insert_board

    assert not should_insert_board(_person(), 15, BOARD_SIZE)
    assert should_insert_board(_person(), 15, BOARD_SIZE * 2)


def test_board_stays_out_of_short_rounds():
    """В круге короче десяти доска съела бы половину."""
    from app.services.match_service import (
        BOARD_SIZE, MIN_ROUND_FOR_BOARD, should_insert_board,
    )

    plenty = BOARD_SIZE * 2
    assert not should_insert_board(_person(), MIN_ROUND_FOR_BOARD - 1, plenty)
    assert should_insert_board(_person(), MIN_ROUND_FOR_BOARD, plenty)


def test_switched_off_means_off():
    from app.services.match_service import BOARD_SIZE, should_insert_board

    assert not should_insert_board(
        _person(match_in_round=False), 15, BOARD_SIZE * 2
    )
