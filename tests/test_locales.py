"""
Согласованность локализации.

Пропущенный ключ не падает с ошибкой — get_text возвращает «[MISSING: key]»,
и это уезжает пользователю в сообщении. Поэтому проверяем статически.
"""

import re
from pathlib import Path

import pytest

from app.locales import LOCALES, get_text

APP = Path(__file__).resolve().parent.parent / "app"

GET_TEXT_LITERAL = re.compile(r'get_text\(\s*["\']([a-zA-Z0-9_]+)["\']')
GET_TEXT_FSTRING = re.compile(r'get_text\(\s*f["\']([a-zA-Z0-9_{}\.]+)["\']')

# Ключи, собираемые из шаблона в рантайме. Перечислены явно, чтобы
# проверка ловила и их.
DYNAMIC_KEYS = {
    *(f"lang_{code}" for code in ("ru", "uk", "en", "tr")),
    *(f"langname_{code}" for code in ("de", "en", "ru", "uk", "tr")),
}


def _app_sources():
    return [p for p in APP.rglob("*.py") if "locales" not in p.parts]


def _used_keys() -> set[str]:
    keys = set()
    for path in _app_sources():
        src = path.read_text(encoding="utf-8")
        keys |= set(GET_TEXT_LITERAL.findall(src))
    return keys


def test_all_locales_have_identical_key_sets():
    """Расхождение означает, что часть пользователей увидит английский ключ."""
    sets = {lang: set(texts) for lang, texts in LOCALES.items()}
    everything = set().union(*sets.values())

    missing = {lang: sorted(everything - keys) for lang, keys in sets.items()}
    missing = {lang: keys for lang, keys in missing.items() if keys}

    assert not missing, f"в локалях не хватает ключей: {missing}"


def test_every_requested_key_exists():
    unknown = sorted(_used_keys() - set().union(*(set(t) for t in LOCALES.values())))
    assert not unknown, f"код запрашивает несуществующие ключи: {unknown}"


def test_dynamic_keys_exist():
    """Ключи, собираемые из шаблона: f\"lang_{code}\" и подобные."""
    everything = set().union(*(set(t) for t in LOCALES.values()))
    missing = sorted(DYNAMIC_KEYS - everything)
    assert not missing, f"не хватает ключей, собираемых динамически: {missing}"


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_no_placeholder_leaks(lang):
    """Ни одно значение не должно содержать след незаполненного шаблона."""
    bad = [key for key, text in LOCALES[lang].items() if "[MISSING:" in text or "[ERROR:" in text]
    assert not bad, f"{lang}: повреждённые значения {bad}"


def test_format_parameters_match():
    """
    У локализованной строки и её вызова должны совпадать параметры.
    Иначе get_text вернёт «[ERROR: key missing parameter ...]».
    """
    placeholder = re.compile(r"\{([a-zA-Z0-9_]+)")
    call = re.compile(
        r'get_text\(\s*["\']([a-zA-Z0-9_]+)["\']\s*,\s*[^,)]+((?:,\s*[a-zA-Z0-9_]+\s*=[^,)]+)*)\)'
    )

    problems = []
    for path in _app_sources():
        src = path.read_text(encoding="utf-8")
        for match in call.finditer(src):
            key, kwargs_part = match.group(1), match.group(2) or ""
            passed = set(re.findall(r"([a-zA-Z0-9_]+)\s*=", kwargs_part))

            for lang, texts in LOCALES.items():
                template = texts.get(key)
                if template is None:
                    continue
                needed = set(placeholder.findall(template))
                if needed - passed:
                    problems.append(
                        f"{path.name}: {key} [{lang}] не передаётся {sorted(needed - passed)}"
                    )
                    break

    assert not problems, "\n".join(problems)


def test_reply_button_texts_are_unique_per_language():
    """
    Реплай-кнопки сопоставляются по тексту. Две кнопки с одинаковой надписью
    в одном языке означают, что одна из них не сработает.
    """
    from app.bot.buttons import BTN_HELP, BTN_LEARN_WORDS, BTN_SETTINGS, BTN_STATS

    keys = [BTN_LEARN_WORDS, BTN_STATS, BTN_SETTINGS, BTN_HELP]
    for lang in LOCALES:
        labels = [get_text(key, lang) for key in keys]
        assert len(set(labels)) == len(labels), f"{lang}: повторяющиеся надписи {labels}"


