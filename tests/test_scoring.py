"""
Начисление баллов: платим за УСИЛИЕ, а не за нажатия.

Прежняя формула давала за верный ответ одинаково, каким бы каналом он ни
был дан. При трёх каналах это прямо вредный совет: узнать слово на слух
труднее, чем прочитать, произнести труднее, чем узнать, — и если цена
одна, рациональный ученик остаётся на самом лёгком. Соревнование тогда
награждает выбор кнопки, а не работу.

Эти тесты держат три отличия новой формулы, каждое из которых меняет
поведение, а не только число:

    1. ответ стоит по каналу — 1 / 2 / 3
    2. точность начисляется ПЛАВНО, без обрыва на 90%
    3. серия РАСТЁТ в цене, а не даёт фиксированные три балла за день
"""

from app.database.models import MonthlyStats


def stats(**kwargs) -> MonthlyStats:
    base = dict(
        monthly_score=0, monthly_quizzes=0, monthly_reverse=0, monthly_words=0,
        monthly_streak=0, monthly_avg_percent=0, total_correct=0,
        total_questions=0, correct_audio=0, correct_speech=0, report_bonus=0,
    )
    base.update(kwargs)
    return MonthlyStats(**base)


def test_answer_by_ear_is_worth_more_than_by_sight():
    """
    Одинаковый объём, разные каналы — на слух должно выйти больше.

    Это главное, ради чего формула переписывалась. Если тест упадёт,
    значит бот снова советует ученику не напрягаться.
    """
    by_sight = stats(total_correct=100, total_questions=100)
    by_ear = stats(total_correct=100, total_questions=100, correct_audio=100)
    by_voice = stats(total_correct=100, total_questions=100, correct_speech=100)

    assert by_sight.calculate_monthly_score() < by_ear.calculate_monthly_score()
    assert by_ear.calculate_monthly_score() < by_voice.calculate_monthly_score()


def test_text_channel_is_derived_from_the_total():
    """
    Текстовых ответов своего счётчика нет — они остаток.

    Отдельной колонкой её рано или поздно обновили бы не вместе с общим
    итогом, и балл разошёлся бы с числом ответов незаметно.
    """
    mixed = stats(total_correct=10, total_questions=10,
                  correct_audio=4, correct_speech=2)
    # 4 текстовых × 1 + 4 слуха × 2 + 2 речи × 3 = 18
    assert mixed.calculate_monthly_score() == 18


def test_channels_cannot_push_text_below_zero():
    """
    Если счётчики каналов вдруг превысят общий итог, текст не должен уйти в
    минус и отнять уже начисленное. Данные так расходиться не должны, но
    балл — не то место, где стоит это выяснять.
    """
    broken = stats(total_correct=1, total_questions=1,
                   correct_audio=5, correct_speech=5)
    assert broken.calculate_monthly_score() >= 0


def test_accuracy_has_no_cliff_at_ninety():
    """
    Прежде 90% давали +50, а 89% — +30: двадцать баллов пропадали из-за
    одного вопроса. Обрыв воспринимается как несправедливость, даже когда
    он описан в правилах.

    Теперь прибавка плавная, и соседние проценты отличаются чуть-чуть.
    """
    def score(percent: int) -> int:
        return stats(
            monthly_avg_percent=percent, total_questions=450,
            total_correct=int(450 * percent / 100),
        ).calculate_monthly_score()

    assert score(90) > score(89)
    assert score(90) - score(89) <= 10, "скачок на 90% вернулся"
    # и монотонность: больше точность — больше баллов
    assert score(70) < score(80) < score(90) < score(100)


def test_accuracy_below_the_floor_adds_nothing_but_takes_nothing():
    """
    Ниже порога прибавка нулевая — но и вычета нет: низкая точность не
    должна отнимать заработанное ответами.

    Число верных ответов держится ОДИНАКОВЫМ, меняется только процент.
    Иначе проверялась бы не точность, а ответы: первая редакция этого теста
    сравнивала 40 верных с 60 и падала на разнице в двадцать баллов,
    которая к точности отношения не имела.
    """
    low = stats(monthly_avg_percent=40, total_questions=100, total_correct=50)
    at_floor = stats(monthly_avg_percent=60, total_questions=100, total_correct=50)

    assert low.calculate_monthly_score() == at_floor.calculate_monthly_score()
    assert low.calculate_monthly_score() == 50, "ответы начислены, точность — нет"


def test_streak_grows_in_value():
    """
    Десятый день подряд должен стоить дороже первого, иначе терять серию не
    жалко. Прежде день давал ровно три балла — что первый, что тридцатый.
    """
    points = MonthlyStats.streak_points

    assert points(0) == 0
    assert points(1) == 1
    assert points(2) - points(1) > points(1) - points(0) or points(2) == 3
    # прибавка за каждый следующий день не убывает
    deltas = [points(d) - points(d - 1) for d in range(1, 11)]
    assert deltas == sorted(deltas), "цена дня должна расти, а не падать"
    # и упирается в потолок, чтобы один марафонец не оторвался навсегда
    assert points(31) - points(30) == MonthlyStats.STREAK_DAILY_CAP


def test_consistency_beats_cramming_at_equal_volume():
    """
    Тот же объём занятий, разная регулярность — у постоянного должно быть
    заметно больше. Это главный рычаг возврата.
    """
    common = dict(monthly_quizzes=30, monthly_words=60, monthly_avg_percent=80,
                  total_correct=360, total_questions=450, correct_audio=180)
    daily = stats(monthly_streak=30, **common)
    sporadic = stats(monthly_streak=3, **common)

    assert daily.calculate_monthly_score() > sporadic.calculate_monthly_score()


def test_empty_month_scores_zero():
    assert stats().calculate_monthly_score() == 0


def test_missing_channel_columns_are_treated_as_text():
    """
    У записей, сделанных до появления каналов, счётчики пусты. Все их ответы
    были текстовыми — других вопросов в боте не было, — и формула обязана
    посчитать их, а не уронить расчёт на None.
    """
    legacy = stats(total_correct=50, total_questions=60)
    legacy.correct_audio = None
    legacy.correct_speech = None

    assert legacy.calculate_monthly_score() == 50
