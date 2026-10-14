"""
Поток викторины: то, что увидит ученик, а не то, что собрал генератор.

Эти тесты закрывают разрыв, из-за которого самая опасная поломка захода
дожила до живого бота. Приёмка `verify_quiz_channels` проверяла СБОРКУ
вопроса — варианты, язык, созвучие — и говорила «верно». А на экране
получалось вот что:

    Вопрос 4/15 · 🎧
    🔊 Послушай и выбери, что прозвучало:
    [Verspätung] [Verspannung] [Verpflegung] [Versöhnung]

Ни звука, ни слова. У вопроса на слух самого слова на экране НЕТ — его
заменяет клип. Без клипа остаются четыре варианта, по которым можно только
ткнуть наугад.

Отсюда главное условие, которое держат эти тесты:

    У КАЖДОГО ВОПРОСА ЕСТЬ ЛИБО СЛОВО НА ЭКРАНЕ, ЛИБО ЗВУК.
"""

from app.database.enums import CEFRLevel, PartOfSpeech, QuizChannel, QuizMode
from app.database.models import User
from app.services.language_service import LanguagePair, option_label
from app.services.quiz_service import enabled_channels, pick_channel
from tests.conftest import build_groups, make_word

# pytest.ini: asyncio_mode = auto — асинхронные тесты подхватываются сами,
# а пометка pytestmark навешивалась бы и на синхронный разбор кода внизу


class _Settings:
    """Пользователь только с теми полями, что читает выбор состава."""

    def __init__(self, channels: str, audio_enabled: bool = True):
        self.quiz_channels = channels
        self.audio_enabled = audio_enabled


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
# ============================================================================

async def test_audio_off_removes_the_listening_channel():
    """
    Выключенная озвучка отменяет слух, что бы ни стояло в составе.

    Это не удобство, а исправление настоящего дефекта. Без клипа вопрос на
    слух неотвечаем, и ученик, выключивший озвучку, получал бы половину
    круга вслепую — не изредка, а КАЖДЫЙ раз, потому что причина
    детерминированная.
    """
    on = enabled_channels(_Settings("ta", audio_enabled=True))
    off = enabled_channels(_Settings("ta", audio_enabled=False))

    assert QuizChannel.AUDIO in on
    assert QuizChannel.AUDIO not in off
    assert off == [QuizChannel.TEXT], "текст обязан остаться всегда"


async def test_empty_composition_still_gives_a_playable_round():
    """
    Занятие без единого канала — не занятие, а пустой экран. Настройка не
    имеет права кончаться пустым экраном.
    """
    assert enabled_channels(_Settings("")) == [QuizChannel.TEXT]
    assert enabled_channels(_Settings("zzz")) == [QuizChannel.TEXT]
    assert enabled_channels(None) == [QuizChannel.TEXT]


# ============================================================================
# ДОПУСК СЛОВА К ВОПРОСУ НА СЛУХ
# ============================================================================

async def _seed(session, count: int = 6):
    words = []
    for i in range(count):
        w = make_word(
            f"Testwort{i}", article="das", pos=PartOfSpeech.NOUN,
            ru=f"слово{i}", uk=f"слово{i}", en=f"word{i}",
            tr=f"kelime{i}", pl=f"slowo{i}",
        )
        w.level = CEFRLevel.B1
        session.add(w)
        words.append(w)
    await session.commit()
    await build_groups(session)
    return words


async def test_unseen_word_is_never_asked_by_ear(session, user):
    """
    Нельзя узнать на слух то, чего ни разу не видел.

    Новое слово, пришедшее сразу звуком, — не упражнение, а загадка: ученик
    жмёт наугад, промахивается и запоминает неверный вариант.
    """
    words = await _seed(session)
    user.quiz_channels = "ta"
    user.audio_enabled = True
    await session.commit()

    channel = await pick_channel(session, user, words[0], "de", recent=[])
    assert channel is QuizChannel.TEXT


