"""Сквозная правка по примете scan_formality_vs_de.

Вся база: 21 ячейка, где немецкий эталон обращается на «du», а турецкий
перевод отвечает вежливым множественным. Везде правится турецкая
сторона — эталон задаёт обращение.

Два случая стоит отметить.

`auslassen` (7569) расходился дважды в одной фразе: «Raporunuzda ...
atladınız» — и притяжательное, и глагол во вежливом. Правится целиком.

`anschnallen` (17204) кроме обращения потерял «Vergiss nicht»:
немецкий просит не забыть, турецкий просто велел пристегнуться.
Исправлено и то и другое.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (358, "example_tr",
     "Ailenize selamlar",
     "Ailene selamlar",
     "эталон «an deine Familie» — на «ты»"),
    (518, "example_tr",
     "Tükenmez kaleminizi kullanabilir miyim?",
     "Tükenmez kalemini kullanabilir miyim?",
     "эталон «deinen Kugelschreiber»"),
    (1374, "example_tr",
     "Benim için bir tavsiyeniz var mı?",
     "Benim için bir tavsiyen var mı?",
     "эталон «Hast du eine Empfehlung»"),
    (1632, "example_tr",
     "Müşteri numaranız nedir?",
     "Müşteri numaran nedir?",
     "эталон «deine Kundennummer»"),
    (1845, "example_tr",
     "Ayakkabı numaranız kaç?",
     "Ayakkabı numaran kaç?",
     "эталон «Welche Schuhgröße hast du»"),
    (1995, "example_tr",
     "Burada aktarma yapmanız gerekiyor",
     "Burada aktarma yapman gerekiyor",
     "эталон «Du musst hier umsteigen»"),
    (2310, "example_tr",
     "Lütfen biniş kartınızı gösterin",
     "Lütfen biniş kartını göster",
     "эталон «Zeig mir bitte deine Bordkarte»"),
    (7233, "example_tr",
     "Arabanız çıkışı engelliyor",
     "Araban çıkışı engelliyor",
     "эталон «Dein Auto»"),
    (7340, "example_tr",
     "Bu yöntemi projenizde uygulamanız gerekiyor",
     "Bu yöntemi projende uygulaman gerekiyor",
     "эталон «in deinem Projekt» и «Du musst»"),
    (7569, "example_tr",
     "Raporunuzda önemli bir noktayı atladınız",
     "Raporunda önemli bir noktayı atladın",
     "расхождение дважды в одной фразе: и притяжательное, и глагол"),
    (8588, "example_tr",
     "Ölçümünüz hatalıydı",
     "Ölçümün hatalıydı",
     "эталон «Deine Messung»"),
    (11027, "example_tr",
     "Ziyaretiniz her zaman hoş karşılanır",
     "Ziyaretin her zaman hoş karşılanır",
     "эталон «Dein Besuch»"),
    (13975, "example_tr",
     "Açıklamanız çok açıktı ve her şeyi anladım",
     "Açıklaman çok açıktı ve her şeyi anladım",
     "эталон «Deine Erklärung»"),
    (14054, "example_tr",
     "Talebiniz nedir? Sadece söyleyin",
     "Talebin nedir? Sadece söyle",
     "эталон «dein Anliegen» и «Sprich»"),
    (14164, "example_tr",
     "Lütfen buraya imzanızı atın",
     "Lütfen buraya imzanı at",
     "эталон «unterschreib hier mit deiner Signatur»"),
    (16230, "example_tr",
     "Kurala uymanız gerekir",
     "Kurala uyman gerekir",
     "эталон «Du musst die Vorschrift beachten»"),
    (17204, "example_tr",
     "Gitmeden önce emniyet kemerinizi takın",
     "Yola çıkmadan önce emniyet kemerini takmayı unutma",
     "обращение и потерянное «Vergiss nicht»"),
    (17654, "example_tr",
     "Bu cihaz resimleri duvara düz bir şekilde asmanıza yardım eder",
     "Bu cihaz resimleri duvara düz bir şekilde asmana yardım eder",
     "эталон «hilft dir»"),
    (17703, "example_tr",
     "Şifreleme verilerinizi korur",
     "Şifreleme verilerini korur",
     "эталон «deine Daten»"),
    (18723, "example_tr",
     "Kiranızın vadesi çoktan geçti",
     "Kiranın vadesi çoktan geçti",
     "эталон «Deine Miete»"),
    (18804, "example_tr",
     "Ziyaretiniz o anda benim için oldukça uygunsuzdu",
     "Ziyaretin o anda benim için oldukça uygunsuzdu",
     "эталон «Dein Besuch»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
            print(f"  зачем: {why}")
        print("\nсухой прогон. применить: --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(
                text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now:
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
