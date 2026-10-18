"""
Перенос словаря на прод (Н1, 16.10): все языки реестра доезжают целиком.

Прежде список колонок кончался польским, и перенос «проходил», привозя
словарь без it/es/fr/cs. Тест гоняет настоящий круг: выгрузка → порча базы
→ заливка, и смотрит, вернулись ли ячейки новых языков.
"""
import json

import pytest
from sqlalchemy import text

from app.scripts import wordbase_transfer as wt
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS
from tests.conftest import make_word

pytestmark = pytest.mark.asyncio


def test_every_language_of_the_registry_is_carried():
    for code in SUPPORTED_LANGS:
        assert LANGUAGES[code].word_attr in wt.CONTENT, code
        assert LANGUAGES[code].example_attr in wt.CONTENT, code


async def test_round_trip_restores_new_language_cells(session, tmp_path):
    words = [make_word(f"Wort{i}", it=f"parola{i}", cs=f"slovo{i}") for i in range(3)]
    session.add_all(words)
    await session.commit()

    dump = str(tmp_path / "wordbase.json")
    assert wt.export(dump) == 0

    # Порча: итальянское значение одного слова пропало
    await session.execute(text("update words set translation_it = null where id = :id"),
                          {"id": words[0].id})
    await session.commit()

    assert wt.load(dump, apply=True) == 0
    restored = (await session.execute(
        text("select translation_it from words where id = :id"), {"id": words[0].id}
    )).scalar()
    assert restored == "parola0"


async def test_dump_without_new_columns_is_refused(session, tmp_path):
    session.add(make_word("Wort"))
    await session.commit()
    dump = tmp_path / "old.json"
    assert wt.export(str(dump)) == 0

    data = json.loads(dump.read_text(encoding="utf-8"))
    for w in data["words"]:
        w.pop("translation_it")
    body = json.dumps({"words": data["words"], "overrides": data["overrides"]},
                      ensure_ascii=False, sort_keys=True, default=str)
    import hashlib

    data["sha256"] = hashlib.sha256(body.encode("utf-8")).hexdigest()
    dump.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    assert wt.load(str(dump), apply=True) == 1
