-- ОТЧЁТ О ПРОДУКТЕ — ТОЛЬКО ЧТЕНИЕ, сводные числа, люди — хешем. Запуск: deploy/product_report.sh.
-- Переменные psql: :admin (владелец, исключается), :since (начало периода, в кавычках SQL).
-- Разделы: A люди и занятия · B игры · C уходы · D журнал · E сообщения · F жалобы · G прогресс ·
-- P глубже (перезапуски, путь новичка, «Говорю», «Собираю», часы, контрольная группа) ·
-- N события 2.2.1 (двери, «Продолжить», «убрать Говорю?», блокировки, ошибки, меню).
-- Собран из разбора 18.10.2026 (IMPROVEMENT_PLAN.md). Новый SQL — сначала на dev-базе.
\pset footer off
\pset format unaligned
\pset fieldsep ' | '
BEGIN READ ONLY;

\echo ## A1 люди
select count(*) total,
  count(*) filter (where created_at >= :since) new_since_20,
  count(*) filter (where created_at < :since) old,
  count(*) filter (where notifications_enabled) notif_on,
  count(*) filter (where reminders_declined_at is not null) declined
from users where id <> :admin;

\echo ## A2 новые по дням | день | новых | из них начали занятие | закончили хоть одно
select u.created_at::date d, count(*),
  count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=u.id)),
  count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=u.id and s.is_completed))
from users u where u.id<>:admin and u.created_at >= :since group by 1 order by 1;

\echo ## A3 занятия по дням (UTC) | день | начато | закончено | людей | людей закончивших | вопросов
select s.started_at::date d, count(*), count(*) filter (where is_completed),
  count(distinct user_id), count(distinct user_id) filter (where is_completed),
  sum(answered_questions)
from quiz_sessions s where s.user_id<>:admin and s.started_at >= :since group by 1 order by 1;

\echo ## A4 активные | 1 дн | 3 дн | 7 дн | с 2.0 всего
select count(distinct user_id) filter (where started_at > now() - interval '1 day'),
  count(distinct user_id) filter (where started_at > now() - interval '3 day'),
  count(distinct user_id) filter (where started_at > now() - interval '7 day'),
  count(distinct user_id)
from quiz_sessions where user_id<>:admin and started_at >= :since and is_completed;

\echo ## A5 возврат: дней с законченным занятием у человека (с 2.0) | дней | людей | из них новых
with d as (select user_id, count(distinct coalesce(local_day, completed_at::date)) n from quiz_sessions
  where user_id<>:admin and is_completed and started_at >= :since group by 1)
select least(n,7) days, count(*), count(*) filter (where u.created_at >= :since)
from d join users u on u.id=d.user_id group by 1 order by 1;

\echo ## A6 новички: вернулись ли на 2-й день и позже | всего новых с занятием | 2+ разных дня | день2 подряд
with f as (select s.user_id, min(coalesce(local_day, completed_at::date)) d1 from quiz_sessions s join users u on u.id=s.user_id
  where s.user_id<>:admin and s.is_completed and u.created_at >= :since group by 1)
select count(*),
  count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=f.user_id and s.is_completed and coalesce(local_day, completed_at::date) > f.d1)),
  count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=f.user_id and s.is_completed and coalesce(local_day, completed_at::date) = f.d1 + 1))
from f;

\echo ## A7 старые пользователи (до 2.0): вернулись после 2.0 | было | начали занятие после 2.0 | закончили
select count(*),
  count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=u.id and s.started_at >= :since)),
  count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=u.id and s.started_at >= :since and s.is_completed))
from users u where u.id<>:admin and u.created_at < :since;

\echo ## A8 языки: учат | пар | людей с занятием после 2.0
select coalesce(s.learning_lang,'?')||' <- '||coalesce(s.native_lang,'?') pair, count(distinct s.user_id)
from quiz_sessions s where s.user_id<>:admin and s.started_at >= :since group by 1 order by 2 desc limit 25;

\echo ## B1 игры | канал | ответов | верно % | медиана сек | p90 сек | без ответа (пусто)
select coalesce(q.channel,'?'), count(*),
  round(100.0*avg(case when q.is_correct then 1 else 0 end),1),
  percentile_cont(0.5) within group (order by q.response_time_seconds),
  percentile_cont(0.9) within group (order by q.response_time_seconds),
  count(*) filter (where q.user_answer is null or q.user_answer='')
