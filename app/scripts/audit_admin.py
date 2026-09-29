# -*- coding: utf-8 -*-
"""
Аудит админ-панели: вызвать каждый обработчик на реальных данных и посмотреть,
что он на самом деле отдаёт.

Статика тут бесполезна — маршруты в порядке, а «не работает» проявляется иначе:
падением на пустых данных, делением на ноль, либо секцией, которая молча
не выводится, потому что колонка никогда не заполнялась.
"""
import asyncio
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault("ENV_FILE", ".env.local")

from app.bot.handlers import admin
from app.config import settings
from app.database.session import AsyncSessionLocal

ADMIN_ID = settings.ADMIN_USER


# ---------------------------------------------------------------- заглушки
class StubBot:
    def __init__(self):
        self.calls = []

    async def send_message(self, chat_id=None, text=None, **kw):
        self.calls.append(("send_message", text or kw.get("text", "")))
        return StubMessage(self)

    async def edit_message_reply_markup(self, **kw):
        self.calls.append(("edit_markup", ""))

    async def send_document(self, **kw):
        self.calls.append(("send_document", ""))


class StubChat:
    id = ADMIN_ID


class StubUser:
    def __init__(self, uid=ADMIN_ID):
        self.id = uid
        self.username = "tester"
        self.first_name = "Tester"
        self.last_name = None


class StubMessage:
    def __init__(self, bot=None, text="", uid=ADMIN_ID):
        self.bot = bot or StubBot()
        self.chat = StubChat()
        self.message_id = 1000
        self.from_user = StubUser(uid)
        self.text = text
        self.sent = []
        self.documents = []
        self.deleted = False

    async def answer(self, text=None, **kw):
        self.sent.append(text or "")
        return StubMessage(self.bot)

    async def answer_document(self, document=None, caption=None, **kw):
        name = getattr(document, "filename", "?")
        self.documents.append((name, caption or ""))
        return StubMessage(self.bot)

    async def edit_text(self, text=None, **kw):
        self.sent.append(text or "")
        return self

    async def edit_reply_markup(self, **kw):
        return self

    async def delete(self):
        self.deleted = True


class StubCallback:
    def __init__(self, data, uid=ADMIN_ID):
        self.bot = StubBot()
        self.data = data
        self.from_user = StubUser(uid)
        self.message = StubMessage(self.bot)
        self.answers = []

    async def answer(self, text=None, show_alert=False, **kw):
        self.answers.append(text or "")


# ---------------------------------------------------------------- проверки
def describe(text: str) -> str:
    if not text:
        return "ПУСТОЙ ОТВЕТ"
    return f"{len(text)} символов"


EMPTY_MARKERS = [
    "нет данных",
    "Нет данных",
    "— Нет",
    "не найден",
]


def find_empty_sections(text: str) -> list[str]:
    """Секции, которые отрисовались как «нет данных» — признак мёртвой колонки."""
    found = []
    for line in text.split("\n"):
        for marker in EMPTY_MARKERS:
            if marker in line:
                found.append(line.strip()[:80])
                break
    return found


async def run_callback(session, name, handler, data):
    cb = StubCallback(data)
    try:
        await handler(cb, session)
    except Exception as exc:
        return name, "ПАДАЕТ", f"{type(exc).__name__}: {exc}", traceback.format_exc()

    text = "\n".join(cb.message.sent)
    docs = cb.message.documents + [c for c in cb.bot.calls if c[0] == "send_document"]
    detail = describe(text)
    if docs:
        detail += f", документов: {len(docs)}"
    return name, "ок", detail, text


async def run_command(session, name, handler, text=""):
    msg = StubMessage(text=text)
    try:
        await handler(msg, session)
    except Exception as exc:
        return name, "ПАДАЕТ", f"{type(exc).__name__}: {exc}", traceback.format_exc()

    body = "\n".join(msg.sent)
    detail = describe(body)
    if msg.documents:
        detail += f", документов: {len(msg.documents)}"
    return name, "ок", detail, body


