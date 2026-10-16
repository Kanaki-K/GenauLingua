"""
Выбор языка: знакомство в три нажатия, /language и «Язык бота» в настройках.

Живой случай 16.10: человек выбрал не тот язык и не смог его сменить.
Три причины, каждую держит свой тест:
  * язык писался в базу первым же нажатием, а на экране 2 не было «Назад»;
  * команды /language не было, а смена лежала на третьем уровне настроек
    под чужим именем, подписанная на языке, которого человек не понимает;
  * ничто не говорило ему, что язык выбран не тот.
"""
import pytest

from app.database.models import User
from app.locales import LOCALES, get_text
from app.services.language_service import (
    INTERFACE_LANGS, LANGUAGES, LEARNABLE_LANGS, SUPPORTED_LANGS, is_learnable,
)
from tests.conftest import build_groups, make_word
from tests.scenario import make_bot, make_dispatcher, press, reset_state, text_update

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


async def _feed(dp, bot, update):
    await dp.feed_update(bot, update)


def _rows(recorder) -> list[list[str]]:
    """Ряды последней инлайн-клавиатуры — `callback_data` по рядам."""
    for _, payload in reversed(recorder.calls):
        markup = payload.get("reply_markup")
        if isinstance(markup, dict) and markup.get("inline_keyboard"):
            return [[b.get("callback_data") for b in row] for row in markup["inline_keyboard"]]
    return []


async def _newcomer(session, user) -> None:
    user.interface_language = None

    await session.commit()


# ============================================================================
# ЭКРАН 1
# ============================================================================

async def test_first_screen_has_one_prompt_per_line_in_button_order(session, user, stage):
    dp, bot, recorder = stage
    await _newcomer(session, user)

    await _feed(dp, bot, text_update(user.id, "/start"))
    text = recorder.last_text()
    lines = text.split("\n")[2:]
    assert lines == [LOCALES[c]["start_pick_language"] for c in INTERFACE_LANGS], text
    assert "·" not in text, "призывы снова склеены в ряд"
    assert [b for row in _rows(recorder) for b in row] == [
        f"select_lang_{c}" for c in INTERFACE_LANGS
    ]


def test_language_order_is_grouped():
    """Украинский первым, русский последним; закрытые встают на свои места."""
    from app.services.language_service import LANGUAGE_ORDER

    assert LANGUAGE_ORDER[0] == "uk" and LANGUAGE_ORDER[-1] == "ru"
    assert set(LANGUAGE_ORDER) == set(SUPPORTED_LANGS)
    assert list(INTERFACE_LANGS) == [c for c in LANGUAGE_ORDER if c in INTERFACE_LANGS]


# ============================================================================
# ЭКРАН 2
# ============================================================================

async def test_first_tap_writes_nothing_and_screen_two_has_back(session, user, stage):
    dp, bot, recorder = stage
    await _newcomer(session, user)

    await _feed(dp, bot, press(user.id, "select_lang_ru"))
    await session.refresh(user)
    assert user.interface_language is None, "язык записан до выбора изучаемого"

    text = recorder.last_text()
    assert text.startswith(get_text("onboard_your_lang", "ru", language="Русский")), text
    assert "/language" in text

    rows = _rows(recorder)
    assert rows[-1][0] == "onboard_back", f"«Назад» не слева в последнем ряду: {rows}"
    assert all(len(row) == 2 for row in rows), f"ряды неполные: {rows}"
    assert "onboard_learn_ru:ru" not in sum(rows, []), "свой язык предложен к изучению"


async def test_back_returns_to_first_screen(session, user, stage):
    dp, bot, recorder = stage
    await _newcomer(session, user)

    await _feed(dp, bot, press(user.id, "select_lang_ru"))
    recorder.clear()
    await _feed(dp, bot, press(user.id, "onboard_back"))
    assert any(b.startswith("select_lang_") for b in recorder.buttons())
    await session.refresh(user)
    assert user.interface_language is None


async def test_second_tap_writes_both_languages(session, user, stage):
    dp, bot, recorder = stage
    for i in range(30):
        session.add(make_word(f"Neu{i:03d}"))
    await build_groups(session, ["de"])
    await _newcomer(session, user)

    await _feed(dp, bot, press(user.id, "select_lang_uk"))
    await _feed(dp, bot, press(user.id, "onboard_learn_de:uk"))
    await session.refresh(user)
    assert (user.interface_language, user.native_lang, user.learning_lang) == ("uk", "uk", "de")

    intro = "\n".join(recorder.sent_texts())
    assert "Ви вивчаєте німецьку з перекладом українською." in intro
    assert "/language" in intro


async def test_learning_own_language_is_refused(session, user, stage):
    dp, bot, recorder = stage
    await _newcomer(session, user)
    await _feed(dp, bot, press(user.id, "onboard_learn_ru:ru"))
    await session.refresh(user)
    assert user.interface_language is None


