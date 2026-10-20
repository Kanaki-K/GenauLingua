"""A1, добор: строки, где списки остались длинными, и формы (неканонические). Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
FORM = "форма глагола/местоимения — перевод формой, а не инфинитивом и не пояснением"
GLOSS = "пояснение вместо перевода"

FIXES = {
    29: (LIST + "; «в формальном электронном письме» — канцелярски", {
        "t_ru": "обращение", "t_uk": "звертання", "t_en": "form of address", "t_tr": "hitap",
        "t_pl": "zwrot grzecznościowy", "t_it": "l'appellativo, la formula di saluto", "t_es": "el tratamiento, el saludo",
        "t_fr": "la formule d'appel", "x_ru": "В деловом письме важно правильное обращение"}),
    204: (GLOSS + " («неопределённый артикль»)", {
        "t_ru": "один, одна", "t_uk": "один, одна", "t_tr": "bir", "t_pl": "jeden", "t_it": "un, una", "t_es": "un, una"}),
    432: (LIST, {"t_ru": "информация", "t_uk": "інформація", "t_en": "information", "t_tr": "bilgi",
                 "t_pl": "informacja"}),
    734: (LIST, {"t_ru": "буклет, брошюра", "t_uk": "брошура, буклет", "t_en": "brochure, leaflet", "t_tr": "broşür",
                 "t_pl": "ulotka, broszura", "t_it": "il dépliant, il volantino", "t_fr": "la brochure, le dépliant",
                 "t_cs": "prospekt, leták"}),
    839: (LIST + "; «её, их» — другие падежи", {
        "t_ru": "она, они", "t_uk": "вона, вони", "t_en": "she, they", "t_tr": "o, onlar", "t_pl": "ona, oni",
        "t_it": "lei, loro", "t_es": "ella, ellos", "t_fr": "elle, ils", "t_cs": "ona, oni"}),
    1035: (LIST, {"t_ru": "как", "t_uk": "як", "t_en": "how, like", "t_tr": "nasıl", "t_pl": "jak", "t_it": "come",
                  "t_es": "cómo", "t_fr": "comment, comme", "t_cs": "jak"}),
    2079: (LIST + "; первым — то, что кричат: «Vorsicht!»", {
        "t_ru": "осторожно, осторожность", "t_uk": "обережно, обережність", "t_en": "caution, watch out",
        "t_tr": "dikkat", "t_pl": "uwaga, ostrożność", "t_it": "attenzione", "t_es": "cuidado", "t_fr": "attention",
        "t_cs": "pozor"}),
    2403: (LIST, {"t_ru": "заканчиваться, кончаться", "t_uk": "закінчуватися", "t_en": "to end",
                  "t_tr": "bitmek, sona ermek", "t_pl": "kończyć się"}),
    6174: (FORM + " (es gibt — «есть, имеется»)", {
        "t_ru": "есть, имеется", "t_uk": "є", "t_en": "there is, there are", "t_tr": "var", "t_pl": "jest",
        "t_it": "c'è", "t_es": "hay", "t_fr": "il y a", "t_cs": "je"}),
    6287: (LIST, {"t_ru": "забрать, сходить за", "t_uk": "принести, забрати"}),
    7695: (LIST, {"t_ru": "иностранный, зарубежный", "t_tr": "yabancı"}),
    8334: (LIST + "; «заполнить пропуски» — пояснение", {
        "t_ru": "дополнить, добавить", "t_uk": "доповнити, додати", "t_en": "to complete, to add",
        "t_tr": "tamamlamak, eklemek", "t_pl": "uzupełnić", "t_it": "completare", "t_es": "completar",
        "t_fr": "compléter", "t_cs": "doplnit"}),
    13269: (LIST, {"t_ru": "никакой, нет", "t_uk": "ніякий, немає", "t_en": "no, not any", "t_tr": "hiç",
                   "t_pl": "żaden", "t_it": "nessuno", "t_es": "ninguno", "t_fr": "aucun, pas de", "t_cs": "žádný"}),
    13274: (FORM + " (will — «хочу, хочет», не «хотеть»)", {
        "t_ru": "хочу, хочет", "t_uk": "хочу, хоче", "t_en": "want, wants", "t_tr": "istiyorum", "t_pl": "chcę, chce",
        "t_it": "voglio, vuole", "t_es": "quiero, quiere", "t_fr": "veux, veut", "t_cs": "chci, chce"}),
    13286: (FORM, {"t_ru": "одному", "t_uk": "одному"}),
    13287: (LIST, {"t_ru": "один, кто-то", "t_uk": "один, хтось", "t_en": "one, someone", "t_tr": "biri",
                   "t_pl": "jeden, ktoś", "t_it": "uno, qualcuno", "t_es": "uno, alguien", "t_fr": "un, quelqu'un",
                   "t_cs": "jeden, někdo"}),
    13290: (FORM + " (soll — «должен», не «надо»)", {"t_ru": "должен", "t_uk": "має, повинен"}),
    13292: ("порча знаний: в переводе три пояснения про падеж; в примере артикль переведён «этого»", {
        "t_ru": "der в родительном падеже", "t_uk": "der у родовому відмінку", "t_pl": "der w dopełniaczu",
        "x_ru": "Машина мужчины красная", "x_uk": "Машина чоловіка червона"}),
    13303: (LIST, {"t_ru": "к, в", "t_uk": "до", "t_en": "to the", "t_pl": "do, na", "t_cs": "do, k"}),
    17147: (LIST, {"t_ru": "автобан, автомагистраль", "t_uk": "автобан, автомагістраль", "t_en": "motorway",
                   "t_tr": "otoyol", "t_pl": "autostrada", "t_es": "la autopista"}),
    17342: (LIST, {"t_ru": "путеводитель, гид", "t_uk": "путівник, гід", "t_tr": "rehber", "t_pl": "przewodnik"}),
    17834: ("четыре значения → главные два (уровень — не A1, сверка уровней)", {
        "t_ru": "товар, имение", "t_uk": "товар, маєток", "t_en": "goods, estate", "t_tr": "mal",
        "t_pl": "towar, majątek", "t_it": "il bene, la merce", "t_es": "el bien, la mercancía",
        "t_fr": "le bien, la marchandise", "t_cs": "zboží, statek"}),
}
