"""
АУДИТ ПОДБОРА СЛОВ: симуляция занятий одного человека через настоящий подбор.

Время двигается сдвигом всех отметок в базе назад (user_words, quiz_questions),
что для подбора равносильно ходу часов вперёд. Печатает замеры (-s).
"""
import collections
import random
from datetime import timedelta

from sqlalchemy import select, text

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, PartOfSpeech, QuizChannel, QuizMode
from app.database.models import QuizQuestion, QuizSession, UserWord, Word, WordFrequency
from app.services import quiz_service as qs
from app.services.language_service import pair_from_user
from app.services.match_service import (
    BOARD_SIZE, board_slot, pick_words, should_insert_board,
)
from tests.conftest import build_groups, make_word

POS_MIX = ([PartOfSpeech.NOUN] * 5 + [PartOfSpeech.VERB] * 3
           + [PartOfSpeech.ADJECTIVE] * 2)
ARTICLES = ["der", "die", "das"]


async def seed(session, n_a1=740, n_a2=300, category=None, n_cat=0, seed_=1):
    rng = random.Random(seed_)
    words = []
    for lvl, n in ((CEFRLevel.A1, n_a1), (CEFRLevel.A2, n_a2)):
        for i in range(n):
            pos = rng.choice(POS_MIX)
            w = make_word(
                f"W{lvl.value}{i:04d}", level=lvl, pos=pos,
                article=rng.choice(ARTICLES) if pos == PartOfSpeech.NOUN else None,
                ru=f"знач{lvl.value}{i:04d}",
                category=(category if category and lvl == CEFRLevel.A1 and i < n_cat else None),
            )
            session.add(w)
            words.append(w)
    await session.flush()
    for w in words:
        session.add(WordFrequency(word_id=w.id, lang="de", zipf=rng.uniform(2.5, 6.5)))
    await build_groups(session, ["de"])
    return words


async def shift(session, delta: timedelta):
    """Ход часов вперёд на delta: все отметки — назад."""
    await session.commit()
    p = {"d": delta.total_seconds()}
    await session.execute(text(
        "update user_words set last_seen_at = last_seen_at - make_interval(secs => cast(:d as double precision)), "
        "created_at = created_at - make_interval(secs => cast(:d as double precision)), learned_at = learned_at - make_interval(secs => cast(:d as double precision)), "
        "updated_at = updated_at - make_interval(secs => cast(:d as double precision))"), p)
    await session.execute(text(
        "update quiz_questions set answered_at = answered_at - make_interval(secs => cast(:d as double precision)), created_at = created_at - make_interval(secs => cast(:d as double precision))"), p)
    await session.execute(text("update quiz_sessions set started_at = started_at - make_interval(secs => cast(:d as double precision))"), p)
    await session.commit()
    for obj in list(session.identity_map.values()):
        if isinstance(obj, UserWord):
            session.expire(obj)


class Learner:
    def __init__(self, rng):
        self.rng = rng
        self.diff = {}

    def answer(self, word_id, uw):
        d = self.diff.setdefault(word_id, self.rng.random())
        tc = (uw.times_correct if uw else 0) or 0
        p = min(0.97, 0.85 - 0.35 * d + 0.06 * min(tc, 3))
        return self.rng.random() < p


async def _uw(session, user, wid):
    return (await session.execute(select(UserWord).where(
        UserWord.user_id == user.id, UserWord.word_id == wid,
        UserWord.learning_lang == "de"))).scalar_one_or_none()


