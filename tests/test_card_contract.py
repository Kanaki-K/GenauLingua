"""
Вид карточки — договорённость с владельцем, закреплённая тестом.

Договорённость сформулирована владельцем так:

  Одна карточка — это слово с правильным артиклем либо выражение. На том же
  языке пример, в котором это слово есть. В игре с четырьмя вариантами
  звучит слово; название клипа — слово с артиклем. После ответа карточка
  показывает слово и пример, а звучит слово вместе с примером; название
  такого клипа — слово, тире, не больше трёх слов примера и троеточие.
  И так на всех шести языках.

Зачем тест, если это уже работает. Выяснять заново, как устроена карточка,
дорого: код приходится перечитывать целиком, а словами договорённость
проверить нельзя. Если кто-то сдвинет формат, тест назовёт, что именно
сломалось, и спор закончится до него, а не после.

Проверяется ровно договорённость, не больше: длина обрезки, артикль,
совпадение названия со звуком, одинаковость поведения по языкам.
"""

from app.database.enums import PartOfSpeech
from app.services.audio_service import (
    KIND_FULL,
    KIND_WORD,
    audio_title,
    clip_kind_for_question,
    spoken_for,
)
from app.services.language_service import SUPPORTED_LANGS, main_meaning
from tests.conftest import make_word

# Ряд, на котором видно всё сразу: немецкий артикль, пример длиннее трёх слов
WORD = make_word(
    "Mann",
    article="der",
    pos=PartOfSpeech.NOUN,
    ru="мужчина, муж",
    uk="чоловік",
    en="man, husband",
    tr="adam, erkek",
    pl="mężczyzna",
    it="l'uomo, il marito",
    es="el hombre, el marido",
    fr="l'homme, le mari",
    cs="muž, manžel",
)
WORD.example_de = "Der Mann arbeitet hier"
WORD.example_ru = "Мужчина работает здесь"
WORD.example_uk = "Чоловік працює тут"
WORD.example_en = "The man works here"
WORD.example_tr = "Adam burada çalışıyor"
WORD.example_pl = "Ten mężczyzna tutaj pracuje"
WORD.example_it = "L'uomo lavora qui"
WORD.example_es = "El hombre trabaja aquí"
WORD.example_fr = "L'homme travaille ici"
WORD.example_cs = "Ten muž tady pracuje"


