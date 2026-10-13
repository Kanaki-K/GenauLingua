"""
Сквозная правка класса «словарная статья во множественном числе при
существительном в единственном».

Класс нашёлся в блоке 54 на ряде `der Partisan` («партизаны,
повстанцы») и был проверен приметой scan_plural_gloss по всей базе:
7250 существительных с артиклем, 65 попаданий, из них 34 законных
(немецкие pluralia tantum вроде `die Gezeiten`, `die Klamotten`,
собирательные `das Gebirge`, `die Kundschaft`) и 30 настоящих.

Чинятся ТОЛЬКО словарные статьи. Пример ряда не трогаем: статья должна
отвечать заголовку, а пример живёт своей жизнью и выверяется отдельно,
при сплошном чтении.

`das Wertpapiere` (id 9928) в список не вошёл: там сломан сам заголовок
(артикль `das` при множественном `Wertpapiere`), а заголовки — решение
владельца, см. HANDOVER.

    python -m app.scripts.fix_plural_gloss            # показать
    python -m app.scripts.fix_plural_gloss --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

WHY = "статья во множественном при слове ряда в единственном"

FIXES: list[tuple[int, str, str, str, str]] = [
    # 9273 der Kaufmann
    (9273, "translation_en", "merchants, traders, businesspeople",
     "merchant, trader, businessman", WHY),
    (9273, "translation_ru", "коммерсанты, торговцы, купцы",
     "коммерсант, торговец, купец", WHY),
    (9273, "translation_uk", "комерсанти, торговці, купці",
     "комерсант, торговець, купець", WHY),
    (9273, "translation_tr", "tüccarlar, iş adamları",
     "tüccar, iş adamı", WHY),
    (9273, "translation_pl", "kupcy, handlowcy",
     "kupiec, handlowiec", WHY),
    # 10750 die Priorität
    (10750, "translation_en", "priorities", "priority", WHY),
    (10750, "translation_ru", "приоритеты, первоочередные задачи",
     "приоритет, первоочередная задача", WHY),
    (10750, "translation_uk", "пріоритети, першочергові завдання",
     "пріоритет, першочергове завдання", WHY),
    (10750, "translation_tr", "öncelikler", "öncelik", WHY),
    (10750, "translation_pl", "priorytety, sprawy najważniejsze",
     "priorytet, sprawa najważniejsza", WHY),
    # 10765 die Unannehmlichkeit
    (10765, "translation_en", "inconveniences, troubles",
     "inconvenience, trouble", WHY),
    (10765, "translation_ru", "неудобства, неприятности, хлопоты",
     "неудобство, неприятность", WHY),
    (10765, "translation_uk", "незручності, неприємності, клопоти",
     "незручність, неприємність", WHY),
    (10765, "translation_tr", "rahatsızlıklar, zahmetler, sıkıntılar",
     "rahatsızlık, zahmet, sıkıntı", WHY),
    (10765, "translation_pl", "niedogodności, kłopoty",
     "niedogodność, kłopot", WHY),
    # 11499 der Vorbehalt
    (11499, "translation_en", "reservations, objections, misgivings",
     "reservation, objection, misgiving", WHY),
    (11499, "translation_ru", "сомнения, возражения, оговорки",
     "сомнение, возражение, оговорка", WHY),
    (11499, "translation_uk", "сумніви, заперечення, застереження",
     "сумнів, заперечення, застереження", WHY),
    (11499, "translation_tr", "çekinceler, itirazlar, kuşkular",
     "çekince, itiraz, kuşku", WHY),
    (11499, "translation_pl", "zastrzeżenia, wątpliwości, obiekcje",
     "zastrzeżenie, wątpliwość, obiekcja", WHY),
    # 12010 das Kraut
    (12010, "translation_en", "herbs, greens", "herb, green herb", WHY),
    (12010, "translation_ru", "травы, зелень, пряные травы",
     "трава, зелень, пряная трава", WHY),
    (12010, "translation_uk", "трави, зелень, пряні трави",
     "трава, зелень, пряна трава", WHY),
    (12010, "translation_tr", "otlar, baharat otları, yeşillik",
     "ot, baharat otu, yeşillik", WHY),
    (12010, "translation_pl", "zioła, zielenina", "zioło, zielenina", WHY),
    # 12257 die Spielsache
    (12257, "translation_en", "toys", "toy", WHY),
    (12257, "translation_ru", "игрушки", "игрушка", WHY),
    (12257, "translation_uk", "іграшки", "іграшка", WHY),
    (12257, "translation_tr", "oyuncaklar", "oyuncak", WHY),
    (12257, "translation_pl", "zabawki", "zabawka", WHY),
    # 12684 das Antibiotikum
    (12684, "translation_en", "antibiotics", "antibiotic", WHY),
    (12684, "translation_ru", "антибиотики", "антибиотик", WHY),
    (12684, "translation_uk", "антибіотики", "антибіотик", WHY),
    (12684, "translation_tr", "antibiyotikler", "antibiyotik", WHY),
    (12684, "translation_pl", "antybiotyki", "antybiotyk", WHY),
    # 12689 die Komplikation
    (12689, "translation_en", "complications, difficulties",
     "complication, difficulty", WHY),
    (12689, "translation_ru", "осложнения, трудности",
     "осложнение, трудность", WHY),
    (12689, "translation_uk", "ускладнення, труднощі",
     "ускладнення, трудність", WHY),
    (12689, "translation_tr", "komplikasyonlar, zorluklar",
     "komplikasyon, zorluk", WHY),
    (12689, "translation_pl", "powikłania, komplikacje, trudności",
     "powikłanie, komplikacja, trudność", WHY),
    # 12831 das Genitale
    (12831, "translation_en", "genitals, genitalia",
     "genital, genital organ", WHY),
    (12831, "translation_ru", "половые органы, генитали",
     "половой орган", WHY),
    (12831, "translation_uk", "статеві органи, геніталії",
     "статевий орган", WHY),
    (12831, "translation_tr", "cinsel organlar, genital organlar",
     "cinsel organ, genital organ", WHY),
    (12831, "translation_pl", "narządy płciowe, genitalia",
     "narząd płciowy", WHY),
    # 12916 das Antidepressivum
    (12916, "translation_en", "antidepressants", "antidepressant", WHY),
    (12916, "translation_ru", "антидепрессанты", "антидепрессант", WHY),
    (12916, "translation_uk", "антидепресанти", "антидепресант", WHY),
    (12916, "translation_tr", "antidepresanlar", "antidepresan", WHY),
    (12916, "translation_pl", "antydepresanty, leki przeciwdepresyjne",
     "antydepresant, lek przeciwdepresyjny", WHY),
    # 14092 die Initiale
    (14092, "translation_en", "initials", "initial, initial letter", WHY),
    (14092, "translation_ru", "инициалы, начальные буквы",
     "инициал, начальная буква", WHY),
    (14092, "translation_uk", "ініціали, початкові літери",
     "ініціал, початкова літера", WHY),
    (14092, "translation_tr", "baş harfler, isim baş harfleri",
     "baş harf, isim baş harfi", WHY),
    (14092, "translation_pl", "inicjały, początkowe litery",
     "inicjał, początkowa litera", WHY),
    # 14683 der Mythos
    (14683, "translation_en", "myths, legends", "myth, legend", WHY),
    (14683, "translation_ru", "мифы, легенды", "миф, легенда", WHY),
    (14683, "translation_uk", "міфи, легенди", "міф, легенда", WHY),
    (14683, "translation_tr", "mitler, efsaneler", "mit, efsane", WHY),
    (14683, "translation_pl", "mity, legendy", "mit, legenda", WHY),
    # 14741 die Katakombe
    (14741, "translation_en", "catacombs, underground tombs",
     "catacomb, underground tomb", WHY),
    (14741, "translation_ru", "катакомбы, подземелья",
     "катакомба, подземелье", WHY),
    (14741, "translation_uk", "катакомби, підземелля",
     "катакомба, підземелля", WHY),
    (14741, "translation_tr", "katakomplar, yeraltı mezarları",
     "katakomp, yeraltı mezarı", WHY),
    (14741, "translation_pl", "katakumby, podziemia",
     "katakumba, podziemie", WHY),
    # 14762 die Saite
    (14762, "translation_en", "strings", "string", WHY),
    (14762, "translation_ru", "струны", "струна", WHY),
    (14762, "translation_uk", "струни", "струна", WHY),
    (14762, "translation_tr", "teller, saz telleri", "tel, saz teli", WHY),
    (14762, "translation_pl", "struny", "struna", WHY),
    # 14793 der Promi
    (14793, "translation_en", "celebrities, stars", "celebrity, star", WHY),
    (14793, "translation_ru", "знаменитости, звёзды",
     "знаменитость, звезда", WHY),
    (14793, "translation_uk", "знаменитості, зірки",
     "знаменитість, зірка", WHY),
    (14793, "translation_tr", "ünlüler, yıldızlar", "ünlü, yıldız", WHY),
    (14793, "translation_pl", "celebryci, gwiazdy",
     "celebryta, gwiazda", WHY),
    # 14797 die Hieroglyphe
    (14797, "translation_en", "hieroglyphs, hieroglyphics",
     "hieroglyph", WHY),
    (14797, "translation_ru", "иероглифы, непонятные знаки",
     "иероглиф, непонятный знак", WHY),
    (14797, "translation_uk", "ієрогліфи, незрозумілі знаки",
     "ієрогліф, незрозумілий знак", WHY),
    (14797, "translation_tr", "hiyeroglifler, anlaşılmaz işaretler",
     "hiyeroglif, anlaşılmaz işaret", WHY),
    (14797, "translation_pl", "hieroglify, niezrozumiałe znaki",
     "hieroglif, niezrozumiały znak", WHY),
    # 15152 der Mitmensch
    (15152, "translation_en",
     "fellow human beings, fellow people, those around us",
     "fellow human being, fellow person, someone around us", WHY),
    (15152, "translation_ru", "окружающие, люди вокруг, ближние",
     "ближний, человек рядом, окружающий человек", WHY),
    (15152, "translation_uk", "оточуючі, люди навколо, близькі",
     "близький, людина поряд, людина з оточення", WHY),
    (15152, "translation_tr",
     "etrafımızdaki insanlar, diğer insanlar, yakın çevre",
     "etrafımızdaki insan, diğer insan, yakın çevreden biri", WHY),
    (15152, "translation_pl", "bliźni, inni ludzie, otoczenie",
     "bliźni, inny człowiek, osoba z otoczenia", WHY),
    # 15808 das Reptil
    (15808, "translation_en", "reptiles", "reptile", WHY),
    (15808, "translation_ru", "рептилии, пресмыкающиеся",
     "рептилия, пресмыкающееся", WHY),
    (15808, "translation_uk", "рептилії, плазуни", "рептилія, плазун", WHY),
    (15808, "translation_tr", "sürüngenler", "sürüngen", WHY),
    (15808, "translation_pl", "gady, płazy i gady", "gad", WHY),
    # 16429 das Indiz
    (16429, "translation_en", "circumstantial evidence, clues",
     "clue, piece of circumstantial evidence", WHY),
    (16429, "translation_ru", "улики, косвенные доказательства",
     "улика, косвенное доказательство", WHY),
    (16429, "translation_uk", "непрямі докази, побічні докази",
     "непрямий доказ, побічний доказ", WHY),
    (16429, "translation_tr", "deliller, emareler", "delil, emare", WHY),
    (16429, "translation_pl", "poszlaki, dowody poszlakowe",
     "poszlaka, dowód poszlakowy", WHY),
    # 16528 die Richtlinie
    (16528, "translation_en", "guidelines, directives",
     "guideline, directive", WHY),
    (16528, "translation_ru",
     "директивы, указания, предписания, руководящие принципы",
     "директива, указание, предписание, руководящий принцип", WHY),
    (16528, "translation_uk", "директиви, вказівки, рекомендації",
     "директива, вказівка, рекомендація", WHY),
    (16528, "translation_tr", "yönergeler, direktifler, ilkeler",
     "yönerge, direktif, ilke", WHY),
    (16528, "translation_pl", "wytyczne, dyrektywy, zalecenia",
     "wytyczna, dyrektywa, zalecenie", WHY),
    # 16739 die Bestimmung
    (16739, "translation_en", "provisions, regulations, rules",
     "provision, regulation, rule", WHY),
    (16739, "translation_ru", "положения, правила, предписания, нормы",
     "положение, правило, предписание, норма", WHY),
    (16739, "translation_uk", "положення, правила, приписи, норми",
     "положення, правило, припис, норма", WHY),
    (16739, "translation_tr", "hükümler, kurallar, şartlar",
     "hüküm, kural, şart", WHY),
    (16739, "translation_pl", "przepisy, postanowienia, regulacje",
     "przepis, postanowienie, regulacja", WHY),
    # 16817 der Anklagepunkt
    (16817, "translation_en", "charges, counts of indictment",
     "charge, count of indictment", WHY),
    (16817, "translation_ru", "пункты обвинения, обвинения",
     "пункт обвинения, обвинение", WHY),
    (16817, "translation_uk", "пункти звинувачення, звинувачення",
     "пункт звинувачення, звинувачення", WHY),
    (16817, "translation_tr", "suçlamalar, iddianame maddeleri",
     "suçlama, iddianame maddesi", WHY),
    (16817, "translation_pl", "zarzuty, punkty oskarżenia",
     "zarzut, punkt oskarżenia", WHY),
    # 16889 die Befugnis
    (16889, "translation_en", "powers, authority, competence",
     "power, authority, competence", WHY),
    (16889, "translation_ru", "полномочия, права, компетенция",
     "полномочие, право, компетенция", WHY),
    (16889, "translation_uk", "повноваження, права, компетенція",
     "повноваження, право, компетенція", WHY),
    (16889, "translation_tr", "yetkiler, yetki alanı, izinler",
     "yetki, yetki alanı, izin", WHY),
    (16889, "translation_pl",
     "uprawnienia, kompetencje, pełnomocnictwo",
     "uprawnienie, kompetencja, pełnomocnictwo", WHY),
    # 16922 die Gräueltat
    (16922, "translation_en", "atrocities", "atrocity", WHY),
    (16922, "translation_ru", "зверства, злодеяния",
     "зверство, злодеяние", WHY),
    (16922, "translation_uk", "звірства, злодіяння",
     "звірство, злодіяння", WHY),
    (16922, "translation_tr", "zulümler, vahşetler", "zulüm, vahşet", WHY),
    (16922, "translation_pl", "okrucieństwa, zbrodnie",
     "okrucieństwo, zbrodnia", WHY),
    # 17335 die Sehenswürdigkeit
    (17335, "translation_en", "sights, attractions, landmarks",
     "sight, attraction, landmark", WHY),
    (17335, "translation_ru", "достопримечательности",
     "достопримечательность", WHY),
    (17335, "translation_uk", "визначні місця, пам'ятки",
     "визначне місце, пам'ятка", WHY),
    (17335, "translation_tr",
     "gezilecek yerler, görülmeye değer yerler, turistik yerler",
     "gezilecek yer, görülmeye değer yer, turistik yer", WHY),
    (17335, "translation_pl", "atrakcje turystyczne, zabytki",
     "atrakcja turystyczna, zabytek", WHY),
    # 17743 der Spezialeffekt
    (17743, "translation_en", "special effects", "special effect", WHY),
    (17743, "translation_ru", "спецэффекты, специальные эффекты",
     "спецэффект, специальный эффект", WHY),
    (17743, "translation_uk", "спецефекти, спеціальні ефекти",
     "спецефект, спеціальний ефект", WHY),
    (17743, "translation_tr", "özel efektler", "özel efekt", WHY),
    (17743, "translation_pl", "efekty specjalne", "efekt specjalny", WHY),
    # 17834 das Gut
    (17834, "translation_en", "goods, freight, assets, estates",
     "good, freight, asset, estate", WHY),
    (17834, "translation_ru", "товары, грузы, блага, имения",
     "товар, груз, благо, имение", WHY),
    (17834, "translation_uk", "товари, вантажі, блага, маєтки",
     "товар, вантаж, благо, маєток", WHY),
    (17834, "translation_tr", "mallar, yük, varlıklar, çiftlikler",
     "mal, yük, varlık, çiftlik", WHY),
    (17834, "translation_pl", "towary, ładunki, dobra, majątki",
     "towar, ładunek, dobro, majątek", WHY),
    # 17885 die Kondition
    (17885, "translation_en", "terms, conditions, rates",
     "term, condition, rate", WHY),
    (17885, "translation_ru", "условия, условия сделки, расценки",
     "условие, условие сделки, расценка", WHY),
    (17885, "translation_uk", "умови, умови угоди, розцінки",
     "умова, умова угоди, розцінка", WHY),
    (17885, "translation_tr", "şartlar, koşullar, fiyat koşulları",
     "şart, koşul, fiyat koşulu", WHY),
    (17885, "translation_pl", "warunki, warunki umowy, stawki",
     "warunek, warunek umowy, stawka", WHY),
    # 18082 die Messung
    (18082, "translation_en", "measurements, readings",
     "measurement, reading", WHY),
    (18082, "translation_ru",
     "измерения, замеры, результаты измерений",
     "измерение, замер, результат измерения", WHY),
    (18082, "translation_uk",
     "вимірювання, заміри, результати вимірювань",
     "вимірювання, замір, результат вимірювання", WHY),
    (18082, "translation_tr", "ölçümler, ölçüm sonuçları",
     "ölçüm, ölçüm sonucu", WHY),
    (18082, "translation_pl", "pomiary, wyniki pomiarów",
     "pomiar, wynik pomiaru", WHY),
    # 18083 die Vibration
    (18083, "translation_en", "vibrations, tremors",
     "vibration, tremor", WHY),
    (18083, "translation_ru", "вибрации, дрожание, колебания",
     "вибрация, дрожание, колебание", WHY),
    (18083, "translation_uk", "вібрації, дрижання, коливання",
     "вібрація, дрижання, коливання", WHY),
    (18083, "translation_tr", "titreşimler, sarsıntılar",
     "titreşim, sarsıntı", WHY),
    (18083, "translation_pl", "wibracje, drgania",
     "wibracja, drganie", WHY),
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

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
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
