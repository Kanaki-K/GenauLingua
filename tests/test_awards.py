# -*- coding: utf-8 -*-
"""
НАГРАДЫ: человек о них узнаёт, и ровно один раз.

ЗАЧЕМ. Сезон закрывался молча: награды записаны, `lifetime_score` вырос,
серия побед обновлена — и ни один человек об этом не узнавал. Владелец
просил обратного: «награды, баджи за викторины (которые были в проде) —
важно сохранить. Это повышает их ценность». Награда, о которой не сказали,
ценности не добавляет.

Та же форма дефекта уже встречалась у жалобы на перевод: баллы
начислялись, а автору не сообщалось ничего, хотя бот обещал награду. Тогда
это нашлось случайно. Теперь проверяется.

ГЛАВНОЕ ЗДЕСЬ — ВТОРОЙ ТЕСТ. Закрытие сезона вызывается первого числа по
расписанию И каждый час страховкой, на случай выключенного бота. Без
отметки `notified_at` победитель получал бы поздравление КАЖДЫЙ ЧАС.
"""

import pytest

from app.database.models import MonthlyAward, MonthlySeason, MonthlyStats
from app.services.monthly_leaderboard_service import (
    AWARD_MARKS, award_mark, notify_season_awards,
)

# Асинхронная метка ставится поимённо: три проверки ниже синхронные,
# и общая метка давала бы на них предупреждение.


class FakeBot:
    """Бот, который помнит, кому и что отправил."""

    def __init__(self, fail: bool = False):
        self.sent: list[tuple[int, str]] = []
        self.fail = fail

    async def send_message(self, chat_id, text, **kwargs):
        if self.fail:
            raise RuntimeError("человек закрыл бота")
        self.sent.append((chat_id, text))


async def _season(session) -> MonthlySeason:
    from datetime import date

    season = MonthlySeason(
        year=2026, month=10, is_active=False,
        start_date=date(2026, 10, 1), end_date=date(2026, 10, 31),
    )
    session.add(season)
    await session.commit()
    return season


async def _award(session, season, user, rank: int = 1,
                 award_type: str = "gold", bonus: int = 100) -> MonthlyAward:
    award = MonthlyAward(
        user_id=user.id, season_id=season.id, rank=rank,
        award_type=award_type, lifetime_bonus=bonus,
    )
    session.add(award)
    await session.commit()
    return award


@pytest.mark.asyncio
async def test_the_winner_is_told(session, user):
    """Самое простое и самое важное: человеку сообщили."""
    season = await _season(session)
    await _award(session, season, user)

    bot = FakeBot()
    sent = await notify_season_awards(bot, session)

    assert sent == 1, "о награде не сообщили"
    assert bot.sent[0][0] == user.id
    text = bot.sent[0][1]
    assert "🥇" in text, f"в поздравлении нет медали: {text!r}"
    assert "100" in text, f"в поздравлении нет бонуса: {text!r}"


@pytest.mark.asyncio
async def test_nobody_is_told_twice(session, user):
    """
    Второй прогон не сообщает НИЧЕГО.

    Сломай это — и победитель получит поздравление каждый час до смены
    сезона: страховочная проверка идёт по расписанию, а не один раз.
    """
    season = await _season(session)
    await _award(session, season, user)

    bot = FakeBot()
    assert await notify_season_awards(bot, session) == 1
    assert await notify_season_awards(bot, session) == 0
    assert len(bot.sent) == 1, f"отправлено {len(bot.sent)} раз"


@pytest.mark.asyncio
async def test_a_failed_delivery_keeps_the_award_unnotified(session, user):
    """
    Не доставили — отметка не ставится, и награда уйдёт в следующий раз.

    Человек мог закрыть бота. Поставь отметку до отправки, и поздравление
    пропало бы навсегда; а награда уже записана, и она не виновата.
    """
    season = await _season(session)
    award = await _award(session, season, user)

    assert await notify_season_awards(FakeBot(fail=True), session) == 0
    await session.refresh(award)
    assert award.notified_at is None, "награда помечена, хотя не доставлена"

    # Со второго раза, когда бот снова на связи
    bot = FakeBot()
    assert await notify_season_awards(bot, session) == 1


@pytest.mark.asyncio
async def test_top10_has_no_medal_but_is_still_told(session, user):
    """
    Четвёртое место — без медали, но с извещением.

    Медаль называет первые три места. Дать её всем десяти значило бы
    обесценить три первые; не сказать человеку про десятое — значило бы
    вернуть ту самую тишину, против которой всё это и написано.
    """
    season = await _season(session)
    await _award(session, season, user, rank=4, award_type="top10", bonus=10)

    bot = FakeBot()
    assert await notify_season_awards(bot, session) == 1
    text = bot.sent[0][1]
    assert not (set("🥇🥈🥉") & set(text)), f"у десятки появилась медаль: {text!r}"
    assert "4" in text, f"место не названо: {text!r}"


