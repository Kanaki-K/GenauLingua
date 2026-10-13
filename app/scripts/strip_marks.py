# -*- coding: utf-8 -*-
"""
Снять значки с текстов интерфейса: 68 видов → четыре.

ПРАВИЛО, А НЕ СПИСОК. Первая опись дала 68 разных значков — и пропустила
`1️⃣`, `2️⃣`, `👉` в многострочных значениях: составные знаки из цифры,
селектора вида и охватывающего ключа не попадают ни в один диапазон,
который выпишешь руками. Поэтому работает обратное правило: оставляем
буквы, цифры, знаки препинания и ПЕРЕЧИСЛЕННУЮ типографику, а всё
остальное из категорий символов снимаем.

Устав внешности — `UI_CONCEPT.md` §3. Разрешены четыре знака:

    🎧  канал слуха
    🎤  канал речи
    ✓   верно
    ✗   неверно

и типографика: `· → ▓ ░ ▸ — – …`. Крупные `✅ ❌` заменяются тонкими
`✓ ✗`: те — цветные пятна, они перетягивают взгляд с самого ответа.

ЧЕГО СКРИПТ НЕ ТРОГАЕТ. Подписи кнопок нижнего меню: их текст ловится
фильтром, и смена подписи обрывает нажатия у тех, у кого клавиатура уже
в чате. Это отдельная правка, с запасом совместимости.

Прогон без ключа только показывает; `--apply` записывает.
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LOCALES_DIR = ROOT / "app" / "locales"
LANGS = ("ru", "uk", "en", "tr", "de", "pl")

# Знаки, которые ОСТАЮТСЯ. Четыре из устава плюс типографика.
KEEP = set("🎧🎤✓✗▓░▸·→—–…«»№")

# Крупные цветные пятна меняются на тонкие знаки того же смысла
REPLACE = {
    "✅": "✓",
    "✔": "✓",
    "☑": "✓",
    "❌": "✗",
    "✖": "✗",
    "❎": "✗",
}

# Категории Unicode, которые считаются «значком»: символы прочие и
# модификаторы (So, Sk), охватывающие и несамостоятельные метки (Me, Mn),
# служебные невидимки (Cf — сюда же склейка эмодзи).
#
# Mn ОБЯЗАТЕЛЕН, и это выяснилось показом: селектор вида U+FE0F имеет
# именно эту категорию, и без неё `◀️ Назад` превращалось в `️ Назад` —
# значок снят, а его невидимый хвост остался.
MARK_CATEGORIES = {"So", "Sk", "Me", "Mn", "Cf"}

# Подписи кнопок нижнего меню — не здесь. Их правка требует запаса
# совместимости: нажатие ловится по тексту.
# Больше ничего не исключается: прежние подписи нижних кнопок перечислены
# в `app/bot/buttons.py` (LEGACY_TEXTS) и остаются в ФИЛЬТРЕ, так что
# нажатие со старой клавиатуры по-прежнему доходит.
SKIP_KEYS: set[str] = set()

VALUE_LINE = re.compile(r'^(\s*)"([a-z0-9_]+)":\s(".*",?)$')


def is_mark(char: str) -> bool:
    if char in KEEP:
        return False
    return unicodedata.category(char) in MARK_CATEGORIES


def strip_marks(text: str) -> str:
    """
    Снять значки со СОДЕРЖИМОГО строки и убрать следы.

    На вход идёт текст БЕЗ обрамляющих кавычек: первая редакция чистила
    строку файла целиком, и пробел от снятого значка оставался внутри
    кавычек — `"🔔 <b>Настройки</b>"` превращалось в `" <b>Настройки</b>"`.
    Экранировка (`\\n`, `\\"`) не затрагивается: символы `\\` и `"` не
    значки и проходят насквозь.
    """
    for old, new in REPLACE.items():
        text = text.replace(old, new)

    kept = "".join(char for char in text if not is_mark(char))

    # Следы от снятых значков: два пробела, пробел перед знаком препинания,
    # пробел после переноса строки и внутри скобки
    kept = re.sub(r"[ \t]{2,}", " ", kept)
    kept = re.sub(r" +([,.!?:;)])", r"\1", kept)
    kept = re.sub(r"(\\n) +", r"\1", kept)
    kept = re.sub(r" +(\\n)", r"\1", kept)
    kept = re.sub(r"\( +", "(", kept)

    # Пробел ВНУТРИ тега разметки. Значок часто стоял внутри: `<b>🎯 Что
    # учу</b>` — и после снятия оставалось `<b> Что учу</b>`, то есть
    # заголовок с отступом в один пробел. Видно это только на экране:
    # в значении локали пробел не отличим от любого другого.
    kept = re.sub(r"(<(?:b|i|u|s|code|pre)>) +", r"\1", kept)
    kept = re.sub(r" +(</(?:b|i|u|s|code|pre)>)", r"\1", kept)

    return kept.strip(" ")


def process(source: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Вернуть новый текст файла и список правок (ключ, было, стало)."""
    changes: list[tuple[str, str, str]] = []
    out_lines = []

    for line in source.split("\n"):
        match = VALUE_LINE.match(line)
        if not match:
            # Многострочные значения (`"""…`) и всё остальное — посимвольно,
            # но только если в строке нет кода: иначе снесём служебное
            if any(is_mark(char) for char in line) and not line.lstrip().startswith("#"):
                cleaned = strip_marks(line)
                if cleaned != line.strip(" "):
                    changes.append(("(многострочное)", line.strip(), cleaned.strip()))
                out_lines.append(cleaned if line.startswith(" ") is False
                                 else re.match(r"^\s*", line).group(0) + cleaned)
                continue
            out_lines.append(line)
            continue

        indent, key, value = match.groups()
        if key in SKIP_KEYS:
            out_lines.append(line)
            continue

        # Кавычки снимаются, чтобы чистка не оставляла пробел внутри них
        tail = "," if value.endswith(",") else ""
        body = value[: -len(tail)] if tail else value
        raw = body[1:-1]

        cleaned_raw = strip_marks(raw)
        if cleaned_raw != raw:
            changes.append((key, raw, cleaned_raw))
        out_lines.append(f'{indent}"{key}": "{cleaned_raw}"{tail}')

    return "\n".join(out_lines), changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="записать правки (по умолчанию только показ)")
    parser.add_argument("--lang", default=None, help="только один язык")
    args = parser.parse_args()

    langs = (args.lang,) if args.lang else LANGS
    total = 0

    for lang in langs:
        path = LOCALES_DIR / f"{lang}.py"
        source = io.open(path, encoding="utf-8").read()
        new_source, changes = process(source)
        total += len(changes)

        print(f"\n{'=' * 76}\n{lang}: правок {len(changes)}\n{'=' * 76}")
        for key, before, after in changes[:200]:
            print(f"  {key}")
            print(f"    было:  {before[:96]}")
            print(f"    стало: {after[:96]}")

        if args.apply:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new_source)

    print(f"\nвсего правок: {total}")
    if not args.apply:
        print("ничего не записано — для правки прогнать с --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
