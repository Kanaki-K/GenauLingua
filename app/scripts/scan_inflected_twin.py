"""ПРИМЕТА: два ряда на один заголовок, но в РАЗНЫХ формах.

`scan_same_headword` сравнивает `word_de` строка в строку и потому видит
только точные повторы. Пара из блока 37 показала, что этого мало:

    heiter   (10716, B2)  «Er war in heiterer Stimmung trotz der Probleme»
    heiterem (11008, B2)  «Sie sprach in heiterem Ton über ihre Pläne»

Это один и тот же заголовок, второй — в дательном падеже. Строки не
совпадают, и прямая примета молчит. Значит её 375 заголовков — это НИЖНЯЯ
ГРАНИЦА класса, и здесь измерено, насколько нижняя.

КАК УСТРОЕНО ПРАВИЛО. Берём пары, где одна форма — строгий ПРЕФИКС
другой, а остаток стоит в списке немецких словоизменительных окончаний.
Без ограничения на окончание выходит 838 пар и почти весь улов — мусор
вроде `Abfall`/`abfallen` и `Absage`/`absagen`: это разные слова, а не
формы одного. Фильтр «та же часть речи И списки переводов пересекаются»
оставляет 83 пары, и они уже по делу.

ЗАМЕР: 83 пары, из них 13 с ПОЛНОСТЬЮ одинаковым списком ru:

    bezaubernd  (10423, B1) ~ bezaubernde (10943, C1)   3/3
    dritt        (7182, B2) ~ dritte      (13464, A2)   1/1
    dritt        (7182, B2) ~ dritte        (194, A1)   1/1
    dritt        (7182, B2) ~ dritter     (13515, A1)   1/1
    Friede      (16209, B2) ~ Frieden      (2484, B1)   3/3
    keine       (13269, A1) ~ keinen      (13306, A1)   3/3
    loyal       (10449, B1) ~ loyale      (11538, B1)   3/3
    rätselhaft   (8198, C2) ~ rätselhafte  (8655, C2)   3/3
    tschüs      (13901, A2) ~ tschüss       (945, A1)   3/3
    tu           (6265, A1) ~ tun           (946, A1)   2/2
    Weihnacht   (18841, C1) ~ Weihnachten  (1017, A1)   1/1
    will        (13274, A1) ~ willst      (13294, A1)   3/3
    zweit       (13436, A1) ~ zweite       (1087, A1)   1/1

ЧТО ЭТО ЗНАЧИТ, И ПОЧЕМУ ЭТО НЕ НОВЫЙ КЛАСС. Почти в каждой паре один
участник — голая словоформа, которой вообще нечего быть заголовком:
`heiterem`, `bezaubernde`, `dritt`, `lenk`, `mittler`, `glaub`, `geh`,
`komm`, `denk`, `guck`, `rühr`, `schnapp`, `überlass`, `dreh`. Это ровно
те ряды, что уже лежат в списке решений владельца как «ряды в форме, а не
в словарном виде» (~62 ряда). То есть два отдельных списка решений —
«повторы заголовков» и «заголовок не в словарной форме» — оказались ОДНИМ
классом, увиденным с двух сторон: голая форма всегда дубль своей же
леммы. Решать их надо одним правилом, а не двумя.

ЧТО ЗАКОННО И ОСТАЁТСЯ В ОСТАТКЕ. Часть пар — настоящие отдельные слова,
а не формы: `gern`/`gerne`, `nochmal`/`nochmals`, `öfter`/`öfters`,
`allein`/`alleine`, `spät`/`später`, `tschüs`/`tschüss` — в немецком
употребительны обе. И отдельно весь набор `kein`/`keine`/`keinem`/
`keinen`/`keines`/`keins`/`keiner` (как и `ein`/`einem`/`einer`/`eines`):
для склонения артиклей и местоимений это не дубли, а предмет урока.
Поэтому примета — ПОДСКАЗКА, и её остаток 83 назван здесь.

ОТМЕНЁННЫЙ ВАРИАНТ: СРАВНИВАТЬ БЕЗ УЧЁТА РЕГИСТРА. Выглядел разумно —
даёт 400 групп повторов вместо 375, то есть ещё 29. Замерено: ВСЕ 29 —
норма немецкого, где большая буква отличает существительное от глагола и
прилагательного: `Essen`/`essen`, `Leben`/`leben`, `Morgen`/`morgen`,
`Arm`/`arm`, `Gut`/`gut`, `Wagen`/`wagen`, `Sie`/`sie`. Ни одного
дефекта. Вариант отменён, а `scan_same_headword` подтверждена в том, что
сравнивает с учётом регистра.

ПРЕДЕЛ ПРИМЕТЫ, НАЗВАННЫЙ ПРЯМО. Правило берёт только пары «префикс +
окончание». Пары с ПЕРЕГЛАСОВКОЙ или с другим изменением внутри слова
(`Buch`/`Bücher`, `nehmen`/`nahm`) она не видит, потому что там форма не
начинается с леммы. Чтобы увидеть и их, нужен лексикон немецких форм; в
базе его нет, а перечислять руками — то самое перечисление, которое шесть
раз за проход покрывало только само себя.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from itertools import combinations

from sqlalchemy import create_engine, text

from app.config import settings
from app.services.language_service import _VARIANT_SPLIT_RE, _fold

# Немецкие словоизменительные окончания. Список намеренно короткий: он
# отсекает деривацию (`Abfall` → `abfallen`), оставляя словоизменение.
ENDINGS = frozenset((
    "e", "em", "en", "er", "es", "ere", "eren", "erem", "eres", "erer",
    "ste", "sten", "stem", "ster", "stes",
    "t", "te", "ten", "test", "tet", "st", "s", "n",
    "nd", "nde", "nden", "ndem", "nder", "ndes",
))

EXPECTED = 83


def tail_of(short: str, long: str) -> str | None:
    """Окончание, на которое long длиннее short, если это словоизменение."""
    if not short or not long or short == long or not long.startswith(short):
        return None
    tail = long[len(short):]
    return tail if tail in ENDINGS else None


def variants(cell: str | None) -> set[str]:
    return {
        _fold(p.strip())
        for p in _VARIANT_SPLIT_RE.split(cell or "")
        if p.strip()
    }


def selfcheck() -> None:
    cases = [
        # ПЛОХО: словоизменение, которое прямая примета не видит
        ("heiter", "heiterem", "em"),
        ("bezaubernd", "bezaubernde", "e"),
        ("will", "willst", "st"),
        ("Friede", "Frieden", "n"),
        # ХОРОШО: деривация, а не форма — остаток не окончание
        ("Abfall", "abfallen", None),
        ("Absage", "absagen", None),
        # ХОРОШО: форма не начинается с леммы — правило молчит честно
        ("Buch", "Bücher", None),
        # ХОРОШО: одинаковые строки — это дело scan_same_headword
        ("heiter", "heiter", None),
    ]
    bad = 0
    for short, long, want in cases:
        got = tail_of(short, long)
        if got != want:
            bad += 1
            print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {short}/{long} -> {got!r}, ждали {want!r}")
    if bad:
        sys.exit(1)
    print("самопроверка правила: 8 из 8")


def main() -> None:
    if "--selfcheck" in sys.argv:
        selfcheck()
        return

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, pos, level, translation_ru FROM words"
        )).mappings().all()

    by_word: dict[str, list] = defaultdict(list)
    for r in rows:
        by_word[(r["word_de"] or "").strip()].append(r)

    hits = []
    for a, b in combinations(sorted(by_word), 2):
        tail = tail_of(a, b) or tail_of(b, a)
        if not tail:
            continue
        short, long = (a, b) if len(a) < len(b) else (b, a)
        for ra in by_word[short]:
            for rb in by_word[long]:
                if ra["pos"] != rb["pos"]:
                    continue
                va, vb = variants(ra["translation_ru"]), variants(rb["translation_ru"])
                if va & vb:
                    hits.append((ra, rb, tail, len(va & vb), len(va | vb)))

    full = [h for h in hits if h[3] == h[4]]
    for ra, rb, tail, inter, union in sorted(hits, key=lambda h: -h[3] / h[4]):
        print(
            f"{ra['word_de']:>18} ({ra['id']}, {ra['level']})  ~  "
            f"{rb['word_de']:<18} ({rb['id']}, {rb['level']})  "
            f"-{tail}  {(ra['pos'] or '')[:4]}  пересечение {inter}/{union}"
        )

    print(f"\nвсего пар: {len(hits)}, с полностью одинаковым списком: {len(full)}")
    print(f"ожидаемый остаток: {EXPECTED} (см. разбор в docstring)")
    if len(hits) != EXPECTED:
        print("ВНИМАНИЕ: остаток изменился — разбери новые пары и обнови docstring")
        sys.exit(1)


if __name__ == "__main__":
    main()
