# -*- coding: utf-8 -*-
"""
Залить копию прод-данных в локальную dev-базу.

Зачем: админка «не работает» проявляется только на настоящих данных —
на пустой базе все 16 инструментов отвечают, просто нечем.

Побочная польза: миграция мультиязычности прогоняется на живых 232 юзерах,
2295 сессиях и 28 082 ответах, а не на четырёх засеянных строках.

Порядок: схема до миграции → импорт CSV → миграции до head → группы.
"""
import csv
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("ENV_FILE", ".env.local")

CSV_DIR = Path("C:/Users/lodk9/GenauLingua_analytics_2026-09-29/csv")
PRE_MULTILANG = "f61639c52096"

# Порядок важен из-за внешних ключей
TABLES = [
    "users",
    "words",
    "quiz_sessions",
    "quiz_questions",
    "user_words",
    "monthly_seasons",
    "monthly_stats",
    "monthly_awards",
    "win_streaks",
    "translation_reports",
]

DSN = "host=localhost port=5434 dbname=genaulingua_dev user=dev_user password=dev_pass"


def _conn():
    import psycopg2

    return psycopg2.connect(DSN)


def sql_scalar_table(query: str) -> str:
    with _conn() as conn, conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        head = [d[0] for d in cur.description]
    width = [max(len(str(head[i])), *(len(str(r[i])) for r in rows)) if rows else len(head[i])
             for i in range(len(head))]
    out = ["  ".join(str(h).ljust(width[i]) for i, h in enumerate(head))]
    out.append("  ".join("-" * w for w in width))
    for r in rows:
        out.append("  ".join(str(v).ljust(width[i]) for i, v in enumerate(r)))
    return "\n".join(out)


def reset_schema() -> None:
    with _conn() as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public; "
                        "GRANT ALL ON SCHEMA public TO dev_user")


def alembic(target: str) -> None:
    env = {**os.environ, "ENV_FILE": ".env.local", "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", target],
        cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"alembic {target}:\n{result.stdout[-2000:]}\n{result.stderr[-2000:]}"
        )
    print(f"  миграции до {target}: ок")


def table_columns(conn, table: str) -> set[str]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s",
            (table,),
        )
        return {r[0] for r in cur.fetchall()}


def import_table(conn, table: str) -> int:
    import io

    path = CSV_DIR / f"{table}.csv"
    if not path.exists():
        print(f"  {table:22} файла нет — пропуск")
        return 0

    available = table_columns(conn, table)

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        cols = [h for h in header if h in available]
        skipped = [h for h in header if h not in available]

        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="\n")
        count = 0
        for row in reader:
            writer.writerow([row.get(c, "") for c in cols])
            count += 1

    if count == 0:
        print(f"  {table:22} пусто")
        return 0

    buf.seek(0)
    col_list = ", ".join(f'"{c}"' for c in cols)
    with conn.cursor() as cur:
        cur.copy_expert(
            f"COPY {table} ({col_list}) FROM STDIN WITH (FORMAT csv, NULL '')", buf
        )
    conn.commit()

    note = f" (нет в этой ревизии: {', '.join(skipped)})" if skipped else ""
    print(f"  {table:22} {count:6} строк{note}")
    return count


def main() -> None:
    if not CSV_DIR.exists():
        print(f"нет выгрузки: {CSV_DIR}")
        sys.exit(1)

    print("1. сбрасываю схему dev-базы")
    reset_schema()

    print(f"2. схема до миграции мультиязычности ({PRE_MULTILANG})")
    alembic(PRE_MULTILANG)

    print("3. импорт прод-данных")
    total = 0
    with _conn() as conn:
        for table in TABLES:
            total += import_table(conn, table)
    print(f"  всего строк: {total}")

    print("4. прогоняю миграции на этих данных")
    alembic("head")

    print("5. пересборка групп слов")
    env = {**os.environ, "ENV_FILE": ".env.local", "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, "-m", "app.scripts.rebuild_word_groups"],
        cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8",
    )
    print(result.stdout[-700:] if result.returncode == 0 else result.stderr[-1500:])

    print("\n6. что получилось")
    counts = sql_scalar_table(
        "SELECT 'users' t, count(*) FROM users "
        "UNION ALL SELECT 'words', count(*) FROM words "
        "UNION ALL SELECT 'quiz_sessions', count(*) FROM quiz_sessions "
        "UNION ALL SELECT 'quiz_questions', count(*) FROM quiz_questions "
        "UNION ALL SELECT 'user_words', count(*) FROM user_words "
        "UNION ALL SELECT 'translation_reports', count(*) FROM translation_reports "
        "UNION ALL SELECT 'word_lang_groups', count(*) FROM word_lang_groups"
    )
    print(counts)

    print("проверка бэкфилла языковой пары:")
    print(sql_scalar_table(
        "SELECT learning_lang, native_lang, reverse_mode, count(*) "
        "FROM users GROUP BY 1,2,3 ORDER BY 4 DESC"
    ))
    print("точность: план против факта")
    print(sql_scalar_table(
        "SELECT sum(total_questions) AS planned, sum(answered_questions) AS answered, "
        "sum(correct_answers) AS correct, "
        "round(100.0*sum(correct_answers)/nullif(sum(total_questions),0),1) AS pct_by_planned, "
        "round(100.0*sum(correct_answers)/nullif(sum(answered_questions),0),1) AS pct_by_answered "
        "FROM quiz_sessions WHERE completed_at IS NOT NULL"
    ))


if __name__ == "__main__":
    main()
