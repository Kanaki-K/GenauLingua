"""
Localisation française pour GenauLingua Bot

Набор ключей и порядок — как в en.py. Обращение только на «vous». Перед
«? ! : ; %» и внутри «ёлочек» — неразрывный пробел (французская типографика:
знак не уезжает на новую строку в Telegram).
"""

TEXTS = {
    # ============================================================================
    # MENU PRINCIPAL
    # ============================================================================
    "btn_learn_words": "Apprendre des mots",
    "btn_stats": "Statistiques",
    "btn_settings": "Réglages",
    "btn_help": "Aide",
    "btn_back": "Retour",
    "menu_placeholder": "Choisissez une action…",

    # ============================================================================
    # ACCUEIL ET DÉMARRAGE
    # ============================================================================
    "welcome_title": "<b>Bonjour, {name} !</b>",








    # ============================================================================
    # RAPPELS
    # ============================================================================
    "notif_title": "<b>Rappels</b>",
    "notif_status": "État : {status}",
    "notif_status_on": "activés",
    "notif_status_off": "désactivés",
    "notif_time": "Heure : {time}",
    "notif_days": "Jours : {days}",
    "notif_timezone": "Fuseau horaire : {timezone}",
    "notif_hint": "Le rappel arrive à l’heure choisie, dans votre fuseau horaire.",
    "notif_hint_off": "Activez les rappels — il sera plus facile de garder votre série.",

    "notif_btn_toggle_on": "Rappels : activés",
    "notif_btn_toggle_off": "Rappels : désactivés",
    "notif_btn_time": "Heure : {time}",
    "notif_btn_days": "Choisir les jours",
    "notif_btn_timezone": "Changer de fuseau horaire",

    "notif_timezone_title": "<b>Votre fuseau horaire</b>",
    "notif_timezone_current": "Actuel : {timezone}",
    "notif_timezone_prompt": "Choisissez une ville de votre fuseau horaire :",
    "notif_timezone_more": "Autre ville",
    "notif_timezone_back": "Retour",
    "notif_timezone_set": "✓ Fuseau horaire défini : {city}",

    "notif_time_title": "<b>Heure du rappel</b>",
    "notif_time_current": "Heure actuelle : {time}",
    "notif_time_timezone": "Fuseau horaire : {timezone}",
    "notif_time_hint": "Le rappel arrive à cette heure, les jours que vous avez choisis.",
    "notif_time_set": "✓ Heure définie : {time}",

    "notif_days_title": "<b>Jours de rappel</b>",
    "notif_days_hint": "Touchez un jour pour l’activer ou le désactiver.\n✓ — jour activé\n✗ — jour désactivé\n\nQuand vous avez terminé, touchez « Enregistrer ».",
    "notif_days_all": "Tous les jours",
    "notif_days_weekdays": "En semaine (lun–ven)",
    "notif_days_save": "Enregistrer",
    "notif_days_saved": "✓ Jours enregistrés !",
    "notif_days_all_selected": "✓ Tous les jours sélectionnés",
    "notif_days_weekdays_selected": "✓ Jours de semaine sélectionnés (lun–ven)",
    "notif_days_none": "Choisissez au moins un jour.",

    "notif_toggle_on": "Rappels activés",
    "notif_toggle_off": "Rappels désactivés",

    "day_mon": "Lun",
    "day_tue": "Mar",
    "day_wed": "Mer",
    "day_thu": "Jeu",
    "day_fri": "Ven",
    "day_sat": "Sam",
    "day_sun": "Dim",

    "notif_btn_back": "Retour aux réglages",

    "notif_default_name": "ami",



    # UNE RAISON DE REVENIR — et elle doit être vraie

    # ============================================================================
    # RÉGLAGES
    # ============================================================================
    "settings_title": "<b>Réglages</b>",
    "settings_mode": "Mode : <b>{mode}</b>",
    "settings_language": "Langue du bot : <b>{language}</b>",

    "settings_btn_quiz_mode": "Niveau et thèmes",
    "settings_btn_change_language": "Langue du bot",
    "settings_btn_notifications": "Rappels",

    "settings_quiz_mode_line": "Niveau : <b>{mode}</b>",
    "start_pick_language": "Choisissez votre langue",
    "onboard_your_lang": "✓ Votre langue : {language}",
    "onboard_change_hint": "Vous pouvez la changer à tout moment : commande /language.",
    "onboard_phone_hint": "Votre Telegram est en français. Si vous avez choisi la mauvaise langue, appuyez sur « {back} ».",
    "lang_confirm_learning": "Vous apprenez : {language}",
    "lang_progress_kept": "La progression de chaque langue est conservée.",
    "btn_done": "Terminé",
    "btn_change_learning": "Changer la langue apprise",
    "intro_pair": "Vous apprenez {learning} avec traduction en {native}.",
    "intro_menu_language": "langue du bot",
    "plural_languages": "langue|langues",
    "cmd_start": "Démarrer et ce que fait le bot",
    "cmd_language": "Langue du bot",
    "cmd_settings": "Réglages",
    "cmd_help": "Aide",

    "language_changed": "✓ Langue changée : {language}",
    "user_not_found": "✗ Profil introuvable. Envoyez /start, s’il vous plaît",

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
    # MODE DU QUIZ
    # ============================================================================
    "qmode_title": "<b>Niveau et thèmes</b>",
    "qmode_current": "Actuel : <b>{mode}</b>",
    "qmode_choose": "Choisissez votre façon d’apprendre.\nVous pouvez changer à tout moment — votre progression est conservée.",

    "qmode_btn_level": "Par niveau",
    "qmode_btn_category": "Par thème",
    "qmode_btn_all": "Tous les mots",
    "qmode_btn_difficult": "Mots difficiles",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Tous les mots",
    "qmode_difficult_short": "Mots difficiles",

    "qmode_level_title": "<b>Choisissez un niveau</b>",
    "qmode_level_desc": "Des premiers mots à la conversation fluide. Tous les niveaux sont ouverts — choisissez le vôtre.\n\n• A1–A2 — vocabulaire de base\n• B1–B2 — communication assurée\n• C1–C2 — langue fluide et nuancée",
    "qmode_level_set": "✓ Mode : par niveau ({level})",

    "qmode_category_title": "<b>Choisissez un thème</b>",
    "qmode_category_desc": "De la cuisine aux sciences — choisissez le thème qu’il vous faut.\n\nChaque thème contient des mots de tous les niveaux.",
    "qmode_category_set": "✓ Thème : {category}",

    # Noms des thèmes
    "cat_arbeit_beruf": "Travail",
    "cat_bildung_lernen": "Éducation",
    "cat_einkaufen_geld": "Achats",
    "cat_emotionen_charakter": "Émotions",
    "cat_essen_trinken": "Alimentation",
    "cat_freizeit_sport": "Sport",
    "cat_gesundheit_medizin": "Santé",
    "cat_grammatik": "Grammaire",
    "cat_kleidung_mode": "Vêtements",
    "cat_kommunikation": "Communication",
    "cat_kultur_kunst": "Culture",
    "cat_mensch_familie": "Famille",
    "cat_natur_wetter": "Nature",
    "cat_recht_staat": "Droit",
    "cat_reisen_transport": "Voyages",
    "cat_technik_digital": "Technologie",
    "cat_wirtschaft": "Économie",
    "cat_wissenschaft": "Sciences",
    "cat_wohnen_haus": "Logement",
    "cat_zeit_alltag": "Quotidien",

    "qmode_all_set": "✓ Mode : tous les mots",

    "qmode_difficult_set": "✓ Mode : mots difficiles",
    "qmode_difficult_few": "Mots difficiles pour l’instant : {count} — il en faut au moins 4.\nFaites encore quelques leçons !",
    "qmode_difficult_empty": "Pas encore de mots difficiles.\nFaites d’abord quelques leçons !",

    "quiz_btn_change_mode": "Niveau et thèmes",
    "quiz_btn_report_error": "Signaler une erreur",
    "report_btn_confirm": "✓ Confirmer ({count})",
    "report_btn_send": "Envoyer",
    "report_kind_text": "Traduction",
    "report_kind_example": "Exemple",
    "report_kind_audio": "Audio",
    "report_pick_hint": "Qu’est-ce qui ne va pas ? Cochez puis appuyez sur « Envoyer »",
    "report_btn_sent": "✓ Signalement envoyé",
    "report_sent_one": "✓ Merci !\nSi l’erreur est confirmée, vous recevrez +{points}.",
    "report_approved_example": "✓ Votre signalement sur l’exemple de <b>{word}</b> a été accepté\n\nNous corrigerons l’exemple\n\n+{points} points à votre score du mois, merci",
    "report_no_words": "Aucun mot à signaler",
    "report_none_selected": "Sélectionnez au moins un mot",
    "report_pick_kind": "Mots sélectionnés : {count}. Indiquez maintenant ce qui ne va pas : la traduction ou la prononciation.",
    "report_sent": "✓ Signalements envoyés : {count} — merci !\nChaque signalement confirmé rapporte +{points}.",
    "report_daily_limit": "Vous avez atteint la limite de 20 signalements pour aujourd’hui.",
    "report_all_reported": "✓ Tous les mots de cette leçon ont déjà été signalés",
    "report_already_sent": "✓ Déjà signalé",
    "report_btn_kind_text": "Traduction erronée",
    "report_btn_kind_audio": "Prononciation erronée",
    "report_sent_audio": "✓ Signalements envoyés : {count} — merci !\nLes signalements de prononciation sont particulièrement précieux : la vérification automatique n’entend pas l’accent tonique.\nChaque signalement confirmé rapporte +{points}.",
    "report_approved": "✓ Votre signalement sur <b>{word}</b> a été accepté, nous corrigerons la traduction\n\n+{points} points à votre score du mois. Merci, le dictionnaire s’améliore pour tout le monde",
    "award_won": "{mark} Classement du mois ({month}) : place {rank}\n\n{bonus} points ajoutés à votre score total",
    "report_approved_audio": "✓ Votre signalement de prononciation sur <b>{word}</b> a été accepté\n\nL’enregistrement sera corrigé\n\n+{points} points à votre score du mois, merci",
    # ============================================================================
    # QUIZ
    # ============================================================================
    "quiz_no_level": "Choisissez d’abord votre niveau : /start",
    "quiz_error_generation": "✗ Un problème est survenu pendant la préparation de la leçon.\nRéessayez via /start",
    "quiz_no_words": "✗ Désolé, il n’y a pas de mots pour ce niveau.\nEssayez un autre niveau.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Juste</b>",
    "quiz_wrong": "✗ <b>Faux</b>",
    "quiz_correct_answer": "Bonne réponse :",

    "quiz_btn_next": "Suivant →",

    "quiz_answer_already_counted": "Votre réponse a déjà été prise en compte. On continue ?",
    "quiz_btn_repeat_errors": "Revoir les erreurs",
    "lesson_resume_prompt": 'Vous avez une leçon inachevée\xa0: {done} sur {total}',
    "btn_lesson_resume": 'Continuer',
    "btn_lesson_new": 'En commencer une nouvelle',
    "speech_offer_text": 'Parler à voix haute ne semble pas pratique en ce moment. Retirer «\xa0Je parle\xa0» des leçons\xa0? Vous pourrez le remettre dans les réglages',
    "btn_speech_off": 'Retirer «\xa0Je parle\xa0»',
    "btn_speech_keep": 'Garder',
    "speech_off_done": 'C’est fait\xa0: «\xa0Je parle\xa0» n’apparaîtra plus dans les leçons. Vous pourrez le remettre dans les réglages',

    "quiz_completed": "<b>Leçon terminée</b>",
    "quiz_result_correct": "Bonnes réponses : <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Résultat : <b>{percentage} %</b>",
    "quiz_result_details": "<b>Détails :</b>",
    "quiz_result_errors": "Erreurs : {count}",

    # ÉLOGES EN FIN DE LEÇON — seulement pour ce qui s’est vraiment passé
    "praise_first_round": "Première leçon terminée. Désormais, les mots vont revenir — c’est ainsi qu’ils se fixent.",
    "praise_first_learned": "Premier mot appris : trois bonnes réponses d’affilée, aucune le jour de la découverte.",
    "praise_learned": "Mots appris pendant cette leçon : {count}",
    "praise_best_streak": "Record personnel : {days_word} d’affilée",
    "praise_milestone": "Vous apprenez maintenant {count} mots",
    "praise_first_speech": "Première bonne réponse à voix haute",
    "praise_first_audio": "Première bonne réponse à l’oreille",
    "praise_comeback": "Bon retour ! Cela faisait {days_word}.",
    "praise_perfect": "Une leçon sans une seule erreur",
    "praise_streak": "Série : {days_word} d’affilée",
    "praise_freeze_saved": "Vous avez manqué hier, mais une protection de série l’a sauvée : {days_word} d’affilée. La prochaine protection sera disponible dans une semaine.",
    "praise_streak_3": "Trois jours d’affilée — une habitude se forme.",
    "praise_streak_7": "Une semaine entière d’affilée ! C’est le cap décisif : à partir d’ici, l’habitude tient toute seule.",
    "praise_streak_14": "Deux semaines d’affilée — excellent rythme.",
    "praise_streak_30": "Un mois d’affilée ! C’est désormais une vraie habitude.",
    "praise_new_words": "Nouveaux mots : {count}",
    "praise_returned": "Reconnus à nouveau : {count}",
    "praise_progress": "Mots en cours d’apprentissage : {count} · encore {left} pour atteindre {target}",
    "praise_progress_top": "Mots en cours d’apprentissage : {count}",
    "praise_points": "Points : +{points}",

    "quiz_repeat_title": "<b>Revoir les erreurs</b>",
    "quiz_no_errors": "✓ Aucune erreur cette fois !",
    "quiz_error_next": "✗ Impossible de charger la question suivante.",

    # ============================================================================
    # STATISTIQUES
    # ============================================================================
    "stats_no_level": "<b>Choisissez d’abord votre niveau !</b>\n\nEnvoyez /start pour commencer.",





    # ============================================================================
    # AIDE
    # ============================================================================
    "help_title": "<b>Aide — GenauLingua</b>",
    "help_description": "Comment fonctionnent les leçons et comment rejoindre la communauté.",
    "help_choose": "Choisissez une rubrique :",

    "help_btn_how_to_use": "Mode d’emploi",
    "help_btn_community": "Communauté",

    "help_how_to_use_title": "<b>Comment utiliser le bot</b>",


    "help_community_title": "<b>Communauté GenauLingua</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

Dans le chat :
Soyez les premiers informés des nouveautés
Vous avez trouvé un bug — écrivez-nous ou envoyez une capture d’écran
Erreur de traduction — signalez-la, nous la corrigerons
Idées et suggestions — nous lisons tout
Échangez avec d’autres apprenants


Plus la communauté est active, meilleur devient le bot. N’hésitez pas ! """,


    # ============================================================================
    # CLASSEMENT
    # ============================================================================
    "rating_not_active": "✗ Le classement n’est pas encore actif.",
    "rating_not_in_ranking": "Pas encore de place au classement",
    "rating_start_quiz": "Faites votre première leçon !",
    "rating_join_by_lesson": "Vos points de signalement ({score}) sont crédités. Terminez une leçon pour entrer dans le classement du mois.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — nous avons reconstruit le bot de zéro</b>\n\n<b>Pas seulement l’allemand.</b> Apprenez l’ukrainien, l’anglais, le turc, l’allemand, le polonais ou le russe — à partir de n’importe laquelle de ces langues. L’interface parle aussi les six.\n\n<b>Six jeux au lieu d’un.</b> Avant, il n’y avait que « choisir la traduction ».\n\nDésormais, les jeux alternent dans chaque leçon :\n📖 Je lis · 💭 Je me souviens · 🎧 J’écoute · 🎤 Je parle · 🧩 Trouvez les paires · 🧱 Je construis\n\nDans « Je parle », vous répondez à voix haute ; dans « Je construis », vous assemblez une phrase — le bot montre quel mot n’est pas à sa place.\n\n<b>Le bot parle.</b> Chaque mot et chaque exemple est lu par une voix naturelle.\n\n<b>Un nouveau look.</b> Un nouveau menu, un chat propre et sans encombrement, un écran d’accueil avec vos compétences, des statistiques claires, un nouvel avatar et un nouveau message d’accueil.\n\n<b>Tout le dictionnaire a été relu</b> — les 12 902 mots, traductions et exemples.\n\n<b>Il s’adapte à vous :</b> les mots reviennent juste avant que vous ne les oubliiez, et le bot propose le niveau suivant quand ça devient facile.\n\n<b>Bugs corrigés :</b> votre série de jours est comptée correctement, et les points du classement sont justes — ils récompensent l’effort. « Appris » est honnête aussi désormais : un mot compte comme appris après trois bonnes réponses d’affilée, à des jours différents, et chaque mot pratiqué apparaît dans « Mots en cours d’apprentissage ».\n\n<b>Les rappels sont activés</b> — à votre heure. Pour les modifier ou les désactiver : Réglages → Bot → Rappels.\n\n⭐ Vous avez repéré une erreur ? Signalez-la directement depuis le bilan de la leçon : chaque signalement confirmé rapporte +15 points.\n\nVotre progression et vos points sont conservés. Essayez — une leçon prend quelques minutes.",
    "release_notes_2026_10_22": '✨ <b>GenauLingua 2.2 - désormais dix langues</b>\n\nBonjour\xa0!\n\nUne grande mise à jour est disponible\xa0:\n\n<b>4 nouvelles langues</b>\n\n🇮🇹 L’italien, 🇪🇸 l’espagnol, 🇫🇷 le français et 🇨🇿 le tchèque - à apprendre depuis n’importe quelle langue du bot\nChacune compte plus de 12\xa0000 mots avec exemples, tous avec audio\n\n<b>Un classement qui donne envie de se battre</b>\n\nMédailles du mois 🥇🥈🥉, couronne 👑 pour la première place parmi ceux qui apprennent votre langue, et des titres qui évoluent avec vous. Premiers résultats selon les nouvelles règles - le 1er novembre\n\n<b>La série pardonne un jour manqué</b>\n\nUne fois par semaine, la protection de série 🧊 sauve votre série si vous manquez un jour\n\n<b>Et aussi\xa0:</b> signalez une erreur de traduction, d’exemple ou d’audio - juste sous la réponse (+15 points par signalement confirmé)\n\nLes mots connus s’apprennent plus vite, et les mises à jour du bot n’interrompent plus la leçon\n\nMerci d’apprendre avec nous et de signaler les erreurs - c’est ainsi que le bot s’améliore pour tous 💙\n\nToutes les nouveautés, en bref et en images\xa0: <a href="{url}">nouveautés de la 2.2</a>',
    "btn_release_news": 'Nouveautés →',


    "table_empty": "Personne n’a encore participé.\nLa première place vous attend : faites une leçon !",
    "table_you_not_ranked": "Pas encore de place au classement",
    "rating_tab_month": "Mois",
    "rating_tab_alltime": "Global",
    "rating_crown_rule": "La première place reçoit la couronne pour tout le mois suivant",
    "rating_screen_title": "<b>Classement · {month} {year}</b>",
    "rating_screen_title_alltime": "<b>Classement · depuis le début</b>",
    "rating_you": "<b>Vous : #{rank} sur {total}</b> · {points}",
    "rating_results_in": "Résultats du mois dans {days}",
    "info_title": "<b>Comment fonctionne le classement</b>",
    "info_month": "<b>Mois</b> — tout le monde. Les trois meilleurs reçoivent 🥇 🥈 🥉 (dès 3 leçons).",
    "info_lang": "<b>Langue</b> — ceux qui apprennent votre langue. Le premier reçoit 👑 pour le mois suivant.",
    "info_alltime": "<b>Global</b> — tous les points. Les médailles font évoluer votre titre 🌱 🌳 🌙 🪐 ☀️",
    "info_points_title": "<b>Points</b>",
    "info_points": "Réponse +1 · à l’oreille +2 · à voix haute +3\nLeçon +10 · mot appris +3\nJours d’affilée — jusqu’à +10 · précision au-dessus de 60% — bonus\nSignalement confirmé +{points}",
    "title_sprout": "Pousse",
    "title_tree": "Arbre",
    "title_moon": "Lune",
    "title_planet": "Planète",
    "title_sun": "Soleil",
    "title_galaxy": "Galaxie",
    "btn_rating_info": "Infos",
    "card_medal_need": "Leçons nécessaires pour une médaille : {need} · vous en avez {have}",
    "card_crown_small": "La couronne se joue quand la langue compte 3+ personnes avec 3+ leçons",
    "summary_place": "↑ Place du mois : {rank}",
    "summary_gap": "{gap} de retard sur {name}",
    "summary_record": "Nouveau record du mois : {points}",
    "collection_title": "<b>Collection</b> · {open} sur {total} débloqués",
    "collection_locked": "▫️ ???",
    "ach_streak_7": "Série de 7 jours",
    "ach_streak_30": "Série de 30 jours",
    "ach_streak_100": "Série de 100 jours",
    "ach_streak_365": "Série de 365 jours",
    "ach_streak_1000": "Série de 1000 jours",
    "ach_words_100": "100 mots appris",
    "ach_words_1000": "1000 mots appris",
    "ach_words_3000": "3000 mots appris",
    "ach_perfect_10": "10 leçons sans faute",
    "ach_voice_1000": "1000 bonnes réponses à voix haute",
    "ach_editor": "Éditeur du dictionnaire : 5 signalements acceptés",
    "ach_polyglot": "Polyglotte : 100 mots dans deux langues",
    "award_month_header": "<b>Résultats du mois</b>",
    "award_crown": "👑 Couronne — {language} : première place. Portez-la tout le mois suivant",
    "award_glory": "+{glory} de gloire",
    "award_new_title": "Nouveau titre : {mark} {name}",
    "nd_overtaken": "On vous a dépassé dans le classement du mois.\nVotre place : {rank} · {gap} de retard sur {name}.",
    "nd_finish": "Jusqu’à la fin du mois : {days}.\nVotre place : {rank} · il vous manque {gap} pour une médaille.",

    "stats_header": "<b>Vos statistiques</b>",
    "stats_in_work_line": "Mots en cours d’apprentissage : {count} · encore {left} pour atteindre {target}",
    "stats_in_work_top": "Mots en cours d’apprentissage : {count}",
    "stats_details": "En cours : {progress}\nNouveaux : {new}\nDifficiles : {difficult}",
    "stats_achievements_title": "<b>Vos réussites</b>",
    "stats_words_count": "Mots appris : <b>{count}</b>",
    "stats_best_streak_line": "Meilleure série : {days_word}",
    "stats_quizzes_header": "<b>Leçons · {level}</b>",
    "stats_quizzes_passed_line": "Terminées : <b>{count}</b>",
    "stats_quizzes_avg_line": "Résultat moyen : <b>{percent} %</b>",
    "stats_quizzes_best_line": "Meilleur résultat : <b>{percent} %</b>",
    "stats_quizzes_empty": "Aucune leçon terminée pour l’instant",
    "stats_recent_header": "<b>Dernières leçons</b>",
    "stats_explanation": "Un mot compte comme appris après trois bonnes réponses d’affilée, à des jours différents.",
}

# ============================================================================
# MULTILINGUE : langue apprise, langue des significations et sens
# ============================================================================
TEXTS.update({
    "langname_de": "Allemand",
    "langname_en": "Anglais",
    "langname_ru": "Russe",
    "langname_uk": "Ukrainien",
    "langname_tr": "Turc",
    "langname_pl": "Polonais",
    "langname_it": "Italien",
    "langname_es": "Espagnol",
    "langname_fr": "Français",
    "langname_cs": "Tchèque",
    # Союз для перечисления языков в текстах помощи и приветствия
    "and_word": "et",

    "settings_learning_lang_line": "J’apprends : <b>{language}</b>",

    "settings_btn_learning_lang": "Langue",

    "learning_lang_title": "<b>Langue à apprendre</b>",
    "learning_lang_description": "Choisissez la langue dont vous voulez apprendre les mots.\nLa progression est suivie séparément pour chaque langue.",
    "learning_lang_set": "✓ J’apprends : {language}",
    # Ligne des réglages et écran du son
    "settings_audio_line": "Son : <b>{state}</b>",
    "settings_btn_audio": "Son",
    "audio_state_on": "activé",
    "audio_state_off": "désactivé",

    "audio_title": "<b>Son</b>",
    "audio_description": "Les mots sont lus par une voix d’IA naturelle. La question fait entendre le mot seul, la réponse le mot avec son exemple.",
    "audio_current_voice": "Voix : <b>{voice}</b>",
    "audio_btn_turn_on": "Activer le son",
    "audio_btn_turn_off": "Désactiver le son",
    "audio_btn_choose_voice": "Choisir une voix",
    "audio_turned_on": "✓ Son activé",
    "audio_turned_off": "Son désactivé",

    "voice_title": "<b>Choisissez une voix</b>",
    "voice_description": "Touchez une voix pour l’écouter. La coche indique la voix actuelle.",
    "voice_male": "Homme",
    "voice_female": "Femme",
    "voice_set": "✓ Voix : {voice}",
    "voice_use": "Choisir {voice}",
    "voice_listening": "Lecture : {voice}",
    "voice_only_one": "Pour cette langue, il n’existe qu’une voix d’homme et une voix de femme.",
    "voice_preview_failed": "Impossible de charger l’extrait. Réessayez, s’il vous plaît.",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Classement",
    "friend_fallback": "ami",
    "onboarding_learning_title": "<b>Quelle langue allez-vous apprendre ?</b>",
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
    "help_how_to_use_text": "<b>Leçon</b>\n{words}, quatre options à chaque fois. Une leçon mélange six jeux : « Je lis », « Je me souviens », « J’écoute », « Je parle », « Je construis » et le plateau « Trouvez les paires ». Le bot retient vos erreurs et ramène plus souvent les mots difficiles. Après la leçon, vous pouvez revoir ceux que vous avez manqués.\n\n<b>Son</b>\nLa question fait entendre le mot ; après votre réponse, vous entendez le mot avec son exemple. Choisissez une voix d’homme ou de femme dans les réglages.\n\n<b>Langues</b>\n{languages} — dans n’importe quelle paire. La progression est suivie séparément pour chaque langue ; le classement a les onglets « Mois », « Global » et « Langue ».\n\n\nUn mot compte comme <b>appris</b> après trois bonnes réponses d’affilée, à des jours différents. Si vous répondez juste à un nouveau mot du premier coup, une seule bonne réponse de plus suffit.\nVotre <b>série</b> grandit chaque jour où vous faites au moins une leçon. Un jour manqué par semaine ne la casse pas — une protection de série le couvre.\nTraduction ou prononciation erronée ? Utilisez le bouton « Signaler une erreur » sous la réponse.",
    "help_community_title": "<b>À propos du bot et de la communauté</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} langues dans n’importe quelle paire : {languages}\n12 900 mots A1–C2, chacun avec un exemple et un son naturel.\nInterface : {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nBugs, erreurs de traduction, idées — nous lisons tout. Les signalements de prononciation sont particulièrement bienvenus : une machine n’entend pas l’accent tonique.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Écoutez et choisissez ce que vous avez entendu :",
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
    "quiz_result_by_ear": "🎧 À l’oreille : {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "Jeux de la leçon",
    "settings_channels_line": "Leçon : <b>{channels}</b>",
    "channels_title": "<b>Jeux de la leçon</b>",
    "channels_description": "Les jeux à mélanger dans une leçon. Un nouveau mot arrive sous forme de carte « Je lis » ; une fois connu, il revient dans d’autres jeux : s’en souvenir, l’entendre, le dire, construire une phrase avec. Plus il y a de jeux, mieux le mot se fixe.",
    "channel_text": "📖 Je lis",
    "channel_audio": "🎧 J’écoute",
    "channel_speech": "🎤 Je parle",
    "channel_build": "🧱 Je construis",
    "home_scale_build": "Je construis",
    "quiz_result_built": "🧱 Construites : {count}",
    "build_hint": "Construisez la phrase avec les mots ci-dessous — certains sont en trop",
    "build_btn_check": "Vérifier",
    "build_full": "Toutes les places sont remplies. Retirez un mot avec ⌫ ou appuyez sur « Vérifier ».",
    "build_order_only": "↔ <b>Bons mots, autre ordre</b>",
    "build_reference": "Correct :",
    "build_yours": "Votre réponse :",
    "build_extra": "En trop : {words}",
    "build_missing": "Manquants : {words}",
    "stats_grammar_line": "Grammaire : {correct} sur {shown} justes",
    "quiz_result_recalled": "💭 Retrouvés : {count}",
    "home_scale_reverse": "Je me souviens",
    "channel_reverse": "💭 Je me souviens",
    "channels_text_always": "« Je lis » ne peut pas être désactivé : chaque nouveau mot commence par là.",
    "channels_audio_blocked": "🎧 « J’écoute » et « Je parle » ne sont pas disponibles tant que le son est désactivé.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Dites ce mot à voix haute — enregistrez un message vocal : maintenez l’icône du micro dans le champ de saisie de Telegram, en bas à droite",
    "speech_btn_reference": "Écouter lentement",
    "speech_btn_skip": "Passer",
    "speech_listening": "🎧 J’écoute…",
    "speech_not_understood": "Je n’ai pas bien entendu. Enregistrez à nouveau, s’il vous plaît — plus près du micro et un peu plus fort.",
    "speech_try_again": "On aurait dit « {heard} » — pas tout à fait. Enregistrez à nouveau : essai {attempt} sur {total}.",
    "speech_send_voice": "🎤 Cette question attend un message vocal. Maintenez le bouton du micro.",
    "speech_skipped": "Passé",
    "speech_not_counted": "De nouveau, on aurait dit « {heard} ». Cela ne compte ni comme juste ni comme erreur — écoutez comment le mot se prononce, et passons à la suite.",
    "lesson_expired": "Cette leçon a été interrompue — le bot a été mis à jour ou la leçon s’est terminée il y a longtemps. Commencez-en une nouvelle avec le bouton ci-dessous.",
    "quiz_result_spoken": "🎤 À voix haute : {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Je lis",
    "home_scale_audio": "J’écoute",
    "home_scale_speech": "Je parle",
    "home_btn_learn": "Apprendre des mots",
    "home_rank": "place {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel} : pas encore. Mots prêts : {ready}, il en faut au moins {minimum}. Entraînez-vous avec les cartes « Je lis » — elles débloquent les autres jeux.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "Ce que j’apprends",
    "settings_group_what_title": "<b>Ce que j’apprends</b>",
    "settings_group_how": "Comment j’apprends",
    "settings_group_how_title": "<b>Comment j’apprends</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Langue, objectif et niveau.",
    "settings_group_how_about": "De quoi se compose une leçon et comment elle sonne.",
    "settings_group_bot_about": "Langue du bot, rappels et aide.",
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
    "quiz_btn_one_more": "Encore une leçon",
    "home_btn_stats": "Plus de détails",
    "notif_off_how_to_return": "Pour les réactiver : Réglages → Bot → Rappels",
    "reminder_offer_done": "✓ C’est fait : le rappel arrivera à <b>{time}</b> ({city})\n\nVous pouvez régler l’heure, les jours et le fuseau horaire",
    "reminder_offer_setup": "Régler les rappels",
    "level_offer": "Vous faites rarement des erreurs au niveau <b>{current}</b>\n\nPasser au niveau <b>{following}</b> ?\n\nTout ce que vous avez appris est conservé",
    "level_offer_yes": "Oui, passer à {following}",
    "level_offer_no": "Rester ici",
    "level_offer_done": "Vous êtes maintenant au niveau <b>{following}</b>\n\nLes mots seront plus difficiles",
    "level_offer_pick": "Le niveau <b>{current}</b> semble facile pour vous\n\nÀ quel niveau voulez-vous continuer ?\n\nTout ce que vous avez appris est conservé",
    "level_offer_stay": "Rester au niveau {current}",
    "level_down_offer": "Il y a encore pas mal d’erreurs au niveau <b>{current}</b>\n\nPasser au niveau <b>{previous}</b> ?\n\nLes mots seront plus faciles, et tout ce que vous avez appris est conservé",
    "level_down_yes": "Oui, passer à {previous}",
    "level_down_done": "Vous êtes maintenant au niveau <b>{previous}</b>\n\nLes mots seront plus faciles",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "Pourquoi avez-vous besoin de cette langue ? Nous choisirons les mots en conséquence.",
    "goal_work": "Pour le travail",
    "goal_travel": "Pour voyager",
    "goal_living": "Pour vivre à l’étranger",
    "goal_study": "Pour les études",
    "goal_any": "Juste apprendre des mots",
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
    "intro_games": "Ici, chaque mot s’apprend à travers cinq jeux : le lire, le retrouver à partir du sens, l’entendre, le dire à voix haute et l’associer sur le plateau.\nChaque leçon les mélange pour vous.",
    "intro_numbers": "12 902 mots · 20 thèmes · 6 niveaux\n{languages} dans n’importe quelle paire : apprenez le polonais via l’anglais, si vous voulez.",
    "intro_menu_settings": "langue, jeux de la leçon, rappels",
    "intro_menu_stats": "votre progression",
    "intro_menu_rating": "le classement du mois",
    "intro_menu_learn": "une leçon",
    "intro_menu_title": "Où trouver quoi :",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Objectif",
    "settings_goal_title": "<b>Pourquoi j’apprends</b>",
    "settings_goal_description": "Les mots de votre thème viendront en premier. La difficulté suit toujours votre niveau, et ce que vous avez appris revient en révision.",
    "settings_goal_set": "Objectif enregistré",
    "settings_goal_line": "Objectif : <b>{goal}</b>",
    "settings_goal_none": "non choisi",
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
    "match_title": "<b>Trouvez les paires</b>",
    "match_progress": "Associées : {matched} sur {total}",
    "match_errors": "✗ erreurs : {count}",
    "match_hint": "Touchez un mot d’un côté, puis sa paire de l’autre.",
    "match_wrong": "✗ Ce n’est pas une paire",
    "match_done": "<b>Plateau terminé !</b>",
    "match_done_counted": "Pris en compte dans la progression : {counted} sur {total}. Seules les paires trouvées du premier coup comptent, et jamais la dernière : à ce moment-là, il n’y a plus de choix.",
    "match_btn_again": "Encore un plateau",
    "match_not_ready": "Pas encore : un plateau demande {need} mots connus, et vous en avez {have}. Entraînez-vous avec les cartes « Je lis » — elles le débloquent.",
})

TEXTS["match_back_to_round"] = "Retour à la leçon."

TEXTS.update({
    "settings_btn_match": "Plateau dans la leçon",
    "settings_match_title": "<b>Plateau dans la leçon</b>",
    "settings_match_description": "Dans chaque leçon, à mi-parcours, un plateau remplace une question : cinq mots et cinq sens à associer. Il n’utilise que des mots connus, il apparaît donc dès que vous en avez au moins dix.",
    "match_state_on": "Le plateau est activé : il arrive au milieu de la leçon.",
    "settings_match_short_on": "avec plateau",
    "settings_channels_short_one": "« Je lis » seulement",
    "settings_channels_short_some": "{count} jeux sur {total}",
    "settings_channels_short_all": "tous les jeux",
    "plural_words": "mot|mots",
    "plural_points": "point|points",
    "plural_days": "jour|jours",
    "settings_audio_short_off": "sans son",
    "settings_audio_short_on": "avec son",
    "settings_match_short_off": "sans plateau",
    "match_state_off": "Le plateau est désactivé : la leçon ne contient que des questions.",
})

# ============================================================================
# СООБЩЕНИЯ ПО ИНИЦИАТИВЕ БОТА — патч 2.1 «Вовлечение» (`nudge_texts`).
# Голос и запрет значков — в ru.py; номера вариантов `_N` те же (тест).
# ============================================================================
TEXTS.update({
    "plural_lessons": "leçon|leçons",
    "nd_teaser_quiz_1": "Vous vous souvenez de ce que veut dire {word} ? {meaning}",
    "nd_teaser_quiz_2": "Testez-vous : {word} - {meaning}",
    "nd_teaser_quiz_3": "Un de vos mots : {word} - {meaning}",
    "nd_teaser_quiz_4": "Comment traduire {word} ? {meaning}",
    "nd_teaser_new_1": "Par exemple : {word} - {meaning}",
    "nd_teaser_new_2": "Premier mot : {word} - {meaning}",
    "nd_teaser_new_3": "Comment traduire {word} ? La traduction est cachée - touchez-la : {meaning}",
    "nd_streak_head_1": "<b>{name}, série : {days} d’affilée</b>",
    "nd_streak_head_2": "<b>{name}, {days} d’affilée. On continue ?</b>",
    "nd_streak_head_3": "<b>{name}, déjà {days} d’affilée</b>",
    "nd_streak_head_4": "<b>{name}, {days} sans interruption</b>",
    "nd_streak_head_5": "<b>{name}, encore une leçon, et ce sera {next_days} d’affilée</b>",
    "nd_streak_head_6": "<b>{name}, votre série vous attend : {days}</b>",
    "nd_streak_head_7": "<b>{days} d’affilée, {name}</b>",
    "nd_streak_head_8": "<b>{name}, {days} d’affilée. Encore une leçon aujourd’hui ?</b>",
    "nd_body_learned_1": "Mots familiers : {known_n} · appris : {learned}",
    "nd_body_learned_2": "Mots en cours : {in_work} · appris : {learned}",
    "nd_body_learned_3": "Vous connaissez déjà {known}, dont {learned} appris.",
    "nd_body_known_1": "Mots familiers : {known_n}. Chaque leçon en ajoute de nouveaux.",
    "nd_body_known_2": "Mots en cours : {in_work}. Les premiers mots appris sont tout proches.",
    "nd_body_known_3": "Vous connaissez déjà {known}.",
    "nd_streak_close_1": "Les petits pas mènent loin.",
    "nd_streak_close_2": "Un peu chaque jour : c’est ainsi que les mots se fixent.",
    "nd_streak_close_3": "Une leçon aujourd’hui prolongera la série.",
    "nd_streak_close_4": "Une leçon prend environ {minutes_n} minutes.",
    "nd_streak_close_5": "La régularité compte plus que la durée de la leçon.",
    "nd_progress_head_known": "<b>{name}, vous connaissez déjà {known}</b>",
    "nd_progress_head_1": "<b>{name}, vos mots attendent une révision</b>",
    "nd_progress_head_2": "<b>{name}, vous avez quelques minutes ?</b>",
    "nd_progress_head_3": "<b>{name}, on reprend là où vous en étiez ?</b>",
    "nd_progress_head_4": "<b>{name}, on retourne à vos mots ?</b>",
    "nd_progress_head_5": "<b>{name}, c’est le bon moment pour rafraîchir vos mots</b>",
    "nd_due_1": "Mots à réviser : {due_n}. Le bot suit lui-même le calendrier.",
    "nd_due_2": "Il est temps de réviser : {due}, avant l’oubli.",
    "nd_due_3": "Mots à réviser : {due_n}. Le bot a déjà choisi par où commencer.",
    "nd_due_many_1": "Pas mal de mots attendent : la leçon commencera par les plus importants.",
    "nd_due_many_2": "Les révisions se sont accumulées. Une leçon par jour suffit, le reste peut attendre.",
    "nd_praise_1": "Déjà {lessons} derrière vous. Petit à petit, mais régulièrement.",
    "nd_praise_2": "Leçons terminées : {lessons_n}. Les petits pas mènent loin.",
    "nd_praise_3": "{lessons} derrière vous, et chacune a ajouté des mots.",
    "nd_short_1": "Une leçon prend environ {minutes_n} minutes.",
    "nd_short_2": "Cela prend quelques minutes.",
    "nd_first_head_words": "<b>{name}, hier vous avez découvert {words}</b>",
    "nd_first_head_1": "<b>{name}, un bon début</b>",
    "nd_first_head_2": "<b>{name}, on vérifie les mots d’hier ?</b>",
    "nd_first_body_1": "Réviser le lendemain aide les mots à se fixer.",
    "nd_first_body_2": "Le deuxième jour est le meilleur moment pour ancrer les nouveaux mots.",
    "nd_first_close_1": "Cela prend quelques minutes.",
    "nd_first_close_2": "Une leçon prend environ {minutes_n} minutes.",
    "nd_kept_head_1": "<b>{name}, tout est à sa place</b>",
    "nd_kept_head_2": "<b>{name}, vos mots sont sauvegardés</b>",
    "nd_kept_head_3": "<b>{name}, cela fait un moment</b>",
    "nd_kept_body_1": "Mots familiers : {known_n} · appris : {learned}. Rien n’est perdu - la leçon commencera par ceux qu’il faut rafraîchir.",
    "nd_kept_body_2": "Tout ce que vous avez appris est sauvegardé. La leçon commencera par les mots à rafraîchir.",
    "nd_kept_body_3": "Tout le monde fait des pauses. Vous pouvez reprendre avec une courte leçon.",
    "nd_kept_best": "Meilleure série : {best} d’affilée. Une nouvelle commence par une seule leçon.",
    "nd_farewell_head_1": "<b>{name}, il n’y aura plus de rappels</b>",
    "nd_farewell_head_2": "<b>{name}, dernier rappel</b>",
    "nd_farewell_body_1": "Le bot ne vous écrira plus jusqu’à votre retour. Tout est sauvegardé : mots familiers {known_n}, appris {learned}. Vous pouvez reprendre à tout moment avec le bouton ci-dessous.",
    "nd_farewell_body_2": "Ce n’est visiblement pas le moment pour les leçons - ce n’est pas grave. Il n’y aura plus de rappels. Vos mots et votre progression sont sauvegardés.",
    "nd_start_head_1": "<b>{name}, vos premiers mots vous attendent</b>",
    "nd_start_head_2": "<b>{name}, on commence ?</b>",
    "nd_start_head_3": "<b>{name}, la première leçon prend environ {minutes_n} minutes</b>",
    "nd_start_body_1": "Le bot choisira les mots les plus utiles pour votre niveau et saura quand les réviser.",
    "nd_start_body_2": "Nous commençons par les mots les plus courants, ceux qu’on entend tous les jours.",
    "nd_start_body_3": "Aucune préparation : {questions} questions, puis le bot vous dira quoi réviser et quand.",
    "nd_start3_head_1": "<b>{name}, vous essayez ?</b>",
    "nd_start3_head_2": "<b>{name}, vos premiers mots vous attendent toujours</b>",
    "nd_start_last_head": "<b>{name}, dernière invitation</b>",
    "nd_start_last_body": "Il n’y aura plus de rappels. Si vous voulez commencer, la première leçon prend environ {minutes_n} minutes - le bouton est ci-dessous.",
    "nd_btn_optin": "Me le rappeler à {time}",
    "nd_btn_stop": "Ne plus envoyer",
    "nd_auto_time": "Je vous enverrai un rappel chaque jour à {time}. Vous pouvez changer l’heure",
    "nd_btn_change_time": "Changer l’heure",
    "nd_optin_done": "✓ C’est fait : le rappel arrivera à <b>{time}</b>\n\nVous pouvez changer l’heure dans les réglages",
})
