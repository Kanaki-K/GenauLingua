"""
Серия дней: прерванная серия должна читаться как прерванная.

ЗАЧЕМ. Серия — главный мотиватор бота: она стоит на домашнем экране, в
напоминании, в статистике, в админке. Считал её ОДИН обработчик, читали
ПЯТЬ мест — каждое напрямую из колонки `users.streak_days`.

А колонка пересчитывается только при завершении круга. Значит у того, кто
перестал заниматься, в ней навсегда остаётся последнее значение. Замер по
рабочей копии 13 октября 2026:

    людей с непустой серией                    128
    из них серия УСТАРЕЛА                     128   (все до единого)
    последняя активность                2026-02-19   (236 дней назад)

Домашний экран и напоминание говорили «1 день подряд» человеку, который не
заходил восемь месяцев. Для экрана, который должен мотивировать, это худший
вид вранья: он хвалит за то, чего нет, и человек перестаёт верить остальным
числам.

И вторая находка того же замера: `best_streak_days` не записывалась НИ РАЗУ
— ноль у всех 233 человек. А это единственное число, которое у прервавшего
серию остаётся.
"""

from datetime import date, timedelta

from app.database.models import User
from app.services.streak_service import current_streak, register_activity

TODAY = date(2026, 10, 13)


def _person(**kwargs) -> User:
    person = User(
        id=1, first_name="Кто-то", interface_language="ru",
        learning_lang="de", native_lang="ru", reverse_mode=False,
    )
    for key, value in kwargs.items():
        setattr(person, key, value)
    return person


# ============================================================================
# ЧТО СЧИТАЕТСЯ ЖИВОЙ СЕРИЕЙ
# ============================================================================

def test_today_keeps_the_streak():
    person = _person(streak_days=7, last_active_date=TODAY)
    assert current_streak(person, TODAY) == 7


def test_yesterday_keeps_the_streak():
    """
    Вчера входит нарочно: занимавшийся вечером утром ещё не прервал серию —
    он как раз успевает её продолжить, и показывать ему ноль несправедливо.
    """
    person = _person(streak_days=7, last_active_date=TODAY - timedelta(days=1))
    assert current_streak(person, TODAY) == 7


def test_the_day_before_yesterday_breaks_it():
    person = _person(streak_days=7, last_active_date=TODAY - timedelta(days=2))
    assert current_streak(person, TODAY) == 0


def test_eight_months_of_silence_is_not_a_streak():
    """Ровно тот случай, что нашёлся у 128 человек из 128."""
    person = _person(streak_days=1, last_active_date=date(2026, 2, 19))
    assert current_streak(person, TODAY) == 0


def test_a_streak_without_a_date_is_not_trusted():
    """
    Серия есть, а дня нет — данные старше колонки с датой. Проверить такую
    серию нечем, значит считать её живой нельзя.
    """
    person = _person(streak_days=5, last_active_date=None)
    assert current_streak(person, TODAY) == 0


def test_no_streak_means_zero():
    assert current_streak(_person(streak_days=0, last_active_date=TODAY), TODAY) == 0
    assert current_streak(_person(streak_days=None, last_active_date=TODAY), TODAY) == 0


def test_the_column_itself_is_not_erased():
    """
    `current_streak` ТОЛЬКО ЧИТАЕТ. Стирать колонку нельзя: по ней
    восстанавливается лучшая серия, и перезапишется она сама при следующем
    занятии.
    """
    person = _person(streak_days=12, last_active_date=date(2026, 1, 1))
    current_streak(person, TODAY)
    assert person.streak_days == 12


# ============================================================================
# ОТМЕТКА ДНЯ
# ============================================================================

def test_a_second_round_today_changes_nothing():
    """
    71% дней — это два круга и больше. Второй круг не должен давать второй
    день серии.
    """
    person = _person(streak_days=3, last_active_date=TODAY)
    assert register_activity(person, TODAY) == 3
    assert person.streak_days == 3


def test_a_round_the_next_day_grows_the_streak():
    person = _person(streak_days=3, last_active_date=TODAY - timedelta(days=1))
    assert register_activity(person, TODAY) == 4
    assert person.last_active_date == TODAY


def test_a_round_after_a_gap_starts_over():
    person = _person(streak_days=30, last_active_date=TODAY - timedelta(days=5))
    assert register_activity(person, TODAY) == 1


def test_the_first_round_ever_starts_at_one():
    person = _person(streak_days=0, last_active_date=None)
    assert register_activity(person, TODAY) == 1


# ============================================================================
# ЛУЧШАЯ СЕРИЯ
# ============================================================================

def test_the_best_streak_is_remembered():
    """Колонка существовала с начала и не записывалась ни разу."""
    person = _person(streak_days=3, last_active_date=TODAY - timedelta(days=1),
                     best_streak_days=0)
    register_activity(person, TODAY)
    assert person.best_streak_days == 4


def test_the_best_streak_survives_a_broken_one():
    """
    Главное свойство: серия оборвалась и началась заново с единицы, а
    лучшая осталась. Это единственное число, которое можно показать вместо
    обнулённой серии — «лучшее: 30 дней» звучит иначе, чем «0 дней».
    """
    person = _person(streak_days=30, last_active_date=TODAY - timedelta(days=5),
                     best_streak_days=30)
    register_activity(person, TODAY)
    assert person.streak_days == 1
    assert person.best_streak_days == 30


def test_the_best_streak_never_shrinks():
    person = _person(streak_days=2, last_active_date=TODAY - timedelta(days=1),
                     best_streak_days=40)
    register_activity(person, TODAY)
    assert person.best_streak_days == 40


# ============================================================================
# ЭКРАНЫ БЕРУТ ИЗ ОДНОГО ИСТОЧНИКА
# ============================================================================

def test_no_screen_reads_the_column_directly():
    """
    Серию читают пять мест, и все обязаны идти через `current_streak`.
    Прямое чтение колонки — это ровно тот дефект, из-за которого экран хвалил
    за прерванную серию.
    """
    import pathlib
    import re

    root = pathlib.Path(__file__).resolve().parents[1] / "app"
    allowed = {"streak_service.py", "models.py"}
    offenders = []

    for path in root.rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        if path.name in allowed or rel.startswith("scripts/"):
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\buser\.streak_days\b", text):
            line = text[:match.start()].count("\n") + 1
            # Присваивание — это запись, её делает register_activity
            if "=" in text.splitlines()[line - 1].split("user.streak_days")[-1][:3]:
                continue
            offenders.append(f"{rel}:{line}")

    assert not offenders, (
        "колонка серии читается напрямую, минуя current_streak: "
        + ", ".join(offenders)
    )
