"""ВТОРОЙ ПРОХОД, блок 4 (ряды 601–800): правки, найденные глазами.

ГЛАВНОЕ В БЛОКЕ — НЕ ПРАВКА, А ОТКАТ. В блоке 3 я исправил
`Folg mir bitte` → `Folge mir bitte`, сослался на «правило базы: в
эталоне усечений нет» и закоммитил. Блок 4 дал подряд ещё три таких
ряда (`Bitte zahl hier`, `Wart mal eine Sekunde`, `Steck den Stecker
in die Steckdose`), и четыре ряда одного вида — это класс. А класс
по правилу надо не править по одному, а замерять по всей базе.

Замер (`scan_de_bare_imperative`) показал:

    повелительное без «-e»:  99
    повелительное с  «-e»:   41

Голая основа — не выброс, а НОРМА базы, и норма немецкой речи:
`Mach die Tür auf`, `Sag das noch mal`, `Zeig mir den Weg`,
`Pass auf`, `Hör auf`, `Hol bitte den Eimer`. Написать «Mache die Tür
auf» или «Passe auf» значит сделать эталон деревянным. Хуже того, база
пишет один и тот же глагол двояко: `Steck` четыре раза против `Stecke`
один, `Zeig` четыре против `Zeige` один, `Hör auf` восемь против
`Höre auf` один.

Значит «правила базы», на которое я ссылался, не существует — я вывел
его из одного примера и применил к верной строке. Ряд 1433 возвращён
как был.

ЧТО ПРИ ЭТОМ ОКАЗАЛОСЬ НАСТОЯЩЕЙ ОШИБКОЙ — ровно один ряд из четырёх:

    Sekunde (18610)  «Wart mal eine Sekunde»  → Warte

У `warten` основа кончается на «-t», и там «-e» не стиль, а
обязательная часть формы: голого `wart` в немецком нет вовсе — это
прошедшее от `sein` («Wo wart ihr?»). Именно из-за этой двусмысленности
`wart` нарочно выброшено из `scan_de_imperative`, и ряд провалился
между двумя приметами. Новый замер снимает двусмысленность позицией:
в «Wo wart ihr?» слово стоит вторым, а не в начале фразы. Поэтому
подмножество «форм, которых в немецком нет» сделано ГЕЙТОМ — по базе
даёт 1 ряд, после правки ноль.

`Bitte zahl hier` и `Steck den Stecker…` оставлены как есть: у `zahlen`
и `stecken` «-e» необязательно.

Остальное обычное. Отдельно стоит отметить два:

    rechts (748)  de «Biege rechts ab» (du)  tr «Sağa dönün» (вы)
        Обращение расходится с эталоном, и `scan_formality_vs_de` это
        не поймала: та примета требует, чтобы в немецком стояло явное
        `du`/`dein`/`dich`/`dir`, а у повелительного местоимения нет
        вовсе. Дыра записана в HANDOVER, класс не сметён.

    Karte (738/462)  en и tr перевели «карту» как MAP, pl — как CARD
        Один и тот же ряд учит двум разным словам в зависимости от
        языка ученика. Немецкое «die Karte» двусмысленно, большинство
        (en, tr, ru, uk) выбрало карту-карту географическую — польский
        приведён к большинству.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── ОТКАТ СОБСТВЕННОЙ ПРАВКИ БЛОКА 3 ─────────────────────────
    (1433, "example_de",
     "Folge mir bitte",
     "Folg mir bitte",
     "замер: голая основа — норма базы (99 против 41) и норма речи; правил верное"),

    # ── форма, которой в немецком нет ────────────────────────────
    (18610, "example_de",
     "Wart mal eine Sekunde",
     "Warte mal eine Sekunde",
     "у warten «-e» обязательно: голое wart это прошедшее от sein"),

    # ── эталон: ненатуральный немецкий ───────────────────────────
    (10088, "example_de",
     "Ich glaube an keinen Geist",
     "Ich glaube nicht an Geister",
     "по-немецки так не говорят; все пять переводов и так во множественном"),
    (18113, "example_de",
     "Ich bleibe heute zu Hause",
     "Ich bleibe heute zuhause",
     "слово ряда «zuhause», а пример писал его раздельно: ученик видит одно, слышит другое"),

    # ── обращение расходится с эталоном ──────────────────────────
    (748, "example_tr",
     "Sağa dönün",
     "Sağa dön",
     "эталон «Biege rechts ab» на «ты», турецкий отвечал на «вы»"),

    # ── подменённый или потерянный смысл ─────────────────────────
    (6330, "example_tr",
     "İki haftadır burada değil",
     "İki hafta için gitmiş",
     "«İki haftadır» это «уже две недели как», а в эталоне отъезд НА две недели"),
    (6330, "translation_ru",
     "прочь, вон, далее, дальше",
     "прочь, в отъезде, вон, далее, дальше",
     "значения примера («в отъезде») в списке не было, и карточка показывала «прочь»"),
    (6330, "translation_uk",
     "геть, далі",
     "геть, у від'їзді, далі",
     "то же"),
    (6344, "example_tr",
     "Buna bakabilir misin?",
     "Buna bakmak ister misin?",
     "«-abilir misin» это können, а в эталоне «Willst du» — wollen"),
    (15936, "example_pl",
     "Jej Wysokość jest tutaj",
     "Jej Majestat jest tutaj",
     "«Wysokość» это Высочество, а Majestät — Величество: разные титулы"),
    (6360, "example_tr",
     "Para gizli",
     "Para saklı",
     "«gizli» это тайный, а «versteckt» — спрятанный; «saklı» есть в переводе"),
    (462, "example_pl",
     "Gdzie jest karta?",
     "Gdzie jest mapa?",
     "en, tr, ru и uk поняли «Karte» как карту географическую, польский — как карточку"),
    (10079, "example_uk",
     "Бідна дитина залишилася без сім'ї",
     "Бідна дитина не має сім'ї",
     "«залишилася без» это событие, а «hat keine Familie» — состояние"),
    (13394, "example_pl",
     "Wpadnij do mnie na chwilę",
     "Przyjdź tutaj do mnie",
     "«na chwilę» в эталоне нет, зато потеряно «rüber» — слово ряда"),
    (10084, "example_pl",
     "To naprawdę dobra dusza",
     "On to dobra dusza",
     "«naprawdę» в эталоне нет, и подлежащее там «Er», а не «To»"),

    # ── русизм в украинском ──────────────────────────────────────
    (1475, "example_uk",
     "Суд приймає рішення по справі",
     "Суд приймає рішення у справі",
     "«по справі» калька с русского: по-украински «у справі»"),

    # ── время глагола ────────────────────────────────────────────
    (1859, "example_uk",
     "Я зроблю це сам",
     "Я роблю це сам",
     "будущее против «Ich mache das selber»; в ru, tr и en настоящее"),
    (1859, "example_pl",
     "Zrobię to sam",
     "Robię to sam",
     "то же"),
    (18113, "example_ru",
     "Сегодня я останусь дома",
     "Сегодня я остаюсь дома",
     "будущее против «Ich bleibe»; в uk, tr, pl и en настоящее"),

    # ── потерянное слово ─────────────────────────────────────────
    (13389, "example_tr",
     "Yağmur yağmasına rağmen gidiyorum",
     "Yağmur yağmasına rağmen dışarı çıkıyorum",
     "потеряно «raus»: в эталоне выходят на улицу, а не просто идут"),
    (945, "example_tr",
     "Hoşça kal",
     "Hoşça kal, yarın görüşürüz",
     "потеряно «bis morgen»: в остальных пяти языках оно есть"),
    (18115, "example_ru",
     "Я иду домой",
     "Я сейчас иду домой",
     "потеряно «jetzt»: в en, uk, tr и pl оно есть"),
    (318, "example_en",
     "The café is opposite",
     "The café is opposite me",
     "потеряно «mir»: в ru, uk, tr и pl оно есть"),
    (1396, "example_en",
     "I still have something to take care of",
     "I still have to take care of something quickly",
     "потеряно «schnell»: в ru, uk и pl оно есть"),
    (1396, "example_tr",
     "Hâlâ halletmem gereken bir şey var",
     "Hızlıca bir şey daha halletmem gerek",
     "то же"),

    # ── добавленное слово ────────────────────────────────────────
    (2749, "example_pl",
     "To jest już załatwione",
     "To jest załatwione",
     "«już» в эталоне нет: «Das ist geregelt»"),
    (282, "example_tr",
     "Fotoğraf çok tatlı",
     "Fotoğraf tatlı",
     "«çok» в эталоне нет: «Das Foto ist süß»"),
    (6366, "example_ru",
     "Это просто прекрасно",
     "Это прекрасно",
     "«просто» в эталоне нет: «Das ist wunderschön»"),
    (1720, "example_ru",
     "Я не могу прийти, дело в том, что я болен",
     "Я не могу, дело в том, что я болен",
     "«прийти» в эталоне нет: «Ich kann nicht»"),
    (10102, "example_pl",
     "Ten film jest naprawdę zabawny",
     "Ten film jest bardzo zabawny",
     "«naprawdę» это «действительно», а в эталоне «sehr» — очень"),

    # ── по-людски ────────────────────────────────────────────────
    (784, "example_ru",
     "Это жаль",
     "Это досадно",
     "«это жаль» по-русски не говорят; «досадно» есть в переводе"),
    (784, "example_uk",
     "Це шкода",
     "Це прикро",
     "то же по-украински; «прикро» есть в переводе"),
    (784, "example_tr",
     "Çok yazık",
     "Ne yazık",
     "«çok» в эталоне нет, а «ne yazık» есть в переводе"),
    (10075, "example_uk",
     "Це було дурістю з мого боку",
     "Це було нерозумно з мого боку",
     "существительное вместо наречия: карточка показывала «дурний», пример говорил «дурістю»"),
    (18606, "example_uk",
     "Я вже деякий час чекаю",
     "Я вже якийсь час чекаю",
     "карточка показывала «якийсь час», пример говорил «деякий»"),

    # ── знак, которого нет ни в эталоне, ни у других ─────────────
    (10097, "example_ru",
     "Ах ты боже мой!",
     "Ах ты боже мой",
     "восклицательного знака нет ни в эталоне, ни в en, tr, pl"),
    (10097, "example_uk",
     "Ах ти Боже мій!",
     "Ах ти Боже мій",
     "то же"),
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
