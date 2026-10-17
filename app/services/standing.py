"""
Положение человека в соревновании: слава, звание, корона, строка игрока.

Замысел — REWARDS.md §0 (владелец, 17.10). Коротко:
  * СЛАВА копится от медалей месяца и больших достижений, не тратится и не
    сгорает; из неё — ЗВАНИЕ, один знак у имени: 🌱 🌳 🌙 🪐 ☀️ 🌌 (верхний
    тайный). Знаки «понятные всем» — от земли до галактики;
  * 👑 КОРОНА — лучший в своём языке за прошлый месяц носит её весь этот
    месяц, потом её разыгрывают заново. Славы не даёт, но каждая записана:
    «👑 3 раза»;
  * СТРОКА ИГРОКА одна на таблицу и якорь: «🌙 Kostia 👑 🔥27».

Всё считается из уже записанных данных (`monthly_awards`, лучшая серия,
выученные слова, принятые жалобы) — новых колонок нет.
"""

import re
from dataclasses import dataclass, field
from typing import Iterable, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import (
    MonthlyAward, MonthlySeason, MonthlyStats, QuizSession, TranslationReport, User, UserWord,
)

# ---------------------------------------------------------------------------
# Правила
# ---------------------------------------------------------------------------

# Серия у имени — с трёх дней, ОДИН порог для таблицы и якоря: строка в
# якоре обязана быть той же, что в таблице
STREAK_FROM_DAYS = 3

# Медали месяца — только с этого числа занятий в зачёт (повтор ошибок не
# считается: `monthly_quizzes`). Иначе первого числа в 00:05 одно занятие
# давало бы место
MEDAL_MIN_QUIZZES = 3

# Корона языка — только если в языке столько участников с MEDAL_MIN_QUIZZES:
# иначе первопроходец редкого языка носил бы её бесплатно
CROWN_MIN_PEOPLE = 3

CROWN = "crown"
CROWN_MARK = "👑"

# Слава за медаль месяца. Корона — 0: она на месяц и в маленьком языке
# копилась бы слишком легко (владелец: «нечестно, если там всего 3 человека»)
AWARD_GLORY = {"gold": 5, "silver": 3, "bronze": 2, "top10": 1, CROWN: 0}

# Звания: (слава от, знак, ключ названия). Последнее — тайное: в справке
# и «до следующего» его не показываем
TITLES = (
    (1, "🌱", "title_sprout"),
    (5, "🌳", "title_tree"),
    (12, "🌙", "title_moon"),
    (22, "🪐", "title_planet"),
    (35, "☀️", "title_sun"),
    (55, "🌌", "title_galaxy"),
)
SECRET_TITLE = TITLES[-1]


@dataclass(frozen=True)
class Achievement:
    key: str          # ключ названия в локали: ach_<key>
    mark: str
    glory: int


# Коллекция. Порядок — порядок показа. Слава у малых вех 0: они для
# коллекции, а звание растёт от побед и больших дел
ACHIEVEMENTS = (
    Achievement("streak_7", "🔥", 0),
    Achievement("streak_30", "🔥", 1),
    Achievement("streak_100", "🔥", 3),
    Achievement("streak_365", "🔥", 5),
    Achievement("streak_1000", "🔥", 10),
    Achievement("words_100", "📚", 0),
    Achievement("words_1000", "📚", 2),
    Achievement("words_3000", "📚", 5),
    Achievement("perfect_10", "🎯", 0),
    Achievement("voice_1000", "🎤", 0),
    Achievement("editor", "✍️", 2),
    Achievement("polyglot", "🌍", 3),
)
STREAK_STEPS = {"streak_7": 7, "streak_30": 30, "streak_100": 100,
                "streak_365": 365, "streak_1000": 1000}
WORD_STEPS = {"words_100": 100, "words_1000": 1000, "words_3000": 3000}
EDITOR_REPORTS = 5
POLYGLOT_WORDS = 100
PERFECT_LESSONS = 10
VOICE_ANSWERS = 1000


@dataclass
class Standing:
    """Всё о человеке, что нужно таблице, якорю и карточкам."""
    user_id: int
    glory: int = 0
    medals: dict = field(default_factory=lambda: {"gold": 0, "silver": 0, "bronze": 0})
    crowns_total: int = 0
    crown_lang: Optional[str] = None       # корона, которую носит сейчас
    achievements: tuple = ()               # ключи открытых

    @property
    def title(self) -> Optional[tuple]:
        return title_for(self.glory)

    @property
    def title_mark(self) -> str:
        t = self.title
        return t[1] if t else ""


def title_for(glory: int) -> Optional[tuple]:
    reached = [t for t in TITLES if glory >= t[0]]
    return reached[-1] if reached else None


def next_title(glory: int) -> Optional[tuple]:
    """Следующая ступень — кроме тайной: её заранее не показываем."""
    for t in TITLES:
        if glory < t[0]:
            return None if t is SECRET_TITLE else t
    return None


# ---------------------------------------------------------------------------
# Вид
# ---------------------------------------------------------------------------

# Знаки, которые человек мог вписать в своё имя Telegram, чтобы выглядеть
# победителем: «👑 Оля», «Max 🔥99». Из имён в таблице и якоре их убираем —
# корону и серию показывает только бот
_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿"
    "️‍⃣\U000E0000-\U000E007F]+"
)
NAME_MAX = 12


def clean_name(name: str) -> str:
    """Первое слово имени, без эмодзи, не длиннее 12 знаков."""
    text = _EMOJI.sub("", name or "").strip()
    first = text.split()[0] if text.split() else ""
    if not first:
        return "…"
    if len(first) > NAME_MAX:
        return first[:NAME_MAX - 1] + "…"
    return first


