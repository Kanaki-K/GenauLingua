# -*- coding: utf-8 -*-
"""
Поощрение в конце круга: за что хвалить, чтобы это было правдой.

ЗАЧЕМ. Экран итога показывал «Правильно 12/15» и разбор слов — и всё.
Ни баллов (хотя круг их платит), ни серии, ни продвижения. Человек
доводил круг до конца и не узнавал ни одной причины вернуться.

ПЕРВОЕ ПРАВИЛО: ХВАЛИТЬ ТОЛЬКО ЗА ТО, ЧТО ПРОИЗОШЛО. Похвала, которая
выдаётся всегда, перестаёт читаться с третьего раза, а похвала за то, чего
не было («отлично!» на 20% верных), ещё и обесценивает остальные числа —
ровно как домашний экран, который говорил «1 день подряд» человеку, не
заходившему восемь месяцев.

Отсюда устройство: все поводы — ИЗМЕРЕННЫЕ события круга, и показывается
РОВНО ОДИН, самый редкий из случившихся. Редкость и есть вес: первое
выученное слово дороже продолженной серии, а та дороже «трёх новых слов».
Если не случилось ничего особенного, берётся сдвиг этого круга — он
всегда непустой и всегда разный, потому что состав круга разный.

ПОЧЕМУ РУБЕЖИ, А НЕ ПРОЦЕНТЫ. Замер 13 октября по 199 людям с прогрессом:
«выучено» — ноль у 156 из 199, а знаменатель в 3 132 слова уровня даёт
вечные 0%. Поэтому главное число — СЛОВА В РАБОТЕ (не ноль ни у кого,
двигается каждый круг), а знаменатель — ближайший рубеж. Медиана 26 слов →
рубеж 50, это два круга; 90-й процентиль 209 → рубеж 250. Всегда близко.

«Выучено» не выброшено: оно осталось редким и потому дорогим поводом.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# Рубежи по словам в работе. Шаг растёт, чтобы следующий всегда был
# достижим: от 26 слов до 50 — два круга, от 209 до 250 — три.
MILESTONES = (10, 25, 50, 100, 250, 500, 1000, 2500)

# Круг «без ошибок» объявляется только если вопросов было достаточно:
# три из трёх — это не достижение, а короткий круг.
PERFECT_MIN_ANSWERS = 5

# Сколько дней молчания делают возврат событием. Неделя — это ровно тот
# порог, по которому админка считает пропавших.
COMEBACK_DAYS = 7


@dataclass(frozen=True)
class RoundFacts:
    """
    Что измеримо случилось в круге. Ничего, кроме чисел: решение «чем
    хвалить» принимается отдельно и проверяется без базы.
    """
    points: int = 0              # прирост месячного балла за этот круг
    answered: int = 0
    correct: int = 0
    rounds_total: int = 0        # пройдено кругов ВСЕГО, включая этот
    learned_before: int = 0
    learned_now: int = 0
    streak_days: int = 0
    best_streak: int = 0
    words_in_work: int = 0       # слов встречено на этой паре языков
    words_in_work_before: int = 0
    new_words: int = 0           # впервые встреченных в этом круге
    returned_right: int = 0      # не новых и отвечено верно
    days_away: int = 0           # сколько дней не заходил до этого круга
    first_audio: bool = False    # первый в жизни верный ответ на слух
    first_speech: bool = False   # первый в жизни верный ответ голосом

    @property
    def learned_now_count(self) -> int:
        return max(0, self.learned_now - self.learned_before)

    @property
    def accuracy(self) -> int:
        return round(self.correct / self.answered * 100) if self.answered else 0


def next_milestone(words: int) -> Optional[int]:
    """
    Ближайший непройденный рубеж. `None` — пройдены все, и тогда шкалы нет:
    выдумывать «до 5 000» бессмысленно, в базе 12 902 слова на пару.
    """
    for milestone in MILESTONES:
        if words < milestone:
            return milestone
    return None


def crossed_milestone(before: int, after: int) -> Optional[int]:
    """Рубеж, взятый именно в этом круге."""
    for milestone in MILESTONES:
        if before < milestone <= after:
            return milestone
    return None


def pick_event(facts: RoundFacts) -> Optional[tuple[str, dict]]:
    """
    Один повод для похвалы — самый редкий из случившихся.

    Порядок не произвольный: он от «бывает раз в жизни» к «бывает каждый
    третий круг». Первое выученное слово случается один раз, рубеж —
    несколько раз за месяц, продолженная серия — ежедневно.

    Возвращает ключ локали и подстановки, либо `None`, если не случилось
    ничего: тогда вызывающий возьмёт сдвиг круга.
    """
    # Первый круг в жизни. Говорится один раз и именно то, что человеку
    # сейчас полезно знать: дальше слова начнут возвращаться
    if facts.rounds_total == 1:
        return "praise_first_round", {}

    # Первое выученное слово — событие, которого у 156 человек из 199 не
    # было ни разу. Молчать о нём нельзя
    if facts.learned_before == 0 and facts.learned_now > 0:
        return "praise_first_learned", {}

    if facts.learned_now_count > 0:
        return "praise_learned", {"count": facts.learned_now_count}

    # Личный рекорд серии. Проверяется до обычной серии, иначе рекорд
    # прозвучал бы как рядовой день
    if facts.streak_days >= 2 and facts.streak_days >= facts.best_streak:
        return "praise_best_streak", {"days": facts.streak_days}

    crossed = crossed_milestone(facts.words_in_work_before, facts.words_in_work)
    if crossed:
        return "praise_milestone", {"count": crossed}

    if facts.first_speech:
        return "praise_first_speech", {}
    if facts.first_audio:
        return "praise_first_audio", {}

    if facts.days_away >= COMEBACK_DAYS:
        return "praise_comeback", {"days": facts.days_away}

    if facts.answered >= PERFECT_MIN_ANSWERS and facts.correct == facts.answered:
        return "praise_perfect", {}

    if facts.streak_days >= 2:
        return "praise_streak", {"days": facts.streak_days}

    return None


def pick_shift(facts: RoundFacts) -> Optional[tuple[str, dict]]:
    """
    Сдвиг этого круга — когда событий нет.

    Берётся большее из двух, и этим обеспечивается разнообразие без
    выдумки: в круге с новыми словами скажется про новые, в круге
    повторения — про вернувшиеся. Состав круга меняется сам (три новых
    слова на пятнадцать), значит и строка меняется.
    """
    if facts.returned_right > facts.new_words and facts.returned_right > 0:
        return "praise_returned", {"count": facts.returned_right}
    if facts.new_words > 0:
        return "praise_new_words", {"count": facts.new_words}
    if facts.returned_right > 0:
        return "praise_returned", {"count": facts.returned_right}
    return None


def progress_line(facts: RoundFacts) -> tuple[str, dict]:
    """
    Строка прогресса: слова в работе и сколько до ближайшего рубежа.

    Эта строка есть ВСЕГДА — она и заменяет шкалу, которая стояла на нуле.
    """
    target = next_milestone(facts.words_in_work)
    if target is None:
        return "praise_progress_top", {"count": facts.words_in_work}
    return "praise_progress", {
        "count": facts.words_in_work,
        "target": target,
        "left": target - facts.words_in_work,
    }


def build_lines(facts: RoundFacts, lang: Optional[str]) -> list[str]:
    """
    Готовый блок поощрения: похвала, прогресс, баллы.

    Три строки максимум. Больше не нужно: итог круга и так несёт разбор по
    словам, а блок, который длиннее разбора, перестаёт быть поощрением и
    становится вторым экраном.
    """
    from app.locales import get_text

    lines: list[str] = []

    chosen = pick_event(facts) or pick_shift(facts)
    if chosen:
        key, params = chosen
        lines.append(get_text(key, lang, **params))

    key, params = progress_line(facts)
    lines.append(get_text(key, lang, **params))

    # Баллы — последними: это награда, а не повод. И показываются только
    # если они начислены: у круга-повтора их нет, и писать «+0» значило бы
    # сообщать о награде, которой не было
    if facts.points > 0:
        lines.append(get_text("praise_points", lang, points=facts.points))

    return lines
