"""
Правки блока 59 (ряды 10101–10300, ранги 20571–21069).

Четыре сломанных эталона, и два из них — одна и та же ошибка:

    Der Kurs ist erfolgversprechend und wir sollten ihn einzuschlagen
    Man kann ihm nicht viel vorzuwerfen

После модального глагола (`sollen`, `können`, `müssen`, `wollen`,
`dürfen`, `mögen`) инфинитив идёт БЕЗ `zu`. В блоке 56 была обратная
ошибка — `Hör auf, mich runterziehen`, где `zu` наоборот потеряно.
Класс решаемый, из него выросла примета scan_de_zu_infinitive.

Ещё два:
  · `Albträume heimsuchen ihn jede Nacht` — приставка не отделена,
    нужно `suchen ihn … heim`. Примета scan_de_separable этого ряда
    не видит: у глаголов множественного числа личная форма совпадает
    с инфинитивом, и отличить склейку нельзя;
  · `Die Sera wird im Labor getestet` — `Sera` множественного числа,
    а сказуемое единственного.

Отдельная находка: русское `Они хаустят в старом заброшенном доме` —
слова «хаустить» в русском языке нет вообще. Машина построила форму от
немецкого `hausen` по русской морфологии.

    python -m app.scripts.fix_block_0059            # показать
    python -m app.scripts.fix_block_0059 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 10101 wohlbehalten
    (17348, "example_ru",
     "Она вернулась с путешествия целая и невредимая",
     "Она вернулась из путешествия целая и невредимая",
     "«с путешествия» — не то управление"),
    (17348, "example_tr", "Seyahatinden esenlik içinde geri döndü",
     "Seyahatinden sağ salim geri döndü",
     "перевод слова — «sağ salim»"),
    # 10104 Körpersprache
    (14278, "example_tr",
     "Onun beden dili sinirli olduğunu ortaya koyuyor",
     "Beden dili onun sinirli olduğunu ortaya koyuyor",
     "притяжание прицепилось не к тому слову"),
    # 10106 Fraktion
    (16777, "example_uk",
     "Зелена фракція в Бундестазі працює над климатичними цілями",
     "Зелена фракція в Бундестазі працює над кліматичними цілями",
     "«климатичними» — русское написание"),
    (16777, "example_tr",
     "Bundestagdaki yeşil fraksiyon iklim hedefleri üzerinde çalışıyor",
     "Bundestag'daki yeşil fraksiyon iklim hedefleri üzerinde çalışıyor",
     "потерян апостроф"),
    # 10107 Rüssel
    (15795, "example_tr", "Fil tutmak için kendi hortumunu kullanır",
     "Fil tutmak için hortumunu kullanır",
     "«kendi» лишнее при притяжательной форме"),
    # 10109 Anmerkung
    (9609, "example_tr", "Öğretmen makalemle ilgili birkaç nota ekledi",
     "Öğretmen makalemle ilgili birkaç not düştü",
     "«nota ekledi» это добавил к заметке"),
    # 10115 Massenmörder
    (16780, "example_en", "The serial killer was finally caught",
     "The mass murderer was finally caught",
     "«serial killer» это другое: убивает по одному"),
    (16780, "example_ru", "Серийного убийцу наконец поймали",
     "Массового убийцу наконец поймали",
     "«серийный убийца» это другое: убивает по одному"),
    # 10117 begnügen
    (11392, "example_en", "I'll settle for a smaller room",
     "He settled for less money",
     "перевод другого предложения"),
    (11392, "example_pl", "Musimy zadowolić się tym co mamy",
     "Zadowolił się mniejszą sumą pieniędzy",
     "перевод другого предложения"),
    # 10119 Vorstrafenregister
    (16781, "example_tr", "Adı suç kaydında var",
     "Adı sabıka kaydında var",
     "перевод слова — «sabıka kaydı»"),
    # 10120 ausrufen
    (14279, "example_en", "He exclaimed in despair",
     "The conductor calls out the next station",
     "перевод другого предложения"),
    (14279, "example_uk", "Він у розпачі вигукнув",
     "Кондуктор оголошує наступну станцію",
     "перевод другого предложения"),
    (14279, "example_tr", "Umutsuzluk içinde bağırdı",
     "Kondüktör sonraki istasyonu duyuruyor",
     "перевод другого предложения"),
    # 10121 verstörend
    (11393, "example_uk", "Це був неспокійний досвід для нього",
     "Це був тривожний досвід для нього",
     "«неспокійний» о состоянии, а не о впечатлении"),
    (11393, "example_pl", "To był bardzo niepokojący film",
     "To było dla niego niepokojące doświadczenie",
     "перевод другого предложения"),
    # 10122 Bulldozer
    (9216, "example_uk", "Бульдозер розбирав стару будівлю",
     "Бульдозер зніс стару будівлю",
     "эталон в совершённом виде"),
    # 10123 Halbschwester
    (15277, "example_uk", "Моя сводна сестра старша від мене",
     "Моя напівсестра старша за мене",
     "«сводна» — русизм, и «старша від» — калька"),
    (15277, "example_pl",
     "Moja siostra przyrodnia mieszka w Krakowie",
     "Moja siostra przyrodnia jest starsza ode mnie",
     "перевод другого предложения"),
    # 10124 Bärchen
    (15278, "example_uk",
     "Дитина гралася зі своїм плюшевим ведмедем",
     "Дитина гралася зі своїм плюшевим ведмедиком",
     "в эталоне уменьшительное «Bärchen»"),
    (15278, "example_pl", "Dziecko zasnęło z misiem w ręku",
     "Dziecko bawiło się swoim misiem",
     "перевод другого предложения"),
    # 10130 geistreich
    (11394, "example_uk", "Це була дотепна замітка з його боку",
     "Це було дотепне зауваження з його боку",
     "«замітка» это запись, а не реплика"),
    (11394, "example_tr", "O çok döteli bir yorum yaptı",
     "Esprili bir yorum yaptı",
     "«döteli» — нет такого слова"),
    # 10132 Unbehagen
    (11396, "example_pl", "Czułem lekki niepokój przed tą rozmową",
     "Niejasny niepokój wypełnił pokój",
     "перевод другого предложения"),
    # 10134 Tuberkulose
    (13033, "example_tr", "Verem 19. yüzyılda ölüm nedeni idi",
     "Verem 19. yüzyılda bir ölüm nedeniydi",
     "«idi» отдельно"),
    (13033, "example_pl", "Jego dziadek chorował na gruźlicę",
     "Gruźlica była w XIX wieku przyczyną śmierci",
     "перевод другого предложения"),
    # 10135 diktieren
    (14280, "example_pl", "Nauczyciel dyktował nam nowe słówka",
     "Podyktował list swojej sekretarce",
     "перевод другого предложения"),
    # 10136 Nominierung
    (9217, "example_tr", "Ödül için onun adaylığı şaşırtıcı idi",
     "Ödül için adaylığı şaşırtıcıydı",
     "«idi» отдельно, и лишнее «onun»"),
    # 10137 strippen — эталон во множественном, три перевода в единственном
    (9218, "example_en",
     "She does striptease at the nightclub for money",
     "They do striptease at the nightclub for money",
     "«Sie strippen» с множественным сказуемым это «они»"),
    (9218, "example_uk",
     "Вона танцює стриптиз у нічному клубі за гроші",
     "Вони танцюють стриптиз у нічному клубі за гроші",
     "«Sie strippen» с множественным сказуемым это «вони»"),
    (9218, "example_tr",
     "Gece kulübünde para için striptiz yapıyor",
     "Gece kulübünde para için striptiz yapıyorlar",
     "«Sie strippen» с множественным сказуемым это «они»"),
    # 10138 Armleuchter
    (11397, "example_pl", "Nie bądź idiotą i weź czapkę",
     "Jest taki głupi, prawdziwy idiota",
     "перевод другого предложения"),
    # 10139 Lesung
    (14748, "example_tr", "Yazarın okuması çok etkileyici idi",
     "Yazarın okuması çok etkileyiciydi",
     "«idi» отдельно"),
    # 10141 verunglücken
    (13034, "example_uk", "Літак зазнав аварії в горах",
     "Літак зазнав аварії, і всі загинули",
     "перевод другого предложения"),
    (13034, "example_pl", "Rozbity samochód stał na poboczu",
     "Samolot się rozbił i wszyscy zginęli",
     "перевод другого предложения"),
    # 10142 variabel
    (18063, "example_en", "Variable costs increase with production",
     "The variable costs are not always the same",
     "перевод другого предложения"),
    (18063, "example_tr", "Değişken maliyetler üretim ile artar",
     "Değişken maliyetler her zaman aynı değil",
     "перевод другого предложения"),
    # 10143 geschieden
    (15279, "example_pl", "Jest rozwiedziony i ma dwoje dzieci",
     "Jest rozwiedzioną kobietą z dwójką dzieci",
     "в эталоне «eine geschiedene Frau»"),
    # 10144 Händedruck
    (14281, "example_tr",
     "Güçlü bir el sıkışma anlaşmayı mühürledi",
     "Sıkı bir el sıkışması anlaşmayı pekiştirdi",
     "потерян изафет"),
    (14281, "example_pl", "Przywitał mnie mocnym uściskiem dłoni",
     "Mocny uścisk dłoni przypieczętował umowę",
     "перевод другого предложения"),
    # 10146 holprig
    (17349, "example_uk", "Дорога ямиста та повна ям",
     "Дорога вибоїста й повна ям",
     "«ямиста ... повна ям» — тавтология"),
    # 10147 geladen
    (16783, "example_en", "The loaded pistols were confiscated",
     "The loaded weapons were confiscated",
     "в эталоне «Waffen» — оружие вообще"),
    (16783, "example_ru", "Заряженные пистолеты были изъяты",
     "Заряженное оружие было изъято",
     "в эталоне «Waffen» — оружие вообще"),
    (16783, "example_uk", "Заряджені пістолети були вилучені",
     "Заряджену зброю було вилучено",
     "в эталоне «Waffen» — оружие вообще"),
    (16783, "example_tr",
     "Davet edilen misafirler akşam sekizde geldi",
     "Dolu silahlar ele geçirildi",
     "перевод другого предложения"),
    # 10149 präparieren
    (13035, "example_tr",
     "Bilim insanı sergi için hayvan iseletini hazırladı",
     "Bilim insanı sergi için hayvan iskeletini hazırladı",
     "«iseletini» — разваленное слово"),
    (13035, "example_pl", "Na biologii preparowaliśmy żabę",
     "Naukowiec preparował szkielet zwierzęcia na wystawę",
     "перевод другого предложения"),
    # 10150 abgeben
    (8348, "example_uk",
     "Міністр дає офіційне заяву щодо політичної кризи",
     "Міністр робить офіційну заяву щодо політичної кризи",
     "рассогласование рода, и «дає заяву»"),
    (8348, "example_tr",
     "Bakan siyasi kriz hakkında bir açıklama veriyor",
     "Bakan siyasi kriz hakkında bir açıklama yapıyor",
     "«açıklama vermek» — не то сочетание"),
    # 10151 weihen
    (14749, "example_uk", "Священник освячує воду на Водохреще",
     "Єпископ освячує нову церкву",
     "перевод другого предложения"),
    (14749, "example_tr", "Rahip yeni evi kutsadı",
     "Piskopos yeni kiliseyi kutsuyor",
     "в эталоне епископ и церковь, а не дом"),
    # 10152 robust
    (8349, "example_en",
     "The sturdy furniture lasted for many years",
     "The furniture was sturdily built and very durable",
     "перевод другого предложения"),
    (8349, "example_uk", "Міцний меблі служили багато років",
     "Меблі були міцно зроблені й дуже довговічні",
     "«міцний меблі» — рассогласование"),
    (8349, "example_tr",
     "Sağlam mobilyalar yıllar boyunca dayanmıştı",
     "Mobilyalar sağlam yapılmıştı ve çok dayanıklıydı",
     "перевод другого предложения"),
    # 10153 trostlos
    (11398, "example_tr",
     "Kasvetli manzara otobüsteki tüm yolcuları deprese etti",
     "Kasvetli manzara otobüsteki tüm yolcuları kedere boğdu",
     "«deprese etmek» — калька"),
    (11398, "example_pl",
     "Widok z okna był naprawdę przygnębiający",
     "Przygnębiający krajobraz zdeprymował wszystkich pasażerów w autobusie",
     "перевод другого предложения"),
    # 10155 Stadtrand
    (18428, "example_uk",
     "Вони живуть на передмісті у спокійному районі",
     "Вони живуть на околиці міста у спокійному районі",
     "перевод слова — «околиця міста»"),
    # 10156 einschlagen — лишнее «zu» после модального
    (8350, "example_de",
     "Der Kurs ist erfolgversprechend und wir sollten ihn einzuschlagen",
     "Der Kurs ist erfolgversprechend und wir sollten ihn einschlagen",
     "после модального «sollten» инфинитив идёт без «zu»"),
    # 10157 gehoben
    (8351, "example_uk",
     "Ресторан подає вишукану кухню з високосортними винами",
     "Ресторан подає вишукану кухню з першокласними винами",
     "«високосортний» о вине не говорят"),
    (8351, "example_tr", "Çok seçkin bir restoranda yemek yedik",
     "Restoran, birinci sınıf şaraplarla seçkin bir mutfak sunuyor",
     "перевод другого предложения"),
    # 10158 Kinderarzt
    (13036, "example_pl", "Jutro idziemy z małym do pediatry",
     "Pediatra zbadał dziecko dokładnie",
     "перевод другого предложения"),
    # 10160 Gehäuse
    (17706, "example_ru",
     "Корпус часов было сделано из нержавеющей стали",
     "Корпус часов был сделан из нержавеющей стали",
     "рассогласование рода"),
    (17706, "example_uk",
     "Корпус годинника було виготовлене зі нержавіючої сталі",
     "Корпус годинника був виготовлений з нержавіючої сталі",
     "рассогласование рода, и «зі» перед согласной"),
    # 10161 vergelten
    (11399, "example_tr", "Saldırıya hemen misilleme yaptılar",
     "Hakaretin karşılığını vermek istedi",
     "перевод другого предложения"),
    (11399, "example_pl", "Chciał odpłacić mu za pomoc",
     "Chciał odpłacić za zniewagę",
     "в эталоне оскорбление, а не помощь"),
    # 10162 Hellseherin
    (14750, "example_uk",
     "Ясновидиця розповіла йому про його майбутнє",
     "Ясновидиця розповіла йому, що принесе майбутнє",
     "в эталоне «was die Zukunft bringt»"),
    (14750, "example_tr", "Falcı ona geleceği anlattı",
     "Medyum ona geleceğin ne getireceğini anlattı",
     "перевод слова — «medyum», и фраза урезана"),
    # 10164 Kommunion
    (14751, "example_uk",
     "Його перша комунія була особливою подією для сім'ї",
     "Його перше причастя було особливою подією для сім'ї",
     "перевод слова — «причастя»"),
    (14751, "example_tr",
     "İlk komyonu aile için özel bir etkinlik idi",
     "İlk komünyonu aile için özel bir etkinlikti",
     "«komyonu» — опечатка, и «idi» отдельно"),
    # 10166 abtauchen
    (8352, "example_uk", "Він сховався в натовпі і зник",
     "Він заліг на дно і зник",
     "перевод другого предложения"),
    # 10167 Städtchen
    (18429, "example_tr", "Sahildeki küçük şehir çok özlemli idi",
     "Sahildeki küçük kasaba çok şirindi",
     "«özlemli» это тоскующий, и «idi» отдельно"),
    # 10168 Schönheitssalon
    (9220, "example_uk", "Вона ходить до салону краси кожен місяць",
     "Вона ходить до салону краси щомісяця",
     "«кожен місяць» — калька"),
    # 10169 verknüpft
    (8353, "example_uk",
     "Дві події були тісно пов'язані одна з одною",
     "Дві події тісно пов'язані одна з одною",
     "эталон в настоящем времени"),
    (8353, "example_tr",
     "İki olay birbiriyle yakından bağlantılı idi",
     "İki olay birbiriyle yakından bağlantılı",
     "«idi» отдельно, и время"),
    # 10170 barbarisch
    (11400, "example_tr", "Bu vahşiça bir eylemdi",
     "Bu barbarca bir eylemdi",
     "«vahşiça» — нет такой формы"),
    (11400, "example_pl", "To było barbarzyńskie zachowanie",
     "To był barbarzyński czyn",
     "«Tat» это поступок, а не поведение"),
    # 10171 Kokon
    (15796, "example_tr", "Tırtıl etrafında bir kokon örüştü",
     "Tırtıl etrafına bir koza ördü",
     "«örüştü» — нет такой формы"),
    # 10172 Karamell
    (11958, "example_uk", "Карамель була солодкою та гіркою",
     "Карамель була солодкою і гіркою водночас",
     "потеряно «zugleich»"),
    (11958, "example_tr", "Karamel tatlı ve acı idi",
     "Karamel aynı zamanda hem tatlı hem acıydı",
     "«idi» отдельно, и потеряно «zugleich»"),
    (11958, "example_pl", "Do kawy dodała trochę karmelu",
     "Karmel smakował jednocześnie słodko i gorzko",
     "перевод другого предложения"),
    # 10173 Biografie
    (14752, "example_tr",
     "Ünlü sanatçının biyografisi çok ilginç idi",
     "Ünlü sanatçının biyografisi çok ilginçti",
     "«idi» отдельно"),
    # 10175 todkrank
    (13037, "example_tr",
     "Doktor hastanın ölümcül hasta olduğunu söyledi",
     "Doktor hastanın ağır hasta olduğunu söyledi",
     "«ölümcül» это смертоносный, а не смертельно больной"),
    (13037, "example_pl", "Jej dziadek jest śmiertelnie chory",
     "Lekarz powiedział, że pacjent jest śmiertelnie chory",
     "перевод другого предложения"),
    # 10176 Rechtssystem
    (16788, "example_tr", "Almanyadaki hukuk sistemi karmaşıktır",
     "Almanya'daki hukuk sistemi karmaşıktır",
     "потерян апостроф"),
    # 10177 zertrümmern
    (8354, "example_uk", "Розгніваний розбив вазу молотком вщент",
     "Розгніваний чоловік розтрощив вазу молотком",
     "«розгніваний» без существительного повисает"),
    # 10178 Lampenfieber
    (11401, "example_ru",
     "Перед выступлением у неё было сильное волнение",
     "Перед выступлением у неё было страшное волнение",
     "в эталоне «schreckliches»"),
    (11401, "example_tr",
     "Performansından önce korkunç sahne korkusu yaşadı",
     "Gösteriden önce korkunç bir sahne korkusu yaşadı",
     "«Performansından» — лишнее притяжание"),
    # 10179 jammerschade
    (11402, "example_uk", "Шкода, що концерт скасували",
     "Дуже шкода, що концерт скасували",
     "потеряно «jammer-»"),
    (11402, "example_tr", "Konsertin iptal edilmesi çok yazık",
     "Konserin iptal edilmesi çok yazık",
     "«Konsertin» — лишняя согласная"),
    # 10181 beherbergen
    (18430, "example_pl", "Hotel gości stu gości na dobę",
     "Hotel przyjmuje stu gości na dobę",
     "«gości ... gości» — тавтология"),
    # 10182 angehören
    (15280, "example_uk",
     "Він належить партії вже двадцять років",
     "Він належить до партії вже двадцять років",
     "«належати» требует «до»"),
    (15280, "example_tr", "Yirmi yıldır partiye ait",
     "Yirmi yıldır partiye üye",
     "«ait» о вещах, о человеке — «üye»"),
    # 10183 schälen
    (11959, "example_pl", "Obieram ziemniaki na obiad",
     "Obieram pomarańczę na śniadanie",
     "перевод другого предложения"),
    # 10184 vorwerfen — лишнее «zu» после модального
    (14282, "example_de", "Man kann ihm nicht viel vorzuwerfen",
     "Man kann ihm nicht viel vorwerfen",
     "после модального «kann» инфинитив идёт без «zu»"),
    (14282, "example_uk", "Не докоряй мені за кожну дрібницю",
     "Йому особливо нічого не докоряти",
     "перевод другого предложения"),
    (14282, "example_tr", "Beni haksız yere suçluyor",
     "Ona pek bir şey söylenemez",
     "перевод другого предложения"),
    # 10186 vollzählig
    (8355, "example_tr", "Aile akşam yemeğinde tamamen hazır idi",
     "Aile akşam yemeğinde eksiksiz hazırdı",
     "«idi» отдельно"),
    # 10187 Eisberg
    (15798, "example_uk", "Айсберг повільно дрейфував в морі",
     "Айсберг повільно дрейфував у морі",
     "«в» перед согласной"),
    (15798, "example_tr",
     "Buz dağı denizde yavaş yavaş sürüklendi",
     "Buzdağı denizde yavaş yavaş sürüklendi",
     "«buzdağı» пишется слитно"),
    # 10188 vierte
    (13592, "example_uk", "Четверте дитя було хлопцем",
     "Четверта дитина була хлопчиком",
     "«дитя» просторечие"),
    # 10189 Raumfahrt
    (18064, "example_en", "Space travel has made great progress",
     "Space travel has taken us to the Moon",
     "перевод другого предложения"),
    (18064, "example_tr", "Uzay seyahati büyük ilerleme kaydetti",
     "Uzay yolculuğu bizi Ay'a götürdü",
     "перевод другого предложения"),
    # 10190 Bergwerk
    (9221, "example_uk", "Гірницю закрили десять років тому",
     "Шахту закрили десять років тому",
     "«гірниця» — нет такого слова"),
    # 10191 Imitation
    (14753, "example_uk",
     "Імітація була настільки досконалою, що ніхто це не помітив",
     "Імітація була настільки досконалою, що ніхто цього не помітив",
     "«не помітив це» требует родительного"),
    # 10192 Hausbesuch
    (13038, "example_pl", "Lekarz robi wizyty domowe w soboty",
     "Wizyty domowe lekarza są ważne",
     "перевод другого предложения"),
    # 10195 besagt
    (8356, "example_uk", "Згаданий фільм мені дуже сподобався",
     "Згаданого чоловіка тут немає",
     "перевод другого предложения"),
    # 10196 Bypass
    (13039, "example_tr", "Bypass başarıyla implante edildi",
     "Baypas başarıyla implante edildi",
     "перевод слова — «baypas»"),
    (13039, "example_pl", "Dziadek ma wszczepiony bajpas",
     "Bajpas został pomyślnie wszczepiony",
     "перевод другого предложения"),
    # 10197 versklavt
    (16789, "example_tr", "Halk köle yapılmış ve baskı altında",
     "Halk köleleştirilmiş ve baskı altındaydı",
     "«köle yapılmış» — калька, и потеряно время"),
    # 10201 pochen
    (14284, "example_tr",
     "O, talepleri yerine getirilmesinde ısrar ediyor",
     "Taleplerinin yerine getirilmesinde ısrar ediyor",
     "потерян родительный, фраза рассыпается"),
    (14284, "example_pl", "Ciągle nalega na swoje prawa",
     "Nalega na to, żeby jego żądania zostały spełnione",
     "перевод другого предложения"),
    # 10202 unbegrenzt
    (8358, "example_tr", "Bu planla sınırsız imkanlarınız var",
     "Bu planla sınırsız imkânların var",
     "эталон обращается на «ты»"),
    # 10203 Gummibärchen
    (11960, "example_uk",
     "Діти люблять гумові ведмідики під час фільму",
     "Діти люблять желейних ведмедиків під час фільму",
     "«гумові ведмідики» — не то слово и опечатка"),
    (11960, "example_tr",
     "Çocuklar film izlerken sakız ayıları seviyorlar",
     "Çocuklar film izlerken jelibon seviyor",
     "«sakız ayısı» — не по-турецки"),
    (11960, "example_pl", "Kupiłam dzieciom żelki do kina",
     "Dzieci lubią żelki podczas filmu",
     "перевод другого предложения"),
    # 10205 Aasgeier
    (15800, "example_uk", "Сип кружив над саваною",
     "Стерв'ятник кружив над саваною",
     "перевод слова — «стерв'ятник»"),
    (15800, "example_tr", "Akbaba savanada dolaşıyor",
     "Akbaba savananın üzerinde daireler çizdi",
     "«dolaşıyor» теряет круженье, и время"),
    # 10208 Meinungsverschiedenheit
    (14286, "example_en",
     "There was a disagreement between the two partners",
     "We had a small disagreement yesterday",
     "перевод другого предложения"),
    (14286, "example_uk",
     "Між двома партнерами була розбіжність поглядів",
     "Вчора в нас була невелика розбіжність у поглядах",
     "перевод другого предложения"),
    (14286, "example_tr", "İki ortak arasında fikir ayrılığı vardı",
     "Dün küçük bir fikir ayrılığımız oldu",
     "перевод другого предложения"),
    (14286, "example_pl", "Mieliśmy drobną różnicę zdań",
     "Mieliśmy wczoraj drobną różnicę zdań",
     "потеряно «gestern»"),
    # 10210 Gesetzlose
    (16791, "example_ru", "Беззаконники терроризировали деревню",
     "Разбойники терроризировали деревню",
     "«беззаконники» — не словарное слово"),
    # 10212 Golfschläger
    (12365, "example_uk", "Хороша клюшка для гольфу дорога",
     "Хороша ключка для гольфу дорога",
     "в статье «ключка», а в примере русское «клюшка»"),
    # 10214 überbieten
    (17874, "example_en", "I won't be able to outbid his offer",
     "I won't be able to outbid your offer",
     "в эталоне «dein Gebot» — твою ставку"),
    (17874, "example_uk", "Я не зможу перевищити його пропозицію",
     "Я не зможу перебити твою ставку",
     "в эталоне «dein Gebot» — твою ставку"),
    (17874, "example_tr", "Onun teklifini geçemeyeceğim",
     "Senin teklifini geçemeyeceğim",
     "в эталоне «dein Gebot» — твою ставку"),
    # 10215 ausfragen
    (14287, "example_uk", "Припини постійно мене допитувати",
     "Припини постійно мене розпитувати",
     "перевод слова — «розпитувати»"),
    (14287, "example_tr", "Beni hep sorgulamaktan vazgeç",
     "Beni sürekli sorguya çekmeyi bırak",
     "«sorgulamaktan vazgeç» — калька"),
    # 10216 Alimente
    (16793, "example_tr",
     "Boşanmadan sonra çocuklar için nafaka ödemek zorunda",
     "Boşandıktan sonra çocuklar için nafaka ödemek zorunda",
     "«boşanmadan sonra» — не та форма"),
    # 10217 Anleihen
    (17875, "example_pl", "Rząd wypuszcza nowe obligacje",
     "Rząd wypuszcza nowe obligacje, żeby pożyczyć pieniądze",
     "потеряно «um sich Geld zu leihen»"),
    # 10218 Familienangelegenheit
    (15281, "example_pl", "To nasza sprawa rodzinna",
     "To sprawa rodzinna, która dotyczy tylko nas",
     "потеряна вторая половина"),
    # 10219 Klugheit
    (11404, "example_pl", "Jego mądrość uratowała całą sytuację",
     "Jego mądrość pomogła mu wyjść z trudnej sytuacji",
     "перевод другого предложения"),
    # 10220 erliegen
    (8359, "example_en",
     "He succumbed to temptation and ate the whole cake",
     "One can easily succumb to this error",
     "перевод другого предложения"),
    (8359, "example_uk", "Він піддався спокусі і з'їв увесь торт",
     "Цій помилці легко піддатися",
     "перевод другого предложения"),
    (8359, "example_tr", "Sonunda dayanamadı ve teslim oldu",
     "Bu yanılgıya kolayca düşülebilir",
     "перевод другого предложения"),
    # 10221 Murmeltier
    (15801, "example_uk", "Навесні сурок виходить зі своєї нори",
     "Навесні бабак виходить зі своєї нори",
     "перевод слова — «бабак»"),
    (15801, "example_tr", "Baharında marmota yuvalarından çıkıyor",
     "İlkbaharda dağ sıçanı yuvasından çıkıyor",
     "«Baharında» и «marmota» — сломанные формы"),
    # 10222 spulen
    (8360, "example_en",
     "I fast forwarded the tape to get to the end",
     "I fast-forward the video to get to the end",
     "эталон в настоящем и про видео"),
    (8360, "example_uk",
     "Я швидко перемотав плівку, щоб дійти до кінця",
     "Я перемотую відео вперед, щоб дійти до кінця",
     "эталон в настоящем и про видео"),
    (8360, "example_tr",
     "Sona ulaşmak için bandı hızlı ileri sardım",
     "Sona ulaşmak için videoyu ileri sarıyorum",
     "эталон в настоящем и про видео"),
    # 10223 Edelstein
    (13764, "example_tr",
     "Elinde güzel bir mücevher taşı takıyordu",
     "Elinde çok güzel bir değerli taş takıyordu",
     "перевод слова — «değerli taş»"),
    # 10224 Arbeiterklasse
    (9222, "example_uk", "Робочий клас борється за кращі умови праці",
     "Робітничий клас бореться за кращі умови праці",
     "перевод слова — «робітничий клас»"),
    # 10225 Pik
    (12366, "example_ru",
     "В карточной игре он любит играть пиковую масть",
     "В карточной игре он любит играть в пики",
     "«играть масть» — не то управление"),
    (12366, "example_uk",
     "У карткові грі він любить грати пікову масть",
     "У картковій грі він любить грати в піки",
     "«карткові» — опечатка, и «грати масть»"),
    # 10227 verhandelbar
    (17876, "example_uk",
     "Ціна придатна для переговорів, якщо ви купите кілька штук",
     "Ціна договірна, якщо ви купите кілька штук",
     "«придатна для переговорів» — канцелярит"),
    (17876, "example_tr",
     "Birden fazla satın alırsan fiyat pazarlık edilebilir",
     "Birden fazla parça alırsan fiyat pazarlığa açık",
     "порядок слов и «pazarlık edilebilir»"),
    (17876, "example_pl", "Cena jest do negocjacji",
     "Cena jest do negocjacji, jeśli kupisz kilka sztuk",
     "потеряно условие"),
    # 10229 Anwohner
    (18431, "example_tr", "Sakinler gürültüden şikayet ediyorlar",
     "Mahalle sakinleri gürültüden şikâyet ediyor",
     "перевод слова — «mahalle sakini»"),
    # 10230 Regenwald
    (15802, "example_uk",
     "Тропічний ліс стає меншим кожного дня",
     "Тропічний ліс щодня стає меншим",
     "«кожного дня» — калька"),
    # 10232 Leuchtfeuer
    (17352, "example_uk", "Маяк у гавані мигає кожну ніч",
     "Маяк у гавані блимає щоночі",
     "«мигає» — русизм, и «кожну ніч» — калька"),
    (17352, "example_tr",
     "Limandaki deniz feneri her gece yanıp söniyor",
     "Limandaki deniz feneri her gece yanıp sönüyor",
     "«söniyor» — опечатка"),
    # 10233 ungeschoren
    (8363, "example_uk", "Він вийшов зі скандалу безкарно",
     "Він вийшов зі скандалу цілий і неушкоджений, безкарно",
     "потеряно «mit heiler Haut»"),
    (8363, "example_tr", "Skandaldan cezasız kurtuldu",
     "Skandaldan yara almadan, cezasız kurtuldu",
     "потеряно «mit heiler Haut»"),
    # 10234 Teer
    (17708, "example_uk", "Дорога зроблена з дегтю та асфальту",
     "Дорога зроблена з дьогтю та асфальту",
     "«дегтю» — русская форма"),
    # 10235 Einsatzkommando
    (16794, "example_en",
     "The task force was called to the bank to prevent the robbery",
     "The task force stormed the apartment",
     "перевод другого предложения"),
    (16794, "example_ru",
     "Спецназ вызвали в банк, чтобы предотвратить ограбление",
     "Спецназ штурмовал квартиру",
     "перевод другого предложения"),
    (16794, "example_uk",
     "Спецназ був викликаний до банку, щоб запобігти грабежу",
     "Спецпідрозділ штурмував квартиру",
     "перевод другого предложения"),
    (16794, "example_tr", "Özel harekât timi binaya girdi",
     "Özel harekât timi daireye girdi",
     "в эталоне квартира, а не здание"),
    (16794, "example_pl", "Oddział specjalny wkroczył do budynku",
     "Oddział specjalny wkroczył do mieszkania",
     "в эталоне квартира, а не здание"),
    # 10236 besiegeln
    (8364, "example_tr",
     "Bu el sıkışmasıyla sözleşmeyi mühürlemektedir",
     "Bu el sıkışmasıyla sözleşmeyi mühürlüyor",
     "«-mektedir» книжное"),
    (8364, "example_pl",
     "Tym uściskiem dłoni przypieczętował umowę",
     "Tym uściskiem dłoni przypieczętowuje umowę",
     "эталон в настоящем времени"),
    # 10237 Grundsatz
    (11405, "example_tr", "Bizim ilkelerimize bağlı kalmalıyız",
     "İlkelerimize bağlı kalmalıyız",
     "«bizim» лишнее при притяжательной форме"),
    (11405, "example_pl", "Mam swoje zasady i ich nie zmieniam",
     "Musimy trzymać się naszych zasad",
     "перевод другого предложения"),
    # 10239 Christentum
    (14756, "example_uk", "Християнство прийшло сюди дуже давно",
     "Християнство — одна з найбільших релігій світу",
     "перевод другого предложения"),
    # 10240 Ferienhaus
    (18432, "example_ru", "Мы сняли коттедж у озера",
     "Мы едем в дом для отдыха на летних каникулах",
     "перевод другого предложения"),
    (18432, "example_uk", "Ми їдемо до будинку для відпочинку",
     "Ми їдемо до будинку для відпочинку на літніх канікулах",
     "потеряно «in den Sommerferien»"),
    (18432, "example_tr", "Yazlık eve gidiyoruz",
     "Yaz tatilinde yazlık eve gidiyoruz",
     "потеряно «in den Sommerferien»"),
    # 10241 heimsuchen — приставка в эталоне не отделена
    (8365, "example_de", "Albträume heimsuchen ihn jede Nacht",
     "Albträume suchen ihn jede Nacht heim",
     "у отделяемой приставки личная форма рвётся: «suchen … heim»"),
    # 10243 bezwingen
    (8367, "example_uk", "Він нарешті покорив гору",
     "Він нарешті підкорив гору",
     "«покорив» — русизм"),
    (8367, "example_tr", "Sonunda dağı fethetmiş",
     "Sonunda dağı fethetti",
     "«-miş» о пересказе, а здесь факт"),
    # 10244 Serum — число в эталоне рассогласовано
    (8368, "example_de", "Die Sera wird im Labor getestet",
     "Das Serum wird im Labor getestet",
     "«Sera» множественного числа при сказуемом единственного"),
    (8368, "example_pl", "Surowice są badane w laboratorium",
     "Surowica jest badana w laboratorium",
     "вслед за исправленным эталоном"),
    # 10245 Einschaltquote
    (14757, "example_tr",
     "Dizi bu hafta yayın izlenme oranları daha iyiydi",
     "Dizinin izlenme oranları bu hafta daha iyiydi",
     "«Dizi ... oranları» без родительного"),
    # 10246 Schönling
    (11406, "example_uk",
     "Красень постійно отримував увагу лише тому, що був гарний",
     "Красунчик постійно отримував увагу лише тому, що був гарний",
     "перевод слова — «красунчик»"),
    (11406, "example_tr",
     "Güzelim sadece güzel olduğu için hep ilgi çekiyordu",
     "Yakışıklı delikanlı sadece yakışıklı olduğu için hep ilgi çekiyordu",
     "«güzelim» это обращение «красавица моя»"),
    (11406, "example_pl", "Ten ładniś cały czas patrzy w lustro",
     "Ładniś ciągle dostawał uwagę tylko dlatego, że był przystojny",
     "перевод другого предложения"),
    # 10247 hochnäsig
    (11407, "example_pl", "Jest zarozumiały i z nikim się nie wita",
     "Wydawała się zarozumiała i prawie nie rozmawiała z innymi",
     "перевод другого предложения"),
    # 10248 impfen
    (13040, "example_tr",
     "Doktor beni grip aşısı ile aşılaması gerekiyor",
     "Doktorun beni gribe karşı aşılaması gerekiyor",
     "потерян родительный, фраза рассыпается"),
    (13040, "example_pl", "Dzisiaj szczepimy dzieci przeciw grypie",
     "Lekarz musi mnie zaszczepić przeciw grypie",
     "перевод другого предложения"),
    # 10251 stolpern
    (8371, "example_uk", "Він спотикається про сходи і падає",
     "Він спотикається на сходах і падає",
     "«спотикатися про» — не то управление"),
    (8371, "example_tr", "Merdivenlerden sendeliyor ve düşüyor",
     "Merdivende tökezliyor ve düşüyor",
     "«merdivenlerden» — не тот падеж"),
    # 10253 getränkt
    (8372, "example_tr", "Kumaş benzinle ıslanmıştı",
     "Kumaş benzinle ıslatılmıştı",
     "«ıslanmıştı» значит намок сам"),
    # 10255 Zitadelle
    (14758, "example_tr", "Eski kale şehrin üzerine yükseliyor",
     "Eski iç kale şehrin üzerinde yükseliyor",
     "перевод слова — «iç kale», и не тот падеж"),
    # 10256 Ausflucht
    (14288, "example_uk", "Це просто відмовка, а не причина",
     "Його відмовки вже нікого не переконують",
     "перевод другого предложения"),
    (14288, "example_pl",
     "Nie szukaj wymówek i po prostu to zrób",
     "Jego wymówki już nikogo nie przekonują",
     "перевод другого предложения"),
    # 10260 unerbittlich
    (11408, "example_uk", "Спека була невблаганна цілий день",
     "Невблаганна спека ускладнювала життя",
     "перевод другого предложения"),
    (11408, "example_pl", "Był nieubłagany w swoich żądaniach",
     "Nieubłagany upał utrudniał życie",
     "перевод другого предложения"),
    # 10261 Kongressabgeordneter
    (16796, "example_tr", "Kongreci plenum önünde konuştu",
     "Kongre üyesi genel kurul önünde konuştu",
     "«kongreci» — нет такого слова"),
    # 10262 Vize
    (9223, "example_en",
     "The vice president took on the responsibility",
     "Today the deputy chairs the meeting",
     "перевод другого предложения"),
    (9223, "example_uk",
     "Віце-президент взяв на себе відповідальність",
     "Сьогодні засідання веде заступник",
     "перевод другого предложения"),
    (9223, "example_tr", "Başkan yardımcısı sorumluluğu üstlendi",
     "Bugün toplantıyı başkan yardımcısı yönetiyor",
     "перевод другого предложения"),
    (9223, "example_pl", "Wiceprezes przejął odpowiedzialność",
     "Dziś zebranie prowadzi zastępca",
     "перевод другого предложения"),
    # 10263 Schwiegereltern
    (1854, "example_en", "My in-laws are nice",
     "My in-laws are very nice",
     "потеряно «sehr»"),
    (1854, "example_ru", "Мои родители супруга очень милые",
     "Мои тесть и тёща очень милые",
     "«родители супруга» — канцелярит"),
    (1854, "example_uk", "Мої тесть і теща приємні",
     "Мої тесть і теща дуже приємні",
     "потеряно «sehr»"),
    # 10264 Zusammenkunft
    (15283, "example_pl", "Nasze spotkanie było bardzo udane",
     "Spotkanie było bardzo produktywne",
     "«udane» это удачное, а не продуктивное"),
    # 10265 ausräumen
    (18434, "example_ru", "Нам нужно разобрать подвал",
     "Нам нужно освободить подвал",
     "перевод слова — «освободить»"),
    (18434, "example_uk", "Нам потрібно розібрати підвал",
     "Нам потрібно звільнити підвал",
     "перевод слова — «звільнити»"),
    # 10266 hausen — в русском выдуманное слово
    (18435, "example_ru",
     "Они хаустят в старом заброшенном доме",
     "Они ютятся в старом заброшенном доме",
     "«хаустить» — выдуманная форма от немецкого hausen"),
    (18435, "example_en",
     "They were dwelling in an old abandoned house",
     "They dwell in an old abandoned house",
     "эталон в настоящем времени"),
    (18435, "example_uk",
     "Вони мешкали в старому занедбаному будинку",
     "Вони туляться в старому занедбаному будинку",
     "эталон в настоящем, и перевод слова — «тулитися»"),
    (18435, "example_tr",
     "Eski terkedilmiş bir evde oturuyorlardı",
     "Eski, terk edilmiş bir evde barınıyorlar",
     "эталон в настоящем, и «terkedilmiş» раздельно"),
    # 10267 lebenswert
    (18898, "example_ru", "Каждый хочет более стоящей жизни",
     "Каждый хочет более достойной жизни",
     "«стоящей жизни» — обрывок"),
    (18898, "example_pl",
     "Każdy pragnie życia bardziej wartego życia",
     "Każdy pragnie życia bardziej wartego przeżycia",
     "«życia wartego życia» — тавтология"),
    # 10268 Doppelleben
    (11409, "example_pl", "Przez lata prowadził podwójne życie",
     "Prowadził podwójne życie – trudno było nosić ten sekret",
     "потеряна вторая половина"),
    # 10269 rundherum
    (8374, "example_en", "There were trees all around the house",
     "All around there were only tall trees",
     "«дома» в эталоне нет, и потеряно «nur hohe»"),
    (8374, "example_uk", "Ми усебічно обговорили все можливе",
     "Кругом стояли лише високі дерева",
     "перевод другого предложения"),
    (8374, "example_tr",
     "Her yönden mümkün olan her şeyi konuştuk",
     "Çepeçevre sadece yüksek ağaçlar vardı",
     "перевод другого предложения"),
    # 10270 Nachrichtendienst
    (16797, "example_pl",
     "Służba wywiadowcza obserwuje podejrzane osoby",
     "Służba wywiadowcza obserwuje podejrzane działania",
     "в эталоне «Aktivitäten», а не люди"),
    # 10271 Kriegsende
    (16798, "example_pl", "Dziadek pamięta koniec wojny",
     "Koniec wojny był w 1945 roku",
     "перевод другого предложения"),
    # 10272 verbleiben
    (8375, "example_en", "After the closure, two branches remain",
     "We have only two days left",
     "перевод другого предложения"),
    (8375, "example_uk",
     "Після закриття залишаються ще два філіали",
     "У нас залишається лише два дні",
     "перевод другого предложения"),
    (8375, "example_tr", "Kapanıştan sonra iki şube daha kalıyor",
     "Bize sadece iki gün kaldı",
     "перевод другого предложения"),
    # 10274 Augenzeuge
    (16799, "example_en",
     "The eyewitness saw everything clearly and told the police",
     "The eyewitness saw the collision and reports it to the police",
     "в эталоне столкновение, и второе сказуемое в настоящем"),
    (16799, "example_uk",
     "Очевидець все чітко бачив і розповів поліції",
     "Очевидець бачив зіткнення і повідомляє про це поліції",
     "в эталоне столкновение, и второе сказуемое в настоящем"),
    (16799, "example_tr",
     "Göz tanığı her şeyi net gördü ve polise anlattı",
     "Görgü tanığı çarpışmayı gördü ve polise bildiriyor",
     "перевод слова — «görgü tanığı», и в эталоне столкновение"),
    (16799, "example_pl",
     "Naoczny świadek opowiedział wszystko policji",
     "Naoczny świadek widział kolizję i zgłasza to policji",
     "в эталоне столкновение, и второе сказуемое в настоящем"),
    # 10275 Besinnung
    (11410, "example_uk",
     "Після довгих розмислів він вирішив почати знову",
     "Після довгих роздумів він вирішив почати знову",
     "«розмисли» — не словарная форма"),
    (11410, "example_pl", "Po chwili namysłu zgodził się pomóc",
     "Po długim namyśle zdecydował się zacząć od nowa",
     "перевод другого предложения"),
    # 10276 feilschen
    (9922, "example_uk", "Він любить торгуватися на базарі",
     "На ринку люди торгуються за ціни",
     "перевод другого предложения"),
    (9922, "example_tr", "Pazarda fiyat üzerinden pazarlık edilir",
     "Pazarda insanlar fiyatlar için pazarlık ediyor",
     "страдательное вместо «die Leute feilschen»"),
    # 10277 gefroren
    (8377, "example_pl",
     "Dzieci biegają po zamarzniętym jeziorze",
     "Zamarznięte jezioro jest wystarczająco grube do jazdy na łyżwach",
     "перевод другого предложения"),
    # 10278 Chefarzt
    (13042, "example_uk", "Головний лікар робить обхід з ранку",
     "Головний лікар робить обхід зранку",
     "«з ранку» пишется слитно"),
    (13042, "example_tr", "Başhekim sabahları ziyaretlerini yapıyor",
     "Başhekim sabahları vizitesini yapıyor",
     "«ziyaret» это визит в гости, обход — «vizite»"),
    (13042, "example_pl",
     "Ordynator przyszedł na obchód po śniadaniu",
     "Ordynator robi obchód rano",
     "перевод другого предложения"),
    # 10279 Drogendezernat
    (16800, "example_ru",
     "Отдел наркотиков проводит расследование против банды",
     "Отдел по борьбе с наркотиками ведёт расследование против банды",
     "«отдел наркотиков» — обрывок названия"),
    (16800, "example_uk",
     "Відділ наркотиків розслідує діяльність банди",
     "Відділ боротьби з наркотиками розслідує діяльність банди",
     "«відділ наркотиків» — обрывок названия"),
    (16800, "example_pl",
     "Wydział narkotykowy prowadzi śledztwo w tej sprawie",
     "Wydział narkotykowy prowadzi śledztwo przeciwko bandzie",
     "в эталоне против банды"),
    # 10280 Rückenschmerzen
    (13043, "example_pl", "Od tygodnia mam ból pleców",
     "Od kilku dni mam ból pleców i prawie nie mogę spać",
     "потеряна вторая половина"),
    # 10281 durchschlagen
    (8378, "example_tr", "Güneş sonunda bulutları delip geçti",
     "Yeni fikirler satış rakamlarında hızla kendini gösteriyor",
     "перевод другого предложения"),
    (8378, "example_pl", "Plama przebiła się przez farbę",
     "Nowe pomysły szybko przebijają się w wynikach sprzedaży",
     "перевод другого предложения"),
    # 10283 Verkehrsunfall
    (17353, "example_en",
     "There was a traffic accident on the highway and traffic backed up",
     "There was a traffic accident on the motorway",
     "второй половины в эталоне нет"),
    (17353, "example_ru",
     "На автостраде произошла дорожная авария и пробка",
     "На автостраде произошла дорожная авария",
     "второй половины в эталоне нет"),
    (17353, "example_uk",
     "На автостраді трапилася дорожна аварія",
     "На автостраді трапилася дорожня аварія",
     "«дорожна» — не форма"),
    (17353, "example_tr",
     "Otoyolda trafik kazası oldu ve tıkanıklık oluştu",
     "Otoyolda trafik kazası oldu",
     "второй половины в эталоне нет"),
    # 10288 kapern
    (16801, "example_pl",
     "Piraci porwali statek na pełnym morzu",
     "Piraci porwali statek na morzu",
     "«na pełnym morzu» в эталоне нет"),
    # 10289 Schalldämpfer
    (16802, "example_tr", "Tüfeğe susturucu takmışlar",
     "Tüfekteki susturucu ateş etmeyi sessizleştiriyor",
     "перевод другого предложения"),
    (16802, "example_pl",
     "Tłumik sprawia, że strzał jest cichszy",
     "Tłumik na karabinie sprawia, że strzał jest cichszy",
     "потеряно «am Gewehr»"),
    # 10290 Motorengeräusch
    (17354, "example_en",
     "The engine noise was so loud that I couldn't sleep",
     "A loud engine noise came from outside",
     "перевод другого предложения"),
    (17354, "example_ru",
     "Звук мотора был такой громкий, что я не мог спать",
     "Снаружи раздался громкий шум мотора",
     "перевод другого предложения"),
    (17354, "example_uk",
     "Звук мотора був таким гучним, що я не міг спати",
     "Знадвору долинув гучний шум мотора",
     "перевод другого предложения"),
    (17354, "example_tr",
     "Motor sesi çok yüksekti, uyuyamadım",
     "Dışarıdan yüksek bir motor sesi geldi",
     "перевод другого предложения"),
    # 10291 Spray
    (13044, "example_pl", "Kup mi spray na komary",
     "Używam sprayu na objawy kataru siennego",
     "перевод другого предложения"),
    # 10297 haften
    (16804, "example_pl",
     "Naklejka dobrze przykleja się do szyby",
     "Znaczek dobrze przykleja się do gładkiego papieru",
     "в эталоне марка и гладкая бумага"),
    # 10298 eingestürzt
    (8379, "example_uk", "Зруйнована будівля була швидко знесена",
     "Обвалена будівля була швидко знесена",
     "перевод слова — «обвалений»"),
    (8379, "example_pl", "Zawalony dom w końcu rozebrali",
     "Zawalony budynek został szybko rozebrany",
     "в эталоне «schnell», а не «в конце концов»"),
    # 10300 Sellerie
    (11963, "example_pl", "Kroję seler do zupy",
     "Kroję drobno seler do zupy",
     "потеряно «klein»"),
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
