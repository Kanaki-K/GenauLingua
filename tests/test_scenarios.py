"""
СЦЕНАРИИ: нажатие доходит до нужного обработчика, и на экране то, что надо.

Это последний непроверенный слой. Приёмка игр проверяет, что вопрос
СОБИРАЕТСЯ верно. Приёмка меню — что у каждой кнопки есть кому её поймать.
Тесты — что функции отвечают как задумано. Но никто не проверял, что
нажатие проходит настоящую цепочку роутеров и приводит к нужному экрану.

Разрыв не умозрительный: оба самых злых дефекта проекта жили именно там.
«Подсказка про голос гасила кнопки меню» — роутер игры подключён раньше
настроек, обработчик глушил событие. NameError в развилке
`show_next_question` — его не видят ни тесты на функции, ни приёмка
генератора, потому что он живёт В ПОТОКЕ обработчика и только на той
ветке, куда доходят немногие.

Здесь диспетчер собран с тем же набором роутеров и в том же порядке, что
боевой (`tests/scenario.py`), а поддельна только сеть.
"""

import pytest

from app.database.enums import CEFRLevel, QuizMode
from app.database.models import UserWord, Word
from tests.conftest import build_groups, make_word
from tests.scenario import (
    make_bot, make_dispatcher, press, reset_state, text_update,
)

pytestmark = pytest.mark.asyncio

# Слов надо больше, чем длина круга: вопросы не повторяются внутри круга,
# и на коротком запасе круг оборвался бы по исчерпанию, а не по счёту
WORDS = 40
ROUND_LENGTH = 6


async def _ready(session, user, *, channels: str = "t") -> list[Word]:
    """Человек с уровнем, составом занятия и запасом слов."""
    for i in range(WORDS):
        session.add(make_word(f"Wort{i:03d}", level=CEFRLevel.A1))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = ROUND_LENGTH
    user.audio_enabled = False      # сценарию не нужен звук: его нет на диске
    user.quiz_channels = channels
    await session.commit()

    from sqlalchemy import select

    return (await session.execute(select(Word).order_by(Word.id))).scalars().all()


async def _feed(dp, bot, update):
    await dp.feed_update(bot, update)


@pytest.fixture
async def stage(session):
    """
    Диспетчер, бот и запись вызовов — на один сценарий.

    Диспетчер ОДИН на весь прогон: роутеры — модульные одиночки и
    привязываются ровно к одному, второй вызов даёт «Router is already
    attached». Поэтому между сценариями меняется сессия базы и чистится
    состояние FSM — иначе брошенный круг предыдущего сценария утянул бы
    следующий.
    """
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


# ============================================================================
# ПОЛНЫЙ КРУГ
# ============================================================================

async def test_round_is_playable_from_the_menu_button_to_the_result(session, user, stage):
    """
    Главный сценарий: человек нажал «Учить слова» и дошёл до итога.

    Проверяется не текст, а ДОХОДИМОСТЬ: каждый вопрос показан, каждый
    ответ принят, итог показан. Любой разрыв в цепочке роутеров обрывает
    сценарий здесь, а не у человека.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))

    assert recorder.sent_texts(), "после нажатия «Учить слова» бот промолчал"
    first = recorder.last_text()
    assert "1/" in first or "1 /" in first, f"нет номера вопроса: {first!r}"

    answers = recorder.buttons()
    assert len(answers) == 4, f"вариантов не четыре: {answers}"
    assert all(a.startswith("answer_") for a in answers), answers

    # Проходим круг до конца, каждый раз отвечая первым вариантом
    for step in range(ROUND_LENGTH):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        assert options, f"шаг {step + 1}: вариантов ответа нет"
        await _feed(dp, bot, press(user.id, options[0]))

        after = recorder.buttons()
        assert "next_question" in after, (
            f"шаг {step + 1}: после ответа нет кнопки «дальше»: {after}"
        )
        await _feed(dp, bot, press(user.id, "next_question"))

    # Итог ищется среди ВСЕХ сообщений, а не в последнем: после круга бот
    # присылает ещё одно, с предложением напоминаний. Моя первая редакция
    # смотрела на последнее и объявила, что круг не кончился итогом
    everything = "\n".join(recorder.sent_texts())
    assert get_text("quiz_completed", "ru").strip("🎉<b/> ") in everything, (
        f"круг не кончился итогом; последнее было: {recorder.last_text()!r}"
    )


async def test_result_offers_another_round_and_it_really_starts(session, user, stage):
    """
    «▶️ Ещё круг» в итоге должен НАЧИНАТЬ круг, а не просто существовать.

    Тест на клавиатуру проверяет, что кнопка на месте и первая. Здесь
    проверяется, что нажатие на неё доходит и даёт вопрос.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(ROUND_LENGTH):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        await _feed(dp, bot, press(user.id, options[0]))
        await _feed(dp, bot, press(user.id, "next_question"))

    assert "learn_now" in recorder.all_buttons(), "в итоге нет «ещё круг»"

    recorder.clear()
    await _feed(dp, bot, press(user.id, "learn_now"))

    assert recorder.sent_texts(), "«ещё круг» ничего не показал"
    assert any(b.startswith("answer_") for b in recorder.buttons()), (
        f"после «ещё круг» нет вопроса: {recorder.buttons()}"
    )


