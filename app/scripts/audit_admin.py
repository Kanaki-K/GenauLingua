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
import logging
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault("ENV_FILE", ".env.local")

from app.bot.handlers import admin
from app.config import settings
from app.database.session import AsyncSessionLocal

ADMIN_ID = settings.ADMIN_USER

# Эхо SQL забивает отчёт: семнадцать разделов дают сотни запросов
logging.disable(logging.ERROR)


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
    # Сессия передаётся, только если обработчик её просит: отмена рассылки
    # берёт один аргумент, и приёмка валилась на TypeError — то есть врала,
    # будто раздел сломан
    import inspect
    takes_session = len(inspect.signature(handler).parameters) > 1
    try:
        await (handler(cb, session) if takes_session else handler(cb))
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


# ---------------------------------------------------------------- разделы
# Вызывать НЕЛЬЗЯ, и для каждого исключения — причина.
DANGEROUS = {
    # Рассылает текст всем 233 людям без подтверждения
    "admin:broadcast_confirm",
}

# Требуют номер слова в адресе и МЕНЯЮТ данные: подтверждение жалобы
# начисляет баллы и шлёт извещения. Приёмка только читает.
MUTATING_PREFIXES = ("admin:report_approve_", "admin:report_reject_")


def _discover_callbacks() -> list:
    """
    Все обработчики разделов — из разбора `admin.py`, а не из списка.

    Подпись берётся из первой строки описания обработчика; нет описания —
    берётся имя функции. Так новый раздел попадает в приёмку сам, с
    осмысленной подписью, и забыть его нельзя.
    """
    import ast

    source = Path(admin.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    found = []
    for node in tree.body:
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or not decorator.args:
                continue
            target = decorator.args[0]
            # F.data == "admin:…"
            if not (isinstance(target, ast.Compare)
                    and len(target.comparators) == 1
                    and isinstance(target.comparators[0], ast.Constant)
                    and isinstance(target.comparators[0].value, str)):
                continue
            data = target.comparators[0].value
            if not data.startswith("admin:"):
                continue
            doc = ast.get_docstring(node)
            label = (doc.strip().split("\n")[0].rstrip(".")
                     if doc else node.name)
            found.append((label[:24], getattr(admin, node.name), data))

    print(f"разделов найдено в коде: {len(found)}")
    print(f"не вызываются, меняют данные: {', '.join(MUTATING_PREFIXES)}")
    return found


async def main():
    results = []
    bodies = {}

    # ОТКУДА БЕРЁТСЯ СПИСОК РАЗДЕЛОВ.
    #
    # Прежде он был выписан здесь руками, с подписями, — и ровно поэтому
    # новый раздел оказался бы необойдённым: так уже вышло с `admin:games`.
    # Сторож тогда сверял список с кнопками ГЛАВНОЙ клавиатуры, но стоило
    # разделам уйти на второй уровень («Приход» и «Отток» внутри «Людей»),
    # как на главной их не стало — и сторож перестал бы их видеть.
    #
    # Теперь обработчики вынимаются из самого кода: каждый
    # `@router.callback_query(F.data == "admin:…")` в `admin.py`. Список
    # устареть не может — он и есть код.
    callbacks = _discover_callbacks()

    # Исключение обязано указывать на СУЩЕСТВУЮЩИЙ раздел: иначе оно
    # осталось от снятого кода и молча прикрывает что-то другое
    all_found = {data for _, _, data in callbacks}
    stale = sorted(DANGEROUS - all_found)
    if stale:
        print("СТОРОЖ: в опасных названы разделы, которых больше нет: "
              + ", ".join(stale))

    callbacks = [item for item in callbacks if item[2] not in DANGEROUS]
    for name in sorted(DANGEROUS & all_found):
        print(f"не вызывается нарочно: {name} — шлёт всем без спроса")
    print()

    drawn = {
        button.callback_data
        for row in admin.get_admin_keyboard().inline_keyboard
        for button in row
        if button.callback_data
    }
    orphan = sorted(drawn - {data for _, _, data in callbacks})
    if orphan:
        print("СТОРОЖ: кнопка на главной ведёт в пустоту: "
              + ", ".join(orphan) + "\n")

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
