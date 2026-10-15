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
from app.testing import lesson_button, starts_lesson  # noqa: F401
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

    again = lesson_button(recorder.all_buttons())
    assert again, "в итоге нет «ещё круг»"

    # Кнопка запоминается ДО очистки записи: после `clear()` список пуст
    recorder.clear()
    await _feed(dp, bot, press(user.id, again))

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

    # Нажимается ИМЕННО дверь напоминания: у неё своя пометка, по которой
    # петля возврата и считается
    await _feed(dp, bot, press(user.id, "learn_now:reminder"))

    assert recorder.sent_texts(), "нажатие из напоминания не дало ничего"
    assert any(b.startswith("answer_") for b in recorder.buttons()), (
        f"из напоминания не начался круг: {recorder.buttons()}"
    )


async def test_home_screen_opens_from_the_progress_button(session, user, stage):
    """
    Кнопка «Статистика» открывает шкалы — и РОВНО ОДНУ кнопку.

    Прежде этот тест требовал, чтобы с экрана можно было начать занятие.
    Требование снято решением владельца: «у статистики 1 кнопка —
    подробнее. Зачем нам на экране 2 раза учить слова, не понимаю».
    «Учить слова» стоит на нижней клавиатуре под каждым экраном, и та же
    кнопка внутри сообщения — одно действие в двух местах.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await _feed(dp, bot, text_update(user.id, get_text("btn_stats", "ru")))

    text = recorder.last_text()
    assert "<code>" in text, f"шкал нет: {text!r}"
    assert recorder.buttons() == ["stats_full"], (
        f"на экране числа не одна кнопка: {recorder.buttons()}"
    )


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

    recorder.clear()
    await _feed(dp, bot, press(user.id, "reminder_offer_yes"))
    await session.refresh(user)
    assert user.notifications_enabled, "согласие не включило напоминания"
    assert user.notification_time, "час напоминания не выставлен"

    # Владелец: «предложить гибкие настройки — с переходом в настройки».
    # Ответ называет поставленное время и ведёт кнопкой в настройки
    assert user.notification_time in recorder.last_text(), (
        f"время не названо: {recorder.last_text()!r}"
    )
    assert "settings:notifications" in recorder.buttons(), "нет кнопки в настройки"


# ============================================================================
# ОНБОРДИНГ ЦЕЛИКОМ: САМЫЙ ДОРОГОЙ ПУТЬ В БОТЕ
#
# Дальше него либо первый круг, либо уход навсегда. Замер: 24 человека из
# 233 прошли онбординг и не начали ни одного круга.
# ============================================================================

async def test_onboarding_runs_from_start_to_the_first_question(session, user, stage):
    """
    /start → язык бота → что учить → [ Заниматься ] → ПЕРВЫЙ ВОПРОС.

    ДВА ВОПРОСА ВМЕСТО ЧЕТЫРЁХ. Решение владельца: «нужно дать возможность
    выбрать язык потом играть. И уже чтобы бот подстраивался сам — это же
    его фишка. Хотят принудительно сложнее — есть настройки».

    Уровень был самым дорогим вопросом: своего уровня по CEFR человек
    обычно не знает, а ошибка в нём портит всё занятие. Теперь начинается
    A1, а поднимает бот — по точности последних ответов.

    Цель («зачем учишь») тоже ушла, и за дело: пять кнопок, каждая молча
    начинала круг, и по экрану нельзя было понять, выбралось ли что-то.
    Владелец об этом экране дословно: «любую тыкаешь — начинаешь игру. И не
    ясно выбралось что-то отдельное или нет». Цель осталась в настройках.
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

    recorder.clear()
    await _feed(dp, bot, press(user.id, "onboard_learn_de"))

    # Уровень НЕ спрашивается — его ставит бот
    assert not any(b.startswith("start_level_") for b in recorder.buttons()), (
        f"уровень всё ещё спрашивают: {recorder.buttons()}"
    )
    await session.refresh(user)
    assert user.level == CEFRLevel.A1, f"уровень не выставлен сам: {user.level}"

    # И цель не спрашивается
    assert not any(b.startswith("goal_") for b in recorder.buttons()), (
        f"цель всё ещё спрашивают: {recorder.buttons()}"
    )

    start = lesson_button(recorder.all_buttons())
    assert start, f"знакомство не кончилось кнопкой занятия: {recorder.all_buttons()}"

    recorder.clear()
    await _feed(dp, bot, press(user.id, start))
    assert any(b.startswith("answer_") for b in recorder.buttons()), (
        f"знакомство не довело до первого вопроса: {recorder.buttons()}"
    )