async def test_word_answered_right_once_becomes_eligible_for_ear(session, user):
    """
    Один успех глазами — ровно та точка, где «узнаю написанное» уже есть, а
    «узнаю на слух» ещё нет.

    Не «показано» (можно было ткнуть мимо) и не «выучено»: к трём верным
    подряд ученик уже перерос текстовый вопрос, и слух пришёл бы поздно.
    """
    from app.services.quiz_service import update_word_progress

    words = await _seed(session)
    user.quiz_channels = "ta"
    user.audio_enabled = True
    await session.commit()

    await update_word_progress(
        user_id=user.id, word_id=words[0].id, is_correct=True,
        session=session, learning_lang="de", channel=QuizChannel.TEXT,
    )

    # История передаётся непустой НАРОЧНО. При пустой выбор начинается с
    # первого канала по кругу, то есть с текста, — и это верно: первый
    # вопрос занятия всегда текстовый, начинать с того, что непонятно без
    # звука, плохо. Допуск проверяется на СЛЕДУЮЩЕМ вопросе.
    assert await pick_channel(session, user, words[0], "de", recent=[]) \
        is QuizChannel.TEXT, "первый вопрос круга обязан быть текстовым"

    channel = await pick_channel(session, user, words[0], "de", recent=["t"])
    assert channel is QuizChannel.AUDIO


async def test_never_three_of_the_same_channel_in_a_row(session, user):
    """
    У продвинутого ученика почти всё допущено к слуху, и занятие
    выродилось бы в сплошное аудирование.
    """
    from app.services.quiz_service import update_word_progress

    words = await _seed(session)
    user.quiz_channels = "ta"
    user.audio_enabled = True
    await session.commit()
    await update_word_progress(
        user_id=user.id, word_id=words[0].id, is_correct=True,
        session=session, learning_lang="de", channel=QuizChannel.TEXT,
    )

    after_two_audio = await pick_channel(
        session, user, words[0], "de", recent=["a", "a"]
    )
    assert after_two_audio is QuizChannel.TEXT


# ============================================================================
# ГЛАВНОЕ: БЕЗ КЛИПА ВОПРОС ПЕРЕСОБИРАЕТСЯ ТЕКСТОМ
# ============================================================================

async def test_audio_question_without_a_clip_becomes_a_text_question(
    session, user, monkeypatch
):
    """
    Клипа может не быть по причинам, которые при сборке вопроса ещё не
    известны: его нет на диске для выбранного голоса, или синтез не ответил
    (на неосновных голосах срывается примерно в одном случае из десяти).

    Поэтому решение принимается в обработчике, ПОСЛЕ попытки получить звук.
    Канал меняется вместе с вопросом — и засчитан ответ будет текстовым,
    что верно: на слух ученик его не давал.
    """
    from app.bot.handlers.quiz import listen

    words = await _seed(session)
    pair = LanguagePair(learning="de", native="ru", reverse=False)

    async def no_clip(*args, **kwargs):
        return None

    monkeypatch.setattr(listen, "_question_clip", no_clip)

    clip, channel, options = await listen._clip_or_text(
        session, user, words[0], pair, QuizChannel.AUDIO, options=[]
    )

    assert channel is QuizChannel.TEXT, "вопрос обязан пересобраться текстом"
    assert clip is None
    assert len(options) == 4, "варианты пересобраны на языке значения"


async def test_text_question_is_left_alone_when_there_is_no_clip(
    session, user, monkeypatch
):
    """
    Текстовому вопросу звук не нужен: слово написано на экране. Отсутствие
    клипа для него — норма (так в обратном направлении всегда), и
    пересобирать там нечего.
    """
    from app.bot.handlers.quiz import listen

    words = await _seed(session)
    pair = LanguagePair(learning="de", native="ru", reverse=True)

    async def no_clip(*args, **kwargs):
        return None

    monkeypatch.setattr(listen, "_question_clip", no_clip)

    sentinel = [("x", "y")]
    clip, channel, options = await listen._clip_or_text(
        session, user, words[0], pair, QuizChannel.TEXT, options=sentinel
    )

    assert channel is QuizChannel.TEXT
    assert options is sentinel, "варианты текстового вопроса трогать незачем"


async def test_listening_question_hides_the_word_but_text_one_shows_it(session, user):
    """
    Разделение, на котором всё и держится: у вопроса на слух слова на экране
    нет, у текстового — есть. Если оба будут показывать слово, слушать
    станет незачем; если оба спрячут — отвечать будет не на что.
    """
    from app.bot.handlers.quiz.question import _question_text

    words = await _seed(session)
    pair = LanguagePair(learning="de", native="ru", reverse=False)
    shown = option_label(words[0], pair.prompt_lang)

    by_ear = _question_text(words[0], pair, "ru", 1, 15, channel=QuizChannel.AUDIO)
    by_eye = _question_text(words[0], pair, "ru", 1, 15, channel=QuizChannel.TEXT)

    assert shown not in by_ear, "на слух слово напечатано — слушать незачем"
    assert "📝" not in by_ear, "пример содержит слово и выдал бы ответ"
    assert shown in by_eye