from quiz_questions q join quiz_sessions s on s.id=q.session_id
where s.user_id<>:admin and s.started_at >= :since and q.answered_at is not null group by 1 order by 2 desc;

\echo ## B2 игры по уровню | уровень | канал | ответов | верно %
select s.level::text, coalesce(q.channel,'?'), count(*), round(100.0*avg(case when q.is_correct then 1 else 0 end),1)
from quiz_questions q join quiz_sessions s on s.id=q.session_id
where s.user_id<>:admin and s.started_at >= :since and q.answered_at is not null group by 1,2 having count(*)>=20 order by 1,2;

\echo ## B3 игры по изучаемому языку | язык | канал | ответов | верно %
select s.learning_lang, coalesce(q.channel,'?'), count(*), round(100.0*avg(case when q.is_correct then 1 else 0 end),1)
from quiz_questions q join quiz_sessions s on s.id=q.session_id
where s.user_id<>:admin and s.started_at >= :since and q.answered_at is not null group by 1,2 having count(*)>=30 order by 1,2;

\echo ## B4 частые ответы-пустышки/пропуски | канал | ответ | раз
select coalesce(q.channel,'?'), left(coalesce(q.user_answer,'<null>'),30), count(*)
from quiz_questions q join quiz_sessions s on s.id=q.session_id
where s.user_id<>:admin and s.started_at >= :since and not coalesce(q.is_correct,false)
group by 1,2 order by 3 desc limit 15;

\echo ## C1 брошенные занятия | первое занятие человека? | начато | брошено | брошено %
with s as (select s.*, row_number() over (partition by user_id order by started_at) rn from quiz_sessions s where user_id<>:admin)
select case when rn=1 then 'первое' when rn<=3 then '2-3' else '4+' end grp, count(*),
  count(*) filter (where not is_completed), round(100.0*count(*) filter (where not is_completed)/count(*),1)
from s where started_at >= :since group by 1 order by 1;

\echo ## C2 на каком вопросе бросают | ответов до ухода | занятий
select least(coalesce(answered_questions,0),16) a, count(*) from quiz_sessions
where user_id<>:admin and started_at >= :since and not is_completed group by 1 order by 1;

\echo ## C3 последняя показанная игра перед уходом | канал | бросили после неё | последний ответ был ошибкой
with last as (select distinct on (q.session_id) q.session_id, q.channel, q.is_correct
  from quiz_questions q join quiz_sessions s on s.id=q.session_id
  where s.user_id<>:admin and s.started_at >= :since and not s.is_completed and q.answered_at is not null
  order by q.session_id, q.answered_at desc)
select coalesce(channel,'?'), count(*), count(*) filter (where not coalesce(is_correct,false)) from last group by 1 order by 2 desc;

\echo ## C4 следующий, не отвеченный вопрос (на чём ушли) | канал | раз
with nxt as (select distinct on (q.session_id) q.session_id, q.channel
  from quiz_questions q join quiz_sessions s on s.id=q.session_id
  where s.user_id<>:admin and s.started_at >= :since and not s.is_completed and q.answered_at is null
  order by q.session_id, q.id)
select coalesce(channel,'?'), count(*) from nxt group by 1 order by 2 desc;

\echo ## C5 ошибки подряд перед уходом (последние 3 ответа) | неверных из 3 | занятий
with r as (select q.session_id, q.is_correct, row_number() over (partition by q.session_id order by q.answered_at desc) k
  from quiz_questions q join quiz_sessions s on s.id=q.session_id
  where s.user_id<>:admin and s.started_at >= :since and not s.is_completed and q.answered_at is not null)
select wrong, count(*) from (select session_id, count(*) filter (where not coalesce(is_correct,false)) wrong from r where k<=3 group by 1) x group by 1 order by 1;

\echo ## C6 источники запуска занятия | источник | начато | закончено %
select coalesce(start_source,'?'), count(*), round(100.0*avg(case when is_completed then 1 else 0 end),1)
from quiz_sessions where user_id<>:admin and started_at >= :since group by 1 order by 2 desc;

\echo ## C7 причины выхода | причина | занятий
select coalesce(exit_reason,'<нет>'), count(*) from quiz_sessions where user_id<>:admin and started_at >= :since group by 1 order by 2 desc;

