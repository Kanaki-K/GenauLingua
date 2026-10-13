"""
Прогресс по каналам: слух и речь отделены от текста.

Три вида вопроса — прочитать, услышать, произнести — это три РАЗНЫХ навыка.
Человек, который узнаёт «Verspätung» глазами, не обязательно узнаёт его на
слух и почти наверняка не произносит. Если считать все три одной парой
счётчиков, самое ценное — видимый разрыв между навыками — пропадает, и
восстановить его задним числом нельзя: данные перемешаны необратимо.

Отсюда устройство, которое эти тесты и держат:

    times_shown / times_correct   ОБЩИЙ итог по всем каналам
    shown_audio / correct_audio   слух
    shown_speech / correct_speech речь
    текстовый канал               итог МИНУС слух МИНУС речь

Текстовых колонок нет нарочно. Будь они, рано или поздно кто-нибудь обновил
бы одну и забыл другую — и расхождение с итогом нашлось бы не сразу.
Вычитание такой возможности не оставляет вовсе.
"""

from app.database.enums import QuizChannel
from app.database.models import UserWord
from app.services.quiz_service import CHANNEL_MASTERY, _count_channel


def _word(**kwargs) -> UserWord:
    base = dict(user_id=1, word_id=1, learning_lang="de", correct_streak=0,
                times_shown=0, times_correct=0, learned=False,
                shown_audio=0, correct_audio=0, shown_speech=0, correct_speech=0)
    base.update(kwargs)
    return UserWord(**base)


def test_text_channel_is_derived_not_stored():
    """Текстовый канал — это остаток, а не отдельный счётчик."""
    uw = _word(times_shown=10, times_correct=7,
               shown_audio=3, correct_audio=2,
               shown_speech=2, correct_speech=1)

    assert uw.shown_text == 5, "10 показов минус 3 слуха минус 2 речи"
    assert uw.correct_text == 4, "7 верных минус 2 слуха минус 1 речь"


def test_old_progress_counts_as_text():
    """
    Всё, накопленное ДО появления каналов, относится к тексту.

    Других вопросов в боте не было: 29 742 показа на момент правки сделаны
    текстовыми карточками. Миграция не трогала ни одной строки — формула
    «итог минус слух минус речь» даёт верный ответ сама.
    """
    legacy = _word(times_shown=29742, times_correct=26133)

    assert legacy.shown_text == 29742
    assert legacy.correct_text == 26133


def test_each_channel_counts_into_its_own_and_into_the_total():
    """Канал учитывается дважды: себе и в общий итог."""
    uw = _word(times_shown=1, times_correct=1)
    _count_channel(uw, QuizChannel.AUDIO, is_correct=True)

    assert (uw.shown_audio, uw.correct_audio) == (1, 1)
    assert (uw.shown_speech, uw.correct_speech) == (0, 0)
    # итог прибавляется вызывающим кодом, здесь он задан вручную
    assert uw.shown_text == 0, "показ ушёл в слух, тексту не осталось ничего"


def test_wrong_answer_counts_the_show_but_not_the_hit():
    uw = _word(times_shown=1, times_correct=0)
    _count_channel(uw, QuizChannel.SPEECH, is_correct=False)

    assert uw.shown_speech == 1
    assert uw.correct_speech == 0


def test_text_channel_adds_nothing_anywhere():
    """
    У текста своих колонок нет, и _count_channel для него ничего не делает.

    Если этот тест однажды упадёт — значит тексту завели колонку, а вместе с
    ней и возможность разойтись с итогом.
    """
    uw = _word(times_shown=1, times_correct=1)
    before = (uw.shown_audio, uw.correct_audio, uw.shown_speech, uw.correct_speech)

    _count_channel(uw, QuizChannel.TEXT, is_correct=True)

    assert (uw.shown_audio, uw.correct_audio,
            uw.shown_speech, uw.correct_speech) == before
    assert uw.shown_text == 1, "показ достался тексту вычитанием"


