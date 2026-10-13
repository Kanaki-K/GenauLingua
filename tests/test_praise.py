"""
Поощрение в конце круга: хвалим только за то, что случилось.

ЗАЧЕМ. Экран итога показывал «Правильно 12/15» и разбор слов — и всё. Ни
баллов (хотя круг их платит), ни серии, ни продвижения: человек доводил
круг до конца и не узнавал ни одной причины вернуться.

Опасность у похвалы ровно одна, и она уже случалась в этом боте: похвала
за то, чего не было. Домашний экран говорил «1 день подряд» человеку,
который не заходил восемь месяцев, — и обесценивал этим все остальные
числа. Поэтому здесь проверяется не «есть ли похвала», а НЕ ХВАЛИТ ЛИ ОНА
ЗА НЕСЛУЧИВШЕЕСЯ.

Правило выбора повода отделено от замеров нарочно: о нём надо спорить на
числах, а не гоняя круги. Эти проверки идут без базы.
"""

from app.locales import LOCALES
from app.services.praise_service import (
    COMEBACK_DAYS, MILESTONES, PERFECT_MIN_ANSWERS, RoundFacts, build_lines,
    crossed_milestone, next_milestone, pick_event, pick_shift,
)


def _facts(**kwargs) -> RoundFacts:
    """Обычный круг середины пути: ничего особенного не случилось."""
    base = dict(
        points=20, answered=15, correct=11, rounds_total=18,
        learned_before=9, learned_now=9, streak_days=1, best_streak=7,
        words_in_work=120, words_in_work_before=117,
        new_words=3, returned_right=8,
    )
    base.update(kwargs)
    return RoundFacts(**base)


# ============================================================================
# ЧЕГО НЕ БЫЛО — ЗА ТО НЕ ХВАЛИМ
# ============================================================================

def test_a_bad_round_is_not_called_perfect():
    """11 из 15 — не «круг без ошибок», сколько бы ни хотелось похвалить."""
    assert pick_event(_facts(correct=11)) != ("praise_perfect", {})


def test_a_short_perfect_round_is_not_an_achievement():
    """
    Три из трёх — это короткий круг, а не достижение. Планка нужна, иначе
    «без ошибок» выдавалось бы человеку, ответившему на один вопрос.
    """
    short = _facts(answered=PERFECT_MIN_ANSWERS - 1,
                   correct=PERFECT_MIN_ANSWERS - 1, streak_days=1,
                   new_words=0, returned_right=0)
    assert pick_event(short) is None


def test_nothing_learned_means_no_learned_praise():
    chosen = pick_event(_facts(learned_before=9, learned_now=9))
    assert chosen is None or chosen[0] != "praise_learned"


def test_a_broken_streak_is_not_praised():
    """
    Серия в один день — это не серия. Хвалить за неё значит повторять ту
    самую ложь, из-за которой домашний экран хвалил за восемь месяцев
    молчания.
    """
    chosen = pick_event(_facts(streak_days=1))
    assert chosen is None or chosen[0] != "praise_streak"


def test_zero_points_are_not_shown():
    """
    «Баллы: +0» — сообщение о награде, которой не было. У круга-повтора
    баллов нет вовсе.
    """
    lines = build_lines(_facts(points=0), "ru")
    assert not any("+0" in line for line in lines), lines


# ============================================================================
# ПОРЯДОК ПОВОДОВ: ОТ РЕДКОГО К ЧАСТОМУ
# ============================================================================

def test_the_first_round_speaks_first():
    """Первый круг в жизни важнее любого числа в нём."""
    first = _facts(rounds_total=1, correct=15, answered=15, streak_days=5)
    assert pick_event(first) == ("praise_first_round", {})


def test_the_first_learned_word_beats_a_streak():
    """
    Первое выученное слово — событие, которого у 156 человек из 199 не было
    ни разу. Продолженная серия бывает ежедневно.
    """
    chosen = pick_event(_facts(
        learned_before=0, learned_now=1, streak_days=4, best_streak=4,
    ))
    assert chosen == ("praise_first_learned", {})


