# -*- coding: utf-8 -*-
"""
СОСТАВ КРУГА: какой игрой задан каждый из пятнадцати вопросов.

ЗАЧЕМ ЭТИ ПРОВЕРКИ СУЩЕСТВУЮТ. Правило состава год прожило ненаписанным:
канал брался по кругу от предыдущего в порядке перечисления `QuizChannel`,
и состав занятия оказывался следствием порядка БУКВ. Описание при этом
уверяло в обратном — «ритм ломается сам, случайности тут нет вовсе», — и
замер на 40 кругах его опроверг: у продвинутого ученика выходило ровное
t r a s t r a s, чистое чередование в 21 круге из 40; речь приходила три
раза за круг в 15 кругах; последним вопросом речь оказывалась в 10.

Ни один тест этого не видел, потому что проверять было нечего: правила не
существовало. Теперь оно есть, и каждый его пункт проверяется здесь —
иначе оно разойдётся с описанием снова.

ПОЧЕМУ ПРОВЕРЯЕТСЯ СТАТИСТИКА, А НЕ ПОСЛЕДОВАТЕЛЬНОСТЬ. В правиле есть
одна нарочная случайность: равно отставшие игры равно правильны, и выбор
между ними случаен — без этого круг у продвинутого выходил одинаковым день
за днём. Значит ждать от него точной строки нельзя; ждать надо того, что
человек ЧУВСТВУЕТ: чем круг начался, чем кончился, сколько раз пришлось
записывать голос, не выродился ли он в одну игру.
"""
import collections
import random

import pytest

from app.database.enums import QuizChannel
from app.services.quiz_service import (
    CHANNEL_UNLOCK,
    WARMUP_QUESTIONS,
    channel_targets,
    enabled_channels,
    place_in_round,
    speech_cap,
)

ROUND = 15
ALL = list(QuizChannel)


class FakeUser:
    """Человек без базы: состав занятия и длина круга — всё, что нужно."""

    # Состав по умолчанию — ВСЕ игры перечисления, как у живого человека
    # (`User.quiz_channels`); строка руками отстала бы от шестой игры
    def __init__(self, channels: str = "".join(c.value for c in QuizChannel),
                 audio: bool = True,
                 length: int = ROUND):
        self.id = -1
        self.quiz_channels = channels
        self.audio_enabled = audio
        self.quiz_word_count = length


def play(profile: dict[int, float], *, rounds: int = 40, seed: int = 20261014,
         user: FakeUser | None = None) -> list[list[str]]:
    """
    Сыграть круги и вернуть, каким каналом задан каждый вопрос.

    `profile` — насколько человек знает слова, которые приносит подбор:
    сколько раз слово уже отвечено верно и с какой частотой такие слова
    попадаются. Это ЕДИНСТВЕННОЕ, от чего зависит допуск, поэтому состав
    круга можно измерить, не поднимая бота.
    """
    user = user or FakeUser()
    enabled = enabled_channels(user)
    rnd = random.Random(seed)
    random.seed(seed)  # случайность в самом правиле — тоже под замком
    out = []
    for _ in range(rounds):
        recent: list[str] = []
        for _ in range(user.quiz_word_count):
            times_correct = rnd.choices(
                list(profile), weights=list(profile.values()))[0]
            unlocked = [c for c in enabled
                        if times_correct >= CHANNEL_UNLOCK.get(c, 0)] or [QuizChannel.TEXT]
            channel = place_in_round(
                unlocked, enabled=enabled, recent=recent,
                round_length=user.quiz_word_count,
            )
            recent.append(channel.value)
        out.append(recent)
    return out


NOVICE = {0: 0.80, 1: 0.15, 2: 0.05}
MIDDLE = {0: 0.35, 1: 0.30, 2: 0.20, 3: 0.15}
ADVANCED = {0: 0.10, 1: 0.20, 2: 0.30, 3: 0.25, 5: 0.15}


# ============================================================================
# 1. РАЗОГРЕВ
# ============================================================================

@pytest.mark.parametrize("profile", [NOVICE, MIDDLE, ADVANCED])
def test_round_opens_with_the_easiest_game(profile):
    """
    Первый вопрос — карточка, и это ПРАВИЛО, а не порядок букв.

    Прежде текст выходил первым потому, что `TEXT` стоит первым в
    перечислении. Первая редакция правила разрешала ничью карточки и
    припоминания по букве — «r» меньше «t», — и круг у продвинутого
    начинался припоминанием в 37 случаях из 40.
    """
    for seq in play(profile):
        assert seq[0] == QuizChannel.TEXT.value, (
            f"круг начался не карточкой: {' '.join(seq)}"
        )


def test_warmup_is_one_question_not_two():
    """
    Разогрев один. При двух круг начинался «t t» — два одинаковых подряд,
    против чего в том же правиле стоит отдельный пункт.
    """
    assert WARMUP_QUESTIONS == 1


# ============================================================================
# 2 и 3. РЕЧЬ: не последней и не чаще потолка
# ============================================================================

@pytest.mark.parametrize("profile", [MIDDLE, ADVANCED])
def test_voice_is_never_the_last_question(profile):
    """
    На последнем вопросе голос не просят.

    Это не вкус: человек в автобусе не запишет ничего, а бросив круг на
    пятнадцатом вопросе, он теряет десять баллов за доведённое занятие —
    ровно перед экраном итога. Прежде речь оказывалась последней в 10
    кругах из 40.
    """
    for seq in play(profile):
        assert seq[-1] != QuizChannel.SPEECH.value, (
            f"круг кончился просьбой записать голос: {' '.join(seq)}"
        )


