"""
🧱 «Собираю» — шестая игра: собрать пример из кнопок-слов.

Тесты идут слоями, как и сама игра:

    правила       годность примера, ловушки, сетка, сравнение — без базы
    подбор        порог допуска, годность по данным, чередование, откат
    учёт          счётчики слова, месячный балл обоими путями, перепривязка
    экраны        настройки, шкалы, строка «Грамматика»
    нажатия       настоящий диспетчер: сетка, ⌫, «Проверить», двойные и
                  устаревшие нажатия, ошибка в «Повторить ошибки»
"""

import random
from datetime import timedelta

import pytest
from sqlalchemy import func, select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, QuizChannel, QuizMode, counted_channels
from app.database.models import MonthlyStats, QuizQuestion, QuizSession, UserWord, Word
from app.services import build_service as bs
from app.services.language_service import LanguagePair
from tests.conftest import build_groups, make_word
from tests.scenario import make_bot, make_dispatcher, press, reset_state

PAIR = LanguagePair(learning="de", native="ru")


class _W:
    """Слово без базы: только то, что читает сборка."""

    def __init__(self, de: str, ru: str = "Собака играет в саду", level=CEFRLevel.A1):
        self.example_de = de
        self.example_ru = ru
        self.level = level
        self.id = 1


# ============================================================================
# ПРАВИЛА
# ============================================================================

def test_tokens_drop_punctuation_but_keep_word_inner_marks():
    assert bs.tokens("Nach dem Essen, gehen wir raus!") == [
        "Nach", "dem", "Essen", "gehen", "wir", "raus"]
    # Тире — не слово; апостроф и дефис внутри слова — часть слова
    assert bs.tokens("Германия — это демократия") == ["Германия", "это", "демократия"]
    assert bs.tokens("I don't read e-mails.") == ["I", "don't", "read", "e-mails"]


@pytest.mark.parametrize("sentence,fits", [
    ("Er ist Tischler", True),                                  # 3 — нижняя граница
    ("Ich gehe", False),                                        # 2
    ("eins zwei drei vier fünf sechs sieben acht neun", True),        # 9
    ("eins zwei drei vier fünf sechs sieben acht neun zehn", False),  # 10 — с ловушкой 11 кнопок
    ("Hallo , Welt", False),                                    # запятая не слово
])
def test_a_sentence_fits_by_its_word_count(sentence, fits):
    assert bs.fits(_W(sentence), PAIR) is fits


def test_without_a_translation_there_is_nothing_to_build():
    assert not bs.fits(_W("Er ist Tischler", ru=""), PAIR)


def test_traps_are_forms_of_the_sentence_words_first():
    """Владелец: «der→den/dem, wir→ihr, ist→sind»."""
    target = ["Er", "ist", "der", "Tischler"]
    traps, sources = bs.pick_distractors(target, "de", [], random.Random(1), 4)
    assert sources == {"similar": 4}
    siblings = {"den", "dem", "des", "die", "das", "sind", "bin", "bist", "seid",
                "Ich", "Du", "Sie", "Es", "Wir", "Ihr"}
    assert set(traps) <= siblings, traps


def test_a_trap_never_looks_like_a_word_of_the_sentence():
    """Две одинаковые кнопки сделали бы проверку неоднозначной."""
    target = ["Die", "Katze", "sieht", "die", "Maus"]
    for seed in range(200):
        traps, _ = bs.pick_distractors(target, "de", ["Katze", "katze", "Hund"],
                                       random.Random(seed))
        folded = {bs.fold(t) for t in target}
        assert not {bs.fold(t) for t in traps} & folded, traps
        assert len({bs.fold(t) for t in traps}) == len(traps), "ловушки повторились"


async def test_the_first_capital_gives_nothing_away():
    """
    «Der» с большой буквы среди «die», «den» сразу говорит, что стоит
    первым. Первое слово из закрытых списков — на кнопке строчным, и
    ловушки к нему тоже; существительное и «I» не трогаются.
    """
    for seed in range(50):
        puzzle = await bs.make_puzzle(
            None, _W("Der Baum ist grün", level=CEFRLevel.C1), PAIR, random.Random(seed))
        assert puzzle.target[0] == "der"
        assert not [t for t in puzzle.tiles if t[0].isupper() and t != "Baum"], puzzle.tiles
        # Проверка регистр первого слова не сравнивает, эталон — из базы
        assert bs.judge(puzzle.target, ["der", "Baum", "ist", "grün"], "de").correct
        assert puzzle.sentence == "Der Baum ist grün"

    assert bs.first_on_tile(["Mathematik", "ist", "toll"], "de")[0] == "Mathematik"
    assert bs.first_on_tile(["I", "see", "you"], "en")[0] == "I"
    assert bs.first_on_tile(["İçin", "geldi", "o"], "tr")[0] == "için"


