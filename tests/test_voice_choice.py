# -*- coding: utf-8 -*-
"""
ВЫБОР ГОЛОСА: слушать — это не выбирать.

ОТКУДА ЭТИ ПРОВЕРКИ. Владелец перебрал голоса подряд, чтобы сравнить, и
получил не тот, что понравился: «выбрал Серафину — в настройках бота один
голос, а в игре другой». В журнале видно, что произошло, — пять сохранений
за двадцать восемь секунд:

    02:42:32  Катя      INSERT
    02:42:39  Амала     UPDATE
    02:42:46  Серафина  UPDATE
    02:42:55  Конрад    UPDATE
    02:43:00  Килиан    UPDATE

Нажатие совмещало прослушивание и выбор, и выигрывало ПОСЛЕДНЕЕ нажатие, а
не выбор человека. Текст экрана при этом был верен: «нажми на голос, чтобы
послушать; галочкой отмечен выбранный». Врал не текст, а код — и ни один
тест этого не видел, потому что проверять было нечего: оба действия были
одним обработчиком.

Проверяется через НАСТОЯЩИЙ диспетчер: дефект жил в обработчике, а не в
функции, и тест на функцию его бы не нашёл.
"""

import pytest

from app.database.models import UserTtsVoice
from app.services.audio_service import voice_for_user
from app.services.tts_voices import VOICES, default_voice
from tests.scenario import make_bot, make_dispatcher, press, reset_state

pytestmark = pytest.mark.asyncio

LANG = "de"
# Любой голос, кроме умолчания: иначе «не сохранилось» и «сохранилось
# верное» были бы неотличимы
OTHER = next(v.name for v in VOICES[LANG] if v.name != default_voice(LANG))


@pytest.fixture
async def stage(session, user):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    user.learning_lang = LANG
    user.native_lang = "ru"
    user.interface_language = "ru"
    user.audio_enabled = True
    await session.commit()
    recorder.clear()
    return dp, bot, recorder, user


async def _saved(session, user_id: int) -> str | None:
    row = await session.get(UserTtsVoice, (user_id, LANG))
    return row.voice if row else None


async def test_listening_does_not_choose(stage, session):
    """
    Главное. Нажатие на голос ничего не сохраняет.

    Сломай это — и вернётся ровно тот дефект: человек слушает пять голосов
    и получает последний.
    """
    dp, bot, rec, user = stage

    await dp.feed_update(bot, press(user.id, f"audio_voice_{OTHER}"))

    assert await _saved(session, user.id) is None, (
        "прослушивание сохранило голос — слушать снова значит выбирать"
    )
    assert await voice_for_user(session, user.id, LANG) == default_voice(LANG)


async def test_listening_offers_a_choice_button(stage):
    """
    Послушал — появилась кнопка «Выбрать: <голос>». Без неё выбрать
    голос стало бы нельзя вообще, и правка превратила бы один дефект в
    другой, хуже.
    """
    dp, bot, rec, user = stage

    await dp.feed_update(bot, press(user.id, f"audio_voice_{OTHER}"))

    assert f"voice_use_{OTHER}" in rec.all_buttons(), (
        f"кнопки выбора нет: {rec.all_buttons()}"
    )


async def test_the_choice_button_saves(stage, session):
    """Выбор сохраняется — и именно тот голос, который выбрали."""
    dp, bot, rec, user = stage

    await dp.feed_update(bot, press(user.id, f"audio_voice_{OTHER}"))
    await dp.feed_update(bot, press(user.id, f"voice_use_{OTHER}"))

    assert await _saved(session, user.id) == OTHER
    assert await voice_for_user(session, user.id, LANG) == OTHER


async def test_listening_many_then_choosing_one(stage, session):
    """
    ТОТ САМЫЙ СЛУЧАЙ ЦЕЛИКОМ: послушать все голоса подряд и выбрать не
    последний, а второй. Должен сохраниться второй.
    """
    dp, bot, rec, user = stage
    names = [v.name for v in VOICES[LANG]]
    assert len(names) >= 3, "для случая нужно хотя бы три голоса"

    for name in names:
        await dp.feed_update(bot, press(user.id, f"audio_voice_{name}"))

    assert await _saved(session, user.id) is None, (
        "перебрав голоса, человек уже что-то «выбрал» — это и был дефект"
    )

    wanted = names[1]
    await dp.feed_update(bot, press(user.id, f"audio_voice_{wanted}"))
    await dp.feed_update(bot, press(user.id, f"voice_use_{wanted}"))

    assert await _saved(session, user.id) == wanted


async def test_chosen_voice_is_marked_on_the_screen(stage, session):
    """
    Выбранный голос помечен ✓, и это единственный способ узнать его с
    экрана. Пометка «слушаешь» — 🎧, и путать их нельзя.
    """
    dp, bot, rec, user = stage

    await dp.feed_update(bot, press(user.id, f"audio_voice_{OTHER}"))
    await dp.feed_update(bot, press(user.id, f"voice_use_{OTHER}"))
    rec.clear()
    await dp.feed_update(bot, press(user.id, "audio_voices"))

    label = next(v.label for v in VOICES[LANG] if v.name == OTHER)
    texts = rec.button_texts()
    assert any(t.startswith("✓") and label in t for t in texts), (
        f"выбранный голос не помечен: {texts}"
    )
    assert not any(t.startswith("🎧") for t in texts), (
        "на свежем экране кто-то помечен как слушаемый"
    )


async def test_choice_button_is_absent_for_the_current_voice(stage, session):
    """
    «Выбрать» не предлагается для уже выбранного голоса: кнопка без
    действия — это обещание, которого нет.
    """
    dp, bot, rec, user = stage
    current = default_voice(LANG)

    await dp.feed_update(bot, press(user.id, f"audio_voice_{current}"))

    assert f"voice_use_{current}" not in rec.all_buttons(), (
        "предложено выбрать то, что уже выбрано"
    )


def test_voice_names_follow_the_interface_language():
    """
    «Voice: Катя» в английском интерфейсе — находка обхода шести языков
    14 октября. Латинское имя берётся из идентификатора движка.
    """
    from app.services.tts_voices import VOICES

    by_name = {v.name: v for group in VOICES.values() for v in group}
    katja = by_name["de-DE-KatjaNeural"]
    assert katja.shown("ru") == "Катя"
    for lang in ("en", "de", "pl", "tr"):
        assert katja.shown(lang) == "Katja"
    assert by_name["de-DE-SeraphinaMultilingualNeural"].shown("en") == "Seraphina"
    assert by_name["uk-UA-PolinaNeural"].shown("uk") == "Поліна"
    for voice in by_name.values():
        for lang in ("en", "de", "pl", "tr"):
            shown = voice.shown(lang)
            assert shown and not any("А" <= ch <= "я" for ch in shown), (voice.name, lang, shown)
