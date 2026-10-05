"""
Сплошная вычитка, блок 22: ряды 2701–2900 по рангу частотности
(id первого 6882, id последнего 15471).

Находки:

* `Anwältin` — в украинской колонке стоял пример из совсем другого ряда:
  «Детектив шукає нові улики» при немецком «Meine Anwältin hat gesagt,
  ich soll nichts unterschreiben». Рядом, в ряду 2843 `Detektiv`, этот
  пример и живёт. Похоже на сбой при переносе: строка попала не туда. И
  «улики» в украинском — русизм, там «докази».
* `auflegen`, `Cola`, `präsentieren`, `Nest`, `Ruder`, `streichen`,
  `Steak`, `verschaffen`, `erhöhen`, `nüchtern`, `Datum`, `engagiert`,
  `Turner`, `geschäftlich`, `übernachten` — перевод переводит другую
  фразу.
* `Ruder` — битый эталон: «rudern übers See». «See» мужского рода, нужно
  «über den See».
* `weisen` — тоже эталон: «Kannst du mir zum Bahnhof weisen?» без «den
  Weg» по-немецки не говорят, а все пять переводов именно про дорогу.
* `Verlobte` — в украинских значениях «нареченій» вместо «наречений».
  `auflegen` — «поклати» вместо «покласти». `Kardinal` — «мессу» с
  русским удвоением. `Tüte` — «ріжок для мороженого». `fit` — «бодрий».
  `Gefangener` — «арестант». Всё это русизмы и опечатки.
* `Experte` — турецкое «İtalyan mutfağı uzmanı» без связки: это не
  предложение, а подпись.
* `Zentimeter`, `reserviert` — турецкое «-dır» в разговорной фразе.
* `runden` — «50ye» без апострофа: в турецком число берёт апостроф.

Отдельно закрыт класс английских сокращений без апострофа («Were» вместо
«We're») — 13 ячеек, скрипт `fix_en_contractions`. Он зеркален классу
`fix_apostrophe_s`: там апостроф влез лишний, тут пропал нужный.

    python -m app.scripts.fix_block_0022            # показать
    python -m app.scripts.fix_block_0022 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- пример из чужого ряда -------------------------------------------------
    (8823, "example_uk", "Детектив шукає нові улики",
     "Моя адвокатка сказала, щоб я нічого не підписував",
     "это пример ряда 2843 `Detektiv`, попавший сюда; и «улики» — русизм"),
    (8823, "translation_uk", "адвокат, юристка, захисниця",
     "адвокатка, юристка, захисниця", "ряд про женщину-адвоката"),

    # --- пример переводит другую фразу ---------------------------------------
    (13500, "example_uk", "Той будинок навпроти — мій",
     "У тому будинку навпроти живе мій друг",
     "немецкий «In jenem Haus da drüben wohnt mein Freund»"),
    (2426, "example_tr", "Patron bu ay maaşımızı artırdı",
     "Fiyatları artırmamız gerekiyor",
     "немецкий «Wir müssen die Preise erhöhen»"),
    (10365, "example_uk", "Вона дуже завзята працівниця",
     "Вона дуже завзята вчителька", "в немецком учительница"),
    (6898, "example_tr", "Devlet öğrencilere ücretsiz kitap sağlıyor",
     "Hobilerim için daha fazla zaman ayırmam gerekiyor",
     "немецкий «Ich muss mir mehr Zeit für Hobbys verschaffen»"),
    (1904, "example_tr", "Akşam yemeğinde biftek yedik",
     "Biftek yemeyi severim", "немецкий «Ich esse gerne Steak»"),
    (10367, "example_en", "I perceive it quite differently",
     "I find this music very relaxing",
     "немецкий «Ich empfinde diese Musik als sehr entspannend»"),
    (13961, "example_en", "He just hung up without saying goodbye",
     "I have to hang up now, bye!",
     "немецкий «Ich muss jetzt auflegen, tschüss!»"),
    (13961, "example_uk", "Він просто поклав слухавку, не попрощавшись",
     "Мені пора класти слухавку, бувай!", "то же"),
    (13961, "example_tr", "Vedalaşmadan telefonu kapattı",
     "Şimdi telefonu kapatmam lazım, hoşça kal!", "то же"),
    (154, "example_en", "She orders a cola", "I'm ordering a cola",
     "немецкий «Ich bestelle mir eine Cola» — я, а не она"),
    (154, "example_uk", "Вона замовляє колу", "Я замовляю собі колу", "то же"),
    (154, "example_tr", "Bir kola sipariş ediyor",
     "Kendime bir kola sipariş ediyorum", "то же"),
    (887, "example_tr", "Saçlarını siyaha boyadı",
     "Odamdaki duvarı boyuyorum",
     "немецкий «Ich streiche die Wand in meinem Zimmer»"),
    (15464, "example_en", "There's a small bird's nest in the tree",
     "The birds are building a nest in the tree",
     "немецкий «Die Vögel bauen ein Nest im Baum» — птицы строят"),
    (15464, "example_ru", "На дереве маленькое птичье гнездо",
     "Птицы строят гнездо на дереве", "то же"),
    (15464, "example_uk", "На дереві маленьке пташине гніздо",
     "Птахи будують гніздо на дереві", "то же"),
    (15464, "example_tr", "Ağaçta küçük bir kuş yuvası var",
     "Kuşlar ağaçta yuva yapıyor", "то же"),
    (12558, "example_uk", "Сьогодні я абсолютно тверезий",
     "Для забору крові ти маєш бути натщесерце",
     "немецкий «Für die Blutabnahme musst du nüchtern sein»"),
    (168, "example_tr", "Düğünün tarihi belli oldu mu?",
     "Bugünün tarihi ne?",
     "немецкий «Wie lautet das heutige Datum?»"),
    (8829, "example_uk", "Завтра в мене ділова поїздка",
     "Завтра я у справах у Берліні",
     "немецкий «Morgen bin ich geschäftlich in Berlin»"),
    (2895, "example_tr", "Bu gece çadırda geceleyeceğiz",
     "Gölün kenarındaki otelde geceleyeceğiz",
     "немецкий «Wir übernachten im Hotel am See» — отель, не палатка"),
    (12163, "example_en", "With the oar we row the boat forward",
     "We take the oars and row across the lake",
     "немецкий «Wir nehmen die Ruder und rudern über den See»"),
    (12163, "example_uk", "Веслом ми гребемо човен",
     "Ми беремо весла і гребемо через озеро", "то же"),
    (12163, "example_tr", "Kürekle tekneyi ileri taşıyoruz",
     "Kürekleri alıp gölün karşısına geçiyoruz", "то же"),
    (12161, "example_uk", "Гімнаст щодня робить вправи на перекладині",
     "Гімнаст тренується щодня", "перекладины в немецком нет"),
    (12161, "example_tr",
     "Jimnastikçi her gün barfiks çubuğunda egzersiz yapıyor",
     "Jimnastikçi her gün antrenman yapıyor", "то же"),

    # --- немецкий эталон -------------------------------------------------------
    (13953, "example_de", "Kannst du mir zum Bahnhof weisen?",
     "Kannst du mir den Weg zum Bahnhof weisen?",
     "без «den Weg» по-немецки так не говорят; все переводы про дорогу"),
    (12163, "example_de", "Wir nehmen die Ruder und rudern übers See",
     "Wir nehmen die Ruder und rudern über den See",
     "«der See» мужского рода: «über den See»"),

    # --- потеряно или добавлено ------------------------------------------------
    (1460, "example_en", "We learn a poem", "We learn a poem by heart",
     "потеряно «auswendig» — наизусть"),
    (1460, "example_uk", "Ми вчимо вірш", "Ми вчимо вірш напам'ять", "то же"),
    (1460, "example_tr", "Bir şiir öğreniyoruz",
     "Bir şiiri ezbere öğreniyoruz", "то же"),
    (1294, "example_en", "Can you saw a board?",
     "Can you help me saw the board?", "потеряно «mir helfen»"),
    (1294, "example_tr", "Bir tahtayı kesebilir misin?",
     "Tahtayı kesmeme yardım eder misin?", "то же"),
    (2729, "example_en", "I present the results",
     "I'll present the results tomorrow", "потеряно «morgen»"),
    (2729, "example_uk", "Я презентую результати",
     "Я презентую результати завтра", "то же"),
    (2729, "example_tr", "Sonuçları sunuyorum",
     "Sonuçları yarın sunacağım", "то же"),
    (17115, "example_en", "There was a car accident",
     "There was a serious car accident", "потеряно «schwer»"),
    (17115, "example_ru", "Произошла авария",
     "Произошла тяжёлая авария", "то же"),
    (17115, "example_uk", "Сталася дорожня аварія",
     "Сталася важка автомобільна аварія", "то же"),
    (17115, "example_tr", "Bir trafik kazası oldu",
     "Ağır bir trafik kazası oldu", "то же"),
    (2390, "example_uk", "Його замкнули в клітці", "Його замкнули",
     "клетки в немецком нет"),
    (6882, "example_uk", "У мене є трохи часу між справами",
     "У мене є ще трохи часу у проміжку", "«між справами» в немецком нет"),
    (621, "example_uk", "У березні вже значно тепліше",
     "У березні стає тепліше", "«вже значно» в немецком нет"),
    (6906, "example_uk", "Будь ласка, скажи мені точний час",
     "Мені потрібен точний час",
     "немецкий «Ich brauche die exakte Zeit» — без «скажи»"),
    (6906, "example_tr", "Lütfen bana kesin saati söyle",
     "Kesin saate ihtiyacım var", "то же"),

    # --- русизмы и опечатки ----------------------------------------------------
    (15008, "translation_uk", "наречена, нареченій",
     "наречена, наречений", "«нареченій» — опечатка"),
    (13961, "translation_uk",
     "покласти слухавку, поклати зверху, подати на стіл, ставити платівки",
     "покласти слухавку, покласти зверху, подати на стіл, ставити платівки",
     "«поклати» — опечатка"),
    (14441, "example_uk", "Кардинал завтра проводить важливу мессу",
     "Кардинал завтра проводить важливу месу",
     "«мессу» — удвоение из русского"),
    (1974, "translation_uk", "пакет, торбинка, ріжок для мороженого",
     "пакет, торбинка, ріжок для морозива", "«мороженого» — русизм"),
    (12557, "translation_uk", "у формі, бодрий, обізнаний",
     "у формі, бадьорий, обізнаний", "«бодрий» — русизм"),
    (16071, "translation_uk", "в'язень, арестант, полонений",
     "в'язень, арештант, полонений", "«арестант» — русизм"),
    (17110, "example_uk", "Машини постійно посигналюють в заторі",
     "Машини постійно сигналять у заторі", "«посигналюють» — не та форма"),

    # --- грамматика целевого языка ---------------------------------------------
    (8821, "example_tr", "İtalyan mutfağı uzmanı",
     "O, İtalyan mutfağı uzmanı", "пропущена связка — это не предложение"),
    (15010, "example_tr", "Kedi hanımının her yere peşinden gidiyor",
     "Kedi her yerde hanımının peşinden gidiyor", "порядок слов"),
    (6912, "example_tr", "Bunun bizim sorunla ilişkisi yok",
     "Bunun bizim sorunumuzla ilişkisi yok",
     "пропущен притяжательный аффикс"),
    (6908, "example_tr", "Sayıyı 50ye yuvarlayabilir misin?",
     "Sayıyı 50'ye yuvarlayabilir misin?",
     "в турецком число берёт апостроф перед окончанием"),
    (8829, "example_tr", "Yarın Berlinde iş için gidiyorum",
     "Yarın iş için Berlin'e gidiyorum",
     "пропущен апостроф, и «Berlinde gidiyorum» — неверный падеж"),
    (10366, "example_uk", "Ця книга може мене повністю захоплювати",
     "Ця книга може мене повністю захопити", "вид глагола"),
    (10367, "example_uk", "Я сприймаю цю музику як дуже розслабляючу",
     "Я сприймаю цю музику як дуже розслабливу",
     "«розслабляючу» — активный причастие, в украинском его нет"),

    # --- подменённое значение ---------------------------------------------------
    (13500, "example_pl",
     "W tamtym domu po drugiej stronie mieszka mój kolega",
     "W tamtym domu po drugiej stronie mieszka mój przyjaciel",
     "«Freund» — друг, а «kolega» приятель"),
    (10363, "example_tr", "Görgün gerçekten kötü",
     "Terbiyen gerçekten kötü", "«görgü» так о человеке не говорят"),
    (6890, "example_tr", "Bu şarkı bana tamamen bilinmiyor",
     "Bu şarkıyı hiç bilmiyorum", "калька; по-турецки «не знаю песню»"),
    (6891, "example_uk", "Стріла влучила прямо в ціль",
     "Стріла полетіла прямо в ціль", "в немецком полетела, а не попала"),
    (2183, "example_tr", "Teknik tesisat modernize edildi",
     "Teknik tesis modernize edildi",
     "«tesisat» — водопровод; в значениях «tesis»"),
    (6882, "example_tr", "Arasında biraz zamanım var",
     "O arada biraz zamanım var", "«Arasında» — между чем?"),

    # --- говорить по-людски -----------------------------------------------------
    (2764, "example_uk", "Німеччина є республікою", "Німеччина — республіка",
     "«є» — канцелярит"),
    (10364, "example_ru", "Я просто не могу сопротивляться этому шоколаду",
     "Я просто не могу устоять перед этим шоколадом",
     "«сопротивляться шоколаду» — калька"),
    (10364, "example_uk", "Я просто не можу опиратися цьому шоколаду",
     "Я просто не можу втриматися від цього шоколаду", "то же"),
    (10365, "example_tr", "O çok kendini adamış bir öğretmen",
     "O, kendini işine adamış bir öğretmen",
     "«çok kendini adamış» так не говорят"),
    (6907, "example_tr", "Ağırlıkla sebze yiyorum",
     "Çoğunlukla sebze yiyorum", "«ağırlıkla» так не говорят"),
    (17931, "example_tr", "Çocuk 120 santimetre boyundadır",
     "Çocuk 120 santimetre boyunda", "«-dır» — канцелярит"),
    (6915, "example_tr", "Restoranda masa ayrılmıştır",
     "Restorandaki masa ayrılmış", "«-tır» — канцелярит"),
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
