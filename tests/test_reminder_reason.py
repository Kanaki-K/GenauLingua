"""
Повод вернуться: один, измеренный, и правдивый на момент отправки.

ЗАЧЕМ. Напоминание — единственный экран, который человек видит, НЕ заходя
в бота, и единственный замеренный рычаг возврата: у включивших напоминания
6.85 дней занятий против 1.59. А вторым блоком в нём стояла случайная
фраза из шести:

    «Шаг за шагом ты достигаешь результата!»
    «Твоя серия растёт — продолжай в том же духе!»

Ни одна ничего не знала о человеке. Вторая ещё и лгала ПО ПОСТРОЕНИЮ:
фраза выбиралась только тогда, когда шкалы пусты, то есть доставалась
человеку без прогресса и без серии — и сообщала ему, что его серия растёт.

Главная проверка здесь не «есть ли повод», а МЁРТВЫЙ ЛИ ПОВОД: правило
может выглядеть верным и при этом не срабатывать никогда. Так уже вышло
дважды, и оба раза увидел это показ экрана, а не чтение кода:

    «первое выученное близко» перекрывался рубежом — у человека без
    выученных слов словарь мал, и ближайший рубеж всегда рядом;
    новичку с нулём слов доставалось «Слов в работе: 0 · до 10 ещё 10» —
    та самая шкала-ноль, от которой и уходили.
"""

from app.locales import LOCALES
from app.services.reminder_reason import (
    DUE_MANY, FACTS_COUNT, MILESTONE_CLOSE, RANK_MIN_FIELD, STREAK_ALIVE,
    ReminderFacts, pick_reason, reason_line,
)

REASON_KEYS = {
    "remind_streak_risk", "remind_due", "remind_due_many",
    "remind_streak_lost", "remind_milestone_close", "remind_almost_learned",
    "remind_rank", *(f"remind_fact_{i}" for i in range(1, FACTS_COUNT + 1)),
}


def _facts(**kwargs) -> ReminderFacts:
    """Играющий человек без особых событий."""
    base = dict(
        due_words=0, streak_days=0, best_streak=1, active_today=False,
        words_in_work=140, learned=11, almost_learned=0,
        rank=0, rank_field=0, rounds_total=20, days_away=2,
    )
    base.update(kwargs)
    return ReminderFacts(**base)


# ============================================================================
# НИ ОДИН ПОВОД НЕ ДОЛЖЕН БЫТЬ МЁРТВЫМ
# ============================================================================

def test_every_reason_is_reachable():
    """
    У каждого повода есть состояние, в котором он выбирается. Повод,
    недостижимый по построению, — это не осторожность, а мёртвый код,
    который выглядит работающим.
    """
    reachable = {
        pick_reason(facts)[0]
        for facts in (
            _facts(streak_days=7),
            _facts(due_words=12),
            _facts(due_words=DUE_MANY + 1),
            _facts(best_streak=9),
            _facts(words_in_work=44, learned=2),
            _facts(learned=0, almost_learned=3, words_in_work=22),
            _facts(rank=9, rank_field=34),
            *(_facts(words_in_work=0, learned=0, rounds_total=n)
              for n in range(FACTS_COUNT)),
        )
    }
    assert reachable == REASON_KEYS, (
        f"недостижимые поводы: {sorted(REASON_KEYS - reachable)}"
    )


def test_the_first_learned_word_is_not_buried_under_a_milestone():
    """
    Ровно тот дефект, что нашёлся показом. У человека без выученных слов
    словарь мал, рубеж всегда рядом — и редкий повод не доставался никому.
    """
    facts = _facts(learned=0, almost_learned=2, words_in_work=22)
    assert pick_reason(facts) == ("remind_almost_learned", {"count": 2})


def test_a_newcomer_is_not_shown_a_zero():
    """
    При нуле слов рубеж молчит: «Слов в работе: 0 · до 10 ещё 10» — это
    ноль в лицо вместо повода. Новичку идёт замечание о боте.
    """
    key, _ = pick_reason(_facts(words_in_work=0, learned=0, rounds_total=0))
    assert key.startswith("remind_fact_"), key


