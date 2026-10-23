"""Вычитка испанского, порция p026 (B1/B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка испанского: "

FIXES = {
    18244: (T + 'без ситуации', {"example_es": 'En el barrio van a construir un colegio nuevo'}),
    18317: (T + '«Siempre usamos … cuando llegamos» — громоздко', {"example_es": 'Cuando llegamos tarde entramos por la puerta trasera'}),
    18320: (T + '«una tetera de té» — тавтология', {"example_es": 'Cuidado, la tetera todavía está caliente'}),
    18349: (T + 'повтор «Decoramos» (18412)', {"example_es": 'Adornamos el árbol todos juntos'}),
    18412: (T + 'повтор 18349', {"example_es": 'He decorado la sala con globos'}),
    18935: (T + 'повтор «adornamos la casa» (18349)', {"example_es": 'En la época navideña las tiendas están a reventar'}),
    18378: (T + '«¿Dónde tiene su domicilio fijo?» — канцелярит', {"example_es": 'No tiene domicilio fijo'}),
    18429: (T + '«muy idílico» — книжно', {"example_es": 'El pueblecito de la costa era un sueño'}),
    18639: (T + '«corro detrás de ti» — не тот смысл', {"example_es": 'Siempre va corriendo detrás de su hermano mayor'}),
    18664: (T + 'нет слова карточки «la prisa» как сущ.', {"example_es": 'Con las prisas me he olvidado el móvil'}),
    18678: (T + '«tenemos que esperar» — калька', {"example_es": 'Esperamos a ver qué dice'}),
    18725: (T + '«deberían aprender de nosotros» — книжно', {"example_es": '¡Esta es mi futura oficina!'}),
    18744: (T + '«No queremos estar sentados» — калька', {"example_es": 'No me voy a pasar el día sin hacer nada'}),
    18751: (T + 'повтор 18823 «el tren va con retraso»', {"example_es": 'El vuelo retrasado por fin ha despegado'}),
    18878: (T + '«Deberíamos salir temprano» — калька', {"example_es": 'Hay que salir pronto'}),
    18910: (T + '«hizo mucho» — книжно', {"example_es": 'El inquilino anterior dejó los muebles'}),
    18949: (T + 'повтор 18948 «siempre … juntos»', {"example_es": 'El jueves por la noche no puedo, lo siento'}),
    19030: (T + '«Lo considero» — книжно', {"example_es": 'Me parece buena idea, ¡vamos a intentarlo!'}),
    19045: (T + '«a Hamburgo» — без нужды', {"example_es": 'El verano que viene nos mudamos a Valencia, mi marido ha encontrado trabajo allí'}),
    1272: (T + '«Tenemos que» — калька', {"example_es": 'Hay que mantener la cabeza fría'}),
    7092: (T + 'повтор 9899 «cortar la etiqueta»', {"example_es": 'Nos han cortado la luz'}),
}

REPLACE = []

SPLIT_LATER = {}