@pytest.mark.parametrize("lang,words,shown", [
    # Проба 14.10: первое слово было единственной заглавной кнопкой
    ("ru", ["Полиция", "конфисковала", "документы"], "полиция"),
    ("uk", ["Корови", "паслися", "на", "пасовищі"], "корови"),
    ("pl", ["Cena", "jest", "do", "negocjacji"], "cena"),
    ("tr", ["Masa", "örtüsü", "güzel"], "masa"),
    ("tr", ["Işık", "yanıyor", "şimdi"], "ışık"),
    ("en", ["That's", "very", "far", "away"], "that's"),
    # Не трогаются: аббревиатура, турецкое имя с падежом, «I»
    ("en", ["USA", "is", "big"], "USA"),
    ("tr", ["İstanbul'da", "yaşıyorum", "şimdi"], "İstanbul'da"),
    ("en", ["I", "am", "here"], "I"),
])
def test_first_word_never_gives_away_the_start(lang, words, shown):
    assert bs.first_on_tile(words, lang)[0] == shown


@pytest.mark.parametrize("level,traps", [
    (CEFRLevel.A1, 2), (CEFRLevel.A2, 3), (CEFRLevel.B1, 3),
    (CEFRLevel.B2, 4), (CEFRLevel.C1, 5), (CEFRLevel.C2, 5),
])
def test_traps_grow_with_the_level(level, traps):
    """Лестница: «многие примеры A1 реально простые» — владелец."""
    assert bs.distractor_count(4, level) == traps
    # длинной фразе — меньше, но не меньше одной, и кнопок не больше 12
    assert bs.distractor_count(bs.MAX_WORDS, level) == min(traps, bs.MAX_TILES - bs.MAX_WORDS)
    assert bs.distractor_count(11, level) == 1


@pytest.mark.parametrize("lang,target,never", [
    ("uk", ["Ми", "живемо", "в", "місті"], {"у"}),          # в/у — оба верны
    ("en", ["I", "see", "the", "dog"], {"a", "an"}),         # артикль с русского не виден
    ("de", ["Ich", "komme", "aus", "Berlin"], {"von"}),
    ("tr", ["Ali", "ve", "Ayşe", "geldi"], {"ile"}),
])
def test_interchangeable_words_are_never_traps(lang, target, never):
    """
    Ловушка, которая тоже верна, хуже отсутствия ловушки: человек собрал
    правильную фразу, а бот засчитал ошибку.
    """
    for seed in range(300):
        traps, _ = bs.pick_distractors(target, lang, [], random.Random(seed))
        assert not {bs.fold(t) for t in traps} & {bs.fold(n) for n in never}, traps


def test_foreign_examples_fill_in_when_the_lists_run_dry():
    traps, sources = bs.pick_distractors(["Ali", "geldi", "dün"], "xx",
                                         ["Haus", "Auto", "Ali"], random.Random(1), 2)
    assert sources == {"foreign": 2}
    assert "Ali" not in traps


@pytest.mark.parametrize("words", range(bs.MIN_WORDS, bs.MAX_WORDS + 1))
@pytest.mark.parametrize("level", list(CEFRLevel))
def test_the_grid_never_exceeds_twelve_and_keeps_a_trap(words, level):
    count = bs.distractor_count(words, level)
    assert words + count <= bs.MAX_TILES
    assert 1 <= count <= bs.MAX_DISTRACTORS


def test_tiles_never_come_in_sentence_order():
    """У фразы из трёх слов без проверки порядок совпадал бы в 1 случае из 6."""
    target = ["Er", "ist", "Tischler"]
    for seed in range(300):
        tiles = bs.shuffle_tiles(target, [], random.Random(seed))
        assert tiles != target


def test_rows_narrow_for_long_words():
    assert bs.row_width(["der", "Hund", "bellt"]) == 4
    assert bs.row_width(["der", "Straßenbahn"]) == 3
    assert bs.row_width(["die", "Bundesregierung"]) == 2


