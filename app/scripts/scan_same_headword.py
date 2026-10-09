"""
Примета: один и тот же немецкий заголовок стоит в базе дважды.

ЗАЧЕМ. До блока 34 этот класс собирался по одной паре за блок:
`Ehepartner` (блок 69 первого прохода), `geheimnisvoll` (28),
`unterbringen` (30), `massiv` (31), `Vegetarier` (32), `anstrengen` и
`eisern` (34). Семь штук выглядели как россыпь случайностей.

Прямой замер показал, что класс на два порядка больше: **375 заголовков
встречаются больше одного раза** (360 групп по два ряда и 15 по три,
итого 405 пар).

КАК УЛОВ РАЗОБРАН. Из 405 пар:

    8 пар  — ПОЛНЫЙ ДУБЛЬ: совпадает и заголовок, и немецкий пример.
             Это ровно тот список из замера блока 24, и он уже в
             HANDOVER (п. 1b). Правило воспроизводится в точности.
    35 пар  — РАЗНЫЕ ЧАСТИ РЕЧИ. Законно: `arm` прилагательное и `arm`
             в составе другого ряда — разные слова.
    23 пары — списки переводов НЕ ПЕРЕСЕКАЮТСЯ. Законно: это разные
             значения одного написания.
    339 пар — та же часть речи И списки пересекаются, то есть оба ряда
             учат ОДНОМУ И ТОМУ ЖЕ.
    175 из них — пересечение полное или почти полное (общих значений не
             меньше, чем объединение минус одно).

ЧТО ЭТО ЗНАЧИТ. Вот как выглядят такие пары:

    Sohn     (847 A1 «Der Sohn ist groß»)
             (14973 A2 «Er hat zwei Söhne»)          ru: «сын» и «сын»
    Student  (892 A1)  / (9485 A2)                   ru: «студент» дважды
    Patient  (703 A1)  / (12515 A2)                  ru: «пациент, больной»
    Firma    (273 A1)  / (17791 B1)
    Junge    (1573 A2 «Der Junge spielt Fußball»)
             (14891 A1 «Die Jungs spielen Fußball»)

У `Junge` одна и та же фраза дана в единственном и множественном числе,
причём МНОЖЕСТВЕННОЕ отнесено к уровню НИЖЕ. Это не похоже на замысел
«встретить слово дважды по спирали»: уровни и ранги расставлены
несогласованно.

Больше похоже, что база собиралась слоями — ядро A1/A2 и более позднее
расширение по частотности, — и слои наложились.

ЧЕГО ПРИМЕТА НЕ РЕШАЕТ. Она не говорит, какой ряд из двух лишний, и
решать это не ей: удаление меняет размер базы, числа целостности и связи
`user_words`. Это решение владельца, и для него примета даёт список.

ПОЧЕМУ ЭТО НЕ ГЕЙТ. Законных пар в улове треть, и отличить их от лишних
можно только по смыслу: `arm` как прилагательное и `arm` в другом
значении — разные слова, а `Sohn` и `Sohn` — один.

    python -m app.scripts.scan_same_headword
"""

from __future__ import annotations

import sys
from collections import defaultdict
from itertools import combinations

from sqlalchemy import create_engine, text

from app.config import settings
from app.services.language_service import _VARIANT_SPLIT_RE, _fold


def variants(cell: str | None) -> set[str]:
    """Значения из ячейки перевода, со снятым регистром и диакритикой."""
    return {
        _fold(p.strip())
        for p in _VARIANT_SPLIT_RE.split(cell or "")
        if p.strip()
    }


def selfcheck() -> bool:
    """Разбор пары должен отличать разные значения от одного."""
    ok = True

    # Один смысл: списки совпадают
    if not (variants("сын") & variants("сын")):
        print("  ПЛОХО: одинаковые списки не признаны пересекающимися")
        ok = False

    # Разные смыслы: списки не пересекаются
    if variants("бедный, убогий") & variants("рука, кисть"):
        print("  ПЛОХО: разные списки признаны пересекающимися")
        ok = False

    # Регистр и диакритика не должны мешать
    if not (variants("Fırın") & variants("fırın")):
        print("  ПЛОХО: регистр помешал сравнению")
        ok = False

    print("  разбор пары отличает одно значение от разных" if ok
          else "  разбор сломан")
    return ok


def main() -> None:
    if not selfcheck():
        sys.exit(1)

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, pos, level, frequency_rank, example_de, "
            "translation_ru FROM words"
        )).mappings().all()

    by_word: dict[str, list] = defaultdict(list)
    for r in rows:
        by_word[r["word_de"]].append(r)
    groups = {w: v for w, v in by_word.items() if len(v) > 1}

    full, diff_pos, diff_sense, teach_same = [], [], [], []
    for word, items in groups.items():
        for a, b in combinations(items, 2):
            if (a["example_de"] or "") == (b["example_de"] or ""):
                full.append((word, a, b))
            elif a["pos"] != b["pos"]:
                diff_pos.append((word, a, b))
            else:
                va, vb = variants(a["translation_ru"]), variants(b["translation_ru"])
                if va & vb:
                    teach_same.append((word, a, b, len(va & vb), len(va | vb)))
                else:
                    diff_sense.append((word, a, b))

    pairs = len(full) + len(diff_pos) + len(diff_sense) + len(teach_same)
    near = [x for x in teach_same if x[3] >= x[4] - 1]

    print(f"\n=== заголовков больше одного раза: {len(groups)}, пар: {pairs} ===\n")
    print(f"  полный дубль (тот же немецкий пример):        {len(full)}")
    print(f"  разные части речи — законно:                  {len(diff_pos)}")
    print(f"  списки не пересекаются, разные значения:      {len(diff_sense)}")
    print(f"  учат ОДНОМУ (та же часть речи, списки общие):  {len(teach_same)}")
    print(f"      из них пересечение почти полное:          {len(near)}")

    print("\n--- пары с почти полным пересечением ---")
    for word, a, b, inter, union in sorted(near, key=lambda x: x[0]):
        print(f"  {word:24} {a['id']:6} [{a['level']}] / {b['id']:6} [{b['level']}]"
              f"   общих {inter} из {union}")
    print(f"\nвсего: {len(near)}")


if __name__ == "__main__":
    main()
