"""
Сторож для пакетов B1 и B2: забрать их, как только закончатся.

Зачем. Процесс, который их создал и ждал, завершился, и никто пакеты не
опрашивает. Пакет живёт 24 часа, после чего результаты истекают — а они
оплачены. Один раз я уже объявил такой пакет зависшим и отменил, потеряв
50 готовых ответов и $1.20.

Опрос раз в пять минут. Как только пакет в состоянии ended — результаты
забираются в файл и сторож о нём забывает. Работа заканчивается, когда оба
пакета забраны или когда истекло время ожидания.
"""

import os
import pathlib
import re
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

import anthropic

POLL_SECONDS = 300
# Пакет живёт 24 часа; ждём с запасом на случай, если он завершится к самому
# концу срока
MAX_HOURS = 20

env = pathlib.Path(".env.local").read_text(encoding="utf-8")
key = re.search(r"ANTHROPIC_API_KEY\s*=\s*(\S+)", env).group(1).strip().strip("\"'")
client = anthropic.Anthropic(api_key=key)

# Читаем id из файлов состояния, а не из кода: так сторож не разойдётся с тем,
# что на самом деле отправлено
targets: dict[str, str] = {}
for state in sorted(list(pathlib.Path(".").glob("wordbase_*.batch")) + list(pathlib.Path(".").glob("final_*.batch"))):
    batch_id = state.read_text(encoding="utf-8").strip()
    if batch_id:
        targets[state.stem] = batch_id

if not targets:
    print("файлов состояния не найдено — нечего ждать", flush=True)
    sys.exit(0)

print(f"жду пакетов: {targets}", flush=True)
deadline = time.monotonic() + MAX_HOURS * 3600
collected: list[str] = []

while targets and time.monotonic() < deadline:
    for name, batch_id in list(targets.items()):
        try:
            batch = client.messages.batches.retrieve(batch_id)
        except Exception as exc:
            print(f"{name}: опрос не удался — {type(exc).__name__}: {exc}", flush=True)
            continue

        counts = batch.request_counts
        total = (counts.processing + counts.succeeded + counts.errored
                 + counts.canceled + counts.expired)
        print(f"{name} {batch.processing_status}: готово {counts.succeeded}/{total}, "
              f"в работе {counts.processing}, ошибок {counts.errored}", flush=True)

        if batch.processing_status != "ended":
            continue

        out = f"{name}_recovered.jsonl"
        print(f"{name}: завершён, забираю в {out}", flush=True)
        result = subprocess.run(
            [sys.executable, "-u", "-m", "app.scripts.collect_batch",
             batch_id, "--kind", "words", "--out", out],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        print(result.stdout[-2000:], flush=True)
        if result.returncode != 0:
            print(f"{name}: забрать не удалось\n{result.stderr[-1500:]}", flush=True)
        else:
            collected.append(out)
        del targets[name]

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
