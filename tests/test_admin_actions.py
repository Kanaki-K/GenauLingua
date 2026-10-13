"""
Админские ДЕЙСТВИЯ: отклонение жалобы и рассылка.

ЗАЧЕМ ОТДЕЛЬНО ОТ ОСТАЛЬНОГО. `audit_admin` вызывает каждый раздел на
живых данных — но два действия вызывать не может по существу: отклонение
меняет данные, а рассылка уходит всем 233 людям без подтверждения. Значит
их не проверял НИКТО: ни приёмка, ни тесты. Награду за подтверждённую
жалобу держат девять проверок (`test_report_reward.py`), а у отклонения не
было ни одной.

Рассылка при этом — самое опасное действие в боте, и в ней уже был дефект
ровно того рода, который виден только на всех получателях сразу: бот шлёт
с `parse_mode=HTML`, любой символ `<` в тексте Telegram считает началом
тега и отклоняет сообщение — ДЛЯ КАЖДОГО получателя. В логах это выглядело
как «Ошибок: 232» без объяснения причины.

Здесь поддельна только сеть: обработчики настоящие, сессия настоящая.
"""

from sqlalchemy import select

from app.bot.handlers import admin
from app.bot.handlers.admin import (
    admin_report_approve, admin_report_reject, broadcast_cancel,
    broadcast_confirm, broadcast_message,
)
from app.database.enums import CEFRLevel
from app.database.models import MonthlyStats, TranslationReport, User
from app.services.monthly_leaderboard_service import get_or_create_current_season
from tests.conftest import make_word
from tests.scenario import make_bot, press, text_update

ADMIN_ID = 1       # совпадает с ADMIN_USER из conftest
OUTSIDER_ID = 777  # не админ


async def _word(session, name="Entwurf"):
    word = make_word(name, level=CEFRLevel.A1, ru="черновик")
    session.add(word)
    await session.commit()
    return word


async def _report(session, user, word, *, kind="text"):
    report = TranslationReport(
        user_id=user.id, word_id=word.id, kind=kind, status="pending",
    )
    session.add(report)
    await session.commit()
    return report


async def _press(handler, session, data, *, uid=ADMIN_ID, with_session=True):
    """
    Нажать кнопку админки напрямую, минуя диспетчер.

    СООБЩЕНИЕ ТОЖЕ ПРИВЯЗЫВАЕТСЯ К БОТУ. Без этого `callback.message.
    edit_text` падает с «method is not mounted to any bot instance» — и
    незаметно это только у подтверждения жалобы, где правка обёрнута в
    try/except. Отмена и запуск рассылки правят экран без обёртки.
    """
    bot, recorder = make_bot()
    callback = press(uid, data).callback_query.as_(bot)
    callback.message.as_(bot)
    if with_session:
        await handler(callback, session)
    else:
        await handler(callback)
    return callback, recorder


# ============================================================================
# ОТКЛОНЕНИЕ ЖАЛОБЫ
# ============================================================================

async def test_rejecting_closes_the_report(session, user):
    word = await _word(session)
    await _report(session, user, word)

    await _press(admin_report_reject, session, f"admin:report_reject_{word.id}")

    statuses = (await session.execute(
        select(TranslationReport.status)
        .where(TranslationReport.word_id == word.id)
    )).scalars().all()
    assert statuses == ["rejected"], statuses


async def test_rejecting_pays_nothing(session, user):
    """
    Главное свойство отклонения: баллов НЕТ. Подтверждение начисляет пять,
    и спутать эти пути нельзя — иначе любая жалоба становится бесплатным
    баллом, и жаловаться выгодно не разобравшись.
    """
    await get_or_create_current_season(session)
    word = await _word(session)
    await _report(session, user, word)

    await _press(admin_report_reject, session, f"admin:report_reject_{word.id}")

    rows = (await session.execute(
        select(MonthlyStats).where(MonthlyStats.user_id == user.id)
    )).scalars().all()
    assert all((row.report_bonus or 0) == 0 for row in rows), (
        "за отклонённую жалобу начислены баллы"
    )


