"""
Награда за подтверждённую жалобу: язык, видимость, одно число.

ЗАЧЕМ. Владелец спросил прямо: можно ли на каждую игру сделать репорт и
«получить достойную награду в виде балов». Отправка жалобы работала и
проверена; НАГРАЖДЕНИЕ — нет, и в нём нашлось три беды разного рода.

    язык       `monthly_stats` ведётся отдельно по языкам (user + сезон +
               язык), а подтверждение искало ряд только по user и сезону:
               у двуязычного `scalar_one_or_none()` ПАДАЛ, а новый ряд
               создавался с языком по умолчанию «de» — балл за польскую
               ошибку ложился туда, где человека в рейтинге нет
    видимость  автору не сообщалось НИЧЕГО, хотя бот обещает «если
               подтвердится — получишь баллы». Обещание выполнялось
               технически и не выполнялось по существу
    число      «+1 балл» был вписан в семи местах: один раз числом в коде
               и шесть раз словами в локалях
"""

from sqlalchemy import select

from app.bot.handlers.admin import REPORT_REWARD_POINTS, admin_report_approve
from app.database.enums import CEFRLevel
from app.database.models import (
    MonthlySeason, MonthlyStats, QuizSession, TranslationReport, User,
)
from app.locales import get_text
from app.services.monthly_leaderboard_service import get_or_create_current_season
from tests.conftest import make_word
from tests.scenario import make_bot, press

# Пометки `pytestmark = pytest.mark.asyncio` здесь НЕТ нарочно: в pytest.ini
# стоит `asyncio_mode = auto`, и она не нужна, а внизу файла лежат
# синхронные проверки про одно число — на них пометка даёт предупреждение.
# То же замечание уже записано в `tests/test_quiz_flow.py`.

ADMIN_ID = 1  # совпадает с ADMIN_USER из conftest


async def _word(session):
    word = make_word("Entwurf", level=CEFRLevel.A1, ru="черновик")
    session.add(word)
    await session.commit()
    return word


async def _report(session, user, word, *, kind="text", quiz=None):
    report = TranslationReport(
        user_id=user.id, word_id=word.id, kind=kind, status="pending",
        quiz_session_id=quiz.id if quiz else None,
    )
    session.add(report)
    await session.commit()
    return report


async def _approve(session, word, *, admin_id=ADMIN_ID):
    """Нажать «подтвердить» в админ-панели, как это делает живой админ."""
    bot, recorder = make_bot()
    update = press(admin_id, f"admin:report_approve_{word.id}")
    callback = update.callback_query.as_(bot)
    await admin_report_approve(callback, session)
    return recorder


# ============================================================================
# ЯЗЫК
# ============================================================================

async def test_points_land_in_the_row_of_the_language_studied(session, user):
    """
    Жалоба из занятия по английскому — балл в английский ряд.

    Прежде новый ряд создавался с «de» по умолчанию, и балл оказывался в
    чужом зачёте: в рейтинге по английскому его не видно.
    """
    season = await get_or_create_current_season(session)
    word = await _word(session)

    quiz = QuizSession(
        user_id=user.id, level=CEFRLevel.A1, learning_lang="en",
        native_lang="ru", total_questions=5, answered_questions=5,
        correct_answers=5, quiz_mode="level",
    )
    session.add(quiz)
    await session.commit()
    await _report(session, user, word, quiz=quiz)

    await _approve(session, word)

    rows = (await session.execute(
        select(MonthlyStats).where(
            MonthlyStats.user_id == user.id,
            MonthlyStats.season_id == season.id,
        )
    )).scalars().all()

    assert len(rows) == 1, f"рядов статистики {len(rows)}, а должен один"
    assert rows[0].learning_lang == "en", (
        f"балл лёг в ряд языка «{rows[0].learning_lang}» вместо «en»"
    )
    assert rows[0].report_bonus == REPORT_REWARD_POINTS