async def test_start_for_a_returning_person_is_the_intro_block(session, user, stage):
    """
    `/start` — ЭТО ПРИВЕТСТВИЕ, и одинаковое для всех.

    Разделения по числу кругов тут нет, и это проверено дважды на живом
    человеке. Сперва играющего вело на экран шкал — «что-то ты не то
    сделал, теперь при /start вызывает статистику». Потом на короткую
    строку «С возвращением» — «СТОП, прошлый старт был ПРАВИЛЬНЫМ... Верни
    старт!», и отдельно: «старт — это приветствие, оно было правильное».

    ПРЕЖДЕ ЭТОТ ТЕСТ БЫЛ ПУСТЫМ. Он искал в тексте «GenauLingua» (ключ
    `intro_title`) и находил имя не во вступлении, а в ЯКОРЕ — строке
    состояния под экраном. Стоило убрать имя из якоря, и тест упал, хотя
    вступление не менялось: он проверял чужой экран.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)
    # Вернувшийся человек знакомство ПРОШЁЛ — значит якорь с меню у него
    # уже был. Без якоря и без единого круга `/start` с 14 октября задаёт
    # заново второй вопрос знакомства («какой язык учить»): так выглядит
    # прервавший его на полпути, и прежде ему молча ставился немецкий.
    user.anchor_message_id = 1
    await session.commit()

    await _feed(dp, bot, text_update(user.id, "/start"))

    everything = "\n".join(recorder.sent_texts())
    # Обращение берётся из ЧАТА (`message.chat.first_name`), а не из ряда
    # человека: во вступлении здороваются с тем, кто пишет. В поддельном
    # обновлении имени чата нет, поэтому срабатывает запасное слово из
    # локали — то самое, которое увидит турок без имени в профиле.
    greeting = get_text("welcome_title", "ru",
                        name=get_text("friend_fallback", "ru"))
    assert greeting.strip("<b/> ") in everything, (
        f"/start не дал приветствия: {everything[:160]!r}"
    )
    assert get_text("intro_games", "ru").split(":")[0] in everything, (
        "вступление не говорит, чем бот занимается"
    )
    assert lesson_button(recorder.all_buttons()), "из вступления не начать занятие"

    # И вступление не обещает кнопку, которой в меню нет
    assert get_text("btn_help", "ru") not in everything, (
        "вступление снова обещает «Помощь» среди кнопок меню"
    )


# ============================================================================
# ДОСКА СОПОСТАВЛЕНИЯ — ЧЕТВЁРТАЯ ИГРА
#
# У доски своё состояние и свои нажатия, и проверять её надо так же, как
# круг: не «собралась ли», а ПРОХОДИТСЯ ли до конца. Проверка клавиатуры
# скажет, что кнопки на месте; только проход покажет, что нажатия доходят,
# пары сходятся, а доска доигрывается до итога.
# ============================================================================

async def _board_ready(session, user, *, words: int = 12) -> None:
    """Человек со знакомыми короткими словами — доске есть из чего собраться."""
    from app.database.models import UserWord
    from sqlalchemy import select

    for i in range(words):
        session.add(make_word(f"Haus{i:02d}", level=CEFRLevel.A1, ru=f"дом{i:02d}"))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.audio_enabled = False
    await session.commit()

    for word in (await session.execute(select(Word))).scalars().all():
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            correct_streak=1, times_shown=2, times_correct=2, learned=False,
        ))
    await session.commit()


def _cells(recorder) -> list[str]:
    return [b for b in recorder.buttons() if b.startswith("mt:")]


async def test_board_opens_from_the_home_screen(session, user, stage):
    from app.locales import get_text

    dp, bot, recorder = stage
    await _board_ready(session, user)

    # ВХОДА С ЭКРАНА ЧИСЕЛ БОЛЬШЕ НЕТ: доска — отдельная игра, а там только
    # числа. Обработчик жив и проверяется напрямую — именно так его вызовет
    # старая клавиатура из переписки.
    recorder.clear()
    await _feed(dp, bot, press(user.id, "match_start"))

    cells = _cells(recorder)
    assert len(cells) == 10, f"доска не 5×2: {cells}"
    assert sum(1 for c in cells if c.startswith("mt:l:")) == 5
    assert sum(1 for c in cells if c.startswith("mt:r:")) == 5


async def test_board_is_playable_to_the_end(session, user, stage):
    """
    Главный сценарий доски: все пять пар сходятся, доска доигрывается.

    Верная пара ищется через состояние: правая колонка — перестановка, и
    угадывать её снаружи значило бы проверять случай, а не игру.
    """
    dp, bot, recorder = stage
    await _board_ready(session, user)
    await _feed(dp, bot, press(user.id, "match_start"))

    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    for step in range(5):
        data = await context.get_data()
        order = data["match_right"]
        matched = data["match_matched"]
        version = data["match_version"]

        left_row = next(i for i in range(5) if i not in matched)
        right_row = order.index(left_row)

        await _feed(dp, bot, press(user.id, f"mt:l:{left_row}:{version}"))
        data = await context.get_data()
        await _feed(dp, bot, press(user.id, f"mt:r:{right_row}:{data['match_version']}"))

        data = await context.get_data()
        assert left_row in data["match_matched"], (
            f"шаг {step + 1}: верная пара не сошлась"
        )
        assert data["match_errors"] == 0, f"шаг {step + 1}: промах на верной паре"

    from app.locales import get_text

    everything = "\n".join(recorder.sent_texts())
    assert get_text("match_done", "ru").strip("🧩<b/>! ") in everything, (
        f"доска не кончилась итогом: {recorder.last_text()[:80]!r}"
    )
    assert "match_start" in recorder.all_buttons(), "из итога не начать новую доску"


async def test_wrong_pair_is_counted_and_board_goes_on(session, user, stage):
    dp, bot, recorder = stage
    await _board_ready(session, user)
    await _feed(dp, bot, press(user.id, "match_start"))

    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    data = await context.get_data()
    order = data["match_right"]
    version = data["match_version"]

    # Берём ряд справа, который НЕ является парой к левому ряду 0
    wrong_row = next(row for row in range(5) if order[row] != 0)

    await _feed(dp, bot, press(user.id, f"mt:l:0:{version}"))
    data = await context.get_data()
    await _feed(dp, bot, press(user.id, f"mt:r:{wrong_row}:{data['match_version']}"))

    data = await context.get_data()
    assert data["match_errors"] == 1, "промах не сосчитан"
    assert data["match_matched"] == [], "неверная пара сошлась"
    assert 0 in data["match_missed"], "промах не отмечен на левом слове"
    assert order[wrong_row] in data["match_missed"], "промах не отмечен на правом"
    assert data["match_selected"] == "", "выбор не снят после промаха"


async def test_tapping_the_same_side_moves_the_choice(session, user, stage):
    """
    Требование владельца: тыкать можно с любой стороны. Повторное нажатие
    по той же стороне — передумал, а не ошибся: промахом это считать нельзя.
    """
    dp, bot, recorder = stage
    await _board_ready(session, user)
    await _feed(dp, bot, press(user.id, "match_start"))

    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    data = await context.get_data()

    await _feed(dp, bot, press(user.id, f"mt:l:0:{data['match_version']}"))
    data = await context.get_data()
    await _feed(dp, bot, press(user.id, f"mt:l:3:{data['match_version']}"))

    data = await context.get_data()
    assert data["match_selected"] == "l:3", "выбор не перенёсся"
    assert data["match_errors"] == 0, "перенос выбора сосчитан промахом"


async def test_stale_tap_is_ignored(session, user, stage):
    """
    Нажатие с устаревшей версией отбрасывается. Человек может тыкнуть
    быстрее, чем придёт ответ, и тогда второе нажатие обработало бы уже
    изменившуюся доску — выглядело бы как «кнопка сработала сама».
    """
    dp, bot, recorder = stage
    await _board_ready(session, user)
    await _feed(dp, bot, press(user.id, "match_start"))

    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await _feed(dp, bot, press(user.id, "mt:l:0:0"))
    after_first = await context.get_data()
    assert after_first["match_selected"] == "l:0"

    # Та же версия, что была до первого нажатия, — уже устарела
    await _feed(dp, bot, press(user.id, "mt:l:2:0"))

    data = await context.get_data()
    assert data["match_selected"] == "l:0", "устаревшее нажатие изменило доску"


async def test_board_refuses_when_there_are_too_few_familiar_words(session, user, stage):
    """
    Новичку доска отказывает, а не собирается из двух пар: там обе
    бесплатны, и упражнение превращается в бессмыслицу.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _board_ready(session, user, words=2)

    await _feed(dp, bot, press(user.id, "match_start"))

    assert not _cells(recorder), "доска собралась из двух пар"

    # Аргументы передаются: у строки есть {need} и {have}, и без них
    # get_text честно вернёт «[ERROR: …]» — на этом первая редакция теста и
    # упала, объявив сбоем совершенно верное сообщение бота
    from app.services.match_service import BOARD_SIZE

    expected = get_text("match_not_ready", "ru", need=BOARD_SIZE, have=2)
    everything = "\n".join(recorder.sent_texts())
    assert expected in everything, f"нет честного отказа: {everything[:120]!r}"


