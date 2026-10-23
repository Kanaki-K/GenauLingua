"""Вычитка турецкого, порция p002 (A1), 23.10: кальки и книжные обороты → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    554: (T + "«yatakta yatıp» — тавтология", {"example_tr": "Yatakta uzanmış kitap okuyorum"}),
    598: (T + "«Lütfen ekmek getir» — без «mit»", {"example_tr": "Gelirken ekmek de getir lütfen"}),
    599: (T + "«Öğle yemeğini yiyoruz» — лишний аккузатив", {"example_tr": "Öğle yemeği yiyoruz"}),
    608: (T + "в примере «bir dakika», а слово дано только как «an»", {"translation_tr": "an, dakika"}),
    663: (T + "«Şimdi ne yapıyoruz?» — «что мы сейчас делаем», а не «что будем делать»", {"example_tr": "Şimdi ne yapacağız?"}),
    755: (T + "«Pirinç pişiriyorum» — так не говорят", {"example_tr": "Pilav yapıyorum"}),
    892: (T + "студент — «üniversite öğrencisi»", {"example_tr": "Kardeşim Münih'te üniversite öğrencisi"}),
    1007: (T + "«Ne istiyorsunuz?» — грубо для продавца", {"example_tr": "Ne alırdınız?"}),
    1066: (T + "«Hesabı ödemek istiyoruz» — подстрочник", {"example_tr": "Ödemek istiyoruz, hesabı getirir misiniz?"}),
    1182: (T + "«Bir gezi yapıyoruz» — калька", {"example_tr": "Geziye çıkıyoruz"}),
    1266: (T + "«Bir su sipariş ediyorum» — так не заказывают", {"example_tr": "Ben bir su sipariş edeyim"}),
}

REPLACE = []

SPLIT_LATER = {}
