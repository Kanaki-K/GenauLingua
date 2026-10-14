"""
Настройки, собранные в три группы: ни один экран не потерялся.

Восемь равных пунктов перемешивали вещи разной природы — «что я учу»
меняют часто, «как мне удобно» ставят один раз, — и первым в списке стоял
режим викторины, которым не пользуются 96%. Пункты разложены по трём
группам: 🎯 что учу · 🎮 как учу · 🔧 бот.

ГЛАВНЫЙ РИСК ПЕРЕГРУППИРОВКИ — ПОТЕРЯННЫЙ ЭКРАН. Кнопка уезжает в группу,
а в группу её вписать забывают: экран остаётся в коде, обработчик жив,
тесты зелёные, и попасть на него нельзя ни одним нажатием. Снаружи это
выглядит как исчезнувшая настройка, и найти такое чтением кода почти
невозможно — отсутствие не бросается в глаза.

Поэтому проверяется не состав групп, а ДОСТИЖИМОСТЬ: каждый экран, который
был доступен из плоского списка, должен быть доступен и теперь, и у
каждого нажатия должен быть обработчик.
"""

from app.bot.handlers.quiz.settings import (
    _GROUPS,
    _PARENT_GROUP,
    _group_keyboard,
    get_settings_keyboard,
)
from app.locales import LOCALES, get_text

# Всё, что было достижимо из плоского списка настроек до перегруппировки.
# Список зафиксирован руками нарочно: вычисли его из того же `_GROUPS` — и
# проверка станет тавтологией, которая пройдёт даже если потерять половину.
WAS_REACHABLE = {
    "settings_quiz_mode",
    "settings_channels",
    "settings_learning",
    "settings_audio",
    "settings_mode",
    "settings_language",
    "settings:notifications",
    "settings_help",
    # Добавлено 12 октября вместе с опросом «зачем учишь». Без этого экрана
    # цель осталась бы пустой навсегда у всех 233 нынешних пользователей:
    # спрашивается она в онбординге, а он у них давно позади.
    "settings_goal",
    # Выключатель 🧩 доски в круге. Отдельно от состава занятия нарочно:
    # там каналы — способы задать вопрос про ОДНО слово, а доска берёт
    # пять сразу и каналом быть не может.
    "settings_match",
}


# Экраны, снятые НАРОЧНО, — с причиной на каждый.
#
# Из `WAS_REACHABLE` они не вычёркиваются: список описывает прошлое, и
# стирание из него превратило бы «мы это решили» в «мы это потеряли» —
# неотличимо через месяц. Отмеченный здесь экран перестаёт требоваться, но
# остаётся названным.
REMOVED_ON_PURPOSE = {
    # «Направление перевода» переворачивало ВСЕ пятнадцать вопросов круга и
    # было включено у 10 человек из 233. Обратная сторона стала пятой игрой
    # в составе занятия (`QuizChannel.REVERSE`), и два рычага на одно и то
    # же держать нельзя. Решение владельца: «реверс будет игрой 5, которая
    # логически будет расставлена среди 15ти вопросов».
    "settings_mode",
}


def _all_group_items() -> set[str]:
    return {data for _, _, items in _GROUPS.values() for _, data in items}


def test_no_screen_was_lost_in_the_regrouping():
    lost = WAS_REACHABLE - _all_group_items() - REMOVED_ON_PURPOSE
    assert not lost, f"экраны стали недостижимы: {sorted(lost)}"


def test_a_removed_screen_is_really_gone():
    """
    Снятый экран не должен остаться ЖИВЫМ и недостижимым.

    Это ровно та беда, что уже случилась: обработчик `settings_mode`
    остался в коде после правки состава групп, а его «Назад» читал
    `_PARENT_GROUP["settings_mode"]` — ключа, которого больше нет. Нажатие
    со старой клавиатуры упало бы с KeyError, и ни один тест этого не
    видел: кнопки на экранах уже не было.
    """
    import re
    from pathlib import Path

    source = (Path(__file__).resolve().parents[1]
              / "app" / "bot" / "handlers" / "quiz" / "settings.py"
              ).read_text(encoding="utf-8")

    for data in REMOVED_ON_PURPOSE:
        handler = re.search(
            rf'@router\.callback_query\(F\.data == "{re.escape(data)}"\)', source
        )
        assert handler is None, (
            f"экран {data} снят из групп, но обработчик жив — "
            f"нажатие со старой клавиатуры ведёт в недостижимый экран"
        )
        assert data not in _PARENT_GROUP, (
            f"{data} остался в таблице возврата"
        )


