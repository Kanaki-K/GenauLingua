"""
Сплошная вычитка, блок 7: ряды 601–700 по рангу частотности.

Находки:

* `wach` — в украинском значении «бодрий», это русское слово; по-украински
  «бадьорий». И русский пример «Я ещё бодрствую» — так не говорят.
* `weitere` — турецкое «Başka sorun var mı?» читается как «есть другая
  проблема?»: «sorun» это проблема, а «soru» вопрос. Ряд про вопросы.
* `Auge` — немецкий «Er hat blaue Augen», а украинский про боль в правом
  глазу, турецкий про попавшую пылинку, польский про что-то в глазу. Три
  языка ушли в одну сторону — к жалобам на глаз.
* `fort` — из пяти переводов к немецкому «Sie ist für zwei Wochen fort»
  подходил только польский.
* `tschüss` — украинское «Чао» вместо «Бувай»: слова нет даже в собственном
  списке значений этого ряда.
* `Meister` — дефис вместо тире в украинском примере.

    python -m app.scripts.fix_block_0007            # показать
    python -m app.scripts.fix_block_0007 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- русизм и неверное слово в значениях ----------------------------------
    (12474, "translation_uk", "бодрий, який прокинувся, який не спить",
     "бадьорий, який прокинувся, який не спить",
     "«бодрий» — русизм, по-украински «бадьорий»"),
    (12474, "example_ru", "Я ещё бодрствую", "Я ещё не сплю",
     "«бодрствую» в живой речи не употребляют"),
    (12474, "example_uk", "Я вже прокинувся, можеш заходити",
     "Я ще не сплю", "в немецком «я ещё не сплю»"),
    (6349, "example_tr", "Başka sorun var mı?", "Başka soru var mı?",
     "«sorun» — проблема, а ряд про вопросы"),

    # --- дефис вместо тире ----------------------------------------------------
    (8740, "example_uk", "Мій батько - майстер у своїй майстерні",
     "Мій батько — майстер у своїй майстерні",
     "дефис вместо тире"),

    # --- пример переводит другую фразу ----------------------------------------
    (554, "example_en", "I like to lie on the sofa",
     "The book is lying on the table",
     "в немецком книга на столе, а не диван"),
    (6330, "example_en", "She walked away without saying anything",
     "She is away for two weeks", "в немецком «её нет две недели»"),
    (6330, "example_ru", "Она уехала прочь на две недели",
     "Она в отъезде на две недели", "«уехала прочь» по-русски не говорят"),
    (6330, "example_uk", "Він пішов геть і не озирнувся",
     "Вона у від'їзді на два тижні", "в немецком «её нет две недели»"),
    (6330, "example_tr", "Topu çok uzağa attı",
     "İki haftadır burada değil", "пример про мяч, а немецкий про отъезд"),
    (10075, "example_uk", "Це було дурно з мого боку",
     "Це було дурістю з мого боку", "«дурно» — русизм"),
    (54, "example_uk", "У мене болить праве око", "У нього голубі очі",
     "в немецком «у него голубые глаза»"),
    (54, "example_tr", "Gözüme toz kaçtı", "Mavi gözleri var",
     "в немецком «у него голубые глаза»"),
    (54, "example_pl", "Coś mi wpadło do oka", "Ma niebieskie oczy",
     "в немецком «у него голубые глаза»"),
    (1486, "example_en", "I hope we win tonight",
     "We really want to win the game",
     "в немецком «мы очень хотим выиграть»"),
    (1486, "example_uk", "Ми виграли гру", "Ми дуже хочемо виграти гру",
     "в немецком игра ещё не сыграна"),
    (1486, "example_tr", "Oyunu kazandık",
     "Maçı kesinlikle kazanmak istiyoruz", "в немецком игра ещё не сыграна"),
    (10076, "example_pl", "Ona jest bardzo zręczna w takich rzeczach",
     "Jesteś bardzo zręczny", "в немецком «ты», а не «она»"),
    (10077, "example_pl", "To dziwne, że nie odpisuje", "To jest dziwne",
     "вторая половина в немецком отсутствует"),
    (13389, "example_uk", "Я йду, хоча йде дощ",
     "Я виходжу на вулицю, хоча йде дощ", "потеряно «на улицу»"),
    (13389, "example_pl", "Wyszedł na dwór, chociaż pada",
     "Wychodzę na dwór, chociaż pada",
     "в немецком «я», настоящее время, а не «он» в прошедшем"),
    (10078, "example_pl", "Miałem dziś dziwny sen", "Miałem piękny sen",
     "в немецком сон был красивый, а не странный"),
    (2749, "example_en", "I'll sort out the tickets tomorrow",
     "That's sorted out", "в немецком «это урегулировано»"),
    (2749, "example_tr", "Yarın küçük bir toplantı düzenleyeceğiz",
     "Bu halledildi", "в немецком «это урегулировано»"),
    (255, "example_pl", "Złap piłkę, lecę do ciebie", "On łapie piłkę",
     "в немецком «он ловит мяч», а не приказ"),
    (6337, "example_tr", "Kapa çeneni", "Sandığın kapağı kırıktı",
     "взято другое значение: «закрой рот» вместо крышки ящика"),
    (1898, "example_en", "He's constantly on his phone",
     "He calls constantly", "в немецком «он постоянно звонит»"),
    (13392, "example_pl", "Ktoś do ciebie dzwonił",
     "Pomagam komuś w przeprowadzce",
     "в немецком «я помогаю кому-то с переездом»"),
    (492, "example_uk", "У нас маленька, але затишна квартира",
     "Моя кімната маленька", "в немецком «моя комната маленькая»"),
    (492, "example_en", "The room is small", "My room is small",
     "потеряно «моя»"),
    (13395, "example_pl", "Kupiłam coś dla dziecka",
     "To jest dla samochodu", "в немецком «это для машины»"),
    (8742, "example_tr", "Şef bugün çok keyifli", "Patronum çok iyi",
     "в немецком «мой начальник очень милый»"),
    (912, "example_en", "They dance together", "We dance together",
     "в немецком «мы», а не «они»"),
    (912, "example_uk", "Вони танцюють разом", "Ми танцюємо разом",
     "в немецком «мы», а не «они»"),
    (10084, "example_tr", "Ruhum bugün çok yorgun",
     "O iyi kalpli bir insan",
     "в немецком «он добрая душа», а не «моя душа устала»"),
    (18605, "example_ru", "Когда-нибудь это случится",
     "Когда-нибудь придёт время", "в немецком «придёт время»"),
    (1832, "example_uk", "Не бий кота, він добрий",
     "Моє серце швидко б'ється", "в немецком про сердце, а не про кота"),
    (1832, "example_tr", "Sinirlenince masaya yumruğunu vurdu",
     "Kalbim hızlı atıyor", "в немецком про сердце, а не про удар по столу"),
    (282, "example_uk", "Фото класне", "Фото миле",
     "«süß» — милое, а не классное"),
    (13399, "example_pl", "Zawsze zamawiam to samo", "Myślimy to samo",
     "в немецком «мы думаем одно и то же»"),
    (913, "example_en", "Where is my bag?", "Where is your bag?",
     "в немецком «deine» — твоя"),
    (913, "example_uk", "Де моя сумка?", "Де твоя сумка?",
     "в немецком «deine» — твоя"),
    (913, "example_tr", "Çantam nerede?", "Çantan nerede?",
     "в немецком «deine» — твоя"),
    (13401, "example_pl", "Powiedz coś, nie milcz", "Coś zapomniałem",
     "в немецком «я что-то забыл»"),
    (945, "example_uk", "Чао, до завтра", "Бувай, до завтра",
     "«чао» нет даже в списке значений этого ряда"),

    # --- потеряно или добавлено против немецкого -------------------------------
    (32, "example_tr", "Cevabınızı bekliyorum", "Cevabını bekliyorum",
     "в немецком «deine» — твоего"),
    (1532, "example_uk", "Ми їздимо навколо міста", "Ми їдемо навколо міста",
     "в немецком однократное действие"),
    (10083, "example_pl", "To dla mnie wielki zaszczyt",
     "To wielki zaszczyt", "«для меня» в немецком нет"),
    (627, "example_uk", "Після роботи я дуже втомлений",
     "Я дуже втомлений", "«после работы» в немецком нет"),
    (1551, "example_uk", "Сукня гарна", "Сукня виглядає гарно",
     "потеряно «выглядит»"),
    (1551, "example_tr", "Elbise güzel", "Elbise güzel görünüyor",
     "потеряно «выглядит»"),
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
