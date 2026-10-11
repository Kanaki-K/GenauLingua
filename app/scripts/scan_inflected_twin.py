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

ПРЕДЕЛ ПРИМЕТЫ, НАЗВАННЫЙ ПРЯМО. Правило не видит пар с ПЕРЕГЛАСОВКОЙ или
другим изменением ВНУТРИ слова (`Buch`/`Bücher`, `nehmen`/`nahm`): там
общего начала нет совсем. Чтобы увидеть и их, нужен лексикон немецких
форм; в базе его нет, а перечислять руками — то самое перечисление,
которое шесть раз за проход покрывало только само себя.

════════════════════════════════════════════════════════════════════════
РАСШИРЕНИЕ: ОБЩИЙ КОРЕНЬ, А НЕ ТОЛЬКО ПРЕФИКС (+23 пары, остаток 106)
════════════════════════════════════════════════════════════════════════

КАК НАШЁЛСЯ ПРОБЕЛ. Не замером, а уборкой. В корне репозитория лежал файл
`rename_later.txt` — 24 id, отложенные переименования заголовков. Перед
удалением проверено, в каком эти ряды состоянии: 23 из 24 давно стоят в
инфинитиве, файл отработан. Двадцать четвёртый — `gelobte` (14294), и он
неинфинитивная форма, рядом с которой в базе стоит `geloben` (14229) с тем
же смыслом. Прогон приметы по этому ряду: МОЛЧИТ.

ПОЧЕМУ МОЛЧАЛА. `tail_of` требует, чтобы короткая строка НАЧИНАЛА длинную.
У `geloben`/`gelobte` общий корень «gelob», но ни одна строка не начинается
с другой — каждая навесила своё окончание. Правило не ошибалось, оно было
структурно слепо к этой половине класса, и ни один прогон этого показать не
мог: примета не умеет сообщать о том, чего не ищет.

Добавлено `stem_tails`: наибольший общий префикс не короче MIN_STEM = 4,
оба остатка — окончания из того же ENDINGS, та же часть речи, списки
переводов пересекаются. Фильтры те же, что у префиксного правила, чтобы
счёт остался сравнимым. На трёх буквах общего начала правило начинает
сводить разные слова — отсюда порог 4.

ЗАМЕР: +23 пары, из них 6 с ПОЛНОСТЬЮ одинаковым списком ru. Все шесть —
личная форма глагола, стоящая заголовком рядом со своим инфинитивом:

    hassen       (10159, A2) ~ hasst        (10137, A2)  -en/t    2/2
    veranlassen   (7498, B2) ~ veranlasst    (7337, B2)  -en/t    3/3
    verkörpern    (8538, B2) ~ verkörpert    (7979, B2)  -n/t     3/3
    verwenden     (2061, A2) ~ verwendeten   (8408, C2)  -n/ten   3/3
    überrumpeln   (8690, C2) ~ überrumpelt   (8060, C2)  -n/t     2/2
    geloben      (14229, C2) ~ gelobte      (14294, C2)  -en/te   2/3

Это НЕ новый класс: те же голые словоформы в заголовке, что и в префиксной
половине, — просто увиденные с другой стороны. Значит число в списке
решений владельца было занижено: не 83 пары, а 106.

ЧТО В НОВОМ ОСТАТКЕ ЗАКОННО. `Galaxie`/`Galaxis` — обе формы словарные, но
ряды дублируют друг друга по смыслу (B1 и C1), и это решение о составе
базы. Набор `keins`/`keine`/`keinen`/`keinem`/`keines`/`keiner` добавил пар
по тому же основанию, что и раньше: склонение местоимения — предмет урока,
а не дубль. `selbst`/`selber`, `Pieps`/`Piepen` — настоящие отдельные
слова.

ПОЧЕМУ НЕ ПРАВЛЮ. Всё это состав базы, а не текст: убрать ряд — значит
решить, что слова в базе больше нет. Решение владельца, список в
`HANDOVER.md` §7.

