"""ВТОРОЙ ПРОХОД, блок 27 (ряды 5201–5400): 71 правка.

ДЕСЯТАЯ И ОДИННАДЦАТАЯ ТРОЙКИ en+uk+tr, обе в одном блоке:

    edler (10717)  de «Er hat einen edlen Charakter» — ХАРАКТЕР
        en «This is a noble WINE VARIETY»
        uk «Це благородний СОРТ ВИНА»
        tr «Bu asil bir ŞARAP ÇEŞİDİDİR»
        ru и pl говорят про характер.

    stillhalten (7405)  de «Beim FRISEUR musst du stillhalten»
        en «Stay still, the DOCTOR wants to examine you»
        uk «Стій спокійно, ЛІКАР хоче тебе оглянути»
        tr «Hareketsiz dur, DOKTOR seni muayene etmek istiyor»
        ru и pl говорят про парикмахера.

Расклад тот же, что в блоках 14–25: ru и pl верны, а три языка ушли
вместе и придумали одно и то же. Одиннадцать подтверждений за
четырнадцать блоков — это уже не совпадение, а общий источник.

ТРЕТИЙ РЯД С НЕВЕРНЫМ НЕМЕЦКИМ ЭТАЛОНОМ (после `Arche` и `Güte` в
блоке 26), и здесь он тянет за собой все пять языков:

    Zünder (17576)  de «Der Zünder des Motors war beschädigt»

`Zünder` это взрыватель, запал у взрывного устройства. У двигателя
бывает `Zündung`, но не `Zünder`. Переводы попытались спасти фразу
каждый по-своему: английский, русский, украинский и польский написали
«зажигание», которого нет ни в одном списке, а турецкий сдался и
подставил совершенно чужое предложение — «Tetikçi olay yerinde
yakalandı», то есть «киллера взяли на месте». Весь ряд переписан на
фразу, где `Zünder` — то самое слово, что в списках.

ПОЛЬСКИХ ПОДМЕН СЕМЬ, И ВСЕ В ЮРИДИЧЕСКИХ РЯДАХ:

    Vorstrafe   (16324)  «Policja sprawdziła jego wcześniejszą karalność»
    Freilassung (16329)  «Uwolnienie ZAKŁADNIKÓW zajęło kilka dni»
    Zulassung   (16328)  «Potrzebuję dopuszczenia do EGZAMINU»
    Einzelhaft  (16325)  «Trafił do izolatki na cały miesiąc»
    Exil        (16334)  «PISARZ musiał żyć na wygnaniu»
    Wahlkampf   (16323)  «...trwa już MIESIĄC» вместо трёх месяцев
    Pyjama      (13691)  «Chodzę po domu w piżamie»

Идентификаторы 16323–16335 идут подряд: подмены сели на один участок
базы, как списки сокола и улитки в блоке 26 сели на соседние ряды.

ПОТЕРЯННАЯ ПРОСЬБА, КОТОРУЮ ПРИМЕТА ПРОПУСКАЕТ ПО УСТРОЙСТВУ. Ряд
`weitergeben` (14080): эталон «Kannst du mir das Salz bitte
weitergeben?» — и вопрос, и «bitte». Русский и украинский оставили
только вопрос. `scan_bitte_dropped` этого не видит нарочно: она считает
вежливость сохранённой, если фраза хотя бы вопросительная, иначе
турецкий «-misin» и польское «Proszę» давали сотни ложных. Предел
назван в самой примете; такие ряды находятся только глазами.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ неверен сам немецкий эталон ═════════════════════════════
    (17576, "example_de",
     "Der Zünder des Motors war beschädigt",
     "Der Zünder der Bombe wurde entschärft",
     "`Zünder` это взрыватель; у двигателя бывает `Zündung`, но не `Zünder`"),
    (17576, "example_en",
     "The engine's ignition was faulty",
     "The detonator of the bomb was defused",
     "«ignition» нет в списке: шло за неверным эталоном"),
    (17576, "example_ru",
     "Зажигание двигателя было неисправно",
     "Взрыватель бомбы был обезврежен",
     "то же: «зажигание» нет в списке"),
    (17576, "example_uk",
     "Запалювання двигуна було несправне",
     "Детонатор бомби був знешкоджений",
     "то же"),
    (17576, "example_tr",
     "Tetikçi olay yerinde yakalandı",
     "Bombanın fünyesi etkisiz hale getirildi",
     "подмена целиком: «киллера взяли на месте» вместо взрывателя"),
    (17576, "example_pl",
     "Zapalnik silnika był uszkodzony",
     "Zapalnik bomby został rozbrojony",
     "то же: шло за неверным эталоном"),

    # ══ КЛАСС: тройка en+uk+tr, десятая и одиннадцатая ══════════
    (10717, "example_en",
     "This is a noble wine variety",
     "He has a noble character",
     "подменено целиком: эталон «Er hat einen edlen Charakter»"),
    (10717, "example_uk",
     "Це благородний сорт вина",
     "У нього благородний характер",
     "то же; ru и pl верны"),
    (10717, "example_tr",
     "Bu asil bir şarap çeşididir",
     "Asil bir karaktere sahip",
     "то же"),
    (7405, "example_en",
     "Stay still, the doctor wants to examine you",
     "At the hairdresser you have to keep still",
     "подменено целиком: эталон «Beim Friseur musst du stillhalten»"),
    (7405, "example_uk",
     "Стій спокійно, лікар хоче тебе оглянути",
     "У перукарні потрібно сидіти спокійно",
     "то же; ru и pl верны"),
    (7405, "example_tr",
     "Hareketsiz dur, doktor seni muayene etmek istiyor",
     "Kuaförde kıpırdamadan durmak zorundasın",
     "то же"),

    # ══ КЛАСС: подменённое предложение, польская полоса ═════════
    (16323, "example_ru",
     "В воскресенье в стране пройдут выборы",
     "Предвыборная кампания длится три месяца",
     "подмена: эталон «Der Wahlkampf dauert drei Monate»"),
    (16323, "example_pl",
     "Kampania wyborcza trwa już miesiąc",
     "Kampania wyborcza trwa trzy miesiące",
     "месяц вместо трёх месяцев"),
    (16324, "example_pl",
     "Policja sprawdziła jego wcześniejszą karalność",
     "Nie ma wcześniejszej karalności",
     "подмена, и потеряно отрицание: эталон «Er hat keine Vorstrafen»"),
    (16329, "example_pl",
     "Uwolnienie zakładników zajęło kilka dni",
     "Uwolnienie więźnia było kontrowersyjne",
     "подмена: заложники вместо заключённого, и другое сказуемое"),
    (16328, "example_pl",
     "Potrzebuję dopuszczenia do egzaminu",
     "Potrzebujesz rejestracji samochodu",
     "подмена: экзамен вместо машины, и лицо не то"),
    (16325, "example_pl",
     "Trafił do izolatki na cały miesiąc",
     "Siedzi w izolatce",
     "подмена: эталон «Er sitzt in Einzelhaft», месяца в нём нет"),
    (16334, "example_pl",
     "Pisarz musiał żyć na wygnaniu",
     "Polityk musiał udać się na wygnanie",
     "подмена: писатель вместо политика"),
    (13691, "example_pl",
     "Chodzę po domu w piżamie",
     "Moja piżama jest bardzo wygodna do spania",
     "подмена: эталон «Mein Pyjama ist sehr bequem zum Schlafen»"),
    (16326, "example_pl",
     "Policja zabezpiecza ślady na miejscu zbrodni",
     "Technicy kryminalistyki znaleźli wiele śladów",
     "подмена: эталон «Die Spurensicherung hat viel gefunden»"),
    (9511, "example_en",
     "The headmaster called my parents",
     "The rector speaks with the students",
     "подмена: эталон «Der Rektor spricht mit den Studierenden»"),

    # ══ сбор улик не может «найти» ══════════════════════════════
    (16326, "example_ru",
     "Сбор улик нашёл много доказательств",
     "Криминалисты нашли много улик",
     "«сбор улик нашёл» — сбор не действующее лицо; в uk уже верно"),
    (16326, "example_tr",
     "Kanıt toplama çok şey buldu",
     "Kriminal ekip birçok kanıt buldu",
     "то же"),

    # ══ потерянная просьба bitte ════════════════════════════════
    (14080, "example_ru",
     "Можешь мне передать соль?",
     "Можешь передать мне соль, пожалуйста?",
     "потеряно «bitte»: в en, tr и pl вежливость на месте"),
    (14080, "example_uk",
     "Можеш мені передати сіль?",
     "Можеш передати мені сіль, будь ласка?",
     "то же"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (10713, "example_uk",
     "Дитина послушна і дотримується правил",
     "Дитина слухняна і дотримується правил",
     "«послушна» русское; по-украински «слухняна», и оно в списке"),
    (10723, "example_uk",
     "Я глажу кота",
     "Я гладжу кота",
     "«глажу» русское; по-украински «гладжу»"),
    (16331, "example_uk",
     "Засудження злочинця обговорювалось гарячо",
     "Засудження злочинця гаряче обговорювали",
     "«гарячо» не форма: нужно «гаряче»"),
    (14085, "example_uk",
     "Він щось бурмотить собі під носом",
     "Він щось бурмотить собі під ніс",
     "оборот «бурмотіти собі під ніс», а не «під носом»"),
    (12698, "example_tr",
     "Cesed morga götürüldü",
     "Ceset morga götürüldü",
     "«cesed» не турецкое написание: «ceset»"),
    (16325, "example_uk",
     "Він знаходиться в одиночному утриманні",
     "Він знаходиться в одиночному ув'язненні",
     "«одиночне утримання» не оборот; в списке «одиночне ув'язнення»"),
    (14078, "translation_ru",
     "проклятый, чертов",
     "проклятый, чёртов",
     "пропущена «ё»"),
    (7405, "translation_uk",
     "не рухатися, стояти спокійно, терпіти молчки",
     "не рухатися, стояти спокійно, терпіти мовчки",
     "«молчки» русское; по-украински «мовчки»"),

    # ══ слово не из своего списка ═══════════════════════════════
    (2212, "example_tr",
     "Nefes alış yüzeysel",
     "Solunum yüzeysel",
     "«nefes alış» не из списка; «solunum» стоит первым"),
    (10715, "example_tr",
     "O hantaldır ve çok şey kırar",
     "O sakardır ve çok şey kırar",
     "«hantal» это неповоротливый; ungeschickt — «sakar», и оно первое"),
    (10722, "example_tr",
     "Savaşın vahşiliği korkunç",
     "Savaşın vahşeti korkunç",
     "«vahşilik» нет в списке, а «vahşet» есть"),
    (18260, "example_tr",
     "Odada büyük bir karışıklık var",
     "Odada büyük bir dağınıklık var",
     "«karışıklık» это путаница; беспорядок в комнате — «dağınıklık»"),
    (7420, "example_tr",
     "Hediyemin üzerindeki kurdele kırmızı ve parlak",
     "Hediyemin üzerindeki fiyonk kırmızı ve parlak",
     "«kurdele» это лента; бант на подарке — «fiyonk», и он первый"),
    (7415, "example_tr",
     "Halat çok kısaydı",
     "İp çok kısaydı",
     "«halat» это толстый канат; `Strick` — «ip», и оно первое"),
    (10720, "example_tr",
     "Bugün hava gerçekten bunaltıcı",
     "Bugün hava gerçekten moral bozucu",
     "«bunaltıcı» о духоте, а не об унынии"),
    (10721, "example_tr",
     "Haberi duyunca dehşete kapıldı",
     "Haberi duyunca dehşete düştü",
     "смешаны два оборота: «dehşete düşmek» и «korkuya kapılmak»"),
    (9510, "example_tr",
     "Defterim masada yatıyor",
     "Not defterim masanın üzerinde",
     "о предмете по-турецки не говорят «yatıyor»"),
    (10718, "example_uk",
     "Він сьогодні погано налаштований",
     "Він сьогодні в поганому настрої",
     "«погано налаштований» о намерениях, а не о настроении"),
    (10710, "example_uk",
     "Він виглядає посоромленим",
     "Він виглядає засоромленим",
     "«посоромлений» это пристыжённый кем-то; в списке «засоромлений»"),
    (15101, "example_uk",
     "Вчора я познайомився з цікавою людиною",
     "Вчора я завів цікаве знайомство",
     "слова ряда в примере не было; в ru и pl существительное на месте"),
    (15101, "example_tr",
     "Dün ilginç biriyle tanıştım",
     "Dün ilginç bir tanışıklık kurdum",
     "то же"),
    (15102, "example_en",
     "Adopting the child was a big step",
     "The adoption of the child was a big step",
     "ряд о существительном, а пример давал отглагольную форму"),
    (8947, "example_tr",
     "Gazeteci ilginç bir makale yazdı",
     "Kadın gazeteci ilginç bir makale yazdı",
     "`Journalistin` женского рода; в списке есть «kadın gazeteci»"),
    (2016, "translation_tr",
     "memnuniyetsiz, hoşnutsuz, memnun olmayan",
     "memnuniyetsiz, hoşnutsuz, memnun değil",
     "по-турецки это сказуемое «memnun değilim», а не причастие"),
    (10699, "translation_ru",
     "запугивать, нагонять страх, робость",
     "запугивать, нагонять страх, устрашать",
     "«робость» существительное среди глаголов"),
    (10714, "translation_pl",
     "rozpieszczony, rozpuszczony, wymagający",
     "rozpieszczony, rozpuszczony, przyzwyczajony do dobrego",
     "«wymagający» это требовательный, а не избалованный"),

    # ══ подменённое слово внутри фразы ══════════════════════════
    (7406, "example_uk",
     "Кіт дряпає кігтями двері",
     "Кіт дряпає кігтями диван",
     "двери вместо дивана: эталон «in die Couch»"),
    (3067, "example_tr",
     "Ailemle birlikte yaşamak uyumlu",
     "Anne babamla birlikte yaşamak uyumlu",
     "«ailem» это вся семья; эталон «mit meinen Eltern» — родители"),
    (9823, "example_uk",
     "Доходи бізнесу зросли",
     "Доходи магазину зросли",
     "`Geschäft` это магазин; в ru, tr и pl магазин"),
    (14082, "example_uk",
     "Я отримав важливого листа на електронну пошту",
     "Я отримав важливий електронний лист",
     "«листа» одушевлённый винительный у неживого"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (2434, "example_uk",
     "Це полегшує роботу",
     "Це полегшує мені роботу",
     "потеряно «mir»: в остальных четырёх оно есть"),
    (16327, "example_pl",
     "Terroryzm to poważny problem na świecie",
     "Terroryzm to duży problem",
     "«na świecie» в эталоне нет"),
    (18258, "example_ru",
     "Гостевая комната очень красивая",
     "Гостевая комната красивая",
     "«очень» в эталоне «ist schön» нет"),
    (7410, "example_ru",
     "Это вызвало настоящую сенсацию",
     "Это вызвало большую сенсацию",
     "«настоящую» вместо «großes»"),
    (819, "example_pl",
     "Mój teść pomaga w ogrodzie",
     "Teść pomaga w ogrodzie",
     "«Mój» в эталоне нет; в остальных четырёх его тоже нет"),
    (15104, "example_uk",
     "У дитини гарна головка",
     "У дитини мила головка",
     "`niedlich` это милый, а не красивый; в ru «милая»"),
    (10726, "example_tr",
     "Bu kadar işle kendimi bunalmış hissediyorum",
     "Bütün bu işlerle tamamen bunaldım",
     "потеряно «total», и добавлено «kendimi hissediyorum»"),
    (7412, "example_tr",
     "Filmin ortasındaydık, ışıklar söndü",
     "Işıklar söndüğünde filmin tam ortasındaydık",
     "потеряна связка «als», и «tam ortasında» стоит в списке первым"),
    (12214, "example_pl",
     "Zapisałem się do klubu piłkarskiego",
     "Jestem członkiem klubu piłkarskiego",
     "«записался» вместо «bin Mitglied»"),
    (16335, "example_pl",
     "Policja zrobiła nalot na magazyn",
     "Policja przeprowadziła nalot na magazyn",
     "«zrobić nalot» разговорно; об операции говорят «przeprowadzić»"),

    # ══ форма и время ═══════════════════════════════════════════
    (10706, "example_pl",
     "Nie ustąpię i nie zmienię zdania",
     "Nie ustępuję i nie zmieniam zdania",
     "будущее против «Ich gebe nicht nach»; в ru и uk настоящее"),
    (10708, "example_pl",
     "Wygląda na błogo szczęśliwego",
     "Wygląda błogo",
     "два значения списка слиты в одно; эталон «Er sieht selig aus»"),
    (14540, "example_tr",
     "Kral bir kriptada gömülü",
     "Kral bir kriptada gömülüdür",
     "без связки фраза не закончена"),
    (16325, "example_tr",
     "O, tek hücrede tutulmuştur",
     "O, tek kişilik hücrede tutuluyor",
     "«tek hücre» это одна клетка; в списке «tek kişilik hücre»"),
    (7422, "example_tr",
     "Bu şehre hedefli bir saldırıydı",
     "Şehre hedefli bir saldırıydı",
     "«Bu şehre» читается как «в этот город»"),
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
