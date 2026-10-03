"""
Дошли следом: знак дописан немецкому — тот же знак нужен его переводам.

Когда в предыдущих двух партиях восемнадцати немецким примерам вернули
вопросительный знак, их переводы тут же попали в первый список сторожа: в
эталоне вопрос, а у них знака нет. Это не новая находка, а хвост
предыдущей правки, и его надо подобрать, иначе сторож будет показывать его
вечно.

Попутно поправлено то, что видно рядом:

* `anwesend` — турецкое «hazır» значит «готов», а не «присутствовал»;
  украинский перевод говорит про собрание, хотя немецкий про лекцию, и
  теряет студентов.
* `durchstellen` — немецкий просит соединить с секретарём, польский и
  турецкий с директором.
* `wem` — польский «Komu dałeś moje klucze» про ключи, а немецкий «с кем
  ты идёшь».
* `Alter` — украинский «Вік для кохання не має значення» не имеет с
  немецким вопросом ничего общего.
* `Lautstärke` — турецкое «ses şiddeti» это физический термин,
  а «sessiz yapmak» так не говорят.

    python -m app.scripts.fix_questions_cascade            # показать
    python -m app.scripts.fix_questions_cascade --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- потерян только знак ---------------------------------------------------
    (2165, "example_en", "At what age", "At what age?", "потерян только знак"),
    (2165, "example_ru", "В каком возрасте", "В каком возрасте?",
     "потерян только знак"),
    (2165, "example_tr", "Hangi yaşta", "Hangi yaşta?",
     "потерян только знак"),
    (6934, "example_en", "Were all the students present at the lecture",
     "Were all the students present at the lecture?",
     "потерян только знак"),
    (13377, "example_tr", "Kiminle gidiyorsun", "Kiminle gidiyorsun?",
     "потерян только знак"),
    (13435, "example_pl", "To jest dobre, no nie", "To jest dobre, no nie?",
     "потерян только знак"),
    (13435, "example_tr", "Bu iyi, değil mi", "Bu iyi, değil mi?",
     "потерян только знак"),
    (13435, "example_uk", "Це добре, так", "Це добре, так?",
     "потерян только знак"),
    (13440, "example_en", "What can I help you with",
     "What can I help you with?", "потерян только знак"),
    (13440, "example_pl", "Czym mogę ci pomóc", "Czym mogę ci pomóc?",
     "потерян только знак"),
    (13440, "example_tr", "Sana neyle yardım edebilirim",
     "Sana neyle yardım edebilirim?", "потерян только знак"),
    (13440, "example_uk", "Чим я можу тобі допомогти",
     "Чим я можу тобі допомогти?", "потерян только знак"),
    (13443, "example_en", "What are you thinking about",
     "What are you thinking about?", "потерян только знак"),
    (13443, "example_pl", "O czym myślisz", "O czym myślisz?",
     "потерян только знак"),
    (13443, "example_tr", "Ne hakkında düşünüyorsun",
     "Ne hakkında düşünüyorsun?", "потерян только знак"),
    (13443, "example_uk", "Про що ти думаєш", "Про що ти думаєш?",
     "потерян только знак"),
    (13523, "example_tr", "Sorun ne yüzden ortaya çıktı",
     "Sorun ne yüzden ortaya çıktı?", "потерян только знак"),
    (13523, "example_uk", "Через що виникла проблема",
     "Через що виникла проблема?", "потерян только знак"),
    (13829, "example_pl", "Eee, jak ty się nazywasz",
     "Eee, jak ty się nazywasz?", "потерян только знак"),
    (14207, "example_pl", "Cześć, jak leci", "Cześć, jak leci?",
     "потерян только знак"),
    (17683, "example_en",
     "The volume is too high, can you turn it down",
     "The volume is too high, can you turn it down?",
     "потерян только знак"),
    (17683, "example_ru",
     "Громкость слишком высокая, можешь сделать тише",
     "Громкость слишком высокая, можешь сделать тише?",
     "потерян только знак"),
    (17683, "example_uk",
     "Гучність занадто висока, можеш зробити тихіше",
     "Гучність занадто висока, можеш зробити тихіше?",
     "потерян только знак"),

    # --- форма глагола и слово не то, плюс знак --------------------------------
    (7078, "example_tr", "Son işlemi geri alabiliriz mi",
     "Son işlemi geri alabilir miyiz?",
     "частица стоит после лица: нужно «alabilir miyiz»"),
    (7078, "example_uk", "Можемо ми скасувати останню дію",
     "Чи можемо ми скасувати останню дію?",
     "порядок слов и потерянный знак"),
    (6934, "example_tr", "Tüm öğrenciler derste hazır mıydı",
     "Tüm öğrenciler derste miydi?",
     "«hazır» — готов, а anwesend — присутствовал"),
    (14069, "example_tr", "Bunların hepsi boş konuşma",
     "Bunların hepsi boş konuşma, değil mi?",
     "потерян оборот «nicht wahr»"),
    (14069, "example_uk", "Це вся балаканина, чи не так",
     "Це все балаканина, чи не так?",
     "«вся балаканина» — неверный род; и потерян знак"),
    (17683, "example_tr",
     "Ses şiddeti çok yüksek, sessiz yapabilir misin",
     "Ses çok yüksek, kısabilir misin?",
     "«ses şiddeti» — физический термин, «sessiz yapmak» так не говорят"),

    # --- перевод переводит другое предложение ---------------------------------
    (2165, "example_uk", "Вік для кохання не має значення",
     "У якому віці?", "пример про другое"),
    (6934, "example_uk", "Усі були присутні на зборах",
     "Чи всі студенти були присутні на лекції?",
     "в немецком студенты на лекции, а не все на собрании"),
    (13377, "example_pl", "Komu dałeś moje klucze", "Z kim idziesz?",
     "пример про ключи, а немецкий «с кем ты идёшь»"),
    (14207, "example_en", "Hi, nice to see you again!",
     "Hi, how are you doing?",
     "в немецком вопрос «как дела», а не «рад снова видеть»"),
    (14283, "example_pl", "Proszę mnie połączyć z dyrektorem",
     "Czy może mnie pan połączyć z sekretarką?",
     "в немецком секретарь, а не директор, и это вопрос"),
    (14283, "example_tr", "Lütfen beni müdüre bağlayın",
     "Lütfen beni sekretere bağlar mısınız?",
     "в немецком секретарь, а не директор, и это вопрос"),
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