\echo ## C8 точность первого занятия → вернулся ли (новые с 2.0) | точность первого | людей | вернулись в другой день
with f as (select distinct on (s.user_id) s.user_id, s.correct_answers, s.answered_questions, coalesce(s.local_day, s.completed_at::date) d
  from quiz_sessions s join users u on u.id=s.user_id where s.user_id<>:admin and u.created_at >= :since and s.is_completed order by s.user_id, s.started_at)
select case when answered_questions=0 then '?' when 1.0*correct_answers/answered_questions >= .9 then '90-100' when 1.0*correct_answers/answered_questions >= .7 then '70-89' else '<70' end acc,
  count(*), count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=f.user_id and s.is_completed and coalesce(s.local_day,s.completed_at::date) > f.d))
from f group by 1 order by 1;

\echo ## D1 журнал: виды событий (с 16.10) | вид | действие | раз | людей | медиана мс | p95 мс
select kind, left(coalesce(action,''),40), count(*), count(distinct user_id),
  percentile_cont(0.5) within group (order by ms), percentile_cont(0.95) within group (order by ms)
from user_events where user_id<>:admin group by 1,2 order by 3 desc limit 40;

\echo ## D2 медленные ответы бота (ms > 3000) | действие | раз | макс мс
select left(coalesce(action,''),40), count(*), max(ms) from user_events where user_id<>:admin and ms > 3000 group by 1 order by 2 desc limit 15;

\echo ## D3 голос: попытки | данные (ключи) | раз
select kind, coalesce(channel,''), jsonb_object_keys(data) k, count(*) from user_events where user_id<>:admin and jsonb_typeof(data)='object' group by 1,2,3 order by 4 desc limit 30;

\echo ## D4 голос: исход попытки | действие | попытка | раз | ср. похожесть | людей
select left(coalesce(action,''),30), data->>'attempt', count(*), round(avg((data->>'similarity')::numeric),2), count(distinct user_id)
from user_events where user_id<>:admin and kind='speech' group by 1,2 order by 1,2;

\echo ## D5 пропуски | канал | попытка | раз | людей
select coalesce(channel,''), coalesce(data->>'attempt',''), count(*), count(distinct user_id) from user_events where user_id<>:admin and kind='skip' group by 1,2 order by 3 desc;

\echo ## D6 смена уровня | действие | с → на | раз
select action, (data->>'frm')||' → '||(data->>'to'), count(*) from user_events where user_id<>:admin and kind='level' group by 1,2 order by 3 desc limit 15;

\echo ## D7 знакомство | действие | раз | людей | язык телефона не совпал
select action, count(*), count(distinct user_id), count(*) filter (where (data->>'mismatch')::text in ('true','1')) from user_events where user_id<>:admin and kind in ('onboard','language') group by 1 order by 2 desc;

\echo ## D8 последнее действие человека в брошенном занятии (журнал) | вид | действие | раз
with ab as (select id from quiz_sessions where user_id<>:admin and not is_completed and started_at >= '2026-10-16'),
last as (select distinct on (e.session_id) e.session_id, e.kind, e.action from user_events e join ab on ab.id=e.session_id order by e.session_id, e.at desc)
select kind, left(coalesce(action,''),30), count(*) from last group by 1,2 order by 3 desc limit 15;

\echo ## D9 время до ухода: сколько минут шло брошенное занятие | минут | занятий
with ab as (select s.id, extract(epoch from (max(q.answered_at) - s.started_at))/60 m from quiz_sessions s join quiz_questions q on q.session_id=s.id
  where s.user_id<>:admin and not s.is_completed and s.started_at >= :since and q.answered_at is not null group by s.id, s.started_at)
select case when m<1 then '<1' when m<3 then '1-3' when m<10 then '3-10' else '10+' end, count(*) from ab group by 1 order by 1;

\echo ## E1 сообщения вовлечения | вид | исход | раз
select kind, coalesce(outcome,'<нет>'), count(*) from nudge_log where user_id<>:admin group by 1,2 order by 1,3 desc;

\echo ## E2 вернулись в течение 24 ч после сообщения | вид | отправлено | вернулись (занятие) %
select n.kind, count(*), round(100.0*avg(case when exists (select 1 from quiz_sessions s where s.user_id=n.user_id and s.started_at between n.sent_at and n.sent_at + interval '24 hour') then 1 else 0 end),1)
from nudge_log n where n.user_id<>:admin and n.sent_at is not null group by 1 order by 2 desc;

