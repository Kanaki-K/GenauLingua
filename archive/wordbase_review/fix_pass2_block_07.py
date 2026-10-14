"""ВТОРОЙ ПРОХОД, блок 7 (ряды 1201–1400): правки, найденные глазами,
плюс сквозной класс, который из них вырос.

КЛАСС: УСЕЧЁННОЕ ПЕРВОЕ ЛИЦО В ЭТАЛОНЕ. Блок дал `Ich genieß die
Ruhe` — ровно предмет `scan_de_colloquial`, и примета промолчала,
потому что основы `genieß` не было в её списке. Это ПЯТАЯ дыра в одном
и том же месте того скрипта: за проход там находили то отсутствующую
приставку, то регистр артикля, то основы на `-ier`, то `sitz`. Каждый
раз список дополняли по найденному примеру — и каждый раз он протекал
снова.

Поэтому вместо шестого дополнения списка написан гейт без перечислений
(`scan_de_first_person_e`): у немецкого глагола первое лицо
единственного ВСЕГДА кончается на «-e», а основы берутся из рядов VERB
самой базы. По базе гейт дал пять рядов:

    genießen (1472)      Ich genieß die Ruhe
    lenken (2658)        Ich lenk das Auto durch die Stadt
    vollgestopft (8469)  ich krieg ihn kaum zu
    nachschlagen (9626)  ich schlag das Wort mal eben nach
    frisieren (13775)    Ich lass mir morgens die Haare frisieren

У последнего ряда усечение ещё и ВТОРОЕ, в конце подчинённой фразы:
«bevor ich zur Arbeit geh». Его гейт не видит и видеть не может —
там глагол отделён от «ich» дополнениями, и позиция не помогает. Это
записано в докстринге приметы как её предел.

Отдельно стоит отметить два ряда, найденных глазами:

    Rechnung (1785)  tr «FATURA lütfen»
        «fatura» это счёт-фактура, бухгалтерский документ. В ресторане
        просят «hesap». Эталон «Die Rechnung bitte» — ресторанная
        фраза, и все остальные языки так её и поняли.

    Samstag (781)  ru «В субботу я СВОБОДНА», uk «я ВІЛЬНА»
        Женский род, тогда как ряд-близнец `Freitag` с тем же эталоном
        «Am ... bin ich frei» написан в мужском. Немецкий рода не
        показывает, и расхождение видно только если положить два ряда
        рядом.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── КЛАСС: усечённое первое лицо в эталоне ───────────────────
    (1472, "example_de",
     "Ich genieß die Ruhe",
     "Ich genieße die Ruhe",
     "у первого лица «-e» обязательно: голого «genieß» в немецком нет"),
    (2658, "example_de",
     "Ich lenk das Auto durch die Stadt",
     "Ich lenke das Auto durch die Stadt",
     "то же"),
    (8469, "example_de",
     "Der Koffer ist völlig vollgestopft, ich krieg ihn kaum zu",
     "Der Koffer ist völlig vollgestopft, ich kriege ihn kaum zu",
     "то же"),
    (9626, "example_de",
     "Moment, ich schlag das Wort mal eben im Wörterbuch nach",
     "Moment, ich schlage das Wort mal eben im Wörterbuch nach",
     "то же"),
    (13775, "example_de",
     "Ich lass mir morgens die Haare frisieren, bevor ich zur Arbeit geh",
     "Ich lasse mir morgens die Haare frisieren, bevor ich zur Arbeit gehe",
     "два усечения в одном ряду; второе в конце фразы, гейт его не видит"),

    # ── подменённое слово ────────────────────────────────────────
    (1785, "example_tr",
     "Fatura lütfen",
     "Hesap lütfen",
     "«fatura» это счёт-фактура; в ресторане просят «hesap»"),
    (2127, "example_tr",
     "Giriş kapalı",
     "Erişim engellendi",
     "«giriş» это вход, а «Zugang» здесь доступ, как в остальных четырёх"),
    (13449, "example_uk",
     "Дощ іде, все ж таки ми йдемо гуляти",
     "Дощ іде, все ж таки ми виходимо на вулицю",
     "«гуляти» это прогулка, а «raus» — выйти наружу"),
    (481, "example_uk",
     "Ми йдемо в кінотеатр",
     "Ми йдемо в кіно",
     "«кіно» стоит первым в переводе, и так во всех остальных языках"),
    (3, "example_uk",
     "Увечері я вчу німецьку",
     "Вечорами я вчу німецьку",
     "«abends» это по вечерам, повторяющееся; «увечері» — один вечер"),
    (6538, "example_uk",
     "Будильник дзвонить щодня о шостій",
     "Будильник дзвонить щоранку о шостій",
     "«jeden Morgen» это каждое утро, а не каждый день"),
    (13455, "example_uk",
     "У нас однаковий смак",
     "У нас той самий смак",
     "«однаковий» нет в списке переводов, карточка показывала «той самий»"),
    (6527, "example_uk",
     "Я зовсім втомився",
     "Я цілком втомився",
     "«зовсім» нет в списке переводов, а «цілком» есть"),
    (61, "example_uk",
     "Ця заява незрозуміла",
     "Це висловлювання незрозуміле",
     "остальные четыре языка взяли первый вариант «висловлювання»"),
    (6532, "example_uk",
     "Магазин відкритий",
     "Магазин відчинений",
     "про магазин по-украински «відчинений»; ряд-близнец geschlossen так и написан"),
    (6542, "example_en",
     "He may be late",
     "He will possibly be late",
     "«may» короче четырёх букв, и карточка показывала «possibly» вместо него"),
    (280, "example_en",
     "The form is correct",
     "The shape looks right",
     "потеряно «sieht aus», и «shape» стоит первым в переводе"),

    # ── потерянное слово ─────────────────────────────────────────
    (280, "example_tr",
     "Form doğru",
     "Form doğru görünüyor",
     "потеряно «sieht aus»: в ru, uk и pl оно есть"),
    (743, "example_uk",
     "Хто зможе це вгадати?",
     "Хто зможе це правильно вгадати?",
     "потеряно «richtig»: в ru и pl оно есть"),
    (743, "example_en",
     "Who can guess this?",
     "Who can guess this correctly?",
     "то же"),
    (743, "example_tr",
     "Kim bunu tahmin edebilir?",
     "Kim bunu doğru tahmin edebilir?",
     "то же"),
    (721, "example_uk",
     "Я йду на пошту",
     "Мені потрібно піти на пошту",
     "потеряно «muss»: в ru и pl оно есть"),
    (721, "example_en",
     "I go to the post office",
     "I have to go to the post office",
     "то же"),
    (6550, "example_uk",
     "Дах дірявий і дощ протікає",
     "Дах дірявий, і дощ протікає всередину",
     "потеряно «rein», и перед «і» между частями нужна запятая"),

    # ── добавленное слово ────────────────────────────────────────
    (2808, "example_tr",
     "Bu çok doğal",
     "Bu zaten doğal",
     "«çok» в эталоне нет, зато есть частица «ja» — это «zaten»"),
    (8762, "example_pl",
     "Nasz projekt jest już prawie gotowy",
     "Nasz projekt jest prawie gotowy",
     "«już» в эталоне нет: «Unser Projekt ist fast fertig»"),

    # ── форма и время глагола ────────────────────────────────────
    (10188, "example_uk",
     "Зрадник був арештований",
     "Зрадника арештували",
     "«був + дієприкметник» калька; по-украински личная форма"),
    (6518, "example_uk",
     "Я буду супроводжувати тебе до лікаря",
     "Я супроводжую тебе до лікаря",
     "будущее против «Ich begleite»; в ru, tr и pl настоящее"),
    (2905, "example_pl",
     "Przekonam cię",
     "Przekonuję cię",
     "будущее против «Ich überzeuge»; в ru, uk и tr настоящее"),
    (1395, "example_tr",
     "Burada sigara içmek yasak",
     "Burada sigara içmeye izin verilmiyor",
     "ряд про erlauben, а турецкий писал «запрещено» — это слово ряда verboten"),

    # ── род, расходящийся с рядом-близнецом ──────────────────────
    (781, "example_ru",
     "В субботу я свободна",
     "В субботу я свободен",
     "ряд-близнец Freitag с тем же эталоном написан в мужском роде"),
    (781, "example_uk",
     "У суботу я вільна",
     "У суботу я вільний",
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