async def test_a_puzzle_holds_every_word_plus_traps():
    puzzle = await bs.make_puzzle(
        None, _W("Nach dem Essen gehen wir raus", "После еды мы идём гулять"),
        PAIR, random.Random(5))
    # «Nach» — предлог из закрытых списков, на кнопке строчным
    assert puzzle.target == ["nach", "dem", "Essen", "gehen", "wir", "raus"]
    assert sorted(puzzle.tiles) == sorted(puzzle.target + puzzle.distractors)
    assert len(puzzle.distractors) == 2, "A1 — две ловушки"
    assert puzzle.translation == "После еды мы идём гулять"


class TestJudge:
    T = ["Nach", "dem", "Essen", "gehen", "wir", "raus"]

    def test_exact_is_correct(self):
        v = bs.judge(self.T, list(self.T), "de")
        assert v.correct and all(v.marks)

    def test_the_first_word_case_does_not_matter(self):
        """«Wir gehen raus» и «Raus gehen wir» — порядок, а не регистр."""
        target = ["Wir", "gehen", "raus"]
        assert bs.judge(target, ["Wir", "gehen", "raus"], "de").correct
        v = bs.judge(target, ["raus", "gehen", "Wir"], "de")
        assert v.same_words and not v.correct

    def test_other_case_is_a_different_word(self):
        """В немецком «Essen» и «essen» — разные слова."""
        v = bs.judge(self.T, ["Nach", "dem", "essen", "gehen", "wir", "raus"], "de")
        assert not v.correct and not v.same_words
        assert v.marks == [True, True, False, True, True, True]
        assert v.extra == ["essen"] and v.missing == ["Essen"]

    def test_same_words_other_order_is_its_own_verdict(self):
        v = bs.judge(self.T, ["Nach", "dem", "Essen", "wir", "gehen", "raus"], "de")
        assert v.same_words and not v.correct
        assert v.marks == [True, True, True, False, False, True]

    def test_a_trap_is_named_as_extra(self):
        v = bs.judge(self.T, ["Nach", "den", "Essen", "gehen", "wir", "raus"], "de")
        assert v.extra == ["den"] and v.missing == ["dem"]
        assert not v.same_words

    def test_repeated_words_are_interchangeable(self):
        target = ["Die", "Katze", "sieht", "die", "Maus"]
        assert bs.judge(target, ["Die", "Katze", "sieht", "die", "Maus"], "de").correct


# ============================================================================
# ПОДБОР
# ============================================================================

def _fit(word: Word, n: int) -> Word:
    # Пять слов: человек сценариев — A1, а на A1 сборка берёт фразы до пяти
    # слов (`build_service.EASY_MAX_WORDS`, патч 2.1)
    word.example_de = f"Der Hund {word.word_de} spielt heute"
    word.example_ru = f"Собака {n} играет сегодня"
    return word


async def _seed(session, user, *, n=60, fit=True, correct=2, channels="tasrb",
                audio=False):
    for i in range(n):
        word = make_word(f"Wort{i:03d}", level=CEFRLevel.A1, ru=f"слово{i:03d}")
        session.add(_fit(word, i) if fit else word)
    await build_groups(session, ["de"])
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = 15
    user.audio_enabled = audio
    user.quiz_channels = channels
    user.quizzes_passed = 2  # не новичок: у новичка первое занятие короче (7)
    await session.commit()
    words = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    if correct:
        for word in words[:40]:
            session.add(UserWord(
                user_id=user.id, word_id=word.id, learning_lang="de",
                times_shown=correct, times_correct=correct, correct_streak=1,
                learned=False, last_seen_at=utcnow() - timedelta(days=30),
            ))
        await session.commit()
    return words


async def test_build_opens_after_two_correct_like_speech(session, user):
    """Порог — одно правило на производство: речь и сборка вместе."""
    from app.services.quiz_service import CHANNEL_UNLOCK, pick_channel

    assert CHANNEL_UNLOCK[QuizChannel.BUILD] == CHANNEL_UNLOCK[QuizChannel.SPEECH] == 2

    words = await _seed(session, user, correct=1, channels="b")
    got = await pick_channel(session, user, words[0], "de", recent=["t", "t"])
    assert got is QuizChannel.TEXT, "сборка открылась после одного верного"


async def test_build_is_not_given_to_a_word_without_a_sentence(session, user):
    from app.services.quiz_service import pick_channel

    words = await _seed(session, user, fit=False, channels="b")
    got = await pick_channel(session, user, words[0], "de", recent=["t", "t"])
    assert got is QuizChannel.TEXT


