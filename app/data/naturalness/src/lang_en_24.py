"""Вычитка английского, порция p024 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    15933: (T + 'учебниково', {"example_en": "There's been a murder in our neighbourhood"}),
    15938: (T + 'повтор «grandad was in the army» (8744)', {"example_en": 'My brother is doing his service in the army'}),
    15947: (T + 'без ситуации', {"example_en": "Since I passed my driving test, I've finally got my freedom"}),
    15951: (T + 'коряво', {"example_en": 'Have you got any proof?'}),
    15967: (T + 'калька', {"example_en": 'The police have freed the hostages'}),
    15973: (T + 'учебниково', {"example_en": 'He spent the night in a cell'}),
    15974: (T + 'книжно', {"example_en": 'He always stands up for his little sister'}),
    15985: (T + 'учебниково', {"example_en": 'Napoleon had himself crowned emperor'}),
    15993: (T + 'оборвано', {"example_en": "I'm at your disposal if you need anything"}),
    15995: (T + 'неживо', {"example_en": "The neighbours' dog attacked our cat"}),
    15996: (T + 'шаблон', {"example_en": 'I have a hunch, but no proof'}),
    16006: (T + '«in Munich» — без нужды', {"example_en": 'Her husband works as a public prosecutor in Leeds'}),
    16009: (T + 'тавтология', {"example_en": 'She has to testify in court next week'}),
    16013: (T + 'коряво', {"example_en": 'After the flood the army is helping residents'}),
    16028: (T + 'учебниково', {"example_en": 'In the fairy tale the whole kingdom is in danger'}),
    16086: (T + 'коряво', {"example_en": 'The hotel gave us royal treatment'}),
    16089: (T + '«in Berlin» — без нужды', {"example_en": 'The congress takes place next week in London'}),
    16099: (T + 'калька', {"example_en": "I don't post photos of the kids — it's their privacy"}),
    16101: (T + 'повтор «guard»', {"example_en": 'Can you watch over my things while I swim?'}),
    16103: (T + 'книжно', {"example_en": "The witness's hearing is tomorrow"}),
    16104: (T + 'повтор 16146 «police arrested»', {"example_en": 'He was detained outside the shop'}),
    16106: (T + 'книжно', {"example_en": "Everything's settled for the trip"}),
    16133: (T + 'повтор 16152 «the king … years»', {"example_en": "Who's governing the country now?"}),
    16134: (T + 'повтор 16128 «in prison»', {"example_en": 'The bank robbery took ten minutes'}),
    16140: (T + 'коряво', {"example_en": "The letter bears the king's seal"}),
    16281: (T + 'книжно', {"example_en": 'Shall we vote on where to go?'}),
    16343: (T + 'книжно', {"example_en": 'The judge was very strict with him'}),
    16355: (T + 'повтор 16717 «police car outside the house»', {"example_en": 'The patrol car is driving with its siren on'}),
    16702: (T + 'повтор 15976 «visiting our school»', {"example_en": 'The health minister is speaking on TV tonight'}),
    17057: (T + 'повтор 17081', {"example_en": 'Welcome on board!'}),
    17081: (T + 'повтор 17057', {"example_en": "It's windy on deck, put a jacket on"}),
    17099: (T + 'повтор «Whose … is that?» (13462)', {"example_en": "Vehicles over 3.5 tonnes can't use this road"}),
    17105: (T + '«to Berlin» — без нужды', {"example_en": 'The plane to Edinburgh takes off at eight'}),
}

REPLACE = []

SPLIT_LATER = {}
