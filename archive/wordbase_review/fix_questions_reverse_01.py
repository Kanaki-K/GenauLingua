"""
Обратный случай: в переводе вопрос, а в немецком утверждение.

Второй список сторожа `scan_question_mark`. Здесь дефект наоборот, и он
важнее, чем кажется: перевод не просто поставил лишний знак, он **задаёт
вопрос там, где немецкий утверждает**. «Ich benutze das Telefon» — «Можна
користуватися твоїм ноутбуком?». Общего у этих фраз только слово.

Три вида, и правятся они по-разному:

1. **Немецкий сам вопрос, но без знака** — мой шаблон их не поймал, потому
   что они без вопросительного слова в начале: «Waren alle Studenten bei der
   Vorlesung anwesend», «Können wir die letzte Aktion rückgängig machen»,
   «In welchem Alter». Правится эталон.
2. **Перевод потерял вторую половину** немецкой фразы, и остался только
   вопрос: «Wo ist der Feuerlöscher? Ich kann ihn nicht finden» — «Де
   вогнегасник?». Дописывается потерянное.
3. **Перевод о другом** — самый частый. Правится перевод.

Попутно две ошибки в немецком: «im Spielplatz» вместо «auf dem Spielplatz»
и «Nähterin» вместо «Näherin».

    python -m app.scripts.fix_questions_reverse_01            # показать
    python -m app.scripts.fix_questions_reverse_01 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- немецкий сам вопрос, но без знака ------------------------------------
    (669, "example_de", "Kaffee oder Tee", "Kaffee oder Tee?",
     "это вопрос, знак потерян"),
    (669, "example_en", "Coffee or tea", "Coffee or tea?",
     "вслед за немецким: это вопрос"),
    (669, "example_uk", "Кава або чай", "Кава або чай?",
     "вслед за немецким: это вопрос"),
    (669, "example_tr", "Kahve veya çay", "Kahve veya çay?",
     "вслед за немецким: это вопрос"),
    (669, "example_pl", "Kawa albo herbata", "Kawa albo herbata?",
     "вслед за немецким: это вопрос"),
    (2165, "example_de", "In welchem Alter", "In welchem Alter?",
     "это вопрос, знак потерян"),
    (6934, "example_de", "Waren alle Studenten bei der Vorlesung anwesend",
     "Waren alle Studenten bei der Vorlesung anwesend?",
     "это вопрос, знак потерян"),
    (7078, "example_de", "Können wir die letzte Aktion rückgängig machen",
     "Können wir die letzte Aktion rückgängig machen?",
     "это вопрос, знак потерян"),

    # --- ошибки в немецком эталоне -------------------------------------------
    (9238, "example_de", "Die Mutter beaufsichtigt die Kinder im Spielplatz",
     "Die Mutter beaufsichtigt die Kinder auf dem Spielplatz",
     "«im Spielplatz» — нужен предлог auf с дательным"),
    (12416, "example_de",
     "Die Nähterin steppte den Saum mit Nadel und Faden",
     "Die Näherin steppte den Saum mit Nadel und Faden",
     "«Nähterin» — лишняя «t», правильно «Näherin»"),

    # --- перевод потерял вторую половину фразы --------------------------------
    (1419, "example_en", "Where is the fire extinguisher?",
     "Where is the fire extinguisher? I can't find it",
     "потеряна вторая половина немецкой фразы"),
    (1419, "example_uk", "Де вогнегасник?",
     "Де вогнегасник? Я не можу його знайти",
     "потеряна вторая половина немецкой фразы"),
    (8210, "example_pl", "Czy możemy skrócić to spotkanie?",
     "Czy możemy skrócić to spotkanie? Mam potem jeszcze jedno",
     "потеряна вторая половина немецкой фразы"),
    (7971, "example_ru", "Можешь опустить жалюзи, слишком светло?",
     "Можешь опустить жалюзи? Слишком светло",
     "вопрос склеен с утверждением запятой, как было и в немецком"),

    # --- перевод спрашивает там, где немецкий утверждает ----------------------
    (93, "example_uk", "Можна користуватися твоїм ноутбуком?",
     "Я користуюся телефоном",
     "в немецком утверждение про телефон, а не вопрос про ноутбук"),
    (200, "example_en", "Am I allowed to sit here?",
     "We are allowed to stay longer today",
     "в немецком утверждение «нам можно остаться дольше»"),
    (200, "example_uk", "Чи дозволено мені тут сісти?",
     "Нам дозволено сьогодні залишитися довше",
     "в немецком утверждение «нам можно остаться дольше»"),
    (501, "example_en", "Stay in contact with me, okay?",
     "Please get in touch",
     "в немецком просьба связаться, а не «оставайся на связи»"),
    (790, "example_tr", "Bana fotoğrafları yollar mısın?",
     "Fotoğrafı sana gönderiyorum",
     "в немецком «я посылаю тебе фото», а не просьба"),
    (859, "example_tr", "Bu lokantanın spesiyalitesi ne?",
     "Bu, evin spesiyalitesi",
     "в немецком утверждение, а не вопрос"),
    (911, "example_tr", "Günün menüsünü alalım mı?",
     "Metro için günlük bilet alıyorum",
     "«меню дня» вместо дневного билета на метро"),
    (923, "example_tr", "Tenis oynamaya varmısın?",
     "Hadi tenis oynayalım",
     "в немецком «давай играть», а не вопрос; и «varmısın» без пробела"),
    (935, "example_tr", "Bir dilim pasta ister misin?",
     "Doğum günü için severek pasta yaparım",
     "в немецком «на день рождения я охотно печу торт»"),
    (1816, "example_en", "May I ask a follow-up question?",
     "If you have any questions, please call",
     "в немецком просьба звонить при вопросах"),
    (1846, "example_uk", "Який тип школи ти обрав?",
     "Існують різні типи шкіл",
     "в немецком утверждение, а не вопрос"),
    (2092, "example_tr", "Bizim kedi dişi mi, erkek mi?",
     "Bebek kız",
     "в немецком про ребёнка, а не про кошку"),
    (2132, "example_en", "Can I just watch for now?",
     "I am watching the game",
     "в немецком утверждение «я смотрю игру»"),
    (2385, "example_tr", "Televizyonu açar mısın?", "Televizyonu aç",
     "в немецком повеление, а не вопрос"),
    (2492, "example_uk", "Хто буде вести машину?", "Я веду розмову",
     "в немецком «я веду разговор», а не вопрос про машину"),
    (2845, "example_uk", "Що тут відбувається?",
     "Концерт відбудеться у п'ятницю",
     "в немецком про концерт в пятницу"),
    (6481, "example_en", "What kind of creature is that?",
     "She is a kind creature", "в немецком утверждение, а не вопрос"),
    (6783, "example_en", "What do you plan for today?",
     "He must be planning something big",
     "в немецком про него и «что-то большое»"),
    (6783, "example_uk", "Що ти плануєш на сьогодні?",
     "Він, мабуть, планує щось велике",
     "в немецком про него и «что-то большое»"),
    (7118, "example_tr", "Odanın genişliğini ölçtün mü?",
     "Denizin genişliğine baktı",
     "в немецком он смотрел на морскую даль"),
    (7147, "example_tr", "Akşam barda buluşalım mı?",
     "Jimnastikçi barfikste hareketler yapıyor",
     "спутаны омонимы: Stange — снаряд, а не бар"),
    (7628, "example_en", "How do you assess this situation?",
     "I take that as a good sign",
     "в немецком утверждение, а не вопрос"),
    (7664, "example_uk", "Можеш стерти це з дошки?",
     "Не затирай своїх слідів",
     "в немецком повеление про следы, а не вопрос про доску"),
    (7675, "example_tr", "Gazı azalt ve daha yavaş gidebilir misin?",
     "Lastikten hava indirmemiz gerek",
     "в немецком про спуск воздуха из шины"),
    (7775, "example_pl", "Czy ta wizyta jest naprawdę konieczna?",
     "To są dokumenty niezbędne do rejestracji",
     "в немецком про необходимые документы"),
    (8132, "example_en", "Can you squeeze the lemon?",
     "I squashed my finger",
     "в немецком «я прищемил палец», а не вопрос про лимон"),
    (8388, "example_en", "What happened to your phone?",
     "I made a stupid mistake",
     "в немецком «я допустил глупую ошибку»"),
    (8393, "example_tr", "Okulda üniforma zorunlu mu?",
     "Bu kesinlikle zorunlu değil",
     "в немецком утверждение «это не обязательно»"),
    (8593, "example_uk", "Можеш приблизно підрахувати вартість ремонту?",
     "Дай я швидко приблизно підрахую витрати",
     "в немецком «дай я прикину расходы», а не вопрос"),
    (8683, "example_en", "Can you straighten up that picture?",
     "He straightened the fallen tree again",
     "в немецком про упавшее дерево, а не про картину"),
    (9238, "example_en", "Who will supervise the children today?",
     "The mother supervises the children at the playground",
     "в немецком утверждение про мать на площадке"),
    (10109, "example_uk", "Чому ти такий стурбований?",
     "Я турбуюся за тебе",
     "в немецком «я беспокоюсь о тебе», а не вопрос"),
    (10783, "example_tr", "Böyle bir ayaktakımıyla ne işin var?",
     "Bu gerçekten alçak bir ayaktakımı",
     "в немецком утверждение, а не вопрос"),
    (11590, "example_tr", "Bunu söylemeye nasıl cüret edersin?",
     "Onun cesareti takdire değerdi",
     "в немецком «его смелость была достойна восхищения»"),
    (12304, "example_pl", "Znasz jakąś ciekawą grę karcianą?",
     "Po obiedzie gramy w karty",
     "в немецком «после еды мы играем в карты»"),
    (12416, "example_en", "Can you stitch this button back on?",
     "The seamstress stitched the hem with needle and thread",
     "в немецком про швею и подол, а не вопрос про пуговицу"),
    (12506, "example_tr", "Neden böyle surat asıyorsun?", "Çeneni kapa",
     "в немецком грубое «замолчи», а не вопрос про хмурый вид"),
    (12517, "example_tr", "Mumları yakar mısın?",
     "Dikkat et, kendini yakabilirsin",
     "в немецком предупреждение «обожжёшься», а не вопрос про свечи"),
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
