"""
Итальянский, испанский, французский, чешский — открыты 16.10. Путь целиком
на каждом из них: знакомство, первый урок, итог, настройки, /language.

Что ловится:
  * «[MISSING: …]» и «[ERROR: …]» — ключ или параметр забыт в локали;
  * КИРИЛЛИЦА в экранах латинского языка — значит, строка пришла из
    русской или украинской локали по запасному пути, а человек её не прочтёт;
  * учить новый язык со значениями на старом — тоже путь до итога.
"""
import re

import pytest

from app.database.enums import CEFRLevel
from app.database.models import User
from app.locales import get_text
from tests.conftest import build_groups, make_word
from tests.scenario import make_bot, make_dispatcher, press, reset_state, text_update

pytestmark = pytest.mark.asyncio

NEW = ("it", "es", "fr", "cs")
CYRILLIC = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")


async def _words(session, langs):
    # Значения на латинице у всех языков, кроме ru/uk: кириллица в экране
    # значит строку интерфейса, а не слово
    for i in range(40):
        session.add(make_word(
            f"Wort{i:02d}", level=CEFRLevel.A1,
            it=f"parola{i}", es=f"palabra{i}", fr=f"mot{i}", cs=f"slovo{i}",
            en=f"word{i}", pl=f"slowo{i}", tr=f"kelime{i}",
        ))
    await build_groups(session, langs)


def _check(texts: list[str], lang: str) -> None:
    # Имя человека (в тестах — «Тестовый») — данные, а не строка интерфейса:
    # с 17.10 оно стоит во второй строке якоря
    texts = [t.replace("Тестовый", "") for t in texts]
    for text in texts:
        assert "[MISSING" not in text and "[ERROR" not in text, (lang, text)
        assert not CYRILLIC.search(text), (lang, text)


async def _play(dp, bot, recorder, uid, context):
    for _ in range(12):
        data = await context.get_data()
        if data.get("match_words") and len(data.get("match_matched") or []) < len(data["match_words"]):
            order, matched = data["match_right"], data["match_matched"]
            left = next(i for i in range(len(order)) if i not in matched)
            await dp.feed_update(bot, press(uid, f"mt:l:{left}:{data['match_version']}"))
            data = await context.get_data()
            await dp.feed_update(bot, press(uid, f"mt:r:{order.index(left)}:{data['match_version']}"))
            continue
        if data.get("match_words"):
            # Доска решена — дальше итог; старая карточка уже удалена
            await dp.feed_update(bot, press(uid, "next_question"))
            break
        if "correct_word_id" not in data:
            break
        await dp.feed_update(bot, press(uid, f"answer_{data['correct_word_id']}"))
        if "next_question" not in recorder.buttons():
            break
        await dp.feed_update(bot, press(uid, "next_question"))


@pytest.mark.parametrize("lang", NEW)
async def test_whole_path_in_the_new_interface_language(session, lang):
    await _words(session, ["de"])
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    uid = 7000
    context = dp.fsm.get_context(bot, chat_id=uid, user_id=uid)

    await dp.feed_update(bot, text_update(uid, "/start", language_code=lang))
    assert f"select_lang_{lang}" in recorder.buttons()
    recorder.clear()
    await dp.feed_update(bot, press(uid, f"select_lang_{lang}", language_code=lang))
    await dp.feed_update(bot, press(uid, f"onboard_learn_de:{lang}", language_code=lang))
    person = await session.get(User, uid)
    await session.refresh(person)
    assert (person.interface_language, person.native_lang, person.learning_lang) == (lang, lang, "de")
    person.audio_enabled = False
    await session.commit()

    await dp.feed_update(bot, text_update(uid, get_text("btn_learn_words", lang)))
    await _play(dp, bot, recorder, uid, context)
    await dp.feed_update(bot, text_update(uid, get_text("btn_settings", lang)))
    for group in ("what", "how", "bot"):
        await dp.feed_update(bot, press(uid, f"settings_group_{group}"))
    await dp.feed_update(bot, text_update(uid, get_text("btn_stats", lang)))
    await dp.feed_update(bot, text_update(uid, "/language"))
    await dp.feed_update(bot, text_update(uid, "/help"))

    # Экран 1 многоязычный по замыслу — его из проверки кириллицы исключаем
    first = recorder.sent_texts()[0]
    _check([t for t in recorder.sent_texts() if t != first
            and "Українська" not in t and "Оберіть" not in t], lang)
    # Итог урока: каждое слово по разу (доска — свои три слова)
    summary = next(t for t in recorder.sent_texts() if "✓ 🧩" in t)
    rows = [line for line in summary.splitlines() if line.startswith(("✓", "✗"))]
    assert len(rows) == len(set(rows)) == 9, rows
    assert recorder.button_texts(), "последний экран без кнопок"


@pytest.mark.parametrize("learning", NEW)
async def test_learning_a_new_language_with_russian_meanings(session, user, learning):
    await _words(session, [learning])
    user.learning_lang = learning
    user.native_lang = "ru"
    user.level = CEFRLevel.A1
    user.audio_enabled = False
    await session.commit()

    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    data = await context.get_data()
    assert data.get("correct_word_id"), f"занятие по {learning} не началось: {recorder.sent_texts()[-1:]}"
    await _play(dp, bot, recorder, user.id, context)
    await session.refresh(user)
    assert user.quizzes_passed == 1, f"урок по {learning} не дошёл до итога"
    for text in recorder.sent_texts():
        assert "[MISSING" not in text and "[ERROR" not in text, text
