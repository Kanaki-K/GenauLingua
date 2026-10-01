"""
Сторож пакетов переводов — единственный на машине.

Зачем именно он. К утру 01.10 за одними и теми же пакетами следили пятеро:
три процесса `propose --batch`, что их создали, и ещё один сторож. Это уже
дало дубль при сборе final_3 (две побайтово одинаковые копии) и грозило тем,
что к шагу apply одни и те же предложения приедут дважды. Владелец
распорядился оставить одного.

Что он делает:

* забирает в `final_N.jsonl` — имена, которые ждёт finish_translation_round,
  а не в `_recovered`-дубли;
* пропускает пакеты, что уже забраны, вместо повторного скачивания;
* ведёт разведчика (пакет из одного запроса) как датчик очереди: только
  смотрит, не забирает — по нему видно, движется ли пакетная обработка вообще;
* после сбора проверяет себя: файл непуст и строки разбираются как JSON.
  Правило дома — смотреть на вывод, а не на число.

Срок ожидания берётся из срока жизни самих пакетов, а не задаётся числом
часов от запуска. Предшественник ждал фиксированные 16 часов, и если его
перезапустить ближе к концу, он успел бы выйти раньше, чем пакеты истекут —
то есть именно тогда, когда он нужен. Пакет живёт 24 часа от создания; ждём
до последнего срока плюс запас на завершение впритык.

Запуск (в фоне, с перенаправлением вывода в файл):

    ENV_FILE=.env.local PYTHONIOENCODING=utf-8 \
        .venv/Scripts/python.exe -u -m app.scripts.watch_batches
"""

import json
import os
import pathlib
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("ENV_FILE", ".env.local")

import anthropic

POLL_SECONDS = 120

# Пакет живёт сутки от создания. Запас — на случай, если он завершится в
# последние минуты срока и результаты надо будет успеть скачать.
BATCH_LIFETIME = timedelta(hours=24)
GRACE = timedelta(minutes=30)

# Разведчик: один запрос на 16 токенов. Квоту занять не может, поэтому его
# задержка — чистый показатель общего затора, а не нашего разбиения на части.
CANARY = "msgbatch_012ELTec4YdwFTsuwjfTcKhw"

env = (ROOT / ".env.local").read_text(encoding="utf-8")
key = re.search(r"ANTHROPIC_API_KEY\s*=\s*(\S+)", env).group(1).strip().strip("\"'")
client = anthropic.Anthropic(api_key=key)


def already_collected(name: str) -> bool:
    """
    Забран ли пакет — по файлу результатов НОВЕЕ файла состояния.

    Проверять просто наличие непустого файла нельзя. Имена результатов
    повторяются от прогона к прогону: `example_fixes.jsonl` остаётся на диске
    с прошлого раза, и сторож счёл бы свежий пакет уже забранным, а он бы
    тихо истёк вместе с оплатой. Файл состояния пишется в момент отправки,
    поэтому «результат старше состояния» в точности значит «ещё не забран».
    """
    out = ROOT / f"{name}.jsonl"
    state = ROOT / f"{name}.batch"
    if not out.exists() or out.stat().st_size == 0:
        return False
    if not state.exists():
        return True
    return out.stat().st_mtime >= state.stat().st_mtime


def _is_json(line: str) -> bool:
    try:
        json.loads(line)
        return True
    except ValueError:
        return False


def kind_of(name: str) -> str:
    """
    Чем разбирать результат — зависит от того, кто пакет отправил.

    Раньше сторож забирал всё как «words», потому что других пакетов не было.
    Теперь их два вида, и разобрать правки примеров разборщиком переводов
    нельзя: он молча не найдёт ожидаемых полей. Вид определяется по имени
    файла состояния, то есть по тому же источнику, из которого берётся id.
    """
    return "words" if name.startswith("final_") else "examples"


