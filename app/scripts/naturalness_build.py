"""Собрать блок: «стало» и «зачем» — в модуле блока, «было» — из базы.

    python -m app.scripts.naturalness_build app/data/naturalness/src/a1_01.py app/data/naturalness/batch_02.json "описание"
"""
import importlib.util
import json
import os
import pathlib
import sys

sys.path.insert(0, os.getcwd())
os.environ.setdefault("ENV_FILE", ".env.local")
from sqlalchemy import create_engine, text  # noqa: E402

from app.config import settings  # noqa: E402

LANGS = ["de", "ru", "uk", "en", "tr", "pl", "it", "es", "fr", "cs"]
COL = {f"t_{l}": f"translation_{l}" for l in LANGS if l != "de"}
COL.update({f"x_{l}": f"example_{l}" for l in LANGS})

spec = importlib.util.spec_from_file_location("fx", sys.argv[1])
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)

engine = create_engine(settings.DATABASE_URL_SYNC)
edits = []
with engine.connect() as c:
    for wid, (why, cols) in fx.FIXES.items():
        for key, new in cols.items():
            col = COL.get(key, key)
            old = c.execute(text(f"select {col}::text from words where id=:id"), {"id": wid}).scalar()
            if old == new:
                continue
            edits.append({"id": wid, "col": col, "old": old or "", "new": new, "why": why})
    # Пример поменялся на немецком — обязаны поменяться все языки
    for wid, (why, cols) in fx.FIXES.items():
        keys = {COL.get(k, k) for k in cols}
        if "example_de" in keys:
            missing = [f"example_{l}" for l in LANGS if f"example_{l}" not in keys]
            assert not missing, (wid, "немецкий пример сменён, а эти — нет:", missing)
out = pathlib.Path(sys.argv[2])
out.write_text(json.dumps({"about": sys.argv[3], "edits": edits,
                           "replace": getattr(fx, "REPLACE", []),
                           "unreplace": getattr(fx, "UNREPLACE", []),
                           "split_later": getattr(fx, "SPLIT_LATER", {})},
                          ensure_ascii=False, indent=1), encoding="utf-8")
print(len(edits), "правок")
