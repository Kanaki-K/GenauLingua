"""
Рейтинг «за всё время» и согласованность трёх экранов рейтинга.

Жалоба владельца 14 октября 2026: 189 баллов за октябрь, а на вкладке «За
всё время» — «Позиция: —, Баллы: 0, Выучено слов: 0, Начни учить слова», в
таблице за всё время — «Ты ещё не в рейтинге». Причина: «за всё время»
читалось из `users.lifetime_score`, а туда закрытие сезона кладёт только
бонус за место. Месячные баллы не входили никуда — ни текущего месяца, ни
закрытых.

Здесь держится:
  * за всё время = месячные баллы всех сезонов (текущий тоже) + бонусы;
  * закрытие сезона прибавляет ровно бонус, месячный балл не двоится;
  * место на карточке, в таблице и в строке «Ты: #N» — одно число;
  * язык — как у таблицы месяца: немецкие баллы не идут в английскую;
  * совет новичку — только тому, кто на этом языке не сыграл ни круга;
  * «Таблица лидеров» с вкладки «За всё время» ведёт в таблицу за всё время.
"""

from app.bot.handlers.leaderboard.alltime import build_alltime_card
from app.bot.handlers.leaderboard.leaderboard_table import (
    build_alltime_table,
    build_monthly_table,
)
from app.bot.handlers.leaderboard.monthly import get_rating_keyboard
from app.database.models import MonthlyStats, User, UserWord
from app.locales import get_text, plural
from app.services.monthly_leaderboard_service import (
    create_new_season,
    finalize_season,
    get_lifetime_leaderboard,
    get_monthly_leaderboard,
    get_user_lifetime_rank,
    get_user_monthly_rank,
)
from tests.conftest import make_word


async def _users(session, spec):
    """spec: [(id, learning_lang)]"""
    for uid, lang in spec:
        session.add(User(id=uid, first_name=f"U{uid}", learning_lang=lang,
                         native_lang="ru", interface_language="ru"))
    await session.commit()


async def _stats(session, season, rows):
    """rows: [(user_id, learning_lang, monthly_score)]"""
    for uid, lang, score in rows:
        session.add(MonthlyStats(user_id=uid, season_id=season.id,
                                 learning_lang=lang, monthly_score=score,
                                     monthly_quizzes=1))
    await session.commit()


class TestCurrentMonthCountsForAllTime:
    async def test_points_of_open_month_are_in_alltime(self, session):
        """
        Случай владельца один в один: сезоны прошлых месяцев закрыты, у него
        только октябрь — 189 баллов. Было: «Баллы: 0», места нет.
        """
        september = await create_new_season(2026, 9, session)
        await _users(session, [(1, "de"), (2, "de")])
        await _stats(session, september, [(2, "de", 300)])
        await finalize_season(september.id, session)

        october = await create_new_season(2026, 10, session)
        await _stats(session, october, [(1, "de", 189)])

        mine = await get_user_lifetime_rank(1, session, learning_lang="de")
        assert mine["lifetime_score"] == 189
        # 2: 300 за сентябрь + 100 за золото = 400, он выше
        assert mine["rank"] == 2
        assert mine["total_users"] == 2

        board = await get_lifetime_leaderboard(session, learning_lang="de")
        assert [(r["user_id"], r["lifetime_score"], r["rank"]) for r in board] == [
            (2, 400, 1), (1, 189, 2),
        ]

    async def test_closing_season_adds_only_the_award(self, session):
        """
        В момент закрытия сумма не скачет: месячный балл уже стоял в ней,
        прибавляется ровно бонус за место. Двойной счёт (балл из колонки и
        из месячной строки разом) дал бы 189 → 478.
        """
        october = await create_new_season(2026, 10, session)
        await _users(session, [(1, "de"), (2, "de")])
        await _stats(session, october, [(1, "de", 189), (2, "de", 50)])

        before = {r["user_id"]: r["lifetime_score"]
                  for r in await get_lifetime_leaderboard(session, learning_lang="de")}
        await finalize_season(october.id, session)
        after = {r["user_id"]: r["lifetime_score"]
                 for r in await get_lifetime_leaderboard(session, learning_lang="de")}

        assert before == {1: 189, 2: 50}
        assert after == {1: 189 + 100, 2: 50 + 50}

    async def test_alltime_is_per_learning_language(self, session):
        """
        Как месяц: английские баллы не идут в немецкую таблицу и не дают
        места в ней.
        """
        october = await create_new_season(2026, 10, session)
        await _users(session, [(1, "de"), (2, "en")])
        await _stats(session, october, [(1, "de", 10), (2, "en", 999), (1, "en", 500)])

        de = await get_lifetime_leaderboard(session, learning_lang="de")
        assert [(r["user_id"], r["lifetime_score"]) for r in de] == [(1, 10)]

        mine = await get_user_lifetime_rank(1, session, learning_lang="de")
        assert (mine["rank"], mine["total_users"], mine["lifetime_score"]) == (1, 1, 10)