async def test_approval_survives_a_user_with_two_languages(session, user):
    """
    У человека два языка в сезоне — подтверждение обязано пройти.

    Прежний запрос брал ряд без языка и падал `MultipleResultsFound` прямо
    под рукой админа. Жалобы остались бы висеть в «ожидании», и причина
    была бы не видна ни из бота, ни из панели.
    """
    season = await get_or_create_current_season(session)
    word = await _word(session)

    for lang in ("de", "en"):
        session.add(MonthlyStats(
            user_id=user.id, season_id=season.id, learning_lang=lang,
            total_correct=10, total_questions=10, monthly_quizzes=1,
        ))
    await session.commit()

    quiz = QuizSession(
        user_id=user.id, level=CEFRLevel.A1, learning_lang="en",
        native_lang="ru", total_questions=5, answered_questions=5,
        correct_answers=5, quiz_mode="level",
    )
    session.add(quiz)
    await session.commit()
    report = await _report(session, user, word, quiz=quiz)

    await _approve(session, word)

    await session.refresh(report)
    assert report.status == "fixed", "подтверждение не прошло"

    en_row = (await session.execute(
        select(MonthlyStats).where(
            MonthlyStats.user_id == user.id,
            MonthlyStats.season_id == season.id,
            MonthlyStats.learning_lang == "en",
        )
    )).scalar_one()
    de_row = (await session.execute(
        select(MonthlyStats).where(
            MonthlyStats.user_id == user.id,
            MonthlyStats.season_id == season.id,
            MonthlyStats.learning_lang == "de",
        )
    )).scalar_one()

    assert en_row.report_bonus == REPORT_REWARD_POINTS
    assert (de_row.report_bonus or 0) == 0, "балл попал и в чужой язык"


async def test_language_falls_back_to_the_users_current_one(session, user):
    """
    Занятие не сохранилось — берём текущий язык человека, а не «de».
    """
    season = await get_or_create_current_season(session)
    word = await _word(session)
    user.learning_lang = "pl"
    await session.commit()

    await _report(session, user, word)          # без quiz_session_id
    await _approve(session, word)

    row = (await session.execute(
        select(MonthlyStats).where(MonthlyStats.season_id == season.id)
    )).scalar_one()
    assert row.learning_lang == "pl"


# ============================================================================
# ВИДИМОСТЬ
# ============================================================================

async def test_the_reporter_is_told_about_the_approval(session, user):
    """
    Невидимая награда — не награда. Бот обещает баллы при отправке, значит
    обязан сказать, когда начислил.
    """
    word = await _word(session)
    await _report(session, user, word)

    recorder = await _approve(session, word)

    sent = [
        payload for name, payload in recorder.calls
        if name == "SendMessage" and payload.get("chat_id") == user.id
    ]
    assert sent, "автору жалобы не сказали ничего"
    assert str(REPORT_REWARD_POINTS) in (sent[0].get("text") or ""), (
        f"в извещении нет числа баллов: {sent[0].get('text')!r}"
    )


async def test_an_audio_report_gets_its_own_wording(session, user):
    """
    Жалоба на произношение и на перевод — разные вещи, и сообщение разное:
    в первом случае обещана ПЕРЕЗАПИСЬ, а не правка словаря.
    """
    word = await _word(session)
    await _report(session, user, word, kind="audio")

    recorder = await _approve(session, word)

    texts = [
        payload.get("text") or ""
        for name, payload in recorder.calls
        if name == "SendMessage" and payload.get("chat_id") == user.id
    ]
    assert texts, "автору жалобы на произношение не сказали ничего"
    expected = get_text(
        "report_approved_audio", user.interface_language,
        word="Entwurf", points=REPORT_REWARD_POINTS,
    )
    assert texts[0] == expected


async def test_a_closed_bot_does_not_break_the_approval(session, user):
    """
    Человек заблокировал бота — жалоба от этого хуже не стала, и
    подтверждение обязано пройти до конца.
    """
    word = await _word(session)
    report = await _report(session, user, word)

    bot, _ = make_bot()

    async def refuse(*args, **kwargs):
        raise RuntimeError("bot was blocked by the user")

    bot.send_message = refuse
    callback = press(ADMIN_ID, f"admin:report_approve_{word.id}").callback_query.as_(bot)
    await admin_report_approve(callback, session)

    await session.refresh(report)
    assert report.status == "fixed", "отказ доставки сорвал подтверждение"