# ============================================================================
# 🧩 ДОСКА ВНУТРИ КРУГА
#
# Доска занимает РОВНО ОДИН вопрос, внутри которого пять подвопросов, —
# поправка владельца к моей первой редакции на пять слотов: «Зачем ломать
# юзеру порядок 6 7 8?» Здесь и проверяется, что счёт идёт подряд и доска
# возвращает круг на том же номере.
#
# Что доска при этом ПИШЕТСЯ в круг — баллы, точность, ошибки, жалоба —
# держит отдельный файл `tests/test_board_in_round.py`: это другой вопрос,
# и приёмка сборки доски была чиста, пока он отвечался «никак».
# ============================================================================

async def _long_round_ready(session, user) -> None:
    """Круг из 15 и запас знакомых коротких слов — доске есть где встать."""
    from app.database.models import UserWord
    from sqlalchemy import select

    for i in range(60):
        session.add(make_word(f"Haus{i:02d}", level=CEFRLevel.A1, ru=f"дом{i:02d}"))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = 15
    user.audio_enabled = False
    user.quiz_channels = "t"
    user.match_in_round = True
    user.quizzes_passed = 2  # чётное — доска положена; не 0: у новичка первое занятие короче (7)
    await session.commit()

    # Знакомыми делаем ПОЛОВИНУ: доске нужны отвеченные верно, а кругу —
    # ещё и новые, иначе он упрётся в исчерпание
    words = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    for word in words[:30]:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            correct_streak=1, times_shown=2, times_correct=2, learned=False,
        ))
    await session.commit()


