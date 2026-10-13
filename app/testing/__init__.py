"""
Обвес для прогонов бота без сети: настоящий диспетчер, поддельный Telegram.

ПОЧЕМУ ЭТО ЛЕЖИТ В `app/`, А НЕ В `tests/`. Пользуются им ДВОЕ: тесты и
приёмочные скрипты из `app/scripts`. Пока он жил в `tests/scenario.py`,
приёмке приходилось бы импортировать тесты — то есть рабочий инструмент
зависел бы от набора проверок, а не наоборот. Один обвес, двое
пользователей, и он стоит выше обоих.

Снаружи подделан РОВНО ОДИН слой — сеть. Роутеры, фильтры, порядок
подключения, обработчики, состояние и база остаются настоящими.
"""

from app.testing.telegram import (
    FAKE_TOKEN,
    RecordingSession,
    make_bot,
    make_dispatcher,
    press,
    reset_state,
    text_update,
    use_session,
)

__all__ = [
    "FAKE_TOKEN",
    "RecordingSession",
    "make_bot",
    "make_dispatcher",
    "press",
    "reset_state",
    "text_update",
    "use_session",
]
