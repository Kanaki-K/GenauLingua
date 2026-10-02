"""
Третий круг вычитки, ряды 1–102 (зерно 31337).

Самое заметное:

* `Mordanklage` — перевод говорит ровно обратное немецкому. В немецком
  «Die Mordanklage wurde fallen gelassen» — обвинение сняли; в польском
  «Postawiono mu oskarżenie» — обвинение предъявили.
* `Gefährdung` — в немецком угроза окружающей среде, в русском и украинском
  загрязнение, причём в украинском вовсе воздуха.
* `abgehoben` — внутри турецкого примера английское слово «arrogant».
* `qualvoll` — в немецком мучительная смерть, в украинском болезнь.
* `Drücker` — в немецком пистолет, в турецком ружьё.

    python -m app.scripts.fix_manual_round3            # показать
    python -m app.scripts.fix_manual_round3 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [

    # --- противоположный или подменённый смысл -------------------------------
    (16813, "example_pl",
     "Postawiono mu oskarżenie o morderstwo",
     "Oskarżenie o morderstwo zostało wycofane z braku dowodów",
     "в немецком обвинение СНЯЛИ, а здесь предъявили"),
    (16921, "example_ru",
     "Загрязнение окружающей среды представляет большую опасность",
     "Угроза окружающей среде — большая проблема",
     "загрязнение вместо угрозы"),
    (16921, "example_uk",
     "Забруднення повітря — велика загроза",
     "Загроза довкіллю — велика проблема",
     "загрязнение воздуха вместо угрозы среде"),
    (11375, "example_uk",
     "Це була довга й болісна хвороба",
     "Болісну смерть родині було важко пережити",
     "в немецком смерть, а не болезнь"),
    (18482, "example_tr",
     "Tüfeğin tetiği paslıydı",
     "Tabancanın tetiği paslıydı",
     "ружьё вместо пистолета"),
    (15230, "example_tr",
     "Oğul, babasının benzeri",
     "Oğul, babasının tıpatıp benzeri",
     "потеряно «точная» копия"),

    # --- чужой язык и опечатки -----------------------------------------------
    (10987, "example_tr",
     "Sıradan insanlar karşısında her zaman çok kibirli ve arrogant görünüyor",
     "Sıradan insanlara karşı her zaman çok kibirli ve küstah görünüyor",
     "«arrogant» — английское слово в турецком примере"),
    (10524, "example_tr",
     "Konuşmadan duygalandı ve gözlerinde gözyaşları vardı",
     "Konuşmadan duygulandı ve gözlerinde yaşlar vardı",
     "«duygalandı» — опечатка"),
    (10437, "example_tr",
     "Filmdeki gerilim harikaydi",
     "Filmdeki gerilim harikaydı",
     "нарушена гармония гласных"),
    (8545, "example_tr",
     "Hafta sonunda ziyaret etmek tercihan daha iyidir",
     "Tercihen hafta sonu ziyaret edin",
     "«tercihan» — опечатка, и фраза тяжёлая"),
    (7401, "example_tr",
     "Sokak burada önemli ölçüde darlıyor",
     "Bu yeni ayakkabılar parmaklarımı sıkıyor",
     "«darlıyor» — такой формы нет, и пример про другое"),
    (12025, "example_tr",
     "Bu garip karışım otlar ve bal gibi tadı geliyor",
     "Bu garip karışımın tadı ot ve bal gibi",
     "неграмотная конструкция"),
    (11184, "example_tr",
     "Babasından gitmemasını yalvarmaya başladı",
     "Babasına gitmemesi için yalvarmaya başladı",
     "«gitmemasını» — опечатка, и неверный падеж"),
    (10566, "example_tr",
     "Dürüstlük önemli bir erdemi",
     "Dürüstlük önemli bir erdemdir",
     "пропущена связка"),
    (14814, "example_tr",
     "Tanrı her şeye gücü yeten",
     "Tanrı her şeye gücü yetendir",
     "пропущена связка"),
    (13513, "example_tr",
     "Birbirinden çok şey bilmiyoruz",
     "Birbirimiz hakkında çok şey bilmiyoruz",
     "неверная форма местоимения"),
    (11882, "example_tr",
     "Noel pazarında sıcak ponş içiyoruz",
     "Noel pazarında meyveli sıcak punç içiyoruz",
     "«ponş» расходится с переводом «punç»"),

    # --- украинские и русские огрехи ----------------------------------------
    (8271, "example_uk",
     "Будь ласка, пощади мене від своїх коментарів",
     "Будь ласка, позбав мене своїх коментарів",
     "«пощадити від» — неверное управление"),
    (12025, "example_uk",
     "Цей дивний напар смакує травами й медом",
     "Це дивне варево має смак трав і меду",
     "«напар» расходится с переводом «варево»"),
    (16618, "example_ru",
     "Идентификация мертвого была очень сложной для властей",
     "Опознание погибшего было очень сложным для властей",
     "«мертвого» — грубо и не по-русски в этом контексте"),
    (16618, "example_uk",
     "Ідентифікація мертвого була дуже складною для влади",
     "Упізнання загиблого було дуже складним для влади",
     "то же"),
    (9554, "example_uk",
     "Учитель повчав учнів про найважливіші історичні події",
     "Учитель розповідав учням про найважливіші історичні події",
     "«повчати про» — неверное управление"),
    (9554, "example_ru",
     "Учитель поучал учеников насчёт важнейших исторических событий",
     "Учитель рассказывал ученикам о важнейших исторических событиях",
     "«поучал насчёт» — неграмотно"),
    (1123, "translation_ru",
     "всё, закончиться",
     "все, всё, закончиться",
     "«alle» — это «все», а стояло только «всё»"),

    # --- примеры про другое --------------------------------------------------
    (896, "example_en",
     "The lesson lasts one hour",
     "The film lasts two hours",
     "в немецком фильм и два часа"),
    (896, "example_uk",
     "Урок математики триває годину",
     "Фільм триває дві години",
     "в немецком фильм и два часа"),
    (896, "example_tr",
     "Bugün üç dersimiz var",
     "Film iki saat sürüyor",
     "в немецком фильм и два часа"),
    (14710, "example_tr",
     "Konserde çok güzel arp çaldı",
     "Harika arp çalıyor",
     "концерт из немецкого примера не следует"),
    (7436, "example_en",
     "He's very particular about his coffee",
     "That's nothing special",
     "пример про кофе, а немецкий про «ничего особенного»"),
    (18375, "example_ru",
     "Он долго отпирал дверь ключом",
     "Можешь отпереть дверь?",
     "в немецком вопрос"),
    (7739, "example_pl",
     "Musisz przedstawić umowę w biurze",
     "Czy możesz przedstawić umowę?",
     "в немецком вопрос про договор"),
    (10778, "example_tr",
     "Bir daha hiç yalan söylemeyeceğine söz verdi",
     "Bir daha asla yalan söylemeyeceğine dair yemin etti",
     "в немецком обет, а не простое обещание"),
    (10515, "example_pl",
     "W upale potrzeba wody jest ogromna",
     "W upale potrzeba wody jest bardzo duża",
     "«ogromna» сильнее немецкого «sehr groß»"),
    (16258, "example_tr",
     "Alay şehirde konuşlanmıştı",
     "Alay şehirde konuşlandırılmıştı",
     "неверный залог"),
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