# ============================================================================
# ЧЕГО НЕТ — О ТОМ НЕ ГОВОРИМ
# ============================================================================

def test_a_single_day_is_not_a_streak_at_risk():
    """
    «Не прерывай серию» при одном дне — призыв не прерывать то, чего не
    было. Та же ложь по форме, что и прежняя фраза про растущую серию.
    """
    key, _ = pick_reason(_facts(streak_days=STREAK_ALIVE - 1, due_words=5))
    assert key != "remind_streak_risk"


def test_a_streak_is_not_at_risk_if_today_is_done():
    """
    Занимался сегодня — серия уже продлена, и пугать потерей нечем.
    Напоминание в такой день говорит о деле, а не о серии.
    """
    key, _ = pick_reason(_facts(streak_days=7, active_today=True, due_words=4))
    assert key == "remind_due"


def test_a_lost_streak_is_mentioned_only_if_it_was_real():
    """Лучшая серия в два дня — не та потеря, о которой стоит писать."""
    key, _ = pick_reason(_facts(best_streak=2))
    assert key != "remind_streak_lost"


def test_a_rank_needs_someone_to_compare_with():
    """
    «Третье место из трёх» не мотивирует. Поле должно быть непустым.
    """
    key, _ = pick_reason(_facts(rank=2, rank_field=RANK_MIN_FIELD - 1))
    assert key != "remind_rank"


def test_a_huge_backlog_does_not_throw_the_number_at_the_face():
    """
    После долгого перерыва просрочено всё: двести слов. Число в такой
    строке не зовёт, а придавливает, — поэтому говорится «начни с одного
    круга», и это тоже правда.
    """
    key, params = pick_reason(_facts(due_words=212))
    assert key == "remind_due_many"
    assert params == {}


# ============================================================================
# ПОРЯДОК: ПО СРОКУ ГОДНОСТИ И ПО ВЕСУ
# ============================================================================

def test_a_streak_at_risk_beats_everything():
    """Серия истекает СЕГОДНЯ, остальные поводы подождут до завтра."""
    key, _ = pick_reason(_facts(
        streak_days=7, due_words=200, best_streak=9, learned=0,
        almost_learned=5, rank=2, rank_field=34, words_in_work=44,
    ))
    assert key == "remind_streak_risk"


def test_a_rare_reason_beats_the_common_one():
    """
    ПОРЯДОК ПО РЕДКОСТИ, А НЕ ПО СИЛЕ. Первая редакция ставила «слова ждут»
    третьим — казалось, дело важнее обещания. Приёмка на живых данных
    показала цену: просроченные слова есть почти у каждого, кто играл
    (140 человек из 233), и три повода ниже не достались НИКОМУ — ни «до
    первого выученного один ответ», ни «лучшая серия была 9 дней», ни
    место в зачёте.

    Частый повод выше редкого делает редкий мёртвым. Поэтому «слова ждут»
    стоит ПОСЛЕ них — он всё равно достанется большинству.
    """
    key, _ = pick_reason(_facts(due_words=7, words_in_work=44))
    assert key == "remind_milestone_close"

    key, _ = pick_reason(_facts(due_words=7, learned=0, almost_learned=2,
                                words_in_work=140))
    assert key == "remind_almost_learned"

    # А когда редких поводов нет — говорится о деле
    key, _ = pick_reason(_facts(due_words=7, words_in_work=140, learned=9))
    assert key == "remind_due"


def test_the_reason_never_runs_out():
    """
    Напоминание без второй строки — голое «пора заниматься», от которого и
    отписываются. Повод обязан найтись при любом состоянии.
    """
    for facts in (
        ReminderFacts(),
        _facts(),
        _facts(words_in_work=0, learned=0, rounds_total=999),
        _facts(due_words=0, best_streak=0, rank=0, words_in_work=2500),
    ):
        key, _ = pick_reason(facts)
        assert key in REASON_KEYS, key


