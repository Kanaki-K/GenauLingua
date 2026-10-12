"""
Türkçe lokalizasyon - GenauLingua Bot
"""

TEXTS = {
    # ============================================================================
    # ANA MENÜ BUTONLARI
    # ============================================================================
    "btn_learn_words": "📚 Kelime öğren",
    "btn_stats": "📊 İstatistik",
    "btn_settings": "🦾 Ayarlar",
    "btn_help": "❓ Yardım",
    "btn_back": "◀️ Geri",
    "menu_placeholder": "Bir eylem seç...",

    # ============================================================================
    # KARŞILAMA VE BAŞLANGIÇ
    # ============================================================================
    "welcome_title": "👋 <b>Merhaba, {name}!</b>",






    "welcome_choose_level": "🎯 <b>Nereden başlayalım?</b>\n\nSeviyen — {language}\n\n• A1–A2 — temel kelimeler\n• B1–B2 — güvenli iletişim\n• C1–C2 — ana dil seviyesi",
    "choose_level_prompt": "Seviye seç:",

    "level_selected": "✅ <b>{level}</b> seviyesi seçildi.\n\n12 902 kelime, altı dil. Haydi on beşle başlayalım.",
    "level_locked": "🔒 Bu seviye yakında geliyor",

    # ============================================================================
    # HATIRLATICILAR
    # ============================================================================
    "notif_title": "🔔 <b>Hatırlatıcı Ayarları</b>",
    "notif_status": "Durum: {status}",
    "notif_status_on": "🔔 Açık",
    "notif_status_off": "🔕 Kapalı",
    "notif_time": "Saat: {time}",
    "notif_days": "Günler: {days}",
    "notif_timezone": "Zaman dilimi: {timezone}",
    "notif_hint": "💡 Hatırlatıcılar belirtilen saatte saat diliminize göre gelecek.",
    "notif_hint_off": "💡 Günlük çalışmayı unutmamak için hatırlatıcıları açın!",

    "notif_btn_toggle_on": "🔔 Hatırlatıcılar: Açık",
    "notif_btn_toggle_off": "🔕 Hatırlatıcılar: Kapalı",
    "notif_btn_time": "🕐 Saat: {time}",
    "notif_btn_days": "📅 Günleri seç",
    "notif_btn_timezone": "🌍 Zaman dilimini değiştir",

    "notif_timezone_title": "🌍 <b>Zaman diliminizi seçin</b>",
    "notif_timezone_current": "Şu anki: {timezone}",
    "notif_timezone_prompt": "Zaman diliminizde bir şehir seçin:",
    "notif_timezone_more": "🌍 Başka şehir seç ▼",
    "notif_timezone_back": "◀️ Geri",
    "notif_timezone_set": "✅ Zaman dilimi ayarlandı: {city}",

    "notif_time_title": "🕐 <b>Hatırlatıcı saatini seçin</b>",
    "notif_time_current": "Şu anki saat: {time}",
    "notif_time_timezone": "Zaman dilimi: {timezone}",
    "notif_time_hint": "Hatırlatıcı her gün seçilen saatte gelecek.",
    "notif_time_set": "✅ Saat ayarlandı: {time}",

    "notif_days_title": "📅 <b>Hatırlatıcı günlerini seçin</b>",
    "notif_days_hint": "Günü açmak/kapatmak için dokunun.\n✅ Yeşil işaret - gün açık\n❌ Kırmızı çarpı - gün kapalı\n\nBitirdiğinizde - 'Kaydet'e basın.",
    "notif_days_all": "📅 Tüm günler",
    "notif_days_weekdays": "🗓️ Hafta içi (Pzt-Cum)",
    "notif_days_save": "💾 Kaydet",
    "notif_days_saved": "✅ Günler kaydedildi!",
    "notif_days_all_selected": "✅ Tüm günler seçildi",
    "notif_days_weekdays_selected": "✅ Hafta içi seçildi (Pzt-Cum)",
    "notif_days_none": "⚠️ Hatırlatıcılar için en az bir gün seçin!",

    "notif_toggle_on": "🔔 Hatırlatıcılar açıldı!",
    "notif_toggle_off": "🔕 Hatırlatıcılar kapatıldı",

    "notif_message_btn_disable": "🔕 Hatırlatıcıları kapat",

    "day_mon": "Pzt",
    "day_tue": "Sal",
    "day_wed": "Çar",
    "day_thu": "Per",
    "day_fri": "Cum",
    "day_sat": "Cmt",
    "day_sun": "Paz",

    "notif_btn_back": "◀️ Ayarlara geri dön",

    "notif_default_name": "arkadaş",
    "notif_message_greeting": "🔥 <b>Çalışma zamanı, {name}!</b>",

    "notif_motivation_1": "Adım adım hedefinize ulaşıyorsunuz!",
    "notif_motivation_2": "Seriniz büyüyor — devam edin!",
    "notif_motivation_3": "Bugün akıcı konuşmaya doğru bir adım daha!",
    "notif_motivation_4": "Her gün küçük çabalar = büyük sonuçlar!",
    "notif_motivation_5": "Doğru yoldasınız! Durmayın!",
    "notif_motivation_6": "Her test sizi hedefinize yaklaştırıyor!",

    # ============================================================================
    # AYARLAR
    # ============================================================================
    "settings_title": "🦾 <b>Ayarlar</b>",
    "settings_level": "📚 Seviye: <b>{level}</b>",
    "settings_mode": "🔄 Çeviri: <b>{mode}</b>",
    "settings_language": "🌍 Arayüz dili: <b>{language}</b>",
    "settings_choose": "Ne değiştirmek istediğini seç:",

    "settings_btn_quiz_mode": "📝 Test modu",
    "settings_btn_change_mode": "🔄 Çeviri modu",
    "settings_btn_change_language": "🌍 Arayüz dili",
    "settings_btn_notifications": "🔔 Hatırlatıcılar",

    "settings_quiz_mode_line": "📝 Mod: <b>{mode}</b>",

    "settings_mode_title": "🔄 <b>Çeviri modu</b>",
    "settings_mode_description": "Çeviri yönünü seç:",

    "settings_language_title": "🌍 <b>Arayüz dili</b>",
    "settings_language_description": "Bot arayüz dilini seç:",

    "language_changed": "✅ Dil {language} olarak değiştirildi",
    "level_not_selected": "Seçilmedi",
    "user_not_found": "❌ Kullanıcı bulunamadı. /start kullan",

    "lang_ru": "🏴 Русский",
    "lang_uk": "🇺🇦 Українська",
    "lang_en": "🇬🇧 English",
    "lang_tr": "🇹🇷 Türkçe",
    "lang_de": "🇩🇪 Deutsch",
    "lang_pl": "🇵🇱 Polski",

    "mode_de_to_ru": "🇩🇪 DE → 🏴 RU",
    "mode_ru_to_de": "🏴 RU → 🇩🇪 DE",
    "mode_de_to_uk": "🇩🇪 DE → 🇺🇦 UK",
    "mode_uk_to_de": "🇺🇦 UK → 🇩🇪 DE",
    "mode_de_to_en": "🇩🇪 DE → 🇬🇧 EN",
    "mode_en_to_de": "🇬🇧 EN → 🇩🇪 DE",
    "mode_de_to_tr": "🇩🇪 DE → 🇹🇷 TR",
    "mode_tr_to_de": "🇹🇷 TR → 🇩🇪 DE",


    # ============================================================================
    # TEST MODU (YENİ)
    # ============================================================================
    "qmode_title": "📝 <b>Test modu</b>",
    "qmode_current": "Şu an: <b>{mode}</b>",
    "qmode_choose": "Nasıl öğrenmek istediğini seç\nİstediğin zaman değiştirebilirsin — ilerlemen kaybolmaz",

    "qmode_btn_level": "📚 Seviyeye göre",
    "qmode_btn_category": "🗂 Kategori",
    "qmode_btn_all": "🌍 Top 10 bin",
    "qmode_btn_difficult": "⚠️ Zor",

    "qmode_level_short": "📚 Seviye {level}",
    "qmode_category_short": "🗂 {category}",
    "qmode_all_short": "🌍 Top 10 bin",
    "qmode_difficult_short": "⚠️ Zor kelimeler",

    "qmode_level_title": "📚 <b>Seviye seç</b>",
    "qmode_level_desc": "İlk «Hallo»dan akıcı tartışmalara\nTüm seviyeler açık — birini seç!\n\n• A1–A2 — temel kelimeler\n• B1–B2 — güvenli iletişim\n• C1–C2 — ana dil seviyesi",
    "qmode_level_set": "✅ Mod: Seviyeye göre ({level})",

    "qmode_category_title": "🗂 <b>Kategori seç</b>",
    "qmode_category_desc": "Yemekten bilime — ihtiyacın olan konuyu seç\n\nHer kategoride tüm seviyelerin kelimeleri var",
    "qmode_category_set": "✅ Mod: {category}",

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

    "qmode_all_set": "✅ Mod: Top 10 bin",

    "qmode_difficult_set": "✅ Mod: Zor kelimeler",
    "qmode_difficult_few": "Henüz sadece {count} zor kelimeniz var — en az 4 gerekli\nBirkaç test daha çöz!",
    "qmode_difficult_empty": "Henüz zor kelimelerin yok.\nÖnce birkaç test çöz!",

    "quiz_btn_change_mode": "⚙️ Test modu",
    "quiz_btn_report_error": "📝 Çeviri hatası",
    "report_btn_confirm": "✅ Onayla ({count})",
    "report_btn_send": "📨 Gönder",
    "report_no_words": "Raporlanacak kelime yok",
    "report_none_selected": "En az bir kelime seç",
    "report_sent": "✅ {count} rapor gönderildi — teşekkürler!\nOnaylanırsa — +1 puan kazanırsın",
    "report_daily_limit": "⚠️ Bugünkü rapor limiti doldu (maks. 20)",
    "report_all_reported": "✅ Bu testdeki tüm kelimeler zaten raporlandı",
    "report_already_sent": "✔️ Zaten raporlandı",
    "report_kind_title": "Tam olarak ne yanlış?",
    "report_btn_kind_text": "📝 Hatalı çeviri",
    "report_btn_kind_audio": "🔊 Hatalı telaffuz",
    "report_sent_audio": "✅ {count} gönderildi — teşekkürler!\nTelaffuz bildirimleri özellikle değerli: otomatik kontrol vurguyu duymaz",

    # ============================================================================
    # TEST
    # ============================================================================
    "quiz_no_level": "⚠️ Önce /start ile seviyeni seç",
    "quiz_error_generation": "❌ Test hazırlanırken hata oluştu.\n/start ile tekrar dene",
    "quiz_no_words": "❌ Üzgünüz, bu seviye için henüz kelime yok.\nBaşka bir seviye seçmeyi dene.",

    "quiz_question_number": "Soru {current}/{total}",
    "quiz_question_choose_word": "Doğru kelimeyi seç:",
    "quiz_question_choose_translation": "Doğru çeviriyi seç:",

    "quiz_correct": "✅ <b>Doğru!</b>",
    "quiz_wrong": "❌ <b>Yanlış!</b>",
    "quiz_correct_answer": "Doğru cevap:",

    "quiz_btn_next": "İleri →",
    "quiz_btn_repeat_errors": "🔄 Hataları tekrarla",

    "quiz_completed": "🎉 <b>Test tamamlandı!</b>",
    "quiz_result_correct": "✅ Doğru: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "📈 Sonuç: <b>{percentage}%</b>",
    "quiz_result_details": "📝 <b>Detaylar:</b>",
    "quiz_result_errors": "❌ Hata: {count}",

    "quiz_repeat_title": "🔄 <b>Hataları tekrarla</b>",
    "quiz_repeat_question": "🔄 Tekrar {current}/{total}",
    "quiz_no_errors": "✅ Hiç hatan yoktu!",
    "quiz_error_next": "❌ Sonraki soru yüklenemedi.",
    "quiz_error_generate": "❌ Sonraki soru oluşturulamadı.",

    # ============================================================================
    # İSTATİSTİK
    # ============================================================================
    "stats_title": "📊 <b>İstatistik</b>",
    "stats_no_level": "⚠️ <b>Önce seviyeni seç!</b>\n\nBaşlamak için /start kullan.",

    "stats_all_words": "📚 Tüm kelimeler ({count})",
    "stats_learned": "✅ Öğrenildi: {count}",
    "stats_in_progress": "🔄 Devam ediyor: {count}",
    "stats_new": "🆕 Yeni: {count}",
    "stats_difficult": "❌ Zor: {count}",

    "stats_level_title": "🎯 Seviye {level} · {mode} ({count} kelime)",
    "stats_quizzes_title": "🏆 <b>Testler (seviye {level}):</b>",
    "stats_quizzes_passed": "Tamamlanan: {count}",
    "stats_quizzes_avg": "Ortalama sonuç: {percentage}%",
    "stats_quizzes_best": "En iyi sonuç: {percentage}%",
    "stats_quizzes_none": "Bu seviyede henüz test çözmedin.",

    "stats_activity_title": "🔥 <b>Aktivite:</b>",
    "stats_streak": "└─ Seri: <b>{days}</b> gün üst üste",

    "stats_recent_title": "<b>Son testler:</b>",
    "stats_learned_explanation": "💡 <b>Öğrenildi</b> — üst üste 3 doğru cevap, ve kelimeyle tanıştığın gün değil",

    # ============================================================================
    # YARDIM
    # ============================================================================
    "help_title": "❓ <b>Yardım — GenauLingua</b>",
    "help_description": "Burada talimatlar, yakında gelecek özellikler ve toplulukla iletişim bilgilerini bulacaksın.",
    "help_choose": "Bölüm seç:",

    "help_btn_how_to_use": "📖 Nasıl kullanılır",
    "help_btn_community": "💬 Topluluk",

    "help_how_to_use_title": "📖 <b>Botu nasıl kullanırsın</b>",
    "help_how_to_use_text": """1️⃣ <b>Hangi dili öğreneceğini seç</b>
🦾 Ayarlar → 🎯 Hangi dili öğrenmek: {languages}.
Aynı ekranda: A1–C2 seviyesi, çeviri yönü ve arayüz dili.
İlerleme her dil için ayrı tutulur, iki dili birlikte öğrenebilirsin.

2️⃣ <b>Test modunu seç</b>
🦾 Ayarlar → 📝 Test modu:
• Seviyeye göre — seviyenin kelimeleri
• Kategoriye göre — 20 konu: yemek, iş, seyahat...
• Top 10 bin — tüm kelime tabanı
• Zor — sık yanlış yaptığın kelimeler

3️⃣ <b>Her gün kelime öğren</b>
📚 Kelime öğren → 25 kelimelik test.
Bot hatalarını hatırlar ve zor kelimeleri daha sık gösterir.

4️⃣ <b>Hatalarını tekrarla</b>
Testten sonra hatalı kelimeleri hemen tekrarlayabilirsin.

5️⃣ <b>İlerlemeni takip et</b>
📊 İstatistik → kaç kelime öğrenildi, test geçmişi, seri.

6️⃣ <b>Diğerleriyle yarış</b>
🏆 Sıralamam → aylık ve tüm zamanlar puanların.
📊 Liderlik Tablosu → tüm katılımcılar arasında ilk 10.

7️⃣ <b>Hatırlatıcıları ayarla</b>
🦾 Ayarlar → 🔔 Hatırlatıcılar → saat, gün ve zaman dilimi seç.

🔊 <b>Seslendirme</b>
Kelime ana dili konuşan bir sesle okunur: soruda kelimenin kendisi, cevaptan sonra örnekle birlikte. Böylece hem telaffuzu hem de kelimenin gerçek konuşmadaki halini duyarsın.
🦾 Ayarlar → 🔊 Seslendirme: kapatabilir ya da ses seçebilirsin. Almanca için üç erkek ve üç kadın sesi var, dokununca hemen çalar.
Ters yönde ses cevaptan sonra gelir: aksi halde okunan kelime cevabın kendisi olurdu.

━━━━━━━━━━━━━━━━━
💡 Kelime <b>öğrenildi</b> sayılır — üst üste 3 doğru cevap verilince.
🔥 <b>Seri</b> günde en az 1 test çözersen artar.
📝 Hata mı buldun? Testten sonra butona bas ve neyin yanlış olduğunu belirt — çeviri mi telaffuz mu. Telaffuz bildirimleri en çok gerekli olan: makine vurguyu duymaz.

Sorular? → t.me/genaulingua_chat""",


    "help_community_title": "💬 <b>GenauLingua Topluluğu</b>",
    "help_community_text": """👉 <b>t.me/genaulingua_chat</b>

Sohbette:
📢 Güncellemelerden ilk sen haberdar ol
🐛 Hata buldun — yaz veya ekran görüntüsü gönder
📝 Çeviri hatası — bildir, düzeltelim
💡 Fikir ve öneriler — hepsini okuyoruz
👥 Diğer öğrencilerle sohbet

━━━━━━━━━━━━━━━━━
Topluluk ne kadar aktif olursa — bot o kadar iyi olur. Çekinme! 🙌""",


    # ============================================================================
    # SIRALAMAM
    # ============================================================================
    "rating_title_monthly": "🏆 <b>Sıralamam — {month} {year}</b>",
    "rating_not_active": "❌ Sıralama henüz aktif değil.",
    "rating_not_in_ranking": "📍 Henüz sıralamada değilsin",
    "rating_start_quiz": "🚀 İlk testini çöz!",
    "rating_position": "📍 Pozisyon: <b>#{rank}</b> / {total}",
    "rating_points": "💎 Puan: <b>{score}</b>",
    "rating_your_month": "⭐ <b>{month} ayın:</b>",
    "rating_quizzes": "├ Testler: {count}",
    "rating_words_learned": "├ Öğrenilen kelimeler: {count}",
    "rating_streak": "├ Seri: {count} gün",
    "rating_avg_result": "└ Ortalama sonuç: {percent}%",
    "rating_goal": "🎯 #{rank} ({name}) için: {diff} puan daha",
    "rating_scoring_title": "💡 <b>Puan nasıl kazanılır:</b>",
    "rating_scoring_quiz": "• Tamamlanan test → +10",
    "rating_scoring_reverse": "• Ters mod → +5",
    "rating_scoring_word": "• Öğrenilen kelime → +2",
    "rating_scoring_streak": "• Gün serisi → +3",
    "rating_scoring_bonus": "• %90+ doğruluk → +50 bonus",
    "rating_scoring_report": "• Onaylanan rapor → +1",

    "rating_title_alltime": "🏆 <b>Sıralamam — Tüm Zamanlar</b>",
    "rating_position_alltime": "📍 Pozisyon: <b>#{rank}</b>",
    "rating_position_none": "📍 Pozisyon: <b>—</b>",
    "rating_achievements": "⭐ <b>Başarıların:</b>",
    "rating_wins": "├ Galibiyet (1. sıra): {count}",
    "rating_total_words": "└ Öğrenilen kelimeler: {count}",
    "rating_motivation_start": "🚀 Kelime öğrenmeye başla — ilk adım en önemlisi!",
    "rating_motivation_continue": "🎯 Devam et — ilk galibiyet yakın!",
    "rating_motivation_champion": "🔥 Gerçek bir şampiyonsun!",
    "rating_lifetime_title": "🌟 <b>Lifetime puanlar:</b>",
    "rating_lifetime_desc": "• Tüm aylardan toplam puanlar\n• 🥇 için +100 · 🥈 için +50 · 🥉 için +25",

    "table_title_monthly": "📊 <b>Liderlik Tablosu — {month} {year}</b>",
    "table_title_alltime": "📊 <b>Liderlik Tablosu — Tüm Zamanlar</b>",
    "table_empty": "Henüz katılımcı yok.\nİlk testi sen çöz! 💪",
    "table_you_in_top": "📍 Sen: <b>#{rank}</b> / {total}",
    "table_you_not_in_top": "📍 Sen: <b>#{rank}</b> / {total} — {score} puan",
    "table_you_outside": "📍 Sen: ilk 10 dışında — {score} puan",
    "table_you_not_ranked": "📍 Henüz sıralamada değilsin",
    "table_points": "puan",
    "btn_leaderboard_table": "📊 Liderlik Tablosu",
    "btn_back_to_rating": "◀️ Sıralamaya geri dön",

    "stats_header": "📊 <b>İstatistiklerin</b>",
    "stats_learned_of": "└─ Öğrenildi <b>{learned}</b> / {total}",
    "stats_details": "⏳ Devam eden: {progress}\n🆕 Yeni: {new}\n⚠️ Zor: {difficult}",
    "stats_achievements_title": "<b>Başarıların</b>",
    "stats_words_count": "├─ Öğrenilen kelimeler: <b>{count}</b>",
    "stats_streak_line": "└─ Seri: <b>{days} gün üst üste</b>",
    "stats_quizzes_header": "<b>Testler · {level}</b>",
    "stats_quizzes_passed_line": "├─ Tamamlanan: <b>{count}</b>",
    "stats_quizzes_avg_line": "├─ Ortalama sonuç: <b>{percent}%</b>",
    "stats_quizzes_best_line": "└─ En iyi sonuç: <b>{percent}%</b>",
    "stats_quizzes_empty": "└─ Henüz tamamlanan test yok",
    "stats_recent_header": "📈 <b>Son testler</b>",
    "stats_overall_header": "🌍 <b>Genel ilerleme</b>",
    "stats_overall_learned": "└─ Öğrenildi <b>{learned}</b> / {total} kelime",
    "stats_cta_start": "💪 Kelime öğrenmeye başla — ilk adım en önemlisi!",
    "stats_cta_begin": "🚀 Harika başlangıç! Devam et!",
    "stats_cta_halfway": "🔥 Yarı yoldasın! Durma!",
    "stats_cta_almost": "🏆 Neredeyse hedefe ulaştın! Harikasın!",
    "stats_explanation": "—————————————————————\nÖğrenildi = üst üste 3 doğru cevap",
    "stats_btn_rating": "🏆 Sıralamam",
}