async def test_board_appears_in_the_middle_of_the_round(session, user, stage):
    from app.locales import get_text
    from app.services.match_service import board_slot

    dp, bot, recorder = stage
    await _long_round_ready(session, user)
    start = board_slot(15)

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))

    # Идём до слота доски обычными вопросами
    for _ in range(start - 1):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        assert options, "вопрос не показан до доски"
        await _feed(dp, bot, press(user.id, options[0]))
        recorder.clear()
        await _feed(dp, bot, press(user.id, "next_question"))

    cells = [b for b in recorder.buttons() if b.startswith("mt:")]
    assert len(cells) == 10, (
        f"на вопросе {start} доски нет: {recorder.buttons()}"
    )


async def test_board_inside_a_round_does_not_break_the_counter(session, user, stage):
    """
    Доска — ОДИН вопрос, и счёт после неё идёт следующим по порядку.

    Поправка владельца к моей ошибке: первая редакция отдавала доске пять
    слотов, и счёт перескакивал с 5 на 11. «Зачем ломать юзеру порядок
    6 7 8?» — сломано было ровно то, что человек видит.
    """
    from app.locales import get_text
    from app.services.match_service import BOARD_SIZE, board_slot

    dp, bot, recorder = stage
    await _long_round_ready(session, user)
    start = board_slot(15)

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(start - 1):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        await _feed(dp, bot, press(user.id, options[0]))
        await _feed(dp, bot, press(user.id, "next_question"))

    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    assert (await context.get_data()).get("match_round_at") == start, (
        "доска не запомнила, куда возвращать круг"
    )

    # Решаем доску целиком
    for _ in range(BOARD_SIZE):
        data = await context.get_data()
        order, matched = data["match_right"], data["match_matched"]
        left_row = next(i for i in range(BOARD_SIZE) if i not in matched)
        right_row = order.index(left_row)
        await _feed(dp, bot, press(user.id, f"mt:l:{left_row}:{data['match_version']}"))
        data = await context.get_data()
        await _feed(dp, bot, press(user.id, f"mt:r:{right_row}:{data['match_version']}"))

    # Доска заняла ОДИН вопрос: счётчик стоит на нём, а не перескочил
    # пять. Порядок для человека остаётся непрерывным — 6, 7, 8
    data = await context.get_data()
    assert data["current_question"] == start, (
        f"счётчик после доски {data['current_question']}, а должен {start}"
    )
    assert not data.get("match_round_at"), "отметка возврата не снята"

    # И круг доигрывается до итога
    recorder.clear()
    await _feed(dp, bot, press(user.id, "next_question"))
    for _ in range(15):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        await _feed(dp, bot, press(user.id, options[0]))
        if "next_question" not in recorder.buttons():
            break
        await _feed(dp, bot, press(user.id, "next_question"))

    everything = "\n".join(recorder.sent_texts())
    assert get_text("quiz_completed", "ru").strip("🎉<b/> ") in everything, (
        f"круг с доской не доигрался: {recorder.last_text()[:90]!r}"
    )


