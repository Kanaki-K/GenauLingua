"""
Правка по примете scan_tr_separate_idi: турецкое `idi` отдельным словом.

43 ячейки по всей базе. 38 из них закрываются склейкой, которую
примета считает сама. Остальные пять трогать одной склейкой нельзя —
там рядом с `idi` сидит второй дефект, и беглая замена суффикса его бы
законсервировала:

  * 8702 `Onun tepkisi tamamen öngörülemeyen idi` — `öngörülemeyen`
    это причастие «непредсказуемый который», и сказуемым оно не
    становится ни с каким суффиксом. Нужно `öngörülemezdi`.
  * 11513 `Yemek o kadar duyarlı ve aromatik idi` — `duyarlı` значит
    «чувствительный» о человеке; о еде так не говорят, а `sinnlich`
    здесь про вкус.
  * 11977 `Yemek tatsız ve iştahsız idi` — `iştahsız` значит «без
    аппетита», и это свойство едока, а не еды.
  * 16846 `Hükümet tarafından sansür savaş sırasında çok katı idi` —
    `Hükümet tarafından` оторвано от своего слова и повисло в начале.
  * 16159 `Başkan yardımcısı konferansta idi` — склейка верна, но
    `konferanstaydı` теряет `zugegen` из немецкого; поставлено
    `konferansta hazır bulunuyordu`.

Это и есть причина, по которой примета только предлагает форму, а не
правит сама: в каждой восьмой ячейке правильная склейка была бы
неправильной правкой.

    python -m app.scripts.fix_tr_separate_idi            # показать
    python -m app.scripts.fix_tr_separate_idi --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

GLUED: list[tuple[int, str, str]] = [
    (2284, "O bir hakaret idi", "O bir hakaretti"),
    (2351, "Bu saçma bir fikir idi", "Bu saçma bir fikirdi"),
    (6928, "Ziyaretçi sayısı çok fazla idi",
     "Ziyaretçi sayısı çok fazlaydı"),
    (7064, "Kötü haberin ardından tamamen müteessir idi",
     "Kötü haberin ardından tamamen müteessirdi"),
    (7065, "Parti için orijinal bir fikir idi",
     "Parti için orijinal bir fikirdi"),
    (8410, "Su kirli idi ve içilemezdi", "Su kirliydi ve içilemezdi"),
    (8488, "Kırılmış vazo yerde yatıyordu – bu bir aile mirası idi",
     "Kırılmış vazo yerde yatıyordu – bu bir aile mirasıydı"),
    (8503, "Yavru kedi, büyük gözleriyle çok sevimli idi",
     "Yavru kedi, büyük gözleriyle çok sevimliydi"),
    (8614, "Gün batışının parlayan renkleri harika idi",
     "Gün batışının parlayan renkleri harikaydı"),
    (8651, "Alan geniş ve iyi bakımlı idi",
     "Alan geniş ve iyi bakımlıydı"),
    (8654, "Konser eşsiz güzellikte idi", "Konser eşsiz güzellikteydi"),
    (8663, "Daha kapsamlı bir soruşturma gerekli idi",
     "Daha kapsamlı bir soruşturma gerekliydi"),
    (8687, "Eski bodrum sıçan deliği gibi karanlık ve kirli idi",
     "Eski bodrum sıçan deliği gibi karanlık ve kirliydi"),
    (8701, "Savaş gemisi en güçlü askeri gemi idi",
     "Savaş gemisi en güçlü askeri gemiydi"),
    (8967, "Bu şirketin kurucusu bir deha idi",
     "Bu şirketin kurucusu bir dehaydı"),
    (9281, "Onun askeri rütbesi albay idi",
     "Onun askeri rütbesi albaydı"),
    (10382, "Hava kasvetli ve gri idi", "Hava kasvetli ve griydi"),
    (10384, "Bu samimi bir özür idi", "Bu samimi bir özürdü"),
    (11176, "Canavarın görünüşü korkutucu idi",
     "Canavarın görünüşü korkutucuydu"),
    (11317, "Bilgiye hevesli idi", "Bilgiye hevesliydi"),
    (11388, "Onun davranışı tamamen onursuz ve utanç verici idi",
     "Onun davranışı tamamen onursuz ve utanç vericiydi"),
    (11501, "Onun cevabı kaba ve sert idi", "Onun cevabı kaba ve sertti"),
    (11532, "Onun dürüstlüğü tartışılmaz idi",
     "Onun dürüstlüğü tartışılmazdı"),
    (11609, "Onun neşeliliği bulaşıcı idi", "Onun neşeliliği bulaşıcıydı"),
    (11998, "Onun içki alışkanlığı hayatının en büyük sorunu idi",
     "Onun içki alışkanlığı hayatının en büyük sorunuydu"),
    (12941, "Operasyondan sonra kan kaybı kritik idi",
     "Operasyondan sonra kan kaybı kritikti"),
    (13071, "Sarhoş idi ve zorlukla yürüyebiliyordu",
     "Sarhoştu ve zorlukla yürüyebiliyordu"),
    (13126, "Tanı beyin tümörü idi", "Tanı beyin tümörüydü"),
    (13129, "Beyin hasarı ciddi idi", "Beyin hasarı ciddiydi"),
    (13152, "Bu onun için travmatik bir deneyim idi",
     "Bu onun için travmatik bir deneyimdi"),
    (15321, "Onunla olan flörtü zararsız ve eğlenceli idi",
     "Onunla olan flörtü zararsız ve eğlenceliydi"),
    (15831, "Bu yaz sivrisinekler özellikle berbat idi",
     "Bu yaz sivrisinekler özellikle berbattı"),
    (16204, "Yaralanma ciddi idi ve hastaneye gitmeliydi",
     "Yaralanma ciddiydi ve hastaneye gitmesi gerekti"),
    (16206, "Kötü davranışı için verilen ceza çok katı idi",
     "Kötü davranışı için verilen ceza çok katıydı"),
    (16825, "Sınır bölgesi iki ülke arasında kimsenin toprağı idi",
     "Sınır bölgesi iki ülke arasında kimsenin toprağıydı"),
    (16830, "Partiye yeniden giriş tartışmalı idi",
     "Partiye yeniden girişi tartışmalıydı"),
    (16918, "Polis başkanlığı çok meşgul idi",
     "Polis başkanlığı çok meşguldü"),
    (18767, "Olayların seyri tuhaf idi", "Olayların seyri tuhaftı"),
]

BY_HAND: list[tuple[int, str, str, str]] = [
    (8702, "Onun tepkisi tamamen öngörülemeyen idi",
     "Onun tepkisi tamamen öngörülemezdi",
     "«öngörülemeyen» это причастие, сказуемым не бывает"),
    (11513, "Yemek o kadar duyarlı ve aromatik idi ki ağzım sulandı",
     "Yemek o kadar lezzetli ve aromatikti ki ağzım sulandı",
     "«duyarlı» о человеке, а не о еде"),
    (11977, "Yemek tatsız ve iştahsız idi",
     "Yemek tatsız ve yavandı",
     "«iştahsız» это свойство едока, а не еды"),
    (16846, "Hükümet tarafından sansür savaş sırasında çok katı idi",
     "Savaş sırasında hükümetin sansürü çok katıydı",
     "«Hükümet tarafından» оторвано от своего слова"),
    (16159, "Başkan yardımcısı konferansta idi",
     "Başkan yardımcısı konferansta hazır bulunuyordu",
     "склейка верна, но теряет «zugegen» из эталона"),
]

FIXES: list[tuple[int, str, str, str, str]] = (
    [(i, "example_tr", a, b, "турецкое «idi» отдельным словом")
     for i, a, b in GLUED]
    + [(i, "example_tr", a, b, why) for i, a, b, why in BY_HAND]
)


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