async def test_the_build_button_gives_builds(session, user):
    """Прямой вход «Собираю»: слова, готовые к сборке, приходят сборкой."""
    from app.services.quiz_service import generate_question

    await _seed(session, user)
    used, recent = [], []
    for _ in range(5):
        q = await generate_question(session, user, exclude_ids=used,
                                    recent_channels=recent,
                                    prefer_channel=QuizChannel.BUILD)
        used.append(q["correct_word"].id)
        recent.append(q["channel"].value)
        assert q["channel"] is QuizChannel.BUILD
        assert len(q["options"]) == len(q["build"].tiles) <= bs.MAX_TILES


async def test_a_forced_build_on_a_short_sentence_falls_back_to_a_card(session, user):
    """Откат, как у слуха без созвучных: слово не теряется, игра другая."""
    from app.services.quiz_service import generate_question

    await _seed(session, user, fit=False)
    q = await generate_question(session, user, channel=QuizChannel.BUILD)
    assert q["channel"] is QuizChannel.TEXT and len(q["options"]) == 4


async def test_build_takes_its_turn_in_the_round(session, user):
    """Чередование мест отработки — общим правилом, сборка в нём своя."""
    from app.services.quiz_service import generate_question

    await _seed(session, user, correct=3)
    used, recent = [], []
    for number in range(1, 16):
        q = await generate_question(session, user, exclude_ids=used,
                                    recent_channels=recent, round_length=15,
                                    question_number=number)
        used.append(q["correct_word"].id)
        recent.append(q["channel"].value)
    assert "b" in recent, "".join(recent)
    assert "bb" not in "".join(recent), "две сборки подряд"


async def test_a_switched_off_build_never_comes(session, user):
    from app.services.quiz_service import _rotation, generate_question

    await _seed(session, user, correct=3, channels="tasr")
    assert QuizChannel.BUILD not in _rotation(user, [], [], position=1, round_length=15)
    used, recent = [], []
    for number in range(1, 16):
        q = await generate_question(session, user, exclude_ids=used,
                                    recent_channels=recent, round_length=15,
                                    question_number=number)
        used.append(q["correct_word"].id)
        recent.append(q["channel"].value)
    assert "b" not in recent


def test_build_does_not_need_sound():
    """В отличие от «Слушаю» и «Говорю», выключенная озвучка сборку не отнимает."""
    from app.services.quiz_service import NEEDS_AUDIO, enabled_channels

    class U:
        quiz_channels = "tasrb"
        audio_enabled = False

    assert QuizChannel.BUILD not in NEEDS_AUDIO
    assert QuizChannel.BUILD in enabled_channels(U())


# ============================================================================
# УЧЁТ
# ============================================================================

def test_every_counted_channel_has_columns_and_a_price():
    """Правило вместо списка: канал без колонки или цены падает здесь."""
    for channel in counted_channels():
        assert hasattr(UserWord, f"shown_{channel.key}")
        assert hasattr(UserWord, f"correct_{channel.key}")
        assert hasattr(MonthlyStats, f"correct_{channel.key}")
        MonthlyStats.points_for(channel)
    assert MonthlyStats.points_for(QuizChannel.BUILD) == MonthlyStats.POINTS_SPEECH == 3


def test_a_build_is_worth_three_and_is_not_a_card():
    stat = MonthlyStats(total_correct=10, total_questions=10, correct_build=4,
                        correct_audio=0, correct_speech=0, correct_reverse=0,
                        monthly_quizzes=0, monthly_reverse=0, monthly_words=0,
                        monthly_streak=0, monthly_avg_percent=0, report_bonus=0)
    # 6 карточек × 1 + 4 сборки × 3
    assert stat.calculate_monthly_score() == 18


async def test_progress_counts_the_build_in_its_own_columns(session, user):
    from app.services.quiz_service import update_word_progress

    words = await _seed(session, user, n=3, correct=0)
    await update_word_progress(user.id, words[0].id, True, session, "de",
                               channel=QuizChannel.BUILD)
    await update_word_progress(user.id, words[0].id, False, session, "de",
                               channel=QuizChannel.BUILD)
    row = (await session.execute(select(UserWord))).scalar_one()
    assert (row.shown_build, row.correct_build) == (2, 1)
    assert (row.shown_text, row.correct_text) == (0, 0), "сборка ушла в карточку"