async def test_rejecting_tells_nobody(session, user):
    """
    Автору отклонённой жалобы ничего не шлётся. Подтверждение, наоборот,
    извещает — и это тоже проверено, в `test_report_reward.py`.

    Смотреть надо на ПОЛУЧАТЕЛЕЙ, а не на тексты: после решения обработчик
    перерисовывает собственный экран админки правкой, и первая редакция
    теста приняла эту правку за письмо автору.
    """
    word = await _word(session)
    await _report(session, user, word)

    _, recorder = await _press(
        admin_report_reject, session, f"admin:report_reject_{word.id}"
    )
    assert user.id not in recorder.sent_to(), (
        f"автору ушло сообщение об отклонении: {recorder.sent_to()}"
    )


async def test_rejecting_closes_every_report_on_the_word(session, user):
    """
    Жалоб на одно слово может быть много — закрываются ВСЕ. Иначе слово
    остаётся в очереди и всплывает снова, уже разобранным.
    """
    word = await _word(session)
    second = User(id=4242, first_name="Второй", interface_language="ru",
                  learning_lang="de", native_lang="ru", reverse_mode=False)
    session.add(second)
    await session.commit()

    await _report(session, user, word)
    await _report(session, second, word)
    await _report(session, user, word, kind="audio")

    await _press(admin_report_reject, session, f"admin:report_reject_{word.id}")

    pending = (await session.execute(
        select(TranslationReport)
        .where(TranslationReport.word_id == word.id,
               TranslationReport.status == "pending")
    )).scalars().all()
    assert not pending, f"осталось нерешённых: {len(pending)}"


async def test_rejecting_nothing_says_so(session, user):
    """Нажатие по уже разобранному слову не должно падать."""
    word = await _word(session)

    _, recorder = await _press(
        admin_report_reject, session, f"admin:report_reject_{word.id}"
    )
    assert recorder.alerts(), "ответа на нажатие не было"
    assert "нечего" in recorder.alerts()[0].lower(), recorder.alerts()


async def test_an_outsider_cannot_reject(session, user):
    word = await _word(session)
    await _report(session, user, word)

    await _press(admin_report_reject, session,
                 f"admin:report_reject_{word.id}", uid=OUTSIDER_ID)

    statuses = (await session.execute(
        select(TranslationReport.status)
        .where(TranslationReport.word_id == word.id)
    )).scalars().all()
    assert statuses == ["pending"], f"чужой закрыл жалобу: {statuses}"


async def test_an_outsider_cannot_approve(session, user):
    """Та же дверь с другой стороны: чужой не должен раздавать баллы."""
    word = await _word(session)
    await _report(session, user, word)

    await _press(admin_report_approve, session,
                 f"admin:report_approve_{word.id}", uid=OUTSIDER_ID)

    statuses = (await session.execute(
        select(TranslationReport.status)
        .where(TranslationReport.word_id == word.id)
    )).scalars().all()
    assert statuses == ["pending"], f"чужой подтвердил жалобу: {statuses}"


# ============================================================================
# РАССЫЛКА
# ============================================================================

async def _broadcast(session, text, *, uid=ADMIN_ID):
    bot, recorder = make_bot()
    message = text_update(uid, text).message.as_(bot)
    await broadcast_message(message, session)
    return recorder


async def test_broadcast_without_text_shows_how_to_use_it(session, user):
    recorder = await _broadcast(session, "/broadcast")
    assert recorder.sent_texts(), "бот промолчал"
    assert "/broadcast" in recorder.last_text()


