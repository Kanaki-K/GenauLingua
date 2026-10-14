"""
Класс: апостроф, вставленный перед конечной «s».

«The verdict wa's not fair», «The lid doe's not fit», «Algebra had
alway's been», «The witnes's got caught», «so a's not to wake the
others». Это не опечатки по одной: порча системная — где-то апостроф
влез перед «s» в конце слова. Семнадцать раз это «wa's» вместо «was».

Нашлось глазами дважды, в блоках 19 (`vergönnen`) и 20 (`gerecht`).
Дальше — так, как велит главное правило: вместо третьего случая выписаны
все английские слова с апострофом списком, по частоте. Законные
сокращения и притяжательные видны сразу («I'm» 286, «that's» 271,
«don't» 130), а битые стоят рядом с ними и не прячутся: «wa's» 17,
«alway's», «doe's», «witnes's», «a's».

**Почему так, а не шаблоном.** Шаблон «апостроф внутри слова» дал бы
сотни ложных: в английском это норма, а в турецком — апостроф перед
падежным окончанием имени собственного («Berlin'de», «Münih'te»). Список
токенов по частоте показывает битое без догадок.

Заодно турецкий апостроф там, где имени собственного нет:
«muayenehane'de», «lobi'si», «sinirli'yim» — три ячейки на базу,
остальные шестьдесят законны. И немецкое «so'n» в эталоне `Trampel`:
разговорное стяжение «so ein», в учебном примере ему не место.

    python -m app.scripts.fix_apostrophe_s            # показать
    python -m app.scripts.fix_apostrophe_s --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

_WAS = "«wa's» — апостроф влез перед конечной «s»"

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- «wa's» вместо «was» --------------------------------------------------
    (8997, "example_en", "He wa's just a henchman of the mafia",
     "He was just a henchman of the mafia", _WAS),
    (10318, "example_en", "The verdict wa's not fair",
     "The verdict was not fair", _WAS),
    (10429, "example_en", "That wa's just an illusion, not reality",
     "That was just an illusion, not reality", _WAS),
    (10764, "example_en", "That wa's not morally justified",
     "That was not morally justified", _WAS),
    (10819, "example_en",
     "That wa's just a bluff; he never had the ability to do it",
     "That was just a bluff; he never had the ability to do it", _WAS),
    (10969, "example_en", "His impulsive decision wa's not well thought out",
     "His impulsive decision was not well thought out", _WAS),
    (11381, "example_en", "That wa's just a figment, not reality",
     "That was just a figment, not reality", _WAS),
    (11888, "example_en", "The food in the hospital wa's not very tasty",
     "The food in the hospital was not very tasty", _WAS),
    (12785, "example_en",
     "The gunshot wound on his arm wa's not life-threatening",
     "The gunshot wound on his arm was not life-threatening", _WAS),
    (14023, "example_en", "The criticism of his plan wa's not unjustified",
     "The criticism of his plan was not unjustified", _WAS),
    (14263, "example_en", "That wa's just nonsense, nobody believed him",
     "That was just nonsense, nobody believed him", _WAS),
    (15520, "example_en", "It wa's just a breath of wind",
     "It was just a breath of wind", _WAS),
    (16486, "example_en", "The violent solution wa's not acceptable",
     "The violent solution was not acceptable", _WAS),
    (16510, "example_en", "His ID was invalid and wa's not accepted",
     "His ID was invalid and was not accepted", _WAS),
    (16688, "example_en", "The prosecution of the crime wa's not simple",
     "The prosecution of the crime was not simple", _WAS),
    (17581, "example_en", "The security system wa's just installed",
     "The security system was just installed", _WAS),
    (18862, "example_en",
     "That wa's just a small mishap, don't worry",
     "That was just a small mishap, don't worry", _WAS),
    # Восемнадцатое «wa's» — `vergönnen`, id 8458 — уже исправлено в
    # fix_late_batch: именно оно и показало класс.

    # --- другие слова той же порчи --------------------------------------------
    (2334, "example_en", "The lid doe's not fit", "The lid does not fit",
     "«doe's» вместо «does»"),
    (8093, "example_en",
     "He spoke in a muffled voice so a's not to wake the others",
     "He spoke in a muffled voice so as not to wake the others",
     "«a's» вместо «as»"),
    (8331, "example_en",
     "The celebrity traveled incognito so a's not to be recognized",
     "The celebrity traveled incognito so as not to be recognized",
     "«a's» вместо «as»"),
    (16491, "example_en",
     "The witnes's got caught in the line of fire and was in danger",
     "The witness got caught in the line of fire and was in danger",
     "«witnes's» вместо «witness»"),
    (15517, "example_en", "My shoe's got stuck in the mud",
     "My shoes got stuck in the mud",
     "«shoe's» вместо «shoes»; в немецком «Meine Schuhe» — обе"),
    (9634, "example_en",
     "Algebra had alway's been his favorite subject in school",
     "Algebra had always been my favorite subject in school",
     "«alway's» вместо «always»; и в немецком «mein», а не «его»"),
    (9634, "example_tr",
     "Cebir, okulda her zaman onun en sevdiği konu olmuştur",
     "Cebir, okulda her zaman en sevdiğim dersti",
     "в немецком «мой любимый предмет», а не «его»; и «konu» — тема, "
     "предмет это «ders»"),

    # --- турецкий апостроф там, где нет имени собственного --------------------
    (728, "example_tr",
     "Ortak muayenehane'de birkaç doktor birlikte çalışır",
     "Ortak muayenehanede birkaç doktor birlikte çalışır",
     "«muayenehane» — обычное слово, апостроф не нужен"),
    (17804, "example_tr",
     "Petrol şirketlerinin lobi'si büyük etkiye sahip",
     "Petrol şirketlerinin lobisi büyük etkiye sahip",
     "«lobi» — обычное слово, апостроф не нужен"),
    (9621, "example_tr", "Final sınav gelecek hafta ve sinirli'yim",
     "Final sınavı gelecek hafta ve gerginim",
     "апостроф не нужен; «sinirli» — злой, а «nervös» это «gergin»; "
     "и «sınav» без притяжательного аффикса"),
    (2564, "example_tr", "Bu, Avrupa'da tarihi bir olayıydı",
     "Bu, Avrupa'da tarihi bir olay",
     "«olayıydı» — двойной аффикс, и в немецком настоящее время"),
    (15062, "example_tr", "Kuzenime Noel'de ziyaret edecek",
     "Kuzenim Noel'de ziyarete geliyor",
     "«Kuzenime ziyaret edecek» — кто кого? В немецком кузен приходит сам"),

    # --- немецкий эталон -------------------------------------------------------
    (11446, "example_de", "Er ist so'n Trampel, immer unbeholfen",
     "Er ist so ein Trampel, immer unbeholfen",
     "«so'n» — разговорное стяжение «so ein»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