async def test_the_month_counts_builds_both_ways(session, user):
    """Инкремент по занятию и полный пересчёт — одно число."""
    from app.services.monthly_leaderboard_service import (
        get_or_create_current_season, update_monthly_stats,
    )

    words = await _seed(session, user, n=3, correct=0)
    await get_or_create_current_season(session)
    now = utcnow()
    quiz = QuizSession(user_id=user.id, level=CEFRLevel.A1, learning_lang="de",
                       native_lang="ru", is_reverse=False, total_questions=3,
                       answered_questions=3, correct_answers=2, is_completed=True,
                       started_at=now, completed_at=now, quiz_mode="level")
    session.add(quiz)
    await session.commit()
    for word, ok in zip(words, (True, True, False)):
        session.add(QuizQuestion(session_id=quiz.id, word_id=word.id, is_correct=ok,
                                 answered_at=now, channel=QuizChannel.BUILD.value))
    await session.commit()

    stat = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
    assert stat.correct_build == 2
    incremental = stat.monthly_score

    stat = await update_monthly_stats(user.id, session, force_full_recalc=True)
    assert stat.correct_build == 2
    assert stat.monthly_score == incremental


async def test_the_remap_keeps_build_counters(session, user):
    """Перепривязка склеивает `shown_`/`correct_` по префиксу — и сборку тоже."""
    from app.services.word_groups import remap_user_progress_to_canonical
    from tests.conftest import build_groups as rebuild

    session.add_all([
        make_word("Meeting", en="meeting", frequency_rank=10),
        make_word("Sitzung", en="meeting", frequency_rank=20),
    ])
    await rebuild(session, ["en"])
    words = {w.word_de: w for w in (await session.execute(select(Word))).scalars().all()}
    session.add_all([
        UserWord(user_id=user.id, word_id=words["Meeting"].id, learning_lang="en",
                 times_shown=3, times_correct=2, shown_build=3, correct_build=2),
        UserWord(user_id=user.id, word_id=words["Sitzung"].id, learning_lang="en",
                 times_shown=2, times_correct=1, shown_build=2, correct_build=1),
    ])
    await session.commit()
    uid = user.id
    await session.run_sync(lambda s: remap_user_progress_to_canonical(s.connection()))
    await session.commit()
    session.expire_all()
    row = (await session.execute(select(UserWord).where(UserWord.user_id == uid))).scalar_one()
    assert (row.shown_build, row.correct_build) == (5, 3)


async def test_repair_puts_builds_back_from_the_answers(session, user):
    """Починка учёта ставит колонку сборки по строкам ответов, как остальные."""
    from app.scripts.repair_accounting import repair_monthly
    from app.services.monthly_leaderboard_service import (
        get_or_create_current_season, update_monthly_stats,
    )

    words = await _seed(session, user, n=2, correct=0)
    await get_or_create_current_season(session)
    now = utcnow()
    quiz = QuizSession(user_id=user.id, level=CEFRLevel.A1, learning_lang="de",
                       native_lang="ru", is_reverse=False, total_questions=2,
                       answered_questions=2, correct_answers=2, is_completed=True,
                       started_at=now, completed_at=now, quiz_mode="level")
    session.add(quiz)
    await session.commit()
    for word in words:
        session.add(QuizQuestion(session_id=quiz.id, word_id=word.id, is_correct=True,
                                 answered_at=now, channel=QuizChannel.BUILD.value))
    await session.commit()
    stat = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
    stat.correct_build = 0
    await session.commit()

    await repair_monthly(session, apply=True, all_seasons=False)
    await session.refresh(stat)
    assert stat.correct_build == 2


# ============================================================================
# ЭКРАНЫ
# ============================================================================

async def test_home_has_a_build_scale_last(session, user):
    from app.bot.handlers.quiz.home import _SCALES, build_home

    await _seed(session, user, n=5, correct=0)
    assert _SCALES[-1][0] is QuizChannel.BUILD
    text, _ = await build_home(user, session)
    assert "Собираю" in text


async def test_grammar_line_shows_builds_only_when_there_were_any(session, user):
    from app.bot.handlers.quiz.stats import build_stats_text

    words = await _seed(session, user, n=5, correct=0)
    assert "Грамматика" not in await build_stats_text(user, session)

    session.add(UserWord(user_id=user.id, word_id=words[0].id, learning_lang="de",
                         times_shown=4, times_correct=3, shown_build=4, correct_build=3))
    await session.commit()
    assert "Грамматика: верно 3 из 4" in await build_stats_text(user, session)


