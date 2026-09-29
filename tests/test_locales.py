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
    from app.bot.buttons import BTN_LEARN_WORDS, button_texts

    assert len(button_texts(BTN_LEARN_WORDS)) == len(LOCALES)