# ============================================================================
# ФОРМА КОДА: обе ветки обязаны задать всё, что используется после них
# ============================================================================

def test_both_branches_of_the_next_question_assign_everything_the_tail_uses():
    """
    Проверка не поведения, а ФОРМЫ — и она тут уместна.

    `_advance` (тело `show_next_question`) устроен как развилка с общим хвостом: одна ветка
    собирает повтор ошибок, другая обычный вопрос, а показ карточки стоит
    ПОСЛЕ них и читает `word`, `options`, `channel`, `clip`. Стоит одной
    ветке забыть присвоить что-то одно — обработчик падает с NameError.

    Так и случилось: при добавлении запасного пути `clip` появился только во
    второй ветке, и кнопка «повторить ошибки» перестала работать. Ни тесты
    на функции, ни приёмка генератора этого не видят: ошибка живёт в потоке
    обработчика, а повтор начинается лишь после круга, в котором ошибки
    были, — то есть на пути, куда доходят немногие.

    Поймать такое поведенческим тестом дорого (нужен весь аиограмовский
    обвес), а разбором кода — дёшево и надёжно.
    """
    import ast
    import inspect

    from app.bot.handlers.quiz import game

    tree = ast.parse(inspect.getsource(game))
    func = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "_advance"
    )

    # Развилка «повтор ошибок / обычный вопрос» — последняя в теле функции
    forks = [n for n in func.body if isinstance(n, ast.If) and n.orelse]
    assert forks, "развилка в _advance пропала — проверку надо переписать"
    fork = forks[-1]

    def assigned(nodes) -> set[str]:
        names: set[str] = set()
        for node in nodes:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store):
                    names.add(sub.id)
        return names

    in_if = assigned(fork.body)
    in_else = assigned(fork.orelse)

    tail = func.body[func.body.index(fork) + 1:]
    used_after: set[str] = set()
    for node in tail:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                used_after.add(sub.id)

    # Интересуют только имена, которые развилка вообще заводит: глобальные и
    # аргументы функции доступны в обеих ветках и так
    local_to_fork = (in_if | in_else) & used_after
    missing_in_if = sorted(local_to_fork - in_if)
    missing_in_else = sorted(local_to_fork - in_else)

    assert not missing_in_if, (
        f"ветка повтора ошибок не задаёт {missing_in_if}, "
        f"а показ карточки это читает — будет NameError"
    )
    assert not missing_in_else, (
        f"ветка обычного вопроса не задаёт {missing_in_else}, "
        f"а показ карточки это читает — будет NameError"
    )


# ============================================================================
# ТРЕТИЙ КАНАЛ: РЕЧЬ
# ============================================================================

async def test_speech_unlocks_later_than_listening(session, user):
    """
    Порог растёт вместе с трудностью канала.

    Прочитать можно сразу; узнать на слух — после одного успеха глазами,
    иначе человек угадывает звук слова, которого ни разу не видел;
    произнести — после двух, потому что производство труднее узнавания, и
    требовать его от едва знакомого слова значит гарантировать промах.
    """
    from app.services.quiz_service import CHANNEL_UNLOCK

    assert CHANNEL_UNLOCK[QuizChannel.TEXT] == 0
    assert (CHANNEL_UNLOCK[QuizChannel.TEXT]
            < CHANNEL_UNLOCK[QuizChannel.AUDIO]
            < CHANNEL_UNLOCK[QuizChannel.SPEECH])


async def test_speech_is_not_asked_for_a_barely_known_word(session, user):
    from app.services.quiz_service import update_word_progress

    words = await _seed(session)
    user.quiz_channels = "ts"
    user.audio_enabled = True
    await session.commit()

    # один верный ответ — для речи ещё рано
    await update_word_progress(
        user_id=user.id, word_id=words[0].id, is_correct=True,
        session=session, learning_lang="de", channel=QuizChannel.TEXT,
    )
    assert await pick_channel(session, user, words[0], "de", recent=["t"]) \
        is QuizChannel.TEXT

    # второй — теперь можно просить вслух
    await update_word_progress(
        user_id=user.id, word_id=words[0].id, is_correct=True,
        session=session, learning_lang="de", channel=QuizChannel.TEXT,
    )
    assert await pick_channel(session, user, words[0], "de", recent=["t"]) \
        is QuizChannel.SPEECH


