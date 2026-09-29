"""Движок викторины: корректность вариантов ответа, изоляция прогресса по языкам, SRS."""

from datetime import timedelta

from app.core.clock import utcnow

import pytest
from sqlalchemy import select

from app.database.enums import CEFRLevel, PartOfSpeech, QuizMode
from app.database.models import UserWord, Word
from app.services import quiz_service as qs
from app.services.language_service import LanguagePair
from tests.conftest import build_groups, make_word


async def _seed_distinct(session, count: int, *, level=CEFRLevel.A1, pos=PartOfSpeech.NOUN):
    """Слова с гарантированно различными переводами на все языки."""
    words = [
        make_word(f"Wort{i}", level=level, pos=pos, article="das", frequency_rank=i)
        for i in range(count)
    ]
    session.add_all(words)
    await session.commit()
    return words


class TestOptionsAreDistinct:
    """
    Главный баг прежней версии: дистракторы подбирались по части речи и артиклю,
    а текст вариантов не сверялся. Вопрос мог содержать два одинаковых варианта
    (die / der / den / dem все показываются как «the»), и ответить было нельзя.
    """

    async def test_colliding_native_translations_never_collide_in_options(self, session, user):
        # Немецкие слова различны, английские переводы совпадают
        colliding = [
            make_word("die", level=CEFRLevel.A1, pos=PartOfSpeech.PRONOUN, en="the", frequency_rank=1),
            make_word("der", level=CEFRLevel.A1, pos=PartOfSpeech.PRONOUN, en="the", frequency_rank=2),
            make_word("den", level=CEFRLevel.A1, pos=PartOfSpeech.PRONOUN, en="the", frequency_rank=3),
            make_word("dem", level=CEFRLevel.A1, pos=PartOfSpeech.PRONOUN, en="the", frequency_rank=4),
        ]
        # Плюс достаточно слов с различными английскими переводами
        others = [
            make_word(f"Pron{i}", level=CEFRLevel.A1, pos=PartOfSpeech.PRONOUN,
                      en=f"pronoun{i}", frequency_rank=100 + i)
            for i in range(8)
        ]
        session.add_all(colliding + others)
        await build_groups(session)

        user.learning_lang, user.native_lang, user.reverse_mode = "de", "en", False
        await session.commit()

        seen_questions = 0
        for _ in range(40):
            question = await qs.generate_question(session, user)
            if question is None:
                continue
            seen_questions += 1
            texts = [text.lower() for _, text in question["options"]]
            assert len(texts) == len(set(texts)), f"повторяющиеся варианты: {texts}"

        assert seen_questions > 0, "не удалось собрать ни одного вопроса"

    async def test_options_distinct_in_reverse_direction(self, session, user):
        # Обратное направление: варианты на изучаемом языке
        words = [
            make_word("Sitzung", level=CEFRLevel.B1, en="meeting", frequency_rank=1),
            make_word("Treff", level=CEFRLevel.B1, en="meeting", frequency_rank=2),
            make_word("Versammlung", level=CEFRLevel.B1, en="meeting", frequency_rank=3),
        ]
        words += [
            make_word(f"Ding{i}", level=CEFRLevel.B1, en=f"thing{i}", frequency_rank=50 + i)
            for i in range(8)
        ]
        session.add_all(words)
        await build_groups(session)

        user.learning_lang, user.native_lang, user.reverse_mode = "en", "ru", True
        user.level = CEFRLevel.B1
        await session.commit()

        for _ in range(30):
            question = await qs.generate_question(session, user)
            if question is None:
                continue
            texts = [t.lower() for _, t in question["options"]]
            assert len(texts) == len(set(texts)), f"повторяющиеся варианты: {texts}"

    async def test_question_has_four_options(self, session, user):
        await _seed_distinct(session, 12)
        await build_groups(session)

        question = await qs.generate_question(session, user)
        assert question is not None
        assert len(question["options"]) == qs.OPTIONS_TOTAL

    async def test_no_question_when_too_few_words(self, session, user):
        """Меньше четырёх различимых вариантов — лучше None, чем сломанный вопрос."""
        await _seed_distinct(session, 2)
        await build_groups(session)

        assert await qs.generate_question(session, user) is None

    async def test_correct_index_points_at_correct_word(self, session, user):
        await _seed_distinct(session, 12)
        await build_groups(session)

        for _ in range(10):
            question = await qs.generate_question(session, user)
            assert question is not None
            idx = question["correct_answer_index"]
            assert question["options"][idx][0] == question["correct_word"].id