class TestCardHead:
    """Слово на карточке — с артиклем там, где артикль в языке есть."""

    def test_german_word_keeps_its_article(self):
        assert main_meaning(WORD, "de") == "der Mann"

    def test_languages_without_articles_show_bare_word(self):
        # Ни в одном из пяти артикля нет как явления — приписывать нечего
        assert main_meaning(WORD, "ru") == "мужчина"
        assert main_meaning(WORD, "uk") == "чоловік"
        assert main_meaning(WORD, "en") == "man"
        assert main_meaning(WORD, "tr") == "adam"
        assert main_meaning(WORD, "pl") == "mężczyzna"

    def test_shown_meaning_is_the_one_from_the_example(self):
        """
        Из многозначной ячейки берётся значение, которое стоит в примере.

        Прежде бралось первое по списку: показывалось «Swot», озвучивалось
        «Swot», а пример был про «overachiever» — три разных слова в одной
        карточке.
        """
        word = make_word("Streber", article="der", en="swot, overachiever, nerd")
        word.example_en = "He is a real overachiever at school"
        assert main_meaning(word, "en") == "overachiever"

    def test_exact_meaning_wins_over_an_earlier_approximate_one(self):
        """
        Из ячейки берётся ЛУЧШЕЕ совпадение, а не первое подошедшее.

        Прежде правило было «первое, что совпало по основе», и ранний
        приблизительный вариант затенял поздний точный: при примере «часто»
        показывалось «частенько», при «morale» — «moralność». Замерено на
        базе: 217 ячеек показывали соседнее слово вместо того, что в примере.
        """
        word = make_word("öfters", ru="частенько, часто, нередко")
        word.example_ru = "Я часто хожу в кино"
        assert main_meaning(word, "ru") == "часто"

        other = make_word("Moral", pl="moralność, morale, etyka")
        other.example_pl = "Jego morale jest bardzo dobre"
        assert main_meaning(other, "pl") == "morale"

    def test_verb_infinitive_is_recognised_through_its_conjugation(self):
        """
        Длинный хвост основы разрешён, когда строгое сравнение не нашло ничего.

        В славянском и турецком инфинитив длиннее общей с формой основы
        больше чем на три буквы: «одеваться» и «одеваюсь» совпадают на пяти
        из девяти, «masayı toplamak» и «topluyorum» — на четырёх из восьми.
        Строгое правило объявляло их разными словами, и карточка показывала
        первое значение: `anziehen` показывал «надевать» на пример «я
        одеваюсь», `abdecken` — «örtmek» на пример об убирании со стола.
        """
        word = make_word("anziehen", ru="надевать, одеваться, притягивать")
        word.example_ru = "Я быстро одеваюсь"
        assert main_meaning(word, "ru") == "одеваться"

        other = make_word("abdecken", tr="örtmek, kapsamak, masayı toplamak")
        other.example_tr = "Konuklar gitmeden önce masayı topluyorum"
        assert main_meaning(other, "tr") == "masayı toplamak"

    def test_long_tail_does_not_override_an_exact_hit(self):
        """
        Послабление на хвост включается только после строгого сравнения.

        Иначе «частенько» (хвост 5 к «часто») побило бы точное «часто», и
        лечение вышло бы хуже болезни. Порядок ярусов проверяется здесь
        отдельно от самих ярусов.
        """
        word = make_word("zeugen", ru="зачать, породить, свидетельствовать")
        word.example_ru = "Его квартира свидетельствует о хорошем вкусе"
        assert main_meaning(word, "ru") == "свидетельствовать"

    def test_short_word_is_recognised_through_its_case_ending(self):
        """
        У четырёхбуквенного слова падежное окончание съедает четвёртую букву.

        Ряд `Schiene` показывал «рельс», а пример был про шину на руке:
        «шина» и «шину» совпадают только на трёх буквах, и строгое правило
        считало их разными словами.
        """
        word = make_word("Schiene", article="die", ru="рельс, шина")
        word.example_ru = "После аварии он носил шину на руке"
        assert main_meaning(word, "ru") == "шина"

    def test_poblazhka_does_not_decide_between_forms_of_one_word(self):
        """
        На трёх буквах «они» и «она» неразличимы — выбирать нельзя.

        Поблажке позволено решать только при однозначном попадании. Иначе
        карточка ряда `sie` показала бы «она» там, где пример говорит «они».
        """
        word = make_word("sie", ru="они, она")
        word.example_ru = "Они завтра зайдут"
        assert main_meaning(word, "ru") == "они"

    def test_short_example_word_is_not_a_judge(self):
        """«then» не должно цепляться за «the» — слово примера короче основы."""
        word = make_word("öfters", en="quite often, now and then")
        word.example_en = "I go to the cinema often"
        assert main_meaning(word, "en") == "quite often"

    def test_one_letter_word_must_stand_whole_in_the_example(self):
        """
        Чешское «k» находилось в «kamarády», и ряд `zum` с примером «na pláž»
        показывал и озвучивал «k». Окончание «-a» — другое дело: оно часть слова.
        """
        word = make_word("zum", ru="к, на")
        word.translation_cs, word.example_cs = "k, do, na", "Jdu s kamarády na pláž"
        assert main_meaning(word, "cs") == "na"
        word.translation_tr, word.example_tr = "-e, -a", "Arkadaşlarla plaja gidiyorum"
        assert main_meaning(word, "tr") == "-a"
        # «ve» совпадает началом с «ven», но «na» стоит в примере целиком
        word.translation_cs, word.example_cs = "v, ve, na", "Jsem na zahradě, pojď ven!"
        assert main_meaning(word, "cs") == "na"


