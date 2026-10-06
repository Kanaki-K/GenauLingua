"""
Ищет ЛОЖНОГО ДРУГА в переводе: перевод построен на созвучии со словом
ряда, а не на его смысле.

Зачем. Блок 58 дал:

    de  Die Demonstranten riefen laute Parolen
    en  The prisoner was released on parole after five years

Немецкое `Parole` это лозунг, английское `parole` — условно-досрочное
освобождение. Фраза вышла осмысленная и грамматически безупречная, но
про совершенно другое. Такой перевод глазами заметить труднее всего:
не за что зацепиться, всё правильно.

Как ищется. Признак решаемый и чисто механический:

  · в примере на чужом языке стоит слово, написанное КАК СЛОВО РЯДА
    (`Parole` → `parole`);
  · а в словарной статье того же языка этого написания НЕТ
    (`slogan, watchword, password`).

Если слово — настоящий общий корень, оно стоит и в статье:
`Agenda` → `agenda`, `Symphonie` → `symphony`, `Diskriminierung` →
`discrimination`. Если же написание есть только в примере, а статья
переводит другими словами — значит пример поехал за созвучием.

Смотрим только языки на латинице (en, tr, pl): для русского и
украинского понадобилась бы транслитерация, а она сама по себе
источник ошибок.

Самопроверка идёт на выдуманных рядах: проверяется логика приметы.

    python -m app.scripts.scan_false_friend
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

WORD = re.compile(r"[A-Za-zÄÖÜäöüßÇĞİıŞşÂÎÛâîûĄĆĘŁŃÓŚŹŻąćęłńóśźż]+")
MIN_LEN = 5

LANGS = ("en", "tr", "pl")


def hit(word_de: str, example: str, gloss: str) -> bool:
    w = (word_de or "").strip().lower()
    if len(w) < MIN_LEN or not example or not gloss:
        return False
    words = {t.lower() for t in WORD.findall(example)}
    if w not in words:
        return False
    # то же написание в словарной статье значит общий корень, а не
    # ложного друга
    return w not in gloss.lower()


FAKE = [
    # ложный друг: написание есть в примере, в статье его нет
    ("Parole", "The prisoner was released on parole after five years",
     "slogan, watchword, password", True),
    # общий корень: написание есть и в статье
    ("Agenda", "We have a full agenda for this week",
     "agenda, list of topics", False),
    ("Symphonie", "Beethoven's ninth symphony is world-famous",
     "symphony", False),
    # слова ряда в примере вообще нет — примета молчит
    ("Hungersnot", "The terrible famine killed millions",
     "famine, starvation", False),
    # слово короче пяти букв не смотрим
    ("Kap", "We sailed around the Cape of Good Hope and kap",
     "cape, headland", False),
]


def selfcheck() -> None:
    for w, ex, gl, want in FAKE:
        got = hit(w, ex, gl)
        if got != want:
            print(f"САМОПРОВЕРКА УПАЛА: {w!r} ожидалось {want}, вышло {got}")
            sys.exit(1)
    print(f"самопроверка: {len(FAKE)} случаев разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = ", ".join(f"example_{l}, translation_{l}" for l in LANGS)
    with engine.connect() as conn:
        rows = conn.execute(text(
            f"SELECT id, word_de, {cols} FROM words "
            "WHERE word_de IS NOT NULL ORDER BY id")).all()

    print(f"прочитано рядов: {len(rows)}")
    found = []
    for r in rows:
        wid, w = r[0], r[1]
        for i, lang in enumerate(LANGS):
            ex, gl = r[2 + i * 2], r[3 + i * 2]
            if hit(w, ex, gl):
                found.append((wid, w, lang, gl, ex))

    print(f"переводов, построенных на созвучии: {len(found)}\n")
    for wid, w, lang, gl, ex in found:
        print(f"  {wid:>6}  {w:<22} {lang}")
        print(f"          статья: {gl}")
        print(f"          пример: {ex}")


if __name__ == "__main__":
    main()
