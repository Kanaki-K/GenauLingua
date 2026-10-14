"""
English localization for GenauLingua Bot
"""

TEXTS = {
    # ============================================================================
    # MAIN MENU BUTTONS
    # ============================================================================
    "btn_learn_words": "Learn words",
    "btn_stats": "Statistics",
    "btn_settings": "Settings",
    "btn_help": "Help",
    "btn_back": "Back",
    "menu_placeholder": "Choose an action...",

    # ============================================================================
    # WELCOME & START
    # ============================================================================
    "welcome_title": "<b>Hello, {name}!</b>",








    # ============================================================================
    # NOTIFICATIONS
    # ============================================================================
    "notif_title": "<b>Notification Settings</b>",
    "notif_status": "Status: {status}",
    "notif_status_on": "Enabled",
    "notif_status_off": "Disabled",
    "notif_time": "Time: {time}",
    "notif_days": "Days: {days}",
    "notif_timezone": "Timezone: {timezone}",
    "notif_hint": "Notifications will arrive at the specified time in your timezone.",
    "notif_hint_off": "Enable notifications to never forget your daily practice!",

    "notif_btn_toggle_on": "Notifications: Enabled",
    "notif_btn_toggle_off": "Notifications: Disabled",
    "notif_btn_time": "Time: {time}",
    "notif_btn_days": "Select days",
    "notif_btn_timezone": "Change timezone",

    "notif_timezone_title": "<b>Select your timezone</b>",
    "notif_timezone_current": "Current: {timezone}",
    "notif_timezone_prompt": "Select a city in your timezone:",
    "notif_timezone_more": "Select another city",
    "notif_timezone_back": "Back",
    "notif_timezone_set": "✓ Timezone set: {city}",

    "notif_time_title": "<b>Select notification time</b>",
    "notif_time_current": "Current time: {time}",
    "notif_time_timezone": "Timezone: {timezone}",
    "notif_time_hint": "Notification will arrive daily at the selected time.",
    "notif_time_set": "✓ Time set: {time}",

    "notif_days_title": "<b>Select notification days</b>",
    "notif_days_hint": "Tap on a day to enable/disable it.\n✓ Green check - day enabled\n✗ Red cross - day disabled\n\nWhen done - tap 'Save'.",
    "notif_days_all": "All days",
    "notif_days_weekdays": "Weekdays (Mon-Fri)",
    "notif_days_save": "Save",
    "notif_days_saved": "✓ Days saved!",
    "notif_days_all_selected": "✓ All days selected",
    "notif_days_weekdays_selected": "✓ Weekdays selected (Mon-Fri)",
    "notif_days_none": "Select at least one day for notifications!",

    "notif_toggle_on": "Notifications enabled!",
    "notif_toggle_off": "Notifications disabled",

    "notif_message_btn_disable": "Disable notifications",

    "day_mon": "Mon",
    "day_tue": "Tue",
    "day_wed": "Wed",
    "day_thu": "Thu",
    "day_fri": "Fri",
    "day_sat": "Sat",
    "day_sun": "Sun",

    "notif_btn_back": "Back to settings",

    "notif_default_name": "friend",

    "anchor_streak": "🔥 {days}",
    "notif_message_greeting": "<b>Time to practice, {name}!</b>",


    # ONE REASON TO COME BACK — and it has to be true
    "remind_streak_risk": "{days} days in a row · not today yet",
    "remind_due": "{count} words are due for review — the bot tracks the timing",
    "remind_due_many": "Quite a lot is due. Start with one round, the rest can wait.",
    "remind_streak_lost": "Your best streak was {days} days. A new one starts with a single round.",
    "remind_milestone_close": "Words in progress: {count} · {left} to go until {target}, that is one round",
    "remind_almost_learned": "One correct answer away from your first learned word. Such words: {count}",
    "remind_rank": "Place {rank} of {total} in your language",
    "remind_fact_1": "A word sticks when it comes back: a day, three days, a week. The bot keeps the schedule.",
    "remind_fact_2": "An answer by ear is worth more: there is no written shape to lean on.",
    "remind_fact_3": "Saying a word out loud is harder than recognising it — and worth three times as much.",
    "remind_fact_4": "Fifteen words take four minutes. Less than a queue for coffee.",

    # ============================================================================
    # SETTINGS
    # ============================================================================
    "settings_title": "<b>Settings</b>",
    "settings_mode": "Direction: <b>{mode}</b>",
    "settings_language": "Bot language: <b>{language}</b>",

    "settings_btn_quiz_mode": "Level and topics",
    "settings_btn_change_language": "Interface language",
    "settings_btn_notifications": "Notifications",

    "settings_quiz_mode_line": "Level: <b>{mode}</b>",


    "settings_language_title": "<b>Interface language</b>",
    "settings_language_description": "Choose the bot interface language:",
    "start_pick_language": "Choose a language",

    "language_changed": "✓ Language changed to {language}",
    "user_not_found": "✗ User not found. Use /start",

    "lang_ru": "Русский",
    "lang_uk": "Українська",
    "lang_en": "English",
    "lang_tr": "Türkçe",
    "lang_de": "Deutsch",
    "lang_pl": "Polski",



    # ============================================================================
    # QUIZ MODE (NEW)
    # ============================================================================
    "qmode_title": "<b>Quiz mode</b>",
    "qmode_current": "Current: <b>{mode}</b>",
    "qmode_choose": "Choose how you want to learn\nYou can switch anytime — your progress is saved",

    "qmode_btn_level": "By level",
    "qmode_btn_category": "Category",
    "qmode_btn_all": "Top 10 thousand",
    "qmode_btn_difficult": "Difficult",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Top 10 thousand",
    "qmode_difficult_short": "Difficult words",

    "qmode_level_title": "<b>Choose level</b>",
    "qmode_level_desc": "From your first «Hallo» to fluent debates\nAll levels available — pick yours!\n\n• A1–A2 — basic vocabulary\n• B1–B2 — confident communication\n• C1–C2 — near-native fluency",
    "qmode_level_set": "✓ Mode: By level ({level})",

    "qmode_category_title": "<b>Choose category</b>",
    "qmode_category_desc": "From food to science — pick the topic you need\n\nEach category includes words from all levels",
    "qmode_category_set": "✓ Mode: {category}",

    # Category names
    "cat_arbeit_beruf": "Work",
    "cat_bildung_lernen": "Education",
    "cat_einkaufen_geld": "Shopping",
    "cat_emotionen_charakter": "Emotions",
    "cat_essen_trinken": "Food",
    "cat_freizeit_sport": "Sports",
    "cat_gesundheit_medizin": "Health",
    "cat_grammatik": "Grammar",
    "cat_kleidung_mode": "Fashion",
    "cat_kommunikation": "Communication",
    "cat_kultur_kunst": "Culture",
    "cat_mensch_familie": "Family",
    "cat_natur_wetter": "Nature",
    "cat_recht_staat": "Law",
    "cat_reisen_transport": "Travel",
    "cat_technik_digital": "Technology",
    "cat_wirtschaft": "Economy",
    "cat_wissenschaft": "Science",
    "cat_wohnen_haus": "Housing",
    "cat_zeit_alltag": "Daily life",

    "qmode_all_set": "✓ Mode: Top 10 thousand",

    "qmode_difficult_set": "✓ Mode: Difficult words",
    "qmode_difficult_few": "You only have {count} difficult words — need at least 4\nTake a few more quizzes!",
    "qmode_difficult_empty": "You don't have difficult words yet.\nTake a few quizzes first!",

    "quiz_btn_change_mode": "Level and topics",
    "quiz_btn_report_error": "Translation error",
    "report_btn_confirm": "✓ Confirm ({count})",
    "report_btn_send": "Send",
    "report_no_words": "No words to report",
    "report_none_selected": "Select at least one word",
    "report_pick_kind": "{count} word(s) selected. Now say what is wrong — the translation or the pronunciation.",
    "report_sent": "✓ Sent {count} reports — thank you!\nIf confirmed — you'll get +{points} points",
    "report_daily_limit": "Daily report limit reached (max 20)",
    "report_all_reported": "✓ All words from this quiz already reported",
    "report_already_sent": "✓ Already reported",
    "report_btn_kind_text": "Wrong translation",
    "report_btn_kind_audio": "Wrong pronunciation",
    "report_sent_audio": "✓ Sent {count} — thank you!\nPronunciation reports are especially valuable: the automated check cannot hear stress\nIf confirmed — +{points} points",
    "report_approved": "✓ Your report was accepted: <b>{word}</b> is fixed.\n+{points} points to your monthly score — thanks, the dictionary got better for everyone.",
    "report_approved_audio": "✓ Your pronunciation report was accepted: <b>{word}</b>.\nThe audio will be re-recorded. +{points} points to your monthly score — thank you.",

    # ============================================================================
    # QUIZ
    # ============================================================================
    "quiz_no_level": "First choose your level using /start",
    "quiz_error_generation": "✗ An error occurred while preparing the quiz.\nTry again via /start",
    "quiz_no_words": "✗ Sorry, no words available for this level.\nTry choosing a different level.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Correct</b>",
    "quiz_wrong": "✗ <b>Wrong</b>",
    "quiz_correct_answer": "Correct answer:",

    "quiz_btn_next": "Next →",
    "quiz_btn_repeat_errors": "Repeat mistakes",

    "quiz_completed": "<b>Round done</b>",
    "quiz_result_correct": "Correct: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Result: <b>{percentage}%</b>",
    "quiz_result_details": "<b>Details:</b>",
    "quiz_result_errors": "Mistakes: {count}",

    # PRAISE AT THE END OF A ROUND — only for what actually happened
    "praise_first_round": "First round done. From here words start coming back — that is how they stick.",
    "praise_first_learned": "First word learned: three correct answers in a row, and not met today.",
    "praise_learned": "Words learned this round: {count}",
    "praise_best_streak": "Personal best: {days} days in a row",
    "praise_milestone": "Milestone {count} reached",
    "praise_first_speech": "First correct answer by voice",
    "praise_first_audio": "First correct answer by ear",
    "praise_comeback": "Welcome back. You were away {days} days.",
    "praise_perfect": "Round without a single mistake",
    "praise_streak": "Streak: {days} days in a row",
    "praise_new_words": "New words: {count}",
    "praise_returned": "Recognised again: {count}",
    "praise_progress": "Words in progress: {count} · {left} to go until {target}",
    "praise_progress_top": "Words in progress: {count}",
    "praise_points": "Points: +{points}",

    "quiz_repeat_title": "<b>Repeat mistakes</b>",
    "quiz_no_errors": "✓ You had no mistakes!",
    "quiz_error_next": "✗ Failed to load next question.",
    "quiz_error_generate": "✗ Failed to generate next question.",

    # ============================================================================
    # STATISTICS
    # ============================================================================
    "stats_no_level": "<b>Choose your level first!</b>\n\nUse /start to begin.",





    # ============================================================================
    # HELP
    # ============================================================================
    "help_title": "<b>Help — GenauLingua</b>",
    "help_description": "Here you'll find instructions, upcoming features and how to reach the community.",
    "help_choose": "Choose a section:",

    "help_btn_how_to_use": "How to use",
    "help_btn_community": "Community",

    "help_how_to_use_title": "<b>How to use the bot</b>",
    "help_how_to_use_text": """1 <b>Pick the language you want to learn</b>
Settings → Language to learn: {languages}.
Same screen: level A1–C2, translation direction and interface language.
Progress is tracked separately per language, so you can learn two at once.

2 <b>Choose quiz mode</b>
Settings → Quiz mode:
• By level — words from your level
• By category — 20 topics: food, work, travel...
• Top 10 thousand — entire word base
• Difficult — words you often get wrong

3 <b>Learn words every day</b>
Learn words → quiz with 25 words.
The bot remembers your mistakes and shows difficult words more often.

4 <b>Repeat your mistakes</b>
After the quiz you can immediately repeat the words you got wrong.

5 <b>Track your progress</b>
Statistics → how many learned, quiz history, streak.

6 <b>Compete with others</b>
My rating → your monthly and all-time points.
Leaderboard → top-10 among all participants.

7 <b>Set up reminders</b>
Settings → Notifications → choose time, days and timezone.

<b>Audio</b>
Words are spoken by a native voice: the question plays the word alone, the answer plays it together with the example. You hear both the pronunciation and how the word sits in real speech.
Settings → Audio: turn it off or pick a voice. German has three male and three female voices, and tapping one plays it right away.
In the reverse direction the sound comes after your answer — otherwise the spoken word would be the answer.


A word is <b>learned</b> when you answer correctly 3 times in a row.
<b>Streak</b> grows if you complete at least 1 quiz per day.
Found a mistake? Tap the button after the quiz and say what is wrong — the translation or the pronunciation. Pronunciation reports matter most: a machine cannot hear stress.

Questions? → t.me/genaulingua_chat""",


    "help_community_title": "<b>GenauLingua Community</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

In the chat:
Be the first to know about updates
Found a bug — write or send a screenshot
Translation error — report it, we'll fix it
Ideas and suggestions — we read everything
Chat with other learners


The more active the community — the better the bot gets. Don't be shy! """,


    # ============================================================================
    # RATING
    # ============================================================================
    "rating_title_monthly": "<b>My rating — {month} {year}</b>",
    "rating_not_active": "✗ Rating is not active yet.",
    "rating_not_in_ranking": "You're not in the ranking yet",
    "rating_start_quiz": "Take your first quiz!",
    "rating_position": "Position: <b>#{rank}</b> of {total}",
    "rating_points": "Points: <b>{score}</b>",
    "rating_title_polyglot": "polyglot",
    "rating_title_professor": "professor",
    "rating_title_expert": "expert",
    "rating_title_student": "student",
    "rating_your_month": "<b>Your {month}:</b>",
    "rating_quizzes": "Quizzes: {count}",
    "rating_words_learned": "Words learned: {count}",
    "rating_streak": "Streak: {count} days",
    "rating_avg_result": "Average result: {percent}%",
    "rating_scoring_title": "<b>How to earn points:</b>",
    "rating_scoring_quiz": "• Completed quiz → +10",
    "rating_scoring_reverse": "• Reverse mode → +5",
    "rating_scoring_word": "• Word learned → +2",
    "rating_scoring_streak": "• Day streak → +3",
    "rating_scoring_bonus": "• 90%+ accuracy → +50 bonus",
    "rating_scoring_report": "• Confirmed report → +1",

    "rating_title_alltime": "<b>My rating — All Time</b>",
    "rating_position_alltime": "Position: <b>#{rank}</b>",
    "rating_position_none": "Position: <b>—</b>",
    "rating_achievements": "<b>Your achievements:</b>",
    "rating_wins": "Wins (1st place): {count}",
    "rating_total_words": "Words learned: {count}",
    "rating_motivation_start": "Start learning — the first step is the most important!",
    "rating_motivation_continue": "Keep going — your first win is near!",
    "rating_motivation_champion": "You're a true champion!",

    "table_title_monthly": "<b>Leaderboard — {month} {year}</b>",
    "table_title_alltime": "<b>Leaderboard — All Time</b>",
    "table_empty": "No participants yet.\nBe the first to take a quiz!",
    "table_you_in_top": "You: <b>#{rank}</b> of {total}",
    "table_you_not_in_top": "You: <b>#{rank}</b> of {total} — {score} points",
    "table_you_outside": "You: outside top-10 — {score} points",
    "table_you_not_ranked": "You're not ranked yet",
    "table_points": "points",
    "btn_leaderboard_table": "Leaderboard",
    "btn_back_to_rating": "Back to rating",

    "stats_header": "<b>Your statistics</b>",
    "stats_in_work_line": "Words in progress: {count} · {left} to go until {target}",
    "stats_in_work_top": "Words in progress: {count}",
    "stats_details": "In progress: {progress}\nNew: {new}\nDifficult: {difficult}",
    "stats_achievements_title": "<b>Your achievements</b>",
    "stats_words_count": "Words learned: <b>{count}</b>",
    "stats_streak_line": "Streak: {days} days in a row",
    "stats_best_streak_line": "Best streak: {days} days",
    "stats_quizzes_header": "<b>Quizzes · {level}</b>",
    "stats_quizzes_passed_line": "Completed: <b>{count}</b>",
    "stats_quizzes_avg_line": "Average result: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Best result: <b>{percent}%</b>",
    "stats_quizzes_empty": "No quizzes completed yet",
    "stats_recent_header": "<b>Recent quizzes</b>",
    "stats_overall_header": "<b>Overall progress</b>",
    "stats_overall_learned": "Learned <b>{learned}</b> of {total} words",
    "stats_explanation": "A word is learned = three correct answers in a row, on different days",
}