def collect(name: str, batch_id: str, expected: int) -> bool:
    out = f"{name}.jsonl"
    print(f"{name}: завершён, забираю в {out}", flush=True)
    result = subprocess.run(
        [sys.executable, "-u", "-m", "app.scripts.collect_batch",
         batch_id, "--kind", kind_of(name), "--out", out],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(ROOT),
    )
    print(result.stdout[-2000:], flush=True)
    if result.returncode != 0:
        print(f"{name}: ЗАБРАТЬ НЕ УДАЛОСЬ\n{result.stderr[-1500:]}", flush=True)
        return False

    # Самопроверка: сбор, который молча отдал пустоту, опаснее несобранного
    path = ROOT / out
    if not path.exists() or path.stat().st_size == 0:
        print(f"{name}: ТРЕВОГА — collect_batch отчитался успехом, а файл пуст",
              flush=True)
        return False
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    broken = sum(1 for ln in lines if not _is_json(ln))
    print(f"{name}: строк {len(lines)}, неразобранных {broken}, "
          f"успешных запросов по API {expected}", flush=True)
    if broken:
        print(f"{name}: ТРЕВОГА — {broken} строк не разобрались как JSON", flush=True)
    return True


targets: dict[str, str] = {}
# Берём все файлы состояния, а не только final_*: правки примеров и лемм
# отправляются своими пакетами и истекают так же через сутки
for state in sorted(ROOT.glob("*.batch")):
    batch_id = state.read_text(encoding="utf-8").strip()
    if not batch_id:
        continue
    if already_collected(state.stem):
        print(f"{state.stem}: уже забран, пропускаю", flush=True)
        continue
    targets[state.stem] = batch_id

if not targets:
    print("забирать нечего — все пакеты уже на диске", flush=True)
    sys.exit(0)

print(f"жду пакетов: {targets}", flush=True)

# Крайний срок — по самому долгоживущему из пакетов, а не по часам от запуска
deadline = datetime.now(timezone.utc) + BATCH_LIFETIME
for name, batch_id in targets.items():
    try:
        created = client.messages.batches.retrieve(batch_id).created_at
    except Exception as exc:
        print(f"{name}: срок жизни узнать не удалось ({type(exc).__name__}), "
              f"считаю сутки от сейчас", flush=True)
        continue
    print(f"{name}: создан {created:%Y-%m-%d %H:%M} UTC, истекает "
          f"{created + BATCH_LIFETIME:%Y-%m-%d %H:%M} UTC", flush=True)
    deadline = max(deadline, created + BATCH_LIFETIME + GRACE)

print(f"жду до {deadline:%Y-%m-%d %H:%M} UTC", flush=True)

collected: list[str] = []

while targets and datetime.now(timezone.utc) < deadline:
    for name, batch_id in list(targets.items()):
        try:
            batch = client.messages.batches.retrieve(batch_id)
        except Exception as exc:
            print(f"{name}: опрос не удался — {type(exc).__name__}: {exc}", flush=True)
            continue

        c = batch.request_counts
        total = c.processing + c.succeeded + c.errored + c.canceled + c.expired
        print(f"{name} {batch.processing_status}: готово {c.succeeded}/{total}, "
              f"в работе {c.processing}, ошибок {c.errored}", flush=True)

        if batch.processing_status != "ended":
            continue

        if collect(name, batch_id, c.succeeded):
            collected.append(f"{name}.jsonl")
        del targets[name]

    # Датчик очереди: если разведчик сдвинулся, значит обработка идёт
    try:
        probe = client.messages.batches.retrieve(CANARY)
        pc = probe.request_counts
        print(f"разведчик {probe.processing_status}: готово {pc.succeeded}/1", flush=True)
    except Exception as exc:
        print(f"разведчик: опрос не удался — {type(exc).__name__}", flush=True)

    if targets:
        time.sleep(POLL_SECONDS)

print(flush=True)
if collected:
    print(f"забрано: {collected}", flush=True)
if targets:
    print(f"НЕ ДОЖДАЛСЯ: {targets} — проверить вручную через collect_batch --list",
          flush=True)
else:
    print("все пакеты забраны", flush=True)