def test_channels_never_exceed_the_total():
    """
    Сумма каналов не может превысить итог — иначе текст уйдёт в минус.

    Это и есть проверка, ради которой текстовые колонки не заводились:
    расхождение здесь означало бы, что счётчики обновляются порознь.
    """
    uw = _word(times_shown=6, times_correct=4,
               shown_audio=2, correct_audio=2,
               shown_speech=1, correct_speech=1)

    assert uw.shown_text >= 0
    assert uw.correct_text >= 0
    assert uw.shown_audio + uw.shown_speech + uw.shown_text == uw.times_shown
    assert uw.correct_audio + uw.correct_speech + uw.correct_text == uw.times_correct


def test_the_scale_measures_recognition_and_learned_measures_knowledge():
    """
    ДВЕ МЕРЫ, И ОНИ НАРОЧНО РАЗНЫЕ.

    Прежде этот тест требовал обратного: порог шкалы канала равен порогу
    «выучено», оба по три верных ответа. Довод был верный по сути — один
    верный ответ бывает угадыванием из четырёх, — но относился не к той
    мере, и замер 13 октября 2026 показал цену:

        у 154 человек из 199 нет НИ ОДНОГО слова с тремя верными ответами
        вообще, а с тремя именно нужным каналом — тем более

    Для 78% людей шкала не могла сдвинуться по построению: одно слово надо
    встретить четыре-пять раз, и каждый раз нужным каналом. Человек слушал,
    отвечал верно — и видел на шкале ноль.

    Поэтому меры разведены:

        CHANNEL_MASTERY = 1         шкала «узнаю на слух» — и значит узнаю
        MIN_ATTEMPTS_FOR_LEARNED=3  «выучено» — три ПОДРЯД плюс сутки

    Шкала движется с первого круга, «выучено» остаётся редким и потому
    дорогим. Строгость никуда не делась — она там, где и должна быть.
    """
    from app.services.quiz_service import MIN_ATTEMPTS_FOR_LEARNED

    assert CHANNEL_MASTERY == 1, (
        "шкала «узнаю» снова требует больше одного верного ответа — "
        "у 78% людей она не сдвинется"
    )
    assert MIN_ATTEMPTS_FOR_LEARNED > CHANNEL_MASTERY, (
        "«выучено» должно быть строже шкалы, иначе двух мер нет"
    )


# ============================================================================
# ВОПРОС НА СЛУХ: варианты должны быть СОЗВУЧНЫ, иначе слушать не надо
# ============================================================================

from app.database.enums import PartOfSpeech
from app.services.language_service import LanguagePair
from app.services.quiz_service import (
    SOUNDALIKE_PREFIX, _bare_meaning, _prefix_len, build_audio_options,
)
from tests.conftest import make_word


def test_audio_options_are_in_the_learning_language():
    """
    На слух спрашивают «что услышал», а не «что это значит».

    Требование владельца дословно: «должно озвучивать на том языке, котором
    ответ. Чтобы человек слушал условно немецкое слово и выбирал что он
    услышал, а не перевод».

    Если звучит немецкое слово, а в вариантах русские переводы, упражнение
    проверяет ПОНИМАНИЕ — то же, что обычная карточка, только вход другой.
    Вариант на том же языке проверяет связку «звук → написание», которой
    текстовая карточка не тренирует вовсе.
    """
    correct = make_word("Verspätung", article="die", pos=PartOfSpeech.NOUN,
                        ru="опоздание", uk="запізнення", en="delay",
                        tr="gecikme", pl="opóźnienie")
    other = make_word("Verspannung", article="die", pos=PartOfSpeech.NOUN,
                      ru="зажатость", uk="затиск", en="tension",
                      tr="gerginlik", pl="napięcie")
    pair = LanguagePair(learning="de", native="ru", reverse=False)

    options, correct_index = build_audio_options(correct, [other], pair)
    texts = [t for _, t in options]

    assert "die Verspätung" in texts
    assert "die Verspannung" in texts
    assert "опоздание" not in [t.lower() for t in texts], (
        "в вариантах не должно быть перевода — иначе это обычная карточка"
    )
    assert options[correct_index][0] == correct.id