def test_button_texts_cover_all_interface_languages():
    """
    Фильтр знает подпись на каждом языке — и нынешнюю, и прежнюю.

    Прежде здесь стояло `len(button_texts(...)) == len(LOCALES)`, то есть
    «ровно по одной подписи на язык». Решение изменилось: подписи нижних
    кнопок потеряли значки, а реплай-клавиатура живёт НА СООБЩЕНИИ и у
    человека в чате остаётся прежняя. Фильтр обязан принимать обе, иначе
    кнопка молча перестаёт работать — и выбраться можно только командой.

    Поэтому проверяется не ЧИСЛО подписей, а покрытие: каждый язык и
    каждая прежняя подпись на месте. Полнее об этом —
    `tests/test_legacy_buttons.py`.
    """
    from app.bot.buttons import BTN_LEARN_WORDS, LEGACY_TEXTS, button_texts

    caught = button_texts(BTN_LEARN_WORDS)

    for lang in LOCALES:
        assert get_text(BTN_LEARN_WORDS, lang) in caught, lang
    for old in LEGACY_TEXTS[BTN_LEARN_WORDS]:
        assert old in caught, old

    # Лишнего в фильтре нет: только нынешние и перечисленные прежние
    expected = {get_text(BTN_LEARN_WORDS, lang) for lang in LOCALES}
    expected |= set(LEGACY_TEXTS[BTN_LEARN_WORDS])
    assert caught == expected


def _dynamic_prefixes() -> set[str]:
    """
    Приставки ключей, которые код собирает НА ХОДУ.

    Собираются из самого кода — `f"remind_fact_{n}"`, `"cat_" + value`, —
    а не выписываются списком: выписанный список отстанет от кода при
    первой же новой приставке, и честный ключ сочтётся мёртвым.
    """
    prefixes: set[str] = set()
    for path in _app_sources():
        src = path.read_text(encoding="utf-8")
        prefixes |= set(re.findall(r'["\']([a-z_]{3,})["\']\s*\+', src))
        prefixes |= set(re.findall(r'f["\']([a-z_]{3,})\{', src))
    return prefixes


def test_no_locale_key_is_dead():
    """
    ОБРАТНАЯ СТОРОНА: в локалях нет строк, которых не показывает никто.

    Проверка `test_every_requested_key_exists` смотрит из кода в локали —
    и ловит пропажу. Эта смотрит обратно и ловит МУСОР, а он не безобиден:

      экран подробной статистики переписали новыми ключами, а 23 старых
      остались — `stats_title`, `stats_learned`, `stats_cta_begin`…;
      экран направления перевода сняли вместе с пятой игрой, а его строки
      остались — `settings_mode_title`, `mode_de_to_ru` и восемь других;
      кнопки игр убрали с экрана чисел, а подписи остались.

    Всего таких нашлось 61 ключ — 366 строк в шести языках. Вред не в
    размере: человек, который придёт править текст бота, будет править
    строку, которой бот не показывает, и не поймёт, почему ничего не
    изменилось. Так уже случилось с «+100 за · +50 за» в рейтинге: строка
    была СЛОМАНА (из неё выпали медали), и никто этого не замечал.
    """
    literal = set()
    for path in _app_sources():
        src = path.read_text(encoding="utf-8")
        literal |= set(re.findall(r'["\']([a-zA-Z0-9_]{3,})["\']', src))

    prefixes = _dynamic_prefixes()
    everything = set().union(*(set(t) for t in LOCALES.values()))

    dead = sorted(
        key for key in everything
        if key not in literal
        and key not in DYNAMIC_KEYS
        and not any(key.startswith(prefix) for prefix in prefixes)
    )
    assert not dead, (
        f"строки, которых не показывает никто ({len(dead)}): {dead[:15]}"
    )
