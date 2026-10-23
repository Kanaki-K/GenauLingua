"""Вычитка испанского, порция p033 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    12947: (T + '«El niño está sanísimo» — учебниково', {"example_es": 'El médico dice que el peque está sanísimo'}),
    13519: (T + 'повтор 13552 «una hora y media»', {"example_es": 'La película dura una hora y media'}),
    13520: (T + '«Vamos hacia el sur» — учебниково', {"example_es": 'En otoño los pájaros vuelan hacia el sur'}),
    13682: (T + '«porque hace frío» — учебниково', {"example_es": 'Coge un jersey, por la noche refresca'}),
    13777: (T + 'повтор 13719 «pijama todo el domingo»', {"example_es": 'Puedes dejarte puesto el abrigo, aquí hace frío'}),
    14010: (T + 'повтор 13979 «¡No me mientas!»', {"example_es": 'Le miente a todo el mundo, hasta a su madre'}),
    14020: (T + 'повтор «ha sobrado tarta» (6383)', {"example_es": 'Puedes quedarte el dinero sobrante'}),
    14060: (T + 'повтор 14055 «avísame cuando llegue»', {"example_es": 'Hay que avisar a la familia del accidente'}),
    14078: (T + 'повтор 10161 «maldito ordenador»', {"example_es": 'Este maldito autobús vuelve a llegar tarde'}),
}

REPLACE = []

SPLIT_LATER = {}
