"""
Правки блока 55 (ряды 9301–9500, ранги 18692–19197).

Классы, которые дал блок:
  · эталон со строчным существительным: `in dem safe` вместо `Safe`
    (в немецком это ошибка, а не стиль);
  · чужое слово вместо перевода: tr `Ladik dağlarda yetişir` у ряда
    `die Tanne` — «Ladik» это город в Турции, а не пихта;
  · подмена предмета: tr `Dönme doğramaca` вместо `hız treni`
    у ряда `die Attraktion`;
  · украинские несуществующие формы: `Верета`, `Койот виття`,
    `Обломок`, `видні`, `Поставь`;
  · турецкие обрывки: `yorgun dum`, `telefon aramas`, `Gonore vardı`,
    `Sektöründe ağır sıklet`, `Gıda zehirlenmesi vardı`;
  · перевод другого предложения — больше сорока рядов.

    python -m app.scripts.fix_block_0055            # показать
    python -m app.scripts.fix_block_0055 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 9301 übereinander
    (8182, "example_uk", "Книги лежать один поверх одного на столі",
     "Книги лежать одна на одній на столі",
     "«книги» жіночого роду"),
    (8182, "example_pl", "Ułóż pudełka jedno na drugim",
     "Książki leżą jedna na drugiej na stole",
     "перевод другого предложения"),
    # 9302 gesellschaftlich
    (8183, "example_pl", "To ważny problem społeczny",
     "To ważne kwestie społeczne",
     "в эталоне «Fragen» во множественном"),
    # 9303 Zusage
    (8184, "example_tr", "Patronun onayını bekliyoruz",
     "Onayına sevindim",
     "перевод другого предложения"),
    (8184, "example_pl", "Dostałem zgodę na nową pracę",
     "Cieszę się z twojej zgody",
     "перевод другого предложения"),
    # 9304 unterstehen
    (8185, "example_tr", "Bu bölüm müdürün altında",
     "Bu bölüm müdüre bağlıdır",
     "«müdürün altında» — не то выражение"),
    (8185, "example_pl", "Ten dział podlega dyrektorowi",
     "Ten dział podlega menedżerowi",
     "в эталоне «Manager»"),
    # 9305 übermütig
    (11307, "example_en", "The kids were excessively cheerful at bedtime",
     "The kids got boisterous after the game",
     "перевод другого предложения"),
    (11307, "translation_uk",
     "розпустований, розбишацький, зухвалий, самовпевнений",
     "розбишацький, грайливий, зухвалий, самовпевнений",
     "«розпустований» — нет такого слова"),
    (11307, "example_uk", "Він відповів учителю зухвалим тоном",
     "Діти розбуялися після гри",
     "перевод другого предложения"),
    # 9306 Gardine
    (18402, "example_ru", "Шторы слишком тонкие",
     "Занавески слишком тонкие",
     "перевод слова — «занавеска»"),
    (18402, "example_uk", "Штори занадто тонкі",
     "Фіранки занадто тонкі",
     "перевод слова — «фіранка»"),
    (18402, "example_pl", "Firanki w kuchni są za cienkie",
     "Firanki są za cienkie",
     "«w kuchni» в эталоне нет"),
    # 9307 Renovierung
    (18403, "example_uk", "Ремонт дому зайняв багато часу",
     "Ремонт будинку тривав довго",
     "«дому» это домашнего очага, строения — «будинку»"),
    (18403, "example_tr", "Evin renovasyonu çok uzun sürdü",
     "Evin tadilatı çok uzun sürdü",
     "перевод слова — «tadilat»"),
    (18403, "example_pl", "Remont kuchni trwał dwa tygodnie",
     "Remont domu trwał długo",
     "перевод другого предложения"),
    # 9308 zeitig
    (18878, "example_tr", "Erkenci yola çıkmalıyız",
     "Erken yola çıkmalıyız",
     "«erkenci» это существительное «ранняя птица»"),
    # 9311 Vorwahl
    (14245, "example_en", "The area code 030 is for Berlin",
     "The area code for Berlin is 030",
     "порядок как в эталоне"),
    (14245, "example_uk", "Телефонний код 030 — це Берлін",
     "Телефонний код Берліна — 030",
     "порядок как в эталоне"),
    (14245, "example_tr", "Ön seçim yapılıyor",
     "Berlin'in alan kodu 030",
     "перевод другого предложения, да ещё по другому значению"),
    # 9313 Videokamera
    (17676, "example_pl", "Kamera wideo nagrała całe przyjęcie",
     "Kamera wideo nagrała wszystko",
     "«całe przyjęcie» в эталоне нет"),
    # 9314 Sonnenbrand
    (12972, "example_uk", "Я отримав опік від сонця",
     "Я отримав сонячний опік",
     "перевод слова — «сонячний опік»"),
    # 9319 zuwenden
    (8187, "example_tr", "Şimdi tamamen yeni projeye yöneldim",
     "Çocuklarına yöneliyor ve işi unutuyor",
     "перевод другого предложения"),
    (8187, "example_pl", "Zwróciła się do dzieci i zapomniała o pracy",
     "Zwraca się do dzieci i zapomina o pracy",
     "эталон в настоящем времени"),
    # 9320 Dynamik
    (8188, "example_tr", "Bu gruptaki dinamik etkileyici",
     "Bu gruptaki hareketlilik etkileyici",
     "«dinamik» прилагательное, нужно существительное"),
    (8188, "example_pl", "Dynamika w tej grupie jest świetna",
     "Dynamika w tej grupie jest imponująca",
     "«beeindruckend» — впечатляющая"),
    # 9321 Schläfchen
    (18879, "example_tr", "Öğleden sonra kısa bir uyku çekiyor",
     "Öğleden sonra kısa bir şekerleme yapıyor",
     "перевод слова — «şekerleme»"),
    # 9322 Hintergedanken
    (11310, "example_uk",
     "Я думаю, він має приховану думку в цій пропозиції",
     "Я думаю, він має приховані наміри в цій пропозиції",
     "«прихована думка» — калька"),
    # 9324 zivil
    (16690, "example_tr", "Hakim boş zamanlarında sivil giyim giyiyor",
     "Hâkim boş zamanlarında sivil kıyafet giyiyor",
     "«giyim giymek» — тавтология, и потеряна шляпка"),
    (16690, "example_pl", "W pracy nosi ubranie cywilne",
     "Sędzia w czasie wolnym nosi ubranie cywilne",
     "в эталоне свободное время, а не работа"),
    # 9325 Lügendetektor
    (16691, "example_tr", "Yalan detektörü birçok ülkede kabul görmüyor",
     "Yalan makinesi birçok ülkede kabul görmüyor",
     "перевод слова — «yalan makinesi»"),
    (16691, "example_pl", "Musiał przejść badanie wykrywaczem kłamstw",
     "Wykrywacz kłamstw nie jest dopuszczalny w wielu krajach",
     "перевод другого предложения"),
    # 9327 abwechselnd
    (18880, "example_uk", "Вони працюють по черзі у змінах",
     "Вони працюють по черзі в зміні",
     "в эталоне «in der Schicht» в единственном"),
    # 9328 Gasthof
    (17319, "example_uk", "Невеликий готель у селі дуже затишний",
     "Невелика корчма в селі дуже затишна",
     "перевод слова — «корчма»"),
    (17319, "example_tr", "Hancı bize sıcak çorba getirdi",
     "Köydeki küçük han çok rahat",
     "перевод другого предложения"),
    # 9330 Vorgesetzte
    (9178, "example_tr", "Amire bana iyi geribildirim verdi",
     "Amirim bana iyi geri bildirim verdi",
     "«Amire» не форма, и «geri bildirim» раздельно"),
    # 9331 Autofahrer
    (17320, "example_uk", "Водій швидко гальмував, щоб уникнути аварії",
     "Водій швидко загальмував, щоб уникнути аварії",
     "«гальмував» незавершённое, а в эталоне «bremste»"),
    # 9332 Schriftrolle
    (14711, "example_tr", "Eski yazma müzede sergilendi",
     "Eski parşömen tomarı müzede sergilendi",
     "перевод слова — «parşömen tomarı»"),
    (14711, "example_pl", "Stary zwój leżał w muzeum za szybą",
     "Stary zwój został wystawiony w muzeum",
     "перевод другого предложения"),
    # 9333 Wartezeit
    (18881, "example_ru", "Время ожидания у врача было долгим",
     "Время ожидания у стоматолога было долгим",
     "в эталоне «beim Zahnarzt»"),
    # 9334 Säugling
    (15245, "example_tr", "Bebek beslenme sonrası uyuyor",
     "Bebek emzirildikten sonra uyuyor",
     "«beslenme sonrası» — обрывок"),
    (15245, "example_pl", "Niemowlę zasnęło po karmieniu",
     "Niemowlę śpi po karmieniu",
     "эталон в настоящем времени"),
    # 9335 Bewerbungsgespräch
    (9179, "example_uk", "Інтерв'ю тривало пів години",
     "Співбесіда тривала пів години",
     "перевод слова — «співбесіда»"),
    # 9336 königlich
    (16692, "example_pl", "Zwiedzaliśmy królewski zamek nad rzeką",
     "Królewski pałac jest imponujący",
     "перевод другого предложения"),
    # 9337 Aktivierung
    (12974, "example_ru", "Активизация мышц важна для здоровья",
     "Активация мышц важна для здоровья",
     "перевод слова — «активация»"),
    # 9338 Korsett
    (13752, "example_uk", "Корсет був модою в XIX столітті",
     "Корсет був у моді в XIX столітті",
     "«був модою» — не по-украински"),
    # 9339 ungerade
    (14876, "example_tr", "Tek sayılar 1, 3, 5tir",
     "Tek sayılar 1, 3, 5'tir",
     "потерян апостроф"),
    # 9340 ägyptisch
    (8189, "example_ru", "Египетская культура очаровательна",
     "Египетская культура завораживает",
     "«faszinierend» — завораживающая"),
    (8189, "example_pl", "Lubię egipską kuchnię",
     "Kultura egipska jest fascynująca",
     "перевод другого предложения"),
    # 9343 Erdbeere
    (227, "example_pl", "Kupiłam truskawki na targu",
     "Truskawki są słodkie",
     "перевод другого предложения"),
    # 9344 hingeben
    (11313, "example_uk", "Вона цілком присвячувала себе роботі",
     "Вона цілком присвятила себе роботі",
     "эталон в совершённом виде"),
    # 9345 verweisen
    (8190, "example_en",
     "The teacher pointed the student to the correct answer",
     "The doctor had to refer me to a specialist",
     "перевод другого предложения"),
    (8190, "example_uk", "Лікар направив мене до хірурга",
     "Лікар мусив направити мене до спеціаліста",
     "в эталоне специалист, и потеряно «musste»"),
    (8190, "example_tr", "Öğretmen öğrenciyi doğru cevaba işaret etti",
     "Doktor beni bir uzmana yönlendirmek zorunda kaldı",
     "перевод другого предложения"),
    (8190, "example_pl", "Odesłali mnie do innego okienka",
     "Lekarz musiał skierować mnie do specjalisty",
     "перевод другого предложения"),
    # 9346 Postfach
    (14246, "example_tr", "Mektuplarım posta kutusu 42ye gider",
     "Mektuplarım 42 numaralı posta kutusuna gidiyor",
     "потерян апостроф и падеж"),
    # 9347 Steg
    (18404, "example_uk", "Ми пройшли місток до озера",
     "Ми пройшли містком до озера",
     "«пройшли місток» — не то управление"),
    (18404, "example_tr", "Gölün yanına köprüden yürüdük",
     "Tahta köprüden geçerek göle indik",
     "«gölün yanına yürüdük» — обрывок"),
    (18404, "example_pl", "Siedzieliśmy na pomoście nad jeziorem",
     "Przeszliśmy przez kładkę w dół do jeziora",
     "перевод другого предложения"),
    # 9348 Pfefferminz
    (11930, "example_ru", "Чай со вкусом мяты и очень освежающий",
     "Чай имеет вкус мяты и очень освежает",
     "фраза без сказуемого"),
    (11930, "example_uk", "Чай зі смаком м'яти і дуже освіжує",
     "Чай має смак м'яти і дуже освіжає",
     "фраза без сказуемого"),
    # 9349 ehemals
    (18882, "example_tr", "O bir zamanlar bu okulun müdürü idi",
     "O bir zamanlar bu okulun müdürüydü",
     "«idi» отдельно"),
    # 9351 Sonderangebot
    (9904, "example_uk", "У магазині сьогодні чудова спецпропозиція",
     "Це спецпропозиція",
     "перевод другого предложения"),
    (9904, "example_pl", "Kawa jest dziś w promocji",
     "To oferta specjalna",
     "перевод другого предложения"),
    # 9352 geistlich
    (14712, "example_tr", "Kilisedeki ruhani müzik harika idi",
     "Kilisedeki ruhani müzik harikaydı",
     "«idi» отдельно"),
    (14712, "example_pl", "Muzyka duchowna w kościele była piękna",
     "Muzyka duchowna w kościele była wspaniała",
     "«wunderbar» — чудесная"),
    # 9353 Lieblingsfilm
    (12340, "example_tr", "Benim favori filmim 80lerin bir klasiği",
     "Benim favori filmim 80'lerin bir klasiği",
     "потерян апостроф"),
    # 9354 Predigt
    (14713, "example_pl", "Kazanie w kościele było dzisiaj bardzo długie",
     "Kazania proboszcza są zawsze bardzo długie",
     "перевод другого предложения"),
    # 9355 Mätresse
    (15246, "example_uk", "У короля була коханка багато років",
     "У короля багато років була коханка",
     "порядок слов"),
    (15246, "example_tr",
     "Kral uzun yıllar boyunca bir metresine sahipti",
     "Kralın uzun yıllar boyunca bir metresi vardı",
     "«sahip olmak» о человеке — калька"),
    (15246, "example_pl", "Król miał piękną metresę",
     "Król miał metresę przez wiele lat",
     "«piękną» в эталоне нет, годы потеряны"),
    # 9356 Ratgeber
    (9596, "example_en", "I read a guide about personal finances",
     "I read a guide about finances",
     "«personal» в эталоне нет"),
    (9596, "example_uk", "Я прочитав порадник про особисті фінанси",
     "Я прочитав порадник про фінанси",
     "«особисті» в эталоне нет"),
    (9596, "example_tr", "Danışmanım bu karara çok yardım etti",
     "Finans konusunda bir rehber kitap okudum",
     "перевод другого предложения"),
    # 9357 allerlei
    (8192, "example_pl", "Na targu były różnego rodzaju owoce",
     "Na targu były różnego rodzaju interesujące rzeczy do kupienia",
     "перевод другого предложения"),
    # 9358 Abwurf
    (12341, "example_uk", "Скидання пакетів відбулось з літака",
     "Пакети скидали з літака",
     "«відбулось з» — не то управление"),
    (12341, "example_tr",
     "Paketlerin uçaktan atılması gece yarısında yapıldı",
     "Paketlerin uçaktan atılması gerçekleşti",
     "«gece yarısında» в эталоне нет"),
    # 9359 Showgeschäft
    (14714, "example_tr", "O, on yıldır gösteri endüstrisinde çalışıyor",
     "O, on yıldır şov dünyasında çalışıyor",
     "перевод слова — «şov dünyası»"),
    (14714, "example_pl", "Pracuje w show-biznesie od lat",
     "Pracuje w show-biznesie już od dziesięciu lat",
     "потеряны десять лет"),
    # 9360 verfault
    (11931, "example_uk", "Фрукт гнилий і більше не їстівний",
     "Фрукти гнилі й більше не їстівні",
     "«das Obst» собирательное"),
    (11931, "example_tr", "Meyve çürümüş ve artık yenilemez",
     "Meyve çürümüş ve artık yenmez",
     "«yenilemez» это «нельзя обновить»"),
    # 9361 Wohlbefinden
    (12975, "example_uk", "Добробут дітей дуже важливий для нас",
     "Самопочуття дітей дуже важливе для нас",
     "«добробут» о материальном достатке"),
    # 9362 Strolch
    (11314, "example_ru",
     "Маленький озорник снова сыграл со мной шутку",
     "Маленький озорник снова подшутил надо мной",
     "«сыграть шутку» — не то выражение"),
    # 9363 schrumpfen
    (8193, "example_en", "Careful, wool shrinks in hot water",
     "The sweater shrank in the wash",
     "перевод другого предложения"),
    (8193, "example_uk", "Светр дав усадку при прання",
     "Светр сів після прання",
     "«при прання» — сломанный падеж"),
    (8193, "example_tr", "Kazak yıkamada çekildi",
     "Kazak yıkamada çekti",
     "«çekildi» это страдательное «был снят»"),
    # 9364 Privatjet
    (17321, "example_uk",
     "Багатий чоловік літав у відпустку на своєму приватному літаку",
     "Багатий чоловік полетів у відпустку своїм приватним літаком",
     "«літав» о регулярности, а в эталоне один раз"),
    (17321, "example_tr", "Zengin adam tatile özel jetinde uçtu",
     "Zengin adam tatile özel jetiyle uçtu",
     "летят «jetiyle», не «jetinde»"),
    # 9365 Untergeschoss
    (18405, "example_uk",
     "Майстерня знаходиться у цокольному поверсі будинку",
     "Майстерня знаходиться на цокольному поверсі будинку",
     "на поверсі, а не у поверсі"),
    (18405, "example_pl", "Warsztat jest w suterenie",
     "Warsztat znajduje się w suterenie domu",
     "потеряно «des Hauses»"),
    # 9366 unvergesslich
    (11315, "example_tr", "Bu benim için unutulmaz bir deneyim idi",
     "Bu benim için unutulmaz bir deneyimdi",
     "«idi» отдельно"),
    # 9367 totschlagen
    (16694, "example_en", "He's trying to stifle the discussion",
     "We're killing time with cards",
     "перевод другого предложения"),
    (16694, "example_ru", "Он пытается заглушить дискуссию",
     "Мы убиваем время за картами",
     "перевод другого предложения"),
    (16694, "example_uk", "Ми вбивали час за картами",
     "Ми вбиваємо час за картами",
     "эталон в настоящем времени"),
    (16694, "example_tr", "Tartışmayı bitirmeye çalışıyor",
     "Kartlarla vakit öldürüyoruz",
     "перевод другого предложения"),
    # 9368 Attraktion
    (12342, "example_uk",
     "Американські гірки — популярна атракція в парку розваг",
     "Американські гірки — популярний атракціон у парку розваг",
     "по-украински «атракціон»"),
    (12342, "example_tr",
     "Dönme doğramaca parkta popüler bir eğlencedir",
     "Hız treni eğlence parkında popüler bir atraksiyondur",
     "«dönme doğramaca» — не американские горки и вообще не предмет"),
    # 9369 Speichel
    (12976, "example_en", "Saliva was dripping from the dogs mouth",
     "Saliva is dripping from the dog's mouth",
     "потерян апостроф, и время"),
    (12976, "example_uk", "У собаки текла слина з пащі",
     "У собаки тече слина з пащі",
     "эталон в настоящем времени"),
    # 9370 Referat
    (9597, "example_uk",
     "Я повинен підготувати доповідь про зміну клімату до п'ятниці",
     "Я повинен до п'ятниці виступити з доповіддю про зміну клімату",
     "«halten» — выступить, а не подготовить"),
    # 9371 baumeln
    (8194, "example_uk", "Ноги дитини бовтаються над підлогою",
     "Ноги дитини бовтаються під столом",
     "в эталоне «unter dem Tisch»"),
    # 9372 Chemotherapie
    (12977, "example_tr", "Hasta kemoterapi görmektedir",
     "Hasta kemoterapi görüyor",
     "«-mektedir» книжное для разговорной фразы"),
    # 9373 hämisch
    (11316, "example_tr", "Benim hatasından kötü niyetle güldü",
     "Hatama alaycı bir şekilde güldü",
     "«Benim hatasından» — сломанная фраза"),
    # 9374 Psychose
    (12978, "example_tr", "Doktor akut psikoz teşhis koydu",
     "Doktor akut psikoz teşhisi koydu",
     "потерян изафет"),
    # 9375 Olivenöl
    (675, "example_uk",
     "Я готую з оливковою олією замість вершкового масла",
     "Я люблю готувати на оливковій олії, а не на вершковому маслі",
     "готують на олії, и потеряно «gerne»"),
    # 9377 Straftäter
    (16695, "example_pl", "Przestępca został zatrzymany przez policję",
     "Przestępca został aresztowany",
     "«przez policję» в эталоне нет"),
    # 9379 bewaffnen
    (16696, "example_ru", "Правительство вооружало ополчение",
     "Правительство вооружило ополчение",
     "эталон в совершённом виде"),
    (16696, "example_uk", "Уряд озброював ополчення",
     "Уряд озброїв ополчення",
     "эталон в совершённом виде"),
    (16696, "example_tr", "Hükümet miliyi silahlandırdı",
     "Hükümet milis gücünü silahlandırdı",
     "«mili» — не форма"),
    (16696, "example_pl", "Rząd uzbroił oddziały ochotników",
     "Rząd uzbroił milicję",
     "в эталоне «Miliz»"),
    # 9381 entfalten
    (8196, "example_uk", "Квітка розгортала свої пелюстки",
     "Квітка розкрила свої пелюстки",
     "эталон в совершённом виде"),
    (8196, "example_tr", "Bahçede çiçekler açıyor",
     "Çiçek taç yapraklarını açtı",
     "перевод другого предложения"),
    # 9382 Sondereinheit
    (16698, "example_ru",
     "Спецвойска были вызваны для выполнения операции",
     "Спецподразделение вызвали на операцию",
     "перевод слова — «спецподразделение»"),
    (16698, "example_uk",
     "Спеціальні сили були викликані на виконання операції",
     "Спецпідрозділ викликали на операцію",
     "перевод слова — «спецпідрозділ»"),
    (16698, "example_tr", "Özel birim görevlendirilmek için çağırıldı",
     "Özel birim göreve çağrıldı",
     "«görevlendirilmek için çağırıldı» — двойная пассивность"),
    (16698, "example_pl", "Na miejsce wezwano jednostkę specjalną",
     "Wezwano jednostkę specjalną do akcji",
     "«na miejsce» в эталоне нет"),
    # 9383 sonnig
    (15754, "example_pl", "Dzisiaj jest ciepły, słoneczny dzień",
     "Dzisiaj jest słonecznie",
     "перевод другого предложения"),
    # 9387 Staatsgefängnis
    (16699, "example_pl", "Siedzi w więzieniu państwowym od roku",
     "Siedzi w więzieniu państwowym",
     "«od roku» в эталоне нет"),
    # 9389 verschwunden
    (8197, "example_en", "The disappeared wallet still hasn't been found",
     "The missing wallet still hasn't been found",
     "«disappeared wallet» — не по-английски"),
    (8197, "example_tr", "Kaybolan cüzdan hâlâ bulunamamıştır",
     "Kaybolan cüzdan hâlâ bulunamadı",
     "«-mıştır» книжное"),
    # 9390 Gefälligkeit
    (11318, "example_uk",
     "Можеш мені зробити послугу і принести цукор з кухні?",
     "Можеш зробити мені маленьку послугу і принести цукор з кухні?",
     "потеряно «kleine»"),
    # 9391 Organismus
    (18045, "example_uk", "Ці крихітні організми видні під мікроскопом",
     "Ці крихітні організми видно під мікроскопом",
     "«видні» — не форма"),
    # 9392 schlafen
    (11319, "example_uk", "Дитина вже спить у своєму ліжечку",
     "Спляча дитина виглядала такою безтурботною",
     "перевод другого предложения"),
    # 9394 zahm
    (15755, "example_tr", "Kuş o kadar evcil ki elimden beslenip yiyor",
     "Kuş o kadar evcil ki elimden yiyor",
     "«beslenip yiyor» — тавтология"),
    # 9395 Untertasse
    (11933, "example_uk", "Поставь чашку кави на блюдце",
     "Постав чашку кави на блюдце",
     "«Поставь» — русская форма повелительного"),
    (11933, "example_tr",
     "Kahve fincanının altındaki fincan tabağını unutma",
     "Kahve fincanını fincan tabağına koy",
     "перевод другого предложения"),
    # 9396 Lederjacke
    (13753, "example_tr",
     "Onun siyah deri ceketı gerçekten havalı görünüyor",
     "Onun siyah deri ceketi gerçekten havalı görünüyor",
     "«ceketı» — нарушена гармония гласных"),
    # 9397 Pipeline
    (17677, "example_pl", "Nowy rurociąg dostarcza gaz do miasta",
     "Rurociąg transportuje ropę przez cały kraj",
     "перевод другого предложения"),
    # 9398 Bürgerrecht
    (16700, "example_pl", "Walczyli o prawa obywatelskie dla wszystkich",
     "Prawa obywatelskie powinny być równe dla wszystkich ludzi",
     "перевод другого предложения"),
    # 9400 Untertreibung
    (14247, "example_uk",
     "Це справді недооцінка — фільм був просто фантастичний",
     "Це справді применшення — фільм був просто фантастичний",
     "перевод слова — «применшення»"),
    (14247, "example_tr", "Güzeldi demek eksik söylemek olur",
     "Bu gerçekten eksik bir ifade – film kesinlikle harikaydı",
     "перевод другого предложения"),
    # 9401 Umkleide
    (1992, "example_tr", "Soyunma odasında üstümü değiştirdim",
     "Üstümü değiştirmek için soyunma odasına gidiyorum",
     "эталон в настоящем и про цель"),
    # 9402 rätselhaft
    (8198, "example_pl", "Jego zachowanie jest dla mnie zagadkowe",
     "Jego zachowanie jest dla mnie całkowicie zagadkowe",
     "потеряно «völlig»"),
    # 9403 vollziehen
    (8199, "example_en", "The sentence will be executed tomorrow",
     "The change will take place slowly",
     "перевод другого предложения"),
    (8199, "example_uk", "Вирок буде виконаний завтра",
     "Зміни відбуватимуться поволі",
     "перевод другого предложения"),
    (8199, "example_tr", "Cezayı yarın sabah infaz edecekler",
     "Değişim yavaş yavaş gerçekleşecek",
     "перевод другого предложения"),
    # 9404 Vertuschung
    (16701, "example_en", "The cover-up of the truth is illegal",
     "The cover-up of the truth was illegal",
     "эталон в прошедшем времени"),
    (16701, "example_ru", "Сокрытие истины незаконно",
     "Сокрытие истины было незаконным",
     "эталон в прошедшем времени"),
    (16701, "example_uk", "Приховування правди незаконно",
     "Приховування правди було незаконним",
     "рассогласование рода, и время"),
    (16701, "example_tr", "Gerçeği gizlemek yasadışıdır",
     "Gerçeğin gizlenmesi yasadışıydı",
     "эталон в прошедшем, и подлежащее — сокрытие"),
    # 9405 Ministerin
    (16702, "example_ru", "Министра провела пресс-конференцию",
     "Министр провела пресс-конференцию",
     "«Министра» винительный падеж на месте подлежащего"),
    # 9406 langfristig
    (2648, "example_uk", "Це довгостроковий план",
     "Це довгостроковий план на майбутнє",
     "потеряно «für die Zukunft»"),
    (2648, "example_tr", "Bu uzun vadeli bir plan",
     "Bu, gelecek için uzun vadeli bir plan",
     "потеряно «für die Zukunft»"),
    # 9407 Absprache
    (14248, "example_pl", "Mieliśmy ustalenia co do ceny",
     "Mieliśmy ustalenie co do ceny",
     "эталон в единственном числе"),
    # 9408 Heide
    (15756, "example_uk", "Верета красива влітку",
     "Пустище красиве влітку",
     "«Верета» — нет такого слова"),
    (15756, "example_tr", "Fundalıkta uzun bir yürüyüş yaptık",
     "Fundalık yazın çok güzel",
     "перевод другого предложения"),
    (15756, "example_pl", "Latem wrzosowisko pięknie kwitnie",
     "Wrzosowisko jest piękne latem",
     "«kwitnie» в эталоне нет"),
    # 9409 Tanne — tr взял турецкий город вместо дерева
    (15757, "example_en", "The fir grows in the mountains",
     "The firs grow in the mountains",
     "эталон во множественном числе"),
    (15757, "example_ru", "Ель растёт в горах",
     "Пихты растут в горах",
     "перевод слова — «пихта», и множественное"),
    (15757, "example_uk", "Ялина росте в горах",
     "Ялиці ростуть у горах",
     "перевод слова — «ялиця», и множественное"),
    (15757, "example_tr", "Ladik dağlarda yetişir",
     "Köknarlar dağlarda yetişir",
     "«Ladik» это город в Турции, а не пихта"),
    (15757, "example_pl", "Przed domem rośnie wysoka jodła",
     "Jodły rosną w górach",
     "перевод другого предложения"),
    # 9410 entgegennehmen
    (8201, "example_pl", "Czy możesz odebrać paczkę od kuriera?",
     "Czy możesz odebrać paczkę?",
     "«od kuriera» в эталоне нет"),
    # 9412 Hochhaus
    (409, "example_en", "She lives in a high-rise in the city",
     "She lives in a high-rise in Berlin",
     "в эталоне Берлин"),
    (409, "example_uk", "Вона живе у багатоповерхівці в місті",
     "Вона живе у багатоповерхівці в Берліні",
     "в эталоне Берлин"),
    (409, "example_tr", "Bir gökdelende şehirde oturuyor",
     "Berlin'de bir gökdelende oturuyor",
     "порядок слов ломает фразу, и в эталоне Берлин"),
    # 9414 Zeigefinger
    (15247, "example_pl", "Pokazał drogę palcem wskazującym",
     "Pokazuję palcem wskazującym",
     "перевод другого предложения"),
    # 9416 Robe
    (13754, "example_uk", "Вона носить елегантну сукню",
     "Вона носить елегантну вечірню сукню",
     "перевод слова — «вечірня сукня»"),
    (13754, "example_tr", "Zarif bir elbise giyiyor",
     "Zarif bir abiye elbise giyiyor",
     "перевод слова — «abiye elbise»"),
    # 9417 Meeresgrund
    (15758, "example_uk", "Обломок лежить на морському дні",
     "Уламки корабля лежать на морському дні",
     "«обломок» — русизм, и «Wrack» это обломки"),
    # 9418 ignorant
    (11322, "example_uk", "Він зовсім неосвічений у цих питаннях",
     "Він справді неосвічений",
     "«у цих питаннях» в эталоне нет"),
    # 9419 verloben
    (15248, "example_pl", "Zaręczyli się w zeszłym miesiącu",
     "Właśnie się zaręczyli",
     "в эталоне «gerade», а не месяц назад"),
    # 9421 argumentieren
    (14249, "example_en", "He argues well",
     "He argues very well in discussions",
     "потеряно «sehr» и «in Diskussionen»"),
    (14249, "example_uk", "Він добре аргументує",
     "Він дуже добре аргументує в дискусіях",
     "потеряно «sehr» и «in Diskussionen»"),
    (14249, "example_tr", "İyi tartışıyor",
     "Tartışmalarda çok iyi gerekçe gösteriyor",
     "потеряно «sehr», и «tartışmak» это спорить"),
    # 9422 entbehrlich
    (8202, "example_pl", "Ten stary fotel jest zupełnie zbędny",
     "To jest całkowicie zbędne",
     "перевод другого предложения"),
    # 9424 abrechnen
    (9905, "example_uk", "Я хочу розрахуватися карткою",
     "Ми розраховуємося в кінці місяця",
     "перевод другого предложения"),
    # 9425 hereinkommen
    (8203, "example_pl", "Proszę wejść i zamknąć drzwi",
     "Właśnie wszedł",
     "перевод другого предложения"),
    # 9426 Babysitterin
    (9181, "example_uk", "Няня сидить з дітьми, поки ми в кіно",
     "Няня сьогодні ввечері догляне дітей, поки ми йдемо в кіно",
     "фраза урезана вдвое"),
    # 9427 Wiedervereinigung
    (3023, "example_tr", "Yeniden birleşme 1990'daydı",
     "Almanya'nın yeniden birleşmesi 1990'daydı",
     "потеряна Германия"),
    # 9428 Kämpferin
    (15249, "example_uk", "Вона відома борчиня за права жінок",
     "Вона смілива борчиня за справедливість і рівність",
     "перевод другого предложения"),
    (15249, "example_pl",
     "Ona jest prawdziwą bojowniczką o prawa kobiet",
     "Ona jest odważną bojowniczką o sprawiedliwość i równość",
     "перевод другого предложения"),
    # 9429 Wertsachen — эталон со строчным существительным
    (9906, "example_de", "Er verschloss alle Wertsachen in dem safe",
     "Er verschloss alle Wertsachen in dem Safe",
     "«Safe» — существительное, пишется с заглавной"),
    (9906, "example_uk", "Він закрив всі цінні речі в сейфі",
     "Він замкнув усі цінні речі в сейфі",
     "«verschloss» — замкнул, а не закрыл"),
    (9906, "example_pl", "Schowaj kosztowności do sejfu",
     "Zamknął wszystkie kosztowności w sejfie",
     "перевод другого предложения"),
    # 9431 Waschraum
    (3000, "example_uk",
     "У умивальні поруч з роздягальнею можна помитися",
     "В умивальні поруч з роздягальнею можна помитися",
     "«у» перед гласной"),
    # 9434 Wörtchen
    (14250, "example_uk", "Замов за мене словечко перед шефом",
     "Він сказав їй кілька приємних словечок",
     "перевод другого предложения"),
    # 9435 rausgeschnitten
    (8205, "example_tr", "Sahne filmden çıkartıldı",
     "Sahne filmden çıkarıldı",
     "«çıkartıldı» — лишний каузатив"),
    # 9436 Länge
    (8206, "example_pl", "Deski muszą mieć taką samą długość",
     "Deski muszą mieć dokładnie taką samą długość",
     "потеряно «genau»"),
    # 9437 kennzeichnen
    (8207, "example_tr", "Yol kırmızı oklar ile işaretlenmiş",
     "Yol kırmızı oklarla işaretlenmişti",
     "«oklar ile» раздельно, и время"),
    # 9438 todmüde
    (12982, "example_tr", "Uzun günün sonrasında yorgun dum",
     "Uzun günün sonunda ölesiye yorgundum",
     "«yorgun dum» — разорванное слово"),
    # 9439 nageln
    (8208, "example_ru",
     "Окно было прибито гвоздями и не могло быть открыто",
     "Окно было заколочено гвоздями и не открывалось",
     "«не могло быть открыто» — канцелярит"),
    # 9440 Glühwürmchen
    (15759, "example_pl", "Wieczorem widzieliśmy świetliki w ogrodzie",
     "Świetliki świeciły w ciemności",
     "перевод другого предложения"),
    # 9441 unartig
    (11324, "example_uk", "Дитина була неслухняна у дитячому садку",
     "Дитина сьогодні знову була неслухняна в дитячому садку",
     "потеряно «heute wieder»"),
    (11324, "example_tr",
     "Çocuk bugün oyun okulunda yine yaramaz davrandı",
     "Çocuk bugün anaokulunda yine yaramaz davrandı",
     "«oyun okulu» — не детский сад"),
    # 9442 prominent
    (8209, "example_uk", "На заході прийшло багато відомих людей",
     "На захід прийшло багато відомих людей",
     "«на заході прийшло» — сломанный падеж"),
    (8209, "example_pl", "Na otwarcie przyszło wielu znanych ludzi",
     "Na wydarzenie przyszło wielu znanych ludzi",
     "в эталоне «Veranstaltung», а не открытие"),
    # 9443 Blutspur
    (12983, "example_uk",
     "Поліція знайшла кров'яні сліди на місці злочину",
     "Поліція знайшла сліди крові на місці злочину",
     "перевод слова — «сліди крові»"),
    # 9444 Sodbrennen
    (12984, "example_tr", "Ağır yemekten sonra mide yanması oldu",
     "Ağır yemekten sonra midem yandı",
     "потерян «ich»: у кого была изжога"),
    # 9445 Rind
    (17864, "translation_uk",
     "корова, бик, велика рогата худоба, говядина",
     "корова, бик, велика рогата худоба, воловина",
     "«говядина» — русское слово"),
    (17864, "example_ru", "Фермер держит стадо коров на ферме",
     "Фермер держит стадо коров на своей ферме",
     "потеряно «seiner»"),
    (17864, "example_uk", "Фермер тримає стадо корів на фермі",
     "Фермер тримає стадо корів на своїй фермі",
     "потеряно «seiner»"),
    (17864, "example_pl", "Rolnik hoduje krowy i świnie",
     "Rolnik ma stado bydła na swojej farmie",
     "перевод другого предложения"),
    # 9446 Schlüsselbein
    (15250, "example_tr",
     "Bisiklet sürerken köprücük kemiklerini kırdı",
     "Bisiklet sürerken köprücük kemiğini kırdı",
     "ключица одна, а не обе"),
    # 9447 Schusswechsel
    (16709, "example_tr",
     "İki grup arasında yoğun bir ateş değişimi yaşandı",
     "İki grup arasında yoğun bir silahlı çatışma yaşandı",
     "«ateş değişimi» — калька"),
    # 9448 Bombenanschlag
    (16710, "example_ru", "Взрыв произошел во время часа пик",
     "Взрыв бомбы произошёл во время часа пик",
     "потеряна бомба, и «ё»"),
    (16710, "example_uk", "Вибух стався під час години пік",
     "Вибух бомби стався під час години пік",
     "потеряна бомба"),
    (16710, "example_tr",
     "Bomba saldırısı yoğun saatlerde meydana geldi",
     "Bombalı saldırı yoğun saatlerde meydana geldi",
     "перевод слова — «bombalı saldırı»"),
    # 9450 Telefonanruf
    (14251, "translation_tr", "telefon görüşmesi, telefon aramas",
     "telefon görüşmesi, telefon araması",
     "«aramas» — обрубленное слово"),
    (14251, "example_tr",
     "Annemin telefon görüşmesi tam zamanında geldi",
     "Annemin telefonu tam zamanında geldi",
     "«görüşme gelmez» — не то слово"),
    (14251, "example_uk", "Дзвінок від моєї мами прийшовся до речі",
     "Телефонний дзвінок від мами був саме вчасно",
     "«прийшовся до речі» — калька"),
    # 9453 Nordwesten
    (15760, "example_uk", "Вітер дув з північно-західного напрямку",
     "Вітер дув з північного заходу",
     "лишнее «напрямку»"),
    # 9455 Anstoß
    (2195, "example_en", "That gave me an impetus to think about it",
     "That was an impetus to think",
     "в эталоне нет «мне» и «об этом»"),
    (2195, "example_uk", "Це був добрий стимул працювати краще",
     "Це був поштовх до роздумів",
     "перевод другого предложения"),
    # 9456 Glückseligkeit
    (11326, "example_uk", "Вона світилася щастям",
     "Вона сяяла від блаженства",
     "перевод слова — «блаженство»"),
    (11326, "example_tr", "Mutluluğundan parlıyordu",
     "Saadetinden parlıyordu",
     "перевод слова — «saadet»"),
    # 9457 Schwergewicht
    (12345, "example_uk", "Цей важковаговик виграв усі бої",
     "Він важковаговик у своїй галузі",
     "перевод другого предложения"),
    (12345, "example_tr", "Sektöründe ağır sıklet",
     "Sektöründe bir ağır sıklet",
     "фраза без связки"),
    # 9459 Lebensmittelvergiftung
    (12986, "example_tr", "Gıda zehirlenmesi vardı",
     "Gıda zehirlenmesi geçirdi",
     "потерян «er»: у кого было отравление"),
    # 9460 Kojote
    (15761, "example_uk", "Койот виття ночами в пустелі",
     "Койот вив уночі",
     "«виття» это существительное, фраза без сказуемого"),
    (15761, "example_pl", "W nocy słyszeliśmy wycie kojota",
     "Kojot wył w nocy",
     "перевод другого предложения"),
    # 9461 Einwand
    (14252, "example_en", "Do you have any further objections?",
     "Do you have another objection?",
     "эталон в единственном числе"),
    (14252, "example_uk", "У тебе є ще якісь заперечення?",
     "У тебе є ще якесь заперечення?",
     "эталон в единственном числе"),
    (14252, "example_pl", "Masz jeszcze jakieś zastrzeżenia?",
     "Masz jeszcze jakieś zastrzeżenie?",
     "эталон в единственном числе"),
    # 9462 Zahnschmerz
    (12987, "example_tr", "Korkunç bir diş ağrısı var",
     "Korkunç bir diş ağrım var",
     "потерян «ich»: у кого болит"),
    # 9464 Leichtigkeit
    (11328, "example_tr", "Büyük hafiflikle dans etti",
     "Büyük bir rahatlıkla dans etti",
     "«hafiflik» о весе, а тут о непринуждённости"),
    # 9465 Tripper
    (12989, "example_tr", "Gonore vardı ve utandı",
     "Belsoğukluğu vardı ve utanıyordu",
     "перевод слова — «belsoğukluğu», и потерян «er»"),
    # 9466 Storch
    (15762, "example_pl", "Na dachu stodoły siedzi bocian",
     "Bocian leci nad naszym domem",
     "перевод другого предложения"),
    # 9467 willig
    (11329, "example_tr", "Bana yardım etmeye istekli idi",
     "Bana yardım etmeye istekliydi",
     "«idi» отдельно"),
    # 9469 Veteran
    (15251, "example_pl", "Mój dziadek jest weteranem wojny",
     "Jest doświadczonym weteranem",
     "перевод другого предложения"),
    # 9470 Ausverkauf
    (9907, "example_uk",
     "На розпродажу в H&M сьогодні справді гарні знижки",
     "На розпродажі в H&M сьогодні справді гарні знижки",
     "«на розпродажу» — не тот падеж"),
    (9907, "example_tr",
     "H&Mdeki indirim satışında bugün gerçekten iyi fiyatlar var",
     "H&M'deki indirimde bugün gerçekten iyi fiyatlar var",
     "потерян апостроф, и «indirim satışı» — тавтология"),
    (9907, "example_pl", "Kupiłam te buty na wyprzedaży",
     "Na wyprzedaży w H&M są dziś naprawdę dobre okazje",
     "перевод другого предложения"),
    # 9471 Nabelschnur
    (15252, "example_uk",
     "Пуповина перерізується відразу після народження",
     "Пуповину перерізають відразу після народження",
     "«перерізується» — канцелярит"),
    (15252, "example_pl",
     "Lekarz przeciął pępowinę zaraz po porodzie",
     "Pępowinę przecina się zaraz po narodzinach",
     "эталон страдательный и в настоящем"),
    # 9472 Ladenbesitzer
    (9183, "example_uk",
     "Власник магазину знає своїх постійних клієнтів",
     "Власник магазину знає майже всіх своїх постійних клієнтів",
     "потеряно «fast alle»"),
    (9183, "example_tr", "Dükkan sahibi tüm düzenli müşterilerini tanır",
     "Dükkân sahibi neredeyse bütün müdavimlerini tanır",
     "«tüm» вместо «fast alle», и «düzenli müşteri» — калька"),
    # 9473 träge
    (11331, "example_tr",
     "Sabahleyin ben hâlâ oldukça ağır hissediyorum",
     "Sabahları hâlâ oldukça hareketsizim",
     "«ağır hissetmek» — не то выражение"),
    # 9474 impotent
    (16711, "example_ru",
     "Глава правительства казался совершенно бессильным перед кризой",
     "Глава правительства казался совершенно бессильным перед кризисом",
     "«кризой» — нет такой формы"),
    # 9476 Algorithmus
    (17678, "example_pl", "Algorytm podpowiada mi nowe filmy",
     "Algorytm automatycznie wylicza najlepszą trasę",
     "перевод другого предложения"),
    # 9477 Verstärker
    (17679, "example_tr",
     "Gitar amplifikatörü çok gürültülü, sessiz yapabilir misin",
     "Gitar amplifikatörü çok yüksek, sesini kısabilir misin",
     "«gürültülü» о шуме, и «sessiz yapmak» — калька"),
    (17679, "example_pl", "Podłącz gitarę do wzmacniacza",
     "Wzmacniacz gitarowy jest za głośny, możesz go przyciszyć",
     "перевод другого предложения"),
    # 9478 Unterleib
    (12990, "example_en",
     "She has pain in her abdomen, maybe she should see a doctor",
     "She has pain in her lower abdomen, maybe she should see a doctor",
     "«Unterleib» — низ живота"),
    (12990, "example_uk",
     "У неї болить живіт, можливо їй потрібно до лікаря",
     "У неї болить низ живота, можливо, їй варто піти до лікаря",
     "потерян низ живота, и пропущена запятая"),
    (12990, "example_tr",
     "Karın bölgesinde ağrısı var, belki doktora gitmeli",
     "Alt karın bölgesinde ağrısı var, belki doktora gitmeli",
     "«Unterleib» — низ живота"),
    # 9480 Linde
    (15763, "example_tr",
     "Parkta eski ihlamur ağaçlarının altında güzelce serindir",
     "Parktaki eski ıhlamur ağaçlarının altı güzelce serin",
     "«ihlamur» с точкой над «i», и фраза без подлежащего"),
    (15763, "example_pl", "Pod starą lipą jest przyjemny chłód",
     "Pod starymi lipami w parku jest przyjemnie chłodno",
     "эталон во множественном, и потерян парк"),
    # 9481 Violine
    (14715, "example_tr",
     "10 yıldan beri keman çalıyor ve gerçekten yetenekli",
     "10 yıldır keman çalıyor ve gerçekten yetenekli",
     "«yıldan beri» — калька"),
    (14715, "example_pl", "Gra na skrzypcach od dziesięciu lat",
     "Gra na skrzypcach od dziesięciu lat i jest naprawdę utalentowana",
     "потеряна вторая половина"),
    # 9482 verkürzen
    (8210, "example_uk", "Давай скоротимо зустріч до півгодини",
     "Чи можемо ми скоротити зустріч? У мене потім ще одна",
     "перевод другого предложения"),
    # 9483 Sensor
    (17680, "example_pl", "Czujnik ruchu włącza światło na korytarzu",
     "Czujnik wykrywa ruch i włącza światło",
     "перевод другого предложения"),
    # 9486 Koje
    (17326, "example_ru",
     "Моя каюта на корабле очень маленькая, но уютная",
     "Моя койка на корабле очень маленькая, но уютная",
     "перевод слова — «койка»"),
    (17326, "example_uk",
     "Моя каюта на кораблі дуже невелика, але затишна",
     "Моя койка на кораблі дуже маленька, але затишна",
     "перевод слова — «койка»"),
    (17326, "example_tr", "Gemi üzerindeki yatağım çok küçük ama rahat",
     "Gemideki ranzam çok küçük ama rahat",
     "«gemi üzerinde» это на крыше корабля"),
    # 9487 Inflation
    (17865, "example_pl", "Inflacja znowu rośnie i wszystko drożeje",
     "Inflacja ciągle rośnie, to duży problem",
     "перевод другого предложения"),
    # 9488 Hauptdarsteller
    (14716, "example_pl", "Główny bohater tego filmu gra świetnie",
     "Odtwórca głównej roli w tym filmie jest naprawdę "
     "niewiarygodnie dobry",
     "перевод другого предложения"),
    # 9489 Vorgeschmack
    (8211, "example_uk", "Я вже хвилююся від передчуття відпустки",
     "Передчуття відпустки вже хвилює",
     "подлежащее подменено"),
    (8211, "example_tr", "Tatil öncesi tadı zaten heyecan verici",
     "Tatilin ön tadı bile heyecan verici",
     "«tatil öncesi tadı» — обрывок"),
    (8211, "example_pl", "To był tylko przedsmak wakacji",
     "Przedsmak wakacji już jest ekscytujący",
     "перевод другого предложения"),
    # 9494 Sommerhaus
    (18408, "example_uk",
     "Ми проводимо кожний серпень у нашому літньому будинку на озері",
     "Ми проводимо кожного серпня в нашому літньому будинку біля озера",
     "«кожний серпень» и «на озері» — не те падежи"),
    (18408, "example_tr",
     "Her Ağustosu göl kenarındaki yazlığımızda geçirebiliyoruz",
     "Her ağustosu göl kenarındaki yazlığımızda geçiriyoruz",
     "«geçirebiliyoruz» это «можем проводить»"),
    (18408, "example_pl", "Lato spędzamy w domku letniskowym nad jeziorem",
     "Każdy sierpień spędzamy w naszym domku letniskowym nad jeziorem",
     "в эталоне каждый август, а не лето"),
    # 9495 Fairness
    (11332, "example_ru",
     "В этой игре нет справедливости, все жульничают",
     "В этой игре нет честности, все жульничают",
     "«Fairness» — честность, а не справедливость суда"),
    (11332, "example_tr", "Bu oyunda adalet yok, herkes hile yapıyor",
     "Bu oyunda adillik yok, herkes hile yapıyor",
     "«adalet» это правосудие, а «Fairness» — adillik"),
    # 9497 ehrwürdig
    (11333, "example_uk", "Шанований професор був поважаний всіма",
     "Шанованого професора поважали всі",
     "«був поважаний» — калька страдательного"),
    (11333, "example_tr",
     "Saygıdeğer profesör herkes tarafından saygı duyuluyordu",
     "Saygıdeğer profesöre herkes saygı duyuyordu",
     "«saygı duymak» требует датива"),
    # 9499 Trauzeugin
    (15253, "example_pl",
     "Moja siostra będzie świadkową na moim weselu",
     "Moja najlepsza przyjaciółka będzie świadkową na moim weselu",
     "в эталоне лучшая подруга, а не сестра"),
    # 9500 Absolution
    (14717, "example_tr",
     "Papaz itiraf sonrasında ona bağışlanma verdi",
     "Papaz, günah çıkarmanın ardından ona günah affı verdi",
     "«itiraf» это признание в суде, исповедь — «günah çıkarma»"),
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
