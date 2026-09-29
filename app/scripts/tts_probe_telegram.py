# -*- coding: utf-8 -*-
"""
Проверка на живом Telegram API: можно ли вести карточку одним сообщением,
если в ней есть аудио.

От ответа зависит архитектура. Бот сейчас держит одну карточку и редактирует
её: вопрос → разбор → следующий вопрос. Если голосовое сообщение нельзя
отредактировать, придётся на каждый вопрос присылать новое — и за викторину
из 25 вопросов чат забьётся 25 голосовыми.

Проверяем:
  1. принимает ли Telegram mp3 от edge-tts без конвертации в ogg/opus
  2. можно ли прицепить к звуку подпись и инлайн-кнопки
  3. можно ли потом отредактировать подпись, кнопки и сам звук
  4. переиспользуется ли file_id (загрузка один раз навсегда)

    python -m app.scripts.tts_probe_telegram

Результат прогона (проверено на живом API): всё выше работает. sendVoice
может быть запрещён настройкой приватности получателя — тогда нужен
фолбэк на sendAudio, карточка при этом остаётся одним сообщением.
"""
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from app.config import settings

API = f"https://api.telegram.org/bot{settings.BOT_TOKEN}"
CHAT = str(settings.ADMIN_USER)


def call(method: str, **params):
    data = urllib.parse.urlencode(params, encoding="utf-8").encode("utf-8")
    req = urllib.request.Request(f"{API}/{method}", data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode("utf-8"))


def upload(method: str, field: str, path: pathlib.Path, **params):
    boundary = "----GenauLinguaProbe"
    body = b""
    for key, value in params.items():
        body += (
            f"--{boundary}\r\nContent-Disposition: form-data; "
            f'name="{key}"\r\n\r\n{value}\r\n'
        ).encode("utf-8")
    body += (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{path.name}"\r\n'
        f"Content-Type: audio/mpeg\r\n\r\n"
    ).encode("utf-8")
    body += path.read_bytes()
    body += f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{API}/{method}", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode("utf-8"))


def verdict(label: str, ok: bool, detail: str = "") -> bool:
    print(f"{'OK  ' if ok else 'FAIL'}  {label}" + (f"  — {detail}" if detail else ""))
    return ok


path = pathlib.Path("tts_samples/demo_word.mp3")
if not path.exists():
    print("нет tts_samples/demo_word.mp3 — сначала tools_demo_audio.py")
    sys.exit(1)

question_kb = json.dumps({"inline_keyboard": [
    [{"text": "Билет", "callback_data": "p1"}, {"text": "Ошибка", "callback_data": "p2"}],
    [{"text": "Йогурт", "callback_data": "p3"}, {"text": "Отец", "callback_data": "p4"}],
]}, ensure_ascii=False)

caption_q = ("<b>ПРОВЕРКА 1/4</b>\n\nВопрос 1 из 25\n\n"
             "🇩🇪 <b>die Fahrkarte</b>\n\nВыбери перевод:")

# sendVoice — голосовой баббл. Может быть запрещён настройкой приватности
# получателя (VOICE_MESSAGES_FORBIDDEN), это не ошибка бота.
rv = upload("sendVoice", "voice", path, chat_id=CHAT, parse_mode="HTML",
            reply_markup=question_kb, caption=caption_q)
voice_allowed = verdict("sendVoice (голосовой баббл)", rv.get("ok"),
                        rv.get("description", "") or "прошло")

if rv.get("ok"):
    msg, kind = rv["result"], "voice"
else:
    print("      → фолбэк на sendAudio, как это сделает бот")
    ra = upload("sendAudio", "audio", path, chat_id=CHAT, parse_mode="HTML",
                reply_markup=question_kb, caption=caption_q,
                title="die Fahrkarte", performer="GenauLingua")
    if not verdict("sendAudio + подпись + кнопки одним сообщением",
                   ra.get("ok"), ra.get("description", "")):
        sys.exit(1)
    msg, kind = ra["result"], "audio"

mid = msg["message_id"]
media = msg.get(kind, {})
file_id = media.get("file_id")
verdict(f"Telegram принял mp3 как {kind}", bool(file_id),
        f"duration={media.get('duration')}s, размер={media.get('file_size')} Б")

# Разбор ответа: та же карточка, новая подпись, новые кнопки
answer_kb = json.dumps({"inline_keyboard": [
    [{"text": "▶️ Следующее слово", "callback_data": "next"}],
    [{"text": "⚠️ Ошибка в переводе", "callback_data": "rep"}],
]}, ensure_ascii=False)

r2 = call("editMessageCaption", chat_id=CHAT, message_id=mid, parse_mode="HTML",
          reply_markup=answer_kb,
          caption=("<b>ПРОВЕРКА 2/4</b>\n\n✅ <b>Правильно!</b>\n\n"
                   "🇩🇪 <b>die Fahrkarte</b> = 🏴 <b>Билет</b>\n\n"
                   "🇩🇪 Ich kaufe eine Fahrkarte"))
verdict("подпись и кнопки редактируются на том же сообщении",
        r2.get("ok"), r2.get("description", ""))

# Подмена самого звука: в вопросе звучит слово, на разборе — слово с примером
full = pathlib.Path("tts_samples/demo_word_example.mp3")
if full.exists():
    spec = json.dumps({
        "type": kind, "media": "attach://f", "parse_mode": "HTML",
        "caption": ("<b>ПРОВЕРКА 3/4</b> — звук подменён на «слово + пример» "
                    "на том же сообщении"),
    }, ensure_ascii=False)
    r3 = upload("editMessageMedia", "f", full, chat_id=CHAT,
                message_id=str(mid), media=spec, reply_markup=answer_kb)
    verdict("сам звук подменяется на том же сообщении",
            r3.get("ok"), r3.get("description", ""))

# Переиспользование file_id: звук грузится в Telegram один раз навсегда
send_by_id = "sendVoice" if kind == "voice" else "sendAudio"
r4 = call(send_by_id, chat_id=CHAT, parse_mode="HTML", **{kind: file_id},
          caption="<b>ПРОВЕРКА 4/4</b> — отправлено по file_id, файл не загружался")
verdict("file_id переиспользуется (загрузка один раз навсегда)",
        r4.get("ok"), r4.get("description", ""))

print()
if not voice_allowed:
    print("Вывод: у тебя в Telegram запрещены голосовые сообщения.")
    print("Для бота это значит: пробуем sendVoice, при отказе — sendAudio.")
