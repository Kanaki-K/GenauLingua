"""Полная вычитка, порция 35: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    15523: (T + "учебниковое «на ферме много гусей, плавают в воде» — живой пример во всех 10", {"example_de": "Auf dem Bauernhof laufen die Gänse den Kindern hinterher und schnattern laut", "example_ru": "На ферме гуси бегают за детьми и громко гогочут", "example_uk": "На фермі гуси бігають за дітьми й голосно ґелґочуть", "example_en": "On the farm the geese run after the children, honking loudly", "example_tr": "Çiftlikte kazlar çocukların peşinden koşup yüksek sesle bağırıyor", "example_pl": "W gospodarstwie gęsi biegają za dziećmi i głośno gęgają", "example_it": "Alla fattoria le oche corrono dietro ai bambini starnazzando", "example_es": "En la granja los gansos corren detrás de los niños graznando", "example_fr": "À la ferme, les oies courent après les enfants en criant", "example_cs": "Na statku husy běhají za dětmi a hlasitě kejhají"}),
    15819: (T + "fr «pagayer en amont» — неестественно", {"example_fr": "Remonter la rivière en canoë a été beaucoup plus dur que ce qu'on pensait"}),
    16150: (T + "смысл разошёлся (de/tr/pl/cs «перегар») — везде «болельщики машут флагами»", {"example_de": "Im Stadion schwenken die Fans ihre Fahnen", "example_ru": "На стадионе болельщики размахивают флагами", "example_uk": "На стадіоні вболівальники розмахують прапорами", "example_en": "The fans are waving flags in the stadium", "example_tr": "Taraftarlar stadyumda bayrak sallıyor", "example_pl": "Kibice na stadionie machają flagami", "example_it": "I tifosi sventolano le bandiere allo stadio", "example_es": "Los aficionados agitan banderas en el estadio", "example_fr": "Les supporters agitent des drapeaux dans le stade", "example_cs": "Fanoušci na stadionu mávají vlajkami"}),
    16160: (T + "es «se han puesto en emboscada» — неестественно", {"example_es": "Los niños se han escondido detrás del seto para tenderle una emboscada a su padre con pistolas de agua"}),
    16213: (T + "es «condenado de por vida», it «condannato a vita» — говорят «пожизненное»", {"example_it": "L'assassino del paese è stato condannato all'ergastolo", "example_es": "El asesino del pueblo ha sido condenado a cadena perpetua"}),
    16229: (T + "ru/uk «доверители», pl «mocodawcy» — канцелярит", {"example_ru": "Адвокат не имеет права ни с кем говорить о своих клиентах, даже с мужем", "example_uk": "Адвокатка не має права ні з ким говорити про своїх клієнтів, навіть із чоловіком", "example_pl": "Adwokatka nie może z nikim rozmawiać o swoich klientach, nawet z mężem"}),
    16236: (T + "ru/uk/fr «скрыть разбитую вазу» — неуклюже", {"example_ru": "Сын пытался скрыть, что разбил вазу, но осколки ещё лежали под диваном", "example_uk": "Син намагався приховати, що розбив вазу, але уламки ще лежали під диваном", "example_fr": "Mon fils a essayé de cacher qu'il avait cassé le vase, mais les morceaux étaient encore sous le canapé"}),
    16262: (T + "en «For the destruction… a company comes» — неестественно", {"example_en": "A company with a big shredder is coming to destroy the old files"}),
    16263: (T + "ru «засвидетельствовать» — книжно", {"example_ru": "Я могу это подтвердить, я был там"}),
}

REPLACE = []
SPLIT_LATER = {}
