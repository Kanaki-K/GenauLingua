"""Схлопывание слов, дающих на конкретном языке один и тот же headword."""

from sqlalchemy import select

from app.database.enums import CEFRLevel, PartOfSpeech
from app.database.models import UserWord, Word, WordLangGroup
from app.services.word_groups import build_groups, remap_user_progress_to_canonical
from tests.conftest import build_groups as rebuild, make_word


async def _groups(session, lang):
    """
    Прочитать группы заново.

    Очистка кэша сессии обязательна: build_groups пишет прямым SQL в обход
    ORM, а сессия создана с expire_on_commit=False. Без этого второе чтение
    в одном тесте вернуло бы объекты со значениями до пересборки. На этом я
    уже потерял время, разыскивая несуществующую ошибку в коде.

    expunge_all, а не expire_all: второй помечает объекты устаревшими, и
    следующее обращение к их полям пытается сходить в базу вне асинхронного
    контекста — получается MissingGreenlet. Первый просто убирает объекты из
    кэша, и запрос загружает их заново.
    """
    session.expunge_all()
    rows = (await session.execute(
        select(WordLangGroup).where(WordLangGroup.lang == lang)
    )).scalars().all()
    return {r.word_id: r for r in rows}


class TestGrouping:
    async def test_same_translation_collapses_to_one_canonical(self, session):
        session.add_all([
            make_word("Meeting", en="meeting", frequency_rank=10),
            make_word("Sitzung", en="meeting", frequency_rank=20),
            make_word("Treff", en="meeting", frequency_rank=30),
        ])
        await rebuild(session, ["en"])

        groups = await _groups(session, "en")
        assert len(groups) == 3
        canonical_ids = {g.canonical_id for g in groups.values()}
        assert len(canonical_ids) == 1, "должна получиться одна группа"
        assert sum(1 for g in groups.values() if g.is_canonical) == 1

    async def test_most_frequent_wins(self, session):
        session.add_all([
            make_word("Treff", en="meeting", frequency_rank=30),
            make_word("Meeting", en="meeting", frequency_rank=10),
            make_word("Sitzung", en="meeting", frequency_rank=20),
        ])
        await rebuild(session, ["en"])

        meeting = (await session.execute(
            select(Word).where(Word.word_de == "Meeting")
        )).scalar_one()

        groups = await _groups(session, "en")
        assert all(g.canonical_id == meeting.id for g in groups.values())

    async def test_words_without_rank_lose_to_ranked(self, session):
        session.add_all([
            make_word("Ohne", en="same", frequency_rank=None),
            make_word("Mit", en="same", frequency_rank=999),
        ])
        await rebuild(session, ["en"])

        mit = (await session.execute(select(Word).where(Word.word_de == "Mit"))).scalar_one()
        groups = await _groups(session, "en")
        assert all(g.canonical_id == mit.id for g in groups.values())

    async def test_choice_is_deterministic(self, session):
        """От выбора представителя зависит прогресс — он обязан быть стабильным."""
        session.add_all([
            make_word("A", en="same", frequency_rank=5),
            make_word("B", en="same", frequency_rank=5),
        ])
        await rebuild(session, ["en"])
        first = {wid: g.canonical_id for wid, g in (await _groups(session, "en")).items()}

        await rebuild(session, ["en"])
        second = {wid: g.canonical_id for wid, g in (await _groups(session, "en")).items()}

        assert first == second

    async def test_different_pos_never_collapse(self, session):
        """«order» как существительное и как глагол — разные слова."""
        session.add_all([
            make_word("Ordnung", pos=PartOfSpeech.NOUN, en="order", frequency_rank=1),
            make_word("ordnen", pos=PartOfSpeech.VERB, en="order", frequency_rank=2),
        ])
        await rebuild(session, ["en"])

        groups = await _groups(session, "en")
        assert len({g.canonical_id for g in groups.values()}) == 2
        assert all(g.is_canonical for g in groups.values())

    async def test_german_duplicates_across_levels_collapse(self, session):
        """В немецком 131 слово повторяется на разных уровнях."""
        session.add_all([
            make_word("genau", level=CEFRLevel.A1, pos=PartOfSpeech.ADVERB, frequency_rank=50),
            make_word("genau", level=CEFRLevel.B1, pos=PartOfSpeech.ADVERB, frequency_rank=80),
        ])
        await rebuild(session, ["de"])

        groups = await _groups(session, "de")
        assert len(groups) == 2
        assert len({g.canonical_id for g in groups.values()}) == 1

    async def test_words_without_translation_are_excluded(self, session):
        empty = make_word("Ohne", en="")
        missing = make_word("Leer")
        missing.translation_en = None
        session.add_all([empty, missing, make_word("Gut", en="good")])
        await rebuild(session, ["en"])

        groups = await _groups(session, "en")
        good = (await session.execute(select(Word).where(Word.word_de == "Gut"))).scalar_one()
        assert set(groups) == {good.id}

    async def test_each_language_grouped_independently(self, session):
        # Различны по-немецки и по-русски, но совпадают по-английски
        session.add_all([
            make_word("Sitzung", ru="заседание", en="meeting", frequency_rank=1),
            make_word("Treff", ru="встреча", en="meeting", frequency_rank=2),
        ])
        await rebuild(session)

        de_groups = await _groups(session, "de")
        ru_groups = await _groups(session, "ru")
        en_groups = await _groups(session, "en")

        assert len({g.canonical_id for g in de_groups.values()}) == 2
        assert len({g.canonical_id for g in ru_groups.values()}) == 2
        assert len({g.canonical_id for g in en_groups.values()}) == 1

    async def test_rebuild_is_idempotent(self, session):
        session.add_all([make_word(f"W{i}", frequency_rank=i) for i in range(5)])
        await rebuild(session)
        first = len(await _groups(session, "de"))
        await rebuild(session)
        assert len(await _groups(session, "de")) == first


