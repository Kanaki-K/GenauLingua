"""ВТОРОЙ ПРОХОД, блок 9 (ряды 1601–1800): правки, найденные глазами.

Правок меньше, чем в предыдущих блоках, и причина не в усталости: здесь
ранги 2600–3000, то есть конкретные существительные — `Ratte`, `Suppe`,
`Sand`, `Planet`, `Zigarette`. У них один перевод и одно значение,
расходиться почти негде. Плотность дефектов зависит от состава, а не
только от качества чтения: служебные слова первых блоков давали по 26
правок на блок, конкретные вещи дают 16.

Самое важное:

    Bulle (15984)  tr «Polis hırsızı tutuklaYIYOR»
        Формы «-layıyor» в турецком нет: у глаголов на `-lamak` в
        настоящем времени гласная основы меняется — tutukla → tutukluyor,
        başla → başlıyor. Это ОПЕЧАТКА В ФОРМЕ, а не выбор слова.
        Проверено по всей базе на этот вид: ровно одна. Не класс.

    Bulle (15984)  регистр
        `Bulle` — немецкое пренебрежительное о полицейском (как «мент»).
        Английский и польский так и переводят — `cop`, `glina`, — а
        русский, украинский и турецкий писали нейтральное «полицейский»,
        хотя в их списках переводов «мент» и «aynasız» стоят ПЕРВЫМИ.
        То есть карточка показывала одно слово, а пример говорил другое,
        и заодно терялся весь смысл ряда: нейтральное слово в базе уже
        есть отдельным рядом (`Polizist`).

    bewahren (1272)  ru «сохранять ХОЛОДНУЮ ГОЛОВУ»
        Калька с немецкого «einen kühlen Kopf bewahren». По-русски
        говорят «сохранять хладнокровие», по-украински —
        «холоднокровність». Польский и турецкий идиому взяли верно
        («zimna krew», «soğukkanlılık»).

    Verfügung (15993)  ru/uk/tr на «вы», pl на «ты»
        Эталон «Ich stehe zur Verfügung» вообще без обращения, и каждый
        язык выбрал сам. По правилу базы (эталон на «du») верен
        польский. Это ТРЕТЬЯ форма класса «обращение»: не «немецкое du
        против вежливого перевода» и не повелительное, а полное
        отсутствие адресата в эталоне. Формального признака у неё нет —
        сравнивать не с чем, — поэтому приметой она не берётся и
        записана в HANDOVER.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── опечатка в форме глагола ─────────────────────────────────
    (15984, "example_tr",
     "Polis hırsızı tutuklayıyor",
     "Aynasız hırsızı tutukluyor",
     "«tutuklayıyor» не форма турецкого: tutukla → tutukluyor; и «aynasız» стоит первым"),

    # ── регистр: пренебрежительное против нейтрального ───────────
    (15984, "example_ru",
     "Полицейский арестует вора",
     "Мент арестует вора",
     "«Bulle» пренебрежительное, «мент» стоит первым; нейтральное слово — отдельный ряд Polizist"),
    (15984, "example_uk",
     "Поліцейський арештовує злодія",
     "Мент арештовує злодія",
     "то же"),

    # ── калька идиомы ────────────────────────────────────────────
    (1272, "example_ru",
     "Мы должны сохранять холодную голову",
     "Мы должны сохранять хладнокровие",
     "«холодную голову» калька; по-русски «хладнокровие», как pl «zimna krew»"),
    (1272, "example_uk",
     "Ми повинні зберігати холодну голову",
     "Ми повинні зберігати холоднокровність",
     "то же по-украински"),

    # ── обращение: эталон без адресата, база на «ты» ─────────────
    (15993, "example_ru",
     "Я в вашем распоряжении",
     "Я в твоём распоряжении",
     "по правилу базы эталон на «du»; польский так и написан"),
    (15993, "example_uk",
     "Я у вашому розпорядженні",
     "Я у твоєму розпорядженні",
     "то же"),
    (15993, "example_tr",
     "Emrinizdeyim",
     "Emrindeyim",
     "то же"),

    # ── подменённое слово ───────────────────────────────────────
    (1008, "example_pl",
     "Piorę ubrania",
     "Piorę bieliznę",
     "«ubrania» это одежда, а «Wäsche» — бельё, как в ru, uk, tr и en"),
    (965, "example_ru",
     "Занятие начинается в девять часов",
     "Урок начинается в девять часов",
     "«урок» стоит первым, и так в uk, pl, tr и en"),
    (183, "example_ru",
     "Во вторник у меня занятия",
     "Во вторник у меня курс",
     "эталон «einen Kurs»; в остальных четырёх курс"),
    (584, "example_uk",
     "Я зазвичай їм удома",
     "Я найчастіше їм удома",
     "«найчастіше» стоит первым, и так в ru, pl, tr и en"),

    # ── потерянное и добавленное слово ──────────────────────────
    (1080, "example_en",
     "How much sugar would you like?",
     "How much sugar would you like in your coffee?",
     "потеряно «in deinen Kaffee»: в остальных четырёх оно есть"),
    (10221, "example_tr",
     "Bu gerçekten akıllı bir fikirdi",
     "Bu senin akıllı bir fikrindi",
     "потеряно «von dir», и «gerçekten» в эталоне нет"),
    (8776, "example_uk",
     "Де ж молоток?",
     "Де молоток?",
     "частицы «ж» в эталоне нет: «Wo ist der Hammer?»"),
    (10227, "example_uk",
     "Настрій тут просто чудовий",
     "Настрій тут чудовий",
     "«просто» в эталоне нет: «Die Stimmung hier ist super»"),

    # ── время глагола ───────────────────────────────────────────
    (12507, "example_pl",
     "Karetka przyjedzie szybko",
     "Karetka przyjeżdża szybko",
     "будущее против «kommt schnell»; в остальных четырёх настоящее"),
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
