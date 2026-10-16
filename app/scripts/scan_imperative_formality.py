"""
Примета: эталон велит на «ты», а перевод — на «вы».

Зачем. `scan_formality_vs_de` закрыла этот класс только наполовину: она
требует, чтобы в немецком стояло ЯВНОЕ `du`/`dein`/`dich`/`dir`. А у
повелительного местоимения нет вовсе — «Biege rechts ab», «Trenn den
Müll», — и половина класса осталась невидимой. Дыра была записана в
HANDOVER после блока 4 (ряд `rechts`), блок 8 дал второй ряд
(`trennen`), и класс стал классом.

Как определяется немецкое повелительное. Тем же разбором, что в
`scan_de_bare_imperative`: слово в начале фразы (или после «Bitte»)
совпало с основой глагола базы — голой или с «-e». Копии нет, функции
импортируются.

Как определяется вежливость в переводе:

  • ТУРЕЦКИЙ. Повелительное 2-го лица множественного/вежливого кончается
    на `-in`/`-ın`/`-un`/`-ün` или `-iniz`. Беда в том, что на те же
    буквы кончается и 2-е лицо единственного у возвратных глаголов
    (`tutun` от `tutunmak` — это «держись», а не «держитесь»), поэтому
    форма проверяется по основам турецких глаголов… которых в базе нет.
    Вместо этого берётся обратный признак: если в ряде есть ЕДИНСТВЕННОЕ
    число (`sen`, `senin`) — ряд чист; если есть `siz`/`-iniz` —
    вежливое наверняка. Остальное выводится мягким списком для глаз.

  • УКРАИНСКИЙ. Повелительное 2-го лица множественного кончается на
    `-те` (`сортуйте`, `зробіть`, `говоріть`). Единственное — на
    `-й`/`-и`/`-ь`. Признак надёжнее турецкого.

Гейтом примета НЕ является: турецкая вежливая форма законна в общих
инструкциях, и решать, инструкция это или обращение к ученику, надо
глазами.

    python -m app.scripts.scan_imperative_formality
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402
from app.scripts.scan_de_bare_imperative import (  # noqa: E402
    function_words,
    positions,
    syllabic_el_er,
)
from app.scripts.scan_formality import has_formal, has_informal  # noqa: E402

FORMAL_DE = re.compile(r"\b(Sie|Ihnen|Ihre?[mnrs]?)\b")

# турецкое вежливое: -iniz/-ınız/-unuz/-ünüz либо местоимение siz
TR_FORMAL_SURE = re.compile(r"\b\w+[ıiuü]n[ıiuü]z\b|\bsiz(in|e|i)?\b", re.IGNORECASE)
TR_INFORMAL = re.compile(r"\bsen(in|i|e|inle)?\b", re.IGNORECASE)
# турецкое вежливое повелительное: -in/-ın/-un/-ün на конце слова.
#
# ПОРОГ ДЛИНЫ: было `\w{4,}`, то есть четыре буквы ПЕРЕД окончанием, и
# короткие формы проваливались — «gidin» (git+in) это пять букв всего.
# Ряд `geradeaus` (329) нашёлся глазами в блоке 13 именно так. Порог
# снижен до двух букв.
TR_FORMAL_MAYBE = re.compile(r"\b\w{2,}[ıiuü]n\b")

# Украинское повелительное множественного/вежливого. Та же ошибка порога:
# «йдіть» — пять букв, под `\w{4,}` + «іть» не подходило.
#
# Окончание «ете» выброшено: в украинском это ещё и обычное настоящее
# время второго лица множественного («читаєте»), и отличить одно от
# другого без словаря нельзя.
UK_FORMAL = re.compile(r"\b\w{2,}(?:йте|іть|ьте|мте)\b", re.IGNORECASE)
UK_INFORMAL = re.compile(r"\b(ти|тебе|тобі|тобою|твій|твоя|твоє|твої)\b", re.IGNORECASE)

# Новые языки. Французское и чешское повелительное на «вы» видно по
# окончанию, как украинское:
#   fr  «Tournez», «Appelez» — первое слово на -ez, или «veuillez», «vous»
#       («rendez-vous» — существительное, не обращение; «Un café, s'il vous
#       plaît» — формула заказа, немецкое «bitte»; «Allez, on s'y met» —
#       междометие)
#   cs  «Odbočte», «Zavolejte», «Přineste» — на -te после согласной или
#       -ejte/-ujte/-ěte. Окончания «-áte, -íte, -ete» выброшены: это ещё и
#       настоящее время («děláte», «nesete»), как украинское «-ете»; «jste»
#       — глагол «быть».
# Итальянское и испанское вежливое повелительное — сослагательное («Giri»,
# «Gire») и по окончанию от «Gira» не отличается без словаря; там берутся
# только явные признаки «Вы» из scan_formality: «Lei, La, Sua», «usted».
FR_FORMAL = re.compile(
    r"^\W*(?!(?:assez|chez|nez)\b|allez\s*,)\w{2,}ez\b"
    r"|(?<![\w-])(?<!s'il )(veuillez|vous|votre|vos)(?![\w])", re.IGNORECASE)
FR_INFORMAL = re.compile(
    r"(?<![\w])(tu|te|toi|ton|ta|tes)(?![\w'])|(?<![\w])t'", re.IGNORECASE)
CS_FORMAL = re.compile(
    r"\b(?!jste\b)\w{2,}(?:ejte|ujte|ěte|[bcčdďfghjklmnňprřsštťvzž]te)\b",
    re.IGNORECASE)
CS_INFORMAL = re.compile(
    r"\b(ty|tebe|tobě|tě|tvůj|tvoje|tvá|tvé|tvou|jsi)\b", re.IGNORECASE)
NEW_LANGS = ("it", "es", "fr", "cs")
NEW_FORMAL = {
    "fr": (FR_FORMAL, FR_INFORMAL),
    "cs": (CS_FORMAL, CS_INFORMAL),
}


def all_verb_stems(conn, skip: set[str]) -> set[str]:
    """Основы ВСЕХ глаголов базы, включая сильные.

    Отличие от `stems_from_base` в примете на усечения: там сильные
    исключены нарочно (у них голая форма — норма). Здесь наоборот нужно
    узнать повелительное ЛЮБОГО глагола, иначе «Biege rechts ab» не
    распознается и половина класса опять останется невидимой.
    """
    rows = conn.execute(
        text("SELECT word_de FROM words WHERE pos = 'VERB' AND word_de IS NOT NULL")
    ).scalars()
    out: set[str] = set()
    for raw in rows:
        for inf in (p.strip() for p in str(raw).split(",")):
            inf = inf.replace("sich ", "").strip()
            if not inf or " " in inf or not inf.endswith("en"):
                continue
            stem = inf[:-2].lower()
            if len(stem) < 3 or stem in skip or syllabic_el_er(stem):
                continue
            out.add(stem)
    return out


def de_is_imperative(sentence: str, stems: set[str]) -> bool:
    """Начинается ли фраза повелительным: основа глагола базы, голая или с «-e»."""
    for w in positions(sentence or ""):
        if w in stems or (w.endswith("e") and w[:-1] in stems):
            return True
    return False


def selfcheck(stems: set[str]) -> None:
    errs = []
    # немецкое повелительное распознаётся
    for s in ("Trenn den Müll", "Biege rechts ab", "Bitte zahle hier", "Mach die Tür auf"):
        if not de_is_imperative(s, stems):
            errs.append(f"не распознано как повелительное: {s!r}")
    for s in ("Der Zug fährt ab", "Ich mache das selber", "Die Schuhe passen gut"):
        if de_is_imperative(s, stems):
            errs.append(f"ложно распознано как повелительное: {s!r}")
    # вежливость в переводах
    if not UK_FORMAL.search("Сортуйте сміття"):
        errs.append("uk: «Сортуйте» не распознано как вежливое")
    if not UK_FORMAL.search("Будь ласка, йдіть прямо"):
        errs.append("uk: короткое «йдіть» не распознано — порог длины")
    if UK_FORMAL.search("Сортуй сміття"):
        errs.append("uk: «Сортуй» ложно распознано как вежливое")
    if not TR_FORMAL_MAYBE.search("Çöpleri ayırın"):
        errs.append("tr: «ayırın» не распознано как возможно вежливое")
    if not TR_FORMAL_MAYBE.search("Lütfen dümdüz gidin"):
        errs.append("tr: короткое «gidin» не распознано — порог длины")
    if TR_FORMAL_MAYBE.search("Çöpleri ayır"):
        errs.append("tr: «ayır» ложно распознано")
    if not TR_FORMAL_SURE.search("Lütfen bekleyiniz"):
        errs.append("tr: «bekleyiniz» не распознано как вежливое наверняка")
    for s in ("Tournez à gauche", "Veuillez fermer la porte"):
        if not FR_FORMAL.search(s):
            errs.append(f"fr: {s!r} не распознано как вежливое")
    for s in ("Tourne à gauche", "Note le rendez-vous", "Assez parlé",
              "Un café, s'il vous plaît", "Allez, on s'y met"):
        if FR_FORMAL.search(s):
            errs.append(f"fr: {s!r} ложно распознано как вежливое")
    for s in ("Odbočte doleva", "Zavolejte správu domu", "Přineste si průkaz"):
        if not CS_FORMAL.search(s):
            errs.append(f"cs: {s!r} не распознано как вежливое")
    for s in ("Odboč doleva", "Kde jste byli", "Co děláte", "Zavolej mi"):
        if CS_FORMAL.search(s):
            errs.append(f"cs: {s!r} ложно распознано как вежливое")
    if errs:
        print("САМОПРОВЕРКА НЕ ПРОШЛА:")
        for e in errs:
            print("   ", e)
        sys.exit(1)
    print("самопроверка: разбор повелительного и вежливости верен")


def main() -> None:
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        stems = all_verb_stems(conn, function_words(conn))
        selfcheck(stems)
        rows = conn.execute(
            text(
                "SELECT id, word_de, example_de, example_uk, example_tr, "
                "example_it, example_es, example_fr, example_cs FROM words "
                "WHERE example_de IS NOT NULL ORDER BY id"
            )
        ).mappings().all()

    uk_hits: list[tuple[int, str, str, str]] = []
    tr_sure: list[tuple[int, str, str, str]] = []
    tr_maybe: list[tuple[int, str, str, str]] = []
    imperatives = 0
    new_hits: dict[str, list[tuple[int, str, str, str]]] = {l: [] for l in NEW_LANGS}

    for r in rows:
        de = r["example_de"] or ""
        if FORMAL_DE.search(de) or not de_is_imperative(de, stems):
            continue
        imperatives += 1
        uk, tr = r["example_uk"] or "", r["example_tr"] or ""
        if UK_FORMAL.search(uk) and not UK_INFORMAL.search(uk):
            uk_hits.append((r["id"], r["word_de"], de, uk))
        for lang in NEW_LANGS:
            ex = r[f"example_{lang}"] or ""
            if not ex:
                continue
            if lang in NEW_FORMAL:
                formal_re, informal_re = NEW_FORMAL[lang]
                formal = formal_re.search(ex) and not informal_re.search(ex)
            else:
                formal = has_formal(lang, ex) and not has_informal(lang, ex)
            if formal:
                new_hits[lang].append((r["id"], r["word_de"], de, ex))
        if TR_INFORMAL.search(tr):
            continue
        if TR_FORMAL_SURE.search(tr):
            tr_sure.append((r["id"], r["word_de"], de, tr))
        elif TR_FORMAL_MAYBE.search(tr):
            tr_maybe.append((r["id"], r["word_de"], de, tr))

    print(f"\nпрочитано рядов: {len(rows)}")
    print(f"из них эталон в повелительном без вежливого местоимения: {imperatives}")
    print(f"украинский на «вы»: {len(uk_hits)}")
    print(f"турецкий вежливый наверняка: {len(tr_sure)}")
    print(f"турецкий вежливый под вопросом: {len(tr_maybe)}  (нужны глаза)")

    for title, items in (
        ("УКРАИНСКИЙ на «вы»", uk_hits),
        ("ТУРЕЦКИЙ вежливый наверняка", tr_sure),
        ("ТУРЕЦКИЙ под вопросом", tr_maybe),
    ):
        print(f"\n── {title} ──────────────────────────────────")
        for wid, word, de, other in items:
            print(f"  {wid:>6}  {word:<20} de: {de}")
            print(f"          {'':<20} ->  {other}")

    print("\nit/es/fr/cs на «вы»: "
          + ", ".join(f"{l} {len(v)}" for l, v in new_hits.items()))
    for lang, items in new_hits.items():
        if not items:
            continue
        print(f"\n── {lang} на «вы» ──────────────────────────────────")
        for wid, word, de, other in items:
            print(f"  {wid:>6}  {word:<20} de: {de}")
            print(f"          {'':<20} ->  {other}")


if __name__ == "__main__":
    main()
