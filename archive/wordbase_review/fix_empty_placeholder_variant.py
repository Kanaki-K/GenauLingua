"""СКВОЗНОЙ КЛАСС: вариант списка, добавляющий только пустое местоимение.

Найдено вычиткой блока 50:

    gegenüberstehen (8268) ru «стоять перед, СТОЯТЬ ПЕРЕД ЧЕМ-ЛИБО,
                               сталкиваться с чем-либо, стоять напротив,
                               относиться к чему-либо определённым образом»

Второй вариант — первый плюс «чем-либо». Для карточки это не второе
значение, а то же самое, занимающее строку. То же в uk и pl того же ряда.

ПЕРВЫЙ ЗАМЕР БЫЛ СЛИШКОМ ШИРОКИМ, И ЭТО ВАЖНО ЗАПИСАТЬ. Я начал с
очевидного признака «один вариант — начало другого»:

    всего попаданий: 1630

Тысяча шестьсот тридцать. И почти все законные:

    Arm        (45) ru «рука, РУКА ОТ ПЛЕЧА ДО КИСТИ, подлокотник»
    bezahlen  (111) en «to pay, TO PAY FOR»
    anfangen   (22) pl «zaczynać, ZACZYNAĆ SIĘ, rozpoczynać»

Удлинение здесь НЕСЁТ СМЫСЛ: уточняет значение, меняет управление,
различает возвратность. Это стиль базы, а не дефект, и примета в таком
виде мерила язык, а не базу — ровно та ошибка, от которой предостерегает
правило в HANDOVER.

СУЖЕНИЕ ДО НАСТОЯЩЕГО ПРИЗНАКА: хвост должен быть ОДНИМ НЕОПРЕДЕЛЁННЫМ
МЕСТОИМЕНИЕМ и ничем больше — «что-то», «кого-то», «czymś», «kogoś»,
«something», «someone», «щось», «когось». Такой хвост не уточняет
значение, он только показывает, что у глагола есть дополнение, — а это
видно и так.

    с пустым хвостом-местоимением: 25 ячеек в 19 рядах

ДВА РЯДА ОСТАВЛЕНЫ, И ПРОВЕРКА ИХ ВЫЯВИЛА:

    rollen (6713) en «to roll, TO ROLL SOMETHING, to wheel»

Здесь «something» — не пустышка, а метка ПЕРЕХОДНОСТИ, и русский список
того же ряда её подтверждает: «катиться, катить» — непереходный и
переходный. Убрать значило бы потерять различение.

    borgen (9815) pl «pożyczyć, POŻYCZYĆ KOMUŚ, pożyczyć od kogoś»

«komuś» (дать) против «od kogoś» (взять) — это lend против borrow, и
английский список ряда («to lend, to borrow») это прямо подтверждает.

ОСТАЛЬНЫЕ 23 ЯЧЕЙКИ В 17 РЯДАХ — чистые повторы, и удаляется ДЛИННЫЙ
вариант, не короткий. Так безопаснее для вида карточки: длинный вариант
начинается с короткого, поэтому любой пример, который матчился на
длинный, матчится и на короткий, и показываемое значение не меняется.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

# (id, колонка, было, стало, что убрано)
FIXES: list[tuple[int, str, str, str, str]] = [
    (1000, "translation_ru",
     "представлять, представлять кого-то, представляться, представлять себе, воображать",
     "представлять, представляться, представлять себе, воображать",
     "«представлять кого-то»"),
    (2010, "translation_en",
     "to do, to do something, to undertake, to take action",
     "to do, to undertake, to take action",
     "«to do something»"),
    (2010, "translation_ru",
     "делать, делать что-то, предпринимать, затевать",
     "делать, предпринимать, затевать",
     "«делать что-то»"),
    (2010, "translation_uk",
     "робити, робити щось, вживати заходів, затівати",
     "робити, вживати заходів, затівати",
     "«робити щось»"),
    (2338, "translation_ru",
     "демонстрация, митинг, показ, демонстрация чего-либо",
     "демонстрация, митинг, показ",
     "«демонстрация чего-либо» — сенс «показ» уже стоит третьим"),
    (2953, "translation_en",
     "to miss, to miss someone, to lack, to find missing",
     "to miss, to lack, to find missing",
     "«to miss someone»"),
    (6812, "translation_ru",
     "заменять, заменять кого-то, представлять, отстаивать мнение",
     "заменять, представлять, отстаивать мнение",
     "«заменять кого-то»"),
    (6812, "translation_uk",
     "заміняти, заміняти когось, представляти, відстоювати думку",
     "заміняти, представляти, відстоювати думку",
     "«заміняти когось»"),
    (7102, "translation_en",
     "to be due to, to be due to someone, to be owed to, to come towards, to approach",
     "to be due to, to be owed to, to come towards, to approach",
     "«to be due to someone»"),
    (7365, "translation_ru",
     "располагать, располагать чем-то, иметь в распоряжении, распоряжаться, предписывать",
     "располагать, иметь в распоряжении, распоряжаться, предписывать",
     "«располагать чем-то» — «иметь в распоряжении» уточняет то же"),
    (8268, "translation_ru",
     "стоять перед, стоять перед чем-либо, сталкиваться с чем-либо, стоять напротив, "
     "относиться к чему-либо определённым образом",
     "стоять перед, сталкиваться с чем-либо, стоять напротив, "
     "относиться к чему-либо определённым образом",
     "«стоять перед чем-либо» — на этом ряде класс и найден"),
    (8268, "translation_uk",
     "стояти перед, стояти перед чимось, стикатися з чимось, стояти навпроти, "
     "ставитися до чогось",
     "стояти перед, стикатися з чимось, стояти навпроти, ставитися до чогось",
     "«стояти перед чимось»"),
    (8268, "translation_pl",
     "stać przed, stać przed czymś, stać naprzeciwko, mierzyć się z czymś, "
     "odnosić się do czegoś",
     "stać przed, stać naprzeciwko, mierzyć się z czymś, odnosić się do czegoś",
     "«stać przed czymś»"),
    (8765, "translation_en",
     "to serve, to be used as, to serve someone",
     "to serve, to be used as",
     "«to serve someone»"),
    (9227, "translation_en",
     "to suspend, to suspend someone, to put on hold",
     "to suspend, to put on hold",
     "«to suspend someone» — «to put on hold» уже различает предмет"),
    (9888, "translation_en",
     "to vouch for, to vouch for someone, to stand surety, to guarantee",
     "to vouch for, to stand surety, to guarantee",
     "«to vouch for someone»"),
    (13979, "translation_en",
     "to lie to, to lie to someone, to deceive",
     "to lie to, to deceive",
     "«to lie to someone»; «to pay, to pay for» (111) — тот же стиль базы"),
    (14010, "translation_en",
     "to lie to, to lie to someone, to deceive",
     "to lie to, to deceive",
     "«to lie to someone»"),
    (14046, "translation_en",
     "to approach, to approach someone, to speak to someone, to bring up a topic, "
     "to appeal to someone",
     "to approach, to speak to someone, to bring up a topic, to appeal to someone",
     "«to approach someone»"),
    (14046, "translation_pl",
     "zagadnąć, zagadnąć kogoś, odezwać się do kogoś, poruszyć temat, podobać się",
     "zagadnąć, odezwać się do kogoś, poruszyć temat, podobać się",
     "«zagadnąć kogoś»"),
    (14291, "translation_pl",
     "spławić, spławić kogoś, odprawić, pozbyć się kogoś",
     "spławić, odprawić, pozbyć się kogoś",
     "«spławić kogoś»"),
    (16445, "translation_uk",
     "обкрадати, обкрадати когось, красти в когось",
     "обкрадати, красти в когось",
     "«обкрадати когось»"),
    (16748, "translation_en",
     "to rob, to rob someone, to steal from someone",
     "to rob, to steal from someone",
     "«to rob someone»"),
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
            print(f"id={wid} {col}  убрано {why}")
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
