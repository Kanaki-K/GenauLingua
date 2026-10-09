"""
Примета: рассказчик в ряде то мужчина, то женщина.

Зачем. Немецкий в прошедшем рода не показывает («Ich bin heimgekommen»,
«Am Samstag bin ich frei»), а русский и украинский — показывают. База
по умолчанию пишет мужской род: «Я очень устал», «Я влюблён», «Я
свободен», «Я вынужден работать дольше». Но не везде: блок 7 дал
`Samstag` («я свободнА» против `Freitag` «я свободеН»), блок 8 —
`Zunge` («Я обожглА язык»). Два ряда — класс.

Почему это дефект, а не придирка. Ученик один, и карточки идут одна за
другой: в одной он мужчина, в следующей женщина. А озвучка читается
ОДНИМ голосом на язык — расхождение слышно.

Чего примета НЕ требует. Два вида законного женского рода:

  • **предмет ряда сам отмечен по полу** — платье, колготки, лак для
    ногтей. Решение записано в `fix_pass2_block_08`;
  • **НЕМЕЦКИЙ САМ ЖЕНСКОГО РОДА.** Это выяснилось в блоке 11 и важнее
    первого: у `Vegetarier` (2021) эталон «Ich bin Vegetarier**in**»,
    у `Veganer/in` (2934) — «Ich bin Veganerin». Там русское
    «вегетарианка» не произвол, а точный перевод, и правка сломала бы
    ряд. Правило базы «рассказчик в мужском роде» действует только
    там, где немецкий рода НЕ показывает.

Из этого следует порядок работы с уловом: прежде чем править ячейку,
смотреть немецкий пример. Примета немецкую сторону не проверяет —
«Vegetarierin» от «Vegetarier» формально не отличишь без словаря
женских форм.

Как ищется. Женская форма прошедшего («-ла», «-лась», «-лася») должна
стоять ПОДЛЕЖАЩИМ при «я»: сразу после него, допуская между ними до
трёх наречий. Без этого ограничения примета дала 34 попадания, из
которых большинство ложные — там женская форма относилась к другому
подлежащему («когда ОНА мне рассказала», «ДВЕРЬ захлопнулась», «моя
ЖЕНА накрывала»), либо совпадала с родительным падежом
существительного («до вокзалА», «со столА»).

    python -m app.scripts.scan_speaker_gender
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

ADVERBS = (
    "не|вже|уже|щойно|тільки|только|что|сейчас|зараз|дуже|очень|раптом|вдруг"
    "|тоді|тогда|сьогодні|сегодня|нарешті|наконец|знову|снова|собі|себе"
)
# «я» не должно быть хвостом другого слова: в «сім'я стояла» подлежащее —
# семья, а не рассказчик, а обычное \b перед «я» этого не различает,
# потому что апостроф сам считается границей слова.
FEM_PAST = re.compile(
    rf"(?<![^\W\d_]|['’])я\b(?:\s+(?:{ADVERBS}))*\s+(\w{{3,}}л(?:а|ась|ася))\b",
    re.IGNORECASE,
)


# ВТОРАЯ ПОЛОВИНА КЛАССА, найденная в блоке 11. Прошедшее на «-ла» — не
# единственный способ выдать пол: `Wäsche` (18149) писал «Я ДОЛЖНА
# постирать», `Vegetarier` (2021) — «Я ВЕГЕТАРИАНКА». Это краткое
# прилагательное и существительное, у них своё окончание.
#
# Отделить их от наречий на «-а» (всегда, завтра, никогда, иногда,
# никуда) формально НЕ получается: окончание то же, а русского словаря
# частей речи в проекте нет. Поэтому вторая половина — мягкий список
# для глаз, а не гейт. По базе даёт 38 строк, из которых ложные —
# именно наречия, и видно это с первого взгляда.
FEM_FORM = re.compile(
    rf"(?<![^\W\d_]|['’])я\b(?:\s+(?:{ADVERBS}))*\s+(\w{{4,}}[нлтвмджрбщк]а)\b",
    re.IGNORECASE,
)


# ТРЕТЬЯ ПОЛОВИНА КЛАССА, найденная в блоке 12: ПОЛЬСКИЙ. Он тоже
# показывает род в прошедшем, а примета смотрела только ru и uk.
# `jahrelang` (2588) писал «CzekaŁAM na niego latami» при русском
# «Я ждал». По базе: 19 женских форм против 307 мужских — мужской род
# здесь такой же умолчание, как в русском.
#
# Признак у польского ЧИЩЕ русского: первое лицо прошедшего — «-łem»
# мужское, «-łam» женское, без исключений. Мешает только то, что на
# «-łam» кончается и настоящее время глаголов на «-łać» (wysyłam,
# przesyłam, odsyłam, działam, wołam) — это 9 из 19 попаданий.
#
# Отделяются они НЕ списком, а проверкой по самой базе: если из слова
# получается инфинитив на «-łać», который в польских переводах базы
# есть, значит это настоящее время. Так «wysyłam» → «wysyłać» ✓
# отбрасывается, а «czekałam» → «czekałać» ✗ остаётся.
PL_FEM_PAST = re.compile(r"\b(\w+łam)\b", re.IGNORECASE)

# ЧЕТВЁРТАЯ ПОЛОВИНА, добавленная в блоке 31: польское УСЛОВНОЕ.
# `verwöhnen` (10831) писал «CHCIAŁABYM się porządnie rozpieścić» при
# немецком «Ich möchte mich mal richtig verwöhnen», где рода нет, и при
# нейтральных русском и украинском («Я хочу себя побаловать»).
#
# Половина на «-łam» этого не видела: условное кончается на «-łabym», а
# не на «-łam». Замер: 1 женская форма против 20 мужских («Chciałbym
# wypłacić sto euro», «Chciałbym zarezerwować stolik») — мужской род
# здесь такое же умолчание базы, как во всех прочих половинах.
#
# Признак ЧИЩЕ, чем «-łam», и фильтр по инфинитивам ему не нужен: ни
# одно польское настоящее первого лица на «-łabym» не кончается, так
# что неоднозначности «wysyłam/kupiłam» здесь не возникает.
PL_FEM_COND = re.compile(r"\b(\w+łabym)\b", re.IGNORECASE)

# ДЫРА, НАЙДЕННАЯ В БЛОКЕ 17. Половина выше смотрит только ГЛАГОЛ, а род
# рассказчика виден и по ПРИЛАГАТЕЛЬНОМУ: `schockiert` (10431) писал
# «Jestem zszokowanA» при русском «Я потрясён» и украинском
# «Я шокований». Класс был объявлен сметённым дважды, и дважды — только
# по глагольному признаку.
#
# Замер: «jestem/czuję się/byłam» плюс женское прилагательное даёт 4
# попадания против 114 мужских — мужской род здесь такое же умолчание.
# Из четырёх два ложных по устройству признака (родительный падеж
# существительного «Jestem z BerlinA», глагол «pociąg zaraz odjeżdżA»),
# и поэтому эта половина — МЯГКАЯ, глаза нужны.
#
# И один трогать НЕЛЬЗЯ: `geborgen` (10862) — «W jego ramionach czuję
# się otoczona» при немецком «in seinen Armen», где эталон сам ставит
# рассказчицу женщиной, а русский и украинский согласованно женские. Тот
# же случай, что `Vegetarierin` выше.
PL_FEM_ADJ = re.compile(
    r"\b(?:jestem|czuję\s+się|czuje\s+się|byłam)\b[^.!?]*?"
    r"\b(\w{4,}(?:na|ta|ła|sza|cza|ża|ra|la|ka|ga|da|ba|wa|ma|pa))\b",
    re.IGNORECASE)


def pl_infinitives(conn) -> set[str]:
    """Польские инфинитивы из переводов базы. Нужны, чтобы отличить
    настоящее время глаголов на «-łać» от прошедшего женского рода."""
    rows = conn.execute(
        text("SELECT translation_pl FROM words WHERE translation_pl IS NOT NULL")
    ).scalars()
    out: set[str] = set()
    for raw in rows:
        for part in str(raw).split(","):
            w = part.strip().lower()
            if w.endswith("ć") and " " not in w:
                out.add(w)
    return out


# ЕЩЁ ОДНА ПОЛОВИНА, добавленная в блоке 21. Род рассказчика виден не
# только по глаголу и прилагательному, но и по МЕСТОИМЕНИЮ: `nähen`
# (1719) писал «Я шью себе одежду САМА» при немецком «Ich nähe meine
# Kleidung selbst», где рода нет.
#
# Замер: ru 1 женское против 4 мужских, uk 1 против 7 — мужской род
# здесь такое же умолчание базы, как везде. Нашёлся ровно один ряд, и
# он же был найден глазами.
#
# ПОЛЬСКИЙ СЮДА НЕ ВХОДИТ, и причина в самом языке: «sama» значит и
# «сама», и «та же». Замер дал 9 попаданий, из них восемь законные —
# «ta SAMA kobieta» (та же женщина), «została sama» (она осталась
# одна), «rozmawia sama ze sobą» (ОНА говорит сама с собой), «sama
# waży» (муравей сам весит). Отличить без разбора подлежащего нельзя.
SELF_FEM = re.compile(r"(?<![^\W\d_])я\b[^.!?]*?\bсама\b", re.IGNORECASE)


def self_pronoun_hit(sentence: str | None) -> str | None:
    """«я … сама» — рассказчица женщина. Только ru и uk."""
    return "сама" if SELF_FEM.search(sentence or "") else None


def pl_adj_hit(sentence: str | None) -> str | None:
    """Женское прилагательное при «jestem/czuję się». Мягкий признак."""
    m = PL_FEM_ADJ.search(sentence or "")
    return m.group(1) if m else None


def pl_hit(sentence: str | None, infinitives: set[str]) -> str | None:
    # Условное «-łabym» однозначно, и фильтр инфинитивов ему не нужен
    m = PL_FEM_COND.search(sentence or "")
    if m:
        return m.group(1)
    for m in PL_FEM_PAST.finditer(sentence or ""):
        word = m.group(1)
        # «wysyłam» → «wysyłać»: настоящее время, не род
        if word[:-1].lower() + "ć" in infinitives:
            continue
        return word
    return None


def hit(sentence: str | None) -> str | None:
    m = FEM_PAST.search(sentence or "")
    return m.group(1) if m else None


def soft_hit(sentence: str | None) -> str | None:
    """Краткая форма или существительное женского рода. Нужны глаза."""
    s = sentence or ""
    if FEM_PAST.search(s):
        return None  # уже поймано точной половиной
    m = FEM_FORM.search(s)
    return m.group(1) if m else None


def selfcheck() -> None:
    bad = [
        "Я обожгла язык",
        "Я только что пришла домой",
        "Смотри, что я нашла",
        "Он посмотрел на меня удивлённо, когда я вдруг рассмеялась",
        "Я щойно прийшла додому",
    ]
    good = [
        "Я обжёг язык",
        "Я только что пришёл домой",
        "Я был очень удивлён, когда она мне это рассказала",
        "Я испугался, когда дверь внезапно захлопнулась",
        "Я готовил еду, тем временем моя жена накрывала стол",
        "Я беру такси до вокзала",
        "Я измеряю длину стола линейкой",
        "Я не могу допустить, чтобы моя подруга осталась одна",
        "Скорботна сім'я стояла біля могили свого близького",  # подлежащее — сім'я
    ]
    errs = [f"пропущено: {s!r}" for s in bad if not hit(s)]
    errs += [f"ложная тревога: {s!r} → {hit(s)}" for s in good if hit(s)]

    # Польское прилагательное: то, что половина на «-łam» не видела.
    if not pl_adj_hit("Jestem zszokowana jego słowami"):
        errs.append("pl: женское прилагательное «zszokowana» не найдено")
    if not pl_adj_hit("Czuję się zmęczona"):
        errs.append("pl: женское прилагательное «zmęczona» не найдено")
    if pl_adj_hit("Jestem zszokowany jego słowami"):
        errs.append("pl: мужское «zszokowany» объявлено женским")
    if pl_adj_hit("Jestem bardzo zmęczony"):
        errs.append("pl: мужское «zmęczony» объявлено женским")

    # Польское условное: «-łabym» женское, «-łbym» мужское.
    if not PL_FEM_COND.search("Chciałabym pójść do spa"):
        errs.append("pl: условное «Chciałabym» не найдено")
    if PL_FEM_COND.search("Chciałbym zarezerwować stolik"):
        errs.append("pl: мужское «Chciałbym» объявлено женским")
    # И оно не должно путаться с нейтральным настоящим на «-łam»
    if PL_FEM_COND.search("Wysyłam ci maila"):
        errs.append("pl: настоящее «wysyłam» принято за условное")

    # Местоимение «сама» при «я».
    if not self_pronoun_hit("Я шью себе одежду сама"):
        errs.append("ru: «я … сама» не распознано")
    if not self_pronoun_hit("Я сама шию собі одяг"):
        errs.append("uk: «я сама» не распознано")
    if self_pronoun_hit("Я шью себе одежду сам"):
        errs.append("ru: мужское «сам» объявлено женским")
    if self_pronoun_hit("Вона розмовляє сама з собою"):
        errs.append("подлежащее «вона» принято за рассказчика")

    if errs:
        print("САМОПРОВЕРКА НЕ ПРОШЛА:")
        for e in errs:
            print("   ", e)
        sys.exit(1)
    print(f"самопроверка: {len(good)} верных и {len(bad)} женских строк разобраны верно")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT id, word_de, example_ru, example_uk FROM words "
                "WHERE example_ru IS NOT NULL ORDER BY id"
            )
        ).mappings().all()

    found: list[tuple[int, str, str, str, str]] = []
    for r in rows:
        for lg in ("ru", "uk"):
            if (form := hit(r[f"example_{lg}"])):
                found.append((r["id"], r["word_de"], lg, form, r[f"example_{lg}"]))

    soft: list[tuple[int, str, str, str, str]] = []
    for r in rows:
        for lg in ("ru", "uk"):
            if (form := soft_hit(r[f"example_{lg}"])):
                soft.append((r["id"], r["word_de"], lg, form, r[f"example_{lg}"]))

    with engine.connect() as conn:
        pl_inf = pl_infinitives(conn)
        pl_rows = conn.execute(
            text("SELECT id, word_de, example_pl FROM words "
                 "WHERE example_pl IS NOT NULL ORDER BY id")
        ).mappings().all()
    pl_found = [
        (r["id"], r["word_de"], form, r["example_pl"])
        for r in pl_rows
        if (form := pl_hit(r["example_pl"], pl_inf))
    ]

    print(f"\nпрочитано рядов: {len(rows)}")
    print(f"ячеек, где рассказчик — женщина (ru, uk): {len(found)}")
    for wid, word, lg, form, ex in found:
        print(f"  {wid:>6}  {word:<18} {lg}  «{form}»  {ex}")

    print(f"\nПОЛЬСКИЙ, прошедшее женского рода: {len(pl_found)}")
    for wid, word, form, ex in pl_found:
        print(f"  {wid:>6}  {word:<18} «{form}»  {ex}")

    pl_adj = [
        (r["id"], r["word_de"], form, r["example_pl"])
        for r in pl_rows
        if (form := pl_adj_hit(r["example_pl"]))
    ]
    print(f"\nПОЛЬСКИЙ, женское прилагательное: {len(pl_adj)}  (нужны глаза,"
          f" родительный падеж и глаголы тут ложные)")
    for wid, word, form, ex in pl_adj:
        print(f"  {wid:>6}  {word:<18} «{form}»  {ex}")

    pron = [
        (r["id"], r["word_de"], lg, r[f"example_{lg}"])
        for r in rows for lg in ("ru", "uk")
        if self_pronoun_hit(r[f"example_{lg}"])
    ]
    print(f"\n«я … сама» (ru, uk): {len(pron)}")
    for wid, word, lg, ex in pron:
        print(f"  {wid:>6}  {word:<18} {lg}  {ex}")

    print(f"\nкраткая форма или существительное: {len(soft)}  (нужны глаза,"
          f" наречия на «-а» тут ложные)")
    for wid, word, lg, form, ex in soft:
        print(f"  {wid:>6}  {word:<18} {lg}  «{form}»  {ex}")


if __name__ == "__main__":
    main()