async def test_answering_actually_records_progress(session, user, stage):
    """
    Ответ должен ДОХОДИТЬ ДО БАЗЫ, а не только до экрана.

    Экран можно показать и не записав ничего — тогда человек занимается, а
    прогресс стоит на месте, и заметно это становится через недели.
    """
    from sqlalchemy import func, select
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    before = (await session.execute(
        select(func.count()).select_from(UserWord).where(UserWord.user_id == user.id)
    )).scalar()

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    options = [b for b in recorder.buttons() if b.startswith("answer_")]
    await _feed(dp, bot, press(user.id, options[0]))

    after = (await session.execute(
        select(func.count()).select_from(UserWord).where(UserWord.user_id == user.id)
    )).scalar()

    assert after > before, "ответ не записался в прогресс"


# ============================================================================
# ПЕТЛЯ ВОЗВРАТА
# ============================================================================

async def test_reminder_button_starts_a_lesson(session, user, stage):
    """
    Кнопка напоминания — самое ценное нажатие в боте: единственное, которое
    человек делает, НЕ заходя в бота. Сообщение приходит от бота, значит
    `from_user` в нём — бот, и искать человека по отправителю нельзя.
    """
    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, press(user.id, "learn_now"))

    assert recorder.sent_texts(), "нажатие из напоминания не дало ничего"
    assert any(b.startswith("answer_") for b in recorder.buttons()), (
        f"из напоминания не начался круг: {recorder.buttons()}"
    )


async def test_home_screen_opens_from_the_progress_button(session, user, stage):
    """Реплай-кнопка «Статистика» открывает домашний экран с тремя шкалами."""
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, text_update(user.id, get_text("btn_stats", "ru")))

    text = recorder.last_text()
    assert "<code>" in text, f"шкал нет: {text!r}"
    assert "learn_now" in recorder.buttons(), "с домашнего экрана не начать занятие"
    assert "stats_full" in recorder.buttons(), "нет входа в подробную статистику"


