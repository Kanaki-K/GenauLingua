# GenauLingua — learn any of six languages from the one you speak

**A production Telegram bot for vocabulary learning (A1–C2)** — six languages in any
pair, six games mixed inside every lesson, natural-voice audio for every word,
speech recognition, adaptive spaced repetition and monthly leaderboards.
Free and ad-free.

🤖 **Live bot:** [t.me/GenauLingua_bot](https://t.me/GenauLingua_bot)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.15-2CA5E0?logo=telegram&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%20async-D71F00)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![Tests](https://img.shields.io/badge/tests-1278-success)

---

## Overview

GenauLingua is a real, deployed Telegram bot. Version **2.0** went live on
**14 October 2026**: the bot grew from one game and one language (German) to six
languages in any combination, six games, full pronunciation and speech practice.
Version **2.1 "Retention"** followed on **16 October 2026**: it is about bringing
people back — 79% of everyone who ever studied had never studied two days in a row.

| | 1.x (until Oct 2026) | 2.0 (14 Oct) | **2.1 (live, 16 Oct)** |
|---|---|---|---|
| Languages to learn | German | 6, any pair — 30 directions | same |
| Interface languages | 4 | 6 | same |
| Games | 1 (pick the translation) | 6, mixed in every lesson | same; **I build** simpler at A1–A2 |
| Audio | — | every word and example, natural voice | same |
| Speech | — | voice answers checked by speech recognition | **+ a hint where to record** |
| First lesson | like any lesson | 7 questions | **7 easy cards from the 60 most common short words** |
| Messages from the bot | daily reminder | daily reminder to everyone who has them on | **one dispatcher: about the person, ≤ 1 a day, stops after 14 days, 10% control group** |
| Day streak | by UTC day | in the learner's time zone | **+ weekly freeze, milestones 3/7/14/30, 🔥 in the ranking** |
| Restarts | interrupted lessons | interrupted lessons | **lessons survive a restart (Redis)** |
| Analytics | admin panel | admin panel, cohorts | **+ per-person journey log, message outcomes vs. control group** |

### Production numbers (16 Oct 2026, at the 2.1 release)

| Metric | Value |
|---|---|
| Registered users | 249 |
| Active in the last 7 / 30 days | 16 / 23 |
| Lessons started / completed in the last 7 days | 83 / 50 |
| Word base | 12,902 words × 6 languages, A1–C2, 20 topics |
| Pronunciation clips | 121,269 |
| Test suite | 1,278 tests |

These are also the **"before" point** for 2.1: the effect of the release is measured against
them (same queries, a week later).

---

## What's new in 2.1 — Retention

Every item below answers a number or a case from production on 15 October 2026.

| Change | Why |
|---|---|
| **Engagement messages** replace the old reminders. After a break the bot writes on day 1, 3, 7 and 14, then stops; a newcomer who never started gets an invitation on day 1, 3 and 7. Those who turned reminders on get them at their own hour while the break is ≤ 2 days. Never more than one a day, at least 12 h apart, daytime only. Each message is about the person — their streak, their numbers, one of their words under a spoiler as a mini-question. "Don't send" is final; blocking the bot counts as "don't send". | The old daily reminder was "a note about the bot instead of about the person"; 24 people blocked the bot after the 2.0 reminder wave. |
| **Control group and outcomes.** 10% of people get no ladder messages; every decision is logged. Admin → "Messages" shows who came back within a day, who tapped the button, who unsubscribed or blocked — next to the control group. | "Track it — so we know whether it works or harms." |
| **Easy first lesson**: 7 cards from the 60 most frequent short words (≤ 10 letters, single word), respecting the chosen topic. | 21 of 32 abandoned lessons were abandoned on question 0–2; a Polish newcomer got "mieć na myśli" as the very first word. |
| **Streak**: one missed day a week is frozen, not reset; milestones at 3, 7, 14 and 30 days; 🔥 next to the name in the ranking from 3 days. | Streak mechanics shown to work elsewhere; approved by the owner. |
| **Known words faster**: a word answered correctly at first sight is learned after one more correct check (two in a row instead of three). There is no "I know this" button — an accidental tap is a guess. | Learner feedback: "I don't need to prove it three times." |
| **I build at A1–A2**: phrases of up to 5–6 words, one trap, never another form of a word in the phrase (`gehe/geht`). | I build: 44% correct overall, 25% at A1, ~51 s per answer. |
| **I speak**: the card says where to record a voice message (hold 🎤 at the bottom right of Telegram). | Two voice attempts in a whole day of production. |
| **Lessons in Redis**: a deploy or restart no longer interrupts a lesson; an answer caught mid-restart does not lock the question. | Restarts on 15 October twice cut people's lessons. |
| **Journey log**: taps, questions, voice attempts (what was heard, similarity, attempt number), skips and level changes — `app/scripts/journey.py --user <hash> --day <date>`. | 15 October's analysis had to reconstruct a path from indirect evidence. |
| **Word base**: slang meanings moved behind a neutral first meaning (13 words); 19 example translations aligned with the German original (e.g. *meinen*). | A 750-pair check against the German original found ~2% flawed examples. |
| **One look for every message**: hyphen instead of a long dash, a blank line between lines, no full stop at the end, formal address in all six languages. | Owner: "full stops visually constrain". |

---

## What the learner gets

### One button, six games
A lesson is **15 questions** behind a single "Learn words" button. Games alternate
inside the lesson — the learner never has to choose:

| Game | Task | Skill |
|---|---|---|
| 📖 **I read** | word → pick the meaning | recognition |
| 💭 **I recall** | meaning → pick the word | recall |
| 🎧 **I listen** | audio → pick the word | listening |
| 🎤 **I speak** | say the word in a voice message | production, pronunciation |
| 🧩 **Find the pairs** | match 5 words with 5 meanings on a board | consolidation |
| 🧱 **I build** | assemble the example sentence from word tiles with traps | grammar, word order |

Games unlock **per word**: a new word always arrives as a card; recall and listening
open after one correct answer, speaking and sentence building after two. A beginner's
first lesson is 7 easy cards (the most common short words); from the second one the other
games join in.

**I build** adds grammatical twins as traps (`der/den/dem`, `ist/sind`, `er/sie`) — one at
A1–A2 with phrases of up to 5–6 words, 2–5 at higher levels — never gives the first word away with a capital
letter, and only uses words at or below the learner's level. The result screen marks
every word ✓/✗, lists what was extra and what was missing, and says "right words,
different order" when only the order differs.

**I speak** uses self-hosted speech recognition (faster-whisper on the bot's own server):
two attempts, then
the question is skipped without a penalty — a microphone problem is not a mistake. The card
says where to record (hold 🎤 in Telegram's input field).
Listening and speaking both have a **Skip** button for when sound is not an option.

### Spaced repetition that adapts
- Words return after an hour (after a mistake), a day, 3 days, a week, 3 weeks, 2 months.
- **Learned** = three correct answers in a row on different days; a word answered correctly
  at first sight needs only one more correct check.
- The bot **offers** the next level at ≥ 90% accuracy (and asks again 5 lessons after a "no").
- A learning goal (work, travel, living abroad, study) puts topic words first.
- Modes: by level, by topic, the whole base, difficult words; mistakes can be repeated right
  after the lesson.

### Audio
Every word and every example sentence is voiced with a natural voice (several voices per
language). Listening questions use a neutral clip title so the answer is not printed on the
player. A slow reference clip is one tap away in the speaking game. Clips are cached as
Telegram `file_id`s — instant playback, no server bandwidth.

### Motivation
- **Monthly and all-time leaderboards**, per learning language, with medals for places 1–3.
- **Points reward effort**: listening ×2, speaking ×3, plus lesson, streak, accuracy and
  learned-word bonuses.
- **Day streak** counted in the learner's own time zone, with one frozen day a week,
  milestones at 3 / 7 / 14 / 30 days and 🔥 next to the name in the ranking from 3 days.
- **Engagement messages** — after a break of 1, 3, 7 and 14 days (then silence until the
  learner returns), or daily at the learner's own hour for those who asked. Each one is about
  the person: their streak, their progress, one of their own words as a mini-question. At most
  one a day; "don't send" is final.
- **Report a mistake** from the lesson summary; each confirmed report earns +15 points.

### Statistics
A home screen with one skill bar per game shows the gap between skills ("I recognise it
in writing but not by ear"); the detailed view adds learned / in progress / difficult,
grammar accuracy, lesson history and overall progress.

### For the owner
An admin panel with analytics, cohorts, churn, "started / completed" lessons, "came back
today out of those active in the last 7 days", per-language broadcasts and report
moderation; a "Messages" report compares people who got an engagement message with the
control group. A per-person journey log answers "where exactly did this person stop".
Release notes go out in every learner's interface language, and the bot sends follow-up
reports on how many came back.

---

## Architecture

```
app/
├── bot/
│   ├── handlers/
│   │   ├── quiz/        # one module per concern:
│   │   │   ├── lesson.py        # lesson flow: start, next question, repeat mistakes
│   │   │   ├── lesson_state.py  # FSM keys, the per-chat lock, restart-safe answer claims
│   │   │   ├── question.py      # question and answer screens
│   │   │   ├── choice.py        # 📖 💭 🎧 answers by button
│   │   │   ├── listen.py        # 🎧 audio and its fallback to text
│   │   │   ├── speech.py        # 🎤 voice answers, slow reference, skip
│   │   │   ├── match.py         # 🧩 pairs board
│   │   │   ├── build.py         # 🧱 sentence building
│   │   │   ├── summary.py       # lesson summary, praise, level offer
│   │   │   ├── expired.py       # buttons of a lesson the bot no longer remembers
│   │   │   └── home / stats / settings / report / help
│   │   ├── leaderboard/  # monthly, all-time, tables
│   │   ├── reminders.py, start.py, admin.py
│   ├── routers.py       # the router set and its ORDER — one source for bot and tests
│   └── keyboards/, states.py
├── services/            # business logic: quiz engine, SRS, scoring, leaderboards,
│                        # build_service, speech_check, audio, word groups,
│                        # nudge_plan / nudge_texts (who gets which message), journal
├── database/            # SQLAlchemy 2.0 models (19 tables), enums, async session
├── schedulers/          # engagement messages (nudges.py), monthly season rollover
├── locales/             # uk / en / tr / de / pl / ru
├── testing/             # fake Telegram + the real dispatcher, shared by tests and tooling
├── scripts/             # 118 tools: acceptance suites, deploy, wordbase, TTS, reports,
│                        # journey log, message forecast
└── main.py

alembic/                 # 45 migrations
tests/                   # 1,278 tests
deploy/                  # preflight and backup scripts
```

About 30k lines of application code, 28k lines of tooling, 20k lines of tests.

**Design principles**
- **One source per decision.** Answer channels, their prices and unlock thresholds come from
  one enum (`QuizChannel`, `counted_channels()`); the scoring formula lives in
  `MonthlyStats.calculate_monthly_score()`; who is ranked in a month is one predicate
  (`ranked_in_month`). Every one of these was once duplicated, and every duplicate drifted.
- **Rule, not list.** Progress columns are merged by a rule read from the table itself, so a
  new column cannot be silently dropped by a rebuild.
- **Handlers stay thin**; learning logic lives in `services/` and is tested without Telegram.
- **Fully async**: aiogram 3 + SQLAlchemy 2.0 + asyncpg.
- **Idempotent answers**: a per-chat lock claims each question exactly once — double taps
  never score twice; a claim left by a process that died mid-answer is released.
- **One sender for every bot-initiated message**: one rule (`nudge_plan.decide`) decides who
  gets what; a conditional UPDATE claims each send, so two processes never send twice.

**Verification beyond unit tests** — every change is also checked by acceptance suites that
play the real dispatcher on the real word base:

| Suite | What it proves |
|---|---|
| `audit_round --full` | 38 lesson compositions played to the end: numbering, counters, mistakes, reports, channels and points agree |
| `verify_quiz_channels` | every game builds correctly in all 30 language pairs |
| `verify_quiz_round` | 60 lessons, 900 questions — every question has a word or a sound |
| `audit_accounting` | 17 checks across five accounting layers: answers ↔ lessons ↔ progress ↔ month ↔ all-time |
| `verify_buttons` | no button leads nowhere, menus work in all 6 languages |
| `release_snapshot --compare` | a deploy loses nothing: users, progress, answers, awards |
| `nudge_forecast` | who would get which engagement message, hour by hour — nothing is sent |

Tests are written "break it on purpose": a fix is accepted only after the test was seen to
fail with the fix removed.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Telegram | aiogram 3.15 (async) |
| Database | PostgreSQL 16, SQLAlchemy 2.0 async, asyncpg, Alembic |
| Lesson state | Redis 7 (append-only), aiogram RedisStorage |
| Speech recognition | faster-whisper (CTranslate2, int8, on CPU) |
| Text-to-speech | edge-tts |
| Scheduling | APScheduler |
| Config | Pydantic Settings |
| Errors | Sentry (optional) |
| Deployment | Docker Compose on Hetzner (EU) |

---

## Getting Started

```bash
git clone https://github.com/Kanaki-K/GenauLingua.git
cd GenauLingua

cp .env.example .env      # BOT_TOKEN, ADMIN_USER, database credentials
docker compose up -d --build
```

Migrations run automatically on container start. The speech-recognition model is baked into
the image at build time, so the first voice answer does not wait for a download.

Run the tests (a PostgreSQL test database on port 5433 is expected; override with
`TEST_DATABASE_URL`):

```bash
pytest
```

### Releasing to production
[`DEPLOY.md`](DEPLOY.md) is the step-by-step procedure used for the 2.0 and 2.1 releases: preflight,
backup, image build while the old bot keeps running, snapshot, migrations, word-base
transfer, the "nothing lost" comparison **before** the accounting repair, and rollback.
It was rehearsed on a copy of the production database before the real run. For 2.1 it adds
a forecast of who gets which message in the next 48 hours (`nudge_forecast`) — run after the
migration and before the bot starts, so a release never sends a wave of messages.

### Working notes
The project notes are in Russian, the owner's language:
[`STATE.md`](STATE.md) · [`ROADMAP.md`](ROADMAP.md) · [`REWARDS.md`](REWARDS.md)
(next: status and competition) · [`WORDBASE_REVIEW.md`](WORDBASE_REVIEW.md) ·
[`AUDIO_STORAGE.md`](AUDIO_STORAGE.md) · [`DEPLOY.md`](DEPLOY.md).

### Configuration
All secrets are supplied via environment variables in `.env`; **no secrets are stored in the
repository**. See [`.env.example`](.env.example).

---

## What This Project Demonstrates

- **Product engineering end to end** — from a one-game bot to a six-game, six-language product,
  deployed to real users with zero data loss (verified row by row).
- **Learning design** — spaced repetition, per-word game unlocking, a difficulty ladder by CEFR
  level, effort-based scoring.
- **Speech and audio** — self-hosted speech recognition with word-boundary matching (so "das Ei"
  is not heard inside "Bleistift"), and a TTS pipeline that produced and verified 121,269 clips.
- **Internationalisation** — six languages with language-specific correctness (Turkish `İ/ı`,
  German noun capitalisation, Polish impersonal politeness, formal address everywhere).
- **Data integrity** — five-layer accounting with an automated audit and an idempotent repair.
- **Operations** — rehearsed releases, backups, rollback tags, firewall and fail2ban on the
  server, scheduled broadcasts and follow-up reports; lessons survive restarts.
- **Retention as an experiment** — every engagement message is logged with its outcome next
  to a fixed 10% control group, so "it works or it harms" is measured, not assumed.

---

## Privacy

The bot processes only what it needs to run (Telegram ID, learning progress, preferences).
Details: [PRIVACY_POLICY.md](PRIVACY_POLICY.md).

## License

Built as an independent product. The bot is free to use and runs without ads.