def test_the_fact_rotates_with_rounds_and_not_at_random():
    """
    Замечание меняется по мере занятий и ВОСПРОИЗВОДИТСЯ: случайность
    пришлось бы подменять заглушкой, чтобы проверить хоть что-то.
    """
    seen = [
        pick_reason(_facts(words_in_work=0, learned=0, rounds_total=n))[0]
        for n in range(FACTS_COUNT * 2)
    ]
    assert len(set(seen)) == FACTS_COUNT, seen
    assert seen[:FACTS_COUNT] == seen[FACTS_COUNT:], "вращение не замкнулось"


# ============================================================================
# ТЕКСТ
# ============================================================================

def test_every_reason_key_exists_in_every_locale():
    for lang, texts in LOCALES.items():
        missing = REASON_KEYS - set(texts)
        assert not missing, f"{lang}: нет ключей {sorted(missing)}"


def test_the_dead_cheerleading_keys_are_gone():
    """
    Шесть общих фраз сняты из всех локалей, а не просто перестали
    вызываться: мёртвая строка в локали рано или поздно всплывает на
    экране, потому что выглядит готовой к работе.
    """
    for lang, texts in LOCALES.items():
        left = [key for key in texts if key.startswith("notif_motivation_")]
        assert not left, f"{lang}: остались {left}"


def test_no_reason_carries_a_decorative_mark():
    import re

    allowed = set("·—–…")
    emoji = re.compile(r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿]")
    offenders = []
    for lang, texts in LOCALES.items():
        for key, value in texts.items():
            if key not in REASON_KEYS:
                continue
            for char in emoji.findall(value):
                if char not in allowed:
                    offenders.append(f"{lang}/{key}: {char!r}")
    assert not offenders, "значки в поводах: " + ", ".join(offenders)


def test_every_locale_renders_every_reason():
    """
    Подстановка, которой нет в строке одной локали, превращается в
    «[ERROR: … missing parameter]» — и уезжает человеку в уведомлении.
    """
    cases = [
        _facts(streak_days=7),
        _facts(due_words=12),
        _facts(due_words=DUE_MANY + 1),
        _facts(best_streak=9),
        _facts(words_in_work=44, learned=2),
        _facts(learned=0, almost_learned=3, words_in_work=22),
        _facts(rank=9, rank_field=34),
        *(_facts(words_in_work=0, learned=0, rounds_total=n)
          for n in range(FACTS_COUNT)),
    ]
    for lang in LOCALES:
        for facts in cases:
            line = reason_line(facts, lang)
            assert "MISSING" not in line and "ERROR" not in line, f"{lang}: {line}"
            assert "{" not in line, f"{lang}: неподставленное место — {line}"
            assert line.strip(), f"{lang}: пустая строка повода"


def test_the_milestone_line_never_promises_the_impossible():
    """
    Рубеж объявляется близким только когда он и правда близок: «ещё 6, это
    один круг» при остатке 40 было бы обещанием, которого бот не держит.
    """
    key, params = pick_reason(_facts(words_in_work=60, learned=4))
    if key == "remind_milestone_close":
        assert params["left"] <= MILESTONE_CLOSE, params


# ============================================================================
# НА ЖИВОЙ СБОРКЕ НАПОМИНАНИЯ
# ============================================================================
#
# Проверки выше — про правило и идут без базы. Эти — про то, что повод
# ДОХОДИТ до текста: правило может быть верным, а строка не попасть в
# сообщение вовсе, и ни одна проверка выше этого не заметит.

import pytest  # noqa: E402

from app.database.enums import CEFRLevel, QuizMode  # noqa: E402


async def _ready(session, user, *, words=4):
    from tests.test_home import _seed

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await _seed(session, user, words_a1=words, words_b1=0)
    await session.commit()


