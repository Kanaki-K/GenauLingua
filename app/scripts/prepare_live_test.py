"""
Подготовить ОДИН счёт к ручному тесту всех каналов на всех языках.

ЗАЧЕМ. Каналы открываются не человеку, а СЛОВУ: слух — после одного
верного ответа по слову, речь — после двух. Правило верное (нельзя узнать
на слух то, чего ни разу не видел), но у ручного теста из него выходит
препятствие: прогресс у человека обычно есть по ОДНОМУ языку.

Замер 13 октября по владельцу: 140 слов готовы к речи по немецкому и НОЛЬ
по остальным пяти. То есть, переключившись на турецкий, он получил бы
круг сплошного текста и не проверил бы ничего — очередная приёмка
вхолостую, только на этот раз с человеком вместо скрипта.

ЧТО ДЕЛАЕТ. Выдаёт указанному счёту прогресс по словам каждого языка:
`times_shown=3, times_correct=2`. Два верных ответа открывают и слух, и
речь; точность 67% кладёт слово в «трудную» корзину, из которой подбор
берёт 60% вопросов, — иначе выданные слова почти не выпадали бы.

ЧЕГО НЕ ДЕЛАЕТ. Не трогает никого, кроме названного счёта. Не выдаёт
отметку «выучено». Не меняет настройки, кроме состава занятия по просьбе
(`--channels`). Не лезет на прод: читает настройки через `app.config`,
который слушается `ENV_FILE`.

ЭТО ИНСТРУМЕНТ ДЛЯ РАБОЧЕЙ КОПИИ. На проде он исказил бы человеку
статистику: прогресс, которого не было, попадёт в шкалы и в отбор слов.

    ENV_FILE=.env.local .venv/Scripts/python.exe -m app.scripts.prepare_live_test 463491762
    ... -m app.scripts.prepare_live_test 463491762 --apply
    ... -m app.scripts.prepare_live_test 463491762 --apply --per-lang 20
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from sqlalchemy import func, select

from app.database.models import User, UserWord, Word, WordLangGroup
from app.database.session import AsyncSessionLocal
from app.services.language_service import LEARNABLE_LANGS
from app.services.quiz_service import CHANNEL_UNLOCK

logging.disable(logging.ERROR)

DEFAULT_PER_LANG = 12

# Сколько показов и верных выдать. Верных — столько, сколько требует самый
# строгий канал (речь), и ни одним больше: отметка «выучено» ставится за
# три подряд, а выученное слово из подбора почти выпадает.
SHOWS = 3
CORRECT = 2


async def _ready_now(session, user_id: int) -> dict[str, int]:
    """Сколько слов уже готово к речи по каждому языку."""
    need = max(CHANNEL_UNLOCK.values())
    rows = (await session.execute(
        select(UserWord.learning_lang, func.count())
        .where(UserWord.user_id == user_id, UserWord.times_correct >= need)
        .group_by(UserWord.learning_lang)
    )).all()
    return {lang: int(count) for lang, count in rows}


async def _pick(session, user_id: int, lang: str, limit: int) -> list[int]:
    """
    Канонические слова языка, по которым у человека ЕЩЁ НЕТ прогресса.

    Берутся слова с озвучкой по смыслу задачи — то есть любые
    канонические: озвучка полна по всем шести языкам, и отдельный отсев
    только запутал бы.
    """
    have = select(UserWord.word_id).where(
        UserWord.user_id == user_id, UserWord.learning_lang == lang
    )
    return list((await session.execute(
        select(Word.id)
        .join(WordLangGroup, (WordLangGroup.word_id == Word.id)
              & (WordLangGroup.lang == lang)
              & (WordLangGroup.is_canonical.is_(True)))
        .where(Word.id.notin_(have))
        .order_by(func.random())
        .limit(limit)
    )).scalars().all())


async def run(user_id: int, per_lang: int, apply: bool,
              channels: str | None) -> int:
    mode = "ПРАВКА" if apply else "только показ (для правки --apply)"
    print(f"Подготовка счёта {user_id} к ручному тесту — {mode}\n")

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user is None:
            print(f"счёта {user_id} в базе нет")
            return 1

        print(f"кто это: {user.first_name} @{user.username or '—'} · "
              f"{user.learning_lang}→{user.native_lang} · "
              f"{user.level.value if user.level else '—'} · "
              f"состав «{user.quiz_channels}» · "
              f"озвучка {'вкл' if user.audio_enabled else 'ВЫКЛ'}")

        before = await _ready_now(session, user_id)
        print("\nготово к речи СЕЙЧАС:")
        for lang in sorted(LEARNABLE_LANGS):
            print(f"   {lang}: {before.get(lang, 0)}")

        added = 0
        for lang in sorted(LEARNABLE_LANGS):
            have = before.get(lang, 0)
            if have >= per_lang:
                continue
            want = per_lang - have
            ids = await _pick(session, user_id, lang, want)
            if len(ids) < want:
                print(f"\n{lang}: свободных слов нашлось {len(ids)} из {want}")
            for word_id in ids:
                added += 1
                if apply:
                    session.add(UserWord(
                        user_id=user_id, word_id=word_id, learning_lang=lang,
                        times_shown=SHOWS, times_correct=CORRECT,
                        correct_streak=1, learned=False, last_seen_at=None,
                    ))

        if apply and channels:
            user.quiz_channels = channels
            user.audio_enabled = True
            print(f"\nсостав занятия выставлен в «{channels}», озвучка включена")

        if apply:
            await session.commit()
            after = await _ready_now(session, user_id)
            print("\nготово к речи ТЕПЕРЬ:")
            for lang in sorted(LEARNABLE_LANGS):
                print(f"   {lang}: {after.get(lang, 0)}")
            print(f"\nдобавлено слов: {added}")
        else:
            print(f"\nбудет добавлено слов: {added} "
                  f"(по {per_lang} на язык, чего не хватает)")
            print("ничего не менялось; для правки прогнать с --apply")

    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("user_id", type=int, help="telegram id счёта")
    ap.add_argument("--per-lang", type=int, default=DEFAULT_PER_LANG,
                    help="сколько слов держать готовыми к речи на язык")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--channels", default=None,
                    help="выставить состав занятия, например «tas»")
    args = ap.parse_args()
    return asyncio.run(
        run(args.user_id, args.per_lang, args.apply, args.channels)
    )


if __name__ == "__main__":
    sys.exit(main())
