#!/usr/bin/env sh
# ПРОВЕРКА СЕРВЕРА ПЕРЕД ВЫКАТКОЙ. Только чтение: ничего не меняет.
#
#     cd /path/to/GenauLingua && sh deploy/preflight.sh
#
# Печатает, хватит ли ресурсов, на какой ревизии схема, что в .env (имена,
# не значения — кроме ENV), и слепок данных людей, с которым потом
# сверяется выкатка (`release_snapshot --compare`). Пороги — по замеру
# 14.10.2026: бот 215 МБ + распознаватель речи 375 МБ + база; образ 2.48 ГБ.

set -u
fail=0
say()  { printf '%s\n' "$*"; }
warn() { printf '[СБОЙ] %s\n' "$*"; fail=1; }
ok()   { printf '[ок  ] %s\n' "$*"; }

say "== машина"
uname -srm; say "ядер: $(nproc)"

mem_mb=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
swap_mb=$(awk '/SwapFree/ {print int($2/1024)}' /proc/meminfo)
say "память доступно: ${mem_mb} МБ, своп свободно: ${swap_mb} МБ"
# Нужно ~1 ГБ сверх нынешнего: распознаватель речи живёт в памяти бота
[ $((mem_mb + swap_mb)) -ge 1200 ] && ok "памяти хватит (нужно ~1.2 ГБ свободно с запасом)" \
  || warn "памяти мало: распознаватель речи (+375 МБ) может уронить бота — добавить своп"

disk_mb=$(df -Pm . | awk 'NR==2 {print $4}')
say "диск свободно: ${disk_mb} МБ"
[ "$disk_mb" -ge 6000 ] && ok "диска хватит (образ 2.5 ГБ + сборка + бэкап)" \
  || warn "диска меньше 6 ГБ: сборка образа может не влезть — docker system prune"

say; say "== docker"
docker --version; docker compose version
docker compose ps
docker system df

say; say "== код"
git rev-parse --abbrev-ref HEAD; git log -1 --format='%h %ad %s' --date=short
git status --short | head -20

say; say "== .env (имена; значение только у ENV)"
if [ -f .env ]; then
  sed -n 's/^\([A-Z_]*\)=.*/\1/p' .env | tr '\n' ' '; say
  env_value=$(sed -n 's/^ENV=//p' .env)
  [ "$env_value" = "prod" ] && ok "ENV=prod" \
    || warn "ENV=${env_value:-не задан}: поставить ENV=prod (иначе SQL-эхо старым кодом)"
else
  warn ".env не найден"
fi

say; say "== схема базы"
docker compose exec -T app alembic current 2>/dev/null || warn "alembic current не ответил"
say "(ожидается f61639c52096 — прод до выкатки)"

say; say "== слепок данных (с ним сверяется выкатка)"
docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -At -F " " -c "
select '"'"'users'"'"', count(*)::text from users
union all select '"'"'users_ids_md5'"'"', md5(string_agg(id::text, '"'"','"'"' order by id))::text from users
union all select '"'"'user_words_rows'"'"', count(*)::text from user_words
union all select '"'"'uw_shown'"'"', coalesce(sum(times_shown),0)::text from user_words
union all select '"'"'uw_correct'"'"', coalesce(sum(times_correct),0)::text from user_words
union all select '"'"'uw_learned'"'"', count(*)::text from user_words where learned
union all select '"'"'quiz_sessions'"'"', count(*)::text from quiz_sessions
union all select '"'"'quiz_questions'"'"', count(*)::text from quiz_questions
union all select '"'"'monthly_awards'"'"', count(*)::text from monthly_awards
union all select '"'"'words'"'"', count(*)::text from words
union all select '"'"'reminders_on'"'"', count(*)::text from users where notifications_enabled"' \
  2>/dev/null || warn "база не ответила"
docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -At -c "select pg_size_pretty(pg_database_size(current_database()))"' 2>/dev/null | sed 's/^/размер базы: /'

say
[ $fail -eq 0 ] && say "ГОТОВ К ВЫКАТКЕ" || say "ЕСТЬ СБОИ — см. [СБОЙ] выше"
exit $fail
