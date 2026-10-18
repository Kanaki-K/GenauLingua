#!/usr/bin/env sh
# ОТЧЁТ О ПРОДУКТЕ — ТОЛЬКО ЧТЕНИЕ. Ничего не меняет, ничего не отправляет.
#
#     sh deploy/product_report.sh                       # последние 7 дней
#     sh deploy/product_report.sh "2026-10-14 20:12"    # с выхода 2.0
#
# Печатает здоровье бота (память, перезапуски, ошибки журнала) и разделы
# `deploy/product_report.sql`: люди и занятия, игры, где уходят, журнал пути,
# сообщения против контрольной группы, путь новичка, события 2.2.1. Люди —
# первыми шестью знаками хеша, владелец (`ADMIN_USER`) исключён. Вывод с
# хешами и ответами людей в git не кладётся.
set -u
cd "$(dirname "$0")/.."
SINCE="${1:-$(date -u -d '7 days ago' '+%Y-%m-%d %H:%M')}"
ADMIN=$(sed -n 's/^ADMIN_USER=//p' .env | tr -dc '0-9')
echo "## отчёт с $SINCE UTC, сейчас $(date -u '+%Y-%m-%d %H:%M') UTC"
echo "## H0 сервер"; free -m | sed -n 2p; df -h / | tail -1
docker inspect genaulingua_app -f 'бот: запущен {{.State.StartedAt}}, перезапусков {{.RestartCount}}, OOM {{.State.OOMKilled}}'
echo "## H1 журнал бота: ERROR / WARNING по видам (цифры вырезаны)"
docker compose logs --since "$(echo "$SINCE" | tr ' ' 'T')" app 2>&1 | grep -E '\| (ERROR|WARNING|CRITICAL) \|' \
  | sed -E 's/^[^|]*\| [0-9-]+ [0-9:,]+ \| //; s/[0-9]{3,}/N/g; s/"[^"]*"/"…"/g' | cut -c1-140 | sort | uniq -c | sort -rn | head -20
echo "## SQL"
docker compose exec -T postgres sh -c "psql -X -q -v ON_ERROR_STOP=1 -v admin=${ADMIN:-0} -v since=\"'$SINCE'\" -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\"" \
  < deploy/product_report.sql
