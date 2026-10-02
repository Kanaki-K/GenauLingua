# Ручная вычитка 200 рядов (зерно 777)

Читал глазами, ряд за рядом. Формальные проверки на всём этом молчат: буквы
правильные, диакритика на месте, слово в примере присутствует.

Доля рядов хотя бы с одним замечанием — **около трети**.

---

## 1. Битые данные

| id | слово | что |
|---|---|---|
| 14493 | Schöpfer | uk: `творець, 創創` — **китайские иероглифы** |
| 12252 | bergab | pl: `w dół, z górki, pod górę w dół` — последнее бессмысленно |
| 2772 | Rücksendung | tr: `İade/geri gönderim` — осталась разметка со слешем |

## 2. Несуществующие слова и опечатки

| id | слово | язык | написано | надо |
|---|---|---|---|---|
| 15673 | Nachtigall | uk | Соловей **поє** | співає |
| 8324 | geschmeidig | uk | рухалась **грацьозно** | граційно |
| 11757 | Cocktail | tr | bir **koktey** | kokteyl |
| 15170 | Witwer | tr | çok **özlediydi** | özlüyordu |
| 17182 | Skipper | tr | deneyimli bir **denizcı** | denizci |
| 12273 | campen | uk | будемо **кемпувати** | відпочивати в наметах |
| 11027 | erwünscht | tr | her zaman **hoşlanılıyor** | hoş karşılanır |

## 3. Русизмы в украинской колонке

| id | слово | написано | надо |
|---|---|---|---|
| 17372 | Kerosin | **керосин** | гас |
| 11445 | anregend | **бодрящий** | бадьорливий |
| 11466 | ermutigend | **ободрюючі** слова | підбадьорливі |
| 17148 | Fähre | на **пароме** | на поромі |
| 16326 | Spurensicherung | багато **улік** | доказів |
| 8826 | Detektiv | нові **улики** | докази |
| 8663 | eingehend | **тщательне** розслідування | ретельне |
| 11580 | Zynismus | **язвливість** | ущипливість |
| 16444 | Bankräuber | **нальотчик** | нальотник |
| 11478 | Fehlverhalten | до його **відстранення** | відсторонення |
| 10947 | wundere | він більше не **звонить** | дзвонить |
| 10271 | beleidigt | **образжений**, ображений | дубль, первого слова нет |

## 4. Неверный смысл

| id | слово | что |
|---|---|---|
| 13721 | Baumwolle | ru/uk: «хлопок, **вата**» — вата это Watte |
| 18254 | Kran | pl/en: добавлен водопроводный кран, а немецкий Kran только подъёмный |
| 7034 | erteilen | tr: `yeni bir **sipariş** verdi` — заказ вместо задания |
| 7695 | ausländisch | pl: `zagranicznych **klientów**` — клиенты вместо коллег |
| 17342 | Reiseführer | ru/uk: «**Путеводитель** показал нам» — книга не может показывать |
| 16205 | Stiftung | pl: `pomaga **chorym** dzieciom` — больным вместо бедных |
| 16444 | Bankräuber | pl: `po **tygodniu**` против немецкого `nach drei Tagen` |
| 15739 | wogen | ru: «Волны **волновались**» — надо «колыхались» |
| 7796 | unterlegen | uk: «сильнішій команді **непідвладна**» — не то слово |

## 5. Неверные немецкие заголовки

| id | стоит | надо |
|---|---|---|
| 16322 | der **Abgeordneter** | der Abgeordnete |
| 10947 | **wundere** | sich wundern |
| 8574 | **ausgesaugt** | aussaugen |
| 11588 | **Befürchtungen** | Befürchtung |

## 6. Примеры, переводящие другое предложение

Самый массовый класс — около **55 на 200 рядов**. Немецкий пример про одно,
перевод про другое.

Примеры из найденного:

| id | слово | немецкий | перевод |
|---|---|---|---|
| 942 | trinken | Ich trinke Wasser | uk: Хочеш випити чаю з нами? |
| 1272 | bewahren | Wir müssen einen kühlen Kopf bewahren | en: Keep the receipt |
| 15739 | wogen | Die Wellen wogen hin und her | uk: Я дуже хвилююся перед екзаменом |
| 14393 | Werk | ein schönes Werk der modernen Kunst | en: a beautiful work by Picasso |
| 1718 | Nähe | In der Nähe ist ein Supermarkt | en: There's a nice park in the vicinity |
| 10422 | aufregen | Du musst dich nicht so aufregen | en: That annoys me |
| 908 | Tablette | Ich nehme jeden Morgen eine Tablette | en: She takes a tablet |
| 1462 | Gegensatz | Die beiden Brüder sind ein echter Gegensatz | en: That is the opposite |
| 7640 | beistehen | Ich werde dir immer beistehen | en: She supported me during difficult times |
| 2954 | verpacken | Kannst du das Geschenk schön verpacken? | en: I pack the gift |

