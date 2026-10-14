"""
Потерянная вопросительная форма, партия 2 из списка `scan_question_mark`.

Та же работа, что в партии 1, и те же три вида.

Самое заметное здесь — ряды, где перевод взял **повелительную форму вместо
вопроса**: «Kannst du mir den Ball werfen?» — «Throw the ball», «Topu bana
at!», а по-украински и вовсе «Не кидай сміття на підлогу». Просьба-вопрос и
приказ — разные вещи, и в немецком вежливом «Kannst du …?» весь смысл ряда.

Ещё один повтор: `mitnehmen` — во всех трёх языках пример про зонт («Возьми
зонт с собой»), а немецкий просит взять с собой **говорящего**.

    python -m app.scripts.fix_questions_manual_02            # показать
    python -m app.scripts.fix_questions_manual_02 --apply    # применить
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
    (1593, "example_uk", "У тебе є дрібні гроші", "У тебе є дрібні гроші?",
     "потерян только знак"),
    (1615, "example_uk", "Ти можеш це для мене скопіювати",
     "Ти можеш це для мене скопіювати?", "потерян только знак"),
    (1625, "example_uk", "Чи можу я заплатити кредитною карткою",
     "Чи можу я заплатити кредитною карткою?", "потерян только знак"),
    (1651, "example_uk", "Можеш позичити мені гроші",
     "Можеш позичити мені гроші?", "потерян только знак"),
    (1694, "example_tr", "Beraber geliyor musun", "Beraber geliyor musun?",
     "потерян только знак"),
    (1780, "example_uk", "Можеш дати мені пораду", "Можеш дати мені пораду?",
     "потерян только знак"),
    (1896, "example_tr", "Vatandaşlığınız nedir", "Vatandaşlığınız nedir?",
     "потерян только знак; здесь немецкий тоже на «Вы»"),
    (1933, "example_tr", "Değiştirebilir miyiz", "Değiştirebilir miyiz?",
     "потерян только знак"),
    (1933, "example_uk", "Ми можемо помінятися", "Ми можемо помінятися?",
     "потерян только знак"),
    (1974, "example_uk", "Вам потрібен пакет", "Вам потрібен пакет?",
     "потерян только знак; здесь немецкий тоже на «Вы»"),
    (2077, "example_uk", "У тебе є пропозиція", "У тебе є пропозиція?",
     "потерян только знак"),
    (2188, "example_uk", "Можу я приміряти сукню", "Можу я приміряти сукню?",
     "потерян только знак"),

    # --- в немецком «ты», в переводе «Вы» --------------------------------------
    (1374, "example_uk", "У вас є рекомендація",
     "У тебе є рекомендація для мене?",
     "в немецком «du» и «für mich»; и потерян знак"),
    (1455, "example_tr", "Doğum tarihiniz nedir", "Doğum tarihin ne?",
     "в немецком «dein» — ты; и потерян знак"),
    (1457, "example_tr", "Kızlık soyadınız nedir", "Kızlık soyadın ne?",
     "в немецком «dein» — ты; и потерян знак"),
    (1736, "example_tr", "Telefon numaranız nedir", "Telefon numaran ne?",
     "в немецком «deine» — ты; и потерян знак"),
    (2103, "example_uk", "Можете, будь ласка, повторити",
     "Можеш, будь ласка, повторити?",
     "в немецком «du» — ты; и потерян знак"),

    # --- вместо вопроса стоит повеление ----------------------------------------
    (1582, "example_en", "Please mark the mistakes",
     "Can you please mark the mistakes?",
     "в немецком вежливый вопрос, а не приказ"),
    (1582, "example_tr", "Lütfen hataları işaretleyin",
     "Lütfen hataları işaretler misin?",
     "в немецком вежливый вопрос, а не приказ"),
    (1582, "example_uk", "Будь ласка, позначте помилки",
     "Можеш, будь ласка, позначити помилки?",
     "в немецком вежливый вопрос, а не приказ"),
    (1646, "example_en", "Put the book on the table",
     "Should I put it here?",
     "в немецком вопрос «мне положить это сюда», а не приказ"),
    (1646, "example_tr", "Kitabı masanın üzerine koy",
     "Bunu buraya koyayım mı?",
     "в немецком вопрос «мне положить это сюда», а не приказ"),
    (1646, "example_uk", "Поклади книгу на стіл", "Покласти це сюди?",
     "в немецком вопрос «мне положить это сюда», а не приказ"),
    (2101, "example_en", "Throw the ball", "Can you throw me the ball?",
     "в немецком вежливый вопрос, а не приказ"),
    (2101, "example_tr", "Topu bana at!", "Topu bana atabilir misin?",
     "в немецком вежливый вопрос, а не приказ"),
    (2101, "example_uk", "Не кидай сміття на підлогу",
     "Можеш кинути мені м'яч?",
     "пример про мусор, а немецкий просит бросить мяч"),

    # --- перевод переводит другое предложение ---------------------------------
    (1398, "example_tr", "Sana bütün gün ulaşamadım",
     "Sana nasıl ulaşabilirim?",
     "в немецком вопрос «как мне тебя застать»"),
    (1404, "example_en", "Math is my favorite subject",
     "Which subject do you like best?", "в немецком вопрос, а не ответ"),
    (1404, "example_tr", "Matematik en sevdiğim ders",
     "En çok hangi dersi seviyorsun?", "в немецком вопрос, а не ответ"),
    (1404, "example_uk", "Математика — мій улюблений предмет",
     "Який предмет ти найбільше любиш?", "в немецком вопрос, а не ответ"),
    (1529, "example_uk", "Я відшукав старі фотографії на горищі",
     "Можеш відшукати цей документ?",
     "пример про фотографии, а немецкий про документ"),
    (1543, "example_en", "I upload the photos",
     "Can you upload the photos right away?",
     "в немецком вопрос «ты», а не «я загружаю»"),
    (1543, "example_tr", "Fotoğrafları yüklüyorum",
     "Fotoğrafları hemen yükleyebilir misin?",
     "в немецком вопрос «ты», а не «я загружаю»"),
    (1543, "example_uk", "Я завантажую фото",
     "Можеш одразу завантажити фото?",
     "в немецком вопрос «ты», а не «я завантажую»"),
    (1693, "example_tr", "Seninle birlikte gitmek istiyorum",
     "Seninle gelebilir miyim?",
     "в немецком вопрос «можно мне с тобой», а не «я хочу»"),
    (1694, "example_uk", "Ти йдеш разом", "Ти йдеш з нами?",
     "«разом» без «с нами» повисает; и потерян знак"),
    (1696, "example_en", "Take an umbrella with you",
     "Can you take me with you?",
     "в немецком просят взять с собой говорящего, а не зонт"),
    (1696, "example_tr", "Yanına bir şemsiye al",
     "Beni de yanında götürebilir misin?",
     "в немецком просят взять с собой говорящего, а не зонт"),
    (1696, "example_uk", "Візьми парасольку із собою",
     "Можеш взяти мене з собою?",
     "в немецком просят взять с собой говорящего, а не зонт"),
    (1725, "example_tr", "Köpeğini Karabaş diye adlandırdı",
     "Buna ne deniyor?",
     "пример про имя собаки, а немецкий «как это называется»"),
    (1749, "example_uk", "Аварія сталася біля школи", "Що сталося?",
     "в немецком вопрос «что случилось»"),
    (1776, "example_en", "The exam is tomorrow", "Is the exam tomorrow?",
     "в немецком вопрос, а не утверждение"),
    (1776, "example_tr", "Sınav yarın", "Sınav yarın mı?",
     "в немецком вопрос, а не утверждение"),
    (1826, "example_en", "He paid with a fifty-euro banknote",
     "Do you have a 100-euro note?",
     "в немецком вопрос про сто евро, а не рассказ про пятьдесят"),
    (1826, "example_uk", "У касі не прийняли стару купюру",
     "У тебе є купюра 100 євро?",
     "пример про кассу, а немецкий спрашивает про купюру"),
    (2010, "example_en", "We should do something about this mess",
     "What shall we do today?",
     "в немецком вопрос «что мы сегодня делаем»"),
    (2011, "example_en", "Honestly, I can't tell the difference",
     "What is the difference?", "в немецком вопрос «в чём разница»"),
    (2061, "example_en", "Please use a ballpoint pen",
     "What do you use this oil for?",
     "в немецком вопрос про масло, а не просьба про ручку"),
    (2061, "example_tr", "Lütfen bir tükenmez kalem kullanın",
     "Bu yağı ne için kullanıyorsun?",
     "в немецком вопрос про масло, а не просьба про ручку"),
    (2061, "example_uk", "Будь ласка, використовуй ручку",
     "Для чого ти використовуєш цю олію?",
     "в немецком вопрос про масло, а не просьба про ручку"),
    (2069, "example_en", "Experience is a requirement for this job",
     "What are the requirements?", "в немецком вопрос, а не утверждение"),
    (2069, "example_tr", "Benim tek bir şartım var", "Şartlar neler?",
     "в немецком вопрос, а не утверждение"),
    (2073, "example_uk", "У нас наявний лише один розмір",
     "Чи є ще місце?",
     "пример про размер, а немецкий спрашивает, есть ли место"),
    (2090, "example_en", "I'm going away now",
     "Do you want to leave again already?",
     "в немецком вопрос «ты», а не «я ухожу»"),
    (2090, "example_tr", "Şimdi gidiyorum", "Yine gitmek mi istiyorsun?",
     "в немецком вопрос «ты», а не «я ухожу»"),
    (2090, "example_uk", "Іди геть, я зараз зайнятий!",
     "Ти вже знову хочеш піти?",
     "в немецком вопрос, а не «уйди, я занят»"),
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