class TestScreensAgree:
    async def test_eleventh_place_is_known_on_card_and_under_table(self, session):
        """
        Место не ищется в первой десятке. Было: одиннадцатый — «Позиция: —»
        на карточке и «за пределами топ-10» под таблицей, а «из N» было
        размером таблицы — «из 10» при двенадцати участниках.
        """
        october = await create_new_season(2026, 10, session)
        ids = list(range(1, 13))
        await _users(session, [(uid, "de") for uid in ids])
        # 1 → 120 баллов, 2 → 110, …, 12 → 10: одиннадцатый — id 11
        await _stats(session, october, [(uid, "de", 130 - uid * 10) for uid in ids])

        board = await get_lifetime_leaderboard(session, limit=10, learning_lang="de")
        mine = await get_user_lifetime_rank(11, session, learning_lang="de")
        assert (mine["rank"], mine["total_users"], mine["lifetime_score"]) == (11, 12, 20)

        table = build_alltime_table(board, mine, 11, "ru")
        expected = get_text("table_you_not_in_top", "ru", rank=11, total=12,
                            score=plural(20, "plural_points", "ru"))
        assert expected in table

        card = build_alltime_card(None, mine, "ru")
        assert get_text("rating_position_alltime", "ru", rank=11) in card
        assert get_text("rating_points", "ru", score=20) in card

    async def test_card_table_and_you_line_show_one_number(self, session):
        """В десятке: строка таблицы, «Ты: #N из M» и карточка — одно место."""
        october = await create_new_season(2026, 10, session)
        await _users(session, [(1, "de"), (2, "de"), (3, "de")])
        await _stats(session, october, [(1, "de", 300), (2, "de", 189), (3, "de", 5)])

        board = await get_lifetime_leaderboard(session, learning_lang="de")
        mine = await get_user_lifetime_rank(2, session, learning_lang="de")
        row = next(r for r in board if r["user_id"] == 2)

        assert row["rank"] == mine["rank"] == 2
        assert row["lifetime_score"] == mine["lifetime_score"] == 189
        table = build_alltime_table(board, mine, 2, "ru")
        assert get_text("table_you_in_top", "ru", rank=2, total=3) in table
        assert get_text("table_you_not_ranked", "ru") not in table

    async def test_tie_gets_one_place_in_month_table_and_you_line(self, session):
        """
        Равные баллы — равное место. Было: в таблице месяца порядковый номер
        строки (второй и третий), а «Ты: #N» — «1 + сколько выше» (оба #2):
        у третьего на одном экране два места.
        """
        october = await create_new_season(2026, 10, session)
        await _users(session, [(1, "de"), (2, "de"), (3, "de")])
        await _stats(session, october, [(1, "de", 100), (2, "de", 40), (3, "de", 40)])

        board = await get_monthly_leaderboard(session, october.id, learning_lang="de")
        for uid in (2, 3):
            mine = await get_user_monthly_rank(uid, session, october.id, learning_lang="de")
            row = next(r for r in board if r["user_id"] == uid)
            assert row["rank"] == mine["rank"] == 2

        lifetime = await get_lifetime_leaderboard(session, learning_lang="de")
        assert [r["rank"] for r in lifetime] == [1, 2, 2]

        text = build_monthly_table(board, mine, october, 3, "ru")
        assert get_text("table_you_in_top", "ru", rank=2, total=3) in text


class TestCardTexts:
    async def test_no_beginner_advice_to_who_has_played(self, session):
        """
        «Начни учить слова — первый шаг самый важный!» человеку со 189
        баллами — не по адресу. Совет новичку — только без месячной строки.
        """
        october = await create_new_season(2026, 10, session)
        await _users(session, [(1, "de"), (2, "de")])
        await _stats(session, october, [(1, "de", 189)])

        played = build_alltime_card(None, await get_user_lifetime_rank(1, session, "de"), "ru")
        fresh = build_alltime_card(None, await get_user_lifetime_rank(2, session, "de"), "ru")

        start = get_text("rating_motivation_start", "ru")
        assert start not in played
        assert get_text("rating_motivation_continue", "ru") in played
        assert start in fresh
        assert get_text("rating_position_none", "ru") in fresh

    async def test_learned_words_counted_from_progress_of_this_language(self, session):
        """
        «Выучено слов» — из `user_words` по изучаемому языку, а не из колонки
        `users.words_learned`, которую пересчитывает конец круга по ТЕКУЩЕМУ
        языку человека.
        """
        october = await create_new_season(2026, 10, session)
        await _users(session, [(1, "de")])
        await _stats(session, october, [(1, "de", 10)])
        words = [make_word(f"Wort{i}") for i in range(3)]
        session.add_all(words)
        await session.flush()
        for word, lang, learned in ((words[0], "de", True), (words[1], "de", False),
                                    (words[2], "en", True)):
            session.add(UserWord(user_id=1, word_id=word.id, learning_lang=lang,
                                 correct_streak=3 if learned else 1, learned=learned))
        user = await session.get(User, 1)
        user.words_learned = 7  # колонка врёт нарочно: читать её нельзя
        await session.commit()

        mine = await get_user_lifetime_rank(1, session, learning_lang="de")
        assert mine["words_learned"] == 1


class TestTableButtonFollowsTab:
    def test_table_button_opens_the_open_tab(self):
        """
        Было: с вкладки «За всё время» кнопка «Таблица лидеров» вела в
        таблицу месяца («Таблица лидеров — Октябрь 2026»).
        """
        def table_cb(tab):
            kb = get_rating_keyboard("ru", tab)
            return kb.inline_keyboard[1][0].callback_data

        assert table_cb("alltime") == "leaderboard_table_alltime"
        assert table_cb("monthly") == "leaderboard_table_monthly"