def test_article_does_not_count_as_the_shared_sound():
    """
    Созвучие считается по СЛОВУ, а не по артиклю.

    `main_meaning` для немецкого возвращает «der Krieg» вместе с артиклем, и
    первыми тремя буквами оказывалось «der». Созвучными признавались
    «der Gründer · der Flieder · der Köder» — общий у них только артикль,
    который стоит во всех четырёх вариантах и не различает ничего.
    """
    word = make_word("Krieg", article="der", pos=PartOfSpeech.NOUN,
                     ru="война", uk="війна", en="war", tr="savaş", pl="wojna")

    assert _bare_meaning(word, "de") == "Krieg", "артикль обязан отпасть"
    assert _bare_meaning(word, "ru") == "война", "где артикля нет — не трогаем"


def test_short_words_get_a_shorter_prefix():
    """
    На коротком слове три буквы не находят ничего, и вопрос сваливается в
    обычные дистракторы: «Age · Pill · Scum · Injection» — слушать не надо.
    Две буквы дают «Age → Agent, Agony», а это уже на слух и путается.
    """
    assert _prefix_len("eigentlich") == SOUNDALIKE_PREFIX
    assert _prefix_len("Age") == 2
    assert _prefix_len("Way") == 2
    assert _prefix_len("Krieg") == SOUNDALIKE_PREFIX


# ============================================================================
# СОСТАВ ЗАНЯТИЯ ПО УМОЛЧАНИЮ
# ============================================================================

def test_all_three_channels_are_on_by_default():
    """
    Значение по умолчанию — это и есть решение о том, увидят ли люди новое.

    Замер 13 октября: 🎤 речь была включена у ОДНОГО человека из 233, и тем
    одним был тестовый счёт. Игра построена, проверена на всех тридцати
    парах в оба направления, озвучка полна — и не доходила ни до кого,
    потому что состав по умолчанию стоял «ta». А 223 пользователя из 233 ни
    разу не меняли режим викторины, лежащий первым пунктом настроек.

    Решение владельца: «речь да, по умолчанию всем».
    """
    from app.database.models import User

    column = User.__table__.c.quiz_channels
    assert column.default.arg == "tas", (
        f"состав по умолчанию {column.default.arg!r}, а должен «tas»"
    )
    # `server_default.arg` бывает и строкой, и текстовым выражением —
    # зависит от того, как объявлено; приводим к строке и сравниваем
    server = str(getattr(column.server_default.arg, "text", column.server_default.arg))
    assert server.strip("'") == "tas", (
        f"значение по умолчанию В БАЗЕ {server!r}, а не «tas» — "
        f"новые люди получат другое"
    )


async def test_a_fresh_person_gets_all_three_channels(session):
    """
    То же, но через настоящую запись: колонка и база могут расходиться.
    """
    from app.database.models import User
    from app.services.quiz_service import enabled_channels

    person = User(
        id=424242, first_name="Новый", interface_language="ru",
        learning_lang="de", native_lang="ru", reverse_mode=False,
    )
    session.add(person)
    await session.commit()
    await session.refresh(person)

    assert person.quiz_channels == "tas"
    assert set(enabled_channels(person)) == {
        QuizChannel.TEXT, QuizChannel.AUDIO, QuizChannel.SPEECH
    }, "у нового человека открыты не все три канала"


def test_turning_audio_off_still_cancels_both_sound_channels():
    """
    Речь по умолчанию НЕ отменяет прежнего правила: без озвучки нет ни
    слуха, ни речи. У вопроса на слух самого слова на экране нет, а у
    вопроса вслух нечем послушать эталон.
    """
    from app.services.quiz_service import enabled_channels

    class _Person:
        quiz_channels = "tas"
        audio_enabled = False

    assert enabled_channels(_Person()) == [QuizChannel.TEXT]
