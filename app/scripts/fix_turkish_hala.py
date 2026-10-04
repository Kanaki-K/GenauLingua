"""
Турецкие классы, найденные в блоках 18–19 и закрытые сплошным поиском.

**1. «hala» вместо «hâlâ» — 24 ячейки.** Это не придирка к значку:
«hala» и «hâlâ» разные слова. «Hala» — тётя по отцу. «Çorba hala çok
sıcak» читается как «суп, тётя, очень горячий». Циркумфлекс в турецком
оставлен ровно там, где без него слово меняется, и это тот случай.
Класс был известен — в блоке 8 правилось «Hâlâ umudum var», — но
сплошным поиском его никто не прошёл.

**2. «tadıyor» — 3 ячейки.** «Yemek iğrenç tadıyor» это калька с
английского «the food tastes disgusting». По-турецки вкус не «пробуют»,
а «имеют»: «yemeğin tadı iğrenç».

**3. «kar» вместо «kâr» — 1 ячейка.** Снова разные слова: kar — снег,
kâr — прибыль. `Profit`: «Şirket büyük kar yapıyor» — «фирма делает
много снега». Остальные три «kar» в базе — про снег, они верны.

Попутно правятся дефекты в тех же строках, раз они всё равно открыты:
«telekoin telefonu» и «Tellerler» (таких слов нет), «Almanyada»,
«Brezilyanın», «Beatlesle» (пропущен апостроф в имени собственном),
«ipotekimizi» (нужно «ipoteğimizi»), и три примера, где немецкий говорит
«ещё 20 лет», «ещё две недели», «на вокзале», а турецкий — другое.

    python -m app.scripts.fix_turkish_hala            # показать
    python -m app.scripts.fix_turkish_hala --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

_HALA = "«hala» без циркумфлекса — это тётя, а не «до сих пор»"

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- только циркумфлекс ---------------------------------------------------
    (7847, "example_tr", "Tabağındaki biftek hala dokunulmamıştı",
     "Tabağındaki biftek hâlâ dokunulmamıştı", _HALA),
    (8256, "example_tr", "Çizilmiş telefon hala çalışıyor",
     "Çizilmiş telefon hâlâ çalışıyor", _HALA),
    (9723, "example_tr", "Sana hala para borçluyum",
     "Sana hâlâ para borçluyum", _HALA),
    (11202, "example_tr", "Yanıtında hala tereddüt ediyor",
     "Yanıtında hâlâ tereddüt ediyor", _HALA),
    (11911, "example_tr", "Dişimin dolgusu hala ağrıyor",
     "Dişimin dolgusu hâlâ ağrıyor", _HALA),
    (12015, "example_tr",
     "Eski bira fabrikası hala geleneksel yöntemlerle bira üretiyordu",
     "Eski bira fabrikası hâlâ geleneksel yöntemlerle bira üretiyordu",
     _HALA),
    (12608, "example_tr", "Ölüm sebebi hala belirsiz",
     "Ölüm sebebi hâlâ belirsiz", _HALA),
    (14651, "example_tr", "Bazı insanlar hala batıl inançlara inanırlar",
     "Bazı insanlar hâlâ batıl inançlara inanırlar", _HALA),
    (15131, "example_tr", "Bekar hala küçük bir dairede yalnız yaşıyor",
     "Bekar hâlâ küçük bir dairede yalnız yaşıyor", _HALA),
    (15703, "example_tr", "Çorba hala çok sıcak, önce soğumasını bekle",
     "Çorba hâlâ çok sıcak, önce soğumasını bekle", _HALA),
    (16479, "example_tr", "Uçağın düşürülmesi hala belirsizdi",
     "Uçağın düşürülmesi hâlâ belirsizdi", _HALA),
    (18483, "example_tr", "Eski dikiş makinesi hala çok iyi çalışıyor",
     "Eski dikiş makinesi hâlâ çok iyi çalışıyor", _HALA),
    (18747, "example_tr", "Şafakta hala karanlıktı",
     "Şafakta hâlâ karanlıktı", _HALA),

    # --- циркумфлекс и несуществующее слово рядом -----------------------------
    (14257, "example_tr", "Köşede hala eski bir telekoin telefonu var",
     "Garda hâlâ eski bir ankesörlü telefon var",
     "«telekoin» — такого слова нет; и в немецком телефон на вокзале, "
     "а не на углу"),
    (17742, "example_tr", "Tellerler akkordan sonra hala titreşiyor",
     "Teller akordan sonra hâlâ titreşiyor",
     "«Tellerler» — двойное множественное, и «akkordan» с двумя «k»"),

    # --- циркумфлекс и пропущенный апостроф в имени собственном ---------------
    (15259, "example_tr",
     "Bu ailenin neslinden gelen bugün hala Almanyada yaşıyor",
     "Bu ailenin soyundan gelen biri bugün hâlâ Almanya'da yaşıyor",
     "«Almanyada» без апострофа, и «gelen» без существительного"),
    (15781, "example_tr",
     "Brezilyanın ilk ormanında hala birçok keşfedilmemiş alan var",
     "Brezilya'nın balta girmemiş ormanlarında hâlâ birçok keşfedilmemiş alan var",
     "«ilk orman» — первый лес; «Urwald» это «balta girmemiş orman». "
     "И «Brezilyanın» без апострофа"),
    (14777, "example_tr",
     "Beatlesle ilgili eski plağını hala severek çalıyor",
     "Eski Beatles plağını hâlâ severek çalıyor",
     "«Beatlesle ilgili» — «про Beatles»; в немецком это его пластинка "
     "Beatles"),

    # --- циркумфлекс и канцелярит или калька ----------------------------------
    (8176, "example_tr", "Yemek hala buhar çıkarıyor, çok sıcak",
     "Yemeğin hâlâ buharı çıkıyor, çok sıcak",
     "«yemek buhar çıkarıyor» — так не говорят"),
    (11822, "example_tr", "Et yemek için hala çok çiğ idi",
     "Et yemek için hâlâ çok çiğdi", "«çiğ idi» пишется слитно: «çiğdi»"),
    (12713, "example_tr", "Partiden sonra hala sarhoş haldeyim",
     "Partiden sonra hâlâ sarhoşum", "«sarhoş haldeyim» — книжно"),
    (17688, "example_tr", "Makine hala işlevseldir",
     "Makine hâlâ çalışır durumda", "«-dir» — канцелярит"),

    # --- в немецком «ещё столько-то», а не «до сих пор» -----------------------
    (9805, "example_tr", "Biz hala 20 yıl ipotekimizi ödüyoruz",
     "İpoteğimizi daha 20 yıl ödeyeceğiz",
     "немецкий «noch 20 Jahre» — ещё двадцать лет; и «ipotekimizi» "
     "вместо «ipoteğimizi»"),
    (12621, "example_tr", "Benim kardeşim hala iki hafta karantinada",
     "Kardeşim daha iki hafta karantinada",
     "немецкий «noch zwei Wochen» — ещё две недели"),

    # --- «tadıyor»: вкус по-турецки не пробуют, а имеют -----------------------
    (10338, "example_tr", "Yemek iğrenç tadıyor", "Yemeğin tadı iğrenç",
     "«tadıyor» — калька с английского «tastes disgusting»"),
    (11003, "example_tr", "Yemek İtalyadaki gibi orijinal tadıyor",
     "Yemeğin tadı İtalya'daki gibi özgün",
     "то же, и «İtalyadaki» без апострофа"),
    (11850, "example_tr", "Bonbon frambuaza tadıyor",
     "Bonbonun tadı frambuaz gibi", "то же, и «frambuaza» — неверный падеж"),

    # --- kar и kâr — разные слова ---------------------------------------------
    (17793, "example_tr", "Şirket büyük kar yapıyor",
     "Şirket büyük kâr ediyor",
     "«kar» — снег; прибыль это «kâr», и говорят «kâr etmek»"),
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
