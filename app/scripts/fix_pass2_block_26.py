"""ВТОРОЙ ПРОХОД, блок 26 (ряды 5001–5200): 60 правок.

РЯД, КОТОРЫЙ ВЗЯЛ ПЕРЕВОДЫ У СОСЕДА. Главная находка блока:

    Falke    (15562)  en «falcon, hawk»  ru «сокол»  uk «сокіл»
    Schnecke (15563)  en «falcon, hawk»  ru «сокол»  uk «сокіл»

У улитки все пять списков от сокола, и артикль тоже чужой — «der» вместо
«die». А примеры свои и верные: «Улитка медленно движется по дорожке».
Человеку показывали «сокол», произносили «сокол» и давали фразу про
улитку. Идентификаторы соседние: списки съехали на один ряд.

Это стало поводом замерить класс по базе, и замер дал два урока.

Первый: «одинаковые списки» — не примета. Таких групп 41, и сорок из них
законны, потому что синонимы и формы обязаны переводиться одинаково:
`Krankenhaus`/`Spital`, `Möhre`/`Karotte`, `Pyjama`/`Schlafanzug`,
`Fotograf`/`Fotograf/in`, `dritte`/`dritter`. Отличает дефект не
совпадение списков, а то, что немецкие слова не синонимы, — а это формально
не проверяется.

Второй, он же находка в рабочем коде: проверять надо не совпадение
списков, а то, встречается ли слово списка в своём примере. И когда это
замерили, выяснилось, что мешает само сравнение основ в `main_meaning`:
при `_STEM_MIN = 4` у четырёхбуквенного слова падежное окончание съедает
нужную четвёртую букву. «шина» и «шину» считались разными словами.
Из-за этого карточки показывали не то значение, что в примере:

    Schiene (17316)  ru показывала «рельс», пример про шину на руке
    Messe    (7057)  uk показывала «виставка», пример про месу в церкві
    Zelle   (15973)  pl показывала «komórka», пример про камеру в тюрьме
    Asche    (6694)  ru показывала «пепел», пример про золу из камина
    saufen  (11731)  pl показывала «chlać», пример про животных у реки

Добавлена поблажка на одну букву (`_stem_in_loose`), и она исправила 26
таких карточек. Каждое её условие отрезает замеренный ложный случай, а
решать ей позволено только при однозначном попадании — иначе «они» и
«она» становятся одним словом. Подробности в самой функции; три новых
теста закрепляют и поблажку, и её границы.

ДВА РЯДА, ГДЕ НЕВЕРЕН САМ НЕМЕЦКИЙ ЭТАЛОН:

    Arche (14525)  de «Der Triumphbogen hat mehrere Archen»

`Arche` это ковчег, а арка — `Bogen`. Фраза бессмысленна по-немецки, и за
ней ушли английский, русский, турецкий и польский («У триумфальной арки
несколько ковчегов»). Украинский при этом верен сам по себе: «Ной
побудував ковчег перед потопом» — по нему и выровнены остальные пять.

    Güte (10097)  de «Ach du meine Güte»

Это восклицание, и слова списка в нём нет ни в одном языке, кроме
английского, где «goodness» совпало случайно. Карточка обещала «доброта»,
а давала «Ах ты боже мой». Эталон заменён на фразу, где `Güte` — то самое
существительное, что в списке.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ ряд взял переводы и артикль у соседа ════════════════════
    (15563, "article", "der", "die",
     "у улитки артикль сокола; «die Schnecke»"),
    (15563, "translation_en", "falcon, hawk", "snail",
     "список унаследован от соседнего ряда `Falke` (15562)"),
    (15563, "translation_ru", "сокол", "улитка", "то же"),
    (15563, "translation_uk", "сокіл", "равлик", "то же"),
    (15563, "translation_tr", "şahin, doğan", "salyangoz", "то же"),
    (15563, "translation_pl", "sokół", "ślimak", "то же"),

    # ══ неверен сам немецкий эталон ═════════════════════════════
    (14525, "example_de",
     "Der Triumphbogen hat mehrere Archen",
     "Noah baute die Arche vor der Sintflut",
     "`Arche` это ковчег, арка — `Bogen`; фраза бессмысленна"),
    (14525, "example_en",
     "The triumphal arch has several arches",
     "Noah built the ark before the flood",
     "шла за неверным эталоном; выровнено по верному uk"),
    (14525, "example_ru",
     "У триумфальной арки несколько ковчегов",
     "Ной построил ковчег перед потопом",
     "то же"),
    (14525, "example_tr",
     "Zafer kemeri birkaç kemere sahiptir",
     "Nuh tufandan önce gemiyi yaptı",
     "то же"),
    (14525, "example_pl",
     "Łuk triumfalny ma kilka arek",
     "Noe zbudował arkę przed potopem",
     "то же"),

    (10097, "example_de",
     "Ach du meine Güte",
     "Seine Güte hat mich sehr berührt",
     "восклицание не показывало слова списка ни в одном языке, кроме en"),
    (10097, "example_en", "Oh my goodness",
     "His kindness touched me deeply", "то же"),
    (10097, "example_ru", "Ах ты боже мой",
     "Его доброта меня очень тронула", "то же"),
    (10097, "example_uk", "Ах ти Боже мій",
     "Його доброта мене дуже зворушила", "то же"),
    (10097, "example_tr", "Aman Tanrım",
     "İyiliği beni çok etkiledi", "то же"),
    (10097, "example_pl", "O mój Boże",
     "Jego dobroć bardzo mnie wzruszyła", "то же"),

    # ══ слова ряда в примере не было (по примете) ═══════════════
    (16142, "example_en",
     "In the fight there were many injured",
     "In the battle there were many injured",
     "«fight» в списке нет; «battle» стоит первым"),
    (10393, "example_ru",
     "Мне хочется пиццы",
     "Мне охота пиццы",
     "ни одного слова списка; «охота» есть, и разговорность сохранена"),
    (10393, "example_uk",
     "Мені хочеться піци",
     "Маю охоту на піцу",
     "то же"),
    (10393, "example_tr",
     "Canım pizza çekiyor",
     "Pizzaya hevesim var",
     "то же; «heves» есть в списке"),
    (12897, "example_ru",
     "Результат анализа крови был в норме",
     "Заключение по анализу крови было в норме",
     "карточка показывала «заключение», пример говорил «результат»"),
    (12897, "example_uk",
     "Результати аналізу крові були в нормі",
     "Висновок аналізу крові був у нормі",
     "то же"),
    (12897, "example_tr",
     "Kan testi sonuçları normaldi",
     "Kan tahlili sonucu normaldi",
     "то же; «tahlil sonucu» есть в списке, «test» нет"),
    (2553, "example_uk",
     "Я сумую за своєю родиною",
     "У мене туга за домом, за родиною",
     "слова списка не было; в ru так же: «тоска по дому, по семье»"),
    (2553, "example_tr",
     "Ailemi özlüyorum",
     "Ailemin özlemini çekiyorum",
     "слова списка не было: «özlem» это существительное"),
    (2817, "example_tr",
     "Bu mantıklı değil",
     "Bunun bir anlamı yok",
     "ни одного слова списка; «anlam» стоит первым"),
    (2691, "example_tr",
     "Kuruyemiş yemeyi severim",
     "Kabuklu yemiş yemeyi severim",
     "«kuruyemiş» нет в списке, а «kabuklu yemiş» есть"),
    (16307, "example_tr",
     "On yıllık esirlikten sonra sonunda özgür oldu",
     "On yıllık esaretten sonra sonunda özgür oldu",
     "«esirlik» нет в списке, а «esaret» стоит первым"),
    (12689, "example_tr",
     "Cerrahiden sonra komplikasyonlar vardı",
     "Ameliyattan sonra komplikasyonlar vardı",
     "«cerrahi» это хирургия как наука; операция — «ameliyat»"),
    (15095, "example_tr",
     "Yaşlı adam satranç oynamayı seviyor",
     "Yaşlı kişi satranç oynamayı seviyor",
     "«adam» добавляет мужской пол, которого в эталоне нет"),
    (8939, "example_tr",
     "Başkan bir toplantı çağırıyor",
     "Başkan bir toplantıya çağrı yapıyor",
     "«toplantı çağırmak» не турецкий оборот"),
    (14072, "example_ru",
     "Мне нужна справка о режиме работы",
     "Мне нужна информация о часах работы",
     "«справка о режиме работы» это документ, а нужна была информация"),
    (18763, "example_ru",
     "Была длинная пауза в программе",
     "В программе был длинный перерыв",
     "«пауза» нет в списке, а «перерыв» стоит первым"),
    (17188, "example_ru",
     "Рецепция отеля на первом этаже",
     "Ресепшен отеля на первом этаже",
     "«рецепция» нет в списке, а «ресепшен» стоит первым"),
    (15560, "example_uk",
     "Ми скоро збиратимемо овочі",
     "Ми скоро збиратимемо врожай овочів",
     "потерян «врожай»: в списке «збирати врожай»"),
    (2073, "example_uk",
     "Чи є ще місце?",
     "Чи є ще місце в наявності?",
     "слова ряда в примере не было: vorhanden это «наявний»"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (12685, "translation_uk",
     "запаморочливо, голова йде обертом",
     "запаморочення, голова йде обертом",
     "«запаморочливо» не слово: есть «запаморочення»"),
    (10687, "example_uk",
     "Він налякується, коли раптом відкривається двері",
     "Він лякається, коли раптом відчиняються двері",
     "«двері» множественное: нужно «відчиняються»"),
    (15094, "translation_tr",
     "baz, alkali, kuzen",
     "baz, alkali, kuzin",
     "в ru, uk и pl сестра: «kuzen» это брат, сестра — «kuzin»"),

    # ══ эталон: форма слова вместо заголовка ════════════════════
    (1068, "example_de",
     "Er hat sich an der Zehe verletzt",
     "Er hat sich am Zeh verletzt",
     "слово ряда `Zeh`, а эталон писал `Zehe` — четвёртый такой случай"),

    # ══ немецкая грамматика и написание ═════════════════════════
    (12686, "example_de",
     "Er hat kein Rückgrat, kein Mut",
     "Er hat kein Rückgrat, keinen Mut",
     "`Mut` мужского рода в винительном: «keinen Mut»"),
    (12691, "example_de",
     "Der Arzt möchte eine Urin-Probe",
     "Der Arzt möchte eine Urinprobe",
     "составное слово пишется слитно"),

    # ══ КЛАСС: подменённое предложение ═══════════════════════════
    (7370, "example_en",
     "Help me pull the sofa inside",
     "Leave me alone, I'm just watching a film",
     "подмена: эталон «Lass mich, ich ziehe mir gerade einen Film rein»"),
    (11766, "example_pl",
     "Podaj mi keczup do frytek",
     "Do frytek chciałbym keczup",
     "подмена: эталон не просьба подать, а «möchte ich gerne haben»"),

    # ══ время глагола ═══════════════════════════════════════════
    (7361, "example_tr",
     "Mutfaktan gürültü duyuldu!",
     "Mutfaktan gürültü geliyor!",
     "прошедшее против «Es poltert»; в остальных четырёх настоящее"),
    (1068, "example_tr",
     "Ayak parmağını yaralıyor",
     "Ayak parmağını yaraladı",
     "настоящее против «hat sich verletzt»"),
    (7387, "example_ru",
     "Он навострил уши, чтобы лучше слышать",
     "Он навостряет уши, чтобы лучше слышать",
     "прошедшее против «Er spitzt»; в uk и pl настоящее"),
    (7387, "example_tr",
     "Daha iyi duymak için kulağını kabarttı",
     "Daha iyi duymak için kulağını kabartıyor",
     "то же"),

    # ══ потерянное слово ════════════════════════════════════════
    (2338, "example_en",
     "The demonstration was peaceful",
     "The demonstration was peaceful and well organized",
     "потеряно «und gut organisiert»: в остальных четырёх оно есть"),
    (2462, "example_en",
     "That goes quite quickly",
     "That goes quite quickly, don't worry",
     "потеряно «keine Sorge»: в остальных четырёх оно есть"),
    (11764, "example_pl",
     "Dziś spożywamy posiłek w restauracji",
     "Dziś wieczorem spożywamy posiłek razem w restauracji",
     "потеряно «heute Abend» и «zusammen»"),
    (15092, "example_uk",
     "Хрещення дитини на наступний тиждень",
     "Хрещення дитини наступної неділі",
     "«nächsten Sonntag» это воскресенье, а не неделя"),
    (1960, "example_tr",
     "Bir ton 1000 kilo",
     "Bir ton 1000 kilogram ağırlığındadır",
     "потерян глагол «wiegt»"),

    # ══ не тот притяжательный ═══════════════════════════════════
    (13690, "example_pl",
     "Obcasy w tych butach są za wysokie",
     "Obcasy w moich butach są za wysokie",
     "«tych» вместо «meinen»; в остальных четырёх «мои»"),

    # ══ сочетаемость ════════════════════════════════════════════
    (7389, "example_pl",
     "Ma nerwowy tik pod okiem",
     "Ma nerwowy tik oka",
     "«pod okiem» это под глазом, а эталон «am Auge»"),

    # ══ список не покрывал своего примера ═══════════════════════
    (11764, "translation_ru",
     "обедать, есть, трапезничать, питать",
     "обедать, ужинать, есть, трапезничать, питать",
     "пример про ужин, а «ужинать» в списке не было"),
    (11764, "translation_uk",
     "обідати, їсти, трапезувати, живити",
     "обідати, вечеряти, їсти, трапезувати, живити",
     "то же"),
    (2092, "translation_tr",
     "dişi, kadın, kadınsı",
     "dişi, kadın, kadınsı, kız",
     "«dişi» о животных; про ребёнка пример говорит «kız»"),
    (7670, "translation_uk",
     "один в одного, одне в одне",
     "один в одного, одна в одну, одне в одне",
     "пример «одна в одну», а женского рода в списке не было"),
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
