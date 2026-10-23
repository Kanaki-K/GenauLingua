"""Вычитка испанского, порция p045 (C1/C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    18939: (T + '«a la nevera» — норм; «Tras esto» — книжно', {"example_es": 'Después de esto, la masa reposa una hora en la nevera'}),
    8124: (T + '«mandamos medir» — коряво', {"example_es": 'Mañana vienen a medir el terreno'}),
    8359: (T + 'повтор 10364 «resistir al chocolate»', {"example_es": 'Al final sucumbió a la tentación'}),
    8393: (T + '«No es imprescindible» — оборвано', {"example_es": 'La asistencia no es imprescindible'}),
    8457: (T + '«Aclaremos» — книжно', {"example_es": 'Hay que aclarar el malentendido antes de que lleguen los invitados'}),
    8487: (T + '«¿Tienes que husmear?» — калька', {"example_es": '¡Deja de husmear en mis cosas!'}),
    8498: (T + '«para nuestra reunión» — книжно', {"example_es": '¿Fijamos una fecha?'}),
    8527: (T + '«en Múnich» — без нужды', {"example_es": '¿Una casa con jardín en Madrid con mi sueldo? Totalmente irreal'}),
    8572: (T + '«Tenemos que» — калька', {"example_es": 'Hay que modificar el plan para hacerlo más realista'}),
}

REPLACE = []

SPLIT_LATER = {}
