# -*- coding: utf-8 -*-
"""
Дымовой прогон движка викторины на реальной словарной базе.

Проверяет то, что юнит-тесты на десяти засеянных словах проверить не могут:
соберётся ли вопрос для каждой из 20 языковых пар × 2 направлений × 6 уровней
× 4 режимов на настоящих 12 772 словах, и не окажется ли в вариантах ответа
двух одинаковых текстов.
"""
import asyncio
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault("ENV", "prod")

from sqlalchemy import delete, select

from app.database.enums import CEFRLevel, QuizMode
from app.database.models import User, UserWord
from app.database.session import AsyncSessionLocal
from app.services.language_service import (
    LEARNABLE_LANGS,
    LanguagePair,
    meaning_variants,
    native_options,
)
from app.services.quiz_service import generate_question

PROBE_USER_ID = -777  # заведомо не пересекается с реальными telegram id
ATTEMPTS = 12


async def main() -> int:
    failures = Counter()
    duplicate_options = []
    empty_prompt = []
    checked = 0

    async with AsyncSessionLocal() as session:
        # Без слов и групп прогон отрапортует провал по каждой комбинации, хотя
        # движок цел. Тестовую БД легко опустошить: conftest делает TRUNCATE,
        # поэтому после pytest данные нужно залить заново.
        from sqlalchemy import func, select

        from app.database.models import Word, WordLangGroup

        word_count = (await session.execute(select(func.count()).select_from(Word))).scalar() or 0
        group_count = (
            await session.execute(select(func.count()).select_from(WordLangGroup))
        ).scalar() or 0

        if word_count < 100 or group_count == 0:
            print(
                f"В базе {word_count} слов и {group_count} записей групп — "
                "для осмысленного прогона этого мало.\n"
                "Залить данные:\n"
                "  python app/scripts/rebuild_words_from_excel.py Wordsbase/<файл>.xlsx\n"
                "  python -m app.scripts.rebuild_word_groups"
            )
            return 2

        await session.execute(delete(UserWord).where(UserWord.user_id == PROBE_USER_ID))
        await session.execute(delete(User).where(User.id == PROBE_USER_ID))
        await session.commit()

        user = User(
            id=PROBE_USER_ID,
            first_name="probe",
            interface_language="ru",
            learning_lang="de",
            native_lang="ru",
            reverse_mode=False,
            level=CEFRLevel.A1,
            quiz_mode=QuizMode.LEVEL,
        )
        session.add(user)
        await session.commit()

        combos = [
            (learning, native, reverse, level, mode)
            for learning in LEARNABLE_LANGS
            for native in native_options(learning)
            for reverse in (False, True)
            for level in CEFRLevel
            for mode in (QuizMode.LEVEL, QuizMode.ALL_WORDS)
        ]

        print(f"комбинаций к проверке: {len(combos)}, попыток на каждую: {ATTEMPTS}\n")

        for learning, native, reverse, level, mode in combos:
            user.learning_lang = learning
            user.native_lang = native
            user.reverse_mode = reverse
            user.level = level
            user.quiz_mode = mode
            user.quiz_category = None
            await session.commit()

            pair = LanguagePair(learning=learning, native=native, reverse=reverse)
            got = 0
            for _ in range(ATTEMPTS):
                question = await generate_question(session, user, exclude_ids=[], pair=pair)
                checked += 1
                if question is None:
                    continue
                got += 1

                texts = [t for _, t in question["options"]]
                lowered = [t.lower() for t in texts]
                if len(set(lowered)) != len(lowered):
                    duplicate_options.append(
                        (learning, native, reverse, level.value, mode.value, texts)
                    )

                # Пересечение по значениям — дистрактор не должен быть тоже верным
                variant_sets = [meaning_variants(t, pair.answer_lang) for t in texts]
                for i, a in enumerate(variant_sets):
                    for b in variant_sets[i + 1:]:
                        if a & b:
                            duplicate_options.append(
                                (learning, native, reverse, level.value, mode.value, texts)
                            )
                            break

                prompt = question["correct_word"]
                from app.services.language_service import word_text

                if not word_text(prompt, pair.prompt_lang).strip():
                    empty_prompt.append((learning, native, level.value, prompt.id))

            if got == 0:
                key = f"{learning}->{native}{' обратный' if reverse else ''} {level.value} {mode.value}"
                failures[key] = ATTEMPTS

        await session.execute(delete(UserWord).where(UserWord.user_id == PROBE_USER_ID))
        await session.execute(delete(User).where(User.id == PROBE_USER_ID))
        await session.commit()

    print(f"сгенерировано попыток: {checked}")

    print(f"\n=== КОМБИНАЦИИ, ГДЕ ВОПРОС НЕ СОБРАЛСЯ НИ РАЗУ: {len(failures)} ===")
    for key, n in failures.most_common(30):
        print(f"  {key}")
    if not failures:
        print("  нет")

    print(f"\n=== ВОПРОСЫ С НЕРАЗЛИЧИМЫМИ ВАРИАНТАМИ: {len(duplicate_options)} ===")
    for learning, native, reverse, level, mode, texts in duplicate_options[:10]:
        print(f"  учим {learning}, значение {native}, обратный={reverse}, {level}, {mode}: {texts}")
    if not duplicate_options:
        print("  нет")

    print(f"\n=== ПУСТОЙ ТЕКСТ ВОПРОСА: {len(empty_prompt)} ===")
    for item in empty_prompt[:10]:
        print(f"  {item}")
    if not empty_prompt:
        print("  нет")

    return 1 if (failures or duplicate_options or empty_prompt) else 0


sys.exit(asyncio.run(main()))