@pytest.mark.asyncio
async def test_the_reminder_carries_a_reason(session, user):
    """
    У новичка без прогресса шкал нет — и раньше на их месте стояла
    случайная фраза. Теперь там замечание о боте, и оно обязано быть.
    """
    from app.schedulers.reminder_scheduler import build_reminder_text

    await _ready(session, user)
    text = await build_reminder_text(user, session)

    assert len(text.splitlines()) >= 2, f"повода в напоминании нет: {text!r}"
    # Последняя строка — повод; у новичка это замечание о боте
    assert any(
        LOCALES["ru"][f"remind_fact_{index}"] in text
        for index in range(1, FACTS_COUNT + 1)
    ), f"ни одно замечание не попало в текст: {text!r}"


@pytest.mark.asyncio
async def test_the_reminder_counts_words_waiting_for_review(session, user):
    """
    Слово, просроченное по расписанию, должно попасть в повод числом.
    Расписание бот считает сам — это и есть самое честное «вернись».

    ПОДГОТОВКА ЦЕЛИТ ИМЕННО В ЭТОТ ПОВОД. Первая редакция давала человеку
    одно слово в работе — и получала «Слов в работе: 1 · до 10 ещё 9»:
    рубеж стоит ВЫШЕ и ловил первым. Проверка падала не потому, что код
    неверен, а потому что состояние было выбрано наугад. Поэтому слов
    четырнадцать: следующий рубеж 25, до него 11 — дальше, чем порог
    «близко», и рубеж молчит.
    """
    from datetime import timedelta

    from sqlalchemy import select

    from app.core.clock import utcnow
    from app.database.models import Word
    from app.schedulers.reminder_scheduler import build_reminder_text
    from tests.test_home import _progress

    await _ready(session, user, words=14)
    words = (await session.execute(select(Word))).scalars().all()
    now = utcnow()

    for index, word in enumerate(words):
        row = _progress(user.id, word.id, times_shown=2, times_correct=1)
        row.correct_streak = 0
        # Первое слово просрочено, остальные показаны только что: при серии
        # ноль срок повторения — час
        row.last_seen_at = now - timedelta(days=3) if index == 0 else now
        session.add(row)
    await session.commit()

    text = await build_reminder_text(user, session)
    assert "повторения" in text.lower(), f"просроченное слово не названо: {text!r}"
    assert "Слов в работе" not in text, (
        f"подготовка попала в чужой повод: {text!r}"
    )


@pytest.mark.asyncio
async def test_the_reminder_does_not_praise_a_broken_streak(session, user):
    """
    Главный дефект, который этот блок и чинит: колонка серии
    пересчитывается только на завершении круга, и у остановившегося в ней
    навсегда остаётся последнее значение. Напоминание — худшее место, чтобы
    хвалить за серию, которой нет: человек открывает уведомление и видит
    «1 день подряд» после восьми месяцев молчания.
    """
    from datetime import date, timedelta

    from app.core.clock import utctoday
    from app.schedulers.reminder_scheduler import build_reminder_text

    await _ready(session, user)
    user.streak_days = 7
    user.best_streak_days = 7
    user.last_active_date = utctoday() - timedelta(days=200)
    await session.commit()

    text = await build_reminder_text(user, session)
    assert "подряд" not in text, f"похвала за прерванную серию: {text!r}"


@pytest.mark.asyncio
async def test_a_live_streak_is_the_reason(session, user):
    """А живая серия — повод, и главный: он истекает сегодня."""
    from datetime import timedelta

    from app.core.clock import utctoday
    from app.schedulers.reminder_scheduler import build_reminder_text

    await _ready(session, user)
    user.streak_days = 5
    user.best_streak_days = 5
    user.last_active_date = utctoday() - timedelta(days=1)
    await session.commit()

    text = await build_reminder_text(user, session)
    assert "5" in text and "подряд" in text, f"серия не названа: {text!r}"


