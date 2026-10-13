"""ВТОРОЙ ПРОХОД, блок 36 (ряды 7001–7200): 43 правки.

НАБЛЮДЕНИЕ ПРОШЛОГО БЛОКА ПОДТВЕРДИЛОСЬ С ПЕРВОГО РАЗА. В HANDOVER
после блока 35 записано: «в блоке с одной польской подменой стоит искать
ещё». Здесь польских подмен снова тринадцать, то есть две полосы подряд:

    obendrein    (7752)  «SPÓŹNIŁ SIĘ i w dodatku ZAPOMNIAŁ KLUCZY»
    Antlitz     (15164)  «JEJ oblicze ROZJAŚNIŁ UŚMIECH»
    Zuversicht  (10978)  «PATRZY W PRZYSZŁOŚĆ z ufnością»
    Mast        (17244)  «Na maszcie łodzi WISI FLAGA»
    Steroid     (12810)  «Brał sterydy PRZED ZAWODAMI»
    ergehen      (7756)  «Jak ci się powodzi W NOWEJ PRACY?»
    telefonisch (14161)  «MOŻNA SIĘ ZAPISAĆ telefonicznie»
    Ohrfeige    (10973)  «Dostał policzek ZA SWOJE BEZCZELNE SŁOWA»
    stolpern     (7749)  «POTKNĄŁEM SIĘ» вместо «Er stolperte»
    Mixer       (18323)  потеряно «endlich» и «smoothie»
    hinführen    (7744)  «TA ROZMOWA» вместо «Die Diskussion»
    niederbrennen(16488) потеряно «до основания»
    zuteil       (7738)  потеряно «für seine Arbeit»

Приём работает: достаточно найти в блоке одну польскую подмену, чтобы
стоило перечитать все польские ячейки блока отдельно. Так и сделано.

ЕЩЁ ДВА ЧИСЛА СЛОВАМИ ПРОТИВ ЦИФР, И ОБА В ПОЛЬСКОМ:

    Radius (17992)  pl «pięć centymetrów» против «5 Zentimeter»
    Quote  (17828)  pl «trzydzieści procent» против «30 Prozent»

`scan_number_mismatch` этого не видит: она сравнивает ЦИФРЫ, а здесь
цифра заменена словом, и сравнивать нечего. Предел приметы назван в ней
самой; класс тот же, что в `Kaufmann` (блок 32).
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: польская полоса подмен, вторая подряд ════════════
    (7752, "example_pl",
     "Spóźnił się i w dodatku zapomniał kluczy",
     "Jedzenie było złe i w dodatku za drogie",
     "подмена: опоздал и забыл ключи вместо «Das Essen war schlecht»"),
    (15164, "example_pl",
     "Jej oblicze rozjaśnił uśmiech",
     "Jego poważne oblicze wyrażało głęboki smutek",
     "подмена: улыбка вместо «ernstes Antlitz drückte tiefe Trauer aus»"),
    (10978, "example_pl",
     "Patrzy w przyszłość z ufnością",
     "Działał z wielką ufnością",
     "подмена: смотрит в будущее вместо «Er handelte»"),
    (17244, "example_pl",
     "Na maszcie łodzi wisi flaga",
     "Maszt statku był imponująco wysoki",
     "подмена: флаг на мачте вместо «war beeindruckend hoch»"),
    (12810, "example_pl",
     "Brał sterydy przed zawodami",
     "Brał sterydy, żeby szybciej budować mięśnie",
     "подмена: перед соревнованиями вместо «um Muskeln aufzubauen»"),
    (7756, "example_pl",
     "Jak ci się powodzi w nowej pracy?",
     "Jak ci się powodzi?",
     "«w nowej pracy» в эталоне «Wie ergeht es dir?» нет"),
    (14161, "example_pl",
     "Można się zapisać telefonicznie",
     "Jestem dostępny telefonicznie",
     "подмена: запись по телефону вместо «Ich bin telefonisch erreichbar»"),
    (10973, "example_pl",
     "Dostał policzek za swoje bezczelne słowa",
     "Dostał policzek, bo był zbyt bezczelny",
     "подмена: за слова вместо «weil er zu frech war»"),
    (7749, "example_pl",
     "Potknąłem się o korzeń i upadłem",
     "Potknął się o korzeń i upadł",
     "первое лицо против «Er stolperte»"),
    (18323, "example_pl",
     "Mikser znowu działa, zrobię koktajl",
     "Mikser w końcu znowu działa, mogę zrobić smoothie",
     "потеряно «wieder/endlich» и «Smoothie»"),
    (7744, "example_pl",
     "Ta rozmowa doprowadziła nas do rozwiązania",
     "Dyskusja powoli doprowadziła nas do rozwiązania",
     "«rozmowa» вместо «Diskussion», и потеряно «langsam»"),
    (16488, "example_pl",
     "Chcieli spalić całą wioskę",
     "Chcieli spalić całą wioskę do fundamentów",
     "потеряно «nieder-»: сжечь ДОТЛА"),
    (7738, "example_pl",
     "Przypadła mu w udziale wielka pochwała",
     "Przypadła mu w udziale wielka pochwała za jego pracę",
     "потеряно «für seine Arbeit»"),

    # ══ число словами вместо цифры ══════════════════════════════
    (17992, "example_pl",
     "Promień tego koła to pięć centymetrów",
     "Promień tego koła to 5 centymetrów",
     "число словами против «5 Zentimeter»; примета сравнивает цифры"),
    (17828, "example_pl",
     "Wskaźnik wynosi trzydzieści procent",
     "Wskaźnik wynosi 30 procent",
     "то же, против «30 Prozent»"),

    # ══ подмена в других языках ═════════════════════════════════
    (14628, "example_tr",
     "Film çok güzel bir aşk hikâyesi",
     "Aşk hikâyesi çok dokunaklıydı",
     "подмена: «фильм — красивая история» вместо «war sehr rührend»"),
    (14628, "example_pl",
     "To była piękna historia miłosna",
     "Historia miłosna była bardzo wzruszająca",
     "«piękna» вместо «rührend»"),
    (15665, "example_tr",
     "Yazın Alpler'de yürüyüşe çıktık",
     "Alpler çok güzel bir sıradağ",
     "подмена: поход летом вместо «sind ein wunderschönes Gebirge»"),
    (7756, "example_en",
     "How did you fare on the exam?",
     "How are you faring?",
     "подмена: экзамен в эталоне «Wie ergeht es dir?» не упомянут"),
    (16494, "example_uk",
     "Після аварії водій втік з місця аварії",
     "Аварія була явною втечею з місця ДТП",
     "перестроено, и «аварія» дважды в одной фразе"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (12802, "example_uk",
     "У мене на балконі всі рослини подохли",
     "У мене на балконі всі рослини поздихали",
     "«подохли» русское; по-украински «поздихали»"),
    (7757, "example_uk",
     "Ковзани ковзають по льду",
     "Ковзани ковзають по льоду",
     "«по льду» русское; по-украински «по льоду»"),
    (12812, "example_uk",
     "Рибна кістка його давить, він з трудом дихає",
     "Риб'яча кістка його душить, він ледве дихає",
     "«з трудом» русизм, и «давить» вместо «душить»"),
    (17628, "example_uk",
     "Можна ще раз включити пісню?",
     "Можна ще раз увімкнути пісню?",
     "«включити» русизм; по-украински «увімкнути»"),
    (12280, "example_uk",
     "Команда розпочинає наступ у останній чверті гри",
     "Команда розпочинає наступ в останній чверті",
     "«у останній» не форма, и «гри» в эталоне нет"),
    (7751, "translation_uk",
     "бездоганний, безукоризненний, ідеальний",
     "бездоганний, досконалий, ідеальний",
     "«безукоризненний» русизм; по-украински «досконалий»"),
    (2431, "example_pl",
     "Dowiaduję się o cenę",
     "Dowiaduję się o cenie",
     "«dowiadywać się o» требует местного падежа"),
    (14159, "example_pl",
     "Blefuje przy pokerze",
     "Blefuje w pokerze",
     "«przy pokerze» не оборот: «w pokerze»"),
    (12279, "example_tr",
     "Senin tarafından çok akıllı bir hamlesi vardı",
     "Senin yaptığın çok akıllı bir hamleydi",
     "фраза не согласована: «hamlesi vardı» при «senin tarafından»"),
    (16494, "example_tr",
     "Kaza açık bir kaçak sürücü olayıydı",
     "Kaza açık bir kaza yapıp kaçma olayıydı",
     "«kaçak sürücü» не оборот; в списке «kaza yapıp kaçma»"),
    (9053, "example_tr",
     "Mağazadaki satış danışmanı çok dosttu ve yardımseverdi",
     "Mağazadaki kadın satıcı çok cana yakın ve yardımseverdi",
     "«dosttu» не форма, и потерян женский род из списка"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (18322, "example_tr",
     "Çöp, sokağa değil çöp kutusuna atılmalı",
     "Çöp, sokağa değil çöp kovasına atılmalı",
     "«çöp kutusu» нет в списке, а «çöp kovası» стоит первым"),
    (7746, "example_ru",
     "Шторм разрушил всё с полной силой",
     "Буря разрушила всё с полной силой",
     "«шторм» о море; `Sturm` на земле — буря, и так в uk, tr, pl и en"),
    (16493, "example_ru",
     "Свидетель должен был пойти на полицейский участок",
     "Свидетель должен был пойти в полицейский участок",
     "в участок ходят, а не на участок"),
    (9053, "example_uk",
     "Продавщиця у магазині була дуже дружелюбна й допомагала",
     "Продавчиня у магазині була дуже дружелюбна й готова допомогти",
     "«продавчиня» стоит в списке первым, и «hilfsbereit» это готовность"),
    (14164, "example_uk",
     "Будь ласка, поставте тут свій підпис",
     "Будь ласка, постав тут свій підпис",
     "вежливое множественное против «unterschreib»"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (2858, "example_uk",
     "Працівники страйкують",
     "Працівники страйкують за кращі умови праці",
     "потеряно «für bessere Arbeitsbedingungen»"),
    (12807, "example_pl",
     "Babcia mieszka teraz w domu starców",
     "Moja babcia mieszka teraz w domu starców",
     "потеряно «Meine»"),
    (12807, "example_tr",
     "Büyükanne artık bir yaşlı bakım evinde yaşıyor",
     "Büyükannem artık bir yaşlı bakım evinde yaşıyor",
     "то же"),
    (17628, "example_en",
     "Can we play the song again, I really like it?",
     "Can we play the song again?",
     "вторая половина в эталоне не упомянута"),
    (17628, "example_tr",
     "Lütfen şarkıyı tekrar çalabilir miyiz?",
     "Şarkıyı tekrar çalabilir miyiz?",
     "«lütfen» в эталоне нет"),
    (7763, "example_en",
     "The stars shine brightly at night",
     "The stars shine at night",
     "«brightly» в эталоне «glänzen in der Nacht» нет"),
    (7763, "example_tr",
     "Yıldızlar gece parlak bir şekilde parıldıyor",
     "Yıldızlar gece parıldıyor",
     "то же"),
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
            print(f"id={wid} {col}")
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
