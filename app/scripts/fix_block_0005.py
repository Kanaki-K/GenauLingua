"""
Сплошная вычитка, блок 5: ряды 401–500 по рангу частотности.

Находки:

* `tu` — немецкий пример был «Ich mach das morgen». Ряд про глагол «tun», а
  в примере стоит «mach»: слова, которому посвящён ряд, в нём нет вовсе.
* `jede` — немецкий пример «Jeder kann das lernen», то есть мужская форма,
  хотя ряд про женскую. И он дословно повторял пример ряда `jeder` (id
  13330): две карточки учили одному и тому же. Теперь здесь «Jede Frau»,
  и переводы за ним.
* `ziehen` — немецкий «Du musst die Tür ziehen, nicht drücken», а
  английский, украинский и турецкий тянут верёвку.
* `verlieren` — в немецком «мне нельзя потерять ключ», в украинском и
  турецком ключ уже потерян, в английском приказ «не теряй снова».
* `Eltern` — польские родители живут в Кракове, немецкие в Кёльне.
* `Menge` — все три языка про разное: про оплаченную сумму, про число
  учеников и про молоко в холодильнике.
* `Kumpel` — русское «кореш» грубее немецкого «Kumpel».

    python -m app.scripts.fix_block_0005            # показать
    python -m app.scripts.fix_block_0005 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- слова ряда нет в его примере -----------------------------------------
    (6265, "example_de", "Ich mach das morgen", "Das tu ich morgen",
     "ряд про «tun», а в примере стоит «mach»"),

    # --- ряд про женскую форму, а пример в мужской и дублирует чужой ----------
    (13372, "example_de", "Jeder kann das lernen",
     "Jede Frau kann das lernen",
     "ряд про «jede», а пример в мужской форме и дословно повторяет ряд 13330"),
    (13372, "example_en", "Everyone can learn this",
     "Every woman can learn this", "вслед за немецким"),
    (13372, "example_ru", "Каждый может этому научиться",
     "Каждая женщина может этому научиться", "вслед за немецким"),
    (13372, "example_uk", "Кожен може це вивчити",
     "Кожна жінка може це вивчити", "вслед за немецким"),
    (13372, "example_tr", "Herkes bunu öğrenebilir",
     "Her kadın bunu öğrenebilir", "вслед за немецким"),
    (13372, "example_pl", "Każdy może się tego nauczyć",
     "Każda kobieta może się tego nauczyć", "вслед за немецким"),

    # --- пример переводит другую фразу ----------------------------------------
    (13367, "example_uk", "Я на це не погоджуюся",
     "Я з нетерпінням чекаю на це",
     "в немецком «я этого жду», а не «я не соглашаюсь»"),
    (1052, "example_tr", "Nereye gidiyoruz?", "Nereye gidiyorsun?",
     "в немецком «ты», а не «мы»"),
    (1039, "example_en", "Seeing her again made me happy", "Goodbye",
     "в немецком «до свидания», а не «встреча с ней обрадовала»"),
    (219, "example_pl", "Moi rodzice mieszkają w Krakowie",
     "Moi rodzice mieszkają w Kolonii", "в немецком Кёльн, а не Краков"),
    (2603, "example_tr", "Bu soru benim için çok zor",
     "Sabırsızlıkla bekliyorum",
     "пример про трудный вопрос, а немецкий «едва могу дождаться»"),
    (200, "example_tr", "Bugün izinliyim, işe gitmiyorum",
     "Bugün daha uzun kalabiliriz",
     "в немецком «нам можно остаться дольше»"),
    (13374, "example_pl", "Kupiłem sześć jajek", "Mam sześć jabłek",
     "в немецком «у меня шесть яблок», а не «я купил шесть яиц»"),
    (15926, "example_ru", "Король живёт в замке", "Король носит корону",
     "в немецком король носит корону"),
    (13375, "example_pl", "Mam dziesięć złotych", "Mam dziesięć lat",
     "в немецком «мне десять лет», а не про деньги"),
    (1685, "example_en", "I paid the full amount yesterday",
     "A large crowd of people was there",
     "в немецком большая толпа людей"),
    (1685, "example_uk", "Кількість учнів у класі зросла",
     "Там була велика кількість людей",
     "в немецком большая толпа людей"),
    (1685, "example_tr", "Dolapta az miktarda süt kaldı",
     "Orada büyük bir kalabalık vardı",
     "в немецком большая толпа людей"),
    (10051, "example_pl", "Ten upał to piekło", "To jest piekło",
     "«жара» в немецком не упомянута"),
    (1092, "example_en", "It is like that everywhere",
     "It happens everywhere", "в немецком «это случается», а не «так бывает»"),
    (1092, "example_uk", "Так всюди", "Це трапляється всюди",
     "фраза без глагола, и в немецком «случается»"),
    (1092, "example_tr", "Bu her yerde böyle", "Bu her yerde oluyor",
     "в немецком «случается», а не «так бывает»"),
    (1972, "example_en", "It was raining; nevertheless we walked",
     "It's raining, but I'm going anyway",
     "в немецком «я», а не «мы», и настоящее время"),
    (1972, "example_uk", "Було холодно, попри це ми гуляли",
     "Іде дощ, але я все одно піду",
     "в немецком дождь и «я», а не холод и «мы»"),
    (547, "example_uk", "Він вчить англійську вже два роки",
     "Я вчу німецьку", "в немецком «я учу немецкий»"),
    (1642, "example_en", "I run every day",
     "I run in the park every day", "потеряно «в парке»"),
    (1642, "example_uk", "Я бігаю щодня", "Я щодня бігаю в парку",
     "потеряно «в парке»"),
    (1642, "example_tr", "Her gün koşuyorum", "Her gün parkta koşuyorum",
     "потеряно «в парке»"),
    (6285, "example_en", "I'm pulling my rope",
     "You have to pull the door, not push",
     "в немецком про дверь, а не про верёвку"),
    (6285, "example_uk", "Я тягну мою мотузку",
     "Двері потрібно тягнути, а не штовхати",
     "в немецком про дверь, а не про верёвку"),
    (6285, "example_tr", "İpimi çekiyorum",
     "Kapıyı çekmen gerekiyor, itmen değil",
     "в немецком про дверь, а не про верёвку"),
    (2041, "example_en", "Don't lose your keys again!",
     "I mustn't lose the key",
     "в немецком «мне нельзя потерять», а не приказ"),
    (2041, "example_uk", "Я втратив ключ", "Мені не можна загубити ключ",
     "в немецком ключ ещё не потерян"),
    (2041, "example_tr", "Anahtarımı kaybettim",
     "Anahtarı kaybetmemem gerek", "в немецком ключ ещё не потерян"),
    (10054, "example_uk", "Я живу один у квартирі", "Я йду в кіно сам",
     "в немецком «я иду в кино один»"),
    (2339, "example_en", "That's why I'm not coming",
     "I'm sick, that's why I'm not coming", "потеряно «я болею»"),
    (2339, "example_tr", "Bu yüzden gelmiyorum",
     "Hastayım, bu yüzden gelmiyorum", "потеряно «я болею»"),
    (6289, "example_en", "The cat has disappeared",
     "I just want to disappear from here",
     "в немецком «я хочу отсюда исчезнуть», а не про кошку"),
    (6289, "example_uk", "Кішка зникла", "Я просто хочу звідси зникнути",
     "в немецком «я хочу отсюда исчезнуть», а не про кошку"),
    (6289, "example_tr", "Kedi kayboldu", "Buradan kaybolmak istiyorum",
     "в немецком «я хочу отсюда исчезнуть», а не про кошку"),
    (391, "example_uk", "Ми одружуємося наступного місяця",
     "Вони одружуються в червні",
     "в немецком «они» и июнь, а не «мы» и следующий месяц"),
    (229, "example_pl", "Wyjaśnij mi, jak to działa",
     "On wyjaśnia zadanie",
     "в немецком «он объясняет задание», а не просьба"),

    # --- вежливая форма и лишнее --------------------------------------------
    (1865, "example_tr", "Lütfen oturun", "Lütfen otur",
     "в немецком «Setz dich» — ты, а не Вы"),
    (1736, "example_uk", "Який ваш номер телефону?",
     "Який твій номер телефону?", "в немецком «deine» — твой"),
    (537, "example_tr", "Lütfen yavaş konuşun", "Lütfen yavaş konuş",
     "в немецком «sprich» — ты, а не Вы"),
    (537, "example_uk", "Будь ласка, говори повільніше",
     "Будь ласка, говори повільно",
     "в немецком «langsam», а не «медленнее»"),
    (10055, "example_pl", "Ufam ci całkowicie", "Ufam ci",
     "«całkowicie» в немецком нет"),

    # --- неестественно сказано ------------------------------------------------
    (1630, "example_ru", "Это мой кореш", "Это мой приятель",
     "«кореш» грубее немецкого «Kumpel»"),
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