\echo ## F1 жалобы | вид | статус | раз
select coalesce(kind,'?'), coalesce(status,'?'), count(*) from translation_reports where created_at >= :since group by 1,2 order by 3 desc;

\echo ## G1 прогресс слов (с 2.0) | язык | слов в работе | выучено | показов
select learning_lang, count(*), count(*) filter (where learned), sum(times_shown) from user_words where user_id<>:admin and last_seen_at >= :since group by 1 order by 2 desc;

\echo ## P1 повторный запуск: брошенное занятие → следующее у того же человека | через | брошенных | из них 0 ответов
with s as (select id, user_id, started_at, is_completed, coalesce(answered_questions,0) a, exit_reason,
  lead(started_at) over (partition by user_id order by started_at) nxt from quiz_sessions where user_id<>:admin)
select case when nxt is null then 'не было' when nxt-started_at < interval '2 min' then '<2 мин'
  when nxt-started_at < interval '30 min' then '2-30 мин' when nxt-started_at < interval '1 day' then '<1 дня' else '1+ дн' end,
  count(*), count(*) filter (where a=0)
from s where started_at >= :since and not is_completed group by 1 order by 1;

\echo ## P2 брошенные по причине и ответам | причина | 0 | 1-2 | 3-6 | 7+
select coalesce(exit_reason,'<нет>'), count(*) filter (where coalesce(answered_questions,0)=0),
  count(*) filter (where answered_questions between 1 and 2), count(*) filter (where answered_questions between 3 and 6),
  count(*) filter (where answered_questions>=7)
from quiz_sessions where user_id<>:admin and started_at >= :since and not is_completed group by 1;

\echo ## P3 открытые без причины: давно ли начаты | возраст | занятий
select case when started_at > now()-interval '1 hour' then '<1 ч' when started_at > now()-interval '1 day' then '<1 дн' else '1+ дн' end, count(*)
from quiz_sessions where user_id<>:admin and started_at >= :since and not is_completed and exit_reason is null group by 1;

\echo ## P4 источник × исход | источник | начато | закончено | брошено с 0 ответов | людей
select coalesce(start_source,'?'), count(*), count(*) filter (where is_completed),
  count(*) filter (where not is_completed and coalesce(answered_questions,0)=0), count(distinct user_id)
from quiz_sessions where user_id<>:admin and started_at >= :since group by 1 order by 2 desc;

\echo ## P5 люди: сколько занятий бросили | брошено у человека | людей | закончено у них занятий всего
with p as (select user_id, count(*) filter (where not is_completed) ab, count(*) filter (where is_completed) ok
  from quiz_sessions where user_id<>:admin and started_at >= :since group by 1)
select least(ab,6), count(*), sum(ok) from p group by 1 order by 1;

\echo ## P6 на каком по счёту показанном вопросе ушли (журнал) | вопрос n | канал | раз
with ab as (select id from quiz_sessions where user_id<>:admin and not is_completed and started_at >= '2026-10-16'),
mx as (select distinct on (e.session_id) e.session_id, (e.data->>'n')::int n, e.channel from user_events e join ab on ab.id=e.session_id
  where e.kind='question' order by e.session_id, e.at desc)
select n, channel, count(*) from mx group by 1,2 order by 1,2;

\echo ## P7 первый вопрос занятия: канал | канал | занятий | брошено | брошено с 0 ответов
with f as (select distinct on (e.session_id) e.session_id, e.channel from user_events e where e.user_id<>:admin and e.kind='question' order by e.session_id, e.at)
select f.channel, count(*), count(*) filter (where not s.is_completed), count(*) filter (where not s.is_completed and coalesce(s.answered_questions,0)=0)
from f join quiz_sessions s on s.id=f.session_id group by 1 order by 2 desc;

\echo ## P8 «Говорю»: позиция в занятии и исход | n | показано | пропущено | ушли на нём
with q as (select e.session_id, (e.data->>'n')::int n, e.word_id, e.at from user_events e where e.user_id<>:admin and e.kind='question' and e.channel='s'),
sk as (select session_id, word_id from user_events where kind='skip' and channel='s'),
lastq as (select distinct on (session_id) session_id, at from user_events where kind='question' order by session_id, at desc)
select case when n<=3 then '1-3' when n<=8 then '4-8' else '9+' end, count(*),
  count(*) filter (where exists (select 1 from sk where sk.session_id=q.session_id and sk.word_id=q.word_id)),
  count(*) filter (where exists (select 1 from quiz_sessions s join lastq l on l.session_id=s.id where s.id=q.session_id and not s.is_completed and l.at=q.at))