class TestCanonicalOnly:
    """В викторине участвуют только канонические слова — иначе одно и то же
    слово на изучаемом языке встречалось бы несколько раз."""

    async def test_collapsed_words_never_selected(self, session, user):
        # Meeting/Sitzung/Treff различны по-немецки, но при изучении английского
        # это одно слово — показываться должно только каноническое
        session.add_all([
            make_word("Meeting", level=CEFRLevel.A1, en="meeting", frequency_rank=10),
            make_word("Sitzung", level=CEFRLevel.A1, en="meeting", frequency_rank=20),
            make_word("Treff", level=CEFRLevel.A1, en="meeting", frequency_rank=30),
        ])
        session.add_all([
            make_word(f"X{i}", level=CEFRLevel.A1, en=f"x{i}", frequency_rank=100 + i)
            for i in range(10)
        ])
        await build_groups(session)

        user.learning_lang, user.native_lang = "en", "ru"
        await session.commit()

        # Каноническим должно стать самое частотное — Meeting (rank 10)
        meeting_ids = (await session.execute(
            select(Word.id).where(Word.word_de.in_(["Sitzung", "Treff"]))
        )).scalars().all()

        for _ in range(60):
            question = await qs.generate_question(session, user)
            if question is None:
                continue
            ids = [wid for wid, _ in question["options"]]
            assert not set(ids) & set(meeting_ids), "выбрано неканоническое слово"

    async def test_words_without_translation_are_skipped(self, session, user):
        """Слово без перевода на язык значения нечем подписать."""
        empty = make_word("Ohne", level=CEFRLevel.A1, en="", frequency_rank=1)
        missing = make_word("Leer", level=CEFRLevel.A1, frequency_rank=2)
        missing.translation_en = None  # в make_word None означает «значение по умолчанию»
        session.add_all([empty, missing])
        good = [
            make_word(f"Gut{i}", level=CEFRLevel.A1, en=f"good{i}", frequency_rank=10 + i)
            for i in range(10)
        ]
        session.add_all(good)
        await build_groups(session)

        user.learning_lang, user.native_lang = "de", "en"
        await session.commit()

        bad_ids = (await session.execute(
            select(Word.id).where(Word.word_de.in_(["Ohne", "Leer"]))
        )).scalars().all()

        for _ in range(40):
            question = await qs.generate_question(session, user)
            if question is None:
                continue
            ids = [wid for wid, _ in question["options"]]
            assert not set(ids) & set(bad_ids)


class TestProgressIsolation:
    """Прогресс ведётся отдельно по каждому изучаемому языку."""

    async def test_learning_german_does_not_mark_english_learned(self, session, user):
        words = await _seed_distinct(session, 5)
        await build_groups(session)
        word = words[0]

        for _ in range(3):
            await qs.update_word_progress(user.id, word.id, True, session, learning_lang="de")

        de_row = (await session.execute(
            select(UserWord).where(
                UserWord.user_id == user.id,
                UserWord.word_id == word.id,
                UserWord.learning_lang == "de",
            )
        )).scalar_one()
        assert de_row.correct_streak == 3

        en_row = (await session.execute(
            select(UserWord).where(
                UserWord.user_id == user.id,
                UserWord.word_id == word.id,
                UserWord.learning_lang == "en",
            )
        )).scalar_one_or_none()
        assert en_row is None, "прогресс протёк в другой язык"

    async def test_new_words_are_per_language(self, session, user):
        words = await _seed_distinct(session, 12)
        await build_groups(session)

        # Проходим все слова на немецком
        for w in words:
            await qs.update_word_progress(user.id, w.id, True, session, learning_lang="de")

        de_pair = LanguagePair(learning="de", native="ru")
        en_pair = LanguagePair(learning="en", native="ru")

        assert await qs.get_new_words(user.id, session, de_pair, [], user=user) is None
        assert await qs.get_new_words(user.id, session, en_pair, [], user=user) is not None


class TestLearnedRequiresSpacing:
    """Три угадывания подряд в один день — не выученное слово."""

    async def test_not_learned_on_first_day(self, session, user):
        words = await _seed_distinct(session, 5)
        await build_groups(session)
        word = words[0]

        for _ in range(4):
            await qs.update_word_progress(user.id, word.id, True, session, learning_lang="de")

        row = (await session.execute(
            select(UserWord).where(UserWord.word_id == word.id, UserWord.user_id == user.id)
        )).scalar_one()

        assert row.correct_streak >= qs.MIN_ATTEMPTS_FOR_LEARNED
        assert row.learned is False, "слово отмечено выученным в день знакомства"

    async def test_learned_after_a_day(self, session, user):
        words = await _seed_distinct(session, 5)
        await build_groups(session)
        word = words[0]

        for _ in range(2):
            await qs.update_word_progress(user.id, word.id, True, session, learning_lang="de")

        # Знакомство было два дня назад
        row = (await session.execute(
            select(UserWord).where(UserWord.word_id == word.id, UserWord.user_id == user.id)
        )).scalar_one()
        row.created_at = utcnow() - timedelta(days=2)
        await session.commit()

        await qs.update_word_progress(user.id, word.id, True, session, learning_lang="de")

        await session.refresh(row)
        assert row.learned is True

    async def test_wrong_answer_reduces_streak(self, session, user):
        words = await _seed_distinct(session, 5)
        await build_groups(session)
        word = words[0]

        for _ in range(5):
            await qs.update_word_progress(user.id, word.id, True, session, learning_lang="de")
        row = (await session.execute(
            select(UserWord).where(UserWord.word_id == word.id, UserWord.user_id == user.id)
        )).scalar_one()
        assert row.correct_streak == 5

        await qs.update_word_progress(user.id, word.id, False, session, learning_lang="de")
        await session.refresh(row)
        assert row.correct_streak == 3
        assert row.times_shown == 6
        assert row.times_correct == 5


