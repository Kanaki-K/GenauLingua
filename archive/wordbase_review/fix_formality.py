"""
Немецкий на «ты», перевод на «Вы» — 35 ячеек. И четыре наоборот.

Класс нашёлся вычиткой: в анкетных словах («Adresse», «Beruf», «Vorname»,
«Nachname», «Größe») ряды с этим дефектом шли подряд. Сплошной поиск
`scan_formality` показал весь объём: почти всё турецкое.

Почему это дефект, а не придирка. Ряд «Wie fühlst du dich?» посвящён
обращению на «ты» — это его грамматическая суть. Перевод «Nasıl
hissediyorsunuz?» учит вежливой форме, которой в эталоне нет, и человек
запоминает не то спряжение. На карточке пара стоит стопкой, и разнобой виден.

ЧТО ПРОВЕРКА ОТКАЗАЛАСЬ СУДИТЬ. Польское «Ta pani czeka na ciebie» она
пометила, и зря: «pani» здесь существительное «дама», а не вежливое
обращение. Немецкое «Die Dame wartet auf dich» переведено верно. Этот ряд
в правку не включён — различить honorific от существительного формально
нельзя, а ломать верную строку нельзя тем более.

    python -m app.scripts.fix_formality            # показать
    python -m app.scripts.fix_formality --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- турецкий: «Вы» вместо «ты» -------------------------------------------
    (101, "example_tr", "Size hızlı iyileşmeler diliyorum",
     "Sana acil şifalar diliyorum",
     "в немецком «dir» — тебе; и по-турецки так желают выздоровления"),
    (111, "example_tr", "Nasıl ödemek istersiniz?", "Nasıl ödemek istersin?",
     "в немецком «du» — ты"),
    (245, "example_tr", "Şoför sizi bekliyor", "Şoför seni bekliyor",
     "в немецком «dich» — тебя"),
    (302, "example_tr", "Nasıl hissediyorsunuz?", "Nasıl hissediyorsun?",
     "в немецком «du» — ты"),
    (341, "example_tr", "Bir içecek ister misiniz?", "Bir içecek ister misin?",
     "в немецком «du» — ты"),
    (731, "example_tr", "Denemek ister misiniz?", "Denemek ister misin?",
     "в немецком «du» — ты"),
    (865, "example_tr", "Hangi dili öğreniyorsunuz?",
     "Hangi dili öğreniyorsun?", "в немецком «du» — ты"),
    (973, "example_tr", "Sizi bağlıyorum", "Seni patronla bağlıyorum",
     "в немецком «dich» и «с начальником»"),
    (1024, "example_tr", "Hangi kitabı istiyorsunuz?",
     "Hangi kitabı istiyorsun?", "в немецком «du» — ты"),
    (1051, "example_tr", "Nereden geliyorsunuz?", "Nereden geliyorsun?",
     "в немецком «du» — ты"),
    (1080, "example_tr", "Ne kadar şeker istersiniz?",
     "Kahvene ne kadar şeker istersin?",
     "в немецком «du» и «в твой кофе»"),
    (1249, "example_tr", "Tüm materyalleri size sağlıyoruz",
     "Tüm materyalleri sana sağlıyoruz", "в немецком «dir» — тебе"),
    (1253, "example_tr", "Hangi meslek alanında çalışıyorsunuz?",
     "Hangi meslek alanında çalışıyorsun?", "в немецком «du» — ты"),
    (1315, "example_tr", "Bayan sizi bekliyor", "Bayan seni bekliyor",
     "в немецком «dich» — тебя"),
    (1317, "example_tr", "Size teşekkür ederim", "Sana teşekkür ederim",
     "в немецком «dir» — тебе"),
    (1516, "example_tr", "Ana yemek olarak ne istersiniz?",
     "Ana yemek olarak ne istersin?", "в немецком «du» — ты"),
    (1556, "example_tr", "Sizi yarın bilgilendireceğim",
     "Seni yarın bilgilendireceğim", "в немецком «dich» — тебя"),
    (1709, "example_tr", "Bana bir örnek gösterebilir misiniz?",
     "Bana bir örnek gösterebilir misin?", "в немецком «du» — ты"),
    (2103, "example_tr", "Bunu tekrar eder misiniz?",
     "Bunu tekrar eder misin?", "в немецком «du» — ты"),
    (3009, "example_tr", "Size yardımcı olabilir miyim?",
     "Sana yardımcı olabilir miyim?", "в немецком «dir» — тебе"),
    (6785, "example_tr", "Pardon, sizi kısaca kesebilir miyim?",
     "Pardon, seni kısaca kesebilir miyim?", "в немецком «dich» — тебя"),
    (8434, "example_tr", "Odanız için herhangi bir renk seçebilirsiniz",
     "Odan için herhangi bir renk seçebilirsin", "в немецком «du» — ты"),
    (10361, "example_tr", "Size yardımcı olabilir miyim?",
     "Sana yardımcı olabilir miyim?", "в немецком «dir» — тебе"),
    (10526, "example_tr",
     "Neden benden yeni işiniz olduğunu gizliyorsunuz?",
     "Neden yeni bir işin olduğunu benden gizliyorsun?",
     "в немецком «du» — ты; и порядок слов"),
    (11549, "example_tr", "Başarınız için sizi tebrik etmek istiyorum",
     "Başarın için seni tebrik etmek istiyorum", "в немецком «dich» — тебя"),
    (13908, "example_tr", "Randevuyu onaylayabilir misiniz?",
     "Randevuyu onaylayabilir misin?", "в немецком «du» — ты"),
    (13956, "example_tr", "Pardon, bunu tekrar söyleyebilir misiniz?",
     "Pardon, bunu tekrar söyleyebilir misin?", "в немецком «du» — ты"),
    (14179, "example_tr", "Bunu başka türlü ifade edebilir misiniz?",
     "Bunu başka türlü ifade edebilir misin?", "в немецком «du» — ты"),
    (16749, "example_tr",
     "Burada park etmek yasaktır ve sizin için pahalı olur",
     "Burada park etmek yasaktır ve senin için pahalı olur",
     "в немецком «für dich» — для тебя"),
    (18348, "example_tr",
     "Bu otelde paranız karşılığında gerçekten çok rahat alıyorsunuz",
     "Bu otelde paran karşılığında gerçekten çok konfor alıyorsun",
     "в немецком «du» и «dein Geld»; и «rahat» вместо «konfor»"),

    # --- украинский: «Вы» вместо «ты» -----------------------------------------
    (359, "example_uk", "Який у Вас розмір?", "Який розмір тобі потрібен?",
     "в немецком «du» — ты, и «нужен», а не «есть»"),
    (636, "example_uk", "Яке Ваше прізвище?", "Яке твоє прізвище?",
     "в немецком «dein» — твоё"),
    (997, "example_uk", "Як Ваше ім’я?", "Як твоє ім'я?",
     "в немецком «dein» — твоё; и апостроф прямой, как в остальной базе"),
    (1093, "example_uk", "Ви взагалі хочете їсти?",
     "Ти взагалі хочеш їсти?", "в немецком «du» — ты"),
    (8588, "example_uk", "Ваше вимірювання було неточним",
     "Твоє вимірювання було неточним", "в немецком «deine» — твоё"),

    # --- наоборот: немецкий на «Вы», перевод на «ты» --------------------------
    (1816, "example_uk", "У мене є уточнювальне запитання до тебе",
     "Якщо будуть питання, дзвоніть",
     "в немецком «rufen Sie an» — звоните при вопросах"),
    (1816, "example_tr", "Sunumdan sonra ek soru sorabilirsiniz",
     "Ek sorularınız olursa arayın",
     "в немецком просят звонить при вопросах, презентации там нет"),
    (10197, "example_uk", "Я радий з тобою познайомитися",
     "Я радий з Вами познайомитися",
     "в немецком «Sie kennenzulernen» — на «Вы»"),
    (10197, "example_tr", "Seninle tanışmaktan memnunum",
     "Sizinle tanışmaktan memnunum",
     "в немецком «Sie kennenzulernen» — на «Вы»"),
    (9165, "example_tr", "Görevli sana yardım edecek",
     "Görevli sorularınızda size yardımcı olur",
     "в немецком «Ihnen bei Ihren Fragen» — на «Вы» и про вопросы"),
]


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

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
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
