"""
Ищет ряд, где заголовок — ГЛАГОЛ БЕЗ ПРИСТАВКИ, а пример показывает
приставочный.

Зачем. Блоки 65 и 66 дали это дважды подряд, и оба раза с настоящим
дефектом в немецком:

    ряд  hecken
    de   Sie hecken einen Plan gegen mich aus      → aushecken

    ряд  riegeln
    de   Er riegelte die Tür von innen ab          → abriegeln

`hecken` значит «плодиться» о животных, `aushecken` — «замышлять»; все
пять переводов перевели второе. `riegeln` и `abriegeln` различаются
меньше, но ряд всё равно учит не тому слову, которое назван.

Это третья разновидность того же, что `Skalp`/`Skalpell` в блоке 64 и
`Quell`/`Quelle` там же: заголовок и пример про разные слова. У
существительных подмена прилипает хвостом, у глаголов — приставкой, и
приставка в немецком ОТДЕЛЯЕТСЯ и уезжает в конец фразы. Поэтому
`scan_de_headword_swap`, который смотрит слова, начинающиеся с
заголовка, такие ряды не видит в принципе.

Как ищется. Заголовок — глагол, и ни одна известная приставка не
является его началом. В примере есть форма этого глагола И отдельная
частица в самом конце фразы. Тогда в примере приставочный глагол.

Три оговорки, без которых примета тонет в ложных. Сырой вариант дал 46
попаданий, из них 24 ложных, и все по одной из трёх причин:

  1. частица принадлежит ДРУГОМУ глаголу в соседней части фразы:
     `Ich muss meinen Reisepass erneuern, bald läuft er ab` — `ab` от
     `ablaufen`, а не от `erneuern`. Отсюда запрет на запятую в примере;
  2. слово только выглядит частицей, а на деле существительное:
     `Der Baum versperrt den Weg`, `Wir veranstalten ein Fest`. Отсюда
     проверка регистра: `Weg` с большой буквы — не частица;
  3. устойчивое наречие: `hin und her`, `vor sich hin`, `schon
     wieder`, `tanzen zusammen`. Отсюда стоп-список `wieder` и
     `zusammen` и запрет на `sich` перед частицей.

Что остаётся. 29 рядов. Шесть из них всё равно ложные, и оговорка
номер один их не берёт: `Er stolperte über eine Wurzel und fiel hin`,
`Sie blinzelt in die Sonne und schaut mich an` — две части фразы без
запятой, соединённые «und», и частица от второго глагола. Ловить это —
значит разбирать немецкое предложение на составляющие, а для этого
нужен синтаксический разбор, которого у базы нет. Шесть ложных из
двадцати девяти — честная цена короткого списка на прочтение.

По-настоящему СЛОМАНЫ из них два:

    2966  Ich versende das Paket heute ab      → versenden ИЛИ absenden,
                                                 но не оба сразу
    9945  Ich tilge meine Schulden langsam ab  → `ab` здесь лишнее

Остальные двадцать не сломаны: `Ich presse die Zitrone aus`, `Ich
zünde eine Kerze an`, `Stell die Tasche hier hin` — фразы верные, но
учат `auspressen`, `anzünden`, `hinstellen`, а ряд назван `pressen`,
`zünden`, `stellen`. Это тот же мягкий случай, что семь составных
существительных из блока 64: не дефект, а вопрос к владельцу, и потому
примета выводит их отдельным списком и гейтом не становится.

    python -m app.scripts.scan_de_verb_prefix
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+")

PARTICLES = {
    "ab", "an", "auf", "aus", "bei", "ein", "mit", "nach", "vor", "zu",
    "zurück", "her", "hin", "los", "fest", "rein", "raus", "runter",
    "hoch", "durch", "um", "über", "unter", "entgegen", "gegenüber",
    "vorbei", "voraus", "weiter", "empor", "nieder", "heraus", "hinaus",
    "herein", "hinein", "weg",
}

# Слишком часто просто наречия, а не приставки: `schon wieder`,
# `tanzen zusammen`.
NOT_PARTICLE = {"wieder", "zusammen"}

# Сломанные ряды: приставка в примере лишняя или противоречит заголовку.
BROKEN = {2966, 9945}


def bare_verb(hw: str) -> str | None:
    h = (hw or "").strip().lower()
    if not h.endswith(("en", "ern", "eln")):
        return None
    if any(h.startswith(p) and len(h) > len(p) + 2 for p in PARTICLES):
        return None          # заголовок сам приставочный — не наш случай
    return h


def trailing_particle(example: str) -> str | None:
    if "," in example or ";" in example:
        return None          # частица может принадлежать другой части фразы
    toks = WORD.findall(example)
    if len(toks) < 3:
        return None
    last = toks[-1]
    if last[0].isupper():
        return None          # `den Weg`, `ein Fest` — существительные
    low = last.lower()
    if low not in PARTICLES or low in NOT_PARTICLE:
        return None
    if toks[-2].lower() == "sich":
        return None          # `vor sich hin`
    return low


def hit(hw: str, example: str) -> str | None:
    h = bare_verb(hw)
    if not h or not example:
        return None
    p = trailing_particle(example)
    if not p:
        return None
    stem = h[:-2]
    toks = WORD.findall(example)
    if not any(t.lower().startswith(stem) for t in toks):
        return None
    return p


def selfcheck() -> None:
    cases = [
        # настоящий случай: заголовок без приставки, частица в конце
        ("hecken", "Sie hecken einen Plan gegen mich aus", "aus"),
        ("pressen", "Ich presse die Zitrone aus", "aus"),
        # запятая: частица от другого глагола
        ("erneuern",
         "Ich muss meinen Reisepass erneuern bald läuft er ab".replace(
             " bald", ", bald"), None),
        # существительное, а не частица
        ("versperren", "Der Baum versperrt den Weg", None),
        ("veranstalten", "Wir veranstalten ein Fest", None),
        # устойчивое наречие
        ("weinen", "Das Baby weint schon wieder", None),
        ("murmeln", "Er murmelt etwas vor sich hin", None),
        # заголовок сам приставочный — не наш случай
        ("aufstehen", "Ich stehe um sieben auf", None),
    ]
    for hw, ex, want in cases:
        got = hit(hw, ex)
        if got != want:
            print(f"САМОПРОВЕРКА УПАЛА: {hw} / {ex!r} дало {got!r}, "
                  f"а надо {want!r}")
            sys.exit(1)
    print(f"самопроверка: {len(cases)} пар заголовок-пример разобраны "
          f"верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_de FROM words "
            "WHERE example_de IS NOT NULL AND pos = 'VERB' "
            "ORDER BY id")).all()

    print(f"прочитано рядов VERB: {len(rows)}")
    broken, soft = [], []
    for wid, hw, ex in rows:
        p = hit(hw, ex)
        if not p:
            continue
        (broken if wid in BROKEN else soft).append((wid, hw, p, ex))

    print(f"сломанных: {len(broken)}")
    for wid, hw, p, ex in broken:
        print(f"  {wid:>6}  {hw:<22} [{p}]  {ex}")

    print(f"\nпример учит приставочный глагол, а ряд назван простым: "
          f"{len(soft)}")
    print("(не дефект: фраза верна, но слово в ней другое — "
          "решать владельцу)")
    for wid, hw, p, ex in soft:
        print(f"  {wid:>6}  {hw:<22} [{p}]  {ex}")


if __name__ == "__main__":
    main()
