# -*- coding: utf-8 -*-
"""
Окончательная проверка озвучки: все языки, по обрезанным клипам.

Запускается после обрезки, а не до: проверять надо то, что поедет людям.
Каждый язык в свой файл, прогон возобновляемый.
"""
import subprocess
import sys
import time

LANGS = ("de", "en", "uk", "ru", "tr", "pl")

for lang in LANGS:
    print(f"\n{'=' * 60}\n{lang}\n{'=' * 60}", flush=True)
    started = time.monotonic()
    subprocess.run(
        [sys.executable, "-u", "-m", "app.scripts.tts_asr_check",
         "--lang", lang, "--all", "--workers", "8",
         "--out", f"asr_final_{lang}.jsonl"],
        check=False,
    )
    print(f"{lang}: {(time.monotonic() - started) / 60:.1f} мин", flush=True)

print("\nпрогон по всем языкам завершён", flush=True)