def test_no_screen_was_invented_out_of_nowhere():
    """
    Обратная половина: группа не обещает кнопку, которой не было. Длина
    круга — как раз такой случай: колонка `quiz_word_count` есть, экрана к
    ней нет, и кнопка привела бы в пустоту.
    """
    extra = _all_group_items() - WAS_REACHABLE
    assert not extra, f"в группах появились кнопки без экрана: {sorted(extra)}"


def test_every_screen_belongs_to_exactly_one_group():
    """
    Пункт в двух группах означает, что человек найдёт его в одном месте, а
    искать будет в другом. И «Назад» тогда ведёт не туда, откуда пришли.
    """
    seen: dict[str, str] = {}
    for key, (_, _, items) in _GROUPS.items():
        for _, data in items:
            assert data not in seen, (
                f"{data} и в группе {seen[data]}, и в группе {key}"
            )
            seen[data] = key


def test_back_from_every_screen_returns_to_its_own_group():
    for data, parent in _PARENT_GROUP.items():
        key = parent.removeprefix("settings_group_")
        assert key in _GROUPS, f"{data} возвращает в несуществующую группу {parent}"
        assert data in {d for _, d in _GROUPS[key][2]}, (
            f"{data} возвращает в группу {key}, которой не принадлежит"
        )


def test_main_screen_offers_exactly_the_three_groups():
    rows = get_settings_keyboard("ru").inline_keyboard
    data = [b.callback_data for row in rows for b in row]

    assert data == [f"settings_group_{k}" for k in _GROUPS], (
        f"главный экран настроек предлагает не те кнопки: {data}"
    )


def test_every_group_button_has_a_handler_that_answers_it():
    """
    Нажатие по группе должно пройти фильтры обработчика. Дефект «кнопка есть,
    нажатие уходит в пустоту» в проекте случался дважды.
    """
    from app.bot.handlers.quiz.settings import router

    class _Probe:
        def __init__(self, value: str) -> None:
            self.data = value

    handlers = router.callback_query.handlers
    for key in _GROUPS:
        probe = _Probe(f"settings_group_{key}")
        matched = any(
            all(f.callback(probe) for f in handler.filters) for handler in handlers
        )
        assert matched, f"нажатие по группе {key} не ловит ни один обработчик"


def test_group_labels_and_titles_exist_in_every_locale():
    """
    Пропущенный ключ не падает — get_text вернёт «[MISSING: …]», и это
    уедет человеку в сообщении.
    """
    missing = []
    for lang in LOCALES:
        for key, (btn_key, title_key, _) in _GROUPS.items():
            for needed in (btn_key, title_key):
                if "[MISSING:" in get_text(needed, lang):
                    missing.append(f"{lang}: {needed}")
    assert not missing, f"нет надписей групп: {missing}"


def test_group_screens_keep_the_state_lines_visible():
    """
    Человек, зашедший менять уровень, должен видеть текущий, не возвращаясь
    назад. Строки состояния показываются и внутри группы.
    """
    for key in _GROUPS:
        rows = _group_keyboard(key, "ru").inline_keyboard
        # пункты группы плюс ровно один «Назад»
        assert len(rows) == len(_GROUPS[key][2]) + 1
        assert rows[-1][0].callback_data == "back_to_settings"


def test_a_group_shows_only_its_own_state_lines():
    """
    Первая редакция печатала внутри каждой группы все шесть строк, и в
    «🔧 Бот» висело «Режим: Уровень B1» с «Занятие: Карточка · На слух» — та
    же простыня, трижды. Ровно против этого группировка и затевалась.
    """
    from app.bot.handlers.quiz.settings import _STATE_LINES, _settings_state
    from app.database.enums import CEFRLevel, QuizMode
    from app.database.models import User

    user = User(
        id=1, interface_language="ru", learning_lang="de", native_lang="ru",
        reverse_mode=False, level=CEFRLevel.B1, quiz_mode=QuizMode.LEVEL,
    )
    user.audio_enabled = True
    user.quiz_channels = "ta"

    full = _settings_state(user, "ru")
    assert full.count("\n") == len(_STATE_LINES) - 1, "главный экран потерял строки"

    for key, (_, _, items) in _GROUPS.items():
        own = tuple(d for _, d in items)
        state = _settings_state(user, "ru", only=own)
        expected = [k for k in _STATE_LINES if k in own]
        got = [line for line in state.splitlines() if line]

        assert len(got) == len(expected), (
            f"группа {key}: строк {len(got)}, а своих пунктов со строкой "
            f"{len(expected)}"
        )
        # Ни одна строка чужого пункта не просочилась
        for other in _STATE_LINES:
            if other in own:
                continue
            assert _STATE_LINES[other](user, "ru") not in state, (
                f"в группе {key} чужая строка пункта {other}"
            )