# ============================================================================
# ÇOK DİLLİLİK: öğrenilen dil, anlam dili ve yön
# ============================================================================
TEXTS.update({
    "langname_de": "🇩🇪 Almanca",
    "langname_en": "🇬🇧 İngilizce",
    "langname_ru": "🏴 Rusça",
    "langname_uk": "🇺🇦 Ukraynaca",
    "langname_tr": "🇹🇷 Türkçe",
    "langname_pl": "🇵🇱 Lehçe",
    # Союз для перечисления языков в текстах помощи и приветствия
    "and_word": "ve",

    "settings_learning_lang_line": "🎯 Öğrenilen: <b>{language}</b>",

    "settings_btn_learning_lang": "🎯 Hangi dili öğrenmek",

    "learning_lang_title": "🎯 <b>Hangi dili öğrenmek</b>",
    "learning_lang_description": "Kelimelerini öğrenmek istediğin dili seç.\nHer dil için ilerleme ayrı tutulur.",
    "learning_lang_set": "✅ Öğreniyoruz: {language}",
    # Ayarlar satiri ve seslendirme ekrani
    "settings_audio_line": "🔊 Seslendirme: <b>{state}</b>",
    "settings_btn_audio": "🔊 Seslendirme",
    "audio_state_on": "açık",
    "audio_state_off": "kapalı",

    "audio_title": "🔊 <b>Seslendirme</b>",
    "audio_description": "Kelimeler ana dili konuşan bir sesle okunur. Soruda kelimenin kendisi, cevaptan sonra örnekle birlikte duyulur.",
    "audio_current_voice": "🎙 Ses: <b>{voice}</b>",
    "audio_btn_turn_on": "🔊 Seslendirmeyi aç",
    "audio_btn_turn_off": "🔇 Seslendirmeyi kapat",
    "audio_btn_choose_voice": "🎙 Ses seç",
    "audio_turned_on": "✅ Seslendirme açık",
    "audio_turned_off": "🔇 Seslendirme kapalı",

    "voice_title": "🎙 <b>Ses seçimi</b>",
    "voice_description": "Dinlemek için bir sese dokun. İşaretli olan seçili sestir.",
    "voice_male": "Erkek",
    "voice_female": "Kadın",
    "voice_set": "✅ Ses: {voice}",
    "voice_only_one": "Bu dil için motorda bir erkek ve bir kadın sesi var — daha fazlası yok.",
    "voice_preview_failed": "Örnek alınamadı, tekrar dene",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "🏆 Sıralama",
    "friend_fallback": "dostum",
    "onboarding_learning_title": "🎯 <b>Hangi dili öğreneceksin?</b>",
    "onboarding_learning_desc": "Kelimelerin anlamı şu dilde gösterilecek: {native}\nDili ve yönü ayarlardan istediğin zaman değiştirebilirsin.",
    "mode_hint_forward": "💡 {learning} → {native} daha kolay: anlamı mantıkla bulursun",
    "mode_hint_reverse": "💡 {native} → {learning} daha zor: kelimeleri daha iyi pekiştirir",
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
    "help_how_to_use_text": "🎮 <b>Test</b>\n25 kelime, dört seçenek. Bot hatalarını hatırlar ve zor kelimeleri daha sık getirir. Testten sonra yanlışları hemen tekrarlayabilirsin.\n\n🔊 <b>Seslendirme</b>\nSoruda kelime duyulur, cevaptan sonra kelime örnekle birlikte gelir. Ayarlardan erkek veya kadın sesi seçebilirsin.\n\n🌍 <b>Diller</b>\n{languages} — her çiftte ve iki yönde. İlerleme ve sıralama her dil için ayrı tutulur.\n\n━━━━━━━━━━━━━━━━━\n💡 Kelime, farklı günlerde üst üste üç doğru cevaptan sonra <b>öğrenilmiş</b> sayılır.\n🔥 <b>Seri</b> o gün yapılan herhangi bir testle büyür.\n📝 Çeviri veya telaffuz hatası — testin altındaki düğme.",
    "help_community_title": "💬 <b>Bot ve topluluk hakkında</b>",
    "help_community_text": "🤖 <b>GenauLingua</b> — her çiftte {language_count} dil: {languages}\nA1–C2 arası 12 900 kelime, her birinde örnek ve ana dili konuşanın sesi.\nArayüz: {interface_languages}\n\n💬 <b>t.me/genaulingua_chat</b>\nHatalar, çeviri yanlışları, fikirler — hepsini okuyoruz. Telaffuzla ilgili bildirimler özellikle değerli: makine vurguyu duymaz.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "🔊 Dinle ve duyduğunu seç:",
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
    "rating_scoring_quiz": "• Tamamlanan tur → +10",
    "rating_scoring_reverse": "• Ters yön → +5",
    "rating_scoring_word": "• Öğrenilen kelime → +3",
    "rating_scoring_streak": "• Üst üste her gün bir öncekinden değerli, +10'a kadar",
    "rating_scoring_bonus": "• %60 üstü doğruluk — ne kadar yüksekse o kadar çok",
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
    "voice_not_ready_hint": "<i>· sesin yanındaysa henüz tamamı kaydedilmemiş: kelime anlık sentezlenir, bazen gecikmeli ya da sessiz gelir</i>",
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
    "settings_btn_channels": "🎮 Ders karışımı",
    "settings_channels_line": "🎮 Ders: <b>{channels}</b>",
    "channels_title": "🎮 <b>Ders karışımı</b>",
    "channels_description": "Hangi sorular sorulsun. Kanal ne kadar çoksa kelime o kadar iyi yerleşir: gözle tanımak, kulakla tanımak ve söylemek üç ayrı beceridir.",
    "channel_text": "🔤 Kart",
    "channel_audio": "🎧 Kulakla",
    "channel_speech": "🎤 Konuşma",
    "channels_text_always": "🔤 Kart kapatılamaz: tek kanalı olmayan ders boş ekran demektir.",
    "channels_audio_blocked": "🎧 Kulakla kullanılamıyor: seslendirme kapalı.",
    "channels_speech_soon": "🎤 Konuşma yakında geliyor.",
    "channels_need_one": "En az bir kanal açık kalmalı",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Bu kelimeyi yüksek sesle söyle — sesli mesaj kaydet",
    "speech_btn_reference": "🔊 Dinle",
    "speech_btn_skip": "⏭ Atla",
    "speech_listening": "🎧 Dinliyorum…",
    "speech_heard": "Duydum: <i>{heard}</i>",
    "speech_not_understood": "🤔 Anlayamadım. Tekrar kaydet — mikrofona yakın ve biraz daha yüksek sesle.",
    "speech_send_voice": "🎤 Bu soru sesli mesajla cevaplanır. Mikrofon düğmesine basılı tut.",
    "speech_skipped": "⏭ Atlandı",
    "quiz_result_spoken": "🎤 Sesli: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Yazılı",
    "home_scale_audio": "Duyarak",
    "home_scale_speech": "Sesli",
    "home_btn_learn": "▶️ Çalış · {count}",
    "home_streak": "🔥 seri: {days}",
    "home_rank": "🏆 sıra: {rank}",
    "home_hint": "Çubuk, daha önce karşılaştığın kelimelerin payıdır: bir kanaldan üç doğru cevap ve kelime o kanalın hanesine yazılır. Ölçekler arasındaki fark, neyin eksik olduğunu gösterir.",
    "home_channel_not_ready": "{channel}: henüz erken. Hazır kelime sayısı {ready}, en az {minimum} gerekiyor. Kartlarla çalış — diğer kanalları onlar açıyor.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "🎯 Ne öğreniyorum",
    "settings_group_what_title": "<b>🎯 Ne öğreniyorum</b>",
    "settings_group_how": "🎮 Nasıl öğreniyorum",
    "settings_group_how_title": "<b>🎮 Nasıl öğreniyorum</b>",
    "settings_group_bot": "🔧 Bot",
    "settings_group_bot_title": "<b>🔧 Bot</b>",
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
    "quiz_btn_one_more": "▶️ Bir tur daha",
    "home_btn_stats": "📊 Ayrıntılar",
    "notif_off_how_to_return": "Geri açmak için: ⚙️ Ayarlar → 🔧 Bot → 🔔 Hatırlatıcılar",
    "reminder_offer": "🔔 Günde bir kez hatırlatayım mı? Öğrendiklerini kaybetmemek böyle daha kolay — seri de kopmaz.",
    "reminder_offer_yes": "🔔 Evet, hatırlat",
    "reminder_offer_no": "Gerek yok",
    "reminder_offer_done": "🔔 Tamam. Saati ve günleri ayarlardan değiştirebilirsin.",
    "level_offer": "📈 <b>{current}</b> seviyesinde neredeyse hiç hata yapmıyorsun. <b>{following}</b> seviyesine geçelim mi? Öğrendiklerin sende kalır.",
    "level_offer_yes": "📈 Evet, {following} seviyesine geç",
    "level_offer_no": "Burada kalayım",
    "level_offer_done": "📈 Seviye <b>{following}</b>. Kelimeler artık daha zor olacak.",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "Dili ne için öğreniyorsun? Kelimeleri ona göre seçeriz.",
    "goal_work": "💼 İş için",
    "goal_travel": "✈️ Seyahat için",
    "goal_living": "🏠 Yurt dışında yaşamak için",
    "goal_study": "🎓 Okumak için",
    "goal_any": "📚 Sadece kelime öğrenmek",
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
    "intro_title": "🌍 <b>GenauLingua</b>",
    "intro_three_games": "Bir kelime tek değil, üç ayrı beceridir:\n🔤 yazılı hâlini tanımak\n🎧 duyarak tanımak\n🎤 yüksek sesle söylemek\n\nDerste kendiliğinden dönüşümlü gelirler — her kelimeyi ne kadar bildiğine göre.",
    "intro_numbers": "12 902 kelime · 20 konu · 6 seviye\nAltı dil, istediğin eşleşmede: dilersen Lehçeyi İngilizce üzerinden öğren.",
    "intro_where_you_are": "Şu anda: <b>{language}</b> · {mode}",
    "intro_btn_progress": "📊 İlerleme",
    "settings_title_short": "🦾 Ayarlar",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "🧭 Ne için öğreniyorum",
    "settings_goal_title": "🧭 <b>Ne için öğreniyorum</b>",
    "settings_goal_description": "Konunun kelimeleri önce gelir. Zorluk yine seviyene göre belirlenir, öğrendiklerin de tekrara dönmeye devam eder.",
    "settings_goal_set": "Hedef kaydedildi",
    "settings_goal_line": "🧭 Hedef: <b>{goal}</b>",
    "settings_goal_none": "seçilmedi",
})