class TestQuizModes:
    async def test_level_mode_respects_level(self, session, user):
        session.add_all([
            make_word(f"A{i}", level=CEFRLevel.A1, frequency_rank=i) for i in range(10)
        ])
        session.add_all([
            make_word(f"C{i}", level=CEFRLevel.C2, frequency_rank=100 + i) for i in range(10)
        ])
        await build_groups(session)

        user.quiz_mode = QuizMode.LEVEL
        user.level = CEFRLevel.A1
        await session.commit()

        for _ in range(20):
            question = await qs.generate_question(session, user)
            if question is None:
                continue
            assert question["correct_word"].level == CEFRLevel.A1

    async def test_difficult_mode_only_struggling_words(self, session, user):
        words = await _seed_distinct(session, 14)
        await build_groups(session)

        # Два слова с низкой точностью
        struggling = words[:2]
        for w in struggling:
            session.add(UserWord(
                user_id=user.id, word_id=w.id, learning_lang="de",
                correct_streak=0, times_shown=4, times_correct=1,
                last_seen_at=utcnow() - timedelta(days=1), learned=False,
            ))
        await session.commit()

        pair = LanguagePair(learning="de", native="ru")
        assert await qs.count_difficult_words(user.id, session, pair) == 2

        struggling_ids = {w.id for w in struggling}
        for _ in range(20):
            word = await qs.get_difficult_word(user.id, session, pair, [])
            assert word is None or word.id in struggling_ids


class TestExcludeIds:
    async def test_excluded_words_not_returned(self, session, user):
        words = await _seed_distinct(session, 12)
        await build_groups(session)

        exclude = [w.id for w in words[:6]]
        pair = LanguagePair(learning="de", native="ru")

        for _ in range(30):
            word = await qs.get_any_word(user.id, session, pair, exclude, user=user)
            assert word is None or word.id not in exclude


class TestPolysemy:
    """
    Прод-данные показали корень проблемы качества: многозначным служебным
    словам присвоено одно значение из нескольких (gleich = и «сразу», и
    «одинаковый»; als = «чем»/«когда»/«в качестве»). Если дистрактор совпадает
    с одним из значений правильного ответа, он тоже верен — и ученик угадывает
    выбор базы, а не язык.
    """

    async def test_distractor_never_shares_a_meaning_with_answer(self, session, user):
        session.add_all([
            make_word("gleich", level=CEFRLevel.A1, pos=PartOfSpeech.ADVERB,
                      ru="сразу, одинаковый", frequency_rank=1),
            make_word("sofort", level=CEFRLevel.A1, pos=PartOfSpeech.ADVERB,
                      ru="сразу", frequency_rank=2),
            make_word("identisch", level=CEFRLevel.A1, pos=PartOfSpeech.ADVERB,
                      ru="одинаковый", frequency_rank=3),
        ])
        session.add_all([
            make_word(f"Adv{i}", level=CEFRLevel.A1, pos=PartOfSpeech.ADVERB,
                      ru=f"наречие{i}", frequency_rank=50 + i)
            for i in range(10)
        ])
        await build_groups(session)

        user.learning_lang, user.native_lang, user.reverse_mode = "de", "ru", False
        await session.commit()

        from app.services.language_service import meaning_variants

        for _ in range(60):
            question = await qs.generate_question(session, user)
            if question is None:
                continue
            # ни одна пара вариантов не должна делить значение
            variant_sets = [meaning_variants(text, "ru") for _, text in question["options"]]
            for i, a in enumerate(variant_sets):
                for b in variant_sets[i + 1:]:
                    assert not (a & b), f"варианты делят значение: {question['options']}"

    async def test_multi_variant_translations_split_correctly(self):
        from app.services.language_service import meaning_variants

        assert meaning_variants("сразу, одинаковый", "ru") == {"сразу", "одинаковый"}
        assert meaning_variants("a / an", "en") == {"a", "an"}
        assert meaning_variants("to stop", "en") == {"stop"}
        assert meaning_variants("", "ru") == frozenset()
        assert meaning_variants(None, "ru") == frozenset()
