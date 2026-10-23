"""QA d13 (новые и изменённые строки из s329-s500), 23.10"""

FIXES = {
    19012: ('проверка выборок: «full of bustle» — неестественно', {'example_en': "On Saturday mornings there's always a lot of bustle in the supermarket"}),
    19020: ('проверка выборок: «perşembe gününü kararlaştırdık» — потерян «Termin»', {'example_tr': 'Elektrikçiyle perşembeye randevu kararlaştırdık'}),
    19024: ('проверка выборок: «хорошая и ровная» — «schön eben» = очень ровная', {'example_ru': 'Дорожка вдоль реки очень ровная — удобно для коляски'}),
    19042: ('проверка выборок: «стала вся смущённая» — не по-русски', {'example_ru': 'От комплимента дочь вся смутилась и покраснела', 'example_uk': 'Від компліменту донька вся зніяковіла й почервоніла'}),
}

REPLACE = []

SPLIT_LATER = {}