class TestLemmaOverrides:
    """
    Ручное указание «эта строка — форма, а лемма вот эта».

    Нужно для 99 пар, где форма и лемма лежат в базе как два отдельных слова
    на одном уровне: «komm» при существующем «kommen». Переименовать нельзя
    из-за уникальности (word_de, level), удалить нельзя из-за каскада на
    quiz_questions — вместе со словом исчезли бы исторические ответы.
    """

    async def _override(self, session, form_id: int, lemma_id: int) -> None:
        from app.database.models import WordLemmaOverride

        session.add(WordLemmaOverride(
            word_id=form_id, lemma_word_id=lemma_id, reason="тест",
        ))
        await session.flush()

    async def test_form_joins_the_lemma_group(self, session):
        # Переводы взяты русские и заведомо разные: английские «come» и
        # «to come» схлопнулись бы и без указания, потому что нормализация
        # снимает частицу «to» — и тест ничего бы не проверял
        form = make_word("komm", ru="приходи", frequency_rank=5)
        lemma = make_word("kommen", ru="приходить", frequency_rank=50)
        session.add_all([form, lemma])
        await session.flush()

        await rebuild(session, ["ru"])
        groups = await _groups(session, "ru")
        assert groups[form.id].canonical_id != groups[lemma.id].canonical_id, (
            "без указания это два разных слова"
        )

        await self._override(session, form.id, lemma.id)
        await rebuild(session, ["ru"])

        groups = await _groups(session, "ru")
        assert groups[form.id].canonical_id == lemma.id
        assert groups[form.id].is_canonical is False
        assert groups[lemma.id].is_canonical is True

    async def test_lemma_wins_even_when_form_is_more_frequent(self, session):
        """
        Представителя обычно выбирает частотность, и форма может оказаться
        частотнее своей леммы. Без принудительного предпочтения канонической
        стала бы форма — ровно то, от чего указание должно избавить.
        """
        form = make_word("komm", en="come", frequency_rank=1)
        lemma = make_word("kommen", en="to come", frequency_rank=9999)
        session.add_all([form, lemma])
        await session.flush()
        await self._override(session, form.id, lemma.id)

        await rebuild(session, ["en"])

        groups = await _groups(session, "en")
        assert groups[form.id].canonical_id == lemma.id, (
            "лемма обязана победить, несмотря на частотность формы"
        )

    async def test_override_applies_to_every_language(self, session):
        form = make_word("komm", ru="приходи", en="come")
        lemma = make_word("kommen", ru="приходить", en="to come")
        session.add_all([form, lemma])
        await session.flush()
        await self._override(session, form.id, lemma.id)

        await rebuild(session, ["ru", "en"])

        for lang in ("ru", "en"):
            groups = await _groups(session, lang)
            assert groups[form.id].canonical_id == lemma.id, lang

    async def test_progress_from_form_merges_into_lemma(self, session, user):
        form = make_word("komm", en="come")
        lemma = make_word("kommen", en="to come")
        session.add_all([form, lemma])
        await session.flush()
        await self._override(session, form.id, lemma.id)

        session.add_all([
            UserWord(user_id=user.id, word_id=form.id, learning_lang="en",
                     times_shown=4, times_correct=3, correct_streak=1),
            UserWord(user_id=user.id, word_id=lemma.id, learning_lang="en",
                     times_shown=10, times_correct=8, correct_streak=3),
        ])
        await session.flush()

        await rebuild(session, ["en"])
        await session.run_sync(
            lambda sync: remap_user_progress_to_canonical(sync.connection())
        )

        rows = (await session.execute(
            select(UserWord).where(UserWord.user_id == user.id)
        )).scalars().all()

        # Ни один ответ не потерян: счётчики суммируются
        assert len(rows) == 1
        assert rows[0].word_id == lemma.id
        assert rows[0].times_shown == 14
        assert rows[0].times_correct == 11
        assert rows[0].correct_streak == 3

    async def test_override_to_itself_is_ignored(self, session):
        word = make_word("kommen", en="to come")
        session.add(word)
        await session.flush()
        await self._override(session, word.id, word.id)

        await rebuild(session, ["en"])

        groups = await _groups(session, "en")
        assert groups[word.id].is_canonical is True

    async def test_words_without_overrides_are_unaffected(self, session):
        form = make_word("komm", en="come")
        lemma = make_word("kommen", en="to come")
        other = make_word("Haus", en="house")
        session.add_all([form, lemma, other])
        await session.flush()
        await self._override(session, form.id, lemma.id)

        await rebuild(session, ["en"])

        groups = await _groups(session, "en")
        assert groups[other.id].is_canonical is True
        assert groups[other.id].canonical_id == other.id