@pytest.mark.parametrize("profile", [MIDDLE, ADVANCED])
def test_voice_within_the_cap(profile):
    """Голосовых за круг не больше потолка. Прежде бывало три."""
    cap = speech_cap(ROUND)
    for seq in play(profile):
        asked = seq.count(QuizChannel.SPEECH.value)
        assert asked <= cap, f"голос просили {asked} раз, потолок {cap}"


def test_cap_grows_with_the_round():
    """Потолок — правило от длины круга, а не вписанное число."""
    assert speech_cap(15) == 2
    assert speech_cap(25) == 3
    assert speech_cap(7) == 1
    assert speech_cap(1) >= 1, "круг из одного вопроса не должен остаться без игры"


# ============================================================================
# 4. ПЕРЕМЕЖЕНИЕ
# ============================================================================

def test_no_two_alike_in_a_row_when_there_is_a_choice():
    """
    Два одинаковых подряд — только если другой игры для слова нет.

    У продвинутого открыто почти всё, значит выбор есть почти всегда, и
    длинных серий быть не должно.
    """
    for seq in play(ADVANCED):
        longest = cur = 1
        for i in range(1, len(seq)):
            cur = cur + 1 if seq[i] == seq[i - 1] else 1
            longest = max(longest, cur)
        assert longest <= 3, f"серия из {longest} одинаковых: {' '.join(seq)}"


def test_beginner_may_get_one_game_all_round_and_that_is_the_unlock_rule():
    """
    ОБРАТНАЯ ПОЛОВИНА, и она важнее: у новичка круг МОЖЕТ быть целиком из
    карточек, и это не поломка состава.

    Нельзя спросить на слух слово, которого человек ни разу не видел.
    Правило состава — цель, а не стена; если открыт один канал, он и
    придёт. Без этой проверки кто-нибудь однажды «починит» состав,
    выдав новичку пятнадцать загадок подряд.
    """
    rounds = play(NOVICE, rounds=60)
    single = [s for s in rounds if len(set(s)) == 1]
    assert single, (
        "ни один круг новичка не оказался однородным — значит порог "
        "допуска обходят, и слово приходит каналом, до которого не доросло"
    )


# ============================================================================
# 5. ДОЛИ
# ============================================================================

def test_shares_follow_the_price_of_an_answer():
    """
    Доля игры обратно пропорциональна цене ответа — одному источнику
    (`MonthlyStats.POINTS_*`), а не вписанным процентам.
    """
    from app.database.models import MonthlyStats

    targets = channel_targets(ALL)
    assert abs(sum(targets.values()) - 1) < 1e-9

    # Карточка и припоминание стоят одинаково — значит и доли равны
    assert MonthlyStats.POINTS_TEXT == MonthlyStats.POINTS_REVERSE
    assert targets[QuizChannel.TEXT] == targets[QuizChannel.REVERSE]

    # Чем дороже ответ, тем реже просят
    assert targets[QuizChannel.TEXT] > targets[QuizChannel.AUDIO]
    assert targets[QuizChannel.AUDIO] > targets[QuizChannel.SPEECH]


def test_advanced_round_reaches_the_target_shares():
    """
    У кого открыто всё — состав круга сходится к цели.

    Допуск беднее цели: у новичка почти всё закрыто, и ждать от него
    долей нельзя. У продвинутого отговорок нет.
    """
    targets = channel_targets(ALL)
    counts = collections.Counter()
    for seq in play(ADVANCED, rounds=60):
        counts.update(seq)
    total = sum(counts.values())

    for channel in ALL:
        want = targets[channel]
        got = counts[channel.value] / total
        assert abs(got - want) < 0.05, (
            f"{channel.value}: цель {want:.0%}, вышло {got:.0%}"
        )


def test_every_game_shows_up_for_the_advanced():
    """
    У продвинутого каждая игра встречается в КАЖДОМ круге.

    Иначе шкала не двигается, и человек не знает, что бот это умеет.
    Прежде речь не встречалась в 3 кругах из 40.
    """
    for seq in play(ADVANCED, rounds=60):
        missing = [c.value for c in ALL if c.value not in seq]
        assert not missing, f"игра не пришла ни разу: {missing} — {' '.join(seq)}"


# ============================================================================
# СОСТАВ ЧЕЛОВЕКА УВАЖАЕТСЯ
# ============================================================================

def test_rounds_differ_from_each_other():
    """
    Два круга подряд не должны быть одинаковыми.

    Это и была беда первой редакции: у продвинутого выходило
    t r a s r t r t a r t s r t a в трёх кругах из трёх. Узор круга —
    тоже часть занятия, и повторяясь, он превращает правило в расписание.
    """
    rounds = play(ADVANCED, rounds=60)
    patterns = {"".join(s) for s in rounds}
    assert len(patterns) > 50, (
        f"разных узоров всего {len(patterns)} из {len(rounds)} кругов"
    )


def test_disabled_games_never_appear():
    """Выключенную игру состав не приносит, как бы она ни отставала."""
    user = FakeUser(channels="tr")
    for seq in play(ADVANCED, user=user):
        assert set(seq) <= {"t", "r"}, f"пришла выключенная игра: {set(seq)}"


def test_audio_off_takes_voice_and_hearing_away():
    """
    Выключенная озвучка отменяет и слух, и речь — что бы ни стояло в
    составе. Припоминание она НЕ отменяет: оно текстовое.
    """
    user = FakeUser(channels="tasr", audio=False)
    seen = set()
    for seq in play(ADVANCED, user=user):
        seen.update(seq)
    assert seen <= {"t", "r"}, f"без озвучки пришли звуковые игры: {seen}"
    assert "r" in seen, "без озвучки пропало и припоминание, а оно текстовое"