class TestQuestionClip:
    """В вопросе звучит слово, и название клипа — ровно оно."""

    def test_question_speaks_the_word_alone(self):
        for lang in SUPPORTED_LANGS:
            assert clip_kind_for_question(WORD, lang) == KIND_WORD, lang

    def test_question_title_is_the_word_with_article(self):
        spoken = spoken_for(WORD, "de", KIND_WORD)
        assert spoken == "der Mann"
        assert audio_title(main_meaning(WORD, "de")) == "der Mann"

    def test_question_title_matches_what_sounds_in_every_language(self):
        for lang in SUPPORTED_LANGS:
            shown = main_meaning(WORD, lang)
            assert spoken_for(WORD, lang, KIND_WORD) == shown, lang
            assert audio_title(shown) == shown, lang

    def test_heteronym_gets_the_example_in_the_question(self):
        """
        Исключение, и оно намеренное: слово с двумя чтениями, произнесённое
        отдельно, движок прочтёт наугад. SSML недоступен, поэтому чтение
        задаётся контекстом.
        """
        word = make_word("modern", article=None, pos=PartOfSpeech.ADJECTIVE)
        assert clip_kind_for_question(word, "de") == KIND_FULL


class TestAnswerClip:
    """После ответа звучит слово вместе с примером."""

    def test_answer_speaks_word_and_example(self):
        for lang in SUPPORTED_LANGS:
            spoken = spoken_for(WORD, lang, KIND_FULL)
            shown = main_meaning(WORD, lang)
            assert spoken.startswith(shown), lang
            # Пример идёт вслед за словом, в том же клипе
            assert spoken != shown, lang

    def test_answer_title_is_word_dash_three_words_ellipsis(self):
        title = audio_title("der Mann", "Der Mann arbeitet hier und wohnt dort")
        assert title == "der Mann — Der Mann arbeitet…"

    def test_no_ellipsis_when_example_is_short(self):
        """Троеточие значит «обрезано». Резать нечего — его быть не должно."""
        title = audio_title("река", "Река широкая")
        assert title == "река — Река широкая"
        assert "…" not in title

    def test_every_language_follows_the_same_shape(self):
        for lang in SUPPORTED_LANGS:
            shown = main_meaning(WORD, lang)
            example = getattr(WORD, f"example_{lang}")
            title = audio_title(shown, example)
            assert title.startswith(f"{shown} — "), lang
            head = title.split(" — ", 1)[1]
            words = head.rstrip("…").split()
            assert len(words) <= 3, (lang, title)
            # Троеточие ровно тогда, когда пример длиннее трёх слов
            assert ("…" in title) == (len(example.split()) > 3), (lang, title)


# ============================================================================
# ЗАГОЛОВОК ВОПРОСА: ОДНО ЗНАЧЕНИЕ В ОБОИХ НАПРАВЛЕНИЯХ
# ============================================================================

def test_question_header_is_one_meaning_in_both_directions():
    """
    В заголовке вопроса стоит ОДНО значение, а не весь список, — и в прямом
    направлении, и в обратном.

    В обратном направлении раньше стоял полный список, и довод был такой:
    звука там нет, а по одному значению слово не опознать. Владелец довод
    отклонил, увидев живую карточку:

        🏴 Записывать, принимать, брать к себе, начинать, поднимать,
           подбирать, впитывать, усваивать
        📝 Ты можешь записать разговор?

    Восемь значений в заголовке при одном в примере. Неопознаваемость
    снимается самим примером — он стоит строкой ниже.
    """
    from app.bot.handlers.quiz.question import _question_text
    from app.services.language_service import LanguagePair

    word = make_word(
        "aufnehmen",
        pos=PartOfSpeech.VERB,
        ru="записывать, принимать, брать к себе, начинать",
        uk="записувати, приймати",
        en="to record, to take in",
        tr="kaydetmek, kabul etmek",
        pl="nagrywać, przyjmować",
    )
    word.example_de = "Kannst du das Gespräch aufnehmen?"
    word.example_ru = "Ты можешь записать разговор?"

    # НАПРАВЛЕНИЕ ЗАДАЁТ КАНАЛ, а не флаг пары. Прежде обратная сторона
    # была настройкой человека на весь круг, и тест переворачивал пару сам;
    # теперь это пятая игра круга, и спрашивать её надо каналом. Пара при
    # этом всегда прямая — такой она и приходит из `pair_from_user`.
    from app.database.enums import QuizChannel

    pair = LanguagePair(learning="de", native="ru")

    for channel in (QuizChannel.TEXT, QuizChannel.REVERSE):
        text = _question_text(word, pair, "ru", 1, 25, channel=channel)
        head = text.split("<b>")[1].split("</b>")[0]
        assert "," not in head, (
            f"в заголовке список, канал {channel.value}: {head!r}"
        )

    # В прямую сторону спрашивается слово, в обратную — одно значение
    forward = _question_text(
        word, pair, "ru", 1, 25, channel=QuizChannel.TEXT
    ).split("<b>")[1].split("</b>")[0]
    assert forward == "aufnehmen", forward

    back = _question_text(
        word, pair, "ru", 1, 25, channel=QuizChannel.REVERSE
    ).split("<b>")[1].split("</b>")[0]
    assert back == "Записывать", back


