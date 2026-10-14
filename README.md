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
![Tests](https://img.shields.io/badge/tests-1118-success)

---

## Overview

GenauLingua is a real, deployed Telegram bot. Version **2.0** went live on
**14 October 2026**: the bot grew from one game and one language (German) to six
languages in any combination, six games, full pronunciation and speech practice.

| | 1.x (until Oct 2026) | **2.0 (live)** |
|---|---|---|
| Languages to learn | German | **6, any pair — 30 directions** |
| Interface languages | 4 | **6** |
| Games | 1 (pick the translation) | **6, mixed in every lesson** |
| Audio | — | **every word and example, natural voice** |
| Speech | — | **voice answers checked by speech recognition** |
| Grammar | — | **sentence building with grammatical traps** |
| Word base | 12,902 words | 12,902 words, proofread 3× (≈14,900 corrections) |

### Production numbers (14 Oct 2026)

| Metric | Value |
|---|---|
| Registered users | 233 |
| Users who completed ≥ 1 lesson | 209 (90%) |
| Active in the last 30 / 90 days | 23 / 50 |
| Word base | 12,902 words × 6 languages, A1–C2, 20 topics |
| Pronunciation clips | 121,269 |
| Test suite | 1,118 tests |

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
first lesson is cards only; from the second one the other games join in.

**I build** adds 2–5 grammatical twins as traps (`der/den/dem`, `ist/sind`,
`er/sie`) — more at higher levels — never gives the first word away with a capital
letter, and only uses words at or below the learner's level. The result screen marks
every word ✓/✗, lists what was extra and what was missing, and says "right words,
different order" when only the order differs.

**I speak** uses self-hosted speech recognition (faster-whisper on the bot's own server):
two attempts, then
the question is skipped without a penalty — a microphone problem is not a mistake.
Listening and speaking both have a **Skip** button for when sound is not an option.

### Spaced repetition that adapts
- Words return after an hour (after a mistake), a day, 3 days, a week, 3 weeks, 2 months.
- **Learned** = three correct answers in a row on different days.
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
- **Day streak** counted in the learner's own time zone.
- **Reminders with a reason** — a streak at risk, words due for review, the place in this
  month's ranking — one reason per message, at the learner's time and days.
- **Report a mistake** from the lesson summary; each confirmed report earns +15 points.

### Statistics
A home screen with one skill bar per game shows the gap between skills ("I recognise it
in writing but not by ear"); the detailed view adds learned / in progress / difficult,
grammar accuracy, lesson history and overall progress.

### For the owner
An admin panel with analytics, cohorts, churn, per-language broadcasts and report
moderation; release notes go out in every learner's interface language, and the bot
sends follow-up reports on how many came back.

---

## Architecture

```
app/
├── bot/
│   ├── handlers/
│   │   ├── quiz/        # one module per concern:
│   │   │   ├── lesson.py        # lesson flow: start, next question, repeat mistakes
│   │   │   ├── lesson_state.py  # FSM keys and the per-chat lock
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
│                        # build_service, speech_check, audio, word groups
├── database/            # SQLAlchemy 2.0 models (15 tables), enums, async session
├── schedulers/          # reminders, monthly season rollover
├── locales/             # uk / en / tr / de / pl / ru
├── testing/             # fake Telegram + the real dispatcher, shared by tests and tooling
├── scripts/             # 112 tools: acceptance suites, deploy, wordbase, TTS, reports
└── main.py

alembic/                 # 42 migrations
tests/                   # 1,118 tests
deploy/                  # preflight and backup scripts
```

About 28k lines of application code, 27k lines of tooling, 17k lines of tests.

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
  never score twice.

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

Tests are written "break it on purpose": a fix is accepted only after the test was seen to
fail with the fix removed.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Telegram | aiogram 3.15 (async) |
| Database | PostgreSQL 16, SQLAlchemy 2.0 async, asyncpg, Alembic |
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
[`DEPLOY.md`](DEPLOY.md) is the step-by-step procedure used for the 2.0 release: preflight,
backup, image build while the old bot keeps running, snapshot, migrations, word-base
transfer, the "nothing lost" comparison **before** the accounting repair, and rollback.
It was rehearsed on a copy of the production database before the real run.

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
  server, scheduled broadcasts and follow-up reports.

---

## Privacy

The bot processes only what it needs to run (Telegram ID, learning progress, preferences).
Details: [PRIVACY_POLICY.md](PRIVACY_POLICY.md).

## License

Built as an independent product. The bot is free to use and runs without ads.
