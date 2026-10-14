"""
Ищет турецкое `idi` / `idiler` / `imiş`, написанное ОТДЕЛЬНЫМ словом.

Зачем. Блоки 60 и 61 дали это подряд пять раз: `korkutucu idi`,
`gizemli idi`, `sadık idi`, `Sarhoş idi`, `tartışmalı idi`. По-турецки
прошедшее время от «быть» пишется слитно, суффиксом: `korkutucuydu`,
`gizemliydi`, `sadıktı`, `Sarhoştu`, `tartışmalıydı`. Раздельное `idi`
в языке есть, но это книжная форма прошлого века; в живой речи и во
всей остальной базе стоит суффикс. Для базы, по которой учатся
говорить, это дефект: ученик заучивает фразу, которой турок не скажет.

Как ищется. Отдельное слово `idi`, `idiler` или `imiş` — регуляркой по
границе слова. Ложных срабатываний у приметы нет: эти три формы в
турецком отдельным словом больше ничего не значат.

Отдельно оговорка про `ise`. Оно того же корня, но это не прошедшее
время, а союз «а вот», «что касается», и пишется законно отдельно:
`İlk film sıkıcıydı, ikincisi ise çok heyecanlıydı`. Примета его
исключает.

Склейка. Суффикс выбирается по правилу гармонии гласных, и правило
детерминированное, поэтому примета его считает сама:

  * слово кончается гласной → `y` + гармоничная гласная + `d`:
    `fazla idi` → `fazlaydı`, `harika idi` → `harikaydı`;
  * кончается глухой согласной (p ç t k f h s ş) → `t`:
    `sadık idi` → `sadıktı`, `Sarhoş idi` → `Sarhoştu`;
  * иначе → `d`: `fikir idi` → `fikirdi`, `ciddi idi` → `ciddiydi`.

Гармоничная гласная берётся по последней гласной слова:
a/ı → ı, e/i → i, o/u → u, ö/ü → ü.

Склейка проверена самопроверкой на двенадцати парах. Но считать её
достаточной нельзя: примета предлагает форму, а подставлять её надо
глазами — в половине случаев вокруг `idi` есть и другие дефекты, и
беглая замена одного суффикса их законсервирует.

    python -m app.scripts.scan_tr_separate_idi
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

COPULA = re.compile(r"\b(idi|idiler|imiş)\b")

VOWELS = "aeıioöuüâî"
VOICELESS = "pçtkfhsş"
BACK_UNROUND = "aı"
FRONT_UNROUND = "ei"
BACK_ROUND = "ou"
FRONT_ROUND = "öü"


# Заимствования, у которых написание обещает заднюю гармонию, а слово
# берёт переднюю: `meşgul` → `meşguldü`, не `meşguldu`. Первый проход
# приметы ошибся ровно на этом слове, поэтому список здесь и стоит.
FRONT_EXCEPTIONS = {
    "meşgul", "rol", "gol", "alkol", "hol", "mobil", "normal", "lokal",
    "sosyal", "petrol", "kontrol", "metal", "sinyal", "profil", "stil",
    "usul", "mahsul", "kabul", "sual",
}


def harmony(word: str) -> str:
    """Гармоничная узкая гласная по последней гласной слова."""
    w = word.lower()
    if w in FRONT_EXCEPTIONS:
        # гармония передняя, а огубленность — по последней гласной:
        # `meşgul` → `meşguldü`, `normal` → `normaldi`
        for ch in reversed(w):
            if ch in BACK_ROUND or ch in FRONT_ROUND:
                return "ü"
            if ch in BACK_UNROUND or ch in FRONT_UNROUND:
                return "i"
    for ch in reversed(w):
        if ch in BACK_UNROUND:
            return "ı"
        if ch in FRONT_UNROUND:
            return "i"
        if ch in BACK_ROUND:
            return "u"
        if ch in FRONT_ROUND:
            return "ü"
    return "ı"


def glue(word: str, copula: str) -> str:
    """Склеивает слово с отдельным `idi`/`idiler`/`imiş`."""
    v = harmony(word)
    last = word[-1].lower()
    if copula == "imiş":
        head = ("y" if last in VOWELS else "") + "m" + v + "ş"
        return word + head
    tail = "ler" if copula == "idiler" else ""
    if last in VOWELS:
        # после гласной вставляется только буфер `y`, своей гласной у
        # него нет: `fazla` + `ydı`, а не `fazlayıdı`
        return word + "yd" + v + tail
    cons = "t" if last in VOICELESS else "d"
    return word + cons + v + tail


def suggest(example: str) -> str | None:
    """Склеенный вариант фразы, или None если приметы нет."""
    toks = example.split()
    out, changed = [], False
    for t in toks:
        bare = t.strip(".,;:!?–—")
        if bare in ("idi", "idiler", "imiş") and out:
            prev = out[-1]
            tailpunct = prev[len(prev.rstrip(".,;:!?")):]
            out[-1] = glue(prev.rstrip(".,;:!?"), bare) + tailpunct
            changed = True
            continue
        out.append(t)
    return " ".join(out) if changed else None


GLUE_CASES = [
    ("hakaret", "idi", "hakaretti"),
    ("fikir", "idi", "fikirdi"),
    ("fazla", "idi", "fazlaydı"),
    ("harika", "idi", "harikaydı"),
    ("sevimli", "idi", "sevimliydi"),
    ("sadık", "idi", "sadıktı"),
    ("Sarhoş", "idi", "Sarhoştu"),
    ("kirli", "idi", "kirliydi"),
    ("albay", "idi", "albaydı"),
    ("katı", "idi", "katıydı"),
    ("korkutucu", "idi", "korkutucuydu"),
    ("öğretmen", "idiler", "öğretmendiler"),
    # заимствования с передней гармонией — на них правило гласных врёт
    ("meşgul", "idi", "meşguldü"),
    ("normal", "idi", "normaldi"),
    ("alkol", "idi", "alkoldü"),
]

GOOD = [
    # `ise` — законный союз, не прошедшее время
    "İlk film sıkıcıydı, ikincisi ise çok heyecanlıydı",
    # суффикс уже на месте
    "Hava kasvetli ve griydi",
    "Sarhoştu ve zorlukla yürüyebiliyordu",
]
BAD = [
    "Hava kasvetli ve gri idi",
    "Onun cevabı kaba ve sert idi",
    "Tanı beyin tümörü idi",
]


def selfcheck() -> None:
    for word, cop, want in GLUE_CASES:
        got = glue(word, cop)
        if got != want:
            print(f"САМОПРОВЕРКА УПАЛА: {word} + {cop} дало {got!r}, "
                  f"а надо {want!r}")
            sys.exit(1)
    for s in GOOD:
        if suggest(s):
            print(f"САМОПРОВЕРКА УПАЛА: ложное срабатывание на {s!r}")
            sys.exit(1)
    for s in BAD:
        if not suggest(s):
            print(f"САМОПРОВЕРКА УПАЛА: пропущено {s!r}")
            sys.exit(1)
    print(f"самопроверка: {len(GLUE_CASES)} склеек, {len(GOOD)} правильных "
          f"и {len(BAD)} испорченных строк разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_tr FROM words "
            "WHERE example_tr IS NOT NULL ORDER BY id")).all()

    print(f"прочитано турецких примеров: {len(rows)}")
    found = [(i, w, e, s) for i, w, e in rows if (s := suggest(e))]
    print(f"с отдельным «idi»: {len(found)}\n")
    for i, w, e, s in found:
        print(f"  {i:>6}  {w}")
        print(f"      было:  {e}")
        print(f"      надо:  {s}")


if __name__ == "__main__":
    main()