# ============================================================================
# MULTILINGUAL: learning language, meaning language and direction
# ============================================================================
TEXTS.update({
    "langname_de": "German",
    "langname_en": "English",
    "langname_ru": "Russian",
    "langname_uk": "Ukrainian",
    "langname_tr": "Turkish",
    "langname_pl": "Polish",
    # Союз для перечисления языков в текстах помощи и приветствия
    "and_word": "and",

    "settings_learning_lang_line": "Learning: <b>{language}</b>",

    "settings_btn_learning_lang": "Language",

    "learning_lang_title": "<b>Language to learn</b>",
    "learning_lang_description": "Pick the language whose words you want to learn.\nProgress is tracked separately for each language.",
    "learning_lang_set": "✓ Learning: {language}",
    # Settings line and the audio screen
    "settings_audio_line": "Audio: <b>{state}</b>",
    "settings_btn_audio": "Audio",
    "audio_state_on": "on",
    "audio_state_off": "off",

    "audio_title": "<b>Audio</b>",
    "audio_description": "Words are spoken by a native voice. The question plays the word alone, the answer plays it with the example.",
    "audio_current_voice": "Voice: <b>{voice}</b>",
    "audio_btn_turn_on": "Turn audio on",
    "audio_btn_turn_off": "Turn audio off",
    "audio_btn_choose_voice": "Choose a voice",
    "audio_turned_on": "✓ Audio is on",
    "audio_turned_off": "Audio is off",

    "voice_title": "<b>Choose a voice</b>",
    "voice_description": "Tap a voice to hear it. The checkmark shows the current one.",
    "voice_male": "Male",
    "voice_female": "Female",
    "voice_set": "✓ Voice: {voice}",
    "voice_use": "Use {voice}",
    "voice_listening": "Playing {voice}",
    "voice_only_one": "For this language the engine has one male and one female voice — no more exist.",
    "voice_preview_failed": "Could not get a sample, try again",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Rating",
    "friend_fallback": "friend",
    "onboarding_learning_title": "<b>Which language will you learn?</b>",
    "onboarding_learning_desc": "Meanings will be shown in {native}\nYou can change the language and direction in settings at any time.",
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
    "help_how_to_use_text": "<b>Quiz</b>\n25 words, four options. The bot remembers your mistakes and brings hard words back more often. After a quiz you can replay the ones you missed.\n\n<b>Audio</b>\nThe question plays the word; after your answer you hear the word with its example. Pick a male or female voice in settings.\n\n<b>Languages</b>\n{languages} — in any pair, both directions. Progress and rating are tracked separately for each language.\n\n\nA word counts as <b>learned</b> after three correct answers in a row, on different days.\nYour <b>streak</b> grows with any quiz that day.\nWrong translation or pronunciation — use the button under the quiz.",
    "help_community_title": "<b>About the bot and the community</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} languages in any pair: {languages}\n12,900 words A1–C2, each with an example and native audio.\nInterface: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nBugs, translation errors, ideas — we read everything. Reports about pronunciation are especially welcome: a machine cannot hear stress.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Listen and pick what you heard:",
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
    "rating_scoring_answer": "• Correct answer → +1, by ear → +2, out loud → +3",
    "rating_scoring_quiz": "• Round finished → +10",
    "rating_scoring_reverse": "• Reverse direction → +5",
    "rating_scoring_word": "• Word learned → +3",
    "rating_scoring_streak": "• Each day in a row is worth more, up to +10",
    "rating_scoring_bonus": "• Accuracy above 60% — the higher, the more",
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
    "quiz_result_by_ear": "🎧 By ear: {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "Lesson mix",
    "settings_channels_line": "Lesson: <b>{channels}</b>",
    "channels_title": "<b>Lesson mix</b>",
    "channels_description": "Which questions to ask. The more channels, the better a word sticks: recognising it by sight, by ear and saying it are three different skills.",
    "channel_text": "📖 Card",
    "channel_audio": "🎧 Listening",
    "channel_speech": "🎤 Speaking",
    "quiz_result_recalled": "← Recalled: {count}",
    "home_scale_reverse": "I recall",
    "channel_reverse": "💭 Recall the word",
    "channels_text_always": "Cards cannot be switched off: a lesson with no channel is an empty screen.",
    "channels_audio_blocked": "🎧 By ear is unavailable: audio is switched off.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Say this word out loud — record a voice message",
    "speech_btn_reference": "Listen",
    "speech_btn_skip": "Skip",
    "speech_listening": "🎧 Listening…",
    "speech_not_understood": "Could not make it out. Record again — closer to the mic and a bit louder.",
    "speech_send_voice": "🎤 This question is answered with a voice message. Press and hold the microphone button.",
    "speech_skipped": "Skipped",
    "quiz_result_spoken": "🎤 Spoken: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "I read",
    "home_scale_audio": "I listen",
    "home_scale_speech": "I speak",
    "home_btn_learn": "Learn words",
    "home_streak": "streak {days} days",
    "home_rank": "rank {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: not yet. Only {ready} words are ready, at least {minimum} are needed. Practise with cards — they unlock the other channels.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "What I learn",
    "settings_group_what_title": "<b>What I learn</b>",
    "settings_group_how": "How I learn",
    "settings_group_how_title": "<b>How I learn</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Language, level and translation direction.",
    "settings_group_how_about": "What a round is made of and how it sounds.",
    "settings_group_bot_about": "Bot language, reminders and help.",
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
    "quiz_btn_one_more": "One more round",
    "home_btn_stats": "More details",
    "notif_off_how_to_return": "To turn it back on: Settings → Bot → Reminders",
    "reminder_offer": "Remind you once a day? It is easier not to lose what you have learnt — and the streak holds.",
    "reminder_offer_yes": "Yes, remind me",
    "reminder_offer_no": "No thanks",
    "reminder_offer_done": "Done. Time and days can be changed in settings.",
    "level_offer": "You hardly ever get <b>{current}</b> wrong. Move up to <b>{following}</b>? Everything you have learnt stays with you.",
    "level_offer_yes": "Yes, move to {following}",
    "level_offer_no": "Stay here",
    "level_offer_done": "Level <b>{following}</b>. The words will be harder now.",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "What do you need the language for? We will pick words to match.",
    "goal_work": "For work",
    "goal_travel": "For travel",
    "goal_living": "For living abroad",
    "goal_study": "For studying",
    "goal_any": "Just learn words",
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
    "intro_games": "A word is learned four ways here: read it, recall it from the meaning, hear it, say it out loud.\nThe lesson mixes them on its own.",
    "intro_numbers": "12,902 words · 20 topics · 6 levels\nSix languages in any pair: learn Polish through English if you like.",
    "intro_menu_settings": "language, round contents, reminders",
    "intro_menu_stats": "your progress",
    "intro_menu_rating": "this month's standings",
    "intro_menu_learn": "a round",
    "intro_menu_title": "What is where:",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Goal",
    "settings_goal_title": "<b>What I need it for</b>",
    "settings_goal_description": "Words from your topic will come first. Difficulty still follows your level, and what you have learnt keeps coming back for review.",
    "settings_goal_set": "Goal saved",
    "settings_goal_line": "Goal: <b>{goal}</b>",
    "settings_goal_none": "not chosen",
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
    "match_title": "<b>Find the pairs</b>",
    "match_progress": "Matched: {matched} of {total}",
    "match_errors": "✗ misses: {count}",
    "match_hint": "Tap a word on either side, then its pair on the other.",
    "match_wrong": "✗ Not a pair",
    "match_done": "<b>Board cleared!</b>",
    "match_done_counted": "Counted towards progress: {counted} of {total} — only pairs matched on the first try, and never the last one, which comes with no choice left.",
    "match_btn_again": "One more board",
    "match_not_ready": "Not yet: a board needs {need} familiar words and you have {have}. Practise with cards — they unlock it.",
})

TEXTS["match_back_to_round"] = "Back to the round."

TEXTS.update({
    "settings_btn_match": "Board in the round",
    "settings_match_title": "<b>Board in the round</b>",
    "settings_match_description": "Every other lesson, the middle of the round brings a board instead of five questions: five words and five meanings to pair up. Only familiar words are used.",
    "match_state_on": "Board is on: it will come mid-round.",
    "settings_match_short_on": "with the board",
    "settings_channels_short_one": "cards only",
    "settings_channels_short_two": "two ways",
    "settings_channels_short_all": "all three ways",
    "settings_audio_short_off": "no sound",
    "settings_audio_short_on": "with sound",
    "settings_match_short_off": "no board",
    "match_state_off": "Board is off: the round is questions only.",
})
