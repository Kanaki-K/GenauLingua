"""
Третий круг вычитки, ряды 103–154.

Самое заметное:

* `Brut` — спутаны омонимы. Немецкое Brut это птичий выводок, а в украинском
  и турецком примерах шампанское брют: «Шампанське брют для тосту». Слово
  то же на вид, значение другое.
* `pflücken` — заголовок инфинитив «срывать», а все переводы причастия
  «сорванный, picked, zerwany». Человек учит не ту часть речи.
* `der Verlobter` — неверная немецкая форма, нужно «der Verlobte».
  И в украинском «нареченець» вместо «наречений».
* `Flugsteig` — в турецком примере английское «Boarding gate».
* `irgendjemand` — польское «kto- kolwiek» разорвано пробелом.

    python -m app.scripts.fix_manual_round3b            # показать
    python -m app.scripts.fix_manual_round3b --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [

    # --- спутаны омонимы -----------------------------------------------------
    (11896, "example_uk",
     "Шампанське брют для тосту",
     "Птахи-батьки годують своїх пташенят",
     "Brut — это птичий выводок, а не шампанское"),
    (11896, "example_tr",
     "Şampanya brut bir şişe tost için",
     "Kuş ebeveynler yavrularını besliyor",
     "то же: не шампанское, а выводок"),
    (11896, "example_en",
     "The hen is feeding her brood",
     "The bird parents are feeding their brood",
     "в немецком оба родителя, а не курица"),

    # --- неверная часть речи --------------------------------------------------
    (15715, "translation_ru",
     "сорванный, собранный",
     "срывать, собирать",
     "заголовок — инфинитив, а перевод стоял причастием"),
    (15715, "translation_uk",
     "зірваний, зібраний",
     "зривати, збирати",
     "то же"),
    (15715, "translation_en",
     "picked, plucked, gathered",
     "to pick, to pluck, to gather",
     "то же"),
    (15715, "translation_tr",
     "toplanmış, koparılmış",
     "toplamak, koparmak",
     "то же"),
    (15715, "translation_pl",
     "zerwany, zebrany",
     "zrywać, zbierać",
     "то же"),

    # --- неверные формы ------------------------------------------------------
    (15043, "word_de",
     "Verlobter",
     "Verlobte",
     "«der Verlobter» — неверная форма, нужно «der Verlobte»"),
    (15043, "example_uk",
     "Мій нареченець та я одружуємось наступного місяця",
     "Ми з нареченим одружуємося наступного місяця",
     "«нареченець» — такого слова нет"),
    (13444, "translation_pl",
     "ktoś, kto- kolwiek",
     "ktoś, ktokolwiek",
     "слово разорвано пробелом"),

    # --- чужой язык и опечатки ------------------------------------------------
    (17333, "example_tr",
     "Boarding gate numarası biletinde yazıyor",
     "Uçuş 5 numaralı kapıdan kalkıyor, lütfen anonsu dinleyin",
     "английское «Boarding gate» в турецком, и пример про другое"),
    (16803, "example_tr",
     "Mahkeme duruşması yarın saat 10da gerçekleşecek",
     "Mahkeme duruşması yarın saat 10'da gerçekleşecek",
     "пропущен апостроф"),
    (11536, "example_tr",
     "Onun kaderi gerçekten yazıklı idi",
     "Onun kaderi gerçekten acınacak haldeydi",
     "«yazıklı» — такого слова нет"),
    (10416, "example_tr",
     "Onun çok çekiciliği var",
     "Onda büyük bir çekicilik var",
     "неграмотная конструкция"),
    (8278, "example_uk",
     "Це привабливо цікава ідея",
     "Це приваблива й цікава ідея",
     "калька, по-украински так не говорят"),

    # --- примеры про другое ---------------------------------------------------
    (1665, "example_en",
     "She had a strong desire to travel",
     "I don't feel like it",
     "в немецком «у меня нет желания»"),
    (1813, "example_en",
     "She plays the main role in the film",
     "That doesn't matter",
     "в немецком «это не играет роли»"),
    (1813, "example_tr",
     "Bu filmde küçük bir rol aldı",
     "Bunun bir önemi yok",
     "в немецком «это не играет роли»"),
    (786, "example_uk",
     "Діти шукали скарб у саду",
     "Ти мій скарб",
     "в немецком обращение к человеку"),
    (483, "example_uk",
     "Купи кілограм вишень на ринку",
     "Вишні солодкі на смак",
     "в немецком про вкус, а не про покупку"),
    (16803, "example_pl",
     "Rozprawa sądowa odbędzie się w poniedziałek",
     "Rozprawa sądowa odbędzie się jutro o dziesiątej",
     "понедельник вместо завтрашних десяти часов"),
    (18321, "example_uk",
     "Після знесення повсюди лежав щебінь на вулиці",
     "Після знесення уламки лежали по всій вулиці",
     "щебень вместо обломков"),
    (15243, "example_tr",
     "Ufaklık bütün gün uyumadı",
     "Ufaklık bütün gün sızlandı",
     "не спал вместо «ныл»"),
    (15859, "example_uk",
     "Канарка співає голосно кожного ранку",
     "Канарка щоранку голосно співає",
     "порядок слов"),
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
    print("word_de у Verlobte изменён — нужна пересборка групп и пересинтез")

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