# ============================================================================
# «ЭТО ОДИН КРУГ» — ТОЛЬКО ЕСЛИ КРУГ ПРАВДА ДОВЕДЁТ ДО РУБЕЖА
#
# Аудит 14 октября: повод «до 50 ещё 6, это один круг» получали люди с
# 44 просроченными словами — их круг приносит три новых слова, и рубеж
# кругом недостижим. Таких было 12 из 72 получавших повод.
# ============================================================================

def test_milestone_is_not_promised_when_the_round_brings_too_few_new_words():
    facts = _facts(words_in_work=44, due_words=44, new_next_round=3)
    key, _ = pick_reason(facts)
    assert key != "remind_milestone_close", "обещан рубеж, недостижимый за круг"


def test_milestone_is_promised_when_the_round_reaches_it():
    facts = _facts(words_in_work=47, due_words=44, new_next_round=3)
    key, params = pick_reason(facts)
    assert key == "remind_milestone_close", key
    assert params["left"] <= 3


# ============================================================================
# КОГДА ПОРА СЛАТЬ: одна попытка в день и догон после перезапуска
# ============================================================================

def _reminder_user(**kwargs):
    from app.database.models import User

    values = dict(
        id=1, timezone="Europe/Berlin", notification_time="14:00",
        notification_days=list(range(7)), last_notification_sent=None,
    )
    values.update(kwargs)
    return User(**values)


def test_a_reminder_catches_up_after_a_restart():
    """
    Бот лежал в 14:00 — напоминание уходит, когда он поднялся.

    Прежде окно было ±2 минуты: перезапуск в 11:58–12:02 UTC оставлял без
    напоминания на день 117 человек из 121 включивших.
    """
    from datetime import datetime

    from app.schedulers.reminder_scheduler import reminder_is_due

    user = _reminder_user()
    # 14:00 по Берлину 15 октября 2026 — это 12:00 UTC
    assert reminder_is_due(user, datetime(2026, 10, 15, 12, 40))
    assert reminder_is_due(user, datetime(2026, 10, 15, 11, 58))
    assert not reminder_is_due(user, datetime(2026, 10, 15, 11, 50)), "раньше срока"
    assert not reminder_is_due(user, datetime(2026, 10, 15, 15, 1)), "позже трёх часов"


def test_one_attempt_a_day_whatever_its_outcome():
    """Отметка дня стоит — второй попытки сегодня нет, завтра — есть."""
    from datetime import datetime

    from app.schedulers.reminder_scheduler import reminder_is_due

    user = _reminder_user(last_notification_sent=datetime(2026, 10, 15, 11, 58))
    assert not reminder_is_due(user, datetime(2026, 10, 15, 12, 1))
    assert reminder_is_due(user, datetime(2026, 10, 16, 12, 0))


@pytest.mark.asyncio
async def test_a_blocked_bot_is_reported_as_forbidden(session, user):
    """
    Заблокировавший бота — не сбой сети: исход отдельный, по нему
    напоминания выключаются. Прежде попыток было пять в день, вечно.
    """
    from aiogram.exceptions import TelegramForbiddenError
    from aiogram.methods import SendMessage

    from app.schedulers.reminder_scheduler import FORBIDDEN, send_notification_to_user

    class Blocked:
        async def send_message(self, chat_id, text, **kwargs):
            raise TelegramForbiddenError(
                method=SendMessage(chat_id=chat_id, text=text),
                message="Forbidden: bot was blocked by the user",
            )

    assert await send_notification_to_user(Blocked(), user, session) == FORBIDDEN


@pytest.mark.asyncio
async def test_name_with_html_characters_is_escaped(session, user):
    """
    Имя идёт в <b>…</b> HTML-сообщения. «Tom <3» без экранирования Telegram
    отвергал — напоминание не доходило никогда, а бот считал это «прочим
    сбоем» (аудит 2.1).
    """
    from app.schedulers.reminder_scheduler import build_reminder_text

    user.first_name = "Tom <3"
    await session.commit()
    text = await build_reminder_text(user, session)
    assert "Tom &lt;3" in text and "Tom <3" not in text