async def test_only_one_board_per_round(session, user, stage):
    """
    Вторая доска превратила бы занятие в сопоставление с довеском из
    вопросов. Отметка в состоянии держит одну на круг.
    """
    from app.locales import get_text
    from app.services.match_service import BOARD_SIZE, board_slot

    dp, bot, recorder = stage
    await _long_round_ready(session, user)
    start = board_slot(15)

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(start - 1):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        await _feed(dp, bot, press(user.id, options[0]))
        await _feed(dp, bot, press(user.id, "next_question"))

    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    for _ in range(BOARD_SIZE):
        data = await context.get_data()
        order, matched = data["match_right"], data["match_matched"]
        left_row = next(i for i in range(BOARD_SIZE) if i not in matched)
        await _feed(dp, bot, press(user.id, f"mt:l:{left_row}:{data['match_version']}"))
        data = await context.get_data()
        await _feed(dp, bot, press(user.id, f"mt:r:{order.index(left_row)}:{data['match_version']}"))

    boards = 0
    await _feed(dp, bot, press(user.id, "next_question"))
    for _ in range(15):
        if [b for b in recorder.buttons() if b.startswith("mt:")]:
            boards += 1
            break
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        if not options:
            break
        await _feed(dp, bot, press(user.id, options[0]))
        if "next_question" not in recorder.buttons():
            break
        recorder.clear()
        await _feed(dp, bot, press(user.id, "next_question"))

    assert boards == 0, "в одном круге показались две доски"


async def test_board_is_skipped_when_switched_off(session, user, stage):
    from app.locales import get_text
    from app.services.match_service import board_slot

    dp, bot, recorder = stage
    await _long_round_ready(session, user)
    user.match_in_round = False
    await session.commit()
    start = board_slot(15)

    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(start - 1):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        await _feed(dp, bot, press(user.id, options[0]))
        recorder.clear()
        await _feed(dp, bot, press(user.id, "next_question"))

    assert not [b for b in recorder.buttons() if b.startswith("mt:")], (
        "доска показалась, хотя выключена"
    )
    assert [b for b in recorder.buttons() if b.startswith("answer_")], (
        "вместо доски не пришёл обычный вопрос"
    )


