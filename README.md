# GenauLingua — German Vocabulary Learning Bot

**A production Telegram bot for learning German vocabulary (A1–C2)** with an adaptive
spaced-repetition engine, gamification, multi-language UI, and an admin analytics panel.

🤖 **Live bot:** [t.me/GenauLingua_bot](https://t.me/GenauLingua_bot)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.15-2CA5E0?logo=telegram&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%20async-D71F00)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

---

## Overview

GenauLingua is a fully deployed, real-world Telegram bot that teaches German vocabulary
using a personalized spaced-repetition system (SRS). It has been running in production,
serving real users, with a curated database of **12,902 words** across CEFR levels A1–C2.

The project is a complete, end-to-end product: data pipeline, async backend, database
design and migrations, gamification systems, background schedulers, full internationalization,
text-to-speech pronunciation, an admin analytics dashboard, and containerized deployment.

### Results in production

| Metric | Value |
|---|---|
| Registered users | 204 |
| Users who completed ≥1 quiz | 116 (57%) |
| Total quizzes completed | 1,570 |
| Uptime | Deployed on Hetzner (EU) via Docker |

### The current release, prepared and pending deployment

| Metric | Value |
|---|---|
| Word database | **12,902 words** (A1–C2) |
| Languages | 🇩🇪 DE · 🇬🇧 EN · 🇷🇺 RU · 🇺🇦 UK · 🇹🇷 TR · 🇵🇱 PL |
| Cells of content | **77,412** (12,902 rows × 6 languages) |
| Language pairs playable | **30**, the thinnest covered by 9,171 rows |
| Pronunciation clips | **121,269** synthesized, 0 missing |
| Editorial passes over the base | 3 — **14,875 corrections** |
| Automated base checks | 50 scans, 10 of them hard gates |
| Test suite | 457 tests |

> **Status:** The live bot runs the previous release (4 languages, no audio). The release
> above — two more languages and full pronunciation — is built and verified on a dev
> copy, awaiting the owner's deployment window.

---

## Key Features

**Adaptive spaced repetition (SRS).** Each word carries an individual repetition interval per
user. Weak and frequently-missed words resurface more often; mastered words fade out. Difficulty
adapts continuously to performance.

**Curated word database.** 12,902 words across A1–C2, organized into 21 thematic categories.
Every word ships with a translation and an example sentence in 6 languages (DE/EN/RU/UK/TR/PL),
plus part of speech, article, and frequency rank. The base has been read end-to-end three times
and corrected 14,875 times; 50 automated checks guard it against regression.

**Pronunciation.** Every word and every example sentence is voiced — 121,269 clips. A card
plays the single meaning it shows, never the whole translation cell, and heteronyms
(`live` as /lɪv/ or /laɪv/) are voiced inside their example so the reading is unambiguous.
Clips are cached as Telegram `file_id`s, so playback is instant and costs the server nothing.

**Smart quizzes.** 25-word sessions with 4 answer options and instant feedback (correct answer +
example sentence). Distractors are chosen intelligently (same part of speech, different article).
Mistake-repetition mode replays missed words after each session.

**Multi-language & multi-mode.** 6 languages in 30 playable pairs, plus a reverse mode for
advanced learners. Every UI string is fully localized.

**Gamification.** Monthly and all-time leaderboards, top-10 rankings, automatic season resets,
win streaks, achievements, and a transparent scoring system (quizzes, reverse mode, words learned,
streak days, accuracy bonuses).

**Reminders.** Configurable reminder time and days with 20+ timezone support and motivational
messages that include the user's progress.

**Learning statistics.** Per-level and overall progress bars, quiz history, word breakdown
(learned / in progress / difficult), streak tracking, and achievements.

**Admin analytics panel.** Dashboard with cohort analysis, churn detection, CSV export,
localized broadcast messaging, and per-user detailed statistics.

---

## Architecture

A clean, layered async architecture — ~20k lines of application code,
backed by ~22k lines of verification tooling:

```
app/
├── bot/
│   ├── handlers/        # Telegram update handlers (quiz, leaderboard, reminders, admin, start)
│   ├── keyboards/       # Inline keyboard builders
│   ├── routers.py       # The router set and its ORDER — one source for bot and tests
│   ├── states.py        # FSM states
│   └── utils.py
├── services/            # Business logic (quiz engine, SRS, scoring, leaderboards, TTS, matching)
├── database/
│   ├── models.py        # SQLAlchemy 2.0 ORM models
│   ├── enums.py         # CEFR levels, POS, quiz modes, answer channels
│   └── session.py       # Async engine / session factory
├── schedulers/          # APScheduler jobs (reminders, monthly season rollover)
├── locales/             # de / en / pl / ru / tr / uk — six interface languages
├── testing/             # Fake Telegram + real dispatcher; used by BOTH tests and tooling
├── scripts/             # 100 live tools: acceptance suites, TTS pipeline, wordbase probes
├── core/                # Logging, Sentry, clock
├── config.py            # Pydantic settings (env-driven, no secrets in code)
└── main.py              # Composition root / bot bootstrap

alembic/                 # Versioned database migrations
archive/                 # Applied one-off wordbase patches — provenance, not code
tests/                   # 667 tests, including 23 end-to-end dispatcher scenarios
```

**Design highlights:**

- **Handlers stay thin** — all learning logic (word selection, SRS scoring, distractor generation,
  progress tracking) lives in `services/` and is independently testable.
- **Fully async** end-to-end: `aiogram 3.x` + `SQLAlchemy 2.0` async ORM + `asyncpg`.
- **Schema-versioned** with Alembic; migrations apply automatically on container startup.
- **Config via environment only** — Pydantic `BaseSettings`, no secrets committed to the repo.
- **Observability** — structured logging and optional Sentry error tracking.
- **One source per decision.** The router set and its order live in `bot/routers.py`;
  the scoring formula lives in `MonthlyStats.calculate_monthly_score()`; the
  "which words does this learner study" filter lives in one query builder. Each of
  these was once duplicated, and each duplicate drifted.
- **Acceptance beyond unit tests.** `app/scripts/audit_round.py` plays a whole
  lesson through the real dispatcher on the real wordbase and asserts the
  invariants that must hold *between* parts — numbering, no repeated word,
  session counters vs answer rows, error list, reportable words, channel
  thresholds, points, and answer idempotence. Checking the parts in isolation had
  passed cleanly while two of those invariants were broken.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Telegram framework | aiogram 3.15 (async) |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Scheduling | APScheduler |
| Config | Pydantic Settings |
| Error tracking | Sentry (optional) |
| Deployment | Docker / Docker Compose |

---

## Getting Started

```bash
git clone https://github.com/Kanaki-K/GenauLingua.git
cd GenauLingua

cp .env.example .env      # fill in BOT_TOKEN, ADMIN_USER, DB credentials
docker compose up -d --build
```

Database migrations run automatically on container startup. See
[`app/scripts/README.md`](app/scripts/README.md) for rebuilding the word database from an
Excel dataset.

### Checking the state of the content

One command answers "is everything in order" — base integrity, language-pair coverage,
card contract, audio store, and the latest speech-recognition results:

```bash
ENV_FILE=.env.local python -m app.scripts.state_report
```

The working notes live in the repository root and are written in Russian, the owner's
language: [`STATE.md`](STATE.md) (where we are) · [`HANDOVER.md`](HANDOVER.md) (full state
and open decisions) · [`WORDBASE_REVIEW.md`](WORDBASE_REVIEW.md) (how the base is proofread)
· [`AUDIO_STORAGE.md`](AUDIO_STORAGE.md) (where audio lives and what it costs)
· [`DEPLOY.md`](DEPLOY.md) (release procedure).

### Configuration

All secrets (bot token, database credentials, admin ID) are supplied via environment variables
in `.env`. **No secrets are stored in the repository.** See [`.env.example`](.env.example) for
the full list of variables.

---

## What This Project Demonstrates

For anyone evaluating this as a portfolio piece, GenauLingua shows end-to-end delivery of:

- **Async Python backend engineering** — non-trivial `aiogram 3` bot with FSM flows, inline
  keyboards, and clean handler/service separation.
- **Relational data modeling** — 12-table PostgreSQL schema with a real migration history.
- **Algorithm design** — a working spaced-repetition engine and weighted word/distractor selection.
- **Product systems** — gamification (seasons, streaks, leaderboards), scheduled jobs, and reminders.
- **Internationalization** — a 6-language product with fully localized content and UI, including
  language-specific correctness most pipelines get wrong (Turkish dotted/dotless `İ`/`I` is cased
  by Turkish rules, not Python's `.upper()`).
- **Data engineering** — an ingestion pipeline that builds a 12.9k-word, 6-language dataset, plus
  a text-to-speech pipeline producing and verifying 121,269 audio clips.
- **Quality engineering at scale** — 50 automated content checks, each with a *documented*
  expected residual so it fails when the residual **changes**, not merely when it is non-zero;
  content correctness closed the loop machine-to-machine by running every generated clip back
  through speech recognition (2,536 checked, 99.76% exact).
- **DevOps** — containerized, environment-driven deployment running in production.

---

## Privacy

The bot processes only the minimal data needed to run (Telegram ID, learning progress,
preferences). Full details: [PRIVACY_POLICY.md](PRIVACY_POLICY.md).

---

## License

Built as an independent product. The bot is free to use and runs without ads.