async def test_detailed_stats_opens_and_comes_back(session, user, stage):
    """
    Подробная статистика и возврат — два нажатия, и оба должны работать.
    Экран, из которого нет пути назад, — тупик.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, text_update(user.id, get_text("btn_stats", "ru")))
    recorder.clear()

    await _feed(dp, bot, press(user.id, "stats_full"))
    detailed = recorder.last_text()
    assert get_text("stats_header", "ru").strip("📊<b/> ") in detailed, (
        f"подробная статистика не открылась: {detailed[:80]!r}"
    )
    assert "home_back" in recorder.buttons(), "из статистики нет пути назад"

    recorder.clear()
    await _feed(dp, bot, press(user.id, "home_back"))
    assert "<code>" in recorder.last_text(), "возврат не дал домашний экран"


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ И ОБРАТНО
# ============================================================================

async def test_settings_groups_open_and_lead_back(session, user, stage):
    """
    Каждая группа открывается, и каждая ведёт назад. Это и есть «логика
    сценариев»: не наличие кнопок, а проходимость туда и обратно.
    """
    from app.bot.handlers.quiz.settings import _GROUPS
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, text_update(user.id, get_text("btn_settings", "ru")))
    top = recorder.buttons()
    assert len(top) == len(_GROUPS), f"на главном экране настроек не группы: {top}"

    for key in _GROUPS:
        recorder.clear()
        await _feed(dp, bot, press(user.id, f"settings_group_{key}"))
        inside = recorder.buttons()
        assert inside, f"группа {key} не открылась"
        assert "back_to_settings" in inside, f"из группы {key} нет пути назад"

        recorder.clear()
        await _feed(dp, bot, press(user.id, "back_to_settings"))
        assert recorder.buttons(), f"возврат из группы {key} ничего не показал"


async def test_goal_can_be_changed_through_settings(session, user, stage):
    """
    Цель должна МЕНЯТЬСЯ из настроек, а не только задаваться в онбординге:
    у всех 233 нынешних пользователей онбординг давно позади.
    """
    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, press(user.id, "settings_goal"))
    assert any(b.startswith("set_goal_") for b in recorder.buttons()), (
        f"экран цели не предлагает целей: {recorder.buttons()}"
    )

    await _feed(dp, bot, press(user.id, "set_goal_work"))
    await session.refresh(user)
    assert user.learning_goal == "work", "цель не сохранилась"


async def test_lesson_composition_can_be_toggled(session, user, stage):
    """Состав занятия переключается, и текст не выключается никогда."""
    dp, bot, recorder = stage
    await _ready(session, user, channels="ta")


    await _feed(dp, bot, press(user.id, "settings_channels"))
    assert any(b.startswith("channel_toggle_") for b in recorder.buttons()), (
        f"экран состава не предлагает каналов: {recorder.buttons()}"
    )

    await _feed(dp, bot, press(user.id, "channel_toggle_t"))
    await session.refresh(user)
    assert "t" in (user.quiz_channels or ""), "карточку удалось выключить"


# ============================================================================
# ПОВТОР ОШИБОК — ВЕТКА, НА КОТОРОЙ ПРОЕКТ УЖЕ ГОРЕЛ
#
# `show_next_question` устроен как развилка с общим хвостом, и при
# добавлении запасного пути `clip` появился только во второй ветке: кнопка
# «повторить ошибки» падала с NameError при каждом нажатии. Ни тесты на
# функции, ни приёмка генератора этого не видели — дефект жил в потоке
# обработчика и только на той ветке, куда доходят немногие.
#
# Разбор кода это держит (test_quiz_flow). Здесь проверяется, что ветка
# ПРОХОДИТСЯ целиком.
# ============================================================================

async def _wrong_answer(dp, bot, user_id: int, recorder) -> str:
    """Вариант, который НЕ является верным ответом на текущий вопрос."""
    context = dp.fsm.get_context(bot, chat_id=user_id, user_id=user_id)
    data = await context.get_data()
    correct = f"answer_{data['correct_word_id']}"
    options = [b for b in recorder.buttons() if b.startswith("answer_")]
    wrong = [o for o in options if o != correct]
    assert wrong, f"все варианты равны верному: {options}"
    return wrong[0]


async def test_repeating_errors_goes_all_the_way_through(session, user, stage):
    """
    Человек ошибся, прошёл круг и нажал «повторить ошибки» — и получил
    вопрос, а не молчание.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))

    # Отвечаем НЕВЕРНО на каждый вопрос: тогда ошибки точно будут
    for _ in range(ROUND_LENGTH):
        await _feed(dp, bot, press(user.id, await _wrong_answer(dp, bot, user.id, recorder)))
        await _feed(dp, bot, press(user.id, "next_question"))

    assert "repeat_errors" in recorder.all_buttons(), (
        f"после круга с ошибками нет кнопки повтора: {recorder.all_buttons()}"
    )

    recorder.clear()
    await _feed(dp, bot, press(user.id, "repeat_errors"))

    assert recorder.sent_texts(), "«повторить ошибки» не показало ничего"
    assert any(b.startswith("answer_") for b in recorder.buttons()), (
        f"повтор ошибок не дал вопроса: {recorder.buttons()}"
    )

    # И повтор должен ПРОХОДИТЬСЯ до конца, а не падать на втором вопросе
    for _ in range(ROUND_LENGTH):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        await _feed(dp, bot, press(user.id, options[0]))
        if "next_question" not in recorder.buttons():
            break
        await _feed(dp, bot, press(user.id, "next_question"))