async def test_the_end_and_the_repeat_never_leave_only_the_anchor(session, user, stage):
    """
    Владелец, 15.10: «пропадает карточка и остаётся якорь, а потом появляется
    новая — как в начале, так и в конце». Итог занятия и первый вопрос
    повтора ошибок приходят РАНЬШЕ, чем удаляется прежнее сообщение.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)
    await _feed(dp, bot, text_update(user.id, get_text("btn_learn_words", "ru")))

    for number in range(ROUND_LENGTH):
        await _feed(dp, bot, press(user.id, await _wrong_answer(dp, bot, user.id, recorder)))
        if number == ROUND_LENGTH - 1:
            recorder.clear()
        await _feed(dp, bot, press(user.id, "next_question"))

    def first(names):
        return next(i for i, (n, _) in enumerate(recorder.calls) if n in names)

    sends = {"SendMessage", "SendAudio"}
    assert first(sends) < first({"DeleteMessage"}), (
        f"итог пришёл после удаления вопроса: {[n for n, _ in recorder.calls]}"
    )

    recorder.clear()
    await _feed(dp, bot, press(user.id, "repeat_errors"))
    assert first(sends) < first({"DeleteMessage"}), (
        f"повтор пришёл после удаления итога: {[n for n, _ in recorder.calls]}"
    )


@pytest.mark.parametrize("button", ["btn_learn_words", "btn_stats", "btn_rating", "btn_settings"])
async def test_menu_buttons_show_the_new_screen_before_removing_the_old(
    session, user, stage, button
):
    """
    Владелец, 15.10: «рейтинг и настройки более плавно работают… чтобы ты
    убедился, что работает всё очень приятно и правильно». Прежние сообщения
    (от старого якоря до нажатия) убираются ПОСЛЕ нового экрана: иначе, пока
    экран готовится, в чате остаётся один якорь.
    """
    from app.locales import get_text
    from app.services.monthly_leaderboard_service import get_or_create_current_season

    dp, bot, recorder = stage
    await _ready(session, user)
    await get_or_create_current_season(session)
    user.anchor_message_id = 1          # прежний якорь где-то выше
    await session.commit()

    update = text_update(user.id, get_text(button, "ru"))
    pressed_id = update.message.message_id
    recorder.clear()
    await _feed(dp, bot, update)

    names = [n for n, _ in recorder.calls]
    sends = [i for i, (n, _) in enumerate(recorder.calls) if n in ("SendMessage", "SendAudio")]
    old = [i for i, (n, p) in enumerate(recorder.calls)
           if n == "DeleteMessage" and p.get("message_id") != pressed_id]
    assert len(sends) >= 2, f"{button}: нет якоря и экрана — {names}"
    assert old, f"{button}: прежние сообщения не убраны — {names}"
    assert sends[1] < old[0], f"{button}: экран пришёл после удаления — {names}"


@pytest.mark.parametrize("door", ["learn_now:home", "learn_now:again", "learn_now:reminder"])
async def test_starting_from_a_screen_removes_it_after_the_first_card(session, user, stage, door):
    """Домашний экран, итог, напоминание: занятие встаёт на их место без пустого чата."""
    dp, bot, recorder = stage
    await _ready(session, user)
    user.anchor_message_id = 1
    await session.commit()

    recorder.clear()
    await _feed(dp, bot, press(user.id, door, message_id=50))

    names = [n for n, _ in recorder.calls]
    card = next(i for i, (n, _) in enumerate(recorder.calls)
                if n in ("SendMessage", "SendAudio")
                and any((b.get("callback_data") or "").startswith("answer_")
                        for row in ((recorder.calls[i][1].get("reply_markup") or {})
                                    .get("inline_keyboard") or []) for b in row))
    gone = [i for i, (n, p) in enumerate(recorder.calls)
            if n == "DeleteMessage" and p.get("message_id") == 50]
    assert gone, f"{door}: экран не убран — {names}"
    assert card < gone[0], f"{door}: экран убран раньше карточки — {names}"
