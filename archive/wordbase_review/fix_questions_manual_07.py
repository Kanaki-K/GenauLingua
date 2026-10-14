"""
Потерянная вопросительная форма, партия 7 — последняя. Класс закрыт.

Остаток списка `scan_question_mark`. Из содержательного:

* `niederlassen` — немецкий спрашивает собеседника, а все пять переводов
  говорят про неё («Она хочет поселиться в городе») или вовсе про них и
  про деревню.
* `vorbeifahren` — немецкий просит заехать в супермаркет, а пять языков
  описывают, как мимо проехала машина, не тормозя. Взято другое значение.
* `Scanner` — немецкий просит отсканировать, переводы сообщают, что «мы не
  можем отсканировать». Отрицание появилось из ничего.
* `abspielen` — к переводу приписана вторая фраза, которой в немецком нет:
  «Мне она очень нравится».

Попутные находки: немецкое «Ruslandreise» с одной «с», украинское «в офісу»
вместо «в офісі», турецкое «verirmisin» без пробела.

    python -m app.scripts.fix_questions_manual_07            # показать
    python -m app.scripts.fix_questions_manual_07 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- ошибка в немецком эталоне -------------------------------------------
    (17267, "example_de", "Brauchst du ein Visum für deine Ruslandreise?",
     "Brauchst du ein Visum für deine Russlandreise?",
     "«Ruslandreise» — пропущена «с»"),

    # --- потерян только знак ---------------------------------------------------
    (17509, "example_en", "On which channel is the movie",
     "On which channel is the movie?", "потерян только знак"),
    (17509, "example_uk", "На якому каналі йде фільм",
     "На якому каналі йде фільм?", "потерян только знак"),
    (17516, "example_ru", "Можешь переключить выключатель",
     "Можешь переключить выключатель?", "потерян только знак"),
    (17516, "example_uk", "Можеш переключити вимикач",
     "Можеш переключити вимикач?", "потерян только знак"),
    (17645, "example_ru", "Можешь ли ты переключиться на другой канал",
     "Можешь ли ты переключиться на другой канал?", "потерян только знак"),
    (17673, "example_ru", "Можешь, пожалуйста, запустить двигатель",
     "Можешь, пожалуйста, запустить двигатель?", "потерян только знак"),
    (17673, "example_uk", "Можеш, будь ласка, запустити двигун",
     "Можеш, будь ласка, запустити двигун?", "потерян только знак"),
    (18153, "example_ru", "Можешь накрыть на стол",
     "Можешь накрыть на стол?", "потерян только знак"),
    (18178, "example_ru", "Можешь дать мне полотенце",
     "Можешь дать мне полотенце?", "потерян только знак"),
    (18178, "example_uk", "Можеш дати мені рушник",
     "Можеш дати мені рушник?", "потерян только знак"),
    (18283, "example_ru", "Можешь ли ты разместить мою кузину на пару ночей",
     "Можешь ли ты разместить мою кузину на пару ночей?",
     "потерян только знак"),
    (18598, "example_ru", "Ты когда-нибудь ел суши",
     "Ты когда-нибудь ел суши?", "потерян только знак"),
    (18686, "example_pl", "Z jakiej okazji ta impreza",
     "Z jakiej okazji ta impreza?", "потерян только знак"),
    (18686, "example_tr", "Bu kutlamanın vesilesi nedir",
     "Bu kutlamanın vesilesi nedir?", "потерян только знак"),
    (18798, "example_ru", "Можешь мне пепельницу передать",
     "Можешь мне пепельницу передать?", "потерян только знак"),
    (18798, "example_uk", "Можеш мені попільницю передати",
     "Можеш мені попільницю передати?", "потерян только знак"),

    # --- опечатки и порядок слов, плюс знак ------------------------------------
    (18798, "example_tr", "Küllüğü bana verirmisin",
     "Küllüğü bana verir misin?",
     "«verirmisin» без пробела; и потерян знак"),
    (18283, "example_uk", "Можеш ти розмістити мою кузину на пару ночей",
     "Можеш розмістити мою кузину на пару ночей?",
     "порядок слов и потерянный знак"),
    (17814, "example_uk", "Я можу внести ідею", "Я можу внести свою ідею?",
     "потеряно «свою»; и знак"),
    (17619, "example_tr", "Telefon numaranız nedir",
     "Cep telefonu numaran ne?",
     "в немецком мобильный и «ты»; и потерян знак"),

    # --- приписана вторая фраза, которой в немецком нет -----------------------
    (17628, "example_ru",
     "Можно ещё раз включить эту песню? Мне она очень нравится",
     "Можно ещё раз включить эту песню?",
     "второй фразы в немецком нет"),
    (17628, "example_uk",
     "Можна ще раз включити пісню? Мені вона дуже подобається",
     "Можна ще раз включити пісню?",
     "второй фразы в немецком нет"),

    # --- вместо вопроса стоит повеление ----------------------------------------
    (17645, "example_pl", "Przełącz na inny kanał",
     "Możesz przełączyć na inny kanał?", "в немецком вопрос, а не приказ"),
    (17673, "example_pl", "Uruchom silnik, już jedziemy",
     "Możesz uruchomić silnik?",
     "в немецком вопрос, и «мы уже едем» там нет"),
    (18670, "example_pl", "Obudź mnie o siódmej",
     "Możesz mnie obudzić wcześnie rano?",
     "в немецком вопрос про утро, а не приказ про семь часов"),
    (18670, "example_ru", "Разбуди меня завтра рано",
     "Можешь разбудить меня завтра рано?",
     "в немецком вопрос, а не приказ"),
    (18798, "example_pl", "Podaj mi popielniczkę ze stołu",
     "Możesz mi podać popielniczkę?", "в немецком вопрос, а не приказ"),

    # --- отрицание появилось из ничего ----------------------------------------
    (17559, "example_en",
     "The scanner in the office is broken, we can't scan the document",
     "The scanner in the office is broken, can you scan the document?",
     "в немецком просьба отсканировать, а не «мы не можем»"),
    (17559, "example_ru",
     "Сканер в офисе сломан, мы не можем отсканировать документ",
     "Сканер в офисе сломан, можешь отсканировать документ?",
     "в немецком просьба отсканировать, а не «мы не можем»"),
    (17559, "example_tr",
     "Ofisteki tarayıcı bozuk, belgeyi tarayamıyoruz",
     "Ofisteki tarayıcı bozuk, belgeyi tarayabilir misin?",
     "в немецком просьба отсканировать, а не «мы не можем»"),
    (17559, "example_uk",
     "Сканер в офісу зламаний, ми не можемо відсканувати документ",
     "Сканер в офісі зламаний, можеш відсканувати документ?",
     "«в офісу» — неверный падеж; и в немецком просьба, а не «мы не можем»"),

    # --- перевод переводит другое предложение ---------------------------------
    (17267, "example_pl", "Potrzebujesz wizy na ten wyjazd",
     "Potrzebujesz wizy na podróż do Rosji?",
     "потеряна поездка в Россию; и знак"),
    (17267, "example_ru", "У тебя есть виза для поездки в Россию",
     "Тебе нужна виза для поездки в Россию?",
     "в немецком «нужна ли виза», а не «есть ли»"),
    (17267, "example_uk", "У тебе є віза для поїздки до Росії",
     "Тобі потрібна віза для поїздки до Росії?",
     "в немецком «нужна ли виза», а не «есть ли»"),
    (17272, "example_en", "The car passed by us without braking",
     "Can you stop by the supermarket?",
     "взято другое значение: «проехать мимо» вместо «заехать»"),
    (17272, "example_pl", "Autobus przejechał obok nas bez zatrzymania",
     "Możesz podjechać pod supermarket?",
     "взято другое значение: «проехать мимо» вместо «заехать»"),
    (17272, "example_ru", "Машина проехала мимо нас, не тормозя",
     "Можешь заехать в супермаркет?",
     "взято другое значение: «проехать мимо» вместо «заехать»"),
    (17272, "example_tr", "Araba frenlenmeden yanımızdan geçti",
     "Süpermarkete uğrayabilir misin?",
     "взято другое значение: «проехать мимо» вместо «заехать»"),
    (17272, "example_uk", "Машина проїхала повз нас, не гальмуючи",
     "Можеш заїхати в супермаркет?",
     "взято другое значение: «проехать мимо» вместо «заехать»"),
    (18363, "example_en", "She wants to settle in the city",
     "You want to settle in the city?",
     "в немецком вопрос «ты», а не рассказ про неё"),
    (18363, "example_pl", "Chcą się osiedlić na wsi",
     "Chcesz się osiedlić w mieście?",
     "в немецком «ты» и город, а не «они» и деревня"),
    (18363, "example_ru", "Она хочет поселиться в городе",
     "Ты хочешь поселиться в городе?",
     "в немецком вопрос «ты», а не рассказ про неё"),
    (18363, "example_tr", "Şehirde yerleşmek istiyor",
     "Şehirde yerleşmek mi istiyorsun?",
     "в немецком вопрос «ты», а не рассказ про неё"),
    (18363, "example_uk", "Вона хоче поселитися в місті",
     "Ти хочеш поселитися в місті?",
     "в немецком вопрос «ты», а не рассказ про неё"),
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
