"""
Сплошная вычитка, блок 24: ряды 3101–3300 по рангу частотности
(id первого 1923, id последнего 14453).

Находки:

* Три заголовка с неверным регистром: `ÄCHZEN` заглавными, `Knarren` и
  `Hochachtungsvoll` с заглавной там, где немецкий требует строчной —
  это глагол и наречие, а не существительные. Сплошной поиск по регистру
  заголовков показал, что других таких нет: остальные заглавные — это
  аббревиатуры (NATO, IBAN, DVD, WC) и вежливые «Sie», «Ihnen».
* `Lügnerin` — битый эталон: «Sie ist eine Lügnerin und kann ihr kein
  Wort glauben». Пропущено «man», фраза не складывается.
* `hacken` — русский рассказывал про воров и дверь, украинский про деда
  и дрова, турецкий про колку дров на зиму. Немецкий: «Der Hacker
  versucht, die Website zu hacken».
* `sich umsehen`, `ergreifen`, `siegen`, `beruflich`, `klettern`,
  `Feierabend`, `demselben`, `Schwager`, `parken`, `Klemme` — то же:
  перевод переводит другую фразу.
* `Gestank` — украинское «жахливий смерд». «Смерд» — крепостной
  крестьянин, а не запах.
* `Ablenkung` — украинское «розсіяння від моїх проблем».
* `grob` — турецкое «hakarettı», `Rollstuhl` — «Büyükbabaam»,
  `abgeschnitten` — польское «resztyitego». Опечатки.
* `grauen` — украинское «Мені жахко»: такого слова нет.
* Турецкое «-dir» в разговорных фразах: `Kürze`, `überraschend`,
  `geschützt`, `Schrott`, `Profil`, `Erpressung`.

    python -m app.scripts.fix_block_0024            # показать
    python -m app.scripts.fix_block_0024 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- заголовок с неверным регистром ---------------------------------------
    (12571, "word_de", "ÄCHZEN", "ächzen",
     "заголовок заглавными; это глагол, в примере он стоит как «ächzt»"),
    (18213, "word_de", "Knarren", "knarren",
     "глагол с заглавной; в примере «Die Dielen knarren»"),
    (14311, "word_de", "Hochachtungsvoll", "hochachtungsvoll",
     "наречие с заглавной; в примере «hochachtungsvollem»"),

    # --- немецкий эталон -------------------------------------------------------
    (10410, "example_de",
     "Sie ist eine Lügnerin und kann ihr kein Wort glauben",
     "Sie ist eine Lügnerin und man kann ihr kein Wort glauben",
     "пропущено «man» — фраза не складывается"),

    # --- пример переводит другую фразу ---------------------------------------
    (17524, "example_ru", "Воры начали взламывать дверь",
     "Хакер пытается взломать сайт",
     "немецкий «Der Hacker versucht, die Website zu hacken»"),
    (17524, "example_uk", "Дід рубає дрова у дворі",
     "Хакер намагається зламати сайт", "то же"),
    (17524, "example_tr", "Kış için odunu kesiyorum",
     "Hacker web sitesini hacklemeye çalışıyor", "то же"),
    (7012, "example_en", "Let's look around the shop first",
     "I just want to look around for a moment",
     "немецкий «Ich will mich nur kurz umsehen»"),
    (7012, "example_uk", "Він озирнувся й побачив мене",
     "Я хочу тільки трохи роззирнутися", "то же"),
    (7012, "example_tr", "İçeri girince etrafına bakındı",
     "Sadece kısaca etrafa bakmak istiyorum", "то же"),
    (6993, "example_en", "The police seized the thief on the street",
     "You have to seize the chance",
     "немецкий «Du musst die Chance ergreifen»"),
    (6993, "example_uk", "Поліція схопила злодія на вулиці",
     "Ти повинен ухопитися за цей шанс", "то же"),
    (6993, "example_tr", "Polis hırsızı sokakta yakaladı",
     "Bu şansı yakalamalısın", "то же"),
    (2815, "example_uk", "Наша команда перемагає сьогодні вечором",
     "Наша команда переможе сьогодні ввечері",
     "немецкий «wird siegen» — будущее, и «сьогодні вечором» — калька"),
    (2815, "example_tr", "Kazanıyoruz", "Takımımız bu akşam kazanacak",
     "потеряно всё, кроме глагола"),
    (97, "example_uk", "Він грає на гітарі професійно",
     "Я багато їжджу по роботі",
     "немецкий «Ich bin beruflich viel unterwegs»"),
    (97, "example_tr", "Akşamları mesleki bir kursa gidiyorum",
     "İş için çok seyahat ediyorum", "то же"),
    (2607, "example_uk", "Я люблю лазити", "На вихідних я лажу по горах",
     "немецкий «Am Wochenende klettere ich in den Bergen»"),
    (2607, "example_tr", "Tırmanmayı severim",
     "Hafta sonları dağlarda tırmanıyorum", "то же"),
    (260, "example_uk", "У мене кінець робочого дня о шостій",
     "Кінець робочого дня! Ходімо",
     "немецкий «Feierabend! Lass uns gehen»"),
    (260, "example_tr", "Mesai bitti", "Paydos! Hadi gidelim", "то же"),
    (260, "example_en", "It's the end of the workday",
     "End of the workday! Let's go", "то же"),
    (13510, "example_uk", "Ми ходимо в той самий спортзал",
     "Він говорить з тим самим чоловіком",
     "немецкий «Er spricht mit demselben Mann»"),
    (15020, "example_uk", "Мій швагер допоміг нам із ремонтом",
     "Мій швагер — лікар", "немецкий «Mein Schwager ist Arzt»"),
    (2710, "example_uk", "Тут паркуватися суворо заборонено",
     "Я паркую свою машину тут", "немецкий «Ich parke mein Auto hier»"),
    (7001, "example_tr", "Bir sıkıntı olursa hemen beni ara",
     "Zor bir durumdayım", "немецкий «Ich bin in einer Klemme»"),
    (11693, "example_uk", "Це був найсмачніший прийом їжі за тиждень",
     "Обід був смачною трапезою",
     "немецкий «Das Mittagessen war eine leckere Mahlzeit»"),
    (18704, "example_pl", "W sezonie jest tu mnóstwo turystów",
     "Sezon letni zaczyna się w czerwcu",
     "немецкий «Die Sommersaison beginnt im Juni»"),
    (2435, "example_uk", "Він харчується переважно овочами",
     "Я харчуюся здорово і збалансовано",
     "немецкий «Ich ernähre mich gesund und ausgewogen»"),
    (85, "example_uk", "Налий мені кухоль чаю", "Я п'ю каву з кухля",
     "немецкий «Ich trinke Kaffee aus einem Becher»"),
    (18702, "example_pl", "Cenię zwięzłość w e-mailach",
     "Zwięzłość tego wyjaśnienia jest ważna",
     "немецкий «Die Kürze dieser Erklärung ist wichtig»"),
    (12167, "example_tr", "Çocuk yayla ok atıyor",
     "Okçu yayıyla nişan alıyor",
     "немецкий «Der Bogenschütze zielt mit seinem Bogen»"),
    (12167, "example_pl", "Chłopiec strzela z łuku do tarczy",
     "Łucznik celuje ze swojego łuku", "то же"),
    (13983, "example_uk", "Пес ричить на незнайомця",
     "Тигр гучно рикає в зоопарку",
     "немецкий «Der Tiger brüllt laut im Zoo»"),

    # --- потеряно или добавлено ------------------------------------------------
    (9472, "example_uk", "Я про це не знаю",
     "У мене немає про це жодних знань", "потеряно само слово «знання»"),
    (2710, "example_en", "I park here", "I park my car here",
     "потеряно «mein Auto»"),
    (1461, "example_en", "That endangers safety",
     "That endangers public safety", "потеряно «öffentliche»"),
    (1461, "example_uk", "Це наражає громадськість на небезпеку",
     "Це ставить під загрозу громадську безпеку", "то же"),
    (1461, "example_tr", "Bu güvenliği tehlikeye atıyor",
     "Bu kamu güvenliğini tehlikeye atıyor", "то же"),
    (2142, "example_en", "I am financially dependent",
     "I am financially dependent on my parents",
     "потеряно «von meinen Eltern»"),
    (2142, "example_tr", "Maddi olarak bağımlıyım",
     "Maddi olarak aileme bağımlıyım", "то же"),
    (2999, "example_uk", "Тепло приємне",
     "Тепло сонця сьогодні приємне", "потеряно «солнца» и «сегодня»"),
    (2999, "example_tr", "Sıcaklık hoş",
     "Güneşin sıcaklığı bugün hoş", "то же"),
    (3065, "example_tr", "İş birliği iyi",
     "Takımla iş birliği çok verimli",
     "потеряно «с командой» и «очень продуктивно»"),
    (12575, "example_uk", "У мене йде кров з носа",
     "У мене починає йти кров з носа", "потеряно «fängt an»"),
    (12575, "example_tr", "Burnumdan kan geliyor",
     "Burnumdan kan gelmeye başlıyor", "то же"),
    (1150, "example_uk", "Дотримуйтесь інструкцій",
     "Будь ласка, дотримуйся інструкцій",
     "потеряно «bitte», и в немецком обращение на «ты»"),
    (1150, "example_tr", "Talimatlara uyun", "Lütfen talimatlara uy",
     "то же"),

    # --- слова, которых нет в языке, и опечатки -------------------------------
    (7007, "example_uk", "У ванній кімнаті був жахливий смерд",
     "У ванній кімнаті був жахливий сморід",
     "«смерд» — крепостной крестьянин, а не запах"),
    (7007, "translation_uk", "сморід, вонь", "сморід, смердота",
     "«вонь» — русизм"),
    (7002, "example_uk", "Мені жахко перед екзаменом",
     "Мене жахає екзамен", "«жахко» — такого слова нет"),
    (10418, "example_uk", "Мені потрібне розсіяння від моїх проблем",
     "Мені потрібно відволіктися від своїх проблем",
     "«розсіяння» — рассеивание, а не отвлечение"),
    (7005, "example_tr", "Bu kaba bir hakarettı",
     "Bu kaba bir hakaretti", "«hakarettı» — опечатка"),
    (12576, "example_tr", "Büyükbabaam tekerlekli sandalyede oturuyor",
     "Büyükbabam tekerlekli sandalyede oturuyor",
     "«Büyükbabaam» — двойная «a»"),
    (6991, "example_pl",
     "Z powodu burzy jesteśmy odcięci od resztyitego świata",
     "Z powodu burzy jesteśmy odcięci od reszty świata",
     "«resztyitego» — склеенные слова"),
    (16114, "example_uk", "Згвалтування було тяжким злочином",
     "Зґвалтування було тяжким злочином",
     "в значениях стоит «зґвалтування» с «ґ»"),

    # --- грамматика целевого языка --------------------------------------------
    (6992, "example_uk", "Можеш ти мені в'язати шнурки?",
     "Можеш зав'язати мені шнурки?", "порядок слов и вид глагола"),
    (10410, "example_uk", "Вона брехунька, і їй не можна вірити ні слова",
     "Вона брехуха, і їй не можна вірити ні на слово",
     "«брехунька» нет в значениях, и «вірити ні слова» — не та форма"),
    (10410, "example_tr", "O bir yalancı ve ona bir kelime dahi inanmak olmaz",
     "O bir yalancı ve söylediği hiçbir şeye inanılmaz",
     "фраза не складывается"),
    (9471, "example_uk", "Він вчена людина, яка багато знає про історію",
     "Він учений чоловік, який багато знає про історію",
     "«він» с «людина» не согласуется"),
    (16113, "example_tr", "Müdür okulda büyük otoritesi vardır",
     "Müdürün okulda büyük otoritesi var", "пропущен родительный падеж"),
    (6995, "example_tr", "O, diz çöktü ve affını istedi",
     "Diz çöküp af diliyor",
     "в немецком настоящее время, и «affını istedi» — не то"),
    (15022, "example_tr", "Doktora gitmek için eşlik etmesi gerekiyor",
     "Doktora gitmek için bana eşlik edecek birine ihtiyacım var",
     "фраза не складывается"),
    (10420, "example_uk", "Це мені чужо", "Це мені незнайоме",
     "«чужо» — не та форма"),
    (7011, "example_tr", "Dik otur, bükülmedin",
     "Dik otur, kamburunu çıkarma",
     "«bükülmedin» — «ты не согнулся», а нужен запрет"),
    (15023, "example_tr", "Adamın şekli uzun ve ince idi",
     "Adamın figürü uzun ve inceydi",
     "«şekli» — форма предмета, и «idi» пишется слитно"),
    (11693, "example_tr", "Öğle yemeği lezzetli bir öğün idi",
     "Öğle yemeği lezzetli bir öğündü", "«idi» пишется слитно"),
    (10411, "example_tr",
     "O merhametli bir kraliçe idi ve yoksul insanlara yardım etti",
     "O merhametli bir kraliçeydi ve yoksul insanlara yardım etti",
     "то же"),
    (13984, "example_tr", "Bu ondan güzel bir jest idi",
     "Bu, ondan güzel bir jestti", "то же"),
    (13979, "example_tr", "Bana yalan söylememeliydin",
     "Bana yalan söylememelisin", "в немецком настоящее время"),
    (10409, "example_uk", "Вона заздрісна моїй новій роботі",
     "Вона заздрить моїй новій роботі", "«заздрісна» — прилагательное"),
    (10409, "example_tr", "O, benim yeni işime kıskanç",
     "Yeni işimi kıskanıyor", "фраза не складывается"),
    (10419, "example_uk", "Ти дійсно параноїдний",
     "Ти дійсно параноїдальний", "в значениях стоит «параноїдальний»"),
    (16115, "example_ru", "Отвод войск начнётся на следующей неделе",
     "Вывод войск начнётся на следующей неделе",
     "в значениях стоит «вывод войск»"),
    (16115, "example_uk", "Відвід військ починається наступного тижня",
     "Виведення військ починається наступного тижня", "то же"),
    (2336, "example_uk", "Німеччина є демократією",
     "Німеччина — демократія", "«є» — канцелярит"),
    (16117, "example_uk", "Це вимагання і це незаконно",
     "Це шантаж, і це незаконно",
     "в русском «шантаж», и пропущена запятая"),

    # --- подменённое значение -------------------------------------------------
    (1923, "example_tr", "Çocuklar şekeri sever",
     "Çocuklar şekerlemeyi sever", "в немецком множественное число"),
    (9773, "example_uk", "Моя сумка червона", "Моя сумочка червона",
     "в значениях стоит «сумочка»"),
    (9773, "example_tr", "Benim çantam kırmızı", "El çantam kırmızı",
     "в значениях стоит «el çantası»"),
    (2831, "example_tr", "Film heyecanlı",
     "Film gerçekten heyecan verici",
     "«heyecanlı» — взволнованный; в значениях «heyecan verici»"),
    (11698, "example_tr", "Kahvaltıda pastırma ve yumurta yemeyi seviyorum",
     "Kahvaltıda domuz pastırması ve yumurta yemeyi seviyorum",
     "«pastırma» — говяжья, а «Speck» это свиной бекон"),
    (7009, "example_tr", "Kapıyı çekme, itmen gerekiyor",
     "Kapıyı sola it!", "немецкий «Schieb die Tür nach links!»"),
    (17128, "example_tr", "Arabayı pazara doğru itiyorum",
     "El arabasını pazara doğru itiyorum",
     "«araba» — машина; в значениях «el arabası»"),
    (1693, "example_tr", "Seninle gelebilir miyim?",
     "Seninle birlikte gidebilir miyim?",
     "в значениях «birlikte gitmek»"),
    (768, "example_tr", "Onun sırt çantası var", "Sırt çantası taşıyor",
     "немецкий «Er trägt einen Rucksack» — носит, а не имеет"),
    (7003, "example_uk", "Ці туфлі не придатні для альпінізму",
     "Це взуття не придатне для гірського спорту",
     "«туфлі» и «альпінізм» — не то, что в немецком"),

    # --- говорить по-людски ---------------------------------------------------
    (10418, "example_ru", "Мне нужно отвлечение от своих проблем",
     "Мне нужно отвлечься от своих проблем", "«отвлечение» — канцелярит"),
    (10418, "example_tr", "Sorunlarımdan bir dikkat dağıtmaya ihtiyacım var",
     "Sorunlarımdan kafamı dağıtmaya ihtiyacım var", "фраза не складывается"),
    (12572, "example_uk", "Кожного ранку я беру таблетку від головного болю",
     "Кожного ранку я приймаю таблетку від головного болю",
     "таблетки приймають, а не беруть"),
    (15016, "example_tr", "Balayımızı Hawaiide geçiriyoruz",
     "Balayımızı Hawaii'de geçiriyoruz",
     "пропущен апостроф в имени собственном"),
    (18704, "example_tr", "Yaz sezonu Haziranda başlıyor",
     "Yaz sezonu Haziran'da başlıyor", "то же"),
    (2793, "example_tr", "Duvarındaki anahtar kapalı",
     "Duvardaki anahtar kapalı", "«Duvarındaki» — на твоей стене"),
    (935, "example_tr", "Doğum günü için severek pasta yaparım",
     "Doğum günü için pasta yapmayı severim", "«severek» — так не говорят"),
    (15020, "example_tr", "Benim eniştem doktor", "Eniştem doktor",
     "«Benim» лишнее"),
    (412, "example_uk", "Я їм мед на хлібі", "Я їм хліб з медом",
     "«мед на хлібі» — калька"),
    (18702, "example_tr", "Bu açıklamanın kısalığı önemlidir",
     "Bu açıklamanın kısalığı önemli", "«-dir» — канцелярит"),
    (10413, "example_tr", "Bu şaşırtıcı bir haberdir",
     "Bu şaşırtıcı bir haber", "то же"),
    (7000, "example_tr", "Veriler korunmuştur", "Veriler korunuyor",
     "то же"),
    (7004, "example_tr", "Eski araba artık sadece hurdadır",
     "Eski araba artık sadece hurda", "то же"),
    (17523, "example_tr", "Sosyal medya profilim özeldir",
     "Sosyal medya profilim özel", "то же"),
    (16117, "example_tr", "Bu şantaj ve yasadışıdır",
     "Bu şantaj ve yasa dışı", "то же"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            if was == now:
                continue
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(ok) + len(skipped)}, совпало {len(ok)}, "
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
