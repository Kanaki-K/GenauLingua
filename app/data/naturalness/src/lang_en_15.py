"""Вычитка английского, порция p015 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    6833: (T + 'повтор шаблона', {"example_en": "Let's go through the list one last time"}),
    6872: (T + 'без ситуации', {"example_en": 'Shall we put the tent up here?'}),
    6876: (T + 'коряво', {"example_en": "Don't look down!"}),
    6889: (T + 'калька', {"example_en": 'Tell me everything, every last detail'}),
    6890: (T + 'книжно', {"example_en": "The number is unknown, I'm not answering"}),
    6925: (T + 'коряво', {"example_en": "I've practically finished"}),
    6927: (T + 'неживо', {"example_en": 'I always carry a replacement battery'}),
    6931: (T + 'без ситуации', {"example_en": 'His boss transferred him to Leeds'}),
    6950: (T + 'повтор 6952 «set off tomorrow»', {"example_en": "We'll set out early tomorrow morning"}),
    6952: (T + 'повтор 6950', {"example_en": 'What time are we setting off?'}),
    6969: (T + 'коряво', {"example_en": 'I noticed twenty pounds were missing from my wallet'}),
    6970: (T + 'нет слова карточки «to apply»', {"example_en": 'The discount applies to children too'}),
    6994: (T + 'неживо', {"example_en": "I can't undo this knot"}),
    7032: (T + 'не то значение', {"example_en": 'Soldiers march through the city on Remembrance Day'}),
    7053: (T + 'калька', {"example_en": "Keep your phone handy, I'll call you"}),
    7061: (T + 'канцелярит', {"example_en": "It's 50 pounds, including delivery"}),
    7091: (T + 'калька', {"example_en": "Hang on, I'll just check my messages"}),
    7116: (T + 'повтор 6743 «keep your distance»', {"example_en": 'We covered a long distance by bike'}),
    7140: (T + 'калька', {"example_en": 'He shakes his head without saying a word'}),
    7190: (T + 'калька', {"example_en": 'Shall we carry on the conversation tomorrow?'}),
    7313: (T + 'нет слова карточки «worldwide»', {"example_en": 'Global warming is a worldwide problem'}),
    7315: (T + 'канцелярит', {"example_en": "In general I'm happy with my job"}),
    7611: (T + 'не то значение', {"example_en": 'Going downhill the bike rolls on its own'}),
    7715: (T + 'калька', {"example_en": 'On Sundays we all sit together at the table'}),
}

REPLACE = []

SPLIT_LATER = {}