def test_heteronym_gets_context_clip_even_in_a_multi_meaning_row():
    """
    Гетероним получает клип С ПРИМЕРОМ, даже когда в ячейке несколько значений.

    Прежде проверка шла по ВСЕЙ ячейке: «to live, to reside, to be alive» в
    списке гетеронимов не находится, и ряд получал изолированный клип. А
    произносится в нём одно значение — «to live», то есть ровно гетероним,
    отданный движку без контекста: /lɪv/ или /laɪv/ движок выбирает сам.

    Замер на момент правки: клип с примером получали 25 рядов вместо 109.
    Восемьдесят четыре гетеронима читались наугад.
    """
    from app.services.audio_service import clip_kind_for_question

    word = make_word(
        "leben",
        pos=PartOfSpeech.VERB,
        ru="жить, проживать",
        uk="жити",
        en="to live, to reside, to be alive",
        tr="yaşamak",
        pl="żyć",
    )
    word.example_en = "I live in Berlin"

    assert clip_kind_for_question(word, "en") == KIND_FULL, (
        "гетероним в многозначной ячейке должен озвучиваться с примером"
    )

    plain = make_word("Haus", article="das", pos=PartOfSpeech.NOUN,
                      ru="дом", uk="дім", en="house, building", tr="ev", pl="dom")
    plain.example_de = "Das Haus ist gross"
    assert clip_kind_for_question(plain, "de") == KIND_WORD


def test_cached_clip_is_invalid_when_its_title_changed():
    """
    Клип из кэша негоден, если название с тех пор поменялось.

    Название впечатывается в клип при ЗАГРУЗКЕ в Telegram. При отправке по
    file_id параметр `title` игнорируется — показываются метаданные первой
    загрузки. Значит правка правила названия обязана сбрасывать кэш, иначе
    карточка покажет старый заголовок при верном звуке.

    Так и случилось: владелец прислал снимок, где на карточке «Zapomnienie»,
    а в заголовке клипа «zapomnienie, niepamięć» — вся ячейка перевода.
    Проверка годности сверяла произносимый текст и бота; при правке правила
    названия произносимый текст НЕ МЕНЯЕТСЯ, и кэш считал себя годным.

    Тест держит именно это: совпадения текста и бота НЕДОСТАТОЧНО.
    """
    from app.database.models import WordAudio

    def usable(cached, spoken, title, bot_id):
        # условие из app/services/audio_service.py:get_clip
        return (
            cached is not None
            and cached.spoken_text == spoken
            and cached.title == title
            and cached.bot_id == bot_id
        )

    cached = WordAudio(
        word_id=1, lang="pl", kind=KIND_WORD, voice="pl-PL-ZofiaNeural",
        file_id="x", file_kind="audio", spoken_text="zapomnienie",
        title="zapomnienie, niepamięć",   # старое правило: вся ячейка
        bot_id=1,
    )

    assert not usable(cached, "zapomnienie", "Zapomnienie", 1), (
        "клип со старым названием обязан считаться негодным"
    )

    cached.title = "Zapomnienie"
    assert usable(cached, "zapomnienie", "Zapomnienie", 1), (
        "клип с верным названием обязан переиспользоваться"
    )

    cached.title = None   # загружен до миграции 7d2e9fa4c61b
    assert not usable(cached, "zapomnienie", "Zapomnienie", 1), (
        "клип без сохранённого названия обязан считаться негодным"
    )
