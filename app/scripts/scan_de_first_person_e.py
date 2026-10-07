"""
ГЕЙТ: «ich» плюс голая основа глагола — формы, которой в немецком нет.

Зачем понадобилось. Блок 7 второго прохода дал `Ich genieß die Ruhe`.
Это ровно предмет `scan_de_colloquial` — усечённое первое лицо, — и
примета промолчала, потому что основы `genieß` не было в её списке.
**Это ПЯТАЯ дыра в одном и том же месте того скрипта:** за проход там
находили то отсутствующую приставку, то регистр артикля, то основы на
`-ier`, то `sitz`. Каждый раз список дополняли по найденному примеру,
и каждый раз он протекал снова.

Причина не в небрежности, а в устройстве: список, собранный по
найденным примерам, покрывает только найденные примеры.

Поэтому здесь перечисления нет совсем. Правило берётся из грамматики, а
основы — из самой базы:

    у немецкого глагола первое лицо единственного числа ВСЕГДА
    кончается на «-e»

«ich mache», «ich sitze», «ich genieße», и у сильных тоже — «ich gebe»,
«ich nehme», «ich sehe». Это не стиль, в отличие от повелительного (см.
`scan_de_bare_imperative`, где голая основа — норма). Голого `ich mach`
в немецком нет, есть только разговорное усечение.

Исключения закрыты и перечислимы грамматикой, а не наблюдением: модальные
(`ich kann`, `soll`, `will`, `muss`, `darf`, `mag`), `ich bin`,
`ich weiß`, и разговорные `ich hab`/`ich tu`, у которых полная форма
существует отдельно (`habe`, `tue`) — их ловит `scan_de_colloquial`
по своему списку, здесь они не нужны.

Основы берутся из рядов с частью речи VERB: инфинитив минус «-en».
Так список не может промолчать о глаголе, который в базе есть.

Самопроверка обязательна: заведомо верные строки молчат, заведомо
усечённые ловятся, модальные и `bin`/`weiß` не трогаются.

    python -m app.scripts.scan_de_first_person_e
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Служебные слова и прилагательные берём ТОЙ ЖЕ функцией, что примета на
# повелительное, а не копией: в этом проекте дублированный разбор уже
# расходился четыре раза (см. HANDOVER §6з про expected_clips).
from app.scripts.scan_de_bare_imperative import function_words  # noqa: E402

# Формы, у которых «-e» в первом лице НЕ бывает. Список закрыт немецкой
# грамматикой: модальные глаголы, `sein`, `wissen`.
NO_E = {
    "kann", "soll", "will", "muss", "darf", "mag", "möchte",
    "bin", "weiß", "werde", "habe", "wäre", "hätte", "würde",
}

# `hab` и `tu` — разговорные усечения, у которых есть полная форма. Их
# предмет — scan_de_colloquial, здесь не дублируем.
COLLOQUIAL_ELSEWHERE = {"hab", "tu"}

ICH = re.compile(r"\bich\s+([A-Za-zÄÖÜäöüß]+)", re.IGNORECASE)


def stems_from_base(conn, skip: set[str]) -> dict[str, str]:
    """Основы глаголов базы → инфинитив. Без исключений по виду букв.

    `skip` — служебные слова и прилагательные базы. Нужны потому, что
    после «ich» часто стоит не глагол: `ich mein Auto`, `ich schon mal`,
    `ich schnell`, `ich fertig`. Основы `mein` (meinen), `schon`
    (schonen), `schnell` (schnellen), `fast` (fasten) существуют, и без
    вычитания примета дала 16 попаданий, из которых 11 ложных.
    """
    rows = conn.execute(
        text("SELECT word_de FROM words WHERE pos = 'VERB' AND word_de IS NOT NULL")
    ).scalars()
    out: dict[str, str] = {}
    for raw in rows:
        for inf in (p.strip() for p in str(raw).split(",")):
            inf = inf.replace("sich ", "").strip()
            if not inf or " " in inf or not inf.endswith("en"):
                continue
            stem = inf[:-2]
            if len(stem) < 3:
                continue
            low = stem.lower()
            if low in NO_E or low in COLLOQUIAL_ELSEWHERE or low in skip:
                continue
            out.setdefault(low, inf)
    return out


def hits(sentence: str, stems: dict[str, str]) -> list[tuple[str, str]]:
    """Слова после «ich», совпавшие с голой основой.

    Слово должно быть со СТРОЧНОЙ: немецкие глаголы пишутся со
    строчной, а слово с заглавной после «ich» — существительное
    («Nach dem Essen hatte ich Durchfall»).

    Чего примета НЕ видит: усечение в конце подчинённой фразы
    («bevor ich zur Arbeit geh»). Там глагол отделён от «ich»
    дополнениями, и позиция не помогает. Такие ряды находятся только
    чтением.
    """
    out = []
    for m in ICH.finditer(sentence or ""):
        raw = m.group(1)
        if raw[:1].isupper():
            continue
        word = raw.lower()
        if word in NO_E or word in COLLOQUIAL_ELSEWHERE:
            continue
        if word in stems:
            out.append((raw, stems[word]))
    return out


def selfcheck(stems: dict[str, str]) -> None:
    good = [
        "Ich mache das selber",          # полная форма
        "Ich genieße die Ruhe",
        "Ich gebe dir das Buch",         # сильный, но тоже с «-e»
        "Ich kann das nicht",            # модальный
        "Ich bin müde",
        "Ich weiß es nicht",
        "Ich will nach Hause",
        "Mach die Tür auf",              # повелительное — не предмет
        "Er macht das selber",           # третье лицо
        "Ich habe Hunger",
        "Nach dem Essen hatte ich Durchfall",   # существительное с заглавной
        "In der Zwischenzeit koche ich schon mal",  # `schon` — наречие базы
        "Wo kann ich mein Auto abstellen?",     # `mein` — местоимение базы
    ]
    bad = [
        "Ich genieß die Ruhe",
        "Ich mach das selber",
        "Ich sitz auf dem Stuhl",
        "Ich sag dir das nicht",
        "Ich zahl das nicht",
    ]
    errs = []
    for s in good:
        if hits(s, stems):
            errs.append(f"ложная тревога: {s!r} → {hits(s, stems)}")
    for s in bad:
        if not hits(s, stems):
            errs.append(f"пропущено: {s!r}")
    if errs:
        print("САМОПРОВЕРКА НЕ ПРОШЛА:")
        for e in errs:
            print("   ", e)
        sys.exit(1)
    print(f"самопроверка: {len(good)} правильных и {len(bad)} усечённых строк разобраны верно")


def main() -> None:
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        stems = stems_from_base(conn, function_words(conn))
        selfcheck(stems)
        print(f"основ глаголов из базы: {len(stems)}")
        rows = conn.execute(
            text(
                "SELECT id, word_de, example_de FROM words "
                "WHERE example_de IS NOT NULL ORDER BY id"
            )
        ).mappings().all()

    found = [
        (r["id"], r["word_de"], r["example_de"], h)
        for r in rows
        if (h := hits(r["example_de"], stems))
    ]

    print(f"\nпрочитано немецких примеров: {len(rows)}")
    print(f"с усечённым первым лицом: {len(found)}")
    for wid, word, ex, h in found:
        forms = ", ".join(f"{f} → {inf[:-2]}e" for f, inf in h)
        print(f"  {wid:>6}  {word:<22} {ex}   [{forms}]")

    if found:
        sys.exit(1)


if __name__ == "__main__":
    main()