async def test_build_can_be_switched_off_and_on_in_settings(session, user):
    await _seed(session, user, n=5, correct=0, channels="tasrb")
    bot, rec = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)

    await dp.feed_update(bot, press(user.id, "settings_channels"))
    assert "channel_toggle_b" in rec.buttons()
    assert "✓ 🧱 Собираю" in rec.button_texts()

    await dp.feed_update(bot, press(user.id, "channel_toggle_b"))
    await session.refresh(user)
    assert "b" not in user.quiz_channels
    await dp.feed_update(bot, press(user.id, "channel_toggle_b"))
    await session.refresh(user)
    assert "b" in user.quiz_channels


# ============================================================================
# НАЖАТИЯ: настоящий диспетчер
# ============================================================================

async def _start_build(session, user, rec, dp, bot):
    """Вход «Собираю» с главной — первым же вопросом сборка."""
    await _seed(session, user)
    await dp.feed_update(bot, press(user.id, f"home_learn_{QuizChannel.BUILD.value}"))
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    data = await context.get_data()
    assert data.get("channel") == "b", rec.alerts()
    return context, data


async def _tap(dp, bot, user, context, index):
    data = await context.get_data()
    await dp.feed_update(bot, press(
        user.id, f"bd:t:{index}:{data['build_word']}:{data['build_version']}"))


async def _assemble(dp, bot, user, context, words):
    data = await context.get_data()
    taken: set[int] = set(data["build_picked"])
    for word in words:
        data = await context.get_data()
        index = next(i for i, t in enumerate(data["build_tiles"])
                     if t == word and i not in taken)
        taken.add(index)
        await _tap(dp, bot, user, context, index)


async def _check(dp, bot, user, context):
    data = await context.get_data()
    await dp.feed_update(bot, press(
        user.id, f"bd:check:{data['build_word']}:{data['build_version']}"))


async def _rows(session, session_id):
    return (await session.execute(
        select(QuizQuestion).where(QuizQuestion.session_id == session_id)
    )).scalars().all()


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


async def test_the_question_screen(session, user, stage):
    dp, bot, rec = stage
    context, data = await _start_build(session, user, rec, dp, bot)

    text = rec.last_text()
    assert "1 / 15 · 🧱" in text
    assert data["build_translation"] in text, "фразы на родном нет"
    # Длина фразы — пропусками ▢ в строке текста
    assert text.count("▢") == len(data["build_target"])
    assert data["build_sentence"] not in text, "эталон на экране"
    tiles = [b for b in rec.buttons() if b.startswith("bd:t:")]
    assert len(tiles) == len(data["build_tiles"]) <= 12
    assert not any(b.startswith("bd:check") for b in rec.buttons()), "проверять нечего"


async def test_placed_words_leave_the_grid_and_spare_words_leave_at_the_end(
    session, user, stage
):
    """
    Два живых теста владельца 14.10. Первый: «после выбранного слова
    ставит точку, а 3, которые предложило с самого начала, висят как
    бесполезные». Второй: собранное кнопками-местами — «половина из них
    пустые клетки… было хорошо, когда заполнялся текст на экране… слева и
    справа максимум по 5». Теперь: собранное — строкой в тексте, нажатое
    уходит из сетки, сетка в две колонки, не больше десяти, после сборки —
    только «⌫» и «Проверить».
    """
    from app.services.build_service import GRID_COLUMNS, MAX_TILES

    dp, bot, rec = stage
    context, data = await _start_build(session, user, rec, dp, bot)
    target = data["build_target"]
    assert len(data["build_tiles"]) <= MAX_TILES == 10

    await _assemble(dp, bot, user, context, target[:2])
    buttons = rec.buttons()
    assert "bd:spent" not in buttons and "bd:idle" not in buttons, "пустые кнопки в сетке"
    pool = [b for b in buttons if b.startswith("bd:t:")]
    assert len(pool) == len(data["build_tiles"]) - 2, "нажатые слова остались в сетке"
    assert " ".join(target[:2]) in rec.last_text(), "собранное не в тексте"
    assert any(b.startswith("bd:back:") for b in buttons)

    await _assemble(dp, bot, user, context, target[2:])
    buttons = rec.buttons()
    assert not any(b.startswith("bd:t:") for b in buttons), "лишние слова висят"
    assert sum(b.startswith("bd:check") for b in buttons) == 1


def test_the_grid_has_two_columns():
    from app.bot.handlers.quiz.build import grid_keyboard

    rows = grid_keyboard([f"w{i}" for i in range(9)], [], 1, 0, "ru", slots=7).inline_keyboard
    assert [len(r) for r in rows] == [2, 2, 2, 2, 1]

