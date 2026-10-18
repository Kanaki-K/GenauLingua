"""
Примета: эталон просит «bitte», перевод велит голым приказом.

ЗАЧЕМ. Класс всплывал по одному ряду в блоках 13 и 16 (`Anweisung`
1150: немецкое «Bitte folge den Anweisungen», английское «Follow the
instructions»). Разница не в стиле: учебная фраза «Klick bitte den Link
an» учит просить, а «Kliknij na ten link» учит командовать. Это разные
фразы.

ПОЧЕМУ ЭТОТ ПРИЗНАК ЗАМКНУТ, А ОБЩИЙ — НЕТ. Сначала я замерил
«усиление вообще»: sehr/echt/wirklich/ganz/total/einfach против их
соответствий в пяти языках. Вышло 209 потерь и 461 добавка, и почти всё
это — дыры моего же списка: польское «całkiem» и «po-настоящему» ничем
не хуже «ganz» и «wirklich», а турецкое «çok» ставится свободнее
немецкого «sehr». Перечисление по шести языкам не работает, и это
ровно тот урок, что записан в журнале пять раз.

А у «bitte» список ЗАМКНУТ: в каждом языке ровно одно-два слова
(please / пожалуйста / будь ласка / lütfen / proszę), и больше их не
бывает. Поэтому замер по «bitte» имеет смысл, а по «sehr» — нет.

ДВА ВИДА ЛОЖНЫХ, И ОБА ОТСЕКАЮТСЯ ПРАВИЛОМ, А НЕ СПИСКОМ:

  • «bitte» — ещё и форма глагола `bitten` (просить): «Ich bitte dich
    um Hilfe», «Ich bitte um Gnade». Там перевод «Я прошу тебя о
    помощи» верен, а примета считала его потерей. Отсекается разбором:
    перед «bitte» стоит «ich», или после идёт «um»/«dich»/«euch».

  • Вежливость может держаться НЕ на частице, а на вопросе: русское
    «Можешь передать соль?» и польское «Czy możesz to przeczytać?»
    вежливы сами по себе, частица там не нужна. Отсекается наличием
    вопросительного знака в переводе.

Замер до отсечения: 108 эталонов с «bitte», 37 переводов без
вежливости, настоящих 14. После отсечения ложные падают с 23 до 3, и
доля настоящих — около четырёх пятых. Гейтом примета всё равно не
является: остаётся «bitte schön» (14035), где английское «there you
go» и турецкое «buyrun» — правильная передача идиомы, а не потеря.

    python -m app.scripts.scan_bitte_dropped
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

BITTE = re.compile(r"\bbitte\b", re.IGNORECASE)

# ОБРАТНОЕ НАПРАВЛЕНИЕ, добавленное в блоке 21: в эталоне просьбы нет, а
# перевод вежлив. Первая версия замера дала 24 попадания, из них 19
# польских — и все законные, потому что **польский формальный императив
# ТАК И ОБРАЗУЕТСЯ**: «Proszę skręcić w lewo», «Proszę zadzwonić».
# Другого способа сказать «Biegen Sie links ab» по-польски нет.
#
# Отсекается правилом: если немецкий эталон сам в вежливой форме
# («Sie»/«Ihnen»/«Ihre»), польское «Proszę» — это перевод этой формы, а
# не добавка. После отсечения 8 попаданий, настоящих 2–4.
FORMAL_DE = re.compile(r"\b(Sie|Ihnen|Ihre?[mnrs]?)\b")

# «bitte» как форма глагола `bitten`, а не вежливая частица.
VERB_BITTEN = re.compile(
    r"\bich\s+bitte\b|\bbitte\s+(?:um|dich|euch|Sie\s+um)\b", re.IGNORECASE)

# Вежливость в переводе. Список замкнут: других слов для этого в языках нет.
# В турецком вежливость несёт ещё и вопросительная частица «-misin», и она
# здесь нужна: «Bunu tekrar eder misin?» вежливо без «lütfen».
POLITE = {
    "en": r"\b(please)\b",
    "ru": r"\b(пожалуйста|будьте\s+добры|будь\s+добр)\b",
    "uk": r"\b(ласка|будьте\s+добрі)\b",
    "tr": r"\b(lütfen|rica\s+ederim|m[iıuü]s[iıuü]n(?:iz)?|m[iıuü]s[iıuü]n[iı]z)\b",
    "pl": r"\b(proszę|poproszę)\b",
    # Голого «prego» и «gentilmente» здесь нет: «Prego che Dio esaudisca» —
    # «молюсь», «mi ha gentilmente prestato» — перевод «freundlicherweise».
    # Вежливая просьба — «La prego», «si prega di»: «La preghiamo di pagare».
    "it": r"\b(per\s+favore|per\s+piacere|cortesemente|la\s+prego|la\s+preghiamo|"
          r"ti\s+prego|si\s+prega)\b",
    "es": r"\b(por\s+favor|haz\s+el\s+favor|haga\s+el\s+favor|tenga\s+la\s+bondad)\b",
    # «Veuillez» и «Merci de» — вежливая просьба сами по себе: «Veuillez
    # indiquer votre adresse», «Merci de ne pas toucher» (так пишут таблички);
    # но «à la merci de» — «во власти», не просьба
    "fr": r"\b(s'il\s+te\s+pla[iî]t|s'il\s+vous\s+pla[iî]t|veuillez|je\s+vous\s+prie|"
          r"je\s+te\s+prie|(?<!la )merci\s+de|(?<!la )merci\s+d')",
    "cs": r"\b(prosím|poprosím|buď\s+tak\s+hodný|buďte\s+tak\s+laskav)\w*",
}
POLITE = {k: re.compile(v, re.IGNORECASE) for k, v in POLITE.items()}
LANGS = tuple(POLITE)


def de_asks(sentence: str) -> bool:
    """Стоит ли в эталоне «bitte» именно как вежливая частица."""
    s = sentence or ""
    if not BITTE.search(s):
        return False
    return not VERB_BITTEN.search(s)


def dropped(lang: str, sentence: str) -> bool:
    """Потеряна ли вежливость: нет ни частицы, ни вопроса."""
    s = sentence or ""
    if not s:
        return False
    if "?" in s:
        return False
    return not POLITE[lang].search(s)


def added(lang: str, de: str, sentence: str) -> str | None:
    """Вежливость в переводе там, где эталон о ней не просит."""
    s = sentence or ""
    if not s or "?" in s:
        return None
    if BITTE.search(de or "") or FORMAL_DE.search(de or ""):
        return None
    m = POLITE[lang].search(s)
    return m.group(0) if m else None


def selfcheck() -> None:
    errs = []
    # Глагол `bitten` просьбой НЕ считается.
    for s in ("Ich bitte dich um Hilfe", "Ich bitte um Gnade"):
        if de_asks(s):
            errs.append(f"de: глагол `bitten` принят за частицу: {s!r}")
    # А частица — считается, и в начале фразы тоже.
    for s in ("Klick bitte den Link an", "Bitte folge den Anweisungen",
              "Schließ bitte die Tür ab"):
        if not de_asks(s):
            errs.append(f"de: вежливое «bitte» не распознано: {s!r}")
    # Потеря вежливости — голый приказ.
    if not dropped("pl", "Kliknij na ten link"):
        errs.append("pl: голый приказ не признан потерей")
    if not dropped("en", "Follow the instructions"):
        errs.append("en: голый приказ не признан потерей")
    if not dropped("uk", "Закрути кришку"):
        errs.append("uk: голый приказ не признан потерей")
    # Вежливость на месте — ни частицей, ни вопросом трогать нельзя.
    if dropped("pl", "Kliknij proszę na ten link"):
        errs.append("pl: «proszę» не распознано")
    if dropped("pl", "Poproszę szklankę wody"):
        errs.append("pl: «Poproszę» не распознано")
    if dropped("ru", "Можешь мне передать соль?"):
        errs.append("ru: вежливость через вопрос не распознана")
    if dropped("tr", "Bunu tekrar eder misin?"):
        errs.append("tr: вежливость через «misin» не распознана")
    if dropped("tr", "Lütfen kapıyı kilitle"):
        errs.append("tr: «Lütfen» не распознано")
    for lang, s in (("it", "Chiudi la porta, per favore"),
                    ("es", "Cierra la puerta, por favor"),
                    ("fr", "Ferme la porte, s'il te plaît"),
                    ("fr", "Veuillez fermer la porte"),
                    ("cs", "Zavři prosím dveře")):
        if dropped(lang, s):
            errs.append(f"{lang}: вежливость не распознана: {s!r}")
    for lang, s in (("it", "Chiudi la porta"), ("es", "Cierra la puerta"),
                    ("fr", "Ferme la porte"), ("cs", "Zavři dveře")):
        if not dropped(lang, s):
            errs.append(f"{lang}: голый приказ не признан потерей: {s!r}")

    # Обратное направление. Главное — не трогать польский формальный
    # императив: он ТАК И ОБРАЗУЕТСЯ через «Proszę + инфинитив».
    if added("pl", "Biegen Sie links ab", "Proszę skręcić w lewo"):
        errs.append("pl: формальный императив принят за добавку вежливости")
    if added("pl", "Rufen Sie die Hausverwaltung an",
             "Proszę zadzwonić do administracji budynku"):
        errs.append("pl: то же")
    if not added("pl", "Mach die Tür zu", "Zamknij drzwi, proszę"):
        errs.append("pl: добавленное «proszę» при неформальном эталоне не найдено")

    if errs:
        print("САМОПРОВЕРКА НЕ ПРОШЛА:")
        for e in errs:
            print("   ", e)
        sys.exit(1)
    print("самопроверка: глагол `bitten` отделён от частицы, "
          "вежливость через вопрос не считается потерей")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = ", ".join(f"example_{l}" for l in LANGS)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT id, word_de, example_de, {cols} FROM words "
                "WHERE example_de IS NOT NULL ORDER BY id"
            )
        ).mappings().all()

    asks = 0
    hits: list[tuple[int, str, str, str, str]] = []
    for r in rows:
        de = r["example_de"] or ""
        if not de_asks(de):
            continue
        asks += 1
        for l in LANGS:
            s = r[f"example_{l}"]
            if s and dropped(l, s):
                hits.append((r["id"], r["word_de"], l, de, s))

    print(f"\nпрочитано рядов: {len(rows)}")
    print(f"эталонов с вежливым «bitte»: {asks}")
    print(f"переводов без вежливости: {len(hits)}  (нужны глаза)")
    print("по языкам:", dict(Counter(h[2] for h in hits).most_common()))
    print()
    for wid, word, lang, de, other in hits:
        print(f"  {wid:>6}  {word:<18} {lang}")
        print(f"          de: {de}")
        print(f"          ->  {other}")

    extra: list[tuple[int, str, str, str, str, str]] = []
    for r in rows:
        de = r["example_de"] or ""
        for l in LANGS:
            if (frag := added(l, de, r[f"example_{l}"])):
                extra.append((r["id"], r["word_de"], l, frag, de, r[f"example_{l}"]))

    print(f"\nвежливость ДОБАВЛЕНА, эталон о ней не просит: {len(extra)}"
          f"  (нужны глаза)")
    print("по языкам:", dict(Counter(h[2] for h in extra).most_common()))
    for wid, word, lang, frag, de, other in extra:
        print(f"  {wid:>6}  {word:<18} {lang} «{frag}»")
        print(f"          de: {de}")
        print(f"          ->  {other}")


if __name__ == "__main__":
    main()
