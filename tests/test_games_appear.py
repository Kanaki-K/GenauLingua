"""
Все игры круга ВИДНЫ человеку, а не только существуют в коде.

ЗАЧЕМ. Живой тест владельца 14 октября: 101 ответ за день — 91 карточка и
10 пар доски, ни одного «Вспоминаю», «Слушаю», «Говорю». «Ниразу не было
режима реверса. Ниразу не предложило мне голосовое записать… юзер зашёл,
ожидает одно, играет в другое».

Код игр работал, приёмки были зелёными — они навязывали канал сами
(`channel=`), а живой подбор до других игр не доходил: игры открываются по
слову, а слово возвращалось только назавтра. Эти тесты проверяют именно
живой подбор, без навязывания.
"""

from datetime import timedelta

from sqlalchemy import select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import UserWord, Word
from app.services.quiz_service import generate_question
from tests.conftest import build_groups, make_word


async def _ready(session, user, *, correct=1, speech_shown=0, seen_ago=timedelta(minutes=30)):
    for i in range(80):
        session.add(make_word(f"Haus{i:02d}", level=CEFRLevel.A1, ru=f"дом{i:02d}"))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = 15
    user.audio_enabled = True
    user.quiz_channels = "tasr"
    await session.commit()

    # Сорок слов узнаны сегодня карточкой: одному верному ответу полчаса
    words = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    for word in words[:40]:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            times_shown=correct, times_correct=correct, correct_streak=1,
            shown_speech=speech_shown, learned=False,
            last_seen_at=utcnow() - seen_ago,
        ))
    await session.commit()


async def _round(session, user, prefer=None) -> list[str]:
    used, recent = [], []
    for _ in range(15):
        q = await generate_question(
            session, user, exclude_ids=used, recent_channels=recent,
            prefer_channel=prefer,
        )
        assert q is not None
        used.append(q["correct_word"].id)
        recent.append(q["channel"].value)
    return recent


async def test_words_met_today_come_back_as_other_games(session, user):
    await _ready(session, user)
    channels = await _round(session, user)

    assert channels[0] == "t", "круг открывается карточкой"
    assert {"r", "a"} & set(channels), (
        f"слова, узнанные сегодня, не вернулись другой игрой: {''.join(channels)}"
    )


async def test_a_round_still_brings_new_words(session, user):
    """Отработка — каждое второе место, а не весь круг: за открытием приходят."""
    await _ready(session, user)
    channels = await _round(session, user)
    assert channels.count("t") >= 6, "новых слов в круге почти не осталось"


async def test_a_word_ready_to_speak_gets_spoken(session, user):
    """Лесенка: два верных и ни разу не произнесено — вперёд, и речью."""
    await _ready(session, user, correct=2)
    channels = await _round(session, user)
    assert "s" in channels, f"речь не наступила: {''.join(channels)}"


async def test_the_speak_button_gives_speech(session, user):
    """Нажал 🎤 — получил речь, а не карточку, если слова к ней готовы."""
    await _ready(session, user, correct=2)
    channels = await _round(session, user, prefer=QuizChannel.SPEECH)
    assert channels[:5] == ["s"] * 5, f"кнопка «Говорю» дала: {''.join(channels)}"


async def test_the_recall_button_gives_recall(session, user):
    await _ready(session, user)
    channels = await _round(session, user, prefer=QuizChannel.REVERSE)
    assert channels.count("r") >= 10, f"кнопка «Вспоминаю» дала: {''.join(channels)}"
