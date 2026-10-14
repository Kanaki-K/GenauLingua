"""
Куда попадает человек, поправивший трудность ПОСЛЕ ЗАНЯТИЯ.

ЧТО СЛОМАЛОСЬ. Согласие на новый уровень и выбор уровня или темы из итога
вели на «домашний экран» — а домашний экран давно стал экраном статистики:
кнопку занятия с него убрали решением владельца. Человек, поправивший
трудность ради следующего занятия, попадал в цифры о себе с одной кнопкой
«Подробнее». Ровно это владелец и описал 14 октября: «попадаю в
статистику». Обход шести языков воспроизвёл это на всех шести.

Вторая половина того же: тема менялась на месте, и над экраном оставался
висеть итог с прежней темой и его «Ещё занятие», а уровень — под свежим
якорем с зачисткой. Одно действие вело себя двумя способами.

Здесь держится одно правило: из итога — подтверждение и ровно одна кнопка
«Ещё занятие», под свежим якорем, чат чист. Из настроек — как было.

И отдельно — «Да, напоминать»: ответ называл время «по Вашему времени»,
хотя пояс никто не спрашивал и у каждого по умолчанию Берлин.
"""

import re

import pytest

from app.database.enums import CEFRLevel, QuizMode
from app.locales import get_text
from app.testing import make_bot, make_dispatcher, press, reset_state

LESSON_AGAIN = "learn_now:again"