from q group by 1 order by 1;

\echo ## P9 «Говорю»: люди — сколько раз показан / ответили голосом / пропустили | показано | ответили | пропустили
with pu as (select user_id, count(*) filter (where kind='question' and channel='s') shown,
  count(*) filter (where kind='speech') voiced, count(*) filter (where kind='skip' and channel='s') skipped
  from user_events where user_id<>:admin group by 1 having count(*) filter (where kind='question' and channel='s')>0)
select substr(md5(user_id::text),1,6), shown, voiced, skipped from pu order by shown desc;

\echo ## P10 «Собираю»: время ответа | секунд | ответов | верно %
select case when response_time_seconds<15 then '<15' when response_time_seconds<30 then '15-30' when response_time_seconds<60 then '30-60' else '60+' end,
  count(*), round(100.0*avg(case when is_correct then 1 else 0 end),1)
from quiz_questions q join quiz_sessions s on s.id=q.session_id where s.user_id<>:admin and s.started_at >= :since and q.channel='b' and q.answered_at is not null group by 1 order by 1;

\echo ## P11 после «Собираю» — ушли из занятия? | следующее событие | раз
with b as (select q.session_id, q.answered_at from quiz_questions q join quiz_sessions s on s.id=q.session_id
  where s.user_id<>:admin and s.started_at >= :since and q.channel='b' and q.answered_at is not null)
select case when exists (select 1 from quiz_questions q2 where q2.session_id=b.session_id and q2.answered_at > b.answered_at) then 'продолжили' else 'последний ответ' end, count(*) from b group by 1;

\echo ## P12 точность занятий: распределение | точность | занятий законченных
select case when correct_answers*1.0/nullif(answered_questions,0) >= .95 then '95-100' when correct_answers*1.0/nullif(answered_questions,0) >= .85 then '85-94'
  when correct_answers*1.0/nullif(answered_questions,0) >= .7 then '70-84' else '<70' end, count(*)
from quiz_sessions where user_id<>:admin and started_at >= :since and is_completed group by 1 order by 1;

\echo ## P13 занятий за день у человека (законченных) | за день | случаев
select n, count(*) from (select user_id, coalesce(local_day, completed_at::date) d, count(*) n from quiz_sessions
  where user_id<>:admin and started_at >= :since and is_completed group by 1,2) x group by 1 order by 1;

\echo ## P14 путь новичка с 2.0 по шагам | шаг | людей
with u as (select id from users where id<>:admin and created_at >= :since)
select 'пришли', count(*) from u
union all select 'начали занятие', count(*) from u where exists (select 1 from quiz_sessions s where s.user_id=u.id)
union all select 'ответили на 1+', count(*) from u where exists (select 1 from quiz_sessions s where s.user_id=u.id and s.answered_questions>=1)
union all select 'ответили на 4+', count(*) from u where exists (select 1 from quiz_sessions s where s.user_id=u.id and s.answered_questions>=4)
union all select 'закончили 1', count(*) from u where exists (select 1 from quiz_sessions s where s.user_id=u.id and s.is_completed)
union all select 'закончили 2+', count(*) from u where (select count(*) from quiz_sessions s where s.user_id=u.id and s.is_completed)>=2
union all select 'занимались 2+ дня', count(*) from u where (select count(distinct coalesce(local_day,completed_at::date)) from quiz_sessions s where s.user_id=u.id and s.is_completed)>=2;

\echo ## P15 новички, не начавшие занятие: что делали (журнал) | вид | действие | раз | людей
with u as (select id from users where id<>:admin and created_at >= '2026-10-16' and not exists (select 1 from quiz_sessions s where s.user_id=users.id))
select e.kind, left(coalesce(e.action,''),40), count(*), count(distinct e.user_id) from user_events e join u on u.id=e.user_id group by 1,2 order by 3 desc limit 15;

\echo ## P16 час суток (UTC) | час | начато | закончено
select extract(hour from started_at)::int, count(*), count(*) filter (where is_completed) from quiz_sessions where user_id<>:admin and started_at >= :since group by 1 order by 1;