def test_a_record_streak_beats_an_ordinary_one():
    record = _facts(streak_days=5, best_streak=4)
    assert pick_event(record) == ("praise_best_streak", {"days": 5})


def test_an_ordinary_streak_is_praised_when_nothing_else_happened():
    chosen = pick_event(_facts(streak_days=3, best_streak=9, new_words=0,
                               returned_right=0, words_in_work_before=120))
    assert chosen == ("praise_streak", {"days": 3})


def test_a_milestone_beats_a_perfect_round():
    """
    Рубеж — след месяца занятий, круг без ошибок — одного вечера. Оба
    случились, говорим о первом.
    """
    chosen = pick_event(_facts(
        answered=15, correct=15, words_in_work_before=48, words_in_work=51,
        streak_days=1,
    ))
    assert chosen == ("praise_milestone", {"count": 50})


def test_a_comeback_is_noticed():
    chosen = pick_event(_facts(days_away=COMEBACK_DAYS + 20, streak_days=1,
                               words_in_work_before=120))
    assert chosen == ("praise_comeback", {"days": COMEBACK_DAYS + 20})


def test_the_first_voice_answer_is_an_event():
    chosen = pick_event(_facts(first_speech=True, streak_days=1,
                               words_in_work_before=120))
    assert chosen == ("praise_first_speech", {})


def test_voice_beats_hearing_when_both_are_first():
    """
    Речь дороже слуха: она не узнавание, а производство. Тот же порядок,
    что в цене балла — 3 против 2.
    """
    chosen = pick_event(_facts(first_speech=True, first_audio=True,
                               streak_days=1, words_in_work_before=120))
    assert chosen == ("praise_first_speech", {})


# ============================================================================
# КОГДА НЕ СЛУЧИЛОСЬ НИЧЕГО — БЕРЁМ СДВИГ КРУГА
# ============================================================================

def test_a_plain_round_still_says_something_true():
    """
    Круг без событий бывает чаще всех, и молчать в нём нельзя: человек
    закончил работу. Говорится измеренный сдвиг — он всегда непустой.
    """
    plain = _facts(streak_days=1, words_in_work_before=120)
    assert pick_event(plain) is None
    assert pick_shift(plain) is not None


def test_the_shift_line_follows_the_round_composition():
    """
    Разнообразие берётся из состава круга, а не из случайного выбора фраз:
    в круге с новыми словами скажется про новые, в круге повторения — про
    вернувшиеся. Состав меняется сам.
    """
    with_new = _facts(new_words=9, returned_right=2)
    repeating = _facts(new_words=0, returned_right=11)

    assert pick_shift(with_new) == ("praise_new_words", {"count": 9})
    assert pick_shift(repeating) == ("praise_returned", {"count": 11})


def test_a_round_where_nothing_moved_says_nothing_extra():
    """
    Ни новых, ни узнанных заново — и выдумывать нечего. Остаётся прогресс
    и баллы, а строки похвалы нет.
    """
    nothing = _facts(new_words=0, returned_right=0, correct=0, streak_days=1,
                     words_in_work_before=120)
    assert pick_shift(nothing) is None
    lines = build_lines(nothing, "ru")
    assert len(lines) == 2, lines


# ============================================================================
# РУБЕЖИ ВМЕСТО ВЕЧНЫХ НУЛЕЙ
# ============================================================================

def test_the_next_milestone_is_always_close():
    """
    Замер 13 октября: медиана слов в работе 26, 90-й процентиль 209. Для
    обоих следующий рубеж должен быть в пределах нескольких кругов, а не
    «3 132 слова уровня» — именно из-за такого знаменателя шкалы стояли на
    вечных нулях.
    """
    assert next_milestone(26) == 50
    assert next_milestone(209) == 250
    assert next_milestone(0) == 10
    assert next_milestone(9) == 10
    assert next_milestone(10) == 25