УРОК, КОТОРЫЙ СТОИТ ПОМНИТЬ. Пробел нашёлся при УБОРКЕ рабочего файла, а
не прогоном примет. Прежде чем удалять список отложенного, проверь каждую
его строку по базе: отработанный файл подтвердит это сам, а неотработанная
строка укажет на то, чего правила не ищут.
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

EXPECTED = 106  # 83 префиксных + 23 с общим корнем, см. раздел ниже в docstring


MIN_STEM = 4


def tail_of(short: str, long: str) -> str | None:
    """Окончание, на которое long длиннее short, если это словоизменение."""
    if not short or not long or short == long or not long.startswith(short):
        return None
    tail = long[len(short):]
    return tail if tail in ENDINGS else None


def stem_tails(a: str, b: str) -> tuple[str, str] | None:
    """
    Два окончания на ОБЩЕМ корне, если ни одна форма не префикс другой.

    `tail_of` требует, чтобы короткая строка начинала длинную, и потому
    видит только пары «лемма + окончание» (`heiter` / `heiterem`). Пара
    `geloben` / `gelobte` ему недоступна структурно: корень общий
    («gelob»), но каждая форма навесила СВОЁ окончание, и ни одна строка
    не начинается с другой.

    Корень не короче MIN_STEM: на трёх буквах общего начала правило
    начинает сводить разные слова.
    """
    if not a or not b or a == b:
        return None
    n = 0
    for x, y in zip(a.lower(), b.lower()):
        if x != y:
            break
        n += 1
    if n < MIN_STEM:
        return None
    ta, tb = a[n:].lower(), b[n:].lower()
    if not ta or not tb:
        return None                  # это префиксный случай — дело tail_of
    if ta not in ENDINGS or tb not in ENDINGS:
        return None
    return ta, tb


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
    # Правило ОБЩЕГО КОРНЯ: ни одна форма не префикс другой.
    stem_cases = [
        # ПЛОХО: словоформенные двойники, которых префиксное правило не видит
        ("geloben", "gelobte", ("en", "te")),
        ("sollen", "sollten", ("en", "ten")),
        ("wundere", "wundert", ("e", "t")),
        ("verwechseln", "verwechselt", ("n", "t")),
        # ХОРОШО: общий корень короче MIN_STEM — разные слова
        ("tun", "tut", None),
        ("geh", "gern", None),
        # ХОРОШО: остаток не словоизменительное окончание
        ("Absage", "absagen", None),
        ("Freiheit", "Freizeit", None),
        # ХОРОШО: префиксный случай — это дело tail_of, здесь молчим
        ("heiter", "heiterem", None),
        # ХОРОШО: одинаковые строки — дело scan_same_headword
        ("geloben", "geloben", None),
    ]

    bad = 0
    for short, long, want in cases:
        got = tail_of(short, long)
        if got != want:
            bad += 1
            print(f"САМОПРОВЕРКА ПРОВАЛЕНА: tail_of {short}/{long} -> "
                  f"{got!r}, ждали {want!r}")
    for a, b, want_pair in stem_cases:
        got_pair = stem_tails(a, b)
        if got_pair != want_pair:
            bad += 1
            print(f"САМОПРОВЕРКА ПРОВАЛЕНА: stem_tails {a}/{b} -> "
                  f"{got_pair!r}, ждали {want_pair!r}")
    if bad:
        sys.exit(1)
    print(f"самопроверка правила: {len(cases) + len(stem_cases)} из "
          f"{len(cases) + len(stem_cases)}")


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
        if tail:
            short, long = (a, b) if len(a) < len(b) else (b, a)
        else:
            # ни одна форма не префикс другой: ищем ОБЩИЙ КОРЕНЬ
            pair = stem_tails(a, b)
            if not pair:
                continue
            short, long = a, b
            tail = f"{pair[0]}/{pair[1]}"
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
