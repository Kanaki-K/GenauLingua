#!/usr/bin/env sh
# БЭКАП ПЕРЕД ВЫКАТКОЙ. Без него дальше не идти.
#
#     sh deploy/backup.sh
#
# Дамп остаётся НА СЕРВЕРЕ, в ~/genaulingua-backups: не скачивается и не
# копируется никуда (правило владельца — без копий прод-данных вне его
# ведома). Проверяется, что архив цел, не пуст и в нём есть данные людей.
set -eu
dir="$HOME/genaulingua-backups"; mkdir -p "$dir"; chmod 700 "$dir"
file="$dir/before-release-$(date +%F-%H%M).sql.gz"

docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > "$file"
chmod 600 "$file"

gzip -t "$file" || { echo "[СБОЙ] архив повреждён"; exit 1; }
size=$(du -k "$file" | cut -f1)
[ "$size" -gt 100 ] || { echo "[СБОЙ] архив подозрительно мал: ${size} КБ"; exit 1; }
for t in users user_words quiz_sessions quiz_questions monthly_stats words; do
  gunzip -c "$file" | grep -q "^COPY public.$t " || { echo "[СБОЙ] в дампе нет таблицы $t"; exit 1; }
done
echo "[ок  ] бэкап: $file (${size} КБ), архив цел, все таблицы на месте"
echo "восстановление при откате: см. DEPLOY.md, «Откат»"
