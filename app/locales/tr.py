"""
Türkçe lokalizasyon - GenauLingua Bot
"""

TEXTS = {
    # ============================================================================
    # ANA MENÜ BUTONLARI
    # ============================================================================
    "btn_learn_words": "Kelime öğren",
    "btn_stats": "İstatistik",
    "btn_settings": "Ayarlar",
    "btn_help": "Yardım",
    "btn_back": "Geri",
    "menu_placeholder": "Bir eylem seçin...",

    # ============================================================================
    # KARŞILAMA VE BAŞLANGIÇ
    # ============================================================================
    "welcome_title": "<b>Merhaba, {name}!</b>",








    # ============================================================================
    # HATIRLATICILAR
    # ============================================================================
    "notif_title": "<b>Hatırlatıcı Ayarları</b>",
    "notif_status": "Durum: {status}",
    "notif_status_on": "Açık",
    "notif_status_off": "Kapalı",
    "notif_time": "Saat: {time}",
    "notif_days": "Günler: {days}",
    "notif_timezone": "Saat dilimi: {timezone}",
    "notif_hint": "Hatırlatıcı, seçtiğiniz günlerde ve saatte, kendi saat diliminize göre gelir.",
    "notif_hint_off": "Hatırlatıcıları açın — serinizi korumak daha kolay olur.",

    "notif_btn_toggle_on": "Hatırlatıcılar: Açık",
    "notif_btn_toggle_off": "Hatırlatıcılar: Kapalı",
    "notif_btn_time": "Saat: {time}",
    "notif_btn_days": "Günleri seç",
    "notif_btn_timezone": "Saat dilimini değiştir",

    "notif_timezone_title": "<b>Saat diliminiz</b>",
    "notif_timezone_current": "Şu anki: {timezone}",
    "notif_timezone_prompt": "Saat diliminizden bir şehir seçin:",
    "notif_timezone_more": "Başka şehir seç",
    "notif_timezone_back": "Geri",
    "notif_timezone_set": "✓ Saat dilimi ayarlandı: {city}",

    "notif_time_title": "<b>Hatırlatıcı saati</b>",
    "notif_time_current": "Şu anki saat: {time}",
    "notif_time_timezone": "Saat dilimi: {timezone}",
    "notif_time_hint": "Hatırlatıcı her gün seçtiğiniz saatte gelir.",
    "notif_time_set": "✓ Saat ayarlandı: {time}",

    "notif_days_title": "<b>Hatırlatıcı günleri</b>",
    "notif_days_hint": "Bir günü açmak ya da kapatmak için ona dokunun.\n✓ — gün açık\n✗ — gün kapalı\n\nBitirince «Kaydet» düğmesine dokunun.",
    "notif_days_all": "Tüm günler",
    "notif_days_weekdays": "Hafta içi (Pzt-Cum)",
    "notif_days_save": "Kaydet",
    "notif_days_saved": "✓ Günler kaydedildi!",
    "notif_days_all_selected": "✓ Tüm günler seçildi",
    "notif_days_weekdays_selected": "✓ Hafta içi seçildi (Pzt-Cum)",
    "notif_days_none": "En az bir gün seçin.",

    "notif_toggle_on": "Hatırlatıcılar açıldı!",
    "notif_toggle_off": "Hatırlatıcılar kapatıldı",

    "notif_message_btn_disable": "Hatırlatıcıları kapat",

    "day_mon": "Pzt",
    "day_tue": "Sal",
    "day_wed": "Çar",
    "day_thu": "Per",
    "day_fri": "Cum",
    "day_sat": "Cmt",
    "day_sun": "Paz",

    "notif_btn_back": "Ayarlara geri dön",

    "notif_default_name": "arkadaş",

    "anchor_streak": "🔥 {days}",
    "notif_message_greeting": "<b>Çalışma zamanı, {name}!</b>",


    # GERİ DÖNMEK İÇİN TEK NEDEN — ve doğru olmalı
    "remind_streak_risk": "{days_word} üst üste · bugün henüz ders yok",
    "remind_due": "{count} kelimenin tekrar zamanı geldi — süreleri bot kendi tutuyor",
    "remind_due_many": "Tekrar edilecek çok şey birikti. Bir dersle başlayın, gerisi bekler.",
    "remind_streak_lost": "En iyi seriniz {days_word}dü. Yenisi tek bir dersle başlar.",
    "remind_milestone_close": "Üzerinde çalıştığınız kelime: {count} · {target} kelimeye {left} kaldı — yani bir ders",
    "remind_almost_learned": "İlk öğrenilen kelimeye bir doğru yanıt kaldı. Böyle kelime sayısı: {count}",
    "remind_rank": "Bu dilin sıralamasında {total} kişi arasında {rank}. sıradasınız",
    "remind_fact_1": "Kelime geri döndüğünde akılda kalır: bir gün, üç gün, bir hafta. Süreyi bot tutar.",
    "remind_fact_2": "Kulakla verilen yanıt daha değerli: dayanacak yazılı bir biçim yok.",
    "remind_fact_3": "Sesli söylemek tanımaktan zordur — ve üç kat değerlidir.",
    "remind_fact_4": "On beş soru dört dakika sürer — kahve kuyruğundan kısa.",

    # ============================================================================
    # AYARLAR
    # ============================================================================
    "settings_title": "<b>Ayarlar</b>",
    "settings_mode": "Yön: <b>{mode}</b>",
    "settings_language": "Bot dili: <b>{language}</b>",

    "settings_btn_quiz_mode": "Seviye ve konular",
    "settings_btn_change_language": "Arayüz dili",
    "settings_btn_notifications": "Hatırlatıcılar",

    "settings_quiz_mode_line": "Seviye: <b>{mode}</b>",


    "settings_language_title": "<b>Arayüz dili</b>",
    "settings_language_description": "Bot arayüz dilini seçin:",
    "start_pick_language": "Dil seçin",

    "language_changed": "✓ Dil {language} olarak değiştirildi",
    "user_not_found": "✗ Kullanıcı bulunamadı. /start kullanın",

    "lang_ru": "Русский",
    "lang_uk": "Українська",
    "lang_en": "English",
    "lang_tr": "Türkçe",
    "lang_de": "Deutsch",
    "lang_pl": "Polski",



    # ============================================================================
    # TEST MODU (YENİ)
    # ============================================================================
    "qmode_title": "<b>Seviye ve konular</b>",
    "qmode_current": "Şu an: <b>{mode}</b>",
    "qmode_choose": "Nasıl öğrenmek istediğinizi seçin\nİstediğiniz zaman değiştirebilirsiniz — ilerlemeniz kaybolmaz",

    "qmode_btn_level": "Seviyeye göre",
    "qmode_btn_category": "Konuya göre",
    "qmode_btn_all": "Tüm kelimeler",
    "qmode_btn_difficult": "Zor",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Tüm kelimeler",
    "qmode_difficult_short": "Zor kelimeler",

    "qmode_level_title": "<b>Seviye seçin</b>",
    "qmode_level_desc": "İlk kelimelerden akıcı sohbetlere. Tüm seviyeler açık — kendinizinkini seçin.\n\n• A1–A2 — temel kelimeler\n• B1–B2 — güvenli iletişim\n• C1–C2 — akıcı kullanım",
    "qmode_level_set": "✓ Mod: Seviyeye göre ({level})",

    "qmode_category_title": "<b>Konu seçin</b>",
    "qmode_category_desc": "Yemekten bilime — ihtiyacınız olan konuyu seçin\n\nHer konuda tüm seviyelerin kelimeleri var",
    "qmode_category_set": "✓ Konu: {category}",

    # Kategori adları
    "cat_arbeit_beruf": "İş",
    "cat_bildung_lernen": "Eğitim",
    "cat_einkaufen_geld": "Alışveriş",
    "cat_emotionen_charakter": "Duygular",
    "cat_essen_trinken": "Yemek",
    "cat_freizeit_sport": "Spor",
    "cat_gesundheit_medizin": "Sağlık",
    "cat_grammatik": "Dilbilgisi",
    "cat_kleidung_mode": "Moda",
    "cat_kommunikation": "İletişim",
    "cat_kultur_kunst": "Kültür",
    "cat_mensch_familie": "Aile",
    "cat_natur_wetter": "Doğa",
    "cat_recht_staat": "Hukuk",
    "cat_reisen_transport": "Seyahat",
    "cat_technik_digital": "Teknoloji",
    "cat_wirtschaft": "Ekonomi",
    "cat_wissenschaft": "Bilim",
    "cat_wohnen_haus": "Konut",
    "cat_zeit_alltag": "Günlük",

    "qmode_all_set": "✓ Mod: Tüm kelimeler",

    "qmode_difficult_set": "✓ Mod: Zor kelimeler",
    "qmode_difficult_few": "Şimdilik zor kelime: {count} — en az 4 gerekiyor.\nBirkaç ders daha yapın!",
    "qmode_difficult_empty": "Henüz zor kelimeniz yok.\nÖnce birkaç ders yapın!",

    "quiz_btn_change_mode": "Seviye ve konular",
    "quiz_btn_report_error": "Hata bildir",
    "report_btn_confirm": "✓ Onayla ({count})",
    "report_btn_send": "Gönder",
    "report_no_words": "Bildirilecek kelime yok",
    "report_none_selected": "En az bir kelime seçin",
    "report_pick_kind": "{count} kelime seçildi. Şimdi neyin yanlış olduğunu seçin: çeviri mi, telaffuz mu?",
    "report_sent": "✓ Gönderilen bildirim: {count} — teşekkürler!\nHata onaylanırsa +{points} puan kazanırsınız.",
    "report_daily_limit": "Bugünkü bildirim sınırı doldu (en fazla 20)",
    "report_all_reported": "✓ Bu dersteki tüm kelimeler zaten bildirildi",
    "report_already_sent": "✓ Zaten bildirildi",
    "report_btn_kind_text": "Hatalı çeviri",
    "report_btn_kind_audio": "Hatalı telaffuz",
    "report_sent_audio": "✓ Gönderilen bildirim: {count} — teşekkürler!\nTelaffuz bildirimleri özellikle değerli: otomatik kontrol vurguyu duymaz.\nOnaylanırsa +{points} puan.",
    "report_approved": "✓ <b>{word}</b> için bildiriminiz kabul edildi — çeviriyi düzelteceğiz.\nAylık puanınıza +{points} puan eklendi — teşekkürler, sözlük herkes için daha iyi olacak.",
    "award_won": "{mark} {month} sıralamasında {rank}. oldunuz.\nTüm zamanlar puanınıza +{bonus} puan eklendi.",
    "report_approved_audio": "✓ Telaffuz bildiriminiz kabul edildi: <b>{word}</b>.\nKelime yeniden seslendirilecek. Aylık puanınıza +{points} puan eklendi — teşekkürler.",

    # ============================================================================
    # TEST
    # ============================================================================
    "quiz_no_level": "Önce /start ile seviyenizi seçin",
    "quiz_error_generation": "✗ Ders hazırlanırken bir hata oluştu.\n/start ile tekrar deneyin",
    "quiz_no_words": "✗ Üzgünüz, bu seviye için henüz kelime yok.\nBaşka bir seviye seçmeyi deneyin.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Doğru</b>",
    "quiz_wrong": "✗ <b>Yanlış</b>",
    "quiz_correct_answer": "Doğru cevap:",

    "quiz_btn_next": "İleri →",
    "quiz_btn_repeat_errors": "Hataları tekrarla",

    "quiz_completed": "<b>Ders tamamlandı</b>",
    "quiz_result_correct": "Doğru: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Sonuç: <b>%{percentage}</b>",
    "quiz_result_details": "<b>Detaylar:</b>",
    "quiz_result_errors": "Hata: {count}",

    # DERS SONUNDA ÖVGÜ — yalnızca gerçekten olan için
    "praise_first_round": "İlk ders tamam. Bundan sonra kelimeler geri dönmeye başlar — böyle akılda kalırlar.",
    "praise_first_learned": "İlk kelime öğrenildi: farklı günlerde üst üste üç doğru yanıt.",
    "praise_learned": "Bu derste öğrenilen kelime: {count}",
    "praise_best_streak": "Kişisel rekor: {days_word} üst üste",
    "praise_milestone": "{count} kelimeye ulaştınız",
    "praise_first_speech": "Sesle ilk doğru yanıt",
    "praise_first_audio": "Kulakla ilk doğru yanıt",
    "praise_comeback": "Tekrar hoş geldiniz. Ara {days_word} sürdü.",
    "praise_perfect": "Hatasız ders",
    "praise_streak": "Seri: {days_word} üst üste",
    "praise_new_words": "Yeni kelime: {count}",
    "praise_returned": "Yeniden tanınan: {count}",
    "praise_progress": "Üzerinde çalıştığınız kelime: {count} · {target} kelimeye {left} kaldı",
    "praise_progress_top": "Üzerinde çalıştığınız kelime: {count}",
    "praise_points": "Puan: +{points}",

    "quiz_repeat_title": "<b>Hataları tekrarla</b>",
    "quiz_no_errors": "✓ Hiç hatanız yoktu!",
    "quiz_error_next": "✗ Sonraki soru yüklenemedi.",

    # ============================================================================
    # İSTATİSTİK
    # ============================================================================
    "stats_no_level": "<b>Önce seviyenizi seçin!</b>\n\nBaşlamak için /start kullanın.",





    # ============================================================================
    # YARDIM
    # ============================================================================
    "help_title": "<b>Yardım — GenauLingua</b>",
    "help_description": "Burada: derslerin nasıl işlediği ve toplulukla nasıl iletişim kurulacağı.",
    "help_choose": "Bölüm seçin:",

    "help_btn_how_to_use": "Nasıl kullanılır",
    "help_btn_community": "Topluluk",

    "help_how_to_use_title": "<b>Bot nasıl kullanılır</b>",


    "help_community_title": "<b>GenauLingua Topluluğu</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

Sohbette:
Güncellemelerden ilk siz haberdar olun
Hata buldunuz — yazın veya ekran görüntüsü gönderin
Çeviri hatası — bildirin, düzeltelim
Fikir ve öneriler — hepsini okuyoruz
Diğer öğrencilerle sohbet


Topluluk ne kadar aktif olursa — bot o kadar iyi olur. Çekinmeyin! """,


    # ============================================================================
    # SIRALAMAM
    # ============================================================================
    "rating_title_monthly": "<b>Sıralamam — {month} {year}</b>",
    "rating_not_active": "✗ Sıralama henüz aktif değil.",
    "rating_not_in_ranking": "Henüz sıralamada değilsiniz",
    "rating_start_quiz": "İlk dersinizi yapın!",
    "rating_join_by_lesson": "Bildirim puanlarınız ({score}) eklendi. Aylık sıralamaya girmek için bir ders tamamlayın.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — botu sıfırdan yeniden kurduk</b>\n\n<b>Sadece Almanca değil.</b> Ukraynaca, İngilizce, Türkçe, Almanca, Lehçe veya Rusça öğrenin — bunlardan herhangi birinden. Arayüz de altı dilde.\n\n<b>Bir yerine altı oyun.</b> Önceden yalnızca “çeviriyi seç” vardı. Artık her derste oyunlar sırayla gelir:\n📖 Okuyorum · 💭 Hatırlıyorum · 🎧 Dinliyorum · 🎤 Konuşuyorum · 🧩 Eşleri bulun · 🧱 Kuruyorum\n“Konuşuyorum”da sesle cevap verirsiniz, “Kuruyorum”da kelimelerden cümle kurarsınız — bot hangi kelimenin yanlış yerde olduğunu gösterir.\n\n<b>Bot artık konuşuyor.</b> Her kelime ve örnek doğal bir sesle seslendirildi.\n\n<b>Yeni görünüm.</b> Yeni menü, gereksiz mesajlar olmadan temiz sohbet, becerilerinizi gösteren ana ekran, anlaşılır istatistikler, yeni avatar ve karşılama.\n\n<b>Sözlüğün tamamı gözden geçirildi</b> — 12.902 kelimenin hepsi, çeviriler ve örnekler.\n\n<b>Bot kendini size göre ayarlar:</b> kelimeleri unutmanıza az kalmışken geri getirir, işler kolaylaşınca bir üst seviyeyi önerir.\n\n<b>Hatalar düzeltildi:</b> gün seriniz doğru sayılıyor, sıralama puanları adil — emeği ödüllendiriyor. “Öğrenildi” de artık dürüst: bir kelimeyi farklı günlerde üst üste üç kez doğru bildiğinizde öğrenilmiş sayılır; çalıştığınız tüm kelimeler “Üzerinde çalıştığınız kelime” satırında görünür.\n\n<b>Hatırlatıcılar açık</b> — sizin saatinizde. Değiştirmek veya kapatmak için: Ayarlar → Bot → Hatırlatıcılar.\n\n⭐ Bir hata mı buldunuz? Ders özetinden bildirin: onaylanan her bildirim +15 puan getirir.\n\nİlerlemeniz ve puanlarınız korundu. Deneyin — bir ders yalnızca birkaç dakika sürer.",
    "rating_position": "Sıranız: <b>#{rank}</b> / {total}",
    "rating_points": "Puan: <b>{score}</b>",
    "rating_your_month": "<b>{month} ayında:</b>",
    "rating_quizzes": "Dersler: {count}",
    "rating_words_learned": "Öğrenilen kelimeler: {count}",
    "rating_streak": "Seri: {days_word}",
    "rating_avg_result": "Ortalama sonuç: %{percent}",
    "rating_scoring_title": "<b>Puan nasıl kazanılır:</b>",
    "rating_scoring_quiz": "• Tamamlanan ders → +10",
    "rating_scoring_word": "• Öğrenilen kelime → +3",
    "rating_scoring_streak": "• Seri: üst üste her gün bir öncekinden değerli, günde +10'a kadar",
    "rating_scoring_bonus": "• %60'ın üstünde doğruluk → bonus; ne kadar yüksekse o kadar çok",
    "rating_scoring_report": "• Onaylanan hata bildirimi → +{points}",

    "rating_title_alltime": "<b>Sıralamam — Tüm Zamanlar</b>",
    "rating_position_alltime": "Sıranız: <b>#{rank}</b>",
    "rating_position_none": "Sıranız: <b>—</b>",
    "rating_achievements": "<b>Başarılarınız:</b>",
    "rating_wins": "Galibiyet (1. sıra): {count}",
    "rating_total_words": "Öğrenilen kelimeler: {count}",
    "rating_motivation_start": "Kelime öğrenmeye başlayın — ilk adım en önemlisi!",
    "rating_motivation_continue": "Devam edin — ilk galibiyet yakın!",
    "rating_motivation_champion": "Gerçek bir şampiyonsunuz!",

    "table_title_monthly": "<b>Liderlik Tablosu — {month} {year}</b>",
    "table_title_alltime": "<b>Liderlik Tablosu — Tüm Zamanlar</b>",
    "table_empty": "Henüz katılımcı yok.\nİlk dersi yapan siz olun!",
    "table_you_in_top": "Siz: <b>#{rank}</b> / {total}",
    "table_you_not_in_top": "Siz: <b>#{rank}</b> / {total} — {score}",
    "table_you_outside": "Siz: ilk 10 dışında — {score}",
    "table_you_not_ranked": "Henüz sıralamada değilsiniz",
    "btn_leaderboard_table": "Liderlik Tablosu",
    "btn_back_to_rating": "Sıralamaya geri dön",
    "rating_tab_month": "Ay",
    "rating_tab_alltime": "Tüm Zamanlar",

    "stats_header": "<b>İstatistikleriniz</b>",
    "stats_in_work_line": "Üzerinde çalıştığınız kelime: {count} · {target} kelimeye {left} kaldı",
    "stats_in_work_top": "Üzerinde çalıştığınız kelime: {count}",
    "stats_details": "Devam eden: {progress}\nYeni: {new}\nZor: {difficult}",
    "stats_achievements_title": "<b>Başarılarınız</b>",
    "stats_words_count": "Öğrenilen kelimeler: <b>{count}</b>",
    "stats_streak_line": "Seri: {days_word} üst üste",
    "stats_best_streak_line": "En iyi seri: {days_word}",
    "stats_quizzes_header": "<b>Dersler · {level}</b>",
    "stats_quizzes_passed_line": "Tamamlanan: <b>{count}</b>",
    "stats_quizzes_avg_line": "Ortalama sonuç: <b>%{percent}</b>",
    "stats_quizzes_best_line": "En iyi sonuç: <b>%{percent}</b>",
    "stats_quizzes_empty": "Henüz tamamlanan ders yok",
    "stats_recent_header": "<b>Son dersler</b>",
    "stats_overall_header": "<b>Genel ilerleme</b>",
    "stats_overall_learned": "Öğrenilen kelime: <b>{learned}</b> / {total}",
    "stats_explanation": "Kelime öğrenildi = farklı günlerde üst üste üç doğru yanıt",
}

# ============================================================================
# ÇOK DİLLİLİK: öğrenilen dil, anlam dili ve yön
# ============================================================================
TEXTS.update({
    "langname_de": "Almanca",
    "langname_en": "İngilizce",
    "langname_ru": "Rusça",
    "langname_uk": "Ukraynaca",
    "langname_tr": "Türkçe",
    "langname_pl": "Lehçe",
    # Союз для перечисления языков в текстах помощи и приветствия
    "and_word": "ve",

    "settings_learning_lang_line": "Öğrenilen: <b>{language}</b>",

    "settings_btn_learning_lang": "Dil",

    "learning_lang_title": "<b>Öğrenilecek dil</b>",
    "learning_lang_description": "Kelimelerini öğrenmek istediğiniz dili seçin.\nHer dil için ilerleme ayrı tutulur.",
    "learning_lang_set": "✓ Öğrenilen dil: {language}",
    # Ayarlar satiri ve seslendirme ekrani
    "settings_audio_line": "Seslendirme: <b>{state}</b>",
    "settings_btn_audio": "Seslendirme",
    "audio_state_on": "açık",
    "audio_state_off": "kapalı",

    "audio_title": "<b>Seslendirme</b>",
    "audio_description": "Kelimeler doğal bir sesle seslendirilir. Soruda kelimenin kendisi, cevaptan sonra örnekle birlikte duyulur.",
    "audio_current_voice": "Ses: <b>{voice}</b>",
    "audio_btn_turn_on": "Seslendirmeyi aç",
    "audio_btn_turn_off": "Seslendirmeyi kapat",
    "audio_btn_choose_voice": "Ses seç",
    "audio_turned_on": "✓ Seslendirme açık",
    "audio_turned_off": "Seslendirme kapalı",

    "voice_title": "<b>Ses seçimi</b>",
    "voice_description": "Dinlemek için bir sese dokunun. İşaretli olan seçili sestir.",
    "voice_male": "Erkek",
    "voice_female": "Kadın",
    "voice_set": "✓ Ses: {voice}",
    "voice_use": "{voice} seç",
    "voice_listening": "{voice} çalıyor",
    "voice_only_one": "Bu dil için yalnızca bir erkek ve bir kadın sesi var — başka ses yok.",
    "voice_preview_failed": "Örnek alınamadı, tekrar deneyin",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Sıralama",
    "friend_fallback": "arkadaş",
    "onboarding_learning_title": "<b>Hangi dili öğreneceksiniz?</b>",
    "onboarding_learning_desc": "Kelimelerin anlamı şu dilde gösterilecek: {native}\nDili ayarlardan istediğiniz zaman değiştirebilirsiniz.",
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
    "help_how_to_use_text": "<b>Ders</b>\n{words}; sorularda dört seçenek var. Oyunlar kendiliğinden değişir: «Okuyorum», «Hatırlıyorum», «Dinliyorum», «Konuşuyorum» ve «Eşleri bulun» tahtası. Bot hatalarınızı hatırlar ve zor kelimeleri daha sık getirir. Dersten sonra yanlışlarınızı hemen tekrarlayabilirsiniz.\n\n<b>Seslendirme</b>\nSoruda kelime duyulur, cevaptan sonra kelime örnekle birlikte gelir. Ayarlardan erkek veya kadın sesi seçebilirsiniz.\n\n<b>Diller</b>\n{languages} — istediğiniz dil çiftinde. İlerleme ve sıralama her dil için ayrı tutulur.\n\n\nKelime, farklı günlerde üst üste üç doğru cevaptan sonra <b>öğrenilmiş</b> sayılır.\n<b>Seri</b>, o gün yapılan herhangi bir dersle uzar.\nÇeviri veya telaffuz hatası mı var? Dersin sonundaki «Hata bildir» düğmesine dokunun.",
    "help_community_title": "<b>Bot ve topluluk hakkında</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} dil, istediğiniz çiftte: {languages}\nA1–C2 arası 12 900 kelime, her birinde örnek ve doğal sesle seslendirme.\nArayüz: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nHatalar, çeviri yanlışları, fikirler — hepsini okuyoruz. Telaffuzla ilgili bildirimler özellikle değerli: makine vurguyu duymaz.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Dinleyin ve duyduğunuzu seçin:",
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
    "rating_scoring_answer": "• Doğru cevap → +1, kulakla → +2, sesli → +3",
    "rating_scoring_quiz": "• Tamamlanan ders → +10",
    "rating_scoring_word": "• Öğrenilen kelime → +3",
    "rating_scoring_streak": "• Seri: üst üste her gün bir öncekinden değerli, günde +10'a kadar",
    "rating_scoring_bonus": "• %60'ın üstünde doğruluk → bonus; ne kadar yüksekse o kadar çok",
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
    "quiz_result_by_ear": "🎧 Kulakla: {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "Dersteki oyunlar",
    "settings_channels_line": "Dersteki oyunlar: <b>{channels}</b>",
    "channels_title": "<b>Dersteki oyunlar</b>",
    "channels_description": "Derse hangi oyunların karışacağını seçin. Yeni kelime «Okuyorum» kartıyla gelir; onu tanıdığınızda başka oyunlarla döner: hatırlamak, duymak, söylemek, cümle kurmak. Oyun ne kadar çoksa kelime o kadar iyi yerleşir.",
    "channel_text": "📖 Okuyorum",
    "channel_audio": "🎧 Dinliyorum",
    "channel_speech": "🎤 Konuşuyorum",
    "channel_build": "🧱 Kuruyorum",
    "home_scale_build": "Kuruyorum",
    "quiz_result_built": "🧱 Kurulan: {count}",
    "build_hint": "Cümleyi aşağıdaki kelimelerden kurun — aralarında fazlalar var",
    "build_btn_check": "Kontrol et",
    "build_full": "Tüm yerler dolu. ⌫ ile bir kelimeyi kaldırın ya da «Kontrol et» düğmesine basın.",
    "build_order_only": "↔ <b>Kelimeler doğru, sıra farklı</b>",
    "build_reference": "Doğrusu:",
    "build_yours": "Cevabınız:",
    "build_extra": "Fazla: {words}",
    "build_missing": "Eksik: {words}",
    "stats_grammar_line": "Dil bilgisi: {shown} cümleden {correct} doğru",
    "quiz_result_recalled": "💭 Hatırlanan: {count}",
    "home_scale_reverse": "Hatırlıyorum",
    "channel_reverse": "💭 Hatırlıyorum",
    "channels_text_always": "«Okuyorum» kapatılamaz: her yeni kelime bu kartla başlar.",
    "channels_audio_blocked": "🎧 «Dinliyorum» ve «Konuşuyorum» kullanılamıyor: seslendirme kapalı.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Bu kelimeyi yüksek sesle söyleyin — sesli mesaj kaydedin",
    "speech_btn_reference": "Yavaş dinle",
    "speech_btn_skip": "Atla",
    "speech_listening": "🎧 Sesinizi dinliyorum…",
    "speech_not_understood": "Anlayamadım. Tekrar kaydedin — mikrofona yakın durun ve biraz daha yüksek sesle konuşun.",
    "speech_try_again": "«{heard}» gibi duyuldu — tam değil. Lütfen tekrar kaydedin: deneme {attempt}/{total}.",
    "speech_send_voice": "🎤 Bu soru sesli mesajla cevaplanır. Mikrofon düğmesine basılı tutun.",
    "speech_skipped": "Atlandı",
    "speech_not_counted": "Yine «{heard}» gibi duyuldu. Bu ne doğru ne de hata sayılır — nasıl söylendiğini dinleyin ve devam edelim.",
    "quiz_result_spoken": "🎤 Sesli: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Okuyorum",
    "home_scale_audio": "Dinliyorum",
    "home_scale_speech": "Konuşuyorum",
    "home_btn_learn": "Kelime öğren",
    "home_streak": "seri {days_word}",
    "home_rank": "sıra {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: henüz erken. Hazır kelime sayısı {ready}, en az {minimum} gerekiyor. Kartlarla çalışın — diğer oyunları onlar açıyor.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "Ne öğreniyorum",
    "settings_group_what_title": "<b>Ne öğreniyorum</b>",
    "settings_group_how": "Nasıl öğreniyorum",
    "settings_group_how_title": "<b>Nasıl öğreniyorum</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Dil, hedef ve seviye.",
    "settings_group_how_about": "Dersin nelerden oluştuğu ve nasıl duyulduğu.",
    "settings_group_bot_about": "Bot dili, hatırlatıcılar ve yardım.",
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
    "quiz_btn_one_more": "Bir ders daha",
    "home_btn_stats": "Ayrıntılar",
    "notif_off_how_to_return": "Geri açmak için: Ayarlar → Bot → Hatırlatıcılar",
    "reminder_offer": "Günde bir kez hatırlatayım mı? Öğrendiklerinizi kaybetmemek böyle daha kolay — seri de kopmaz.",
    "reminder_offer_yes": "Evet, hatırlat",
    "reminder_offer_no": "Gerek yok",
    "reminder_offer_done": "✓ Tamam: hatırlatıcı saat <b>{time}</b> ({city}) gelecek. Saati, günleri ve saat dilimini ayarlayabilirsiniz.",
    "reminder_offer_setup": "Hatırlatıcıları ayarla",
    "level_offer": "<b>{current}</b> seviyesinde neredeyse hiç hata yapmıyorsunuz. <b>{following}</b> seviyesine geçelim mi? Öğrendikleriniz sizde kalır.",
    "level_offer_yes": "Evet, {following} seviyesine geç",
    "level_offer_no": "Burada kalayım",
    "level_offer_done": "Yeni seviye: <b>{following}</b>. Kelimeler artık daha zor olacak.",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "Dili ne için öğreniyorsunuz? Kelimeleri ona göre seçeriz.",
    "goal_work": "İş için",
    "goal_travel": "Seyahat için",
    "goal_living": "Yurt dışında yaşamak için",
    "goal_study": "Öğrenim için",
    "goal_any": "Sadece kelime öğrenmek",
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
    "intro_games": "Bir kelime burada beş oyunla öğrenilir: okumak, anlamından hatırlamak, duymak, yüksek sesle söylemek ve tahtada eşini bulmak.\nHer derste bot bunları kendisi karıştırır.",
    "intro_numbers": "12 902 kelime · 20 konu · 6 seviye\nAltı dil, istediğiniz çiftte: dilerseniz Lehçeyi İngilizce üzerinden öğrenin.",
    "intro_menu_settings": "dil, dersteki oyunlar, hatırlatıcılar",
    "intro_menu_stats": "ilerlemeniz",
    "intro_menu_rating": "ayın sıralaması",
    "intro_menu_learn": "bir ders",
    "intro_menu_title": "Ne nerede:",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Hedef",
    "settings_goal_title": "<b>Ne için öğreniyorum</b>",
    "settings_goal_description": "Hedefinize uygun konunun kelimeleri, yeni kelimeler arasında önce gelir. Zorluk yine seviyenize göre belirlenir, öğrendikleriniz de tekrara dönmeye devam eder.",
    "settings_goal_set": "Hedef kaydedildi",
    "settings_goal_line": "Hedef: <b>{goal}</b>",
    "settings_goal_none": "seçilmedi",
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
    "match_title": "<b>Eşleri bulun</b>",
    "match_progress": "Eşleşen: {matched} / {total}",
    "match_errors": "✗ Iskalanan: {count}",
    "match_hint": "Bir kelimeye herhangi bir taraftan dokunun, sonra eşine öbür taraftan.",
    "match_wrong": "✗ Eş değil",
    "match_done": "<b>Tahta tamamlandı!</b>",
    "match_done_counted": "İlerlemeye sayılan: {total} içinden {counted} — yalnızca ilk denemede eşleşenler, son eşleşme ise hiç sayılmaz: orada seçenek kalmıyor.",
    "match_btn_again": "Bir tahta daha",
    "match_not_ready": "Henüz erken: tahta için {need} bildik kelime gerek, sizde {have} var. Kartlarla çalışın — tahtayı onlar açıyor.",
})

TEXTS["match_back_to_round"] = "Derse dönüyoruz."

TEXTS.update({
    "settings_btn_match": "Derste tahta",
    "settings_match_title": "<b>Derste tahta</b>",
    "settings_match_description": "Her derste ortadaki sorulardan birinin yerine tahta gelir: beş kelime ve beş anlam, eşlerini bulun. Yalnızca bildiğiniz kelimeler alınır; bu yüzden tahta, en az on bildik kelimeniz olduğunda belirir.",
    "match_state_on": "Tahta açık: dersin ortasında gelecek.",
    "settings_match_short_on": "tahta ile",
    "settings_channels_short_one": "yalnızca «Okuyorum»",
    "settings_channels_short_some": "dört oyundan {count} tanesi",
    "settings_channels_short_all": "dört oyunun hepsi",
    "plural_words": "kelime",
    "plural_points": "puan",
    "plural_days": "gün",
    "settings_audio_short_off": "sessiz",
    "settings_audio_short_on": "sesli",
    "settings_match_short_off": "tahtasız",
    "match_state_off": "Tahta kapalı: ders yalnızca sorulardan oluşur.",
})
