"""
Сплошная вычитка, блок 25: ряды 3301–3500 по рангу частотности
(id первого 7031, id последнего 7072).

Находки:

* `Haft` — числа разошлись в трёх языках: немецкий «drei Jahre»,
  английский «ten years», украинский «п'ять років», а русский вообще про
  выход из заключения прошлой весной. Это прямая порча знаний.
* `verkleidet` — немецкий пришёл на вечеринку пиратом, украинский
  клоуном.
* `mächtig` — турецкое «O güçlü bir patlamadı». «Patlamadı» это «не
  взорвался», а нужно «patlamaydı». Отрицание вместо утверждения.
* `eintreten`, `erben`, `Überwachung`, `gratulieren`, `Chefin`,
  `tagsüber`, `Abwesenheit`, `abgelaufen`, `stundenlang`, `gewinnen`,
  `Schirm`, `Anwesen` — перевод переводит другую фразу.
* Английские апострофы, продолжение класса `fix_en_contractions`: «or
  well miss the train» (we'll), «the companys staff», «the directors
  approval», «the mens restroom», «the bus drivers strike».
* `igitt` — турецкие значения с заглавных: «İyy, Öf, Ööö». Прошлый
  прогон класса не охватил часть речи OTHER, теперь охвачен.
* `Kompanie` — ряд про воинское подразделение, а русский, украинский и
  турецкий переводили «компания» и «şirket».
* `Hamburger` — в русских значениях «жительгамбурга» слитно.
* `Dummheit` — турецкое «aptalıktı», `schlucken` — «yutıyor`,
  `Wohnwagen` — украинское «на караване». Опечатки.
* `streifen` — украинское «дотикнувся»: такого слова нет.

    python -m app.scripts.fix_block_0025            # показать
    python -m app.scripts.fix_block_0025 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- неверное число: прямая порча знаний ----------------------------------
    (16128, "example_en", "He faces ten years of imprisonment",
     "He spent three years in prison",
     "немецкий «Er saß drei Jahre in Haft» — три года, а не десять"),
    (16128, "example_ru", "Он вышел из заключения прошлой весной",
     "Он сидел три года в заключении", "то же"),
    (16128, "example_uk", "Йому дали п'ять років ув'язнення",
     "Він сидів три роки у в'язниці", "то же: было пять лет вместо трёх"),

    # --- английский апостроф (продолжение класса) -----------------------------
    (7048, "example_en", "We must go quickly or well miss the train",
     "We must go quickly or we'll miss the train",
     "«well» вместо «we'll»"),
    (9196, "example_en", "The companys staff is very competent",
     "The company's staff is very competent",
     "пропущен притяжательный апостроф"),
    (13993, "example_en", "We need the directors approval for this project",
     "We need the director's approval for this project", "то же"),
    (18422, "example_en",
     "The mens restroom is at the end of the hall on the left",
     "The men's restroom is at the end of the hall on the left", "то же"),
    (8913, "example_en", "The bus drivers strike lasted three weeks",
     "The bus drivers' strike lasted three weeks", "то же"),

    # --- значение с заглавной (часть речи OTHER) ------------------------------
    (10445, "translation_tr", "İyy, Öf, Ööö", "iyy, öf, ööö",
     "значения с заглавных букв"),
    (10445, "example_tr", "İğğ, bu iğrenç", "İyy, bu iğrenç!",
     "в значениях «iyy», и потерян восклицательный знак"),

    # --- пример переводит другую фразу ---------------------------------------
    (13660, "example_uk", "Він прийшов переодягнений у клоуна",
     "Він прийшов на вечірку переодягнений у пірата",
     "в немецком пират, а не клоун"),
    (13660, "example_tr", "Partiye kıyafet değiştirmiş olarak geldi",
     "Partiye korsan kılığında geldi", "потерян пират"),
    (7050, "example_en", "Please knock before you enter",
     "You may enter now", "немецкий «Sie dürfen jetzt eintreten»"),
    (7050, "example_uk", "Якщо цей випадок настане, ми швидко діятимемо",
     "Тепер ви можете увійти", "то же"),
    (7050, "example_tr", "Bu durum meydana gelirse hızlı hareket edeceğiz",
     "Şimdi girebilirsiniz", "то же"),
    (16132, "example_uk", "Діти успадковують очі батьків",
     "Вона успадкує дім від своєї бабусі",
     "немецкий «Sie wird das Haus von ihrer Großmutter erben»"),
    (17527, "example_uk", "Діти граються під наглядом учительки",
     "Нагляд за будівельним майданчиком ведеться цілодобово",
     "немецкий «Die Überwachung der Baustelle läuft rund um die Uhr»"),
    (10438, "example_uk", "Хочу привітати тебе з днем народження",
     "Вітаю тебе з твоїм успіхом",
     "немецкий «Ich gratuliere dir zu deinem Erfolg»"),
    (8857, "example_tr", "Patronum bugün bana izin verdi",
     "Kadın patron tüm çalışanları ofise davet etti",
     "немецкий «Die Chefin hat alle Mitarbeiter ins Büro eingeladen»"),
    (18712, "example_pl", "W ciągu dnia nikogo nie ma w domu",
     "W ciągu dnia pracuję w biurze, wieczorem w domu",
     "немецкий «Tagsüber arbeite ich im Büro, am Abend zu Hause»"),
    (18708, "example_pl", "Podczas mojej nieobecności podlej kwiaty",
     "Z powodu swojej nieobecności przegapiłeś spotkanie",
     "немецкий «Wegen deiner Abwesenheit hast du die Besprechung verpasst»"),
    (18707, "example_pl", "Ten jogurt jest już przeterminowany",
     "Twój paszport jest nieważny", "немецкий «Dein Pass ist abgelaufen»"),
    (18706, "example_pl", "Potrafi godzinami gadać przez telefon",
     "Ona pracuje godzinami", "немецкий «Sie arbeitet stundenlang»"),
    (7035, "example_en", "I really hope we win tomorrow",
     "He won the game against his friend",
     "немецкий «Er gewann das Spiel gegen seinen Freund»"),
    (13659, "example_pl", "Weź parasol, bo pada",
     "Zapomniałem parasola, a teraz pada",
     "немецкий «Ich habe meinen Schirm vergessen, jetzt regnet es»"),
    (18197, "example_ru", "Они купили старое поместье под городом",
     "Поместье расположено на большом участке за городом",
     "немецкий «Das Anwesen liegt auf einem großen Grundstück»"),
    (15028, "example_uk", "Наша кицька спить на дивані",
     "Кицька сидить на підвіконні й дивиться надвір",
     "немецкий «Die Muschi sitzt auf der Fensterbank»"),

    # --- `Kompanie`: ряд про воинское подразделение ---------------------------
    (17787, "example_ru", "Компания была очень успешна",
     "Рота была очень успешной",
     "«Kompanie» — рота; «компания» это первое значение в списке"),
    (17787, "example_uk", "Компанія була дуже успішна в бізнесі",
     "Рота була дуже успішною", "то же, и бизнеса в немецком нет"),
    (17787, "example_tr", "Şirket işte çok başarılı oldu",
     "Bölük çok başarılı oldu", "то же"),

    # --- потеряно или добавлено ------------------------------------------------
    (258, "example_en", "In February it is cold",
     "In February it is often cold and it snows a lot",
     "потеряно «und es schneit viel»"),
    (258, "example_tr", "Şubat ayında hava soğuk",
     "Şubat ayında hava sık sık soğuk olur ve çok kar yağar", "то же"),
    (258, "example_pl", "W lutym jest zwykle bardzo zimno",
     "W lutym jest często zimno i pada dużo śniegu", "то же"),
    (1932, "example_en", "He has a tattoo",
     "He has a big tattoo on his arm", "потеряно «großes» и «auf dem Arm»"),
    (1932, "example_uk", "У нього є тату",
     "У нього велике тату на руці", "то же"),
    (1932, "example_tr", "Onun bir dövmesi var",
     "Kolunda büyük bir dövmesi var", "то же"),
    (1647, "example_en", "He is doing an apprenticeship",
     "He is doing an apprenticeship as an electrician",
     "потеряно «zum Elektriker»"),
    (1647, "example_uk", "Він проходить професійне навчання",
     "Він проходить професійне навчання на електрика", "то же"),
    (1647, "example_tr", "Elektrikçi olarak mesleki eğitim yapıyor",
     "Elektrikçi olarak çıraklık eğitimi yapıyor",
     "в значениях «çıraklık eğitimi»"),
    (12583, "example_uk", "Хвороба сильно ослабила його організм",
     "Довга хвороба сильно ослабила його",
     "потеряно «долгая», и организма в немецком нет"),
    (13990, "example_uk", "Вони шепчуть один одному на уроці",
     "Вони шепчуть один одному щось на уроці", "потеряно «etwas»"),
    (12174, "example_en", "That's a piece of cake, I can manage that easily",
     "That's a piece of cake for me",
     "«я легко справлюсь» в немецком нет"),
    (12174, "example_ru", "Для меня это детская игра!",
     "Для меня это пустяк!",
     "«детская игра» дословно; в значениях стоит «пустяк»"),
    (12174, "example_uk", "Це дитяча гра, я легко впораюся",
     "Для мене це дурниця!", "то же"),

    # --- слова, которых нет в языке, и опечатки -------------------------------
    (6707, "example_tr", "O güçlü bir patlamadı",
     "O güçlü bir patlamaydı",
     "«patlamadı» — «не взорвался»; нужно «patlamaydı»"),
    (11707, "translation_ru", "гамбургер, бургер, жительгамбурга",
     "гамбургер, бургер, житель Гамбурга",
     "«жительгамбурга» — слипшиеся слова"),
    (10442, "example_tr", "Bu benim için gerçek bir aptalıktı",
     "Bu gerçekten benim aptallığımdı",
     "«aptalıktı» — опечатка, и «benim için» не то"),
    (11708, "example_tr", "Çocuk hapı suyla yutıyor",
     "Çocuk hapı suyla yutuyor", "«yutıyor» — опечатка"),
    (3029, "example_uk", "Ми їдемо у відпустку на нашому караване",
     "Ми їдемо у відпустку нашим караваном", "«на караване» — не та форма"),
    (3029, "translation_uk",
     "житловий прицеп, караван, дім на колесах",
     "житловий причіп, караван, дім на колесах", "«прицеп» — русизм"),
    (7044, "example_uk", "Він ледь дотикнувся її руки",
     "Він ледь торкнувся її руки", "«дотикнувся» — такого слова нет"),
    (10440, "example_uk", "Я почуваюся дуже почитаним",
     "Я почуваюся дуже вшанованим", "«почитаним» — не то слово"),
    (15490, "translation_uk", "червяк, хробак", "черв'як, хробак",
     "пропущен апостроф: «черв'як»"),
    (15490, "example_uk", "У саду багато хробаків, які добре для грунту",
     "У саду багато хробаків, які добрі для ґрунту",
     "«які добре» не согласовано, и «ґрунт» с «ґ»"),
    (7057, "example_uk", "Ми йдемо разом на меса до церкви",
     "Ми йдемо разом на месу до церкви", "«на меса» — не та форма"),
    (10447, "translation_uk", "пригнічений, подавлений, у депресії",
     "пригнічений, прибитий, у депресії", "«подавлений» — русизм"),
    (10442, "example_uk", "Це була справжня дурість з моєї сторони",
     "Це була справжня дурість з мого боку", "«з моєї сторони» — русизм"),
    (7040, "example_uk", "Він пристально дивився на стіну",
     "Він пильно дивився на стіну", "«пристально» — русизм"),

    # --- грамматика целевого языка --------------------------------------------
    (10434, "example_uk", "Вона люблячої матері", "Вона любляча мати",
     "фраза не складывается"),
    (13994, "example_tr",
     "Öğretmenler daha çalışkan çalışması gerektiğini düşündüler",
     "Öğretmenler onun daha çok çalışması gerektiğini düşündü",
     "«daha çalışkan çalışması» — так не говорят"),
    (15029, "example_tr", "Ortağım ve ben gelecek için büyük planlarımız var",
     "Partnerim ve benim gelecek için büyük planlarımız var",
     "пропущен родительный падеж"),
    (15030, "example_uk",
     "Мати годує своєї дитини грудьми в залі очікування",
     "Мати годує свою дитину грудьми в залі очікування",
     "неверный падеж"),
    (15030, "example_tr", "Bebeği emzirmek için odaya geçti",
     "Anne bekleme odasında bebeğini emziriyor",
     "немецкий «Die Mutter stillt ihr Baby im Wartezimmer»"),
    (12582, "example_tr", "Ceket olmadığı için soğuktan titriyor",
     "Ceketi olmadığı için soğuktan titriyor",
     "пропущен притяжательный аффикс"),
    (16129, "example_tr", "Ceketi altında bir hançer gizledi",
     "Ceketinin altında bir hançer sakladı", "пропущен родительный падеж"),
    (15027, "example_tr",
     "Felaketinden sonra yaşamaya devam etmek zorunda kaldı",
     "Felaketten sonra yaşamaya devam etmek zorunda kaldı",
     "«Felaketinden» — его катастрофа"),
    (15025, "example_tr", "Eski arkadaşımla buluşma gerçekten güzeldi",
     "Eski arkadaşımla buluşmam gerçekten güzeldi",
     "пропущен притяжательный аффикс"),
    (13511, "example_tr", "Kitaplar masada birinin üzerine istiflenmiş duruyor",
     "Kitaplar masada üst üste istiflenmiş duruyor",
     "«birinin üzerine» — на чьём-то"),
    (7051, "example_uk", "Вона скрізь шукала свою втрачену кішку",
     "Вона скрізь шукала свою загублену кішку",
     "«втрачену» — об умершей; потерялась это «загублена»"),
    (12175, "example_tr", "Biz oyuna katılmak ister misin?",
     "Oyuna katılmak ister misin?", "«Biz» с «ister misin» не вяжется"),
    (15491, "example_uk", "Бджоли гудять навколо квітів",
     "Бджоли дзижчать навколо квітів",
     "в значениях первым стоит «дзижчати», и так точнее"),
    (7053, "example_uk",
     "Будь ласка, тримай таксі в готівності, якщо мені його потрібно",
     "Будь ласка, тримай таксі наготові, якщо воно мені знадобиться",
     "«в готівності» и «якщо мені його потрібно» — не по-украински"),
    (7053, "example_tr", "Lütfen ihtiyacım olursa bir taksi hazırda tutun",
     "Lütfen ihtiyacım olursa diye bir taksiyi hazır tut",
     "порядок слов, и «tutun» — обращение на «вы»"),
    (14456, "example_uk", "Святість цього місця була поважана усіма",
     "Святість цього місця всі шанували", "«була поважана» — калька"),
    (7037, "example_uk",
     "Вони тримаються один за одного, неважливо що відбувається",
     "Вони тримаються один за одного, що б не сталося",
     "«неважливо що» — калька"),
    (7037, "example_pl",
     "Oni trzymają się razem, pasują do siebie, cokolwiek się stanie",
     "Oni trzymają się razem, cokolwiek się stanie",
     "вставка «pasują do siebie» лишняя"),

    # --- подменённое значение -------------------------------------------------
    (17130, "example_ru", "Номерной знак твоей машины закончился",
     "Номерной знак твоей машины просрочен",
     "«знак закончился» — так не говорят"),
    (17130, "example_uk", "Номерний знак твоєї машини застарів",
     "Номерний знак твоєї машини прострочений", "то же"),
    (18707, "example_ru", "Твой паспорт истёк",
     "Твой паспорт просрочен", "«паспорт истёк» — так не говорят"),
    (18707, "example_uk", "Твій паспорт закінчився",
     "Твій паспорт прострочений", "то же"),
    (9781, "example_uk", "Собака просить їжу", "Собака випрошує їжу",
     "в значениях «випрошувати»"),
    (8855, "example_uk", "Чиновник працює в уряді",
     "Чиновник працює на уряд", "немецкий «arbeitet für die Regierung»"),
    (15028, "example_en",
     "The cat is sitting on the windowsill looking outside",
     "The kitty is sitting on the windowsill looking outside",
     "ряд про кошечку, а не про кошку вообще"),
    (15028, "example_tr",
     "Kedi pencere eşiğinde oturuyor ve dışarı bakıyor",
     "Pisi pencere eşiğinde oturuyor ve dışarı bakıyor", "то же"),
    (9477, "example_tr", "Telefon numarasını ezberden biliyorum",
     "Telefon numarasını ezbere biliyorum", "в значениях «ezbere»"),
    (10451, "example_tr", "Çikolata yeme ayartısı büyük",
     "Çikolata yemenin cazibesi büyük", "«ayartısı» — так не говорят"),
    (15493, "example_pl", "Ręcznik jest jeszcze wilgotny po kąpieli",
     "Ręcznik jest jeszcze wilgotny po prysznicu",
     "в немецком душ, а не ванна"),
    (10449, "example_tr", "O, sayılabilecek sadık bir arkadaş",
     "O, güvenilebilecek sadık bir arkadaş",
     "«sayılabilecek» — исчисляемый"),
    (7058, "example_uk", "Картина ідеально підходить в рамку",
     "Картина ідеально підходить до рамки", "неверный предлог"),
    (10450, "example_uk", "Він зовсім закоханий у свою однокласницю",
     "Він по вуха закоханий у свою однокласницю",
     "«total verknallt» — по уши"),
    (7045, "example_tr", "Arabanın her yerde duyulan gür bir klaksonu var",
     "Arabanın her yerde duyulan yüksek sesli bir klaksonu var",
     "«gür» о звуке так не говорят"),

    # --- говорить по-людски ---------------------------------------------------
    (13989, "example_tr", "Bu gizli bilgidir", "Bu gizli bir bilgi",
     "«-dir» — канцелярит"),
    (10434, "example_tr", "O sevgi dolu bir annedir",
     "O sevgi dolu bir anne", "то же"),
    (17526, "example_tr", "Bu teknik bir sorundur",
     "Bu teknik bir sorun", "то же"),
    (18197, "example_tr",
     "Mülk şehrin dışında geniş bir arsada bulunmaktadır",
     "Mülk şehrin dışında geniş bir arsada bulunuyor", "то же"),
    (7032, "example_tr", "Askerler şehre yürüyüş yapıyorlar",
     "Askerler şehre doğru yürüyor",
     "«yürüyüş yapmak» — гулять, а не идти строем"),
    (18194, "example_tr", "Kışın şöminenin önünde sık oturuyoruz",
     "Kışın sık sık şöminenin önünde oturuyoruz", "порядок слов"),
    (18193, "example_tr", "Odun kırmak için baltayı aldı",
     "Odun kesmek için baltayı aldı", "дрова рубят, а не бьют"),
    (17129, "example_tr", "Paket posta gelmişti",
     "Paket posta ile geldi", "пропущено «ile»"),
    (8854, "example_tr", "Bekçi tutukluları gözetiyor",
     "Gardiyan tutukluları gözetliyor",
     "в значениях первым стоит «gardiyan»"),
    (10440, "example_tr", "Kendimi çok onurlandırılmış hissediyorum",
     "Çok onur duydum", "по-турецки так и говорят"),
    (8851, "example_en", "The janitor is fixing the heating",
     "The janitor takes care of the heating in the building",
     "немецкий «kümmert sich um die Heizung im Gebäude»"),
    (8851, "example_tr", "Kapıcı ısıtmayı onarıyor",
     "Kapıcı binadaki ısıtmayla ilgileniyor", "то же"),
    (2174, "example_tr", "Onun çalışmasının tanınması onun için önemliydi",
     "Çalışmasının takdir edilmesi onun için önemliydi",
     "«onun» сказано дважды"),
    (7052, "example_uk", "Наповнену сумку було важко носити",
     "Наповнену сумку було дуже важко нести",
     "«носити» — постоянно; и потеряно «очень»"),
    (13995, "example_tr", "Hoşça kalın, arkadaşım! Yakında görüşürüz",
     "Hoşça kal, arkadaşım! Yakında görüşürüz",
     "«kalın» — на «вы», а дальше «arkadaşım»"),
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