def compact_number(n: int) -> str:
    """365 → «365», 1234 → «1.2k», 12000 → «12k»: серия не растягивает строку."""
    if n < 1000:
        return str(n)
    if n < 10000:
        whole, rest = divmod(n, 1000)
        tenth = rest // 100
        return f"{whole}.{tenth}k" if tenth else f"{whole}k"
    return f"{n // 1000}k"


def streak_mark(days: int) -> str:
    return f"🔥{compact_number(days)}" if days >= STREAK_FROM_DAYS else ""


def player_line(name: str, standing: Optional[Standing], streak_days: int) -> str:
    """«🌙 Kostia 👑 🔥27» — звание · имя · корона · серия; пустое не пишется."""
    parts = []
    if standing and standing.title_mark:
        parts.append(standing.title_mark)
    parts.append(name)
    if standing and standing.crown_lang:
        parts.append(CROWN_MARK)
    fire = streak_mark(streak_days)
    if fire:
        parts.append(fire)
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Расчёт
# ---------------------------------------------------------------------------

async def crown_season_id(session: AsyncSession) -> Optional[int]:
    """
    Сезон, чьи короны носят сейчас: последний закрытый.

    Корона за октябрь — на ноябрь. Если декабрь не закрыт, а уже январь,
    короны октября всё ещё на головах — до закрытия следующего сезона.
    """
    return (await session.execute(
        select(MonthlySeason.id)
        .where(MonthlySeason.winners_finalized.is_(True))
        .order_by(MonthlySeason.year.desc(), MonthlySeason.month.desc())
        .limit(1)
    )).scalar_one_or_none()


async def current_crowns(session: AsyncSession) -> dict[int, str]:
    """{user_id: язык} — кто носит корону сейчас."""
    season_id = await crown_season_id(session)
    if season_id is None:
        return {}
    rows = (await session.execute(
        select(MonthlyAward.user_id, MonthlyAward.learning_lang)
        .where(MonthlyAward.season_id == season_id, MonthlyAward.award_type == CROWN)
    )).all()
    return {uid: lang for uid, lang in rows}


async def crown_holders(session: AsyncSession, learning_lang: str) -> list[int]:
    """Кто носит корону этого языка сейчас (при равенстве — несколько)."""
    return [uid for uid, lang in (await current_crowns(session)).items() if lang == learning_lang]


async def standings(session: AsyncSession, users: Iterable[User]) -> dict[int, Standing]:
    """Положение каждого — несколькими запросами на всех сразу."""
    users = list(users)
    ids = [u.id for u in users]
    if not ids:
        return {}
    result = {uid: Standing(user_id=uid) for uid in ids}

    for uid, kind, count in (await session.execute(
        select(MonthlyAward.user_id, MonthlyAward.award_type, func.count())
        .where(MonthlyAward.user_id.in_(ids))
        .group_by(MonthlyAward.user_id, MonthlyAward.award_type)
    )).all():
        st = result[uid]
        st.glory += AWARD_GLORY.get(kind, 0) * count
        if kind in st.medals:
            st.medals[kind] += count
        if kind == CROWN:
            st.crowns_total += count

    crowns = await current_crowns(session)
    for uid in ids:
        result[uid].crown_lang = crowns.get(uid)

    learned: dict[int, dict[str, int]] = {}
    for uid, lang, count in (await session.execute(
        select(UserWord.user_id, UserWord.learning_lang, func.count())
        .where(UserWord.user_id.in_(ids), UserWord.learned.is_(True))
        .group_by(UserWord.user_id, UserWord.learning_lang)
    )).all():
        learned.setdefault(uid, {})[lang] = int(count)

    fixed = dict((await session.execute(
        select(TranslationReport.user_id, func.count(func.distinct(TranslationReport.word_id)))
        .where(TranslationReport.user_id.in_(ids), TranslationReport.status == "fixed")
        .group_by(TranslationReport.user_id)
    )).all())

    perfect = dict((await session.execute(
        select(QuizSession.user_id, func.count())
        .where(QuizSession.user_id.in_(ids), QuizSession.is_completed.is_(True),
               QuizSession.total_questions > 0,
               QuizSession.correct_answers >= QuizSession.total_questions)
        .group_by(QuizSession.user_id)
    )).all())

    voice = dict((await session.execute(
        select(MonthlyStats.user_id, func.sum(func.coalesce(MonthlyStats.correct_speech, 0)))
        .where(MonthlyStats.user_id.in_(ids))
        .group_by(MonthlyStats.user_id)
    )).all())

    for user in users:
        st = result[user.id]
        best = int(user.best_streak_days or 0)
        words = learned.get(user.id, {})
        open_keys = []
        for ach in ACHIEVEMENTS:
            if ach.key in STREAK_STEPS:
                ok = best >= STREAK_STEPS[ach.key]
            elif ach.key in WORD_STEPS:
                ok = sum(words.values()) >= WORD_STEPS[ach.key]
            elif ach.key == "editor":
                ok = int(fixed.get(user.id, 0)) >= EDITOR_REPORTS
            elif ach.key == "polyglot":
                ok = sum(1 for n in words.values() if n >= POLYGLOT_WORDS) >= 2
            elif ach.key == "perfect_10":
                ok = int(perfect.get(user.id, 0)) >= PERFECT_LESSONS
            elif ach.key == "voice_1000":
                ok = int(voice.get(user.id, 0) or 0) >= VOICE_ANSWERS
            else:
                ok = False
            if ok:
                open_keys.append(ach.key)
                st.glory += ach.glory
        st.achievements = tuple(open_keys)
    return result


async def standing_of(session: AsyncSession, user: User) -> Standing:
    return (await standings(session, [user]))[user.id]