async def run_lesson(session, user, learner, log, day, lesson_no, length=15,
                     q_seconds=20):
    pair = pair_from_user(user)
    qsess = QuizSession(user_id=user.id, level=user.level, learning_lang="de",
                        native_lang="ru", total_questions=length, quiz_mode="level")
    session.add(qsess)
    await session.commit()
    used, recent, errors = [], [], []
    board_done = False
    for q in range(1, length + 1):
        if not board_done and q == board_slot(length):
            eligible = await pick_words(user, session, pair, size=BOARD_SIZE * 2, exclude_ids=used)
            if should_insert_board(user, length, len(eligible)):
                board_done = True
                bwords = await pick_words(user, session, pair, exclude_ids=used)
                for w in bwords:
                    await _record(session, user, learner, log, qsess, w.id, "m", day, lesson_no, q, "board", errors)
                    used.append(w.id)
                await shift(session, timedelta(seconds=q_seconds * 2))
                continue
        question = await qs.generate_question(
            session, user, exclude_ids=used, pair=pair, recent_channels=recent,
            round_length=length, question_number=q)
        if question is None:
            log.append(dict(day=day, lesson=lesson_no, q=q, word=None, kind="NONE"))
            break
        w = question["correct_word"]
        ch = question["channel"]
        await _record(session, user, learner, log, qsess, w.id, ch.value, day, lesson_no, q, None, errors,
                      options=question["options"], cidx=question.get("correct_answer_index"), word=w)
        used.append(w.id)
        recent.append(ch.value)
        await shift(session, timedelta(seconds=q_seconds))
    return errors


async def _record(session, user, learner, log, qsess, wid, ch, day, lesson_no, q, src, errors,
                  options=None, cidx=None, word=None):
    uw = await _uw(session, user, wid)
    now = utcnow()
    if uw is None:
        kind = "new"
    elif qs._is_due(uw, now):
        kind = "due"
    else:
        kind = "early"
    prev = dict(streak=uw.correct_streak if uw else None,
                tc=uw.times_correct if uw else 0,
                learned=uw.learned if uw else None)
    ok = learner.answer(wid, uw)
    log.append(dict(day=day, lesson=lesson_no, q=q, word=wid, ch=ch, kind=kind, src=src,
                    ok=ok, options=options, cidx=cidx, **prev))
    session.add(QuizQuestion(session_id=qsess.id, word_id=wid, is_correct=ok,
                             answered_at=utcnow(), channel=ch))
    await session.commit()
    await qs.update_word_progress(user.id, wid, ok, session, "de",
                                  channel=QuizChannel(ch) if ch != "m" else QuizChannel.TEXT)
    if not ok:
        errors.append(wid)


async def setup_user(session, user, mode=QuizMode.LEVEL, category=None, channels="tasr"):
    user.level = CEFRLevel.A1
    user.quiz_mode = mode
    user.quiz_category = category
    user.quiz_word_count = 15
    user.audio_enabled = True
    user.quiz_channels = channels
    user.quizzes_passed = 5
    await session.commit()


async def simulate(session, user, days=7, lessons_per_day=2, seed_=7, gap_between=60):
    learner = Learner(random.Random(seed_))
    log = []
    n = 0
    for day in range(days):
        for k in range(lessons_per_day):
            n += 1
            await run_lesson(session, user, learner, log, day, n)
            await shift(session, timedelta(seconds=gap_between))
        # остаток суток
        await shift(session, timedelta(hours=24) - timedelta(seconds=(15 * 20 + gap_between) * lessons_per_day))
    return log


