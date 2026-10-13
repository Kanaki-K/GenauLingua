"""ВТОРОЙ ПРОХОД, блок 29 (ряды 5601–5800): 58 правок.

ПЕРВЫЙ РЯД, ГДЕ ПОДМЕНИЛИ ЧЕТЫРЕ ЯЗЫКА ИЗ ПЯТИ:

    erstmals (18781)  de «Wir haben uns erstmals in Berlin getroffen»
        en «I'm seeing you for the first time, we don't know each other»
        ru «Я вижу тебя впервые, мы не знакомы»
        uk «Я тебе вперше, ми не знайомі»
        tr «Seni ilk kez görüyorum, tanışmıyız»
        pl «Spotkaliśmy się po raz pierwszy w Berlinie» — ВЕРНО

До этого худшим расклад был en+uk+tr против ru и pl (двенадцать раз) или
один верный язык из пяти (`блок 19`). Здесь прав остался только польский,
и видно, что подмена шла ОДНОЙ фразой: все четыре написали вариацию «я
вижу тебя впервые, мы не знакомы». Украинский при этом потерял сказуемое
(«Я тебе вперше»), а турецкий дал несуществующую форму («tanışmıyız»
вместо «tanışmıyoruz») — то есть фраза-источник ещё и портилась по пути.

ЧТО ПОДТВЕРДИЛО ПРАВКУ ПРОШЛОГО БЛОКА. В блоке 27 я переписал ряд
`Zünder` (17576), у которого немецкий эталон говорил «Der Zünder des
Motors war beschädigt» — у двигателя не бывает `Zünder`. В этом блоке
стоит ряд `Zündung` (17594), и его эталон «Die Zündung des Motors
funktioniert nicht richtig» ВЕРЕН. То есть `Zünder` взял смысл и фразу у
соседа по смыслу, а четыре языка послушно написали «зажигание».

Это четвёртое подтверждение наблюдения про участки базы, и первое, где
источник подмены найден прямо.

ЛОЖНЫЙ ДРУГ В ДВУХ РЯДАХ СРАЗУ:

    Therapeut  (12722)  ru «Мой терапевт помогает мне с моими проблемами»
    Therapeutin (12732) ru «Мой терапевт действительно хорошо помогает...»

Русское «терапевт» — это врач общей практики, а немецкое `Therapeut` —
психотерапевт. Карточка обещала «психотерапевт» (первым в списке) и
давала пример про участкового врача. В `Therapeutin` список к тому же
начинался с «терапевт», так что показывалось именно неверное значение.
Оба ряда исправлены, у второго переставлен список.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ подмена в четырёх языках из пяти ════════════════════════
    (18781, "example_en",
     "I'm seeing you for the first time, we don't know each other",
     "We met for the first time in Berlin",
     "подмена: эталон «Wir haben uns erstmals in Berlin getroffen»"),
    (18781, "example_ru",
     "Я вижу тебя впервые, мы не знакомы",
     "Мы впервые встретились в Берлине",
     "то же; верен остался только pl"),
    (18781, "example_uk",
     "Я тебе вперше, ми не знайомі",
     "Ми вперше зустрілися в Берліні",
     "то же, и в придачу потеряно сказуемое"),
    (18781, "example_tr",
     "Seni ilk kez görüyorum, tanışmıyız",
     "Berlin'de ilk kez tanıştık",
     "то же, и «tanışmıyız» не форма: было бы «tanışmıyoruz»"),

    # ══ ложный друг «терапевт» в двух рядах ═════════════════════
    (12722, "example_ru",
     "Мой терапевт помогает мне с моими проблемами",
     "Мой психотерапевт помогает мне с моими проблемами",
     "русское «терапевт» это врач общей практики; `Therapeut` — психотерапевт"),
    (12722, "example_uk",
     "Мій терапевт допомагає мені з моїми проблемами",
     "Мій психотерапевт допомагає мені з моїми проблемами",
     "то же"),
    (12732, "translation_ru",
     "терапевт, психотерапевт",
     "психотерапевт, терапевт",
     "ложный друг стоял первым, и карточка показывала именно его"),
    (12732, "translation_uk",
     "терапевт, психотерапевтка",
     "психотерапевтка, терапевт",
     "то же"),
    (12732, "example_ru",
     "Мой терапевт действительно хорошо помогает мне с моими проблемами",
     "Мой психотерапевт действительно хорошо помогает мне с моими проблемами",
     "то же"),
    (12732, "example_uk",
     "Моя терапевтка мені справді добре допомагає з моїми проблемами",
     "Моя психотерапевтка мені справді добре допомагає з моїми проблемами",
     "то же"),

    # ══ КЛАСС: подменённое предложение ══════════════════════════
    (11784, "example_pl",
     "Postaw kubki na tacy",
     "Jedzenie leży na tacy",
     "подмена: эталон «Das Essen liegt auf dem Tablett»"),
    (7478, "example_uk",
     "На столі застиг віск від свічки",
     "Свічка зроблена з воску",
     "подмена: эталон «Die Kerze besteht aus Wachs»"),
    (1970, "example_uk",
     "У сходовій клітці знову перегоріла лампа",
     "Сходова клітка чиста",
     "подмена: эталон «Das Treppenhaus ist sauber»"),
    (7481, "example_pl",
     "Muszę sam poradzić sobie ze stresem",
     "Próbuję pokonać swój strach",
     "подмена: стресс вместо страха, и «должен» вместо «пытаюсь»"),
    (14103, "example_tr",
     "Günlüğüne yeni bir girdi ekledi",
     "Günlükteki kayıt çok kişisel yazılmış",
     "подмена: эталон о том, КАК запись написана, а не о том, кто её добавил"),
    (16363, "example_pl",
     "Policjant wystrzelił w powietrze",
     "Policjant oddaje strzał",
     "«в воздух» в эталоне нет, и время не то"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (12724, "translation_uk",
     "умирущий, що вмирає, присмертний",
     "вмираючий, що вмирає, присмертний",
     "«умирущий» не слово: по-украински «вмираючий»"),
    (7482, "translation_uk",
     "залізний, незламний, стальний",
     "залізний, незламний, сталевий",
     "«стальний» русское; по-украински «сталевий»"),
    (16360, "example_uk",
     "Суд винес смертний вирок проти нього",
     "Суд виніс йому смертний вирок",
     "«винес» русское; по-украински «виніс»"),
    (7485, "example_uk",
     "Кинь окурок у смітник, не на вулицю",
     "Кинь недопалок у смітник, а не на вулицю",
     "«окурок» русское; «недопалок» стоит в списке первым"),
    (12229, "translation_ru",
     "гребсти, идти на веслах, размахивать руками",
     "грести, идти на вёслах, размахивать руками",
     "«гребсти» не форма: нужно «грести»; и пропущена «ё»"),
    (7485, "example_tr",
     "Sigara izmaritesini çöpe at, caddeye değil",
     "Sigara izmaritini çöpe at, caddeye değil",
     "«izmaritesini» не форма: «izmaritini»"),
    (12230, "example_tr",
     "At tırıtla gidiyor, cümbür değil",
     "At tırısla gidiyor, dörtnala değil",
     "«tırıtla» не форма, а «cümbür» не слово; галоп это «dörtnala»"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (7484, "translation_uk",
     "безпечний, безневинний",
     "безпечний, нешкідливий",
     "«безневинний» это невинный, а не безвредный"),
    (14100, "example_tr",
     "Reklam çok komikti",
     "Reklam filmi çok komikti",
     "в списке «reklam filmi», а пример давал половину"),
    (12724, "example_tr",
     "Ölüm döşeğindeki adam su istedi",
     "Ölmekte olan adam su istedi",
     "«ölüm döşeğinde» это на смертном одре; в списке «ölmekte olan»"),
    (10775, "example_tr",
     "Sonucu gördüğümde dilsiz kaldım",
     "Sonucu gördüğümde dilim tutuldu",
     "«dilsiz» это немой от рождения; в списке «dili tutulmuş»"),
    (17206, "example_tr",
     "Kaptan her şeyi gemi defterine yazıyor",
     "Kaptan her şeyi seyir defterine yazıyor",
     "«gemi defteri» нет в списке, а «seyir defteri» стоит первым"),
    (7472, "example_tr",
     "Onu gelecek hafta işten atmak istiyorlar",
     "Onu gelecek hafta kapı dışarı etmek istiyorlar",
     "«işten atmak» это уволить; `rausschmeißen` шире, и «kapı dışarı» первое"),
    (2473, "example_tr",
     "Düzenli spor sağlığı teşvik eder",
     "Düzenli spor sağlığı destekler",
     "«teşvik etmek» поощряют человека, а не здоровье"),
    (12727, "example_uk",
     "Медсестра допомагає старому чоловікові вмиватися",
     "Медбрат допомагає старому чоловікові вмиватися",
     "`Pfleger` мужского рода; «медбрат» стоит в списке первым"),
    (8975, "example_uk",
     "Кучер веде карету через місто",
     "Кучер править каретою по місту",
     "карету не «ведуть»; в ru «правит»"),
    (8973, "example_uk",
     "Яку професію ти хочеш мати згодом?",
     "Якою професією ти хочеш займатися згодом?",
     "ни одного слова списка; «займатися» стоит первым"),
    (16356, "example_ru",
     "Избиратель решает судьбу политики",
     "Избиратель решает, какой будет политика",
     "«судьбу» в эталоне нет; «über die Politik entscheiden»"),
    (8977, "example_ru",
     "Генерал возглавит армию в войне",
     "Генерал поведёт армию на войну",
     "«in den Krieg anführen» это повести НА войну; в остальных четырёх так"),
    (7491, "example_en",
     "The child sucks on a lollipop",
     "The child sucks on a candy",
     "`Bonbon` это конфета, а не леденец на палочке"),
    (7491, "example_tr",
     "Çocuk bir lolipop emiyor",
     "Çocuk bir şeker emiyor",
     "то же"),
    (7491, "example_pl",
     "Dziecko ssie lizaka",
     "Dziecko ssie cukierka",
     "то же"),
    (17594, "example_en",
     "The car's ignition isn't working properly",
     "The engine's ignition isn't working properly",
     "эталон «des Motors» — двигателя, а не машины"),

    # ══ управление и сочетаемость ═══════════════════════════════
    (16359, "example_tr",
     "Pek çok kişi reformun karşısında protesto ediyor",
     "Pek çok kişi reforma karşı protesto ediyor",
     "«karşısında» это напротив; против чего-то — «-a karşı»"),
    (17207, "example_tr",
     "Senin tarafından çok riskli bir manevra oldu",
     "Senin yaptığın çok riskli bir manevraydı",
     "«senin tarafından» канцелярский пассив вместо «von dir»"),
    (12728, "example_uk",
     "Мені спокійніше, тепер коли я це сказав",
     "Мені спокійніше, відтоді як я це сказав",
     "«тепер коли» не связка; «seitdem» это «відтоді як»"),
    (17207, "example_uk",
     "Це був дуже ризикований маневр з твоєї сторони",
     "Це був дуже ризикований маневр з твого боку",
     "«з твоєї сторони» русизм; по-украински «з твого боку»"),
    (12230, "example_uk",
     "Кінь їде рисаком, а не галопом",
     "Кінь іде риссю, а не галопом",
     "конь не «їде», и «рисаком» это порода, а не бег"),
    (11786, "example_uk",
     "Соус смакував з м'ясом",
     "Соус чудово смакував із м'ясом",
     "потеряно «köstlich»"),
    (10770, "example_uk",
     "Вона справді капризуля",
     "Вона справжня капризуля",
     "«richtige» это настоящая, а не «справді»"),
    (14552, "example_pl",
     "Legenda o świętym Graalu jest bardzo znana",
     "Legenda o Świętym Graalu jest bardzo znana",
     "`Heiliger Gral` пишется с большой буквы"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (15115, "example_ru",
     "Мы хороним дедушку на следующей неделе",
     "Мы хороним моего дедушку на следующей неделе",
     "потеряно «meinen»: в en, tr и pl оно есть"),
    (15115, "example_uk",
     "Ми поховаємо дідуся наступного тижня",
     "Ми поховаємо мого дідуся наступного тижня",
     "то же"),
    (8980, "example_ru",
     "Завтра отправляю заявку на работу",
     "Завтра отправляю свою заявку на работу",
     "потеряно «meine»: в en, tr и pl оно есть"),
    (8980, "example_uk",
     "Завтра посилаю заявку на роботу",
     "Завтра надсилаю свою заявку на роботу",
     "то же"),
    (18272, "example_ru",
     "На чердаке много старых вещей",
     "Чердак полон старых вещей",
     "потеряно «ist voll»: в остальных четырёх сказуемое есть"),
    (12723, "example_tr",
     "Hastaneye kaldırıldı",
     "O, hastaneye kaldırıldı",
     "потеряно подлежащее «Er»"),
    (16359, "example_pl",
     "Ludzie demonstrują przeciw nowej ustawie",
     "Wielu ludzi demonstruje przeciw reformie",
     "потеряно «Viele», и «ustawa» это закон, а не реформа"),
    (16355, "example_pl",
     "Radiowóz przejechał szybko obok nas",
     "Radiowóz przejechał szybko obok",
     "«nas» в эталоне нет"),
    (12721, "example_tr",
     "Omurga çok önemli",
     "Omurga önemli",
     "«çok» в эталоне «ist wichtig» нет"),

    # ══ немецкое написание ══════════════════════════════════════
    (14100, "example_de",
     "Der Werbe-Spot war sehr lustig",
     "Der Werbespot war sehr lustig",
     "составное слово пишется слитно"),

    # ══ время глагола ═══════════════════════════════════════════
    (2935, "example_tr",
     "Gelecek hafta buluşmak için sözleştik",
     "Gelecek hafta buluşmak için sözleşiyoruz",
     "прошедшее против «Wir verabreden uns»"),
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