async def test_speech_question_shows_the_word_and_has_no_options(session, user):
    """
    Вопрос вслух — зеркало вопроса на слух.

    Там слово спрятано и его заменяет звук; здесь слово ПОКАЗАНО, потому что
    произнести можно только то, что видишь, а вариантов нет вовсе: ответ
    приходит голосовым сообщением.
    """
    from app.bot.handlers.quiz.question import _question_keyboard, _question_text

    words = await _seed(session)
    pair = LanguagePair(learning="de", native="ru", reverse=False)
    shown = option_label(words[0], pair.learning)

    text = _question_text(words[0], pair, "ru", 1, 15, channel=QuizChannel.SPEECH)
    assert shown in text, "слово обязано быть на экране: его надо произнести"
    assert "📝" not in text, "пример подталкивал бы прочитать предложение целиком"

    keyboard = _question_keyboard(QuizChannel.SPEECH, [], "ru")
    buttons = [b for row in keyboard.inline_keyboard for b in row]
    assert len(buttons) == 2, "послушать эталон и пропустить — больше нечего"
    assert {b.callback_data for b in buttons} == {"speech_reference", "speech_skip"}


async def test_counters_survive_a_fresh_row(session, user):
    """
    У только что созданной записи счётчики ещё None: значения по умолчанию
    ставятся при вставке, а учёт идёт до неё. Первый же ответ вслух по
    новому слову падал с «NoneType + int».
    """
    from app.services.quiz_service import _count_channel
    from app.database.models import UserWord

    fresh = UserWord(user_id=user.id, word_id=1, learning_lang="de",
                     correct_streak=0, times_shown=0, times_correct=0,
                     learned=False)
    assert fresh.shown_speech is None, "иначе этот тест ничего не проверяет"

    _count_channel(fresh, QuizChannel.SPEECH, is_correct=True)
    assert fresh.shown_speech == 1
    assert fresh.correct_speech == 1


# ============================================================================
# ИТОГ КРУГА: КАКИМ КАНАЛОМ ЧТО ПРИШЛО
#
# Строки «🎧 На слух: N» и «🎤 Вслух: N» существовали в шести локалях и не
# печатались ни разу: счётчик слуха считался и не использовался, речь не
# считалась вовсе. Три канала затевались ради видимого разрыва между
# навыками — а в итоге круга он был не виден.
# ============================================================================

class _Asked:
    """Вопрос круга только с теми полями, что читает разбор."""

    def __init__(self, channel: str | None, is_correct: bool = True) -> None:
        self.channel = channel
        self.is_correct = is_correct


def _pair() -> LanguagePair:
    return LanguagePair(learning="de", native="ru", reverse=False)


def _round(*channels: str | None):
    from app.bot.handlers.quiz.game import _round_breakdown

    word = make_word("Haus", ru="дом")
    items = [(_Asked(c), word) for c in channels]
    return _round_breakdown(items, _pair(), "ru")


def test_speech_questions_are_marked_in_the_round_summary():
    """Речь помечена и сосчитана — прежде её не было ни там, ни там."""
    details, lines = _round(
        QuizChannel.TEXT.value, QuizChannel.SPEECH.value, QuizChannel.SPEECH.value
    )

    assert sum("🎤" in d for d in details) == 2, "речь не помечена в разборе"
    assert any("2" in line and "🎤" in line for line in lines), \
        f"нет строки про речь: {lines}"


def test_listening_and_speech_are_counted_apart():
    details, lines = _round(
        QuizChannel.AUDIO.value, QuizChannel.SPEECH.value, QuizChannel.TEXT.value
    )

    assert len(lines) == 2, f"ожидались две строки каналов, вышло {lines}"
    assert "🎧" in lines[0] and "🎤" in lines[1], f"порядок строк сбит: {lines}"


def test_channel_line_is_absent_when_the_channel_was_not_used():
    """
    «🎤 Вслух: 0» напоминало бы о неудаче там, где её нет: человек просто не
    включал этот канал.
    """
    _, lines = _round(QuizChannel.TEXT.value, QuizChannel.TEXT.value)

    assert lines == [], f"у круга из одного текста появились строки: {lines}"


def test_text_questions_carry_no_channel_mark():
    """
    Текст не помечается нарочно: он основной, и значок у каждой строки
    зарябил бы весь список ради того, что видно по отсутствию остальных.
    """
    details, _ = _round(QuizChannel.TEXT.value)

    assert "🎧" not in details[0] and "🎤" not in details[0]


def test_rounds_played_before_channels_existed_do_not_break_the_summary():
    """
    У вопросов, заданных до появления каналов, колонка пуста. Разбор обязан
    счесть их текстом, а не упасть на поиске значка по None.
    """
    details, lines = _round(None, None)

    assert len(details) == 2
    assert lines == []
