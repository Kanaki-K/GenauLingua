#!/usr/bin/env python3
"""
Проверка целостности проекта GenauLingua после рефакторинга.

Запуск:
  python check_integrity.py

Что проверяет:
  1. Все модули импортируются без ошибок
  2. Нет дубликатов функций delete_messages_fast / ensure_anchor
  3. PartOfSpeech определён только в enums.py
  4. Нет print() в хендлерах (только logger)
  5. Все файлы из структуры проекта существуют
  6. Нет мёртвых импортов (удалённые модули)
"""

import os
import sys
import re
from pathlib import Path

# Определяем корень проекта
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR  # скрипт лежит в корне проекта

# Добавляем корень в sys.path
sys.path.insert(0, str(PROJECT_ROOT))

PASSED = 0
FAILED = 0
WARNINGS = 0


def ok(msg):
    global PASSED
    PASSED += 1
    print(f"  ✅ {msg}")


def fail(msg):
    global FAILED
    FAILED += 1
    print(f"  ❌ {msg}")


def warn(msg):
    global WARNINGS
    WARNINGS += 1
    print(f"  ⚠️ {msg}")


# ============================================================================
# 1. ПРОВЕРКА ИМПОРТОВ
# ============================================================================

def check_imports():
    print("\n📦 1. Проверка импортов модулей...")

    modules = [
        "app.config",
        "app.database.enums",
        "app.database.models",
        "app.database.session",
        "app.bot.states",
        "app.bot.utils",
        "app.bot.keyboards",
        "app.bot.keyboards.notifications",
        "app.bot.handlers.start",
        "app.bot.handlers.admin",
        "app.bot.handlers.reminders",
        "app.bot.handlers.quiz.game",
        "app.bot.handlers.quiz.settings",
        "app.bot.handlers.quiz.stats",
        "app.bot.handlers.quiz.help",
        "app.bot.handlers.leaderboard.monthly",
        "app.bot.handlers.leaderboard.alltime",
        "app.bot.handlers.leaderboard.leaderboard_table",
        "app.bot.handlers.leaderboard.utils",
        "app.services.quiz_service",
        "app.services.monthly_leaderboard_service",
        "app.schedulers.reminder_scheduler",
        "app.schedulers.season_scheduler",
        "app.locales",
        "app.locales.ru",
        "app.locales.uk",
        "app.locales.en",
        "app.locales.tr",
        "app.utils.timezones",
        "app.core.logging",
        "app.core.sentry",
    ]

    for module_name in modules:
        try:
            __import__(module_name)
            ok(f"{module_name}")
        except Exception as e:
            fail(f"{module_name} — {type(e).__name__}: {e}")


# ============================================================================
# 2. ПРОВЕРКА ДУБЛИКАТОВ ФУНКЦИЙ
# ============================================================================

def check_no_duplicate_functions():
    print("\n🔍 2. Проверка дубликатов функций...")

    handler_files = [
        "app/bot/handlers/quiz/game.py",
        "app/bot/handlers/quiz/help.py",
        "app/bot/handlers/quiz/settings.py",
        "app/bot/handlers/quiz/stats.py",
        "app/bot/handlers/start.py",
        "app/bot/handlers/leaderboard/monthly.py",
    ]

    functions_to_check = ["delete_messages_fast", "ensure_anchor"]

    for filepath in handler_files:
        full_path = PROJECT_ROOT / filepath
        if not full_path.exists():
            fail(f"{filepath} не найден")
            continue

        content = full_path.read_text(encoding="utf-8")

        for func_name in functions_to_check:
            pattern = f"async def {func_name}"
            matches = content.count(pattern)
            if matches > 0:
                fail(f"{filepath}: содержит локальную {func_name}() — должна быть в utils.py")
            else:
                ok(f"{filepath}: нет локальной {func_name}()")


# ============================================================================
# 3. ПРОВЕРКА PartOfSpeech
# ============================================================================

