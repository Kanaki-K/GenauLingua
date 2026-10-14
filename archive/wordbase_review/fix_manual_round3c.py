"""
Третий круг вычитки, ряды 155–204.

Самое заметное:

* `Zeitlupe` — ошибка в самом немецком примере: «zeigte jeden Detail»
  вместо «jedes Detail». Немецкий здесь эталон для пяти переводов, и если
  он неверен, учится неверное.
* `lügen` — турецкое слово разорвано пробелом: «söylememeli sin».
* `machbar` — украинское «виконуємий», такого слова нет.
* `gesegnet` — «благословленною» вместо «благословенною».
* `Aufforderung` — в немецком «я получил», в украинском и турецком «он».
* `ausbilden` — в немецком «молодых людей», в польском «молодых механиков».

    python -m app.scripts.fix_manual_round3c            # показать
    python -m app.scripts.fix_manual_round3c --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [

    # --- ошибка в немецком эталоне -------------------------------------------
    (18892, "example_de",
     "Die Zeitlupe zeigte jeden Detail des Unfalls ganz deutlich",
     "Die Zeitlupe zeigte jedes Detail des Unfalls ganz deutlich",
     "«jeden Detail» — Detail среднего рода, нужно «jedes»"),

    # --- разорванные и несуществующие слова -----------------------------------
    (10086, "example_tr",
     "Yalan söylememeli sin",
     "Yalan söylememelisin",
     "слово разорвано пробелом"),
    (7613, "example_uk",
     "Цей план абсолютно виконуємий за два тижні",
     "Цей план цілком здійсненний за два тижні",
     "«виконуємий» — такого слова нет"),
    (14451, "example_uk",
     "Він був благословленною людиною зі щасливою сім'єю",
     "Він був благословенною людиною зі щасливою сім'єю",
     "опечатка в слове"),

    # --- турецкая грамматика --------------------------------------------------
    (10788, "example_tr",
     "Maceranın cazibesinin onu çekiyor",
     "Maceranın cazibesi onu çekiyor",
     "лишний родительный падеж"),
    (18728, "example_tr",
     "Günlük rutin beni organize kalmam sağlıyor",
     "Günlük rutin organize kalmamı sağlıyor",
     "неграмотная конструкция"),
    (14534, "example_tr",
     "Dini inanç göre dünya Tanrının yaratılışıdır",
     "Dini inanca göre dünya Tanrı'nın yaratılışıdır",
     "пропущен дательный падеж и апостроф"),
    (17855, "example_tr",
     "Malzemeleri depolamak için depo doldu",
     "Depo malzemelerle dolu",
     "фраза не о том и построена неверно"),
    (15021, "example_tr",
     "Annem-babam beni sıkı yetiştirdi",
     "Annem babam beni sıkı yetiştirdi",
     "дефис между словами не ставится"),

    # --- неверное лицо и подмена слова ----------------------------------------
    (14239, "example_uk",
     "Він отримав вимогу оплатити свій внесок",
     "Я отримав вимогу сплатити свій внесок",
     "в немецком «я», а не «он»"),
    (14239, "example_tr",
     "Katkısını ödeme talebini aldı",
     "Aidatımı ödemem için bir talep aldım",
     "в немецком «я», а не «он»"),
    (9568, "example_pl",
     "Kształcimy młodych mechaników",
     "Kształcimy młodych ludzi",
     "механики вместо молодых людей"),

    # --- украинские огрехи ----------------------------------------------------
    (2628, "example_uk",
     "Деревина гриміла під вагою",
     "Дерево тріснуло, коли він на нього наступив",
     "«гриміла» — не то слово, и пример про другое"),
    (14534, "example_uk",
     "Світ - творення Бога",
     "Згідно з релігійними уявленнями світ — творіння Бога",
     "потеряна половина фразы, и дефис вместо тире"),

    # --- примеры про другое ---------------------------------------------------
    (11090, "example_uk",
     "Оце нахаба — проліз без черги!",
     "Цей нахаба поводиться як дитина",
     "пример про другое"),
    (15766, "example_uk",
     "Ремінь вдавлюється мені в живіт",
     "Берегова лінія в цьому місці глибоко врізається в сушу",
     "пример про ремень, а немецкий про береговую линию"),
    (15766, "example_pl",
     "Za te kradzieże wsadzili go do więzienia",
     "Linia brzegowa w tym miejscu głęboko się wcina",
     "взято другое значение слова"),
    (10086, "example_pl",
     "Nie kłam mi w oczy",
     "Nie powinieneś kłamać",
     "в немецком «ты не должен лгать»"),
    (17855, "example_pl",
     "Towar leży jeszcze w magazynie",
     "Magazyn jest pełen materiałów",
     "пример про другое"),
    (18728, "example_pl",
     "Codzienna rutyna bardzo mi pomaga",
     "Codzienna rutyna pomaga mi zachować porządek",
     "потеряно «оставаться организованным»"),
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