async def test_a_right_build_is_recorded_once(session, user, stage):
    dp, bot, rec = stage
    context, data = await _start_build(session, user, rec, dp, bot)
    target = data["build_target"]

    await _assemble(dp, bot, user, context, target)
    assert any(b.startswith("bd:check") for b in rec.buttons()), "«Проверить» не появилась"
    await _check(dp, bot, user, context)

    assert "Верно" in rec.last_text()
    assert data["build_sentence"] in rec.last_text()
    rows = await _rows(session, data["session_id"])
    assert [(r.channel, r.is_correct) for r in rows] == [("b", True)]
    assert rows[0].user_answer == " ".join(target)

    # Второе «Проверить» и нажатие по сетке после проверки — ничего
    await _check(dp, bot, user, context)
    await _tap(dp, bot, user, context, 0)
    assert len(await _rows(session, data["session_id"])) == 1
    progress = (await session.execute(
        select(UserWord).where(UserWord.word_id == data["build_word"])
    )).scalar_one()
    assert (progress.shown_build, progress.correct_build) == (1, 1)


async def test_double_and_stale_taps_do_not_break_the_grid(session, user, stage):
    dp, bot, rec = stage
    context, data = await _start_build(session, user, rec, dp, bot)
    word, version = data["build_word"], data["build_version"]

    # Двойной тык: оба нажатия с одной версией — слово встаёт один раз
    await dp.feed_update(bot, press(user.id, f"bd:t:0:{word}:{version}"))
    await dp.feed_update(bot, press(user.id, f"bd:t:1:{word}:{version}"))
    assert (await context.get_data())["build_picked"] == [0]

    # Сетка чужого вопроса и мусор — молча
    await dp.feed_update(bot, press(user.id, f"bd:t:2:{word + 999}:1"))
    await dp.feed_update(bot, press(user.id, "bd:t:X"))
    assert (await context.get_data())["build_picked"] == [0]

    # ⌫ убирает последнее
    data = await context.get_data()
    await dp.feed_update(bot, press(user.id, f"bd:back:{word}:{data['build_version']}"))
    assert (await context.get_data())["build_picked"] == []


async def test_a_wrong_build_marks_words_and_goes_to_errors(session, user, stage):
    dp, bot, rec = stage
    context, data = await _start_build(session, user, rec, dp, bot)
    target, tiles = data["build_target"], data["build_tiles"]
    trap = next(t for t in tiles if t not in target)

    await _assemble(dp, bot, user, context, [trap] + target[1:])
    await _check(dp, bot, user, context)

    text = rec.last_text()
    assert "Неверно" in text and "✗" in text and "✓" in text
    assert f"Лишнее: {trap}" in text
    rows = await _rows(session, data["session_id"])
    assert [(r.channel, r.is_correct) for r in rows] == [("b", False)]
    assert data["build_word"] in (await context.get_data())["errors"]


async def test_right_words_in_another_order_get_the_soft_verdict(session, user, stage):
    dp, bot, rec = stage
    context, data = await _start_build(session, user, rec, dp, bot)
    target = data["build_target"]

    await _assemble(dp, bot, user, context, list(reversed(target)))
    await _check(dp, bot, user, context)

    assert "Слова верные, порядок другой" in rec.last_text()
    rows = await _rows(session, data["session_id"])
    assert rows[0].is_correct is False, "другой порядок засчитан верным"


async def test_the_full_check_only_comes_when_slots_are_full(session, user, stage):
    """«Проверить» по полусобранной сетке не принимается."""
    dp, bot, rec = stage
    context, data = await _start_build(session, user, rec, dp, bot)
    await _assemble(dp, bot, user, context, data["build_target"][:1])
    await _check(dp, bot, user, context)
    assert await _rows(session, data["session_id"]) == []


@pytest.mark.parametrize("word_level,user_level,fits", [
    (CEFRLevel.A2, CEFRLevel.A2, True),
    (CEFRLevel.A1, CEFRLevel.A2, True),
    # Живой тест 14.10: A2, режим «по теме», слово C1 —
    # «Die Kritik an seinem Plan war nicht ungerechtfertigt», «топорно»
    (CEFRLevel.C1, CEFRLevel.A2, False),
    (CEFRLevel.B1, CEFRLevel.A2, False),
    (CEFRLevel.C1, None, True),           # приёмки без человека — без условия
])
def test_build_takes_words_not_above_the_learners_level(word_level, user_level, fits):
    from app.services.quiz_service import channel_fits

    # Четыре слова: на A1–A2 сборка берёт фразы до 5–6 слов (патч 2.1) —
    # здесь проверяется уровень слова, а не длина
    word = _W("Die Kritik war berechtigt", level=word_level)
    assert channel_fits(QuizChannel.BUILD, word, PAIR, user_level) is fits


