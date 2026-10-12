# -*- coding: utf-8 -*-
"""
ПРИЁМКА МЕНЮ: НИ ОДНА КНОПКА НЕ ВЕДЁТ В ПУСТОТУ.

    python -m app.scripts.verify_buttons

ЗАЧЕМ. Дефект «кнопка есть, нажатие уходит в никуда» в этом проекте
случался дважды, и оба раза выглядел одинаково снаружи: человек жмёт, бот
молчит. Один раз надпись реплай-кнопки вписали в фильтр руками и только
по-русски, и на пяти языках кнопка не работала. Другой раз обработчик
перехватывал событие и ничего не делал — кнопки меню гасли во время
вопроса.

Найти такое чтением кода почти нельзя: отсутствие обработчика не бросается
в глаза, а тесты проверяют те экраны, про которые вспомнили. Поэтому
проверка идёт С ДВУХ КОНЦОВ:

  кнопки → обработчики   каждое `callback_data` из кода должно пройти
                         фильтры хотя бы одного ЗАРЕГИСТРИРОВАННОГО
                         обработчика настоящего роутера
  надписи → фильтры      каждая реплай-кнопка меню должна ловиться на
                         ВСЕХ шести языках интерфейса

Роутер собирается ровно так, как в `app.main`: проверять набор роутеров,
отличный от боевого, значит проверять не тот бот.

Скрипт ТОЛЬКО ЧИТАЕТ: ни базы, ни сети.
"""
from __future__ import annotations

import argparse
import logging
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

logging.disable(logging.INFO)

from aiogram import Dispatcher  # noqa: E402

from app.locales import LOCALES, get_text  # noqa: E402

# Литерал: callback_data="что-то". Берём и одинарные кавычки.
LITERAL = re.compile(r"""callback_data\s*=\s*["']([^"'{}]+)["']""")

# f-строка: callback_data=f"префикс_{...}". Проверяем ПРЕФИКС: именно на нём
# стоят фильтры вида startswith, и именно его опечатка делает кнопку мёртвой.
FSTRING = re.compile(r"""callback_data\s*=\s*f["']([^"'{]*)\{""")

# Чем подставить хвост f-строки. Любая непустая строка годится: фильтры
# смотрят на начало, а на точное совпадение f-строка не рассчитана.
TAIL = "X"


class _Probe:
    """Событие только с тем полем, на которое смотрят фильтры кнопок."""

    def __init__(self, data: str) -> None:
        self.data = data


def build_dispatcher() -> Dispatcher:
    """Тот же набор роутеров и в том же порядке, что в боевом `app.main`."""
    from app.bot.handlers.admin import router as admin_router
    from app.bot.handlers.leaderboard.alltime import router as alltime_router
    from app.bot.handlers.leaderboard.leaderboard_table import router as table_router
    from app.bot.handlers.leaderboard.monthly import router as monthly_router
    from app.bot.handlers.quiz.game import router as game_router
    from app.bot.handlers.quiz.help import router as help_router
    from app.bot.handlers.quiz.home import router as home_router
    from app.bot.handlers.quiz.report import router as report_router
    from app.bot.handlers.quiz.settings import router as settings_router
    from app.bot.handlers.quiz.stats import router as stats_router
    from app.bot.handlers.reminders import router as reminders_router
    from app.bot.handlers.start import router as start_router

    dp = Dispatcher()
    for router in (
        monthly_router, alltime_router, table_router, report_router,
        start_router, home_router, game_router, settings_router,
        stats_router, help_router, reminders_router, admin_router,
    ):
        dp.include_router(router)
    return dp


def _callback_handlers(dp: Dispatcher) -> list:
    """
    Все обработчики нажатий дерева роутеров — КАЖДЫЙ ПО ОДНОМУ РАЗУ.

    Первая редакция обходила `dp.sub_routers + [dp]`, а внутри ещё и
    `router.sub_routers` — и считала каждый обработчик дважды. Само
    «ловится или нет» от этого не менялось, зато число в отчёте врало
    вдвое (178 вместо 89), а список «кто ловит» двоился и прятал
    настоящую находку: нажатие, которое ловят ДВА РАЗНЫХ обработчика.
    """
    found = []
    seen: set[int] = set()

    def walk(router) -> None:
        if id(router) in seen:
            return
        seen.add(id(router))
        found.extend(router.callback_query.handlers)
        for nested in router.sub_routers:
            walk(nested)

    walk(dp)
    return found


def _is_state_filter(check) -> bool:
    """
    Фильтр про СОСТОЯНИЕ, а не про данные кнопки.

    Различается по типу, и это важно. Первая редакция пыталась различать по
    поведению — «фильтр упал на пробе, значит он не про данные», — и не
    сработала: фильтр состояния не падает, он честно возвращает False,
    потому что состояния у пробы нет. В итоге проверка объявила мёртвыми
    четыре ЖИВЫЕ кнопки: `next_question`, `speech_reference`,
    `speech_skip`, `answer_*`. У каждой обработчик на месте, просто рядом
    стоит `QuizStates.answering`.

    Та же форма, что и у девяти прежних дефектов проекта, только внутри
    самой проверки: смотрела не на то поле. Спрашивать надо, ЧЕМ фильтр
    является, а не как он себя повёл.
    """
    from aiogram.filters import StateFilter
    from aiogram.fsm.state import State, StatesGroup

    target = check.callback
    return isinstance(target, (State, StateFilter)) or (
        isinstance(target, type) and issubclass(target, StatesGroup)
    )