def check_partofspeech():
    print("\n🏷️ 3. Проверка PartOfSpeech...")

    enums_path = PROJECT_ROOT / "app/database/enums.py"
    models_path = PROJECT_ROOT / "app/database/models.py"

    # Должен быть в enums.py
    if enums_path.exists():
        content = enums_path.read_text(encoding="utf-8")
        if "class PartOfSpeech" in content:
            ok("PartOfSpeech определён в enums.py")
        else:
            fail("PartOfSpeech НЕ найден в enums.py")
    else:
        fail("enums.py не найден")

    # НЕ должен быть в models.py
    if models_path.exists():
        content = models_path.read_text(encoding="utf-8")
        if "class PartOfSpeech" in content:
            fail("PartOfSpeech всё ещё определён в models.py — дубликат!")
        else:
            ok("models.py не содержит дубль PartOfSpeech")

        if "from app.database.enums import" in content and "PartOfSpeech" in content:
            ok("models.py импортирует PartOfSpeech из enums.py")
        else:
            fail("models.py не импортирует PartOfSpeech из enums.py")


# ============================================================================
# 4. ПРОВЕРКА print() В ХЕНДЛЕРАХ
# ============================================================================

def check_no_prints():
    print("\n🖨️ 4. Проверка отсутствия print() в хендлерах...")

    files_to_check = [
        "app/bot/handlers/quiz/game.py",
        "app/bot/handlers/quiz/help.py",
        "app/bot/handlers/quiz/settings.py",
        "app/bot/handlers/quiz/stats.py",
        "app/bot/handlers/start.py",
        "app/bot/handlers/leaderboard/monthly.py",
        "app/bot/handlers/admin.py",
        "app/bot/handlers/reminders.py",
        "app/services/monthly_leaderboard_service.py",
    ]

    for filepath in files_to_check:
        full_path = PROJECT_ROOT / filepath
        if not full_path.exists():
            fail(f"{filepath} не найден")
            continue

        content = full_path.read_text(encoding="utf-8")
        # Ищем print( но не в комментариях и не в строках
        lines = content.split("\n")
        print_lines = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if "print(" in stripped and not stripped.startswith('"') and not stripped.startswith("'"):
                print_lines.append(i)

        if print_lines:
            fail(f"{filepath}: print() на строках {print_lines}")
        else:
            ok(f"{filepath}: нет print()")


# ============================================================================
# 5. ПРОВЕРКА СТРУКТУРЫ ФАЙЛОВ
# ============================================================================

def check_file_structure():
    print("\n📁 5. Проверка структуры проекта...")

    # Файлы которые ДОЛЖНЫ существовать
    required_files = [
        "app/main.py",
        "app/config.py",
        "app/bot/utils.py",
        "app/bot/states.py",
        "app/bot/keyboards/__init__.py",
        "app/bot/keyboards/notifications.py",
        "app/bot/handlers/start.py",
        "app/bot/handlers/admin.py",
        "app/bot/handlers/reminders.py",
        "app/bot/handlers/quiz/game.py",
        "app/bot/handlers/quiz/settings.py",
        "app/bot/handlers/quiz/stats.py",
        "app/bot/handlers/quiz/help.py",
        "app/bot/handlers/leaderboard/monthly.py",
        "app/bot/handlers/leaderboard/alltime.py",
        "app/bot/handlers/leaderboard/leaderboard_table.py",
        "app/bot/handlers/leaderboard/utils.py",
        "app/bot/handlers/leaderboard/__init__.py",
        "app/database/enums.py",
        "app/database/models.py",
        "app/database/session.py",
        "app/services/quiz_service.py",
        "app/services/monthly_leaderboard_service.py",
        "app/schedulers/reminder_scheduler.py",
        "app/schedulers/season_scheduler.py",
        "app/locales/__init__.py",
        "app/locales/ru.py",
        "app/locales/uk.py",
        "app/locales/en.py",
        "app/locales/tr.py",
        "app/utils/timezones.py",
        "app/core/logging.py",
        "app/core/sentry.py",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.prod.yml",
        "requirements.txt",
        "alembic.ini",
        "alembic/env.py",
    ]

    # Файлы которые НЕ ДОЛЖНЫ существовать (удалены)
    deleted_files = [
        "app/bot/handlers/__init__.py",
        "app/bot/handlers/leaderboard/personal.py",
        "privacy.html",
    ]

    for filepath in required_files:
        full_path = PROJECT_ROOT / filepath
        if full_path.exists():
            ok(f"{filepath}")
        else:
            fail(f"{filepath} — НЕ НАЙДЕН")

    for filepath in deleted_files:
        full_path = PROJECT_ROOT / filepath
        if full_path.exists():
            warn(f"{filepath} — должен быть удалён")
        else:
            ok(f"{filepath} — удалён")