# ============================================================================
# ПАТЧ 2.1: A1–A2 — короче и без падежных ловушек
# ============================================================================

async def _puzzle_words(session):
    from app.database.models import Word as W

    target = make_word("Garten", level=CEFRLevel.A1)
    target.example_de = "Der Hund spielt im Garten"
    target.example_ru = "Собака играет в саду"
    other = make_word("Katze", level=CEFRLevel.A1)
    other.example_de = "Meine Katze schläft sehr gern"
    other.example_ru = "Моя кошка очень любит спать"
    long_one = make_word("Wohnung", level=CEFRLevel.A1)
    long_one.example_de = "Wir suchen seit Monaten eine neue Wohnung in Berlin"
    long_one.example_ru = "Мы уже несколько месяцев ищем новую квартиру в Берлине"
    session.add_all([target, other, long_one])
    await build_groups(session, ["de"])
    return target, long_one


async def test_a1_gets_one_trap_and_not_a_grammar_twin(session, user):
    from app.services import build_service as bs
    from app.services.language_service import pair_from_user

    target, _ = await _puzzle_words(session)
    pair = pair_from_user(user)
    for seed in range(10):
        import random
        puzzle = await bs.make_puzzle(session, target, pair, random.Random(seed),
                                      learner_level=CEFRLevel.A1)
        assert puzzle is not None
        assert len(puzzle.distractors) == 1, puzzle.distractors
        twins = {s.lower() for t in puzzle.target for s in bs._siblings(t, "de")}
        assert puzzle.distractors[0].lower() not in twins, (
            f"новичку попалась падежная ловушка: {puzzle.distractors}"
        )


async def test_a1_long_sentence_goes_to_another_game(session, user):
    from app.services import build_service as bs
    from app.services.language_service import pair_from_user

    _, long_one = await _puzzle_words(session)
    assert await bs.make_puzzle(session, long_one, pair_from_user(user),
                                learner_level=CEFRLevel.A1) is None


async def test_b1_keeps_the_harder_build(session, user):
    from app.services import build_service as bs
    from app.services.language_service import pair_from_user

    _, long_one = await _puzzle_words(session)
    puzzle = await bs.make_puzzle(session, long_one, pair_from_user(user),
                                  learner_level=CEFRLevel.B1)
    assert puzzle is not None and len(puzzle.distractors) >= 1


def test_easy_trap_skips_twins_from_foreign_words():
    """«in» из чужого примера — двойник «im»: новичку такую ловушку не давать."""
    import random

    from app.services import build_service as bs

    target = ["der", "Hund", "spielt", "im", "Garten"]
    for seed in range(20):
        picked, _ = bs.pick_distractors(target, "de", ["in", "Katze"], random.Random(seed), 1, easy=True)
        assert picked == ["Katze"], f"двойник в ловушках новичка: {picked}"


def test_selection_knows_the_easy_length():
    """Подбор не выбирает сборке слово, чья фраза длинна для A1 (проверка 2.1)."""
    from app.services.quiz_service import channel_fits
    from app.services.language_service import LanguagePair

    pair = LanguagePair(learning="de", native="ru", reverse=False)
    long_one = _W("Wir suchen seit Monaten eine neue Wohnung", level=CEFRLevel.A1)
    assert not channel_fits(QuizChannel.BUILD, long_one, pair, CEFRLevel.A1)
    assert channel_fits(QuizChannel.BUILD, long_one, pair, CEFRLevel.B1)


def test_easy_never_takes_a_twin_even_without_foreign_words():
    """Чужих слов нет — двойник «den» к «der» всё равно не берётся."""
    import random

    from app.services import build_service as bs

    target = ["der", "Hund", "spielt", "heute"]
    twins = {s.lower() for t in target for s in bs._siblings(t, "de")}
    for seed in range(30):
        picked, _ = bs.pick_distractors(target, "de", [], random.Random(seed), 1, easy=True)
        assert not ({p.lower() for p in picked} & twins), f"двойник: {picked}"
