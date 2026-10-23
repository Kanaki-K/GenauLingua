"""Вычитка чешского, порция p028 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    7487: (T + "«svůj» — лишнее", {"example_cs": "Při vybalování po stěhování jsem v krabici znovu našel oblíbený svetr"}),
    7548: (T + "«se nesmí přeskočit» — грамматика", {"example_cs": "Snídani bys neměl jen tak přeskakovat, říká vždycky máma"}),
    7618: (T + "«tuto obtížnou» — книжно", {"example_cs": "S dostatkem cviku tuhle těžkou techniku zvládneš"}),
    7633: (T + "«svůj» — лишнее", {"example_cs": "V šedesáti si máma splnila sen a otevřela malou kavárnu"}),
    7788: (T + "«do mého auta» — калька", {"example_cs": "Při parkování mi soused narazil do auta a prostě odjel"}),
    8069: (T + "«Moje tetování … vyblednulo» — калька", {"example_cs": "Tetování mi po deseti letech už dost vybledlo"}),
    8070: (T + "«k ní patří» — смысл", {"example_cs": "V nové třídě má dcera konečně pocit, že tam patří"}),
    8072: (T + "«své» — лишнее", {"example_cs": "Ráno dokážu kudrny zkrotit jen se spoustou gelu"}),
    8156: (T + "«velmi» — книжно", {"example_cs": "Pohled do synovy lednice byl hodně výmluvný: jen kečup a energetické nápoje"}),
    8357: (T + "«záchod jí» — двусмысленно", {"example_cs": "Jediná odpovědná za kočku je dcera, ale kočičí záchod stejně uklízím já"}),
    8369: (T + "«plynule» — не то слово", {"example_cs": "Od té doby, co každý večer čteme spolu, se synovy známky z němčiny stále zlepšují"}),
    8395: (T + "«velmi náchylný na» — коряво", {"example_cs": "Táta je na komplimenty hodně náchylný, tak se dá přemluvit ke všemu"}),
    8410: (T + "«velmi» — книжно", {"example_cs": "V pubertě měla dcera hodně problematickou pleť a skoro se neodvážila ven"}),
    8456: (T + "«měnit» — не тот вид", {"example_cs": "Baterii v hlásiči kouře jsem musel vyměnit ve tři ráno, protože pořád pípal"}),
    8697: (T + "«tento» — книжно", {"example_cs": "Tiskárna opět stávkuje, už potřetí tenhle týden"}),
}

REPLACE = []

SPLIT_LATER = {}
