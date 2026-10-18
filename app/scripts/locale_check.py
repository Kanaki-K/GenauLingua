#!/usr/bin/env python3
"""
Сверка новой локали с английской: ключи, подстановки, HTML-теги, формы
множественного числа.

Тесты (test_locales, test_nudges) проверяют локаль, только когда она уже в
LOCALES. Этот скрипт проверяет файл до подключения — чтобы переводчик видел
изъяны сам.

    python -m app.scripts.locale_check it
"""

from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

PLACEHOLDER = re.compile(r"\{[a-z_0-9]+\}")
TAG = re.compile(r"</?[a-z]+[^>]*>")
FORMS = {"cs": 3, "pl": 3, "ru": 3, "uk": 3, "fr": 2, "it": 2, "es": 2, "en": 2, "de": 2}


def main() -> None:
    lang = sys.argv[1]
    en = importlib.import_module("app.locales.en").TEXTS
    new = importlib.import_module(f"app.locales.{lang}").TEXTS
    others = [importlib.import_module(f"app.locales.{c}").TEXTS for c in ("ru", "uk", "en", "tr", "de", "pl")]
    problems = []
    missing = set(en) - set(new)
    extra = set(new) - set(en)
    if missing:
        problems.append(f"нет ключей ({len(missing)}): {sorted(missing)[:30]}")
    if extra:
        problems.append(f"лишние ключи: {sorted(extra)[:30]}")
    for key in sorted(set(en) & set(new)):
        a, b = en[key], new[key]
        if not isinstance(b, str):
            continue
        # Имена подстановок у локалей законно разные ({lessons} / {lessons_n} —
        # где нужна форма числа); годится любое, что есть у ключа хоть где-то
        allowed = set().union(*(PLACEHOLDER.findall(t.get(key, "")) for t in others))
        bad = set(PLACEHOLDER.findall(b)) - allowed
        if bad:
            problems.append(f"{key}: неизвестные подстановки {sorted(bad)}")
        if PLACEHOLDER.findall(a) and not PLACEHOLDER.findall(b):
            problems.append(f"{key}: потеряны подстановки {sorted(PLACEHOLDER.findall(a))}")
        if sorted(t.split()[0].rstrip(">") for t in TAG.findall(a)) != \
                sorted(t.split()[0].rstrip(">") for t in TAG.findall(b)):
            problems.append(f"{key}: HTML-теги не совпадают")
        if a.count("\n") != b.count("\n") and key.startswith("nd_"):
            problems.append(f"{key}: число строк не совпадает (вид уведомления)")
        if key.startswith("plural_") and lang in FORMS:
            n = len(b.split("|"))
            if n != FORMS[lang] and not (lang in ("tr",) and n == 1):
                problems.append(f"{key}: форм {n}, а нужно {FORMS[lang]}")
        if b.strip() == a.strip() and len(a) > 12 and not key.startswith(("lang_", "settings_mode_hint")):
            problems.append(f"{key}: не переведено (как в en)")
    for p in problems:
        print(p)
    print(f"{lang}: ключей {len(new)} из {len(en)}, замечаний {len(problems)}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
