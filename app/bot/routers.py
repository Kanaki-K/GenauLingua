"""
Набор роутеров и ПОРЯДОК их подключения — в одном месте.

ЗАЧЕМ ОТДЕЛЬНЫЙ МОДУЛЬ. Этот список был выписан трижды: в `app.main`, в
приёмке меню (`verify_buttons`) и в сценарных тестах. Три списка об одном
расходятся всегда — и разошлись: добавив четвёртую игру в `app.main`, я
забыл про остальные два, и приёмка объявила кнопку `match_start` мёртвой.
Она была права формально и ошибалась по сути: обработчик есть, его просто
не было в ЕЁ копии списка.

То же правило, по которому в проекте сведены `STATE.md` с `HANDOVER.md` и
надписи кнопок с локалями: **один источник, остальные на него смотрят.**

ПОРЯДОК ЗНАЧИМ. Он решает, кто поймает нажатие первым, и один из
разобранных дефектов был ровно про это: подсказка про голос гасила кнопки
меню, потому что роутер игры подключён раньше настроек. Поэтому порядок
задан здесь списком, а не собирается по модулям автоматически.
"""

from __future__ import annotations

from aiogram import Dispatcher, Router


def all_routers() -> list[Router]:
    """Роутеры в порядке подключения. Первый ловит нажатие первым."""
    from app.bot.handlers.admin import router as admin_router
    from app.bot.handlers.leaderboard.alltime import router as alltime_router
    from app.bot.handlers.leaderboard.leaderboard_table import router as table_router
    from app.bot.handlers.leaderboard.monthly import router as monthly_router
    from app.bot.handlers.quiz.game import router as game_router
    from app.bot.handlers.quiz.help import router as help_router
    from app.bot.handlers.quiz.home import router as home_router
    from app.bot.handlers.quiz.match import router as match_router
    from app.bot.handlers.quiz.report import router as report_router
    from app.bot.handlers.quiz.settings import router as settings_router
    from app.bot.handlers.quiz.stats import router as stats_router
    from app.bot.handlers.reminders import router as reminders_router
    from app.bot.handlers.start import router as start_router

    ordered = [
        # Рейтинги ПЕРВЫМИ: иначе `show_my_rating` перехватывается
        ("leaderboard/monthly", monthly_router),
        ("leaderboard/alltime", alltime_router),
        ("leaderboard/table", table_router),
        # Репорт ПЕРЕД игрой: иначе `report_translation_error` не доходит
        ("quiz/report", report_router),
        # Дальше всё остальное. Домашний экран и доска — перед игрой: у них
        # свои нажатия, и перехватывать их не должен никто
        ("start", start_router),
        ("quiz/home", home_router),
        ("quiz/match", match_router),
        ("quiz/game", game_router),
        ("quiz/settings", settings_router),
        ("quiz/stats", stats_router),
        ("quiz/help", help_router),
        ("reminders", reminders_router),
        ("admin", admin_router),
    ]

    # Имя ставится здесь, потому что по умолчанию aiogram даёт роутеру
    # шестнадцатеричный адрес, и в логе «0x18546d10cd0» не говорит ничего.
    # Имя же — ровно то, по чему человек найдёт файл.
    for name, router in ordered:
        router.name = name

    return [router for _, router in ordered]


def attach_routers(dp: Dispatcher) -> Dispatcher:
    """Подключить все роутеры к диспетчеру в правильном порядке."""
    for router in all_routers():
        dp.include_router(router)
    return dp