async def _dispatch(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


def _screens(recorder):
    """Сообщения и правки, у которых есть инлайн-кнопки."""
    out = []
    for name, payload in recorder.calls:
        if name not in ("SendMessage", "EditMessageText"):
            continue
        rows = (payload.get("reply_markup") or {}).get("inline_keyboard") or []
        if rows:
            out.append((payload.get("text") or "",
                        [b.get("callback_data") for row in rows for b in row]))
    return out


def _deleted(recorder):
    return {p["message_id"] for n, p in recorder.calls if n == "DeleteMessage"}


# ============================================================================
# СОГЛАСИЕ НА УРОВЕНЬ
# ============================================================================

async def test_level_agreement_leads_to_the_next_lesson_not_to_statistics(session, user):
    user.level = CEFRLevel.A1
    user.anchor_message_id = 990
    await session.commit()
    dp, bot, recorder = await _dispatch(session)

    await dp.feed_update(bot, press(user.id, "level_up_A2", message_id=995))

    screens = _screens(recorder)
    assert len(screens) == 1, screens
    text, buttons = screens[0]
    assert text == get_text("level_offer_done", "ru", following="A2"), text
    assert buttons == [LESSON_AGAIN], f"вместо кнопки занятия: {buttons}"
    assert {990, 995} <= _deleted(recorder)


async def test_stale_agreement_says_nothing_and_changes_nothing(session, user):
    # Человек уже сам перешёл на B1, а в переписке висит «Да, на A2»:
    # прежде под ней писалось «Уровень A2», хотя уровень не менялся
    user.level = CEFRLevel.B1
    await session.commit()
    dp, bot, recorder = await _dispatch(session)

    await dp.feed_update(bot, press(user.id, "level_up_A2", message_id=995))

    await session.refresh(user)
    assert user.level == CEFRLevel.B1
    assert _screens(recorder) == [], "устаревшая кнопка показала экран"
    assert 995 in _deleted(recorder)


async def test_stale_refusal_does_not_refuse_the_next_level(session, user):
    # Отказ от «A1 → A2», нажатый уже на A2, не отказ от B1
    user.level = CEFRLevel.A2
    user.level_offer_declined = None
    await session.commit()
    dp, bot, recorder = await _dispatch(session)

    await dp.feed_update(bot, press(user.id, "level_up_no_A2", message_id=995))

    await session.refresh(user)
    assert user.level_offer_declined is None
    assert 995 in _deleted(recorder)


async def test_refusal_button_names_the_offered_level(session, user):
    user.level = CEFRLevel.A1
    await session.commit()
    dp, bot, recorder = await _dispatch(session)

    await dp.feed_update(bot, press(user.id, "level_up_no_A2", message_id=995))

    await session.refresh(user)
    assert user.level_offer_declined == "A1"


# ============================================================================
# ВЫБОР ИЗ ИТОГА: УРОВЕНЬ И ТЕМА ВЕДУТ СЕБЯ ОДИНАКОВО
# ============================================================================

@pytest.mark.parametrize("data, mode, done_key", [
    ("qmode_set_level_B1:result", QuizMode.LEVEL, "qmode_level_set"),
    ("qmode_all:result", QuizMode.ALL_WORDS, "qmode_all_set"),
    ("qmode_difficult:result", QuizMode.DIFFICULT, "qmode_difficult_set"),
    ("qmode_set_cat_ESSEN_TRINKEN:result", QuizMode.CATEGORY, "qmode_category_set"),
])
async def test_a_choice_from_the_result_cleans_the_chat_and_offers_a_lesson(
    session, user, data, mode, done_key,
):
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.anchor_message_id = 990          # якорь над итогом занятия
    await session.commit()
    dp, bot, recorder = await _dispatch(session)

    # Экран уровня и тем — сообщение 996 под итогом 993
    await dp.feed_update(bot, press(user.id, data, message_id=996))

    await session.refresh(user)
    assert user.quiz_mode == mode
    deleted = _deleted(recorder)
    # Итог с прежней трудностью устарел: якорь переезжает и забирает его
    assert {990, 993, 996} <= deleted, sorted(deleted)
    assert user.anchor_message_id not in deleted

    screens = _screens(recorder)
    assert len(screens) == 1, screens
    text, buttons = screens[0]
    assert text.startswith("✓"), text
    assert get_text(done_key, "ru", level="B1", category="")[:8] in text, text
    assert buttons == [LESSON_AGAIN], f"вместо кнопки занятия: {buttons}"

    # Подтверждение — текстом экрана, а не вторым разом во всплывающем окне
    alerts = [p for n, p in recorder.calls if n == "AnswerCallbackQuery" and p.get("show_alert")]
    assert not alerts, alerts


async def test_the_same_choice_from_settings_still_returns_to_settings(session, user):
    """Из настроек правило прежнее: окно с подтверждением и экран настроек."""
    user.anchor_message_id = 990
    await session.commit()
    dp, bot, recorder = await _dispatch(session)

    await dp.feed_update(bot, press(user.id, "qmode_all", message_id=996))

    alerts = [p for n, p in recorder.calls if n == "AnswerCallbackQuery" and p.get("show_alert")]
    assert alerts and alerts[0]["text"] == get_text("qmode_all_set", "ru")
    screens = _screens(recorder)
    assert screens and LESSON_AGAIN not in screens[-1][1]
    assert not _deleted(recorder), "из настроек чат зачищаться не должен"


# ============================================================================
# «ДА, НАПОМИНАТЬ»: ПОЯС НАЗВАН, А НЕ ПОДРАЗУМЕВАЕТСЯ
# ============================================================================

@pytest.mark.parametrize("lang, city", [
    ("ru", "Берлин"), ("uk", "Берлін"), ("en", "Berlin"),
    ("de", "Berlin"), ("pl", "Berlin"), ("tr", "Berlin"),
])
async def test_reminder_agreement_names_the_city_of_the_time_zone(session, user, lang, city):
    user.interface_language = lang
    user.timezone = "Europe/Berlin"
    await session.commit()
    dp, bot, recorder = await _dispatch(session)

    await dp.feed_update(bot, press(user.id, "reminder_offer_yes", message_id=960))

    await session.refresh(user)
    text = recorder.last_text()
    assert user.notification_time in text
    # С флагом — как на кнопке выбора города. Сырое «Europe/Berlin» тоже
    # содержит «Berlin», и без флага такая подмена прошла бы незамеченной
    assert f"🇩🇪 {city}" in text, f"пояс не назван: {text!r}"
    assert "Вашему времени" not in text and "Вашим часом" not in text


def test_time_zone_buttons_are_never_cyrillic_for_latin_interfaces():
    """
    Справочник городов знает ru/uk/en/tr, а немецкому и польскому прежде
    отдавал русские названия: «🇩🇪 Берлин» на немецком экране.
    """
    from app.bot.keyboards.notifications import (
        get_timezone_extended_keyboard, get_timezone_main_keyboard,
    )

    for lang in ("en", "de", "pl", "tr"):
        for keyboard in (get_timezone_main_keyboard(lang), get_timezone_extended_keyboard(lang)):
            labels = [b.text for row in keyboard.inline_keyboard for b in row]
            cyrillic = [t for t in labels if re.search(r"[А-Яа-яЁёІіЇїЄєҐґ]", t)]
            assert not cyrillic, f"{lang}: {cyrillic}"
