"""
Localización española para GenauLingua Bot

Набор ключей совпадает с остальными локалями — это проверяется тестом
test_all_locales_have_identical_key_sets. Обращение — только на «usted».
"""

TEXTS = {
    # ============================================================================
    # MENÚ PRINCIPAL
    # ============================================================================
    "btn_learn_words": "Aprender palabras",
    "btn_stats": "Estadísticas",
    "btn_settings": "Ajustes",
    "btn_help": "Ayuda",
    "btn_back": "Atrás",
    "menu_placeholder": "Elija una acción…",

    # ============================================================================
    # BIENVENIDA E INICIO
    # ============================================================================
    "welcome_title": "<b>¡Hola, {name}!</b>",








    # ============================================================================
    # RECORDATORIOS
    # ============================================================================
    "notif_title": "<b>Recordatorios</b>",
    "notif_status": "Estado: {status}",
    "notif_status_on": "activados",
    "notif_status_off": "desactivados",
    "notif_time": "Hora: {time}",
    "notif_days": "Días: {days}",
    "notif_timezone": "Zona horaria: {timezone}",
    "notif_hint": "El recordatorio llega a la hora elegida en su zona horaria.",
    "notif_hint_off": "Active los recordatorios — así es más fácil mantener la racha.",

    "notif_btn_toggle_on": "Recordatorios: activados",
    "notif_btn_toggle_off": "Recordatorios: desactivados",
    "notif_btn_time": "Hora: {time}",
    "notif_btn_days": "Elegir días",
    "notif_btn_timezone": "Cambiar zona horaria",

    "notif_timezone_title": "<b>Su zona horaria</b>",
    "notif_timezone_current": "Actual: {timezone}",
    "notif_timezone_prompt": "Elija una ciudad de su zona horaria:",
    "notif_timezone_more": "Otra ciudad",
    "notif_timezone_back": "Atrás",
    "notif_timezone_set": "✓ Zona horaria fijada: {city}",

    "notif_time_title": "<b>Hora del recordatorio</b>",
    "notif_time_current": "Hora actual: {time}",
    "notif_time_timezone": "Zona horaria: {timezone}",
    "notif_time_hint": "El recordatorio llega a esta hora los días que haya elegido.",
    "notif_time_set": "✓ Hora fijada: {time}",

    "notif_days_title": "<b>Días de recordatorio</b>",
    "notif_days_hint": "Pulse un día para activarlo o desactivarlo.\n✓ — día activado\n✗ — día desactivado\n\nCuando termine, pulse “Guardar”.",
    "notif_days_all": "Todos los días",
    "notif_days_weekdays": "Días laborables (lun–vie)",
    "notif_days_save": "Guardar",
    "notif_days_saved": "✓ ¡Días guardados!",
    "notif_days_all_selected": "✓ Todos los días seleccionados",
    "notif_days_weekdays_selected": "✓ Días laborables seleccionados (lun–vie)",
    "notif_days_none": "Elija al menos un día.",

    "notif_toggle_on": "Recordatorios activados",
    "notif_toggle_off": "Recordatorios desactivados",

    "day_mon": "Lun",
    "day_tue": "Mar",
    "day_wed": "Mié",
    "day_thu": "Jue",
    "day_fri": "Vie",
    "day_sat": "Sáb",
    "day_sun": "Dom",

    "notif_btn_back": "Volver a ajustes",

    "notif_default_name": "amigo",



    # UN MOTIVO PARA VOLVER — y tiene que ser verdadero

    # ============================================================================
    # AJUSTES
    # ============================================================================
    "settings_title": "<b>Ajustes</b>",
    "settings_mode": "Modo: <b>{mode}</b>",
    "settings_language": "Idioma del bot: <b>{language}</b>",

    "settings_btn_quiz_mode": "Nivel y temas",
    "settings_btn_change_language": "Idioma del bot",
    "settings_btn_notifications": "Recordatorios",

    "settings_quiz_mode_line": "Nivel: <b>{mode}</b>",
    "start_pick_language": "Elija su idioma",
    "onboard_your_lang": "✓ Su idioma: {language}",
    "onboard_change_hint": "Puede cambiarlo en cualquier momento: comando /language.",
    "onboard_phone_hint": "Su Telegram está en español. Si eligió el idioma por error, pulse «{back}».",
    "lang_confirm_learning": "Idioma de estudio: {language}",
    "lang_progress_kept": "El progreso de cada idioma se conserva.",
    "btn_done": "Listo",
    "btn_change_learning": "Cambiar el idioma que aprendo",
    "intro_pair": "Usted aprende {learning} con traducción al {native}.",
    "intro_menu_language": "idioma del bot",
    "plural_languages": "idioma|idiomas",
    "cmd_start": "Inicio y qué hace el bot",
    "cmd_language": "Idioma del bot",
    "cmd_settings": "Ajustes",
    "cmd_help": "Ayuda",

    "language_changed": "✓ Idioma cambiado a {language}",
    "user_not_found": "✗ Perfil no encontrado. Envíe /start, por favor",

    "lang_ru": "Русский",
    "lang_uk": "Українська",
    "lang_en": "English",
    "lang_tr": "Türkçe",
    "lang_de": "Deutsch",
    "lang_pl": "Polski",
    "lang_it": "Italiano",
    "lang_es": "Español",
    "lang_fr": "Français",
    "lang_cs": "Čeština",



    # ============================================================================
    # MODO DE ESTUDIO
    # ============================================================================
    "qmode_title": "<b>Nivel y temas</b>",
    "qmode_current": "Actual: <b>{mode}</b>",
    "qmode_choose": "Elija cómo quiere aprender.\nPuede cambiarlo en cualquier momento — su progreso se conserva.",

    "qmode_btn_level": "Por nivel",
    "qmode_btn_category": "Por tema",
    "qmode_btn_all": "Todas las palabras",
    "qmode_btn_difficult": "Palabras difíciles",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Todas las palabras",
    "qmode_difficult_short": "Palabras difíciles",

    "qmode_level_title": "<b>Elija un nivel</b>",
    "qmode_level_desc": "De las primeras palabras a la conversación fluida. Todos los niveles están abiertos — elija el suyo.\n\n• A1–A2 — vocabulario básico\n• B1–B2 — comunicación con soltura\n• C1–C2 — dominio y matices",
    "qmode_level_set": "✓ Modo: por nivel ({level})",

    "qmode_category_title": "<b>Elija un tema</b>",
    "qmode_category_desc": "De la comida a la ciencia — elija el tema que necesita.\n\nCada tema incluye palabras de todos los niveles.",
    "qmode_category_set": "✓ Tema: {category}",

    # Nombres de las categorías
    "cat_arbeit_beruf": "Trabajo",
    "cat_bildung_lernen": "Educación",
    "cat_einkaufen_geld": "Compras",
    "cat_emotionen_charakter": "Emociones",
    "cat_essen_trinken": "Comida",
    "cat_freizeit_sport": "Deporte",
    "cat_gesundheit_medizin": "Salud",
    "cat_grammatik": "Gramática",
    "cat_kleidung_mode": "Ropa",
    "cat_kommunikation": "Comunicación",
    "cat_kultur_kunst": "Cultura",
    "cat_mensch_familie": "Familia",
    "cat_natur_wetter": "Naturaleza",
    "cat_recht_staat": "Derecho",
    "cat_reisen_transport": "Viajes",
    "cat_technik_digital": "Tecnología",
    "cat_wirtschaft": "Economía",
    "cat_wissenschaft": "Ciencia",
    "cat_wohnen_haus": "Vivienda",
    "cat_zeit_alltag": "Vida diaria",

    "qmode_all_set": "✓ Modo: todas las palabras",

    "qmode_difficult_set": "✓ Modo: palabras difíciles",
    "qmode_difficult_few": "Palabras difíciles por ahora: {count} — se necesitan al menos 4.\n¡Haga unas lecciones más!",
    "qmode_difficult_empty": "Todavía no hay palabras difíciles.\n¡Haga primero algunas lecciones!",

    "quiz_btn_change_mode": "Nivel y temas",
    "quiz_btn_report_error": "Informar de un error",
    "report_btn_confirm": "✓ Confirmar ({count})",
    "report_btn_send": "Enviar",
    "report_kind_text": "Traducción",
    "report_kind_example": "Ejemplo",
    "report_kind_audio": "Audio",
    "report_pick_hint": "¿Qué está mal? Márquelo y pulse «Enviar»",
    "report_btn_sent": "✓ Aviso enviado",
    "report_sent_one": "✓ ¡Gracias!\nSi el error se confirma, recibirá +{points}.",
    "report_approved_example": "✓ Su aviso sobre el ejemplo de <b>{word}</b> ha sido aceptado\n\nCorregiremos el ejemplo\n\n+{points} puntos a su marcador del mes - gracias",
    "report_no_words": "No hay palabras de las que avisar",
    "report_none_selected": "Seleccione al menos una palabra",
    "report_pick_kind": "Palabras seleccionadas: {count}. Ahora indique qué está mal: la traducción o la pronunciación.",
    "report_sent": "✓ Avisos enviados: {count} — ¡gracias!\nCada aviso confirmado le da +{points}.",
    "report_daily_limit": "Ha alcanzado el límite de hoy: 20 avisos.",
    "report_all_reported": "✓ Ya se ha avisado de todas las palabras de esta lección",
    "report_already_sent": "✓ Ya enviado",
    "report_btn_kind_text": "Traducción incorrecta",
    "report_btn_kind_audio": "Pronunciación incorrecta",
    "report_sent_audio": "✓ Avisos enviados: {count} — ¡gracias!\nLos avisos de pronunciación son especialmente valiosos: la revisión automática no oye el acento tónico.\nCada aviso confirmado le da +{points}.",
    "report_approved": "✓ Su aviso sobre <b>{word}</b> ha sido aceptado - corregiremos la traducción\n\n+{points} puntos a su marcador del mes. Gracias - el diccionario mejora para todos",
    "award_won": "{mark} Ha quedado en el puesto {rank} de la clasificación de {month}\n\nSe han sumado {bonus} puntos a su marcador total",
    "report_approved_audio": "✓ Su aviso de pronunciación sobre <b>{word}</b> ha sido aceptado\n\nEl audio se corregirá\n\n+{points} puntos a su marcador del mes - gracias",
    # ============================================================================
    # LECCIÓN
    # ============================================================================
    "quiz_no_level": "Primero elija su nivel: /start",
    "quiz_error_generation": "✗ Algo falló al preparar la lección.\nInténtelo de nuevo con /start",
    "quiz_no_words": "✗ Lo sentimos, no hay palabras para este nivel.\nPruebe con otro nivel.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Correcto</b>",
    "quiz_wrong": "✗ <b>Incorrecto</b>",
    "quiz_correct_answer": "Respuesta correcta:",

    "quiz_btn_next": "Siguiente →",

    "quiz_answer_already_counted": "Su respuesta ya se ha contado. ¿Seguimos?",
    "quiz_btn_repeat_errors": "Repasar errores",
    "lesson_resume_prompt": 'Tiene una lección sin terminar: {done} de {total}',
    "btn_lesson_resume": 'Continuar',
    "btn_lesson_new": 'Empezar una nueva',
    "speech_offer_text": '¿Ahora no le viene bien hablar en voz alta? No pasa nada. ¿Quitar «Hablo» de las lecciones? Puede recuperarlo cuando quiera en los ajustes',
    "btn_speech_off": 'Quitar «Hablo»',
    "btn_speech_keep": 'Mantener',
    "speech_off_done": 'Hecho, «Hablo» se ha quitado. Puede recuperarlo en los ajustes',
    "speech_invite_text": '🎤 ¿Quiere probar a responder en voz alta? El bot escuchará su pronunciación y le avisará si algo no va bien. Es opcional',
    "btn_speech_try": 'Probar',
    "btn_speech_later": 'Ahora no',
    "speech_try_done": '¡Estupendo! «Hablo» aparecerá en sus próximas lecciones. Para responder, mantenga pulsado el icono del micrófono abajo a la derecha y diga la palabra',

    "quiz_completed": "<b>Lección terminada</b>",
    "quiz_result_correct": "Correctas: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Resultado: <b>{percentage}%</b>",
    "quiz_result_details": "<b>Detalles:</b>",
    "quiz_result_errors": "Errores: {count}",

    # ELOGIO AL FINAL DE LA LECCIÓN — solo por lo que de verdad ocurrió
    "praise_first_round": "Primera lección terminada. A partir de aquí las palabras empiezan a volver — así es como se quedan.",
    "praise_first_learned": "Primera palabra aprendida: tres respuestas correctas seguidas, ninguna el día en que la conoció.",
    "praise_learned": "Palabras aprendidas en esta lección: {count}",
    "praise_best_streak": "Récord personal: {days_word} seguidos",
    "praise_milestone": "Ya está aprendiendo {count} palabras",
    "praise_first_speech": "Primera respuesta correcta en voz alta",
    "praise_first_audio": "Primera respuesta correcta de oído",
    "praise_comeback": "¡Qué bien verle de nuevo! Han pasado {days_word}.",
    "praise_perfect": "Una lección sin un solo error",
    "praise_streak": "Racha: {days_word} seguidos",
    "praise_freeze_saved": "Ayer no hubo lección, pero la protección de racha la ha salvado: {days_word} seguidos. La próxima protección estará disponible dentro de una semana.",
    "praise_streak_3": "Tres días seguidos — el hábito empieza a formarse.",
    "praise_streak_7": "¡Una semana entera seguida! Es el hito clave: a partir de aquí el hábito se sostiene solo.",
    "praise_streak_14": "Dos semanas seguidas — muy buen ritmo.",
    "praise_streak_30": "¡Un mes seguido! Ya es un hábito de verdad.",
    "praise_new_words": "Palabras nuevas: {count}",
    "praise_returned": "Reconocidas de nuevo: {count}",
    "praise_progress": "Palabras en estudio: {count} · {left} más hasta {target}",
    "praise_progress_top": "Palabras en estudio: {count}",
    "praise_points": "Puntos: +{points}",

    "quiz_repeat_title": "<b>Repasar errores</b>",
    "quiz_no_errors": "✓ ¡Esta vez sin errores!",
    "quiz_error_next": "✗ No se pudo cargar la siguiente pregunta.",

    # ============================================================================
    # ESTADÍSTICAS
    # ============================================================================
    "stats_no_level": "<b>¡Primero elija su nivel!</b>\n\nUse /start para empezar.",





    # ============================================================================
    # AYUDA
    # ============================================================================
    "help_title": "<b>Ayuda — GenauLingua</b>",
    "help_description": "Cómo funcionan las lecciones y cómo contactar con la comunidad.",
    "help_choose": "Elija una sección:",

    "help_btn_how_to_use": "Cómo usarlo",
    "help_btn_community": "Comunidad",

    "help_how_to_use_title": "<b>Cómo usar el bot</b>",


    "help_community_title": "<b>Comunidad GenauLingua</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

En el chat:
Entérese antes que nadie de las novedades
¿Ha encontrado un fallo? Escríbanos o envíe una captura
¿Error de traducción? Avísenos y lo corregiremos
Ideas y sugerencias — lo leemos todo
Charle con otros estudiantes


Cuanto más activa la comunidad, mejor el bot. ¡Anímese a escribir! """,


    # ============================================================================
    # CLASIFICACIÓN
    # ============================================================================
    "rating_not_active": "✗ La clasificación aún no está activa.",
    "rating_not_in_ranking": "Todavía no está en la clasificación",
    "rating_start_quiz": "¡Haga su primera lección!",
    "rating_join_by_lesson": "Sus puntos por avisos ({score}) ya están sumados. Complete una lección para entrar en la clasificación de este mes.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — hemos rehecho el bot desde cero</b>\n\n<b>No solo alemán.</b> Aprenda ucraniano, inglés, turco, alemán, polaco o ruso — desde cualquiera de ellos. La interfaz también habla los seis.\n\n<b>Seis juegos en lugar de uno.</b> Antes solo había “elija la traducción”.\n\nAhora los juegos se alternan en cada lección:\n📖 Leo · 💭 Recuerdo · 🎧 Escucho · 🎤 Hablo · 🧩 Encuentre las parejas · 🧱 Construyo\n\nEn “Hablo” responde con la voz; en “Construyo” arma una frase — el bot le muestra qué palabra está fuera de sitio.\n\n<b>El bot habla.</b> Cada palabra y cada ejemplo se leen en voz alta con una voz natural.\n\n<b>Un aspecto nuevo.</b> Menú nuevo, un chat limpio y sin desorden, una pantalla de inicio con sus habilidades, estadísticas claras, nuevo avatar y nuevo saludo.\n\n<b>Todo el diccionario revisado</b> — las 12 902 palabras, traducciones y ejemplos.\n\n<b>Se adapta a usted:</b> las palabras vuelven justo antes de que las olvide, y el bot le propone el siguiente nivel cuando todo resulta fácil.\n\n<b>Errores corregidos:</b> la racha de días se cuenta bien y los puntos de la clasificación son justos — premian el esfuerzo. “Aprendida” también es honesto ahora: una palabra cuenta como aprendida cuando la acierta tres veces seguidas en días distintos, y cada palabra que ha practicado aparece en “Palabras en estudio”.\n\n<b>Los recordatorios están activados</b> — a su hora. Para cambiarlos o desactivarlos: Ajustes → Bot → Recordatorios.\n\n⭐ ¿Ha visto un error? Avise desde el resumen de la lección: cada aviso confirmado da +15 puntos.\n\nSu progreso y sus puntos se conservan. Pruébelo — una lección dura un par de minutos.",
    "release_notes_2026_10_22": '✨ <b>GenauLingua 2.2 - ahora diez idiomas</b>\n\n¡Hola!\n\nYa está aquí una gran actualización:\n\n<b>4 idiomas nuevos</b>\n\n🇮🇹 Italiano, 🇪🇸 español, 🇫🇷 francés y 🇨🇿 checo - puede aprenderlos desde cualquier idioma del bot\nCada uno tiene más de 12 000 palabras con ejemplos, todo con audio\n\n<b>Una clasificación por la que merece la pena competir</b>\n\nMedallas del mes 🥇🥈🥉, una corona 👑 para el primer puesto entre quienes aprenden su idioma y rangos que crecen con usted. Los primeros resultados con las nuevas reglas - el 1 de noviembre\n\n<b>La racha perdona un día sin practicar</b>\n\nUna vez por semana, la protección de racha 🧊 salva su racha si se salta un día\n\n<b>Además:</b> avise de un error en la traducción, el ejemplo o el audio - justo debajo de la respuesta (+15 puntos por cada aviso confirmado)\n\nLas palabras conocidas se aprenden más rápido, y las actualizaciones del bot ya no interrumpen la lección\n\nGracias por aprender con nosotros y avisar de los errores - así el bot mejora para todos 💙\n\nTodas las novedades, de forma breve y clara: <a href="{url}">novedades de la 2.2</a>',
    "btn_release_news": 'Novedades →',


    "table_empty": "Todavía no hay participantes.\n¡Sea el primero en hacer una lección!",
    "table_you_not_ranked": "Todavía no está en la clasificación",
    "rating_tab_month": "Mes",
    "rating_tab_alltime": "Total",
    "rating_crown_rule": "El primer puesto recibe la corona durante todo el mes siguiente",
    "rating_screen_title": "<b>Clasificación · {month} {year}</b>",
    "rating_screen_title_alltime": "<b>Clasificación · histórica</b>",
    "rating_you": "<b>Usted: #{rank} de {total}</b> · {points}",
    "rating_results_in": "Resultados del mes en {days}",
    "info_title": "<b>Cómo funciona la clasificación</b>",
    "info_month": "<b>Mes</b> — todos. Los tres mejores reciben 🥇 🥈 🥉 (a partir de 3 lecciones).",
    "info_lang": "<b>Idioma</b> — quienes aprenden su idioma. El primero recibe 👑 para el mes siguiente.",
    "info_alltime": "<b>Total</b> — todos los puntos. Las medallas suben su rango 🌱 🌳 🌙 🪐 ☀️",
    "info_points_title": "<b>Puntos</b>",
    "info_points": "Respuesta +1 · de oído +2 · en voz alta +3\nLección +10 · palabra aprendida +3\nDías seguidos — hasta +10 · precisión superior al 60 % — bonificación\nAviso confirmado +{points}",
    "title_sprout": "Brote",
    "title_tree": "Árbol",
    "title_moon": "Luna",
    "title_planet": "Planeta",
    "title_sun": "Sol",
    "title_galaxy": "Galaxia",
    "btn_rating_info": "Info",
    "card_medal_need": "Lecciones necesarias para una medalla: {need} · usted tiene {have}",
    "card_crown_small": "La corona se disputa cuando el idioma tiene 3+ personas con 3+ lecciones",
    "summary_place": "↑ Puesto del mes: {rank}",
    "summary_gap": "a {gap} de {name}",
    "summary_record": "Nuevo récord del mes: {points}",
    "collection_title": "<b>Colección</b> · {open} de {total} desbloqueados",
    "collection_locked": "▫️ ???",
    "ach_streak_7": "Racha de 7 días",
    "ach_streak_30": "Racha de 30 días",
    "ach_streak_100": "Racha de 100 días",
    "ach_streak_365": "Racha de 365 días",
    "ach_streak_1000": "Racha de 1000 días",
    "ach_words_100": "100 palabras aprendidas",
    "ach_words_1000": "1000 palabras aprendidas",
    "ach_words_3000": "3000 palabras aprendidas",
    "ach_perfect_10": "10 lecciones sin errores",
    "ach_voice_1000": "1000 respuestas correctas en voz alta",
    "ach_editor": "Editor del diccionario: 5 avisos aceptados",
    "ach_polyglot": "Políglota: 100 palabras en dos idiomas",
    "award_month_header": "<b>Resultados del mes</b>",
    "award_crown": "👑 Corona — {language}: primer puesto. Llévela todo el mes siguiente",
    "award_glory": "+{glory} de gloria",
    "award_new_title": "Nuevo rango: {mark} {name}",
    "nd_overtaken": "Le han adelantado en la clasificación del mes.\nSu puesto: {rank} · a {gap} de {name}.",
    "nd_finish": "Hasta fin de mes: {days}.\nSu puesto: {rank} · le faltan {gap} para una medalla.",

    "stats_header": "<b>Sus estadísticas</b>",
    "stats_in_work_line": "Palabras en estudio: {count} · {left} más hasta {target}",
    "stats_in_work_top": "Palabras en estudio: {count}",
    "stats_details": "En estudio: {progress}\nNuevas: {new}\nDifíciles: {difficult}",
    "stats_achievements_title": "<b>Sus logros</b>",
    "stats_words_count": "Palabras aprendidas: <b>{count}</b>",
    "stats_best_streak_line": "Mejor racha: {days_word}",
    "stats_quizzes_header": "<b>Lecciones · {level}</b>",
    "stats_quizzes_passed_line": "Terminadas: <b>{count}</b>",
    "stats_quizzes_avg_line": "Resultado medio: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Mejor resultado: <b>{percent}%</b>",
    "stats_quizzes_empty": "Todavía no ha terminado ninguna lección",
    "stats_recent_header": "<b>Últimas lecciones</b>",
    "stats_explanation": "Una palabra cuenta como aprendida tras tres respuestas correctas seguidas, en días distintos.",
}

# ============================================================================
# MULTILINGÜE: idioma de estudio, idioma de los significados y dirección
# ============================================================================
TEXTS.update({
    "langname_de": "Alemán",
    "langname_en": "Inglés",
    "langname_ru": "Ruso",
    "langname_uk": "Ucraniano",
    "langname_tr": "Turco",
    "langname_pl": "Polaco",
    "langname_it": "Italiano",
    "langname_es": "Español",
    "langname_fr": "Francés",
    "langname_cs": "Checo",
    # Союз для перечисления языков в текстах помощи и приветствия
    "and_word": "y",

    "settings_learning_lang_line": "Aprendo: <b>{language}</b>",

    "settings_btn_learning_lang": "Idioma",

    "learning_lang_title": "<b>Idioma que aprender</b>",
    "learning_lang_description": "Elija el idioma cuyas palabras quiere aprender.\nEl progreso se cuenta por separado para cada idioma.",
    "learning_lang_set": "✓ Aprendo: {language}",
    # Línea de ajustes y pantalla de audio
    "settings_audio_line": "Audio: <b>{state}</b>",
    "settings_btn_audio": "Audio",
    "audio_state_on": "activado",
    "audio_state_off": "desactivado",

    "audio_title": "<b>Audio</b>",
    "audio_description": "Una voz de IA con sonido natural lee las palabras en voz alta. En la pregunta suena solo la palabra; en la respuesta, la palabra con el ejemplo.",
    "audio_current_voice": "Voz: <b>{voice}</b>",
    "audio_btn_turn_on": "Activar el audio",
    "audio_btn_turn_off": "Desactivar el audio",
    "audio_btn_choose_voice": "Elegir una voz",
    "audio_turned_on": "✓ Audio activado",
    "audio_turned_off": "Audio desactivado",

    "voice_title": "<b>Elija una voz</b>",
    "voice_description": "Pulse una voz para escucharla. La marca indica la actual.",
    "voice_male": "Masculina",
    "voice_female": "Femenina",
    "voice_set": "✓ Voz: {voice}",
    "voice_use": "Usar {voice}",
    "voice_listening": "Reproduciendo {voice}",
    "voice_only_one": "Para este idioma solo hay una voz masculina y una femenina.",
    "voice_preview_failed": "No se pudo cargar la muestra. Inténtelo de nuevo.",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Clasificación",
    "friend_fallback": "amigo",
    "onboarding_learning_title": "<b>¿Qué idioma va a aprender?</b>",
})


# ============================================================================
# ПОМОЩЬ ПОСЛЕ СОКРАЩЕНИЯ: было четыре экрана, стало два
#
# Убран экран «Скоро в боте» — он обещал Goethe/ÖSD и тексты на немецком,
# то есть врал всем, кто учит не немецкий. «О боте» слит с «Сообществом».
# Инструкция сокращена: из неё выброшено всё, что человек и так видит на
# экране, и оставлено то, чего из интерфейса не видно.
# ============================================================================
TEXTS.update({
    "help_how_to_use_text": "<b>Lección</b>\n{words}, cuatro opciones en cada una. Una lección mezcla seis juegos: “Leo”, “Recuerdo”, “Escucho”, “Hablo”, “Construyo” y el tablero “Encuentre las parejas”. El bot recuerda sus errores y repite más a menudo las palabras difíciles. Después de la lección puede repasar las que falló.\n\n<b>Audio</b>\nEn la pregunta suena la palabra; tras su respuesta oye la palabra con su ejemplo. Elija voz masculina o femenina en los ajustes.\n\n<b>Idiomas</b>\n{languages} — en cualquier combinación. El progreso se cuenta por separado para cada idioma; la clasificación tiene las pestañas «Mes», «Total» e «Idioma».\n\n\nUna palabra cuenta como <b>aprendida</b> tras tres respuestas correctas seguidas, en días distintos. Si acierta una palabra nueva a la primera, basta con una respuesta correcta más.\nSu <b>racha</b> crece cada día en que hace al menos una lección. Un día perdido a la semana no la rompe — la protección de racha lo cubre.\n¿Traducción o pronunciación incorrecta? Use el botón “Informar de un error” bajo la respuesta.",
    "help_community_title": "<b>Sobre el bot y la comunidad</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} idiomas en cualquier combinación: {languages}\n12 900 palabras A1–C2, cada una con un ejemplo y audio de sonido natural.\nInterfaz: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nFallos, errores de traducción, ideas — lo leemos todo. Los avisos de pronunciación son especialmente bienvenidos: una máquina no oye el acento tónico.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Escuche y elija lo que ha oído:",
    "quiz_question_article": "¿Qué artículo?",
})


# ============================================================================
# БАЛЛЫ: ПЛАТИМ ЗА УСИЛИЕ, А НЕ ЗА НАЖАТИЯ
#
# Верный ответ стоит по-разному в зависимости от канала (1/2/3): узнать на
# слух труднее, чем прочитать, а произнести труднее, чем узнать. Платить
# за все три одинаково значило бы советовать «не напрягайся».
#
# Точность начисляется плавно, без прежнего обрыва на 90%: человек с 89%
# видел, что двадцать баллов пропали из-за одного вопроса.
#
# Серия растёт в цене: десятый день дороже первого. Прежде день давал ровно
# три балла, и терять серию было почти не жалко.
# ============================================================================
TEXTS.update({
})


# ============================================================================
# ГОТОВНОСТЬ ГОЛОСА
#
# Предсинтезированы не все голоса: это гигабайты и часы на каждый. У
# остальных клип делается на лету, и на недокументированном движке синтез
# срывается примерно в одном случае из пяти — слово приходит без звука.
#
# Владелец выбрал голос без единого клипа и половину карточек слушал молча,
# не имея возможности узнать причину: все голоса выглядели одинаково.
# ============================================================================
TEXTS.update({
})


# ============================================================================
# ИТОГ КРУГА: сколько вопросов было на слух
#
# Иначе новая игра растворяется в общем списке, и человек не замечает, что
# уже узнаёт слова ушами. Строка показывается, только если такие вопросы
# были.
# ============================================================================
TEXTS.update({
    "quiz_result_by_ear": "🎧 De oído: {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "Juegos de la lección",
    "settings_channels_line": "Lección: <b>{channels}</b>",
    "channels_title": "<b>Juegos de la lección</b>",
    "channels_description": "Qué juegos mezclar en una lección. Una palabra nueva llega como tarjeta “Leo”; cuando ya la conoce, vuelve en otros juegos: recordarla, oírla, decirla, construir una frase con ella. Cuantos más juegos, mejor se fija la palabra.",
    "channel_text": "📖 Leo",
    "channel_audio": "🎧 Escucho",
    "channel_speech": "🎤 Hablo",
    "channel_build": "🧱 Construyo",
    "home_scale_build": "Construyo",
    "quiz_result_built": "🧱 Construidas: {count}",
    "build_hint": "Construya la frase con las palabras de abajo — algunas sobran",
    "build_btn_check": "Comprobar",
    "build_full": "Todos los huecos están llenos. Quite una palabra con ⌫ o pulse “Comprobar”.",
    "build_order_only": "↔ <b>Palabras correctas, otro orden</b>",
    "build_reference": "Correcto:",
    "build_yours": "Su respuesta:",
    "build_extra": "Sobran: {words}",
    "build_missing": "Faltan: {words}",
    "stats_grammar_line": "Gramática: {correct} de {shown} correctas",
    "quiz_result_recalled": "💭 Recordadas: {count}",
    "home_scale_reverse": "Recuerdo",
    "channel_reverse": "💭 Recuerdo",
    "channels_text_always": "“Leo” no se puede desactivar: toda palabra nueva empieza por ahí.",
    "channels_audio_blocked": "🎧 “Escucho” y “Hablo” no están disponibles mientras el audio esté desactivado.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Diga esta palabra en voz alta — grabe un mensaje de voz: mantenga pulsado el icono del micrófono en el campo de mensaje de Telegram, abajo a la derecha",
    "speech_btn_reference": "Escuchar despacio",
    "speech_btn_skip": "Saltar",
    "speech_listening": "🎧 Escuchando…",
    "speech_not_understood": "No se ha entendido. Grábelo de nuevo, por favor — más cerca del micrófono y un poco más alto.",
    "speech_try_again": "Ha sonado como “{heard}” — no del todo. Grábelo de nuevo, por favor: intento {attempt} de {total}.",
    "speech_send_voice": "🎤 Esta pregunta necesita un mensaje de voz. Mantenga pulsado el botón del micrófono.",
    "speech_skipped": "Saltada",
    "speech_not_counted": "Otra vez ha sonado como “{heard}”. No cuenta ni como acierto ni como error — escuche cómo suena y sigamos.",
    "lesson_expired": "Esta lección se ha interrumpido — el bot se actualizó o la lección terminó hace tiempo. Empiece una nueva con el botón de abajo.",
    "quiz_result_spoken": "🎤 En voz alta: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Leo",
    "home_scale_audio": "Escucho",
    "home_scale_speech": "Hablo",
    "home_btn_learn": "Aprender palabras",
    "home_rank": "puesto {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: todavía no. Palabras listas: {ready}, se necesitan al menos {minimum}. Practique con las tarjetas “Leo” — desbloquean los demás juegos.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "Qué aprendo",
    "settings_group_what_title": "<b>Qué aprendo</b>",
    "settings_group_how": "Cómo aprendo",
    "settings_group_how_title": "<b>Cómo aprendo</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Idioma, objetivo y nivel.",
    "settings_group_how_about": "De qué se compone una lección y cómo suena.",
    "settings_group_bot_about": "Idioma del bot, recordatorios y ayuda.",
})


# ============================================================================
# ПЕТЛЯ ВОЗВРАТА
#
# Замер на 233 людях: 79% тех, кто вообще играл, ни разу не занимались два
# дня подряд. У каждого экрана, которым кончается действие, должна быть
# кнопка следующего — иначе человек уходит там, где был готов продолжить.
# Разбор — MENU_CONCEPT.md.
# ============================================================================
TEXTS.update({
    "quiz_btn_one_more": "Otra lección",
    "home_btn_stats": "Más detalles",
    "notif_off_how_to_return": "Para volver a activarlos: Ajustes → Bot → Recordatorios",
    "reminder_offer_done": "✓ Listo: el recordatorio llegará a las <b>{time}</b> ({city})\n\nPuede ajustar la hora, los días y la zona horaria",
    "reminder_offer_setup": "Ajustar recordatorios",
    "level_offer": "En <b>{current}</b> apenas comete errores\n\n¿Quiere pasar a <b>{following}</b>?\n\nTodo lo aprendido se conserva",
    "level_offer_yes": "Sí, pasar a {following}",
    "level_offer_no": "Quedarme aquí",
    "level_offer_done": "Ahora está en <b>{following}</b>\n\nLas palabras serán más difíciles",
    "level_offer_pick": "Parece que <b>{current}</b> le resulta fácil\n\n¿En qué nivel quiere continuar?\n\nTodo lo aprendido se conserva",
    "level_offer_stay": "Quedarme en {current}",
    "placement_result": "Según sus respuestas, le corresponde el nivel <b>{level}</b> — las próximas palabras serán de este nivel\n\nSi prefiere otro, elíjalo abajo",
    "level_set_done": "Nivel <b>{level}</b>\n\nLas próximas palabras serán de este nivel",
    "level_down_offer": "Por ahora hay bastantes errores en <b>{current}</b>\n\n¿Quiere pasar a <b>{previous}</b>?\n\nLas palabras serán más fáciles, y todo lo aprendido se conserva",
    "level_down_yes": "Sí, pasar a {previous}",
    "level_down_done": "Ahora está en <b>{previous}</b>\n\nLas palabras serán más fáciles",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "¿Para qué necesita el idioma? Elegiremos las palabras en consecuencia.",
    "goal_work": "Para el trabajo",
    "goal_travel": "Para viajar",
    "goal_living": "Para vivir en el extranjero",
    "goal_study": "Para estudiar",
    "goal_any": "Solo aprender palabras",
})


# ============================================================================
# ВСТУПИТЕЛЬНЫЙ БЛОК /start
#
# Сюда возвращаются, только набрав команду руками, — то есть затем,
# чтобы понять, что это за бот и что он умеет. Прежний текст вместо
# этого перечислял кнопки, которые человек видит перед собой, и обещал
# «Помощь» среди них, откуда она уехала в настройки.
# ============================================================================
TEXTS.update({
    "intro_games": "Aquí cada palabra se aprende con cinco juegos: leerla, recordarla a partir del significado, oírla, decirla en voz alta y emparejarla en el tablero.\nCada lección los mezcla por usted.",
    "intro_numbers": "12 902 palabras · 20 temas · 6 niveles\n{languages} en cualquier combinación: puede aprender polaco a través del inglés, si quiere.",
    "intro_menu_settings": "idioma, juegos de la lección, recordatorios",
    "intro_menu_stats": "su progreso",
    "intro_menu_rating": "la clasificación del mes",
    "intro_menu_learn": "una lección",
    "intro_menu_title": "Qué hay en cada sitio:",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Objetivo",
    "settings_goal_title": "<b>Para qué lo necesito</b>",
    "settings_goal_description": "Primero llegarán las palabras de su tema. La dificultad sigue dependiendo de su nivel, y lo aprendido seguirá volviendo para repasarlo.",
    "settings_goal_set": "Objetivo guardado",
    "settings_goal_line": "Objetivo: <b>{goal}</b>",
    "settings_goal_none": "sin elegir",
})


# ============================================================================
# ДОСКА СОПОСТАВЛЕНИЯ — ЧЕТВЁРТАЯ ИГРА
#
# Пять слов слева, их значения справа, стоят не напротив друг друга.
# Это НЕ четвёртый навык: сопоставление проверяет узнавание
# написанного, то есть то же, что карточка, только задачу делает легче
# — последняя пара достаётся бесплатно. Поэтому в прогресс идут лишь
# пары, сошедшиеся с первой попытки, и никогда последняя.
# ============================================================================
TEXTS.update({
    "match_title": "<b>Encuentre las parejas</b>",
    "match_progress": "Emparejadas: {matched} de {total}",
    "match_errors": "✗ errores: {count}",
    "match_hint": "Pulse una palabra de cualquier lado y luego su pareja del otro.",
    "match_wrong": "✗ No es pareja",
    "match_done": "<b>¡Tablero completado!</b>",
    "match_done_counted": "Cuentan para el progreso: {counted} de {total}. Solo cuentan las parejas acertadas al primer intento, y nunca la última: para entonces ya no queda elección.",
    "match_btn_again": "Otro tablero",
    "match_not_ready": "Todavía no: un tablero necesita {need} palabras conocidas, y usted tiene {have}. Practique con las tarjetas “Leo” — lo desbloquean.",
})

TEXTS["match_back_to_round"] = "Volvemos a la lección."

TEXTS.update({
    "settings_btn_match": "Tablero en la lección",
    "settings_match_title": "<b>Tablero en la lección</b>",
    "settings_match_description": "En cada lección, a mitad de camino, un tablero ocupa el lugar de una pregunta: cinco palabras y cinco significados que emparejar. Solo usa palabras conocidas, así que aparece cuando tiene al menos diez.",
    "match_state_on": "El tablero está activado: aparece a mitad de la lección.",
    "settings_match_short_on": "con tablero",
    "settings_channels_short_one": "solo “Leo”",
    "settings_channels_short_some": "{count} de {total} juegos",
    "settings_channels_short_all": "todos los juegos",
    "plural_words": "palabra|palabras",
    "plural_points": "punto|puntos",
    "plural_days": "día|días",
    "settings_audio_short_off": "sin sonido",
    "settings_audio_short_on": "con sonido",
    "settings_match_short_off": "sin tablero",
    "match_state_off": "El tablero está desactivado: la lección son solo preguntas.",
})

# ============================================================================
# СООБЩЕНИЯ ПО ИНИЦИАТИВЕ БОТА — патч 2.1 «Вовлечение» (`nudge_texts`).
# Голос и запрет значков — в ru.py; номера вариантов `_N` те же (тест).
# ============================================================================
TEXTS.update({
    "plural_lessons": "lección|lecciones",
    "nd_teaser_quiz_1": "¿Recuerda qué significa {word}? {meaning}",
    "nd_teaser_quiz_2": "Póngase a prueba: {word} - {meaning}",
    "nd_teaser_quiz_3": "Una de sus palabras: {word} - {meaning}",
    "nd_teaser_quiz_4": "¿Cómo se traduce {word}? {meaning}",
    "nd_teaser_new_1": "Por ejemplo: {word} - {meaning}",
    "nd_teaser_new_2": "Primera palabra: {word} - {meaning}",
    "nd_teaser_new_3": "¿Cómo se traduce {word}? La traducción está oculta - tóquela: {meaning}",
    "nd_streak_head_1": "<b>{name}, racha: {days} seguidos</b>",
    "nd_streak_head_2": "<b>{name}, {days} seguidos. ¿Continuamos?</b>",
    "nd_streak_head_3": "<b>{name}, ya son {days} seguidos</b>",
    "nd_streak_head_4": "<b>{name}, {days} sin interrupción</b>",
    "nd_streak_head_5": "<b>{name}, una lección más y serán {next_days} seguidos</b>",
    "nd_streak_head_6": "<b>{name}, su racha le espera: {days}</b>",
    "nd_streak_head_7": "<b>{days} seguidos, {name}</b>",
    "nd_streak_head_8": "<b>{name}, {days} seguidos. ¿Una lección más hoy?</b>",
    "nd_body_learned_1": "Palabras conocidas: {known_n} · aprendidas: {learned}",
    "nd_body_learned_2": "Palabras en estudio: {in_work} · aprendidas: {learned}",
    "nd_body_learned_3": "Ya conoce {known}; {learned} de ellas, aprendidas.",
    "nd_body_known_1": "Palabras conocidas: {known_n}. Cada lección añade nuevas.",
    "nd_body_known_2": "Palabras en estudio: {in_work}. Las primeras aprendidas están cerca.",
    "nd_body_known_3": "Ya conoce {known}.",
    "nd_streak_close_1": "Pasos pequeños llevan a un gran resultado.",
    "nd_streak_close_2": "Un poco cada día: así se quedan las palabras.",
    "nd_streak_close_3": "Una lección hoy alargará la racha.",
    "nd_streak_close_4": "Una lección dura unos {minutes_n} minutos.",
    "nd_streak_close_5": "La constancia importa más que la duración de la lección.",
    "nd_progress_head_known": "<b>{name}, ya conoce {known}</b>",
    "nd_progress_head_1": "<b>{name}, sus palabras esperan un repaso</b>",
    "nd_progress_head_2": "<b>{name}, ¿tiene unos minutos?</b>",
    "nd_progress_head_3": "<b>{name}, ¿seguimos donde lo dejó?</b>",
    "nd_progress_head_4": "<b>{name}, ¿volvemos a sus palabras?</b>",
    "nd_progress_head_5": "<b>{name}, buen momento para refrescar sus palabras</b>",
    "nd_due_1": "Palabras para repasar: {due_n}. El bot lleva la cuenta de los plazos.",
    "nd_due_2": "Es hora de repasar {due} antes de que se borren.",
    "nd_due_3": "Palabras por repasar: {due_n}. El bot ya ha elegido por dónde empezar.",
    "nd_due_many_1": "Hay bastantes palabras pendientes: la lección empezará por las más importantes.",
    "nd_due_many_2": "Se han acumulado repasos. Basta con una lección al día, el resto puede esperar.",
    "nd_praise_1": "{lessons} hechas. Poco a poco, pero con constancia.",
    "nd_praise_2": "Lecciones completadas: {lessons_n}. Pasos pequeños llevan a un gran resultado.",
    "nd_praise_3": "{lessons} a sus espaldas, y cada una sumó palabras.",
    "nd_short_1": "Una lección dura unos {minutes_n} minutos.",
    "nd_short_2": "Son unos pocos minutos.",
    "nd_first_head_words": "<b>{name}, ayer aprendió {words}</b>",
    "nd_first_head_1": "<b>{name}, un buen comienzo</b>",
    "nd_first_head_2": "<b>{name}, ¿repasamos las palabras de ayer?</b>",
    "nd_first_body_1": "Repasar al día siguiente ayuda a fijar las palabras.",
    "nd_first_body_2": "El segundo día es el mejor momento para afianzar palabras nuevas.",
    "nd_first_close_1": "Son unos pocos minutos.",
    "nd_first_close_2": "Una lección dura unos {minutes_n} minutos.",
    "nd_kept_head_1": "<b>{name}, todo sigue en su sitio</b>",
    "nd_kept_head_2": "<b>{name}, sus palabras están guardadas</b>",
    "nd_kept_head_3": "<b>{name}, ha pasado un tiempo</b>",
    "nd_kept_body_1": "Palabras conocidas: {known_n} · aprendidas: {learned}. No se ha perdido nada - la lección empezará por las que toca refrescar.",
    "nd_kept_body_2": "Todo lo que ha aprendido está guardado. La lección empezará por las palabras que toca refrescar.",
    "nd_kept_body_3": "Todos hacemos pausas. Puede empezar con una lección corta.",
    "nd_kept_best": "Mejor racha: {best} seguidos. Una nueva empieza con una lección.",
    "nd_farewell_head_1": "<b>{name}, no habrá más recordatorios</b>",
    "nd_farewell_head_2": "<b>{name}, el último recordatorio</b>",
    "nd_farewell_body_1": "El bot no volverá a escribirle hasta que usted vuelva. Todo está guardado: palabras conocidas {known_n}, aprendidas {learned}. Puede continuar cuando quiera con el botón de abajo.",
    "nd_farewell_body_2": "Parece que ahora no es momento para lecciones - no pasa nada. No habrá más recordatorios. Sus palabras y su progreso están guardados.",
    "nd_start_head_1": "<b>{name}, sus primeras palabras le esperan</b>",
    "nd_start_head_2": "<b>{name}, ¿empezamos?</b>",
    "nd_start_head_3": "<b>{name}, la primera lección dura unos {minutes_n} minutos</b>",
    "nd_start_body_1": "El bot elegirá las palabras más útiles para su nivel y llevará la cuenta de cuándo repasarlas.",
    "nd_start_body_2": "Empezamos por las palabras más frecuentes, las que se oyen cada día.",
    "nd_start_body_3": "No hace falta prepararse: {questions} preguntas, y después el bot le dirá qué repasar y cuándo.",
    "nd_start3_head_1": "<b>{name}, ¿lo prueba?</b>",
    "nd_start3_head_2": "<b>{name}, sus primeras palabras siguen esperando</b>",
    "nd_start_last_head": "<b>{name}, la última invitación</b>",
    "nd_start_last_body": "No habrá más recordatorios. Si quiere empezar, la primera lección dura unos {minutes_n} minutos - el botón está abajo.",
    "nd_btn_optin": "Recuérdemelo a las {time}",
    "nd_btn_stop": "No enviar más",
    "nd_auto_time": "Le enviaré un recordatorio cada día a las {time}. Puede cambiar la hora",
    "nd_btn_change_time": "Cambiar la hora",
    "nd_optin_done": "✓ Listo: el recordatorio llegará a las <b>{time}</b>\n\nPuede cambiar la hora en los ajustes",
})
