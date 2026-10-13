"""
Разговорное усечение в НЕМЕЦКОМ ЭТАЛОНЕ: 88 ячеек по всей базе.

Класс нашёлся в блоках 26 и 27 (`Ich häng`, `Ich bring`, `Ich schüttel`,
`Ich brauch mal ne Auszeit`) и затем был выметен сплошь скриптом
`scan_de_colloquial`.

Почему это правится, хотя главное правило базы — «говорить по-людски».
«Ich hab keine Zeit» действительно так говорят, и в живой речи это не
ошибка. Но эталон здесь — не речь, а то, что ученик запоминает как
форму. Человек, который учит спряжение `haben`, увидит `hab` и выучит
форму, которую ему зачтут за ошибку. Поэтому окончание возвращается, а
сама разговорная лексика (`vergeigen`, `vermasseln`, `Gassi gehen`)
остаётся как есть: правится форма, а не регистр.

Что именно меняется:

* `Ich hab` → `Ich habe` и так далее по 48 слабым основам. `schüttel`
  даёт `schüttle` — у основ на `-el` выпадает «e».
* Усечённый артикль: `ne` → `eine`, `nen` → `einen`, `nem` → `einem`,
  `'ne` → `eine`, `so'n` → `so ein`.
* Одна строка поправлена вручную: `Nach der Arbeit brauch ich` — там
  обратный порядок, и правило «Ich <основа>» её не ловило.

Переводы не трогаются: смысл фразы не меняется, значит пять отражений
остаются верными.

    python -m app.scripts.fix_de_colloquial            # показать
    python -m app.scripts.fix_de_colloquial --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, слово ряда)
FIXES: list[tuple[int, str, str, str, str]] = [
    (176, "example_de", 'Ich mach einen Deutschkurs',
     'Ich mache einen Deutschkurs',
     "Deutschkurs"),
    (215, "example_de", 'Ich kauf mir eine Einzelfahrkarte',
     'Ich kaufe mir eine Einzelfahrkarte',
     "Einzelfahrkarte"),
    (525, "example_de", 'Berlin bis Potsdam ist ne Kurzstrecke',
     'Berlin bis Potsdam ist eine Kurzstrecke',
     "Kurzstrecke"),
    (752, "example_de", 'Ich fahr mit der Regionalbahn',
     'Ich fahre mit der Regionalbahn',
     "Regionalbahn"),
    (764, "example_de", 'Ich koch mir gerne Rindfleisch',
     'Ich koche mir gerne Rindfleisch',
     "Rindfleisch"),
    (876, "example_de", 'Ich brauch einen Stadtplan',
     'Ich brauche einen Stadtplan',
     "Stadtplan"),
    (883, "example_de", 'Ich hab mir die Stirn gestoßen',
     'Ich habe mir die Stirn gestoßen',
     "Stirn"),
    (911, "example_de", 'Ich kauf mir eine Tageskarte für die U-Bahn',
     'Ich kaufe mir eine Tageskarte für die U-Bahn',
     "Tageskarte"),
    (1078, "example_de", 'Ich geh zu Fuß nach Hause',
     'Ich gehe zu Fuß nach Hause',
     "zu Fuß"),
    (1112, "example_de", 'Ich hab einen guten Abschluss gemacht',
     'Ich habe einen guten Abschluss gemacht',
     "Abschluss"),
    (1222, "example_de", 'Ich spiel gern Basketball',
     'Ich spiele gern Basketball',
     "Basketball"),
    (1391, "example_de", "Ich hab's gestern erfahren",
     "Ich habe's gestern erfahren",
     "erfahren"),
    (1424, "example_de", 'Ich geh regelmäßig ins Fitness-Studio für meine Gesundheit',
     'Ich gehe regelmäßig ins Fitness-Studio für meine Gesundheit',
     "Fitness"),
    (1445, "example_de", 'Ich geh zum Frisör',
     'Ich gehe zum Frisör',
     "Frisör/in"),
    (1450, "example_de", 'Ich geh mit meinem Hund Gassi',
     'Ich gehe mit meinem Hund Gassi',
     "Gassi gehen"),
    (1459, "example_de", 'Ich brauch meine Geburtsurkunde',
     'Ich brauche meine Geburtsurkunde',
     "Geburtsurkunde"),
    (1587, "example_de", 'Ich kauf mir zwei Kinokarten für heute Abend',
     'Ich kaufe mir zwei Kinokarten für heute Abend',
     "Kinokarte"),
    (1697, "example_de", 'Ich schreib mir alles mit',
     'Ich schreibe mir alles mit',
     "mitschreiben"),
    (1727, "example_de", 'Ich hab den Newsletter abonniert',
     'Ich habe den Newsletter abonniert',
     "Newsletter"),
    (1755, "example_de", 'Ich komm persönlich vorbei',
     'Ich komme persönlich vorbei',
     "persönlich"),
    (1860, "example_de", 'Ich mach das selbst',
     'Ich mache das selbst',
     "selbst"),
    (1903, "example_de", 'Ich nehm mir Tee statt Kaffee',
     'Ich nehme mir Tee statt Kaffee',
     "statt"),
    (1929, "example_de", 'Ich geh auf einen Tanzkurs',
     'Ich gehe auf einen Tanzkurs',
     "Tanzkurs"),
    (2125, "example_de", 'Ich mach mir heute Zucchini',
     'Ich mache mir heute Zucchini',
     "Zucchini"),
    (2313, "example_de", 'Ich brauch neues Briefpapier fürs Büro',
     'Ich brauche neues Briefpapier fürs Büro',
     "Briefpapier"),
    (2474, "example_de", 'Das ist nur ne Formalität',
     'Das ist nur eine Formalität',
     "Formalität"),
    (2490, "example_de", 'Ich hab großen Frust, weil das Projekt gescheitert ist',
     'Ich habe großen Frust, weil das Projekt gescheitert ist',
     "Frust"),
    (2507, "example_de", 'Ich mach einen Gegenvorschlag',
     'Ich mache einen Gegenvorschlag',
     "Gegenvorschlag"),
    (2627, "example_de", 'Ich kauf mir neue Kosmetik',
     'Ich kaufe mir neue Kosmetik',
     "Kosmetik"),
    (2918, "example_de", 'Ich hab einen unbefristeten Vertrag',
     'Ich habe einen unbefristeten Vertrag',
     "unbefristet"),
    (2931, "example_de", 'Ich hab noch 10 Urlaubstage',
     'Ich habe noch 10 Urlaubstage',
     "Urlaubstag"),
    (2998, "example_de", 'Ich hab so viel in meinen Warenkorb gelegt',
     'Ich habe so viel in meinen Warenkorb gelegt',
     "Warenkorb"),
    (3071, "example_de", 'Ich hab eine Zusatzqualifikation',
     'Ich habe eine Zusatzqualifikation',
     "Zusatzqualifikation"),
    (6212, "example_de", 'Ich hab die ganze Zeit gewartet',
     'Ich habe die ganze Zeit gewartet',
     "ganz"),
    (6301, "example_de", 'Ich hab das Buch genommen',
     'Ich habe das Buch genommen',
     "genommen"),
    (6397, "example_de", 'Ich hab mich entschieden',
     'Ich habe mich entschieden',
     "entschieden"),
    (6460, "example_de", 'Ich hab einiges zu erledigen',
     'Ich habe einiges zu erledigen',
     "einiges"),
    (6584, "example_de", 'Ich hab die Wahrheit herausgefunden',
     'Ich habe die Wahrheit herausgefunden',
     "herausgefunden"),
    (6634, "example_de", 'Ich hab mir ein rosa Kleid gekauft',
     'Ich habe mir ein rosa Kleid gekauft',
     "rosa"),
    (6882, "example_de", 'Ich hab noch etwas Zeit dazwischen',
     'Ich habe noch etwas Zeit dazwischen',
     "dazwischen"),
    (7166, "example_de", 'Ich hab das Projekt total vermasselt, und mein Chef ist sauer',
     'Ich habe das Projekt total vermasselt, und mein Chef ist sauer',
     "vermasseln"),
    (7242, "example_de", 'Ich denk mir einen Plan aus',
     'Ich denke mir einen Plan aus',
     "ausdenken"),
    (7493, "example_de", 'Ich hab die Nachricht nur flüchtig gelesen',
     'Ich habe die Nachricht nur flüchtig gelesen',
     "flüchtig"),
    (8041, "example_de", 'Ich hab die Präsentation total vergeigt',
     'Ich habe die Präsentation total vergeigt',
     "vergeigen"),
    (8053, "example_de", 'Ich mach schnell die Teller weg',
     'Ich mache schnell die Teller weg',
     "wegmachen"),
    (8775, "example_de", 'Ich brauch eine Leiter',
     'Ich brauche eine Leiter',
     "Leiter"),
    (10062, "example_de", 'Ich glaub, das stimmt',
     'Ich glaube, das stimmt',
     "glaub"),
    (10129, "example_de", 'Ich hab kein Interesse',
     'Ich habe kein Interesse',
     "Interesse"),
    (10242, "example_de", 'Ich hab Mitleid mit ihm',
     'Ich habe Mitleid mit ihm',
     "Mitleid"),
    (10296, "example_de", 'Ich hab den Willen, das zu schaffen',
     'Ich habe den Willen, das zu schaffen',
     "Wille"),
    (10298, "example_de", 'Ich hab ne klare Vision für mein Leben',
     'Ich habe eine klare Vision für mein Leben',
     "Vision"),
    (11310, "example_de", 'Ich glaub, er hat Hintergedanken bei diesem Vorschlag',
     'Ich glaube, er hat Hintergedanken bei diesem Vorschlag',
     "Hintergedanken"),
    (11499, "example_de", 'Ich hab keine Vorbehalte gegen diesen Plan',
     'Ich habe keine Vorbehalte gegen diesen Plan',
     "Vorbehalt"),
    (11834, "example_de", 'Ich hab mir gestern einen Schokoriegel gekauft und er schmeckt mir sehr',
     'Ich habe mir gestern einen Schokoriegel gekauft und er schmeckt mir sehr',
     "Schokoriegel"),
    (11843, "example_de", 'Ich trink mein Wasser durch einen Strohhalm',
     'Ich trinke mein Wasser durch einen Strohhalm',
     "Strohhalm"),
    (11884, "example_de", 'Ich hab mir gestern ne Dose Sardinen gekauft',
     'Ich habe mir gestern eine Dose Sardinen gekauft',
     "Sardine"),
    (11891, "example_de", 'Nach der Arbeit brauch ich ne Erfrischung',
     'Nach der Arbeit brauche ich eine Erfrischung',
     "Erfrischung"),
    (12109, "example_de", 'Ich geh gern schwimmen',
     'Ich gehe gern schwimmen',
     "schwimmen"),
    (12412, "example_de", 'Ich mach zweimal die Woche Pilates',
     'Ich mache zweimal die Woche Pilates',
     "Pilates"),
    (12545, "example_de", 'Ich brauch eine medizinische Untersuchung',
     'Ich brauche eine medizinische Untersuchung',
     "medizinisch"),
    (13043, "example_de", 'Ich hab seit Tagen Rückenschmerzen und kann kaum schlafen',
     'Ich habe seit Tagen Rückenschmerzen und kann kaum schlafen',
     "Rückenschmerzen"),
    (13306, "example_de", 'Ich hab keinen Hunger mehr',
     'Ich habe keinen Hunger mehr',
     "keinen"),
    (13315, "example_de", 'Ich hab Pizza gekauft und davon schon die Hälfte gegessen',
     'Ich habe Pizza gekauft und davon schon die Hälfte gegessen',
     "davon"),
    (13369, "example_de", 'Ich brauch irgendwas zum Essen',
     'Ich brauche irgendwas zum Essen',
     "irgendwas"),
    (13422, "example_de", 'Ich hab Angst davor',
     'Ich habe Angst davor',
     "davor"),
    (13490, "example_de", 'Ich hab denselben Fehler nochmal gemacht',
     'Ich habe denselben Fehler nochmal gemacht',
     "denselben"),
    (13499, "example_de", 'Ich hab sämtliche Unterlagen mitgebracht',
     'Ich habe sämtliche Unterlagen mitgebracht',
     "sämtlich"),
    (13548, "example_de", 'Ich hab dir das tausendmal schon gesagt',
     'Ich habe dir das tausendmal schon gesagt',
     "tausendmal"),
    (13560, "example_de", 'Ich hab dir das schon zehnmal gesagt',
     'Ich habe dir das schon zehnmal gesagt',
     "zehnmal"),
    (13572, "example_de", 'Ich geh heute nicht ins Fitnessstudio, zumal es regnet',
     'Ich gehe heute nicht ins Fitnessstudio, zumal es regnet',
     "zumal"),
    (13639, "example_de", 'Ich trag eine Maske im Bus',
     'Ich trage eine Maske im Bus',
     "Maske"),
    (13729, "example_de", 'Ich mach mir samstags immer ne Maniküre im Salon',
     'Ich mache mir samstags immer eine Maniküre im Salon',
     "Maniküre"),
    (13749, "example_de", 'Ich hab mir gerade den roten Nagellack gekauft',
     'Ich habe mir gerade den roten Nagellack gekauft',
     "Nagellack"),
    (13886, "example_de", 'Ich lern Englisch in der Schule',
     'Ich lerne Englisch in der Schule',
     "englisch"),
    (14241, "example_de", 'Ich muss noch ne Briefmarke auf den Brief kleben, bevor ich ihn abschicke',
     'Ich muss noch eine Briefmarke auf den Brief kleben, bevor ich ihn abschicke',
     "Briefmarke"),
    (14247, "example_de", 'Das ist wirklich ne Untertreibung – der Film war einfach fantastisch',
     'Das ist wirklich eine Untertreibung – der Film war einfach fantastisch',
     "Untertreibung"),
    (14610, "example_de", 'Ich spiel ganz gerne Cello',
     'Ich spiele ganz gerne Cello',
     "Cello"),
    (15753, "example_de", 'Die Eidechse sonnt sich auf nem Stein',
     'Die Eidechse sonnt sich auf einem Stein',
     "Eidechse"),
    (15996, "example_de", 'Ich hab den Verdacht, dass er lügt',
     'Ich habe den Verdacht, dass er lügt',
     "Verdacht"),
    (16222, "example_de", 'Ich hab einen Strafzettel für falsches Parken bekommen',
     'Ich habe einen Strafzettel für falsches Parken bekommen',
     "Strafzettel"),
    (16899, "example_de", "Der Ladendiebstahl ist 'ne Straftat mit ernsthaften Konsequenzen",
     'Der Ladendiebstahl ist eine Straftat mit ernsthaften Konsequenzen',
     "Ladendiebstahl"),
    (17176, "example_de", 'Ich hab meinen Autoschlüssel verloren',
     'Ich habe meinen Autoschlüssel verloren',
     "Autoschlüssel"),
    (18459, "example_de", 'Ich hol den Mopp und wisch schnell den Boden',
     'Ich hole den Mopp und wisch schnell den Boden',
     "Mopp"),
    (18652, "example_de", 'Ich hab momentan keine Zeit',
     'Ich habe momentan keine Zeit',
     "momentan"),
    (18735, "example_de", 'Die Mittagspause dauert ne Stunde',
     'Die Mittagspause dauert eine Stunde',
     "Mittagspause"),
    (18792, "example_de", 'Ich hab ne dringende Frage',
     'Ich habe eine dringende Frage',
     "dringend"),
    (18900, "example_de", 'Ich sag dir schon vorab, dass das nicht billig wird',
     'Ich sage dir schon vorab, dass das nicht billig wird',
     "vorab"),
    (18918, "example_de", 'Ich hab mir die Haare gebürstet, bevor ich rausgegangen bin',
     'Ich habe mir die Haare gebürstet, bevor ich rausgegangen bin',
     "bürsten"),]


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
