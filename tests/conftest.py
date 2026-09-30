"""
Фикстуры для тестов.

БД поднимается отдельно от рабочей:
    docker compose -f docker-compose.test.yml up -d

Переопределить адрес можно через TEST_DATABASE_URL.
"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Настройки должны быть в окружении ДО импорта app.config,
# иначе pydantic подхватит рабочий .env и тесты пойдут в боевую БД.
TEST_DSN = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://test_user:test_pass@localhost:5433/genaulingua_test",
)
_async_dsn = TEST_DSN.replace("postgresql://", "postgresql+asyncpg://")
_sync_dsn = TEST_DSN.replace("postgresql://", "postgresql+psycopg2://")

os.environ["DATABASE_URL"] = _async_dsn
os.environ["DATABASE_URL_SYNC"] = _sync_dsn
os.environ.setdefault("BOT_TOKEN", "0:test")
os.environ.setdefault("ADMIN_USER", "1")

import pytest  # noqa: E402
import pytest_asyncio  # noqa: E402
from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: E402
from sqlalchemy.pool import NullPool  # noqa: E402

from app.database.enums import CEFRLevel, PartOfSpeech  # noqa: E402
from app.database.models import Base, User, Word  # noqa: E402


@pytest.fixture(scope="session")
def migrated_db():
    """Прогнать alembic upgrade head один раз на весь прогон."""
    env = {**os.environ, "DATABASE_URL": _async_dsn, "DATABASE_URL_SYNC": _sync_dsn}
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(
            "alembic upgrade head упал — тестовая БД поднята?\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return True


@pytest_asyncio.fixture
async def engine(migrated_db):
    # Движок создаётся на каждый тест: asyncpg привязывает соединения
    # к event loop, а у каждого теста он свой.
    eng = create_async_engine(_async_dsn, poolclass=NullPool)
    yield eng
    await eng.dispose()


_TRUNCATE_SQL = text(
    "TRUNCATE TABLE "
    "  monthly_quiz_events, monthly_awards, monthly_stats, monthly_seasons,"
    "  win_streaks, translation_reports, quiz_questions, quiz_sessions,"
    "  user_words, word_lang_groups, words, users "
    "RESTART IDENTITY CASCADE"
)


@pytest_asyncio.fixture
async def session(engine):
    """
    Чистая сессия на каждый тест. Таблицы чистятся до теста, чтобы порядок
    выполнения не влиял на результат.

    Очистка идёт отдельным соединением: если делать её из той же сессии,
    которую потом отдаём тесту, незакрытая транзакция предыдущего теста
    встаёт в блокировку с TRUNCATE следующего.
    """
    async with engine.begin() as conn:
        await conn.execute(_TRUNCATE_SQL)

    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as s:
        try:
            yield s
        finally:
            await s.rollback()


@pytest_asyncio.fixture
async def user(session):
    u = User(
        id=1000,
        first_name="Tester",
        interface_language="ru",
        learning_lang="de",
        native_lang="ru",
        reverse_mode=False,
    )
    session.add(u)
    await session.commit()
    return u


async def build_groups(session, langs=None):
    """
    Пересобрать word_lang_groups для засеянных слов.

    Логика синхронная (её же использует миграция), поэтому прокидываем
    через run_sync.
    """
    from app.services.word_groups import build_groups as _build

    await session.commit()
    await session.run_sync(lambda s: _build(s.connection(), langs))
    await session.commit()


def make_word(
    word_de: str,
    *,
    level: CEFRLevel = CEFRLevel.A1,
    pos: PartOfSpeech = PartOfSpeech.NOUN,
    article: str | None = None,
    ru: str | None = None,
    uk: str | None = None,
    en: str | None = None,
    tr: str | None = None,
    pl: str | None = None,
    translation_pl: str | None = None,
    example_pl: str | None = None,
    frequency_rank: int | None = None,
    category: str | None = None,
) -> Word:
    """Слово с переводами на все языки — по умолчанию производные от word_de."""
    # translation_pl как псевдоним pl: в тестах читаемее указывать колонку
    polish = translation_pl if translation_pl is not None else pl
    return Word(
        word_de=word_de,
        article=article,
        pos=pos,
        level=level,
        category=category,
        frequency_rank=frequency_rank,
        translation_ru=ru if ru is not None else f"{word_de}_ru",
        translation_uk=uk if uk is not None else f"{word_de}_uk",
        translation_en=en if en is not None else f"{word_de}_en",
        translation_tr=tr if tr is not None else f"{word_de}_tr",
        translation_pl=polish if polish is not None else f"{word_de}_pl",
        example_de=f"Beispiel {word_de}",
        example_ru=f"пример {word_de}",
        example_uk=f"приклад {word_de}",
        example_en=f"example {word_de}",
        example_tr=f"ornek {word_de}",
        example_pl=example_pl if example_pl is not None else f"przyklad {word_de}",
    )
