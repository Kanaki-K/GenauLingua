"""QA d09 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    13888: ('проверка выборок: слово W «послание/послання» не узнаётся в «сообщение»', {'example_ru': 'У меня для тебя послание', 'example_uk': 'У мене для тебе послання'}),
    13911: ('проверка выборок: «wichtiger Hinweis» — не подсказка в игре, а важное замечание', {'example_en': "Here's an important note for you"}),
    13914: ('проверка выборок: «The radio signal doesn\'t work» — не по-английски', {'example_en': "The radio isn't working"}),
    13962: ('проверка выборок: «bildiriyi» — канцелярит для новости', {'example_tr': 'Haberlerde o haberi gördün mü?'}),
    14298: ('проверка выборок: «це ще м\'яко кажучи» — неграмотно; нужно «м\'яко сказано»', {'example_uk': "Сказати, що моя сестра любить поговорити, — це ще м'яко сказано"}),
    14632: ('проверка выборок: «Every time my mum begs me» — читается как придаточное без главного', {'example_en': 'My mum begs me to put a hat on in winter every single time, as if I were still twelve'}),
    14767: ('проверка выборок: «izledikleri … izliyor» — повтор глагола', {'example_tr': 'Annemle babam her akşam sevdikleri Türk dizisinin bir bölümünü izliyor'}),
    14947: ('проверка выборок: «ist begraben» — состояние (похоронен), а не действие', {'example_tr': 'Köpek bahçede gömülü'}),
    15155: ('проверка выборок: «уже ли утро» — не по-русски; cs «mžouravě» — неживо', {'example_ru': 'После дневного сна сын выходит из комнаты, щурясь, и спрашивает, не утро ли уже', 'example_cs': 'Po odpoledním spánku vyjde syn z pokoje, mžourá a ptá se, jestli už je ráno'}),
    15261: ('проверка выборок: «для двух маленьких брата и сестры» — неграмотно', {'example_ru': 'Наши соседи уже два года — приёмная семья для маленьких брата и сестры', 'example_uk': "Наші сусіди вже два роки — прийомна сім'я для маленьких брата і сестри"}),
}

REPLACE = []

SPLIT_LATER = {}