\echo ## P17 «Ещё занятие» после законченного | у законченного было продолжение в течение 10 мин | занятий
with s as (select user_id, started_at, completed_at, is_completed, lead(started_at) over (partition by user_id order by started_at) nxt from quiz_sessions where user_id<>:admin)
select case when nxt is not null and nxt - completed_at < interval '10 min' then 'да' else 'нет' end, count(*) from s where started_at >= :since and is_completed group by 1;

\echo ## P18 напоминания: кому включено и было ли занятие за 7 дней | вкл | авто | человек | занимались 7 дн
select notifications_enabled, coalesce(reminders_auto,false), count(*),
  count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=users.id and s.is_completed and s.started_at > now()-interval '7 day'))
from users where id<>:admin group by 1,2 order by 1,2;

\echo ## E3 сообщения против контрольной группы | вид | исход | решений | вернулись 24 ч % | вернулись 72 ч %
select kind, outcome, count(*),
  round(100.0*avg(case when exists (select 1 from quiz_sessions s where s.user_id=n.user_id and s.started_at between n.sent_at and n.sent_at+interval '24 hour') then 1 else 0 end),1),
  round(100.0*avg(case when exists (select 1 from quiz_sessions s where s.user_id=n.user_id and s.started_at between n.sent_at and n.sent_at+interval '72 hour') then 1 else 0 end),1)
from nudge_log n where n.user_id<>:admin and n.sent_at is not null group by 1,2 order by 1,2;

\echo ## E4 контрольная группа по людям (формула кода) | в контроле | людей | занимались после 2.0 | занимались 2+ дня
select (u.id::numeric*2654435761) % 1000 < 100, count(*),
  count(*) filter (where exists (select 1 from quiz_sessions s where s.user_id=u.id and s.is_completed and s.started_at >= :since)),
  count(*) filter (where (select count(distinct coalesce(local_day,completed_at::date)) from quiz_sessions s where s.user_id=u.id and s.is_completed and s.started_at >= :since)>=2)
from users u where u.id<>:admin group by 1;

\echo ## E5 час отправки напоминаний (UTC) | вид | час | раз
select kind, extract(hour from sent_at)::int, count(*) from nudge_log where user_id<>:admin and outcome='sent' group by 1,2 order by 1,2;

\echo ## N1 занятия по журналу (с 2.2.1): дверь входа → закончено | дверь | начато | закончено | медиана сек
select s.data->>'source', count(*), count(f.id), percentile_cont(0.5) within group (order by (f.data->>'seconds')::int)
from user_events s left join user_events f on f.kind='lesson' and f.action='finished' and f.session_id=s.session_id
where s.user_id<>:admin and s.kind='lesson' and s.action='started' and s.at >= :since group by 1 order by 2 desc;

\echo ## N2 «Продолжить / Начать новое» | действие | раз | людей
select action, count(*), count(distinct user_id) from user_events
where user_id<>:admin and kind='lesson' and action in ('resume','new_instead') and at >= :since group by 1;

\echo ## N3 «Говорю»: вопрос «убрать?» | действие | раз | людей
select action, count(*), count(distinct user_id) from user_events
where user_id<>:admin and kind='speech_offer' and at >= :since group by 1;

\echo ## N4 блокировки по дням (журнал) | день | заблокировали | вернулись
select at::date, count(*) filter (where action='blocked'), count(*) filter (where action='unblocked')
from user_events where user_id<>:admin and kind='chat' and at >= :since group by 1 order by 1;

\echo ## N5 заблокировавшие: дней от последнего законченного занятия | дней | людей
with b as (select user_id, max(at) at from user_events where user_id<>:admin and kind='chat' and action='blocked' and at >= :since group by 1)
select coalesce(least(extract(day from b.at - (select max(completed_at) from quiz_sessions s where s.user_id=b.user_id and s.is_completed))::int, 30)::text, 'не занимались'), count(*)
from b group by 1 order by 1;

\echo ## N6 ошибки по людям (журнал) | вид | где | раз | людей
select action, data->>'where', count(*), count(distinct user_id) from user_events
where user_id<>:admin and kind='error' and at >= :since group by 1,2 order by 3 desc limit 20;

\echo ## N7 кнопки меню и команды | действие | раз | людей
select action, count(*), count(distinct user_id) from user_events
where user_id<>:admin and kind='msg' and (action like 'меню %' or action like 'команда %') and at >= :since group by 1 order by 2 desc;
ROLLBACK;