async def test_broadcast_previews_to_the_admin_only(session, user):
    """
    Предпросмотр уходит САМОМУ админу тем же вызовом, каким пойдёт
    рассылка, и никому больше. На этом ловится разметка: иначе сообщение
    отклонится у каждого получателя по очереди.
    """
    admin._PENDING_BROADCASTS.clear()
    recorder = await _broadcast(session, "/broadcast Привет всем")

    everything = "\n".join(recorder.sent_texts())
    assert "Привет всем" in everything, "предпросмотра не было"
    assert "Рассылка" in everything, "нет экрана подтверждения"
    assert ADMIN_ID in admin._PENDING_BROADCASTS, "текст не запомнен"


async def test_broadcast_is_not_sent_until_confirmed(session, user):
    """
    Между набором и отправкой стоит подтверждение. Без него любая опечатка
    в команде уходит всем немедленно.
    """
    admin._PENDING_BROADCASTS.clear()
    recorder = await _broadcast(session, "/broadcast Проверка")

    # Получатель один — сам админ, и это предпросмотр
    assert recorder.sent_to() == [ADMIN_ID] or set(recorder.sent_to()) <= {ADMIN_ID}, (
        f"до подтверждения сообщение ушло кому-то ещё: {recorder.sent_to()}"
    )


async def test_cancelling_forgets_the_text(session, user):
    admin._PENDING_BROADCASTS[ADMIN_ID] = "черновик"

    await _press(broadcast_cancel, session, "admin:broadcast_cancel",
                 with_session=False)

    assert ADMIN_ID not in admin._PENDING_BROADCASTS, "черновик остался"


async def test_confirming_sends_to_everyone(session, user):
    """
    Подтверждение рассылает всем. Получателей считаем по базе, а не по
    обещанию экрана.
    """
    extra = User(id=5151, first_name="Ещё один", interface_language="ru",
                 learning_lang="de", native_lang="ru", reverse_mode=False)
    session.add(extra)
    await session.commit()

    admin._PENDING_BROADCASTS[ADMIN_ID] = "Всем привет"
    _, recorder = await _press(
        broadcast_confirm, session, "admin:broadcast_confirm"
    )

    everyone = set((await session.execute(select(User.id))).scalars().all())
    reached = set(recorder.sent_to())
    assert everyone <= reached, f"не дошло до {sorted(everyone - reached)}"
    assert ADMIN_ID not in admin._PENDING_BROADCASTS, "черновик не очищен"


async def test_confirming_without_a_draft_does_not_send(session, user):
    """
    После перезапуска бота черновик теряется НАРОЧНО: неотправленный текст
    лучше потерять, чем отправить неожиданно. Кнопка в такой переписке
    остаётся жить — и не должна рассылать пустоту.
    """
    admin._PENDING_BROADCASTS.clear()
    _, recorder = await _press(
        broadcast_confirm, session, "admin:broadcast_confirm"
    )

    assert not recorder.sent_to(), f"ушло без текста: {recorder.sent_to()}"
    assert recorder.alerts(), "ответа на нажатие не было"
    assert "заново" in recorder.alerts()[0].lower(), recorder.alerts()


async def test_an_outsider_cannot_broadcast(session, user):
    admin._PENDING_BROADCASTS.clear()
    recorder = await _broadcast(session, "/broadcast Я не админ",
                                uid=OUTSIDER_ID)

    assert not recorder.sent_texts(), f"чужому ответили: {recorder.sent_texts()}"
    assert not admin._PENDING_BROADCASTS, "чужой текст запомнен"


async def test_an_outsider_cannot_confirm_someone_elses_broadcast(session, user):
    admin._PENDING_BROADCASTS[ADMIN_ID] = "текст админа"

    _, recorder = await _press(
        broadcast_confirm, session, "admin:broadcast_confirm", uid=OUTSIDER_ID
    )

    assert not recorder.sent_to(), "чужой запустил рассылку"
    assert admin._PENDING_BROADCASTS.get(ADMIN_ID) == "текст админа", (
        "чужой стёр черновик админа"
    )