@pytest.mark.parametrize("phone,shown", [
    ("en", True), ("en-GB", True), ("ru", False), (None, False), ("pt", False),
])
async def test_phone_language_hint(session, user, stage, phone, shown):
    dp, bot, recorder = stage
    await _newcomer(session, user)

    await _feed(dp, bot, press(user.id, "select_lang_ru", language_code=phone))
    text = recorder.last_text()
    hint = get_text("onboard_phone_hint", "en", back=get_text("btn_back", "ru"))
    assert (hint in text) is shown, text


# ============================================================================
# ЗАКРЫТЫЕ ЯЗЫКИ (Н2)
# ============================================================================

@pytest.fixture
def one_closed(monkeypatch):
    """
    Закрыть один язык на время теста. С 16.10 открыты все десять, но
    правило «закрытый язык не выбрать» нужно и дальше: следующий язык
    будет добавляться так же — сперва в реестр, потом в открытые.
    """
    from app.services import language_service

    monkeypatch.setattr(language_service, "LEARNABLE_LANGS",
                        tuple(c for c in LEARNABLE_LANGS if c != "cs"))
    return "cs"


def test_closed_language_is_not_learnable(one_closed):
    assert one_closed in LANGUAGES and not is_learnable(one_closed)


async def test_forged_tap_on_closed_language_is_refused(session, user, stage, one_closed):
    dp, bot, recorder = stage
    await _feed(dp, bot, press(user.id, f"set_learning_{one_closed}"))
    await _feed(dp, bot, press(user.id, f"onboard_learn_{one_closed}:ru"))
    await session.refresh(user)
    assert user.learning_lang == "de"


def test_all_ten_languages_are_open():
    """16.10: все языки реестра выбираются и для бота, и для изучения."""
    assert set(LEARNABLE_LANGS) == set(LANGUAGES) == set(INTERFACE_LANGS)


# ============================================================================
# /language И НАСТРОЙКИ
# ============================================================================

async def test_language_command_marks_current_and_confirms(session, user, stage):
    dp, bot, recorder = stage

    await _feed(dp, bot, text_update(user.id, "/language"))
    assert "chlang_uk:c" in recorder.buttons()
    assert any(t.startswith("✓ ") and "Русский" in t for t in recorder.button_texts())

    recorder.clear()
    await _feed(dp, bot, press(user.id, "chlang_uk:c"))
    await session.refresh(user)
    assert (user.interface_language, user.native_lang, user.learning_lang) == ("uk", "uk", "de")

    text = recorder.last_text()
    assert get_text("lang_progress_kept", "uk") in text
    assert recorder.buttons() == ["chdone:c", "settings_learning"]


async def test_new_language_equal_to_learning_asks_learning_again(session, user, stage):
    dp, bot, recorder = stage

    await _feed(dp, bot, press(user.id, "chlang_de:c"))
    await session.refresh(user)
    assert user.interface_language == "ru", "записано до выбора изучаемого"
    assert "chlearn_en:de:c" in recorder.buttons()
    assert "chback:c" in recorder.buttons()

    await _feed(dp, bot, press(user.id, "chlearn_en:de:c"))
    await session.refresh(user)
    assert (user.interface_language, user.native_lang, user.learning_lang) == ("de", "de", "en")


async def test_settings_item_opens_the_same_screen(session, user, stage):
    dp, bot, recorder = stage

    await _feed(dp, bot, press(user.id, "settings_language"))
    buttons = recorder.buttons()
    assert "chlang_ru:s" in buttons and buttons[-1] == "settings_group_bot"
    # Подписи — на самих языках, а не на языке человека
    assert "Українська" in recorder.button_texts()


async def test_settings_summary_names_the_learning_language(session, user):
    from app.bot.handlers.quiz.settings import _settings_text

    assert get_text("langname_de", "ru") in _settings_text(user, "ru")


def test_one_name_for_the_bot_language():
    """Н12: пункт настроек и строка состояния зовут одну вещь одинаково."""
    for code, texts in LOCALES.items():
        label = texts["settings_btn_change_language"]
        assert texts["settings_language"].startswith(label), code


# ============================================================================
# ФОРМЫ НАЗВАНИЙ И МЕНЮ КОМАНД
# ============================================================================

def test_language_forms_cover_every_locale_and_language():
    from app.locales.language_forms import FORMS

    assert set(FORMS) == set(LOCALES)
    for locale, places in FORMS.items():
        for place in ("learn", "into"):
            assert set(places[place]) == set(SUPPORTED_LANGS), (locale, place)


def test_command_menu_has_language_in_every_interface_language():
    from app.bot.commands import commands_for

    for lang in INTERFACE_LANGS:
        commands = {c.command: c.description for c in commands_for(lang)}
        assert "language" in commands, lang
        assert not any(d.startswith("[") for d in commands.values()), (lang, commands)
