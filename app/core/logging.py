import logging
import logging.handlers
import os
import sys

def setup_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_dir = os.getenv("LOG_DIR", "./logs")
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    root = logging.getLogger()
    root.setLevel(level)

    # ЖУРНАЛ ПИШЕТСЯ В UTF-8 ПРИ ЛЮБОЙ КОНСОЛИ. На Windows stdout в cp1251/
    # cp866, и строка со значком или словом вроде 'żółw' падала
    # UnicodeEncodeError и терялась ЦЕЛИКОМ — в том числе сторож «игра вслух
    # включена, а распознавателя нет». Снимать значки списком (af9b479) не
    # помогло: слова из базы в журнал всё равно попадают. Правило вместо
    # списка — нераспечатываемое экранируется, а не роняет запись.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
        except (AttributeError, ValueError):
            pass  # подменённый поток (тесты, pythonw) — оставляем как есть

    # Console (docker logs)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    # Rotating file logs
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