async def test_reminders_are_offered_after_the_first_finished_round(session, user, stage):
    """
    Предложение напоминаний — единственный замеренный рычаг возврата, и
    показывается он ровно один раз в жизни, после первого круга.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)
    user.notifications_enabled = False
    user.reminder_offered_at = None
    await session.commit()

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(ROUND_LENGTH):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        await _feed(dp, bot, press(user.id, options[0]))
        await _feed(dp, bot, press(user.id, "next_question"))

    assert "reminder_offer_yes" in recorder.all_buttons(), (
        "после первого круга напоминания не предложены"
    )

    await _feed(dp, bot, press(user.id, "reminder_offer_yes"))
    await session.refresh(user)
    assert user.notifications_enabled, "согласие не включило напоминания"
    assert user.notification_time, "час напоминания не выставлен"


# ============================================================================
# ОНБОРДИНГ ЦЕЛИКОМ: САМЫЙ ДОРОГОЙ ПУТЬ В БОТЕ
#
# Дальше него либо первый круг, либо уход навсегда. Замер: 24 человека из
# 233 прошли онбординг и не начали ни одного круга.
# ============================================================================

async def test_onboarding_runs_from_start_to_the_first_question(session, user, stage):
    """
    /start → язык → что учить → уровень → зачем учишь → ПЕРВЫЙ ВОПРОС.

    Ни одного экрана, где надо что-то искать: каждый шаг кончается кнопкой.
    """
    dp, bot, recorder = stage

    # Слова нужны, иначе первый вопрос не соберётся
    for i in range(WORDS):
        session.add(make_word(f"Neu{i:03d}", level=CEFRLevel.A1))
    await build_groups(session, ["de"])

    # Человек, который ещё ничего не выбрал.
    #
    # Уровень в НОЛЬ не ставится: колонка `users.level` объявлена
    # не-NULL со значением по умолчанию A1. Отсюда, кстати, следует, что
    # ветка `if user.level:` в `cmd_start` истинна ВСЕГДА, а её `else` —
    # выбор уровня при `/start` — недостижим. Это не беда онбординга (он
    # спрашивает уровень своим шагом), но мёртвая ветка там есть, и
    # замечена она именно этим сценарием.
    user.interface_language = None
    user.quiz_word_count = ROUND_LENGTH
    user.audio_enabled = False
    await session.commit()

    await _feed(dp, bot, text_update(user.id, "/start"))
    assert recorder.sent_texts(), "/start не показал выбор языка"
    assert any(b.startswith("select_lang_") for b in recorder.buttons()), (
        f"нет выбора языка интерфейса: {recorder.buttons()}"
    )

    await _feed(dp, bot, press(user.id, "select_lang_ru"))
    assert any(b.startswith("onboard_learn_") for b in recorder.buttons()), (
        f"нет выбора изучаемого языка: {recorder.buttons()}"
    )

    await _feed(dp, bot, press(user.id, "onboard_learn_de"))
    assert any(b.startswith("start_level_") for b in recorder.buttons()), (
        f"нет выбора уровня: {recorder.buttons()}"
    )

    recorder.clear()
    await _feed(dp, bot, press(user.id, "start_level_A1"))
    assert any(b.startswith("goal_") for b in recorder.buttons()), (
        f"после уровня не спросили о цели: {recorder.buttons()}"
    )

    recorder.clear()
    await _feed(dp, bot, press(user.id, "goal_work"))

    await session.refresh(user)
    assert user.learning_goal == "work", "цель из онбординга не сохранилась"
    assert any(b.startswith("answer_") for b in recorder.buttons()), (
        f"онбординг не довёл до первого вопроса: {recorder.buttons()}"
    )


async def test_start_for_a_returning_person_is_the_intro_block(session, user, stage):
    """
    Вернувшийся человек видит вступление, а не шкалы: шкалы живут на кнопке
    «Прогресс», куда приходят постоянно, а /start набирают раз в жизни.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, text_update(user.id, "/start"))

    everything = "\n".join(recorder.sent_texts())
    assert get_text("intro_title", "ru").strip("🌍<b/> ") in everything, (
        f"/start не дал вступления: {everything[:120]!r}"
    )
    assert "learn_now" in recorder.all_buttons(), "из вступления не начать занятие"

    # И вступление не обещает кнопку, которой в меню нет
    assert get_text("btn_help", "ru") not in everything, (
        "вступление снова обещает «Помощь» среди кнопок меню"
    )
