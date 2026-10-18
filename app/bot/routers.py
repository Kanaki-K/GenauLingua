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
    from app.bot.handlers.admin_rating import router as admin_rating_router
    from app.bot.handlers.chat_status import router as chat_status_router
    from app.bot.handlers.quiz.build import router as build_router
    from app.bot.handlers.quiz.choice import router as choice_router
    from app.bot.handlers.quiz.help import router as help_router
    from app.bot.handlers.quiz.home import router as home_router
    from app.bot.handlers.quiz.lesson import router as lesson_router
    from app.bot.handlers.quiz.match import router as match_router
    from app.bot.handlers.quiz.report import router as report_router
    from app.bot.handlers.quiz.report_inline import router as report_inline_router
    from app.bot.handlers.quiz.settings import router as settings_router
    from app.bot.handlers.quiz.speech import router as speech_router
    from app.bot.handlers.quiz.speech_invite import router as speech_invite_router
    from app.bot.handlers.quiz.expired import router as expired_router
    from app.bot.handlers.quiz.stats import router as stats_router
    from app.bot.handlers.reminders import router as reminders_router
    from app.bot.handlers.start import router as start_router

    ordered = [
        # Блокировка/возврат — свой вид обновления, мешать никому не может
        ("chat_status", chat_status_router),
        # Рейтинги ПЕРВЫМИ: иначе `show_my_rating` перехватывается
        ("leaderboard/monthly", monthly_router),
        ("leaderboard/alltime", alltime_router),
        ("leaderboard/table", table_router),
        # Репорт ПЕРЕД игрой: иначе `report_translation_error` не доходит
        ("quiz/report", report_router),
        # Жалоба на разборе ответа: свои нажатия `rp:`, в любом состоянии
        ("quiz/report_inline", report_inline_router),
        # Дальше всё остальное. Домашний экран, доска и сборка — перед игрой: у них
        # свои нажатия, и перехватывать их не должен никто
        ("start", start_router),
        ("quiz/home", home_router),
        ("quiz/match", match_router),
        # Сетка «Собираю» — рядом с доской и по той же причине: свои
        # нажатия `bd:`, и ловить их, кроме неё, некому
        ("quiz/build", build_router),
        # Игра — блоком из трёх на месте прежнего «quiz/game»: ход занятия,
        # ответ кнопкой, ответ голосом. Речь раньше настроек и статистики,
        # и её `hint_to_speak` отсеивает надписи меню в фильтре
        ("quiz/lesson", lesson_router),
        ("quiz/choice", choice_router),
        ("quiz/speech", speech_router),
        # Приглашение «Говорю» под итогом: свои нажатия, в любом состоянии
        ("quiz/speech_invite", speech_invite_router),
        # Кнопки занятия, которого бот уже не помнит (перезапуск, давно
        # законченное занятие) — ПОСЛЕ игры: живое ловит свои раньше
        ("quiz/expired", expired_router),
        ("quiz/settings", settings_router),
        ("quiz/stats", stats_router),
        ("quiz/help", help_router),
        ("reminders", reminders_router),
        ("admin", admin_router),
        ("admin/rating", admin_rating_router),
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