# ============================================================================
# ОДИН БАЛЛ ЧЕЛОВЕКУ ЗА СЛОВО, РЕШЕНИЕ ПО ВИДУ
#
# Аудит 14 октября: человек, пожаловавшийся на перевод и на звук одного
# слова, получал за одно нажатие админа 10 баллов вместо 5 и два
# поздравления, а принятие перевода стирало озвучку — кнопка была одна на
# слово и решала оба вида разом.
# ============================================================================

async def _press_approve(session, data):
    bot, recorder = make_bot()
    callback = press(ADMIN_ID, data).callback_query.as_(bot)
    await admin_report_approve(callback, session)
    return recorder


def _told(recorder, user_id):
    return [payload.get("text") or "" for name, payload in recorder.calls
            if name == "SendMessage" and payload.get("chat_id") == user_id]


async def _bonus(session, user_id) -> int:
    rows = (await session.execute(
        select(MonthlyStats.report_bonus).where(MonthlyStats.user_id == user_id)
    )).scalars().all()
    return sum(r or 0 for r in rows)


async def test_two_kinds_of_one_word_pay_one_point(session, user):
    """Прежняя кнопка решает оба вида — и всё равно балл один, поздравление одно."""
    word = await _word(session)
    await _report(session, user, word, kind="text")
    await _report(session, user, word, kind="audio")

    recorder = await _approve(session, word)

    assert await _bonus(session, user.id) == REPORT_REWARD_POINTS, (
        "за два вида жалобы на одно слово начислено дважды"
    )
    assert len(_told(recorder, user.id)) == 1, "поздравлений больше одного"
    alert = next(a for a in recorder.alerts() if a)
    assert "1 человек" in alert, f"окно считает жалобы, а не людей: {alert!r}"


async def test_accepting_the_translation_leaves_the_audio_report_open(session, user):
    """Принять перевод — не значит принять звук: жалоба на звук ждёт своего решения."""
    word = await _word(session)
    text_report = await _report(session, user, word, kind="text")
    audio_report = await _report(session, user, word, kind="audio")

    await _press_approve(session, f"admin:report_approve_text_{word.id}")

    await session.refresh(text_report)
    await session.refresh(audio_report)
    assert text_report.status == "fixed"
    assert audio_report.status == "pending", "жалобу на звук решили вместе с переводом"


async def test_the_second_kind_accepted_later_pays_nothing(session, user):
    """Балл — за слово, а не за нажатие: второй вид, принятый позже, его не удваивает."""
    word = await _word(session)
    await _report(session, user, word, kind="text")
    await _report(session, user, word, kind="audio")

    await _press_approve(session, f"admin:report_approve_text_{word.id}")
    second = await _press_approve(session, f"admin:report_approve_audio_{word.id}")

    assert await _bonus(session, user.id) == REPORT_REWARD_POINTS
    assert not _told(second, user.id), "второе поздравление за то же слово"


async def test_a_repeated_press_pays_nothing(session, user):
    """Второе нажатие той же кнопки ничего не находит и ничего не начисляет."""
    word = await _word(session)
    await _report(session, user, word)

    await _press_approve(session, f"admin:report_approve_text_{word.id}")
    second = await _press_approve(session, f"admin:report_approve_text_{word.id}")

    assert await _bonus(session, user.id) == REPORT_REWARD_POINTS
    assert any("нечего" in a.lower() for a in second.alerts()), second.alerts()


