"""
Обратный случай, партия 2 — остаток списка.

Десять немецких примеров здесь — настоящие вопросы без знака, которых не
нашёл мой шаблон: он смотрит на вопросительное слово в начале, а эти
начинаются иначе или спрашивают частицей в конце: «Das ist gut, ne», «Das
ist alles Geschwätz, nicht wahr», «Moin, wie gehts dir denn».

Остальное — переводы, спрашивающие там, где немецкий утверждает. Самый
показательный ряд `anhalten`: немецкий «Der Bus hält an der Kirche an», а
все четыре перевода просят водителя остановиться здесь. Четыре языка ушли в
одну сторону, и ни один не о том, что в эталоне.

    python -m app.scripts.fix_questions_reverse_02            # показать
    python -m app.scripts.fix_questions_reverse_02 --apply    # применить
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
    (13377, "example_de", "Mit wem gehst du", "Mit wem gehst du?",
     "это вопрос, знак потерян"),
    (13435, "example_de", "Das ist gut, ne", "Das ist gut, ne?",
     "вопрос частицей в конце, знак потерян"),
    (13440, "example_de", "Womit kann ich dir helfen",
     "Womit kann ich dir helfen?", "это вопрос, знак потерян"),
    (13443, "example_de", "Woran denkst du", "Woran denkst du?",
     "это вопрос, знак потерян"),
    (13523, "example_de", "Wodurch entstand das Problem",
     "Wodurch entstand das Problem?", "это вопрос, знак потерян"),
    (13829, "example_de", "Äh, wie heißt du nochmal",
     "Äh, wie heißt du nochmal?", "это вопрос, знак потерян"),
    (14069, "example_de", "Das ist alles Geschwätz, nicht wahr",
     "Das ist alles Geschwätz, nicht wahr?",
     "вопрос оборотом в конце, знак потерян"),
    (14207, "example_de", "Moin, wie gehts dir denn",
     "Moin, wie geht's dir denn?",
     "пропущен апостроф, и это вопрос без знака"),
    (14283, "example_de",
     "Können Sie mich bitte zur Sekretärin durchstellen",
     "Können Sie mich bitte zur Sekretärin durchstellen?",
     "это вопрос, знак потерян"),
    (17683, "example_de",
     "Die Lautstärke ist zu hoch, kannst du sie runterdrehen",
     "Die Lautstärke ist zu hoch, kannst du sie runterdrehen?",
     "вторая половина — вопрос, знак потерян"),

    # --- перевод потерял вторую половину фразы --------------------------------
    (14165, "example_pl", "Możesz mi wyjaśnić to zadanie?",
     "Możesz mi wyjaśnić to zadanie? Nie rozumiem tego",
     "потеряна вторая половина немецкой фразы"),

    # --- перевод спрашивает там, где немецкий утверждает ----------------------
    (12833, "example_tr", "Sütü sindirebiliyor musun?",
     "Midem bu ağır yemeği sindiremiyor",
     "в немецком про свой желудок и тяжёлую еду, а не вопрос про молоко"),
    (13377, "example_en", "Whom did you invite tonight?",
     "Who are you going with?",
     "в немецком «с кем ты идёшь», а не «кого ты пригласил»"),
    (13377, "example_uk", "Кому ти дзвониш так пізно?", "З ким ти йдеш?",
     "в немецком «с кем ты идёшь», а не вопрос про звонок"),
    (13432, "example_tr", "Bu çanta kimin?",
     "Arabası kırmızı olan adam",
     "в немецком утверждение-оборот, а не вопрос про сумку"),
    (13432, "example_uk", "Чий це рюкзак на столі?",
     "Чоловік, чия машина червона",
     "в немецком утверждение-оборот, а не вопрос про рюкзак"),
    (13524, "example_tr", "Para neyin içinde saklı?",
     "Farkın nerede olduğunu bilmiyorum",
     "в немецком «не знаю, в чём разница», а не вопрос про деньги"),
    (14139, "example_tr", "Bugünün anahtar kelimesi ne?",
     "Bugünün anahtar kelimesi iletişim",
     "в немецком утверждение: ключевое слово — коммуникация"),
    (14154, "example_uk", "Можна тебе дещо запитати?",
     "Я ще перепитаю",
     "в немецком «я ещё переспрошу», а не вопрос"),
    (14219, "example_tr", "Mektubu bana yüksek sesle okur musun?",
     "Hâkim kararı okuyor",
     "в немецком судья оглашает приговор, а не просьба про письмо"),
    (14375, "example_en", "Can you play that song again?",
     "I like that song very much",
     "в немецком утверждение «песня мне очень нравится»"),
    (16173, "example_tr", "Seçimde kime oy verdin?",
     "Oylamada çoğunluk teklife karşı çıktı",
     "в немецком про итог голосования, а не вопрос"),
    (16928, "example_uk", "Як ти міг так вчинити зі мною?",
     "Терорист вчинив замах на будівлю",
     "в немецком про теракт, а не упрёк"),
    (17069, "example_en", "Can you please stop here?",
     "The bus stops at the church",
     "в немецком автобус останавливается у церкви, а не просьба"),
    (17069, "example_ru", "Можешь, пожалуйста, здесь остановить?",
     "Автобус останавливается у церкви",
     "в немецком автобус останавливается у церкви, а не просьба"),
    (17069, "example_tr", "Lütfen burada durabilir misin?",
     "Otobüs kilisenin orada duruyor",
     "в немецком автобус останавливается у церкви, а не просьба"),
    (17069, "example_uk", "Чи можеш, будь ласка, тут зупинити?",
     "Автобус зупиняється біля церкви",
     "в немецком автобус останавливается у церкви, а не просьба"),
    (17432, "example_en", "Which travel option is the cheapest?",
     "There are many travel options to Berlin",
     "в немецком утверждение, а не вопрос"),
    (17489, "example_ru", "Кто будет ремонтировать стиральную машину?",
     "Он ремонтирует машину",
     "в немецком «он ремонтирует машину», а не вопрос"),
    (18057, "example_tr", "Bu ampul kaç watt?",
     "Bu ampul 60 watt harcıyor",
     "в немецком утверждение про 60 ватт, а не вопрос"),
    (18590, "example_uk", "Ти уже прийшов додому?", "Я вже готовий",
     "в немецком «я уже готов», а не вопрос"),
    (18876, "example_en", "Are you nervous about the upcoming exam?",
     "There is a party next week",
     "в немецком про праздник на следующей неделе, а не экзамен"),
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
