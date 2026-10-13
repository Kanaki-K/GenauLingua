"""
Второй круг вычитки, вторая половина: ряды 156–300.

Самое заметное:

* `Ware` — в турецком осталась разметка со слешем: «Mal / ürün geldi».
  Это второй такой случай за два круга; значит класс не единичный.
* `Spesen` — «Командирувальні видатки»: такого слова в украинском нет.
* `Mob` — «Розгнівана натовп»: «натовп» мужского рода.
* `Ehepartner` — «Мій супруг»: русизм, да ещё и противоречит собственному
  переводу, где стоит «чоловік».
* `vorladen` — в немецком вызывает суд, в русском и украинском судья.
* `Doktorarbeit` — «doktórat» вместо «doktorat».

    python -m app.scripts.fix_manual_round2b            # показать
    python -m app.scripts.fix_manual_round2b --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [

    # --- разметка и несуществующие слова ------------------------------------
    (2997, "example_tr",
     "Mal / ürün geldi",
     "Mal geldi",
     "осталась разметка со слешем"),
    (9080, "example_uk",
     "Командирувальні видатки відшкодовуються",
     "Витрати на відрядження відшкодовуються",
     "«командирувальні» — такого слова нет"),
    (9601, "translation_pl",
     "doktórat, praca doktorska, rozprawa doktorska",
     "doktorat, praca doktorska, rozprawa doktorska",
     "«doktórat» — опечатка"),

    # --- русизмы и грамматика ------------------------------------------------
    (9286, "example_uk",
     "Це дело виходить за межі моєї галузі компетенції",
     "Ця справа виходить за межі моєї компетенції",
     "«дело» — русизм, и «галузі» лишнее"),
    (10380, "example_uk",
     "Це тільки лінива відговорка",
     "Це просто дешева відмовка",
     "«відговорка» — русизм, «лінива» — калька"),
    (16495, "example_uk",
     "Розгнівана натовп зібралась на вулиці",
     "Розгніваний натовп зібрався на вулиці",
     "«натовп» мужского рода"),
    (15602, "example_uk",
     "Мій дідусь годами розводить голубів у своєму саду",
     "Мій дідусь роками розводить голубів у своєму саду",
     "«годами» — русизм"),
    (15338, "example_uk",
     "Мій супруг і я святкуємо цього року 25-річчя нашого весілля",
     "Ми з чоловіком святкуємо цього року 25-річчя весілля",
     "«супруг» — русизм, и перевод говорит «чоловік»"),

    # --- турецкая грамматика -------------------------------------------------
    (12275, "example_tr",
     "Antrenmanın ardından sauna gitmek hoşuma gidiyor",
     "Antrenmandan sonra saunaya gitmeyi severim",
     "пропущен дательный падеж"),
    (16664, "example_tr",
     "Japonyadan bir delegasyon şirketi ziyaret etti",
     "Japonya'dan bir heyet şirketi ziyaret etti",
     "пропущен апостроф в имени собственном"),
    (7884, "example_tr",
     "Cevabı elde yok",
     "Cevap şu an elimde yok",
     "неграмотная конструкция"),

    # --- неверный смысл ------------------------------------------------------
    (16929, "example_ru",
     "Судья вызвала свидетеля на судебное заседание",
     "Суд вызвал его в качестве свидетеля",
     "в немецком вызывает суд, а не судья"),
    (16929, "example_uk",
     "Суддя викликав свідка на судовий слух",
     "Суд викликав його як свідка",
     "«судовий слух» — не то слово, и вызывает суд"),

    # --- примеры про другое --------------------------------------------------
    (18059, "example_ru",
     "Северный полюс очень холодный",
     "Полюс Земли очень холодный и непригодный для жизни",
     "в немецком полюс Земли, и вторая половина фразы потеряна"),
    (18059, "example_uk",
     "Північний полюс дуже холодний",
     "Полюс Землі дуже холодний і непридатний для життя",
     "то же"),
    (12508, "example_tr",
     "Doktor hastayı kısa sürede iyileştirdi",
     "Yara çabuk iyileşecek",
     "в немецком заживает рана, а не врач лечит больного"),
    (7922, "example_pl",
     "Nasza łódka zaczęła tonąć",
     "Statek zatonął podczas sztormu",
     "лодка вместо корабля, и нет шторма"),
    (7192, "example_en",
     "We will continue on to Berlin",
     "You can continue reading",
     "в немецком про чтение"),
    (7192, "example_uk",
     "Ми продовжимо їхати в Берлін",
     "Ти можеш продовжити читання",
     "в немецком про чтение"),
    (7192, "example_tr",
     "Berline devam edeceğiz",
     "Okumaya devam edebilirsin",
     "в немецком про чтение, плюс пропущен апостроф"),
    (8456, "example_pl",
     "Trzeba wymienić żarówkę w lampie",
     "Trener zmienia zawodnika",
     "лампочка вместо замены игрока"),
    (10700, "example_tr",
     "Cevabında hiç kesinlik yoktu",
     "Geleceğinden emin değilim",
     "пример про другое"),
    (1652, "example_en",
     "His performance last night was amazing",
     "Your performance is good",
     "в немецком «твой результат», а не «его вчерашний»"),
    (11020, "example_pl",
     "Z ciężkim westchnieniem zamknął książkę",
     "Z westchnieniem poddał się i wyszedł z pokoju",
     "книга вместо того, что он сдался и вышел"),
    (14397, "example_en",
     "The crowd broke into loud applause",
     "The audience applauds",
     "в немецком настоящее время, публика хлопает"),
    (14397, "example_uk",
     "Після виступу лунали гучні аплодисменти",
     "Публіка аплодує",
     "то же"),
    (14397, "example_tr",
     "Sahneye çıkınca alkışlar başladı",
     "Seyirciler alkışlıyor",
     "то же"),
    (16632, "example_pl",
     "Jego wysiłki zostały uwieńczone sukcesem",
     "Projekt uwieńczony sukcesem zasługuje na uznanie",
     "пример про другое"),
    (6620, "example_en",
     "Please close the door properly",
     "I can't find my way around here",
     "пример про дверь, а немецкий про «не могу разобраться»"),
    (6620, "example_uk",
     "Не хвилюйся, я сам дам цьому раду",
     "Я тут ніяк не дам собі ради",
     "пример про другое"),
    (7876, "example_pl",
     "Zatrzymajmy się i chwilę odpocznijmy",
     "Po pięciu godzinach jazdy musimy wreszcie odpocząć",
     "потеряны пять часов езды"),
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
    if skipped:
        print("\n--- пропущено, в базе другое ---")
        for wid, col, cur in skipped:
            print(f"  {wid} {col}: {cur!r}")

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
