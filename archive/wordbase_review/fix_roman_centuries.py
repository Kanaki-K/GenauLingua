"""Римские цифры в примерах: век написан так, что движок читает по буквам.

НАШЛОСЬ НЕ ГЛАЗАМИ. После досинтеза прогнан `tts_audit_clips` — дешёвая
проверка длительности. Она дала два подозрительных клипа на 121 347, и
один из них: русское «XXI век» звучит 3,3 секунды вместо ожидаемых 1,4.
Втрое дольше короткой фразы — значит движок произносит не число, а
буквы: «икс икс и».

Дальше сплошной поиск по базе: 41 ячейка с римским числом. Из них 12
законны — это сокращения, которые и читаются по буквам: `CV`
(резюме), `IV drip` (капельница). Остальные 29 — века в русской,
украинской и польской колонках.

ПОЧЕМУ ПРАВИТСЯ ТЕКСТ, А НЕ КОД. Напрашивалось добавить разворот
римских чисел в `tts_text`, как сделано для арабских. Но век требует
согласования падежа: «в XIX веке» это «в девятнадцатом веке», «до
XVIII века» — «до восемнадцатого», «XXI век» — «двадцать первый».
Падеж зависит от предлога и от языка, кодом это не берётся без
морфологии трёх языков.

А образец уже есть в самой базе. Ряд 2589, тот же `Jahrhundert`:
польская ячейка написана «Dwudziesty pierwszy wiek» — словами. Значит
решение принято раньше и здесь просто не доведено до конца.

Выигрыш не только в озвучке: учащийся видит словоформу, а не римскую
запись, которую ему всё равно пришлось бы проговаривать словами.

Немецкая и английская колонки не тронуты: там «Das 21. Jahrhundert» и
«The 21st century», арабские цифры, и их `expand_numbers` разворачивает
сам. Турецкая «21. yüzyıl» тоже.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (2589, "example_ru",
     "XXI век",
     "Двадцать первый век",
     "«XXI» движок читает по буквам; польская ячейка этого ряда уже словами"),
    (2589, "example_uk",
     "XXI століття",
     "Двадцять перше століття",
     "то же"),
    (9929, "example_ru",
     "Это редкая золотая монета XVIII века",
     "Это редкая золотая монета восемнадцатого века",
     "римское число словами, с падежом по предлогу"),
    (9929, "example_uk",
     "Це рідкісна золота монета XVIII століття",
     "Це рідкісна золота монета вісімнадцятого століття",
     "то же"),
    (9929, "example_pl",
     "To rzadka złota moneta z XVIII wieku",
     "To rzadka złota moneta z osiemnastego wieku",
     "то же"),
    (12943, "example_pl",
     "Cholera była w XIX wieku groźną chorobą",
     "Cholera była w dziewiętnastym wieku groźną chorobą",
     "то же"),
    (12973, "example_ru",
     "В XIX веке многие люди умирали от брюшного тифа",
     "В девятнадцатом веке многие люди умирали от брюшного тифа",
     "то же"),
    (12973, "example_uk",
     "У XIX столітті багато людей померло від черевного тифу",
     "У дев'ятнадцятому столітті багато людей померло від черевного тифу",
     "то же"),
    (12973, "example_pl",
     "W XIX wieku wielu ludzi umarło na tyfus",
     "W dziewiętnastym wieku wielu ludzi umarło na tyfus",
     "то же"),
    (13033, "example_uk",
     "Туберкульоз був причиною смерті в XIX столітті",
     "Туберкульоз був причиною смерті у дев'ятнадцятому столітті",
     "то же"),
    (13033, "example_pl",
     "Gruźlica była w XIX wieku przyczyną śmierci",
     "Gruźlica była w dziewiętnastym wieku przyczyną śmierci",
     "то же"),
    (13752, "example_ru",
     "Корсет был в моде в XIX веке",
     "Корсет был в моде в девятнадцатом веке",
     "то же"),
    (13752, "example_uk",
     "Корсет був у моді в XIX столітті",
     "Корсет був у моді у дев'ятнадцятому столітті",
     "то же"),
    (13752, "example_pl",
     "Korset był modny w XIX wieku",
     "Korset był modny w dziewiętnastym wieku",
     "то же"),
    (14838, "example_ru",
     "Этот предмет мебели — настоящий антиквариат XVIII века",
     "Этот предмет мебели — настоящий антиквариат восемнадцатого века",
     "то же"),
    (14838, "example_uk",
     "Цей предмет меблів — справжній антикваріат XVIII століття",
     "Цей предмет меблів — справжній антикваріат вісімнадцятого століття",
     "то же"),
    (14838, "example_pl",
     "Ten mebel to prawdziwy antyk z XVIII wieku",
     "Ten mebel to prawdziwy antyk z osiemnastego wieku",
     "то же"),
    (15201, "example_ru",
     "Я исследовал своё генеалогическое дерево до XVIII века",
     "Я исследовал своё генеалогическое дерево до восемнадцатого века",
     "то же"),
    (15201, "example_uk",
     "Я досліджував свій родовід аж до XVIII століття",
     "Я досліджував свій родовід аж до вісімнадцятого століття",
     "то же"),
    (15201, "example_pl",
     "Zbadałem swoje drzewo genealogiczne aż do XVIII wieku",
     "Zbadałem swoje drzewo genealogiczne aż do osiemnastego wieku",
     "то же"),
    (15298, "example_ru",
     "Наша семейная история уходит в XVIII век",
     "Наша семейная история уходит в восемнадцатый век",
     "то же"),
    (15298, "example_uk",
     "Наша сімейна історія сягає XVIII століття",
     "Наша сімейна історія сягає вісімнадцятого століття",
     "то же"),
    (15298, "example_pl",
     "Nasza historia rodziny sięga XVIII wieku",
     "Nasza historia rodziny sięga osiemnastego wieku",
     "то же"),
    (16450, "example_ru",
     "Коммунизм был важным движением в XX веке",
     "Коммунизм был важным движением в двадцатом веке",
     "то же"),
    (16450, "example_uk",
     "Комунізм був важливим рухом XX століття",
     "Комунізм був важливим рухом двадцятого століття",
     "то же"),
    (16450, "example_pl",
     "Komunizm był ważnym ruchem XX wieku",
     "Komunizm był ważnym ruchem dwudziestego wieku",
     "то же"),
    (16684, "example_ru",
     "Социализм — это политическая идеология XX века",
     "Социализм — это политическая идеология двадцатого века",
     "то же"),
    (16684, "example_uk",
     "Соціалізм — це політична ідеологія XX століття",
     "Соціалізм — це політична ідеологія двадцятого століття",
     "то же"),
    (16684, "example_pl",
     "Socjalizm to ideologia polityczna XX wieku",
     "Socjalizm to ideologia polityczna dwudziestego wieku",
     "то же"),
    (16937, "example_uk",
     "У XIX столітті притулки були місцем для нужденних",
     "У дев'ятнадцятому столітті притулки були місцем для нужденних",
     "то же"),
    (16937, "example_pl",
     "W XIX wieku przytułki były schronieniem dla potrzebujących",
     "W dziewiętnastym wieku przytułki były schronieniem dla potrzebujących",
     "то же"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
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