async def main():
    results = []
    bodies = {}

    callbacks = [
        ("📈 Аналитика", admin.admin_analytics, "admin:analytics"),
        ("👥 Когорты", admin.admin_cohorts, "admin:cohorts"),
        ("⚠️ Churn", admin.admin_churn, "admin:churn"),
        ("📤 Экспорт (меню)", admin.admin_export_menu, "admin:export"),
        ("📤 Экспорт юзеров", admin.admin_export_users, "admin:export_users"),
        ("📤 Экспорт викторин", admin.admin_export_quizzes, "admin:export_quizzes"),
        ("👤 Топ юзеры", admin.admin_top_users_callback, "admin:top_users"),
        ("📊 Детали", admin.admin_detailed_callback, "admin:detailed"),
        ("📝 Репорты", admin.admin_reports, "admin:reports"),
        ("◀️ Назад", admin.admin_back, "admin:back"),
    ]

    commands = [
        ("/admin", admin.admin_panel, ""),
        ("/admin_users", admin.admin_users, "/admin_users"),
        ("/admin_stats", admin.admin_detailed_stats, "/admin_stats"),
        ("/admin_user <id>", admin.admin_user_details, f"/admin_user {ADMIN_ID}"),
        ("/admin_user (без арг.)", admin.admin_user_details, "/admin_user"),
        ("/broadcast (без текста)", admin.broadcast_message, "/broadcast"),
        # /broadcast с текстом НЕ вызываем: он рассылает всем пользователям
        # сразу, без подтверждения. Проверен отдельно на заглушке.
    ]

    async with AsyncSessionLocal() as session:
        for name, handler, data in callbacks:
            res = await run_callback(session, name, handler, data)
            results.append(res[:3])
            bodies[name] = res[3]

        for name, handler, text in commands:
            res = await run_command(session, name, handler, text)
            results.append(res[:3])
            bodies[name] = res[3]

    print("=" * 84)
    print("РЕЗУЛЬТАТ ВЫЗОВА КАЖДОГО ОБРАБОТЧИКА")
    print("=" * 84)
    print(f"{'инструмент':26} {'статус':8} детали")
    broken = []
    for name, status, detail in results:
        mark = "!!" if status != "ок" else "  "
        print(f"{mark} {name:24} {status:8} {detail}")
        if status != "ок":
            broken.append((name, detail))

    print()
    print("=" * 84)
    print("СЕКЦИИ, КОТОРЫЕ ОТРИСОВАЛИСЬ КАК «НЕТ ДАННЫХ»")
    print("=" * 84)
    any_empty = False
    for name, body in bodies.items():
        empties = find_empty_sections(body or "")
        if empties:
            any_empty = True
            print(f"\n{name}:")
            for line in empties:
                print(f"    {line}")
    if not any_empty:
        print("  таких нет")

    print()
    print("=" * 84)
    print("ЧТО АДМИН РЕАЛЬНО ВИДИТ")
    print("=" * 84)
    import re as _re
    for name, body in bodies.items():
        bar = "-" * 84
        print(f"\n{bar}\n### {name}\n{bar}")
        plain = _re.sub(r"</?b>|</?i>|</?code>", "", body or "")
        print(plain.strip() or "(пусто)")

    if broken:
        print()
        print("=" * 84)
        print("ТРАССИРОВКИ ПАДЕНИЙ")
        print("=" * 84)
        async with AsyncSessionLocal() as session:
            for name, handler, data in callbacks:
                if any(name == b[0] for b in broken):
                    res = await run_callback(session, name, handler, data)
                    if res[1] != "ок":
                        print(f"\n--- {name} ---")
                        print(res[3][-1600:])
            for name, handler, text in commands:
                if any(name == b[0] for b in broken):
                    res = await run_command(session, name, handler, text)
                    if res[1] != "ок":
                        print(f"\n--- {name} ---")
                        print(res[3][-1600:])

    return 1 if broken else 0


sys.exit(asyncio.run(main()))