def test_medals_belong_to_the_first_three_only():
    """Таблица наград: медаль есть у трёх типов и только у них."""
    assert award_mark("gold") == "🥇"
    assert award_mark("silver") == "🥈"
    assert award_mark("bronze") == "🥉"
    assert award_mark("top10") == ""
    assert award_mark("чего-то-такого-нет") == ""
    assert len([m for m in AWARD_MARKS.values() if m]) == 3


def test_the_leaderboard_shows_medals_instead_of_numbers():
    """
    С 17.10 в таблице МЕСТО — ЧИСЛОМ, медалей нет: 🥇 в таблице текущего
    месяца путала бы — медаль выдают в конце месяца (владелец: «не нравится
    обилие эмодзи, которые ещё не ясно что значат»). Медали — в карточке
    «За всё время» и в коллекции.
    """
    from app.bot.handlers.leaderboard.leaderboard_table import _rows

    rows = [{"user_id": i, "rank": i, "display_name": f"N{i}", "lifetime_score": 100 - i}
            for i in range(1, 5)]
    text = "\n".join(_rows(rows, 1, None, None)[0])
    assert "1. <b>N1</b>" in text and "4. N4" in text, text
    for medal in ("🥇", "🥈", "🥉"):
        assert medal not in text, text


def test_month_is_named_in_every_interface_language():
    """
    Название месяца — на языке человека.

    Прежде выбор шёл цепочкой условий, в которую не попали немецкий и
    польский: читающий бота по-немецки видел «Октябрь» русскими буквами.
    Два языка из шести.
    """
    from app.bot.handlers.leaderboard.utils import MONTH_NAMES, format_month_name
    from app.locales import LOCALES

    missing = sorted(set(LOCALES) - set(MONTH_NAMES))
    assert not missing, f"языки без названий месяцев: {missing}"

    for lang in LOCALES:
        names = {format_month_name(m, lang) for m in range(1, 13)}
        assert len(names) == 12, f"{lang}: месяцы повторяются"

    assert format_month_name(10, "de") == "Oktober"
    assert format_month_name(10, "pl") == "Październik"
    # Неизвестный язык и негодный номер не ломают экран
    assert format_month_name(10, "xx") == "10"
    assert format_month_name(0, "ru") == "0"


# ============================================================================
# ДОСЫЛКА: КАЖДЫЙ ЧАС, НО ТОЛЬКО СВЕЖЕЕ (аудит 14 октября)
#
# Прежде извещение звалось один раз, при закрытии сезона: недоставленное не
# повторялось, а через месяц уходило вместе с наградами следующего сезона.
# ============================================================================

@pytest.mark.asyncio
async def test_an_old_award_is_not_sent_a_month_late(session, user):
    """Награда старше трёх суток не досылается: поздравлять с забытым — хуже тишины."""
    from datetime import timedelta

    from app.core.clock import utcnow

    season = await _season(session)
    award = await _award(session, season, user)
    award.created_at = utcnow() - timedelta(days=10)
    await session.commit()

    bot = FakeBot()
    assert await notify_season_awards(bot, session) == 0
    assert not bot.sent, "поздравление за прошлый сезон ушло через месяц"


@pytest.mark.asyncio
async def test_a_blocked_winner_is_not_retried_every_hour(session, user):
    """Заблокировал бота — извещение закрывается, а не повторяется каждый час."""
    from aiogram.exceptions import TelegramForbiddenError
    from aiogram.methods import SendMessage

    class Blocked:
        def __init__(self):
            self.tries = 0

        async def send_message(self, chat_id, text, **kwargs):
            self.tries += 1
            raise TelegramForbiddenError(
                method=SendMessage(chat_id=chat_id, text=text),
                message="Forbidden: bot was blocked by the user",
            )

    season = await _season(session)
    await _award(session, season, user)

    bot = Blocked()
    await notify_season_awards(bot, session)
    await notify_season_awards(bot, session)
    assert bot.tries == 1, f"попыток {bot.tries}: заблокировавшему пишем каждый час"


@pytest.mark.asyncio
async def test_top10_notice_names_the_place_once(session, user):
    """«#5 … место 5» — номер дважды; остаться должен один."""
    season = await _season(session)
    await _award(session, season, user, rank=5, award_type="top10", bonus=10)

    bot = FakeBot()
    await notify_season_awards(bot, session)
    text = bot.sent[0][1]
    assert "#5" not in text, f"номер дважды: {text!r}"
    assert not text.startswith(" "), f"пустой знак оставил пробел: {text!r}"