def _catchers(handlers: list, data: str) -> list[str]:
    """Имена всех обработчиков, которые поймают это нажатие, по порядку."""
    probe = _Probe(data)
    names = []
    for handler in handlers:
        passed_data_filter = False
        rejected = False
        for check in handler.filters:
            if _is_state_filter(check):
                continue
            try:
                verdict = check.callback(probe)
            except Exception:
                continue
            if verdict:
                passed_data_filter = True
            else:
                rejected = True
                break
        if passed_data_filter and not rejected:
            names.append(getattr(handler.callback, "__name__", "?"))
    return names


def _matches(handlers: list, data: str) -> bool:
    """
    Есть ли обработчик, чьи фильтры ПО ДАННЫМ пропускают это нажатие.

    Состояние не проверяется нарочно: кнопка, живущая только внутри
    занятия, — это норма, а не дефект. Спрашиваем ровно одно: есть ли вообще
    кому её поймать.

    Совпадение засчитывается, лишь когда хотя бы один фильтр ПРО ДАННЫЕ
    ответил «да». Без этого условия обработчик с одним фильтром состояния
    ловил бы всё подряд, и проверка стала бы бесполезной.
    """
    probe = _Probe(data)
    for handler in handlers:
        passed_data_filter = False
        rejected = False
        for check in handler.filters:
            if _is_state_filter(check):
                continue
            try:
                verdict = check.callback(probe)
            except Exception:
                continue
            if verdict:
                passed_data_filter = True
            else:
                rejected = True
                break
        if passed_data_filter and not rejected:
            return True
    return False


def collect_buttons() -> dict[str, set[str]]:
    """Все `callback_data` из кода бота: файл → набор значений."""
    found: dict[str, set[str]] = {}
    for path in pathlib.Path("app").rglob("*.py"):
        # Скрипты — не бот. У демонстрационных и приёмочных бывают свои
        # кнопки, которых боевой роутер и не должен знать
        if path.name == "verify_buttons.py" or "scripts" in path.parts:
            continue
        src = path.read_text(encoding="utf-8")
        values = set(LITERAL.findall(src))
        values |= {prefix + TAIL for prefix in FSTRING.findall(src) if prefix}
        if values:
            found[str(path)] = values
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    dp = build_dispatcher()
    handlers = _callback_handlers(dp)
    buttons = collect_buttons()

    dead: list[str] = []
    shared: list[tuple[str, list[str]]] = []
    total = 0
    for path, values in sorted(buttons.items()):
        for data in sorted(values):
            total += 1
            catchers = _catchers(handlers, data)
            if not catchers:
                dead.append(f"{path}: {data!r}")
            elif len(catchers) > 1:
                shared.append((data, catchers))

    print(f"\nобработчиков нажатий: {len(handlers)}")
    print(f"кнопок проверено: {total} в {len(buttons)} файлах")

    # ГДЕ РЕШАЕТ ПОРЯДОК — печатается, а не замалчивается.
    #
    # Нажатие, которое подходит двум обработчикам, достаётся тому, кто
    # зарегистрирован раньше. Это не дефект сам по себе: общий фильтр
    # `tz:` нарочно стоит ПОСЛЕ точных `tz:more_cities` и
    # `tz:back_to_main`, да ещё и сам отбрасывает служебные коды. Но
    # именно так случился разобранный дефект «подсказка про голос гасила
    # кнопки меню»: обработчик перехватывал событие и ничего не делал.
    #
    # Проверка не берётся судить, верен ли порядок — она показывает, где
    # он вообще значим, чтобы следующая правка роутеров это увидела.
    if shared:
        print(f"\nнажатий, где решает порядок роутеров: {len(shared)}")
        for data, catchers in shared:
            print(f"   {data!r} → {' → '.join(catchers)}  (ловит первый)")

    # Реплай-кнопки ловятся по НАДПИСИ, и надпись у каждого языка своя
    from app.bot.buttons import (
        BTN_HELP, BTN_LEARN_WORDS, BTN_RATING, BTN_SETTINGS, BTN_STATS,
        button_texts,
    )

    # ПРОВЕРЯЕТСЯ ВХОЖДЕНИЕ НАДПИСИ В ФИЛЬТР, А НЕ РАЗМЕР НАБОРА.
    #
    # Первая редакция сравнивала число надписей с числом языков и объявила
    # бедой `btn_stats` и `btn_rating`: пять надписей на шесть языков. Беды
    # нет — русский и украинский дают ОДНУ И ТУ ЖЕ строку («📊 Статистика»,
    # «🏆 Рейтинг»), слова в этих языках совпадают. Фильтр же — набор строк,
    # и оба языка им ловятся.
    #
    # Важно другое: нажатие на каждом языке должно попасть в фильтр. Это и
    # проверяем — вхождением, а не счётом.
    reply_bad: list[str] = []
    for key in (BTN_LEARN_WORDS, BTN_STATS, BTN_RATING, BTN_SETTINGS, BTN_HELP):
        labels = button_texts(key)
        for lang in LOCALES:
            label = get_text(key, lang)
            if "[MISSING:" in label or not label.strip():
                reply_bad.append(f"{key} [{lang}]: нет надписи")
            elif label not in labels:
                reply_bad.append(f"{key} [{lang}]: надпись {label!r} вне фильтра")
    print(f"реплай-кнопок проверено: 5 × {len(LOCALES)} языков")

    if total == 0:
        print("\nПРОВЕРЯТЬ БЫЛО НЕЧЕГО — это неудача, а не успех")
        return 1

    if dead:
        print(f"\nКНОПОК БЕЗ ОБРАБОТЧИКА: {len(dead)}")
        for line in dead:
            print(f"   {line}")
    if reply_bad:
        print(f"\nРЕПЛАЙ-КНОПКИ: {len(reply_bad)} беды")
        for line in reply_bad:
            print(f"   {line}")

    if dead or reply_bad:
        return 1

    print("\nни одна кнопка не ведёт в пустоту; меню ловится на всех языках")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