def test_past_the_last_milestone_there_is_no_fake_target():
    """
    Все рубежи взяты — шкалы нет. Выдумывать «до 5 000» бессмысленно:
    столько слов на паре просто нет.
    """
    assert next_milestone(MILESTONES[-1]) is None
    lines = build_lines(_facts(words_in_work=MILESTONES[-1] + 100), "ru")
    assert any("2 600" in line or "2600" in line for line in lines), lines


def test_a_milestone_counts_only_on_the_round_that_crossed_it():
    assert crossed_milestone(48, 51) == 50
    assert crossed_milestone(51, 54) is None
    assert crossed_milestone(9, 30) == 10, "взят первый из пройденных"


# ============================================================================
# ТЕКСТ
# ============================================================================

def test_the_block_is_three_lines_at_most():
    """
    Блок длиннее разбора перестаёт быть поощрением и становится вторым
    экраном. Разбор круга — пятнадцать строк, похвала — три.
    """
    richest = _facts(rounds_total=1, points=99)
    assert len(build_lines(richest, "ru")) <= 3


def test_every_praise_key_exists_in_every_locale():
    """
    Пропущенный ключ не падает — он уезжает человеку как «[MISSING: …]».
    Проверка общая есть в `test_locales`, здесь — именно про поощрение,
    чтобы новый повод нельзя было добавить в одну локаль.
    """
    keys = {
        "praise_first_round", "praise_first_learned", "praise_learned",
        "praise_best_streak", "praise_milestone", "praise_first_speech",
        "praise_first_audio", "praise_comeback", "praise_perfect",
        "praise_streak", "praise_new_words", "praise_returned",
        "praise_progress", "praise_progress_top", "praise_points",
    }
    for lang, texts in LOCALES.items():
        missing = keys - set(texts)
        assert not missing, f"{lang}: нет ключей {sorted(missing)}"


def test_no_praise_line_carries_a_decorative_mark():
    """
    Поощрение — первый блок бота, написанный по уставу внешности: знаков
    нет, слова и типографика. Если сюда вернётся `🎉`, то вернётся и во всё
    остальное.
    """
    import re

    allowed = set("·—–…")
    emoji = re.compile(r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿]")
    offenders = []
    for lang, texts in LOCALES.items():
        for key, value in texts.items():
            if not key.startswith("praise_"):
                continue
            for char in emoji.findall(value):
                if char not in allowed:
                    offenders.append(f"{lang}/{key}: {char!r}")
    assert not offenders, "значки в поощрении: " + ", ".join(offenders)


def test_every_locale_renders_without_a_missing_parameter():
    """
    Подстановка, которой нет в строке одной локали, превращается в
    «[ERROR: … missing parameter]». Прогоняем все поводы по всем языкам.
    """
    cases = [
        _facts(rounds_total=1),
        _facts(learned_before=0, learned_now=1),
        _facts(learned_before=1, learned_now=3),
        _facts(streak_days=5, best_streak=4),
        _facts(words_in_work_before=48, words_in_work=51),
        _facts(first_speech=True, streak_days=1, words_in_work_before=120),
        _facts(first_audio=True, streak_days=1, words_in_work_before=120),
        _facts(days_away=30, streak_days=1, words_in_work_before=120),
        _facts(answered=15, correct=15, streak_days=1, words_in_work_before=120),
        _facts(streak_days=3, best_streak=9, new_words=0, returned_right=0,
               words_in_work_before=120),
        _facts(new_words=7, returned_right=1),
        _facts(new_words=0, returned_right=9),
        _facts(words_in_work=MILESTONES[-1] + 1),
    ]
    for lang in LOCALES:
        for facts in cases:
            for line in build_lines(facts, lang):
                assert "MISSING" not in line and "ERROR" not in line, (
                    f"{lang}: {line}"
                )
                assert "{" not in line, f"{lang}: неподставленное место — {line}"


