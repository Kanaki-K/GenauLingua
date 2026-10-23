"""Вычитка английского, порция p023 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    15152: (T + 'книжно', {"example_en": 'We should help our fellow human beings'}),
    15166: (T + 'коряво', {"example_en": 'My thighs ache after the run'}),
    15206: (T + 'коряво', {"example_en": 'I fell on my elbow'}),
    15209: (T + '«in Berlin» — без нужды', {"example_en": 'My half-brother lives in Cardiff'}),
    15263: (T + 'учебниково', {"example_en": "He grew up in a children's home"}),
    15314: (T + 'учебниково', {"example_en": 'The little one can already use the potty on his own'}),
    15388: (T + 'калька', {"example_en": 'The cat hunts mice in the attic'}),
    15402: (T + 'учебниково', {"example_en": "Come and sit in the shade, it's too hot"}),
    15411: (T + 'повтор 15574 «lying in the grass»', {"example_en": 'The grass is still wet this morning'}),
    15443: (T + 'повтор 15744 «lays an egg»', {"example_en": 'The neighbours keep five chickens in the garden'}),
    15444: (T + 'учебниково', {"example_en": "We're going to plant a tree for the baby's birth"}),
    15455: (T + 'повтор 10227 «The atmosphere here is…»', {"example_en": "There's a strange atmosphere in this house"}),
    15463: (T + 'неживо', {"example_en": 'My dream is to cross the ocean by boat'}),
    15465: (T + 'калька', {"example_en": "I can't stand the cold"}),
    15475: (T + 'книжно', {"example_en": 'The frost killed the flowers on the balcony'}),
    15482: (T + 'книжно', {"example_en": 'Darkness scares my little son'}),
    15609: (T + 'учебниково', {"example_en": 'The tractor is ploughing the field'}),
    15618: (T + 'повтор 15454 «feed the fish»', {"example_en": 'The dentist has a huge aquarium in the waiting room'}),
    15786: (T + 'книжно', {"example_en": 'We strolled along the riverbank'}),
    15859: (T + 'повтор «sings every morning» (15727)', {"example_en": 'Grandma has a canary called Tweety'}),
}

REPLACE = []

SPLIT_LATER = {}
