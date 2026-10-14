"""ВТОРОЙ ПРОХОД, блок 20 (ряды 3801–4000): 18 правок.

БЛОК ЗАМЕТНО ЧИЩЕ ПРЕДЫДУЩИХ, и это стоит записать: 18 правок против
66 в блоке 19 и 71 в блоке 18. Состав блока — ранги 6895–7163, то есть
конкретные существительные B2 с короткими описательными примерами
(`Niere`, `Yen`, `Laken`, `Armband`, `Turnier`). Там, где пример просто
называет вещь, ошибаться почти негде. Низкий улов здесь — свойство
состава, а не признак того, что я читал хуже.

ЗАМЕР: СЛОВО ДВАЖДЫ ПОДРЯД. Приём из блока 19 («починив ряд, посмотри
близнецов») сработал сразу: `diskret` (10499) повторял украинскую
запинку «Будь, будь ласка», которую я правил у `geduldig` (2504).
Запинка при чтении вслух — признак формальный, напрашивался гейт.

По базе: **75 попаданий, настоящих три.** И причина провала —
грамматика одного языка: 64 попадания турецкие, и все законные.
Удвоение в турецком это способ образования наречий, а не опечатка:
«sık sık» (часто), «yavaş yavaş» (медленно), «dik dik» (уставившись),
«boş boş» (праздно), «zaman zaman» (время от времени), «pırıl pırıl»,
«hıçkıra hıçkıra». Русские «что что-то не так» и польские «Nie, nie
mam ochoty» тоже законны.

Гейта не вышло. Но примета всё равно оправдалась, и вот чем:

    dritt (7182)  de «Das ist schon die dritte Flasche Milch diese Woche»
        tr «Bu bu hafta üçüncü süt şişesi» — запинка, из-за неё я и
            полез смотреть ряд
        pl «To już trzecia KAWA dzisiaj» — ПОДМЕНА: польская ячейка
            скопирована из ряда-близнеца `dritter` (13515), где пример
            действительно про кофе

То есть слабый признак довёл до подмены, которую сам он найти не мог.
Это стоит отдельной записи: примета с долей настоящих 3 из 75 не годится
в гейт, но годится как повод посмотреть ряд глазами.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ подмена, найденная через запинку ═════════════════════════
    (7182, "example_pl",
     "To już trzecia kawa dzisiaj",
     "To już trzecia butelka mleka w tym tygodniu",
     "ячейка скопирована из ряда-близнеца `dritter` (13515), где про кофе"),
    (7182, "example_tr",
     "Bu bu hafta üçüncü süt şişesi",
     "Bu, bu haftanın üçüncü süt şişesi",
     "«Bu bu» — запинка при чтении вслух"),
    (1125, "example_tr",
     "Atık cam cam konteynerine atılır",
     "Atık cam, cam konteynerine atılır",
     "«cam cam» подряд: запятая разводит две разные группы"),
    (10499, "example_uk",
     "Будь, будь ласка, тактовним і не розповідай нікому мій секрет",
     "Будь ласка, будь тактовним і не розповідай нікому мій секрет",
     "«Будь, будь» — та же запинка, что у `geduldig` (2504) в блоке 19"),

    # ══ потерянное слово ════════════════════════════════════════
    (13668, "example_uk",
     "Він потягнув мене за комір куртки",
     "Він потягнув мене назад за комір куртки",
     "потеряно «zurück»: в ru, en и tr оно есть"),
    (13668, "example_pl",
     "Pociągnął mnie za kołnierz kurtki",
     "Odciągnął mnie za kołnierz kurtki",
     "то же: «od-» несёт «назад»"),
    (16180, "example_ru",
     "В Средневековье преступников казнили через отрубание головы",
     "В Средневековье было принято отрубать преступникам голову",
     "потеряно «üblich»: в tr и pl оно есть"),
    (16180, "example_uk",
     "У Середньовіччі злочинців страчували через відрубання голови",
     "У Середньовіччі було звичаєм відрубувати злочинцям голову",
     "то же"),
    (16180, "example_en",
     "In the Middle Ages criminals were executed by beheading",
     "In the Middle Ages it was common to behead criminals",
     "то же"),
    (10507, "example_tr",
     "Yabancılara karşı şüpheci",
     "O, yabancılara karşı şüpheci",
     "потеряно подлежащее"),

    # ══ добавленное слово ═══════════════════════════════════════
    (14023, "example_tr",
     "Planına yapılan eleştiri tamamen haksız değildi",
     "Planına yapılan eleştiri haksız değildi",
     "«tamamen» в эталоне нет, и оно переворачивает двойное отрицание"),
    (14029, "example_pl",
     "Przekażę mu tę wiadomość",
     "Przekażę tę wiadomość",
     "«mu» в эталоне «Ich werde die Nachricht überbringen» нет"),

    # ══ управление и слово не из своего списка ══════════════════
    (18725, "example_ru",
     "Будущие поколения должны учиться на нас",
     "Будущие поколения должны учиться у нас",
     "«учиться на нас» значит «на нашем примере плохого»; нужно «у нас»"),
    (18725, "example_uk",
     "Майбутні покоління повинні вчитися на нас",
     "Майбутні покоління повинні вчитися в нас",
     "то же"),
    (10510, "example_tr",
     "Talimatlar çok karışık, anlamıyorum",
     "Talimatlar çok kafa karıştırıcı, anlamıyorum",
     "«karışık» это перепутанный, а в списке «kafa karıştırıcı»"),

    # ══ время глагола ═══════════════════════════════════════════
    (13174, "example_tr",
     "Göbek, göbek kordonu bağlı olan noktadır",
     "Göbek, göbek kordonunun bağlı olduğu noktadır",
     "эталон «verbunden war» в прошедшем, и падеж не согласован"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    seen: set[tuple[int, str]] = set()
    dupes: list[tuple[int, str]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            if (wid, col) in seen:
                dupes.append((wid, col))
            seen.add((wid, col))
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
        print("\nсухой прогон. применить: --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(
                text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now:
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
