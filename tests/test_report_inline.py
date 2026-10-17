"""
Жалоба на разборе ответа (17.10): у каждого слова, а не в итоге занятия.

Владелец: «в конце игры уже просто можно не помнить что там было не так».
Проверяется путь целиком — разбор → «Сообщить об ошибке» → отметки →
«Отправить» → строки в базе с парой → решение админа по виду «пример».
"""
import pytest
from sqlalchemy import select

from app.bot.handlers.admin import _build_reports_text_and_keyboard
from app.bot.handlers.quiz import report_inline as ri
from app.database.models import TranslationReport, User
from app.locales import LOCALES, get_text
from tests.conftest import build_groups, make_word
from tests.scenario import make_bot, make_dispatcher, press, reset_state, text_update

pytestmark = pytest.mark.asyncio


async def _answered(session, user, native="ru"):
    for i in range(12):
        session.add(make_word(f"Wort{i:02d}"))
    await build_groups(session, ["de"])
    user.audio_enabled = False
    user.native_lang = native
    await session.commit()

    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    data = await context.get_data()
    word_id = data["correct_word_id"]
    await dp.feed_update(bot, press(user.id, f"answer_{word_id}"))
    return bot, recorder, dp, word_id


async def test_answer_card_offers_report_under_next(session, user):
    _, recorder, _, word_id = await _answered(session, user)
    buttons = recorder.buttons()
    # «Далее» — последней, под жалобой
    assert buttons[-1] == "next_question"
    # Звук выключен — озвучку не предлагаем: перевод и пример
    assert buttons[0] == f"rp:o:{word_id}:{ri.TEXT | ri.EXAMPLE}:0"


async def test_pick_and_send_writes_each_kind_with_the_pair(session, user):
    bot, recorder, dp, word_id = await _answered(session, user)
    avail = ri.TEXT | ri.EXAMPLE
    await dp.feed_update(bot, press(user.id, f"rp:o:{word_id}:{avail}:0"))
    assert f"rp:t:{word_id}:{avail}:{ri.TEXT}" in recorder.buttons()
    # «Отправить» появляется только после первой отметки
    assert not any(b.startswith("rp:s:") for b in recorder.buttons())
    await dp.feed_update(bot, press(user.id, f"rp:t:{word_id}:{avail}:{ri.TEXT}"))
    assert "✓ " + get_text("report_kind_text", "ru") in recorder.button_texts()
    await dp.feed_update(bot, press(user.id, f"rp:t:{word_id}:{avail}:{ri.TEXT | ri.EXAMPLE}"))
    await dp.feed_update(bot, press(user.id, f"rp:s:{word_id}:{avail}:{ri.TEXT | ri.EXAMPLE}"))

    rows = (await session.execute(select(TranslationReport))).scalars().all()
    assert sorted(r.kind for r in rows) == ["example", "text"]
    assert {(r.word_id, r.learning_lang, r.native_lang) for r in rows} == {(word_id, "de", "ru")}
    assert recorder.buttons()[-1] == "next_question"
    assert get_text("report_btn_sent", "ru") in recorder.button_texts()

    # Второе нажатие той же кнопки — без дублей
    await dp.feed_update(bot, press(user.id, f"rp:s:{word_id}:{avail}:{ri.TEXT | ri.EXAMPLE}"))
    assert len((await session.execute(select(TranslationReport))).scalars().all()) == 2


async def test_sel_outside_offer_is_ignored(session, user):
    bot, _, dp, word_id = await _answered(session, user)
    # Озвучку не предлагали — подделанная кнопка её не запишет
    await dp.feed_update(bot, press(user.id, f"rp:s:{word_id}:{ri.TEXT}:{ri.AUDIO | ri.TEXT}"))
    kinds = [r.kind for r in (await session.execute(select(TranslationReport))).scalars()]
    assert kinds == ["text"]


async def test_lesson_goes_on_after_a_report(session, user):
    bot, recorder, dp, word_id = await _answered(session, user)
    await dp.feed_update(bot, press(user.id, f"rp:s:{word_id}:{ri.TEXT}:{ri.TEXT}"))
    await dp.feed_update(bot, press(user.id, "next_question"))
    assert any(b.startswith("answer_") for b in recorder.buttons()), recorder.buttons()


async def test_admin_decides_example_separately(session, user):
    word = make_word("Haus")
    session.add(word)
    await session.commit()
    session.add(TranslationReport(user_id=user.id, word_id=word.id, kind="example",
                                  status="pending", learning_lang="de", native_lang="ru"))
    await session.commit()
    text, keyboard = await _build_reports_text_and_keyboard(session)
    assert "пример 1" in text
    data = [b.callback_data for row in keyboard.inline_keyboard for b in row]
    assert f"admin:report_approve_example_{word.id}" in data


async def test_summary_has_no_report_list_button():
    from app.bot.handlers.quiz.summary import get_results_keyboard

    data = [b.callback_data for row in get_results_keyboard(True, "ru").inline_keyboard for b in row]
    assert "report_translation_error" not in data


def test_new_keys_in_every_locale():
    for lang in LOCALES:
        for key in ("report_kind_text", "report_kind_example", "report_kind_audio",
                    "report_pick_hint", "report_btn_sent", "report_approved_example"):
            assert "[MISSING" not in get_text(key, lang), (lang, key)
        assert "[" not in get_text("report_sent_one", lang, points="1"), lang
