"""Вычитка немецкого, порция p026 (B1–B2), 23.10: заглушки и канцелярит → живые бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    18415: (W, ex("Psst, im Nebenzimmer schläft das Baby",
        "Тсс, в соседней комнате спит малыш", "Тсс, у сусідній кімнаті спить малюк",
        "Shh, the baby's asleep in the next room", "Şşş, yan odada bebek uyuyor",
        "Ciii, w pokoju obok śpi dziecko", "Sss, nella stanza accanto dorme il bambino",
        "Chis, en la habitación de al lado duerme el bebé", "Chut, le bébé dort dans la pièce d'à côté",
        "Pst, ve vedlejším pokoji spí miminko")),
    1399: (W + "; «Man erstattet die Kosten» — канцелярит", ex("Die Firma erstattet mir die Fahrtkosten zum Kunden",
        "Фирма возмещает мне расходы на дорогу к клиенту", "Фірма відшкодовує мені витрати на дорогу до клієнта",
        "The company refunds my travel costs to the client", "Şirket müşteriye gidiş masraflarımı geri ödüyor",
        "Firma zwraca mi koszty dojazdu do klienta", "L'azienda mi rimborsa le spese di viaggio dal cliente",
        "La empresa me reembolsa el viaje hasta el cliente", "L'entreprise me rembourse les frais de déplacement chez le client",
        "Firma mi proplácí cestovné ke klientovi")),
    1461: (W + "; «öffentliche Sicherheit» — канцелярит", ex("Wer beim Fahren aufs Handy schaut, gefährdet alle",
        "Кто за рулём смотрит в телефон, ставит под угрозу всех", "Хто за кермом дивиться в телефон, наражає на небезпеку всіх",
        "Anyone who looks at their phone while driving puts everyone at risk", "Araba kullanırken telefona bakan herkesi tehlikeye atar",
        "Kto podczas jazdy patrzy w telefon, naraża wszystkich", "Chi guarda il cellulare mentre guida mette in pericolo tutti",
        "Quien mira el móvil al volante pone en peligro a todos", "Celui qui regarde son portable en conduisant met tout le monde en danger",
        "Kdo se při řízení dívá do mobilu, ohrožuje všechny")),
    7088: (W, ex("Durch das kaputte Dach ist Wasser in die Wohnung eingedrungen",
        "Через дырявую крышу в квартиру проникла вода", "Через дірявий дах у квартиру проникла вода",
        "Water got into the flat through the damaged roof", "Kırık çatıdan daireye su sızdı",
        "Przez dziurawy dach do mieszkania dostała się woda", "Dal tetto rotto è entrata acqua in casa",
        "Por el tejado roto ha entrado agua en el piso", "L'eau a pénétré dans l'appartement par le toit abîmé",
        "Rozbitou střechou pronikla do bytu voda")),
}

REPLACE = []

SPLIT_LATER = {}
