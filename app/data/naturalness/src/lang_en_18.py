"""Вычитка английского, порция p018 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    10112: (T + 'книжно', {"example_en": "You're the one responsible"}),
    10150: (T + 'коряво', {"example_en": 'All he thinks about is revenge'}),
    10152: (T + 'без ситуации', {"example_en": 'After the party the whole flat is in a mess'}),
    10184: (T + 'калька', {"example_en": 'Can you feel that draught?'}),
    10190: (T + 'учебниково', {"example_en": 'Grandma prays every evening'}),
    10208: (T + 'калька', {"example_en": 'Cooking is my strong point'}),
    10215: (T + 'калька', {"example_en": 'Losing her dog really affected her'}),
    10218: (T + 'калька', {"example_en": "Behave yourself at Grandma's, OK?"}),
    10220: (T + 'учебниково', {"example_en": 'The little one was really well-behaved today'}),
    10241: (T + 'коряво', {"example_en": "The kids were very brave at the dentist's"}),
    10267: (T + 'нет слова карточки «soft spot»', {"example_en": "I've got a soft spot for chocolate"}),
    10285: (T + 'без ситуации', {"example_en": 'The police are still looking for a motive'}),
    10288: (T + 'повтор 10164 «awkward for me»', {"example_en": 'The sound of the drill is really unpleasant'}),
    10296: (T + 'повтор 10098 «against my will»', {"example_en": "With a bit of willpower you'll manage"}),
    10298: (T + 'калька', {"example_en": 'The new director has a clear vision for the company'}),
    10321: (T + 'неживо', {"example_en": 'You scared me!'}),
    10324: (T + 'калька', {"example_en": 'Tell me your troubles'}),
    10335: (T + 'повтор 10338', {"example_en": "There's a disgusting smell in the fridge"}),
    10338: (T + 'повтор 10295', {"example_en": 'Ew, this soup is gross!'}),
    10347: (T + 'коряво', {"example_en": 'Those guys are scum'}),
    10356: (T + 'коряво', {"example_en": 'You can lure the cat inside with a bit of ham'}),
    10371: (T + 'книжно', {"example_en": "Stand up for yourself, don't let them walk all over you"}),
    10372: (T + 'коряво', {"example_en": 'Thunderstorms really scare my dog'}),
    10373: (T + 'книжно', {"example_en": 'Her intelligence impresses all her teachers'}),
    10404: (T + 'учебниково', {"example_en": "Without discipline you won't get anywhere"}),
    10405: (T + 'калька', {"example_en": "Don't disturb him, he's really focused"}),
    10406: (T + 'книжно', {"example_en": 'She always has a positive attitude'}),
    10409: (T + 'повтор 10179 «jealous of her sister»', {"example_en": "He's a bit envious of my new car"}),
}

REPLACE = []

SPLIT_LATER = {}