---

## Что из этого чинится чем

**Русизмы, опечатки, неверный смысл** — только переводом заново. Это деньги
на API.

**Непараллельные примеры** — прогоном `fix_parallel_examples --lang <язык>`.
Инструмент написан и проверен, польский и часть русского им уже исправлены.
Тоже деньги.

**Неверные немецкие заголовки** — `fix_lemmas`, уже отработал на 463 словах,
эти остались в столкновениях и ждут решения, какую строку оставить.

**Иероглифы и разметка** — точечная правка, бесплатно, но надо знать
правильный перевод.

---

# Ряды 201–300 (тот же круг, зерно 777)

## Порча знаний смыслом

| id | слово | что |
|---|---|---|
| 9563 | **Fünfer** | Немецкая «пятёрка» — это **двойка**, худшая оценка (mangelhaft). В русском и украинском переведено «пятёрка», и пример «Ученик получил пятёрку по математике» учит обратному. Человек выучит, что Fünfer — это отлично. |
| 18836 | täglich | ru: «помогает оставаться **в форме**» против немецкого «organisiert zu bleiben» — организованным |
| 16680 | Erbschaft | de: наследство **от дяди**, pl: `spadek po **dziadku**` — от деда |
| 16883 | Kriegsgebiet | ru: перевод «зона боевых действий», а в примере «Боевая зона» — другая форма |

## Несуществующие слова и грамматика

| id | слово | язык | написано | надо |
|---|---|---|---|---|
| 11122 | sinnlos | uk | нікуди не **ведить** | не веде |
| 15487 | Hahn | uk | Півень **кукарічить** | кукурікає |
| 16147 | Invasion | uk | було **важною** подією | важливою |
| 13024 | kribbeln | uk | **Мене щипле шкіру** | У мене щипає шкіру |
| 13935 | Missverständnis | en | That **wa's** just | was |
| 16946 | Doppelagent | ru | играл обе стороны **против друг друга** | друг против друга |
| 15837 | verschmutzt | tr | gömleği tamamen **kir olmuştu** | kirlenmişti |
| 12316 | Karaoke | tr | çok **yüksek seslice** | yüksek sesle |
| 13749 | auslachen | tr | **ona alay ettiler** | onunla alay ettiler |
| 10864 | Gespür | pl | **nosa do czegoś** | nos do czegoś |
| 6761 | verwickelt | uk | **заплутаний** у скандалі | замішаний |
| 8648 | unerkannt | uk | покинув місто **непізнаним** | невпізнаним |

## Неверные немецкие заголовки

| id | стоит | надо |
|---|---|---|
| 16890 | der **Geschworener** | der Geschworene |

## Непараллельные примеры

Ещё около двадцати пяти на эту сотню. Среди заметных:

| id | слово | немецкий | перевод |
|---|---|---|---|
| 2949 | verlaufen | Die Prüfung ist gut verlaufen | uk: Концерт проходить у парку |
| 1876 | sorgen | Ich sorge mich um dich | uk: Хто піклується про твого собаку? |
| 7151 | hinzu | Komm hinzu, wir spielen Fußball | en: In addition, we need more time |
| 880 | stehen | Ich stehe hier | pl: Samochód stoi przed domem |
| 12262 | Rennbahn | Wir gehen nächsten Samstag zur Rennbahn | en: We watched the horses at the racetrack |
| 1976 | üben | Ich muss heute noch Klavier üben | uk: Я тренуюся тричі на тиждень |
| 17363 | Spazierfahrt | Spazierfahrt mit dem Boot | tr: Dün Boğaz'da gemi gezisi yaptık |

---

# Итог круга: 300 рядов

| класс | найдено |
|---|---|
| Примеры переводят другое предложение | ~80 |
| Опечатки, несуществующие слова, грамматика | 19 |
| Русизмы в украинской колонке | 12 |
| Неверный смысл | 13 |
| Неверные немецкие заголовки | 5 |
| Битые данные | 3 |

Рядов хотя бы с одним замечанием — **около трети**.