async def test_the_reporter_sees_the_word_he_was_learning(session, user):
    """
    Учил английский — в извещении английское слово, а не немецкое.

    Прежде там всегда стояло `word_de`: ученик английского, пожаловавшийся
    на «from, starting from, off», читал «жалоба принята: ab».
    """
    word = make_word("Entwurf", level=CEFRLevel.A1, ru="черновик", en="draft")
    session.add(word)
    await session.commit()
    quiz = QuizSession(
        user_id=user.id, level=CEFRLevel.A1, learning_lang="en",
        native_lang="ru", total_questions=5, answered_questions=5,
        correct_answers=5, quiz_mode="level",
    )
    session.add(quiz)
    await session.commit()
    await _report(session, user, word, quiz=quiz)

    recorder = await _approve(session, word)

    text = _told(recorder, user.id)[0]
    assert "raft" in text, f"слова на изучаемом языке нет: {text!r}"
    assert "Entwurf" not in text, f"ученику английского показали немецкое: {text!r}"


# ============================================================================
# ОДНО ЧИСЛО
# ============================================================================

def test_the_promised_number_comes_from_the_same_place_as_the_payout():
    """
    Обещание при отправке и начисление при подтверждении — одно число.

    Прежде «+1 балл» стоял в семи местах: числом в коде и словами в шести
    локалях. Правка цены соврала бы человеку в лицо.
    """
    from app.bot.handlers.quiz.report import (
        REPORT_REWARD_POINTS as promised,
    )

    assert promised == REPORT_REWARD_POINTS == MonthlyStats.POINTS_PER_REPORT


def test_no_locale_promises_a_number_of_its_own():
    """
    Ни в одной локали не должно остаться вписанного числа баллов.
    """
    import re

    from app.locales import LOCALES

    for lang, texts in LOCALES.items():
        for key in ("report_sent", "report_sent_audio",
                    "report_approved", "report_approved_audio"):
            value = texts.get(key)
            if not value:
                continue
            assert "{points}" in value, (
                f"{lang}.{key} не берёт число из кода: {value!r}"
            )
            # Цифра рядом с плюсом — признак вписанного числа
            assert not re.search(r"\+\s*\d", value), (
                f"{lang}.{key} обещает своё число: {value!r}"
            )


def test_a_report_is_worth_more_than_a_learned_word():
    """
    «Достойная награда» — решение владельца, и вот его числовой смысл.

    14 октября владелец поднял цену: «подтверждённый репорт я считаю должно
    быть 15 а то и 20. Чем больше помогают и это подтверждают — больше
    пользы боту = выше награда». Жалоба дороже выученного слова и не
    дешевле занятия.
    """
    assert MonthlyStats.POINTS_PER_REPORT > MonthlyStats.POINTS_PER_WORD
    assert MonthlyStats.POINTS_PER_REPORT >= MonthlyStats.POINTS_PER_ROUND


# ============================================================================
# ПЛАТИМ ЗА КАЖДУЮ ПОДТВЕРЖДЁННУЮ — потолка нет
# ============================================================================

async def test_every_confirmed_report_is_paid(session, user):
    """
    Владелец: «мы платим всегда, если реально репорт подтверждает, что
    ошибка была! Абуз — это нельзя чтобы на 1 слово несколько раз
    присылали». Месячный потолок в десять жалоб был — и снят.
    """
    words = []
    for i in range(12):
        word = make_word(f"Entwurf{i}", level=CEFRLevel.A1, ru=f"черновик{i}")
        session.add(word)
        words.append(word)
    await session.commit()

    for word in words:
        await _report(session, user, word)
        recorder = await _approve(session, word)
        assert len(_told(recorder, user.id)) == 1

    assert await _bonus(session, user.id) == len(words) * REPORT_REWARD_POINTS, (
        "подтверждённая жалоба осталась без баллов"
    )


async def test_one_word_pays_once_however_often_it_is_reported(session, user):
    """Антиабуз по слову: за одно слово человеку платят один раз."""
    word = await _word(session)
    await _report(session, user, word, kind="text")
    await _press_approve(session, f"admin:report_approve_text_{word.id}")
    await _report(session, user, word, kind="audio")
    await _press_approve(session, f"admin:report_approve_audio_{word.id}")

    assert await _bonus(session, user.id) == REPORT_REWARD_POINTS, (
        "за одно слово заплачено дважды"
    )