# ============================================================================
# 6. ПРОВЕРКА УДАЛЁННЫХ ИМПОРТОВ
# ============================================================================

def check_dead_imports():
    print("\n💀 6. Проверка мёртвых импортов...")

    # Проверяем что никто не импортирует удалённые модули
    dead_imports = [
        "personal_router",
        "from app.bot.handlers.leaderboard.personal",
        "get_quiz_word_count_keyboard",
    ]

    all_py_files = list((PROJECT_ROOT / "app").rglob("*.py"))

    for dead_import in dead_imports:
        found_in = []
        for py_file in all_py_files:
            content = py_file.read_text(encoding="utf-8")
            if dead_import in content:
                rel_path = py_file.relative_to(PROJECT_ROOT)
                found_in.append(str(rel_path))

        if found_in:
            fail(f"'{dead_import}' всё ещё используется в: {', '.join(found_in)}")
        else:
            ok(f"'{dead_import}' нигде не используется")


# ============================================================================
# 7. ПРОВЕРКА ALEMBIC.INI
# ============================================================================

def check_alembic():
    print("\n🔐 7. Проверка alembic.ini...")

    alembic_path = PROJECT_ROOT / "alembic.ini"
    if not alembic_path.exists():
        fail("alembic.ini не найден")
        return

    content = alembic_path.read_text(encoding="utf-8")

    if "genau_password" in content:
        fail("alembic.ini содержит пароль!")
    else:
        ok("alembic.ini без credentials")


# ============================================================================
# 8. ПРОВЕРКА MIDDLEWARE (rollback)
# ============================================================================

def check_middleware():
    print("\n🛡️ 8. Проверка middleware...")

    main_path = PROJECT_ROOT / "app/main.py"
    if not main_path.exists():
        fail("app/main.py не найден")
        return

    content = main_path.read_text(encoding="utf-8")

    if "await session.rollback()" in content:
        ok("Rollback в middleware присутствует")
    else:
        fail("Rollback в middleware ОТСУТСТВУЕТ")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("🔍 GenauLingua — Проверка целостности проекта")
    print("=" * 50)

    check_file_structure()
    check_no_duplicate_functions()
    check_partofspeech()
    check_no_prints()
    check_dead_imports()
    check_alembic()
    check_middleware()

    # Импорты проверяем только если есть .env (нужен для config)
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        check_imports()
    else:
        print("\n📦 1. Проверка импортов...")
        warn("Пропущено — нет .env файла (нужен для app.config)")

    print("\n" + "=" * 50)
    print(f"📊 Результат: ✅ {PASSED} passed  ❌ {FAILED} failed  ⚠️ {WARNINGS} warnings")
    print("=" * 50)

    if FAILED > 0:
        print("\n💡 Есть ошибки — исправь перед деплоем!")
        sys.exit(1)
    else:
        print("\n🚀 Всё чисто — можно деплоить!")
        sys.exit(0)