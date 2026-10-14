"""ВТОРОЙ ПРОХОД, блок 19 (ряды 3601–3800).

ШЕСТОЙ БЛОК ПОДРЯД С ПОДМЕНОЙ. На этот раз подмен больше, чем в любом
прошлом блоке, и en+uk+tr опять вместе:

    ertrinken (12597)  de «Hier kann man leicht ertrinken»
        en «The man drowned in the lake»
        uk «Чоловік потонув у озері»
        tr «Adam gölde boğuldu»
        Все три про утонувшего мужчину, которого в эталоне нет. ru и pl
        верны.

    schlachten (11719) en, uk, tr перевели в пассив, а эталон активен

Но главное в этом блоке — РЯД, ГДЕ ВЕРЕН ТОЛЬКО ОДИН ЯЗЫК:

    Reue (10476)  de «Aus echter Reue bat er um Vergebung»
        en «He regretted his deed out of genuine remorse» — не просил
        uk «Він розкаялся у своєму вчинку з щирого розкаяння» —
            тавтология, и «розкаялся» русизм
        tr «Gerçek pişmanlıktan eyleminden pişman oldu» — тавтология
        pl «Czuł szczerą skruchę po tej kłótni» — после какой-то ссоры
        ru — единственный верный

Четыре языка из пяти, каждый по-своему. Это не один источник.

ЗАМЕР: ПОТЕРЯННОЕ ЧИСЛО. Гейт `scan_number_mismatch` нарочно пропускает
ряды, где в переводе цифр нет вовсе, — потому что число может быть
написано словом («um 10 Uhr» → «o dziesiątej»). Значит случай «число
есть в эталоне, а в переводе его нет НИ ЦИФРОЙ, НИ СЛОВОМ» гейт не
видит. Проверено отдельно: 168 эталонов с цифрой, 23 попадания.

**Все 23 — дыры в моём же списке числительных**, а не дефекты базы:
польские порядковые в косвенных падежах («ósmej», «dziesiątej»,
«szóstej», «siódmej»), «osiemdziesiąt», «osiemset», украинское
«сімдесятих», английское «noon». Настоящих ноль.

Класс «потерянное число» по базе ЧИСТ, и пропуск в гейте ничего не
скрывает. Записано как положительный результат, а не как «примета
ничего не нашла».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: подменённое предложение ═══════════════════════════
    (12597, "example_en",
     "The man drowned in the lake",
     "You can easily drown here",
     "подмена: эталон «Hier kann man leicht ertrinken»"),
    (12597, "example_uk",
     "Чоловік потонув у озері",
     "Тут легко потонути",
     "то же"),
    (12597, "example_tr",
     "Adam gölde boğuldu",
     "Burada kolayca boğulabilirsin",
     "то же"),
    (7092, "example_tr",
     "Sınavda kötü sonuç aldı",
     "Etiketi kesmek istiyorum",
     "подмена: эталон «Ich will das Etikett abschneiden»"),
    (10475, "example_tr",
     "Saçını kestirdiğini hemen fark ettim",
     "Tarihi aklında tut",
     "подмена: эталон «Merk dir das Datum»"),
    (10479, "example_pl",
     "Wierzy, że dusza jest nieśmiertelna",
     "Miłość w tym filmie jest nieśmiertelna",
     "подмена: эталон про любовь в фильме, а не про душу"),
    (7100, "example_tr",
     "Aramızda karşılıklı bir saygı var",
     "Sana da her şeyin en iyisi, aynı şekilde",
     "подмена: эталон «Dir auch alles Gute, gleichfalls»"),
    (16154, "example_pl",
     "Rosja jest federacją wielu republik",
     "Federacja składa się z wielu krajów",
     "подмена: Россия в эталоне не упоминается"),
    (16155, "example_pl",
     "Prezydentka wygłosiła krótkie przemówienie",
     "Prezydentka mówi do ludzi",
     "подмена: эталон «spricht zu den Menschen»"),
    (7102, "example_tr",
     "Para bana ait",
     "Bu para benim hakkım",
     "«деньги мои» не то же, что «мне причитаются»"),
    (12181, "example_pl",
     "Potrzebuję trochę odmiany w pracy",
     "Potrzebowaliśmy trochę odmiany",
     "подмена лица и времени: эталон «Wir brauchten»"),
    (8871, "example_tr",
     "Öğretmenlik onun için gerçek bir meslek aşkı",
     "Tıp benim meslek aşkım",
     "подмена: эталон «Medizin ist meine Berufung»"),
    (2385, "example_uk",
     "Не вмикай світло, дитина спить",
     "Увімкни телевізор",
     "подмена: эталон «Schalte den Fernseher ein»"),
    (16158, "example_pl",
     "Nie wolno torturować więźniów",
     "Policja nie może torturować",
     "подмена: эталон «Die Polizei darf nicht foltern»"),
    (10483, "example_pl",
     "Jej mąż był brutalny wobec dzieci",
     "Był brutalnym człowiekiem",
     "подмена: эталон «Er war ein gewalttätiger Mensch»"),
    (13517, "example_tr",
     "Bu konuda sana katılıyorum",
     "Bu durumda dikkatli olmak gerekir",
     "подмена: эталон «Hierbei ist Vorsicht geboten»"),
    (7110, "example_uk",
     "Це виключено, я не погоджуся",
     "Для мене це не береться до уваги",
     "подмена: эталон «Das kommt für mich nicht infrage»"),

    # ══ РЯД, ГДЕ ВЕРЕН ТОЛЬКО РУССКИЙ ════════════════════════════
    (10476, "example_en",
     "He regretted his deed out of genuine remorse",
     "Out of genuine remorse he asked for forgiveness",
     "эталон «bat er um Vergebung» — просил прощения"),
    (10476, "example_uk",
     "Він розкаялся у своєму вчинку з щирого розкаяння",
     "З щирого розкаяння він попросив пробачення",
     "тавтология, «розкаялся» русизм, и «просил прощения» потеряно"),
    (10476, "example_tr",
     "Gerçek pişmanlıktan eyleminden pişman oldu",
     "Gerçek pişmanlıkla af diledi",
     "«pişmanlıktan ... pişman oldu» тавтология"),
    (10476, "example_pl",
     "Czuł szczerą skruchę po tej kłótni",
     "Ze szczerej skruchy poprosił o przebaczenie",
     "подмена: никакой ссоры в эталоне нет"),

    # ══ эталон: не та форма слова ряда ═══════════════════════════
    (10481, "example_de",
     "Er wirkt blasé, als würde ihn nichts interessieren",
     "Er wirkt blasiert, als würde ihn nichts interessieren",
     "слово ряда — «blasiert», а в примере стояло французское «blasé»"),

    # ══ формы, которых в языке нет ═══════════════════════════════
    (15503, "example_uk",
     "Гриф кружити над горами",
     "Гриф кружляє над горами",
     "инфинитив вместо третьего лица"),
    (7106, "example_tr",
     "Bez çok yumuşaktu",
     "Bez çok yumuşaktı",
     "«yumuşaktu» не форма: гармония гласных даёт «yumuşaktı»"),
    (8872, "example_tr",
     "Bar sahibi çok dostaneceydi",
     "Meyhane sahibi çok cana yakındı",
     "«dostaneceydi» не форма; и в списке «meyhane sahibi»"),
    (7094, "example_tr",
     "Mumı üfliyor",
     "Mumu üflüyor",
     "гармония гласных дважды: «mumu» и «üflüyor»"),
    (7114, "example_pl",
     "Wie o tym najmniej ludzi",
     "Najmniej ludzi o tym wie",
     "порядок слов разрушал фразу"),
    (16155, "example_tr",
     "Başkan insanlara konuşuyor",
     "Başkan halka hitap ediyor",
     "«insanlara konuşmak» не управление: нужно «hitap etmek»"),
    (10485, "example_tr",
     "Ödevler için çok konsantrasyona ihtiyacım var",
     "Ödevler için çok fazla konsantrasyona ihtiyacım var",
     "«çok konsantrasyona» не согласовано"),
    (14009, "example_tr",
     "Benim yardımıma bağımlı",
     "O benim yardımıma bağımlı",
     "потеряно подлежащее"),
    (17135, "example_tr",
     "Sokak bir çıkmaz sokaktır",
     "Bu sokak bir çıkmaz",
     "«sokak» дважды в одной фразе"),

    # ══ слово не из своего списка и не то слово ══════════════════
    (8869, "example_tr",
     "Barista bana bir kokteyl yapıyor",
     "Barmen bana bir kokteyl yapıyor",
     "«barista» это кофевар, а Barkeeper — бармен"),
    (10483, "example_tr",
     "O şiddetli bir insandı",
     "O şiddete eğilimli bir insandı",
     "«şiddetli» это сильный, а не склонный к насилию"),
    (17945, "example_tr",
     "Felsefe çalışıyorum",
     "Felsefe okuyorum",
     "«çalışmak» это работать; изучать — «okumak»"),
    (7098, "example_tr",
     "Bu piknik için ideal havadır",
     "Bu gezi için ideal bir hava",
     "в эталоне Ausflug — поездка, а не пикник"),
    (7095, "example_tr",
     "Şu tarafa bak, diğer tarafta",
     "Karşı tarafa bak",
     "«taraf» дважды, и местный падеж вместо направительного"),
    (14469, "example_tr",
     "Bu şarkı sıralamada büyük bir hit",
     "Bu şarkı büyük bir hit",
     "«в чартах» в эталоне нет"),
    (15507, "example_tr",
     "Gece dolunay var",
     "Bu gece dolunay var",
     "потеряно «heute»"),
    (8873, "example_uk",
     "Водій відвіз нас до аеропорту",
     "Шофер відвіз нас до аеропорту",
     "карточка показывает «шофер», а пример говорил «водій»"),
    (9786, "example_ru",
     "Мешок полный",
     "Пакет полный",
     "«мешок» нет в списке переводов, а «пакет» стоит первым"),
    (9785, "example_ru",
     "Старая машина бесполезна",
     "Старая машина ничего не стоит",
     "wertlos это «ничего не стоящий», а не «бесполезный»"),
    (12601, "example_uk",
     "Він наркоман",
     "Він залежний від наркотиків",
     "эталон «süchtig nach Drogen», а не «он наркоман»"),
    (18211, "example_uk",
     "Дверний дзвоник не працює",
     "Дверний дзвінок не працює",
     "в списке «дверний дзвінок», а не «дзвоник»"),
    (12186, "example_uk",
     "Постріл був прямим попаданням у ціль",
     "Постріл був влучним попаданням у яблучко",
     "эталон «ins Schwarze» — в яблочко; оно есть в списке"),

    # ══ русизмы в украинских списках переводов ═══════════════════
    (12596, "translation_uk",
     "болісний, болючий, мучительний",
     "болісний, болючий, нестерпний",
     "«мучительний» русское слово"),
    (10477, "translation_uk",
     "нестерпний, невиносний",
     "нестерпний, незносний",
     "«невиносний» русизм: по-украински «незносний»"),
    (10486, "translation_uk",
     "чарівний, чудовий, звабливий",
     "чарівний, чудовий, милий",
     "«звабливий» это соблазнительный — не про младенца"),

    # ══ потерянный модальный и залог ═════════════════════════════
    (16153, "example_ru",
     "Люди эвакуируют здание",
     "Люди должны эвакуировать здание",
     "потерян модальный: эталон «müssen evakuieren»"),
    (16153, "example_uk",
     "Люди евакуюють будинок",
     "Люди повинні евакуювати будинок",
     "то же"),
    (16153, "example_pl",
     "Trzeba natychmiast ewakuować budynek",
     "Ludzie muszą ewakuować budynek",
     "подмена подлежащего и добавлено «natychmiast»"),
    (16153, "example_tr",
     "İnsanlar binaları tahliye etmelidir",
     "İnsanlar binayı tahliye etmelidir",
     "множественное против «das Gebäude»"),
    (11719, "example_en",
     "The pig is slaughtered",
     "They slaughter the pig",
     "пассив против активного «Sie schlachten»"),
    (11719, "example_uk",
     "Свиню забивають",
     "Вони забивають свиню",
     "то же"),
    (11719, "example_tr",
     "Domuz kesiliyor",
     "Domuzu kesiyorlar",
     "то же"),
    (16164, "example_pl",
     "Policja przesłuchała podejrzanego",
     "Podejrzany został przesłuchany przez policję",
     "актив против пассивного «wurde verhört»; в остальных четырёх пассив"),
    (16151, "example_ru",
     "Заключённый сбежал из тюрьмы",
     "Заключённый убегает из тюрьмы",
     "прошедшее против «flüchtet»; в остальных четырёх настоящее"),

    # ══ потерянное и добавленное слово ═══════════════════════════
    (7100, "example_uk",
     "Тобі всього хорошого, взаємно",
     "Тобі теж усього найкращого, взаємно",
     "потеряно «auch»: в ru оно есть"),
    (10477, "example_pl",
     "Ten upał jest nieznośny",
     "Ten upał jest naprawdę nieznośny",
     "потеряно «wirklich»: в остальных четырёх оно есть"),
    (16157, "example_pl",
     "Ankieta wśród klientów trwała godzinę",
     "Ankieta trwała godzinę",
     "«среди клиентов» в эталоне нет"),
    (16161, "example_pl",
     "Na piasku były wyraźne odciski stóp",
     "Odciski na piasku były wyraźne",
     "«stóp» в эталоне нет"),
    (16161, "example_tr",
     "Kumda izler çok açıktı",
     "Kumdaki izler belirgindi",
     "«çok» в эталоне нет"),
    (10484, "example_pl",
     "Zrobiłem to tylko dla ciebie",
     "Zrobiłem to dla ciebie",
     "«tylko» в эталоне нет"),
    (16159, "example_pl",
     "Wiceprezydent przyjechał na konferencję",
     "Wiceprezydent był na konferencji",
     "«приехал» против «war bei» — был"),

    # ══ сиблинг-ряд: та же ошибка, что в блоке 18 ════════════════
    (15502, "example_pl",
     "Jedziemy w południowy region",
     "Jedziemy do południowego regionu",
     "та же ошибка, что у `nördlich` (15498) в блоке 18: «jechać do»"),

    # ══ мелочи орфографии и благозвучия ══════════════════════════
    (16160, "example_uk",
     "На них напали з засідки",
     "На них напали із засідки",
     "перед «з» потрібне «із» для милозвучності"),
    (2504, "example_uk",
     "Будь, будь ласка, терплячим",
     "Будь ласка, будь терплячим",
     "«Будь, будь» — запинка при чтении вслух"),
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