# ============================================================================
# НА НАСТОЯЩЕМ КРУГЕ
# ============================================================================
#
# Проверки выше — про правило выбора повода и идут без базы. Эти — про то,
# что блок ДОХОДИТ до экрана: правило может быть верным, а строки не
# попасть в итог вовсе, и ни одна проверка выше этого не заметит.

import pytest  # noqa: E402

from app.database.enums import CEFRLevel, QuizMode  # noqa: E402
from app.database.models import Word  # noqa: E402
from tests.conftest import build_groups, make_word  # noqa: E402
from tests.scenario import (  # noqa: E402
    make_bot, make_dispatcher, press, reset_state, text_update,
)

ROUND = 5


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


async def _ready(session, user) -> None:
    for i in range(40):
        session.add(make_word(f"Wort{i:03d}", level=CEFRLevel.A1))
    await build_groups(session, ["de"])
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = ROUND
    user.audio_enabled = False
    user.quiz_channels = "t"
    user.match_in_round = False
    user.quizzes_passed = 0
    await session.commit()


async def _play(dp, bot, recorder, user, *, wrong: bool = False) -> None:
    """Сыграть круг. `wrong` — отвечать неверно, чтобы набрать ошибки."""
    from app.locales import get_text

    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(ROUND):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        if wrong:
            correct = (await context.get_data()).get("correct_word_id")
            choice = next((o for o in options if o != f"answer_{correct}"),
                          options[0])
        else:
            choice = options[0]
        await dp.feed_update(bot, press(user.id, choice))
        if "next_question" not in recorder.buttons():
            break
        await dp.feed_update(bot, press(user.id, "next_question"))


async def test_the_praise_block_reaches_the_screen(session, user, stage):
    """
    Строка прогресса есть ВСЕГДА — по ней и проверяется, что блок дошёл.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play(dp, bot, recorder, user)

    everything = "\n".join(recorder.sent_texts())
    assert "Слов в работе" in everything, (
        f"блока поощрения нет в итоге: {recorder.last_text()!r}"
    )


async def test_the_round_shows_what_it_paid(session, user, stage):
    """
    Круг платит баллами, и до этой правки экран о них не говорил ни слова:
    награда была невидимой.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play(dp, bot, recorder, user)

    everything = "\n".join(recorder.sent_texts())
    assert "Баллы: +" in everything, f"баллы не показаны: {everything[-400:]!r}"


async def test_the_very_first_round_is_greeted(session, user, stage):
    """
    Первый круг в жизни — единственный повод, который нельзя отложить: у
    79% людей второго дня не было, и сказать «дальше слова начнут
    возвращаться» надо именно сейчас.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play(dp, bot, recorder, user)

    everything = "\n".join(recorder.sent_texts())
    assert "Первый круг пройден" in everything, everything[-400:]


async def test_the_repeat_round_gets_no_praise(session, user, stage):
    """
    Круг-повтор не платит баллов, не двигает серию и не считается
    пройденным. Поощрять его значило бы обещать награду, которой нет.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play(dp, bot, recorder, user, wrong=True)

    assert "repeat_errors" in recorder.all_buttons(), "ошибок не набралось"
    recorder.clear()
    await dp.feed_update(bot, press(user.id, "repeat_errors"))

    # Пройти повтор до конца
    for _ in range(ROUND):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        await dp.feed_update(bot, press(user.id, options[0]))
        if "next_question" not in recorder.buttons():
            break
        await dp.feed_update(bot, press(user.id, "next_question"))

    everything = "\n".join(recorder.sent_texts())
    assert "Слов в работе" not in everything, (
        f"повтор получил поощрение: {everything[-400:]!r}"
    )
    assert "Баллы: +" not in everything, "повтор показал баллы"
