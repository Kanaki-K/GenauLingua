# -*- coding: utf-8 -*-
"""
Дата в боевом коде берётся по UTC, а не по местному времени сервера.

Почему это важно. Все метки времени в схеме хранятся по UTC: `utcnow()` так и
задуман, и колонки объявлены как timestamp without time zone. Если рядом
спросить «какое сегодня число» у местного времени, два источника разойдутся.

Это не догадка: в часовом поясе +02:00 месячный сезон создавался по местной
дате уже первым числом, старый сезон помечался неактивным, а викторины
последних двух часов месяца штамповались ещё прошлым числом по UTC — и не
попадали ни в один сезон. Двенадцать тестов лидерборда упали ровно на этом,
когда сутки перевалили за полночь.

На проде дефект спал: у контейнера часовой пояс не задан, то есть UTC, и
местная дата совпадала с UTC. Достаточно выставить TZ или перенести образ —
и он просыпается. Поэтому проверка смотрит не на поведение, а на источник
даты: `date.today()` в боевом коде быть не должно.
"""
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Скрипты сюда не входят: они запускаются руками на машине разработчика, их
# вывод не попадает в схему, и местная дата в имени файла отчёта уместна
PRODUCTION_DIRS = ("app/bot", "app/services", "app/schedulers", "app/core",
                   "app/database", "app/handlers")

LOCAL_DATE = re.compile(r"\bdate\.today\(\)")
LOCAL_NOW = re.compile(r"\bdatetime\.now\(\)")


def production_files() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for folder in PRODUCTION_DIRS:
        base = ROOT / folder
        if base.exists():
            files.extend(base.rglob("*.py"))
    return files


def test_production_code_has_no_local_date():
    """
    `date.today()` даёт местную дату сервера — она разойдётся с хранимым UTC.

    Вместо неё есть `app.core.clock.utctoday()`.
    """
    offenders = []
    for path in production_files():
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if LOCAL_DATE.search(line) and "utctoday" not in line:
                offenders.append(f"{path.relative_to(ROOT)}:{number}")
    assert not offenders, (
        "местная дата в боевом коде — заменить на utctoday():\n  "
        + "\n  ".join(offenders)
    )


def test_production_code_has_no_naive_local_now():
    """`datetime.now()` без таймзоны — то же самое, но для времени."""
    offenders = []
    for path in production_files():
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if LOCAL_NOW.search(line):
                offenders.append(f"{path.relative_to(ROOT)}:{number}")
    assert not offenders, (
        "местное время в боевом коде — заменить на utcnow():\n  "
        + "\n  ".join(offenders)
    )


def test_clock_helpers_agree():
    """utctoday() обязан быть датой того же момента, что utcnow()."""
    from app.core.clock import utcnow, utctoday

    # Между двумя вызовами могут пройти сутки, если попасть ровно в полночь;
    # поэтому сравниваем с обеих сторон
    before = utcnow().date()
    today = utctoday()
    after = utcnow().date()
    assert today in (before, after)


@pytest.mark.parametrize("name", ["utcnow", "utctoday"])
def test_clock_exports(name):
    """Обе функции должны существовать: на них опирается весь боевой код."""
    import app.core.clock as clock

    assert callable(getattr(clock, name))
