"""ВТОРОЙ ПРОХОД, блок 17 (ряды 3201–3400) + НОВЫЙ ГЕЙТ.

РЯД, КОТОРЫЙ ДАЛ ГЕЙТ. `entgehen` (7021), украинский список переводов:

    «уникнути, ускользнути, пройти мимо увагиь»

Три дефекта в одной ячейке: русское слово «ускользнути» с украинским
окончанием, русская фраза «пройти мимо» и «увагиь» — слово, которого
нет ни в одном языке.

`scan_ru_in_uk` этого не видела, и не по недосмотру, а ПО УСТРОЙСТВУ:
она сравнивает корпуса, ищет слово, частое в русских ячейках и
однократное в украинских. «ускользнути» — гибрид, его нет НИ В ОДНОМ
корпусе, частота ноль с двух сторон. Примета по частоте гибрид не
найдёт никогда.

Зато у «увагиь» есть признак ОРФОГРАФИЧЕСКИЙ: мягкий знак после
гласной невозможен ни в русском, ни в украинском. Это проверка буквы, а
не слова, поэтому годится в гейты. Написан `scan_soft_sign`.

ПЕРВАЯ ВЕРСИЯ ГЕЙТА ДАЛА 658 ПОПАДАНИЙ И ВСЕ ЛОЖНЫЕ. Я применил
украинское правило к русскому: в украинском «ь» после г/к/х/ж/ч/ш/щ
невозможен, а в русском он нормален и очень част — «ночь», «помощь»,
«хочешь», «печь». Правила разведены по языкам, и обе половины стоят в
самопроверке. По базе после этой правки — ноль.

ЕЩЁ ОДИН РУСИЗМ В СПИСКЕ, который приметa тоже не видит: `überwinden`
(10432), украинский список «подолати, перемогти, **превзойти**».
Частота «превзойти» в русских ячейках ниже порога шести, то есть слово
редкое с обеих сторон — та же дыра, что у гибрида.

ЧЕТВЁРТЫЙ БЛОК ПОДРЯД С ПОДМЕНЁННЫМ ПРЕДЛОЖЕНИЕМ:

    ablegen (1104)    de «Du kannst den Mantel ablegen»
        tr «Sınavı başarıyla verdi» — про экзамен, а не про пальто
    anzeigen (16126)  de «Ich werde ihn bei der Polizei anzeigen»
        ru «Сосед донёс на нас в полицию» — другое лицо и другие люди
    erfinden (9474)   de «Mein Sohn kann tolle Geschichten erfinden»
        en «Who invented the wheel», tr «Tekerleği kim icat etti»,
        uk «Він вигадав смішну історію для дітей» — три языка, и все
        три по-разному
    Pop (14453)       uk и tr про популярность поп-музыки в странах,
        а эталон про то, что это музыкальное направление
    Dankbarkeit (10427) tr «Ona minnettarlığımı ... gösterdim» —
        подменено лицо: «я ему», а эталон «она свою»

ДЫРА В ПОЛЬСКОЙ ПОЛОВИНЕ ПРИМЕТЫ НА РОД. `schockiert` (10431) по-польски
«Jestem zszokowanA» — женский род, а русский и украинский мужские.
Польская половина `scan_speaker_gender` смотрит только глагольное
«-łam», а прилагательных не видела.

Замер: «jestem/czuję się» плюс женское прилагательное даёт 4 попадания
против 114 мужских — мужской род норма базы, как и записано. Из четырёх
два ложных (родительный «Berlina», глагол «odjeżdża»), один настоящий
(10431) и **один трогать нельзя**: `geborgen` (10862), где немецкое
«in seinen Armen» само ставит рассказчицу женщиной, и русский с
украинским там согласованно женские. Это тот же случай, что
`Vegetarierin` в блоке 8, и предупреждение в приметe сработало.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ ГЕЙТ: невозможный знак и русизмы в списках ════════════════
    (7021, "translation_uk",
     "уникнути, ускользнути, пройти мимо увагиь",
     "уникнути, прослизнути, пройти поза увагою",
     "«увагиь» слова нет, «ускользнути» гибрид, «пройти мимо» русское"),
    (7021, "example_uk",
     "Це не має мені втекти",
     "Це не повинно пройти поза моєю увагою",
     "«втекти» это убежать; entgehen — ускользнуть от внимания"),
    (7021, "example_tr",
     "Bunun benden kaçması gerekmiyor",
     "Bunun gözümden kaçmaması gerekiyor",
     "перевод сказал «не обязательно», а эталон «не должно»"),
    (10432, "translation_uk",
     "подолати, перемогти, превзойти",
     "подолати, перемогти, перевершити",
     "«превзойти» русское; частота ниже порога scan_ru_in_uk"),
    (10432, "example_tr",
     "Korkmamı yenmem gerekiyor",
     "Korkumu yenmem gerekiyor",
     "«korkmamı» значит «моё не-боящееся»; нужно «korkumu»"),

    # ══ КЛАСС: подменённое предложение ═══════════════════════════
    (1104, "example_tr",
     "Sınavı başarıyla verdi",
     "Paltonu çıkarabilirsin",
     "подмена: эталон «Du kannst den Mantel ablegen»"),
    (16126, "example_ru",
     "Сосед донёс на нас в полицию",
     "Я заявлю на него в полицию",
     "подмена лица и людей: эталон «Ich werde ihn ... anzeigen»"),
    (9474, "example_en",
     "Who invented the wheel",
     "My son can make up great stories",
     "подмена: эталон про сына, а не про колесо"),
    (9474, "example_tr",
     "Tekerleği kim icat etti",
     "Oğlum harika hikayeler uydurabiliyor",
     "то же"),
    (9474, "example_uk",
     "Він вигадав смішну історію для дітей",
     "Мій син вміє вигадувати чудові історії",
     "то же, и ещё третья своя фраза"),
    (14453, "example_uk",
     "Поп-музика популярна в усіх країнах",
     "Поп — популярний музичний напрям",
     "подмена: эталон «Pop ist eine beliebte Musikrichtung»"),
    (14453, "example_tr",
     "Pop müzik tüm ülkelerde popülerdir",
     "Pop popüler bir müzik türüdür",
     "то же"),
    (10427, "example_tr",
     "Ona minnettarlığımı küçük bir hediyeyle gösterdim",
     "Minnettarlığını bir hediyeyle gösterdi",
     "подменено лицо: «я ему», а эталон «она свою»"),

    # ══ род рассказчика: дыра в польской половине приметы ════════
    (10431, "example_pl",
     "Jestem zszokowana jego słowami",
     "Jestem zszokowany jego słowami",
     "женский род при мужском в ru и uk; база по умолчанию мужская"),

    # ══ формы, которых в языке нет ═══════════════════════════════
    (16123, "example_uk",
     "Страта було жахливою подією",
     "Страта була жахливою подією",
     "«страта» женского рода: «була»"),
    (7026, "example_tr",
     "Köpek kızgın olduğunda homurtur",
     "Köpek kızgın olduğunda hırlıyor",
     "«homurtur» не форма; и у собаки это «hırlamak»"),
    (13988, "example_uk",
     "Дай мені взяватися за цю проблему",
     "Дай мені взятися за цю проблему",
     "«взяватися» не слово"),
    (13988, "example_tr",
     "Bırak bu soruna başa çıkayım",
     "Bırak bu sorunla başa çıkayım",
     "«başa çıkmak» требует орудного: «sorunla»"),
    (10433, "example_uk",
     "Я прокльнав мою невдачу",
     "Я проклинав своє невезіння",
     "«прокльнав» не форма, и «мою» вместо «своє»"),
    (10433, "example_tr",
     "Şansızlığımı lanetledim",
     "Şanssızlığımı lanetledim",
     "«şansızlık» пишется с двумя «s»"),
    (7013, "example_tr",
     "Tam adresi gerekli",
     "Tam adrese ihtiyacım var",
     "«adresi gerekli» не согласовано"),
    (7052, "example_tr",
     "Dolu çanta taşımak çok zordu",
     "Dolu çantayı taşımak çok zordu",
     "нужен винительный: «çantayı»"),
    (7044, "example_tr",
     "Onun elini çok hafifçe değdi",
     "Onun eline çok hafifçe değdi",
     "«değmek» требует дательного: «eline»"),
    (10428, "example_tr",
     "Bana şiddetle tehdit ediyor",
     "Beni şiddet kullanmakla tehdit ediyor",
     "«tehdit etmek» требует винительного, и «şiddetle» это «резко»"),

    # ══ слово не из своего списка и не то слово ══════════════════
    (18192, "example_tr",
     "Pencerenin kafesi var",
     "Pencerenin parmaklığı var",
     "«kafes» это клетка; Gitter — «parmaklık», и оно первое в списке"),
    (7028, "example_tr",
     "Müdahaleleri kovmalıyız",
     "İşgalcileri kovmalıyız",
     "«müdahale» это вмешательство, а Eindringling — захватчик"),
    (15025, "example_tr",
     "Eski arkadaşımla buluşmam gerçekten güzeldi",
     "Eski arkadaşımla karşılaşmam gerçekten güzeldi",
     "«buluşma» это условленная встреча, а Begegnung — случайная"),
    (7040, "example_tr",
     "Duvara dikkatle bakıyordu",
     "Duvara dik dik bakıyordu",
     "«dikkatle» это внимательно, а starren — уставиться"),
    (7047, "example_tr",
     "Daha iyi notlar almak için çalışıyorum",
     "Daha iyi notlar almak için çabalıyorum",
     "«çalışmak» это работать; bemühen — «çabalamak»"),
    (10448, "example_uk",
     "Шкода, що матч скасували",
     "Яка досада, що матч скасували",
     "«шкода» нет в списке переводов, а «досада» стоит первой"),
    (15488, "example_uk",
     "Павук плете свою сітку",
     "Павук плете свою павутину",
     "«сітка» это сеть; в списке «павутину»"),
    (15024, "example_pl",
     "Jego życie prywatne jest bardzo tajemnicze",
     "Jego życie prywatne jest bardzo tajne",
     "«tajemnicze» это загадочное, а geheim — тайное"),
    (7048, "example_tr",
     "Hızlı gitmemiz gerekiyor yoksa treni kaçıracağız",
     "Hızlıca gitmemiz gerekiyor yoksa treni kaçıracağız",
     "нужно наречие: «hızlıca» стоит в списке первым"),

    # ══ эталон: слитное написание ════════════════════════════════
    (11702, "example_de",
     "Wir treffen uns in unserem Lieblings-Lokal",
     "Wir treffen uns in unserem Lieblingslokal",
     "«Lieblingslokal» пишется слитно"),

    # ══ время и вид глагола ══════════════════════════════════════
    (16122, "example_tr",
     "Ordu şehri fethetti",
     "Ordu şehri fethediyor",
     "прошедшее против «erobert»; в остальных четырёх настоящее"),

    # ══ потерянное слово ═════════════════════════════════════════
    (2498, "example_en",
     "I guarantee you that",
     "I guarantee you that this works",
     "потеряно «dass das funktioniert»"),
    (2498, "example_uk",
     "Я тобі це гарантую",
     "Я гарантую тобі, що це працює",
     "то же"),
    (2498, "example_tr",
     "Sana bunu garanti ederim",
     "Bunun işe yaradığını sana garanti ederim",
     "то же"),
    (9473, "example_uk",
     "Можеш прочитати мені листа?",
     "Можеш прочитати мені листа вголос?",
     "потеряно «vorlesen»: читать ВСЛУХ"),
    (9473, "example_tr",
     "Mektubu bana okuyabilir misin?",
     "Mektubu bana sesli okuyabilir misin?",
     "то же"),
    (9473, "example_en",
     "Can you read the letter to me?",
     "Can you read the letter aloud to me?",
     "то же"),
    (258, "example_uk",
     "У лютому холодно й багато снігу",
     "У лютому часто холодно й багато снігу",
     "потеряно «oft»: в остальных четырёх оно есть"),
    (13992, "example_uk",
     "Ми балакали про давні часи",
     "Ми приємно балакали про давні часи",
     "потеряно «gemütlich»: в ru и pl оно есть"),

    # ══ добавленное слово ════════════════════════════════════════
    (10419, "example_ru",
     "Ты действительно очень мнительный",
     "Ты действительно мнительный",
     "«очень» в эталоне «Du bist wirklich paranoid» нет"),
    (7014, "example_uk",
     "Видатки були розділені порівну",
     "Видатки були розділені",
     "«порівну» в эталоне «Die Kosten wurden geteilt» нет"),
    (7014, "example_tr",
     "Masraflar eşit olarak paylaştırıldı",
     "Masraflar paylaştırıldı",
     "то же"),

    # ══ управление и порядок слов ════════════════════════════════
    (7037, "example_ru",
     "Они держатся друг друга, что бы ни случилось",
     "Они держатся друг за друга, что бы ни случилось",
     "«держаться друг за друга», а не «друг друга»"),
    (15029, "example_uk",
     "Моя партнерка і я маємо великі плани на майбутнє",
     "Ми з моєю партнеркою маємо великі плани на майбутнє",
     "по-украински «ми з», а не «я і»; в ru так и написано"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
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
