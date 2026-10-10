"""
ДЕВЯТЫЙ ГЕЙТ. Немецкий пример противоречит грамматике собственного ряда.

Две проверки одного семейства, обе формальные и обе нашлись в блоке 52.

════════════════════════════════════════════════════════════════════════
ПРОВЕРКА A: артикль в примере не того рода, что артикль ряда.
════════════════════════════════════════════════════════════════════════

    Sellerie (11963) article='der', а пример «Ich schneide DIE Sellerie»

Проверяются только ОДНОЗНАЧНЫЕ формы:

    den X  — только мужской (винительный)
    das X  — только средний
    die X  — женский или МНОЖЕСТВЕННОЕ число

ЗАМЕР: 7250 существительных с артиклем, расхождений 5. И все пять
законны — потому что у «die X» есть второе чтение, множественное:

    Daumen       (1323)  «Ich drücke dir die Daumen»     — оба больших пальца
    Goldbarren   (9925)  «Er versteckte die Goldbarren»  — слитки
    Zügel       (17234)  «Der Reiter hält die Zügel»     — поводья
    Sommerferien (9572)  «In den Sommerferien»           — plurale tantum

У всех четырёх множественное СОВПАДАЕТ с единственным, потому что они на
-en и -el. Отсюда отсечка: существительные на -en, -el, -er, -chen, -lein
из проверки исключены по построению, а не по списку.

Пятый, `Sellerie`, остаётся — и он тоже законен: Дуден даёт ему ОБА рода,
«der Sellerie» и «die Sellerie». Исключён по id с этой причиной.

После отсечки остатка нет, поэтому проверка — ГЕЙТ: ошибка в роде
существительного для базы изучения немецкого один из самых дорогих
дефектов, и ловится она даром.

════════════════════════════════════════════════════════════════════════
ПРОВЕРКА B: субстантивированное прилагательное склонено неверно.
════════════════════════════════════════════════════════════════════════

    Kongressabgeordneter (16796) «DER KongressabgeordnetER sprach»

По-немецки субстантивированное прилагательное в мужском именительном
берёт СЛАБОЕ «-e» после определённого определителя и СИЛЬНОЕ «-er» после
неопределённого:

    der Abgeordnete      ein Abgeordneter
    der Vorsitzende      mein Vorgesetzter

ПОЧЕМУ ЭТО НЕ ПРИДИРКА. База делает это ПРАВИЛЬНО 26 раз из 27, и её
собственная норма и есть довод:

    Abgeordneter   (16322) «DER AbgeordnetE sprach»            ✓
    Beamter         (8921) «DER BeamtE beim Rathaus»            ✓
    Freiwilliger   (11130) «DER FreiwilligE hilft»              ✓
    Gelehrter       (9582) «DER GelehrtE verfügte»              ✓
    Polizeibeamter (16642) «DER PolizeibeamtE kontrollierte»    ✓
    Vorsitzender    (8861) «DER VorsitzendE leitet»             ✓
    Angehöriger    (15334) «EIN AngehörigER der Familie»        ✓
    Verwandter     (15108) «MEIN VerwandtER besucht»            ✓
    Vorgesetzter    (8926) «MEIN VorgesetztER möchte»           ✓

Выпадает ровно один ряд. Это тот же приём, что в блоках 48, 49 и 50
(правило 1r): расхождение внутри базы решает вопрос дешевле внешней
нормы.

Класс в базе ЗАКРЫТЫЙ — субстантивированных прилагательных-заголовков 27,
они перечислены основами в `ADJ_NOUN_STEMS`. Проверка смотрит не на
заголовок, а на сам пример: какой определитель и какое окончание рядом
стоят. Поэтому `Vorgesetzte` (8837) с примером «Mein Vorgesetzter ist
nett» проходит — форма в примере не обязана совпадать с заголовком.

    python -m app.scripts.scan_de_declension
    python -m app.scripts.scan_de_declension --selfcheck
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# ─── A: род ──────────────────────────────────────────────────────────
# Формы, у которых множественное совпадает с единственным: «die Daumen»
# может быть и женским единственным, и мужским множественным.
PLURAL_LIKE_ENDINGS = ("en", "el", "er", "chen", "lein")

# 11963 Sellerie — Дуден даёт оба рода: «der Sellerie», также «die Sellerie».
# 7791  Risse — заголовок стоит во МНОЖЕСТВЕННОМ числе при артикле «der»
#       (единственное «der Riss»). «Die Risse» в примере верно; дефект в
#       самой паре заголовок/артикль, и он в куче решений владельца
#       («~62 ряда с несловарной формой заголовка», HANDOVER). Правка
#       здесь означала бы переименование ряда — это не моё решение.
GENDER_OK: frozenset[int] = frozenset({11963, 7791})

_ART_RE_CACHE: dict[str, re.Pattern[str]] = {}


def gender_clash(word: str, article: str, example: str) -> str | None:
    """Однозначное расхождение рода между артиклем ряда и примером."""
    art = (article or "").strip().lower()
    if art not in ("der", "die", "das"):
        return None

    # Эта проверка идёт ДО отсечки по окончаниям нарочно: отсечка нужна
    # из-за чтения «die X» как множественного, а для «der X» в НАЧАЛЕ
    # фразы множественного чтения нет вовсе. `Karnickel` на -el иначе
    # проваливался бы сквозь отсечку — это нашла самопроверка.
    if art == "das":
        start = re.compile(
            r"(?:^|(?<=[.!?–—]\s))\s*der\s+" + re.escape(word) + r"\b",
            re.IGNORECASE,
        )
        match = start.search(example or "")
        if match:
            return (
                f"{match.group(0).strip()!r} при артикле 'das': "
                "«der» в начале фразы не может быть генитивом"
            )

    if word.endswith(PLURAL_LIKE_ENDINGS):
        return None
    pattern = _ART_RE_CACHE.get(word)
    if pattern is None:
        # ВАЖНО: без IGNORECASE примета пропускает артикль в начале фразы
        # («Das Tisch ist neu»). Эту дыру нашла собственная самопроверка.
        pattern = re.compile(
            r"\b(der|die|das|den)\s+" + re.escape(word) + r"\b",
            re.IGNORECASE,
        )
        _ART_RE_CACHE[word] = pattern
    for match in pattern.finditer(example or ""):
        found = match.group(1).lower()
        if found == "den" and art != "der":
            return f"{match.group(0)!r} при артикле {art!r}: «den» только мужской"
        if found == "das" and art != "das":
            return f"{match.group(0)!r} при артикле {art!r}: «das» только средний"
        if found == "die" and art == "der":
            return f"{match.group(0)!r} при артикле {art!r}: «die» не мужской"
    return None


# ─── B: слабое и сильное окончание ───────────────────────────────────
# Основы субстантивированных прилагательных-заголовков базы.
#
# ПОЛНОТА ПРОВЕРЕНА ЗАМЕРОМ (блок 56), а не на глаз. Запрос искал пары
# заголовков <основа>e и <основа>er, присутствующие в базе одновременно,
# и выдал 31 кандидата. Восемь из них оказались настоящими и в списке
# отсутствовали — они добавлены ниже отдельной группой. Остальные 23 —
# шум от неродственных пар существительных: «Apotheke/Apotheker»,
# «Geige/Geiger», «Lehre/Lehrer», «Miete/Mieter», «Rolle/Roller»,
# «Wunde/Wunder». Признак «в базе есть обе формы» сам по себе класс не
# определяет, и это стоит помнить, если список придётся пополнять снова.
ADJ_NOUN_STEMS = (
    "Kongressabgeordnet", "Abgeordnet", "Polizeibeamt", "Angehörig",
    "Beamt", "Bekannt", "Erwachsen", "Freiwillig", "Gelehrt", "Gesetzlos",
    "Jugendlich", "Unschuldig", "Verwandt", "Vorgesetzt", "Vorsitzend",
    "Arbeitslos", "Betroffen", "Verletzt", "Fremd", "Krank",
    # добавлено замером полноты, блок 56
    "Angeklagt", "Angestellt", "Gefangen", "Geliebt", "Gesandt",
    "Geschworen", "Verbündet",
)
# «Gläubig» в список НЕ входит, и это важный капкан. Замер полноты выдал
# его как кандидата, я добавил — и гейт тут же упал на `Gläubiger`
# (17836) «Der Gläubiger forderte sein Geld zurück». Но это ВЕРНЫЙ
# немецкий: «der Gläubiger» значит КРЕДИТОР и является обычным
# существительным на -er, а не сильной формой прилагательного. Верующий
# — отдельный ряд `Gläubige` (14791).
#
# ОТСЮДА ПРАВИЛО ДЛЯ ПОПОЛНЕНИЯ СПИСКА: замер полноты необходим, но
# недостаточен. Каждого кандидата надо проверить на ОМОНИМИЧНОЕ имя
# деятеля на -er. Остальные семь добавленных проверены: ни у
# «Angeklagter», ни у «Angestellter», ни у «Gefangener», «Geliebter»,
# «Gesandter», «Geschworener», «Verbündeter» самостоятельного значения
# на -er нет — это только сильные формы.
_STEMS = "|".join(sorted(ADJ_NOUN_STEMS, key=len, reverse=True))

# После определённого определителя — слабое «-e», сильное «-er» неверно.
_STRONG_AFTER_DEF = re.compile(
    r"\b(?:Der|der|Dieser|dieser|Jeder|jeder|Welcher|welcher|Jener|jener)\s+"
    r"(?:" + _STEMS + r")er\b"
)
# После неопределённого — сильное «-er», слабое «-e» неверно.
_WEAK_AFTER_INDEF = re.compile(
    r"\b(?:Ein|ein|Mein|mein|Dein|dein|Sein|sein|Unser|unser|Kein|kein)\s+"
    r"(?:" + _STEMS + r")e\b"
)


def declension_clash(example: str) -> str | None:
    text_ = example or ""
    match = _STRONG_AFTER_DEF.search(text_)
    if match:
        return f"{match.group(0)!r}: после определённого определителя нужно «-e»"
    match = _WEAK_AFTER_INDEF.search(text_)
    if match:
        return f"{match.group(0)!r}: после неопределённого нужно «-er»"
    return None


def selfcheck() -> int:
    good_gender = [
        ("Daumen", "der", "Ich drücke dir die Daumen"),
        ("Zügel", "der", "Der Reiter hält die Zügel fest"),
        ("Tasche", "die", "Die Tasche ist schwer"),
        ("Haus", "das", "Das Haus ist alt"),
        ("Tisch", "der", "Ich stelle das Glas auf den Tisch"),
        # «der X» при женском артикле — датив, законно и встречается 137 раз
        ("Garage", "die", "Das Auto steht in der Garage"),
        # «der X» при среднем, но НЕ в начале фразы — генитив множественного
        ("Arbeitslager", "das", "Die Geschichte der Arbeitslager ist dunkel"),
    ]
    bad_gender = [
        ("Sellerie", "der", "Ich schneide die Sellerie klein"),
        ("Tasche", "die", "Ich nehme den Tasche mit"),
        ("Tisch", "der", "Das Tisch ist neu"),
        ("Karnickel", "das", "Der Karnickel sitzt in seinem Käfig"),
    ]
    good_decl = [
        "Der Abgeordnete sprach im Parlament",
        "Mein Vorgesetzter ist nett",
        "Ein Angehöriger der Familie war im Krieg gefallen",
        "Die Abgeordnete hat im Parlament gestimmt",
        "Die Jugendlichen treffen sich hier",
    ]
    bad_decl = [
        "Der Kongressabgeordneter sprach vor dem Plenum",
        "Der Vorsitzender leitet die Versammlung",
        "Ein Abgeordnete sprach im Parlament",
    ]
    failures = 0
    for word, art, ex in good_gender:
        got = gender_clash(word, art, ex)
        if got:
            print(f"GOOD помечен (род): {ex!r} -> {got}")
            failures += 1
    for word, art, ex in bad_gender:
        if not gender_clash(word, art, ex):
            print(f"BAD не помечен (род): {ex!r}")
            failures += 1
    for ex in good_decl:
        got = declension_clash(ex)
        if got:
            print(f"GOOD помечен (склонение): {ex!r} -> {got}")
            failures += 1
    for ex in bad_decl:
        if not declension_clash(ex):
            print(f"BAD не помечен (склонение): {ex!r}")
            failures += 1
    if failures:
        print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {failures}")
        return 1
    print(
        f"самопроверка: род {len(good_gender)}+{len(bad_gender)}, "
        f"склонение {len(good_decl)}+{len(bad_decl)} — различены"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()

    if args.selfcheck:
        return selfcheck()

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, article, pos::text AS pos, example_de "
            "FROM words ORDER BY id"
        )).mappings().all()

    gender_hits: list[tuple[int, str, str]] = []
    decl_hits: list[tuple[int, str, str]] = []
    for row in rows:
        word = (row["word_de"] or "").strip()
        example = row["example_de"] or ""
        if row["pos"] == "NOUN" and word and row["id"] not in GENDER_OK:
            why = gender_clash(word, row["article"] or "", example)
            if why:
                gender_hits.append((row["id"], word, why))
        why = declension_clash(example)
        if why:
            decl_hits.append((row["id"], word, why))

    for wid, word, why in gender_hits:
        print(f"РОД        {wid:>6}  {word:<24} {why}")
    for wid, word, why in decl_hits:
        print(f"СКЛОНЕНИЕ  {wid:>6}  {word:<24} {why}")

    total = len(gender_hits) + len(decl_hits)
    print(f"\nвсего: {total} (род {len(gender_hits)}, склонение {len(decl_hits)})")
    if total:
        print("ГЕЙТ: пример противоречит грамматике своего же ряда")
        return 1
    print("ЧИСТО")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