def report(log, title):
    shown = [r for r in log if r.get("word")]
    lessons = collections.defaultdict(list)
    for r in shown:
        lessons[r["lesson"]].append(r)
    dup_in_lesson = sum(len(v) - len(set(x["word"] for x in v)) for v in lessons.values())
    kinds = collections.Counter((r["kind"], r["src"] or "q") for r in shown)
    per_word = collections.Counter(r["word"] for r in shown)
    per_word_day = collections.Counter((r["word"], r["day"]) for r in shown)
    dist = collections.Counter(per_word.values())
    dist_day = collections.Counter(per_word_day.values())
    # пересечение соседних занятий
    keys = sorted(lessons)
    overlaps = []
    for a, b in zip(keys, keys[1:]):
        sa = set(x["word"] for x in lessons[a])
        sb = set(x["word"] for x in lessons[b])
        overlaps.append(len(sa & sb) / max(1, len(sb)))
    early_prev_ok = sum(1 for r in shown if r["kind"] == "early")
    print(f"\n===== {title} =====")
    print(f"показов {len(shown)}, слов {len(per_word)}, занятий {len(lessons)}, "
          f"обрывов {sum(1 for r in log if r.get('kind') == 'NONE')}")
    print(f"дублей внутри занятия: {dup_in_lesson}")
    print(f"виды показа: {dict(kinds)}")
    print(f"доля 'досрочных' (не новое и не по сроку): {early_prev_ok / len(shown):.1%}")
    print(f"каналы: {dict(collections.Counter(r['ch'] for r in shown))}")
    print(f"показов слова за весь срок -> слов: {dict(sorted(dist.items()))}")
    print(f"показов слова за один день -> (слово,день): {dict(sorted(dist_day.items()))}")
    print(f"пересечение соседних занятий (доля слов занятия, бывших в предыдущем): "
          f"среднее {sum(overlaps) / max(1, len(overlaps)):.1%}, макс {max(overlaps or [0]):.1%}")
    per_lesson_new = [sum(1 for x in lessons[k] if x["kind"] == "new") for k in keys]
    per_lesson_due = [sum(1 for x in lessons[k] if x["kind"] == "due") for k in keys]
    per_lesson_early = [sum(1 for x in lessons[k] if x["kind"] == "early") for k in keys]
    print(f"по занятиям new: {per_lesson_new}")
    print(f"по занятиям due: {per_lesson_due}")
    print(f"по занятиям early: {per_lesson_early}")
    return dict(shown=shown, per_word=per_word, per_word_day=per_word_day, dup=dup_in_lesson)


async def test_sim_level_2_per_day(session, user):
    await seed(session)
    await setup_user(session, user)
    log = await simulate(session, user, days=7, lessons_per_day=2)
    r = report(log, "A1 по уровню, 2 занятия подряд в день, 7 дней")
    assert r["dup"] == 0


async def test_sim_level_5_per_day(session, user):
    await seed(session)
    await setup_user(session, user)
    log = await simulate(session, user, days=7, lessons_per_day=5)
    report(log, "A1 по уровню, 5 занятий подряд в день, 7 дней")


async def test_sim_level_1_per_day(session, user):
    await seed(session)
    await setup_user(session, user)
    log = await simulate(session, user, days=7, lessons_per_day=1)
    report(log, "A1 по уровню, 1 занятие в день, 7 дней")


def breakdown(log):
    shown = [r for r in log if r.get("word")]
    print("due по серии до показа:", dict(collections.Counter(
        r["streak"] for r in shown if r["kind"] == "due")))
    print("early по (серия, источник, канал):", dict(collections.Counter(
        (r["streak"], r["src"] or "q", r["ch"]) for r in shown if r["kind"] == "early")))
    # судьба слова, верно отвеченного с первого раза: когда вернулось
    first_ok = {}
    for r in shown:
        if r["kind"] == "new" and r["ok"]:
            first_ok[r["word"]] = r["day"]
    back = collections.Counter()
    for r in shown:
        w = r["word"]
        if w in first_ok and r["kind"] != "new":
            back[(r["day"] - first_ok[w], r["kind"], r["src"] or r["ch"])] += 1
    print(f"верно с первого раза: {len(first_ok)} слов; их возвраты (через дней, вид, игра):",
          dict(sorted(back.items())))
    timelines = collections.defaultdict(list)
    for r in shown:
        timelines[r["word"]].append(f"d{r['day']}:{r['ch']}{'+' if r['ok'] else '-'}({r['kind'][0]},s{r['streak']})")
    for w, t in list(timelines.items())[:12]:
        print(w, " ".join(t))


async def test_sim_trace_1_per_day(session, user):
    await seed(session)
    await setup_user(session, user)
    log = await simulate(session, user, days=7, lessons_per_day=1)
    report(log, "ТРАССА: 1 занятие в день")
    breakdown(log)


async def test_sim_trace_2_per_day_no_board(session, user):
    await seed(session)
    await setup_user(session, user)
    user.match_in_round = False
    await session.commit()
    log = await simulate(session, user, days=7, lessons_per_day=2)
    report(log, "ТРАССА: 2 занятия в день, без доски")
    breakdown(log)