class TestProgressRemap:
    async def test_progress_on_collapsed_word_moves_to_canonical(self, session, user):
        session.add_all([
            make_word("Meeting", en="meeting", frequency_rank=10),
            make_word("Sitzung", en="meeting", frequency_rank=20),
        ])
        await rebuild(session, ["en"])

        meeting = (await session.execute(
            select(Word).where(Word.word_de == "Meeting")
        )).scalar_one()
        sitzung = (await session.execute(
            select(Word).where(Word.word_de == "Sitzung")
        )).scalar_one()

        # Прогресс записан на слово, которое перестало быть представителем
        session.add(UserWord(
            user_id=user.id, word_id=sitzung.id, learning_lang="en",
            correct_streak=2, times_shown=5, times_correct=4, learned=False,
        ))
        await session.commit()

        await session.run_sync(lambda s: remap_user_progress_to_canonical(s.connection()))
        await session.commit()

        rows = (await session.execute(
            select(UserWord).where(UserWord.user_id == user.id)
        )).scalars().all()

        assert len(rows) == 1
        assert rows[0].word_id == meeting.id
        assert rows[0].times_shown == 5

    async def test_counters_merge_when_both_words_have_progress(self, session, user):
        session.add_all([
            make_word("Meeting", en="meeting", frequency_rank=10),
            make_word("Sitzung", en="meeting", frequency_rank=20),
        ])
        await rebuild(session, ["en"])

        words = {
            w.word_de: w
            for w in (await session.execute(select(Word))).scalars().all()
        }

        session.add_all([
            UserWord(user_id=user.id, word_id=words["Meeting"].id, learning_lang="en",
                     correct_streak=2, times_shown=5, times_correct=4, learned=False),
            UserWord(user_id=user.id, word_id=words["Sitzung"].id, learning_lang="en",
                     correct_streak=4, times_shown=7, times_correct=7, learned=True),
        ])
        await session.commit()

        await session.run_sync(lambda s: remap_user_progress_to_canonical(s.connection()))
        await session.commit()

        rows = (await session.execute(
            select(UserWord).where(UserWord.user_id == user.id)
        )).scalars().all()

        assert len(rows) == 1
        row = rows[0]
        assert row.word_id == words["Meeting"].id
        assert row.correct_streak == 4          # максимум
        assert row.times_shown == 12            # сумма
        assert row.times_correct == 11          # сумма
        assert row.learned is True              # логическое ИЛИ

    async def test_progress_in_different_languages_stays_separate(self, session, user):
        session.add_all([
            make_word("Meeting", en="meeting", frequency_rank=10),
            make_word("Sitzung", en="meeting", frequency_rank=20),
        ])
        await rebuild(session)

        words = {
            w.word_de: w
            for w in (await session.execute(select(Word))).scalars().all()
        }

        # По-немецки Sitzung каноническое само по себе, по-английски — нет
        session.add_all([
            UserWord(user_id=user.id, word_id=words["Sitzung"].id, learning_lang="de",
                     correct_streak=1, times_shown=3, times_correct=2, learned=False),
            UserWord(user_id=user.id, word_id=words["Sitzung"].id, learning_lang="en",
                     correct_streak=1, times_shown=2, times_correct=1, learned=False),
        ])
        await session.commit()

        await session.run_sync(lambda s: remap_user_progress_to_canonical(s.connection()))
        await session.commit()

        rows = (await session.execute(
            select(UserWord).where(UserWord.user_id == user.id)
        )).scalars().all()
        by_lang = {r.learning_lang: r for r in rows}

        assert by_lang["de"].word_id == words["Sitzung"].id
        assert by_lang["en"].word_id == words["Meeting"].id


class TestBuildStats:
    async def test_stats_report_collapse_counts(self, session):
        session.add_all([
            make_word("Meeting", en="meeting", frequency_rank=1),
            make_word("Sitzung", en="meeting", frequency_rank=2),
            make_word("Haus", en="house", frequency_rank=3),
        ])
        await session.commit()

        stats = await session.run_sync(lambda s: build_groups(s.connection(), ["en"]))
        await session.commit()

        assert stats["en"]["rows"] == 3
        assert stats["en"]["groups"] == 2
        assert stats["en"]["collapsed"] == 1
