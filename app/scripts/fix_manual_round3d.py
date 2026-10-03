"""
Третий круг вычитки, ряды 205–300 (зерно 31337). Круг дочитан до конца.

Правки руками, без API. Критерии — в REVIEW_CRITERIA.md.

Самое заметное:

* `Anhieb` — противоположный смысл сразу в двух языках. В немецком «Auf
  Anhieb konnte er die Aufgabe nicht lösen» — не смог с первой попытки; в
  английском «He passed the test at first attempt» и в польском «Udało mu
  się za pierwszym razem» — смог. Человек выучит обратное.
* `brennen` — в русском списке значений «горсть». Это существительное
  «пригоршня», затесавшееся между глаголами.
* `hiernach` — пример обрублен до двух слов в трёх языках сразу: «После
  этого лучше», «Після цього краще», «Bundan sonra daha iyi». Подлежащее
  потеряно, фраза ничему не учит.
* `Handgranate` — турецкого «el granatı» не существует (el bombası), а в
  примере ещё и «granasını» с потерянной буквой.
* `Glut` — турецкий пример про вечернюю зарю в небе, немецкий про жар огня.
* `Patron` — в украинском примере «Керівник», которого нет даже в списке
  значений, и «підвищення» вместо прибавки: повышение в должности — другое.
* `Gatte` — в украинском «подружжя чоловічої статі»: это не слово, а
  попытка описать его.

    python -m app.scripts.fix_manual_round3d            # показать
    python -m app.scripts.fix_manual_round3d --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- противоположный смысл: худший класс ---------------------------------
    (8384, "example_en",
     "He passed the test at first attempt",
     "He couldn't solve the task straight away",
     "в немецком НЕ смог с первой попытки — здесь обратное"),
    (8384, "example_pl",
     "Udało mu się za pierwszym razem",
     "Za pierwszym razem nie udało mu się rozwiązać zadania",
     "в немецком НЕ смог с первой попытки — здесь обратное"),
    (8384, "example_uk",
     "Одразу він не міг розв'язати завдання",
     "Одразу він не зміг розв'язати завдання",
     "незавершённый вид: «не міг» вместо «не зміг»"),

    # --- слово не из того ряда -----------------------------------------------
    (1293, "translation_ru",
     "горсть, гореть, жечь, печь, быть включённым",
     "гореть, жечь, печь, быть включённым",
     "«горсть» — существительное среди глаголов"),
    (15124, "translation_uk",
     "чоловік, подружжя чоловічої статі, супутник життя",
     "чоловік, супутник життя",
     "«подружжя чоловічої статі» — описание, а не слово"),
    (11117, "translation_uk",
     "чарівний, чудовий, звабливий",
     "чарівний, чудовий, милий",
     "«звабливий» — соблазнительный, а entzückend — очаровательный"),
    (11899, "translation_tr",
     "çırpılmış yumurta, menemensiz sahanda karışık yumurta",
     "çırpılmış yumurta, sahanda karışık yumurta",
     "«menemensiz» — бессмыслица: «без менемена»"),
    (16730, "translation_tr",
     "el bombası, el granatı",
     "el bombası",
     "«el granatı» в турецком не существует"),

    # --- обрубленный пример: подлежащее потеряно -----------------------------
    (18939, "example_ru",
     "После этого лучше",
     "После этого положение улучшилось",
     "обрублено до двух слов, потеряно подлежащее"),
    (18939, "example_uk",
     "Після цього краще",
     "Після цього становище покращилося",
     "обрублено до двух слов, потеряно подлежащее"),
    (18939, "example_tr",
     "Bundan sonra daha iyi",
     "Bundan sonra durum düzeldi",
     "обрублено до трёх слов, потеряно подлежащее"),
    (2565, "example_en",
     "There is flooding",
     "The flood has flooded the city",
     "в немецком наводнение затопило город"),
    (2565, "example_tr",
     "Sel var",
     "Sel şehri bastı",
     "в немецком наводнение затопило город"),

    # --- пример про другое ----------------------------------------------------
    (14789, "example_pl",
     "Dziadek obdarował wnuki prezentami",
     "Prezent świąteczny sprawia dzieciom wielką radość",
     "в немецком рождественский подарок радует детей"),
    (14794, "example_uk",
     "Вона поводиться, як справжня дива",
     "У короля багато років була коханка",
     "пример про другое"),
    (14328, "example_tr",
     "Maçı ünlü bir yorumcu anlattı",
     "Yorumcu maçı çok iyi anlatıyor",
     "в немецком комментатор объясняет хорошо, а не «известный»"),
    (16169, "example_tr",
     "Binanın sakinleri çok sessiz",
     "Bu şehrin yaklaşık 50000 sakini var",
     "пример про тихих жильцов, а немецкий про число жителей"),
    (13703, "example_pl",
     "Dzieci przebierają się za duchy",
     "Dzieci przebierają się na Halloween",
     "в немецком на Хэллоуин, а не в привидений"),
    (8581, "example_en",
     "The guys are just standing around doing nothing",
     "Why do you have to stand around here doing nothing?",
     "в немецком вопрос «ты», а не рассказ про парней"),
    (8581, "example_uk",
     "Хлопці просто стоять і нічого не роблять",
     "Чому ти мусиш тут стовбичити без діла?",
     "в немецком вопрос «ты», а не рассказ про парней"),
    (8581, "example_tr",
     "Oğlanlar hiçbir şey yapmadan durup duruyorlar",
     "Neden burada boş boş dikilmek zorundasın?",
     "в немецком вопрос «ты», а не рассказ про парней"),
    (17215, "example_uk",
     "Ми пропустили з'їзд із шосе",
     "Ми з'їжджаємо на наступному з'їзді з автостради",
     "в немецком съезжают на следующем, а не пропустили"),
    (16146, "example_uk",
     "Зломщик заліз у квартиру через вікно",
     "Поліція зловила зломщика",
     "в немецком полиция поймала взломщика"),
    (14804, "example_pl",
     "Dziadek rzeźbi w drewnie małe figurki",
     "Lubię rzeźbić w drewnie w wolnym czasie",
     "в немецком «я люблю», а не про деда"),
    (13145, "example_pl",
     "Chodzi na grupę wsparcia w każdy wtorek",
     "Grupa wsparcia spotykała się w każdy wtorek, by rozmawiać o problemach",
     "в немецком собиралась сама группа, и сказано зачем"),
    (1047, "example_uk",
     "Де ти купив цю куртку?",
     "Де ти?",
     "пример про другое"),
    (15574, "example_uk",
     "Корови пасуться на лузі",
     "Ми граємо на лузі",
     "в немецком играют, а не пасутся коровы"),
    (15752, "example_tr",
     "Gökyüzündeki akşam kızıllığına bak",
     "Ateşin koru geceyi aydınlattı",
     "пример про вечернюю зарю, а немецкий про жар огня"),
    (15752, "example_pl",
     "W kominku został jeszcze żar",
     "Żar ognia rozświetlał noc",
     "в немецком жар освещал ночь"),
    (7708, "example_pl",
     "Nie szczyp mnie w rękę",
     "Szczypie się, żeby sprawdzić, czy to nie sen",
     "в немецком щиплет себя сам"),
    (16910, "example_tr",
     "Düşman birden yaylım ateşi açtı",
     "Topun yaylım ateşi savaş alanında yankılandı",
     "в немецком залп разнёсся по полю боя"),
    (12656, "example_en",
     "The surgical procedure lasted two hours",
     "The surgical procedure was successful",
     "в немецком операция прошла успешно, часов там нет"),
    (12656, "example_pl",
     "To był drobny zabieg pod narkozą",
     "Zabieg był udany",
     "в немецком операция прошла успешно"),
    (328, "example_uk",
     "Ти прийшов якраз вчасно",
     "Я саме тут",
     "пример про другое"),
    (17061, "example_pl",
     "Jazda pociągiem była przyjemna",
     "Jazda była przyjemna",
     "поезда в немецком примере нет"),
    (16382, "example_uk",
     "Відступ був запланований на сім ранку",
     "Вирушання було заплановане на сім ранку",
     "«відступ» — отступление, а Abmarsch — выход в поход"),
    (11566, "example_pl",
     "Zgodził się niechętnie i nic nie powiedział",
     "Zgodził się niechętnie i nie wyglądał na zadowolonego",
     "в немецком выглядел недовольным, а не молчал"),
    (13158, "example_pl",
     "Dziadek charczy w nocy przez sen",
     "Stary mężczyzna ciężko rzęzi nocą",
     "в немецком старик, а не собственный дед"),
    (2632, "example_uk",
     "Я дивлюся кримінальний серіал",
     "Я дивлюся детектив",
     "в немецком фильм, а не сериал"),
    (2632, "example_tr",
     "Bir polisiye dizi izliyorum",
     "Bir polisiye film izliyorum",
     "в немецком фильм, а не сериал"),

    # --- время и вид глагола --------------------------------------------------
    (11927, "example_tr",
     "Anneanemin hep lezzetli bir peynir keki vardı",
     "Anneannem her zaman lezzetli peynirli kek yapar",
     "в немецком бабушка печёт, а здесь «у бабушки был»; плюс опечатка"),
    (16146, "example_ru",
     "Полиция ловит взломщика",
     "Полиция поймала взломщика",
     "в немецком действие завершено"),
    (7159, "example_uk",
     "Що вказує на те, що він брехав?",
     "Що ж вказує на те, що він бреше?",
     "в немецком настоящее время"),

    # --- неверное слово при верном смысле ------------------------------------
    (10274, "example_uk",
     "Дощ зруйнує наш пікнік",
     "Дощ зіпсує наш пікнік",
     "пикник портят, а не разрушают"),
    (14804, "example_uk",
     "Я люблю вирізати дерево у вільний час",
     "Я люблю різьбити по дереву у вільний час",
     "«вирізати дерево» значит спилить его"),
    (9120, "example_uk",
     "Керівник дав підвищення всім робітникам",
     "Хазяїн дав надбавку всім робітникам",
     "«підвищення» — повышение в должности; и «керівника» нет в значениях"),
    (7708, "example_tr",
     "Rüya görüp görmediğini görmek için kendini sıkıyor",
     "Rüya görüp görmediğini anlamak için kendini çimdikliyor",
     "kneifen — çimdiklemek, а не sıkmak; и «görüp görmediğini görmek» повтор"),
    (16730, "example_tr",
     "Asker el granasını sipere attı",
     "Asker sığınağa bir el bombası attı",
     "«granasını» — нет такого слова; и Bunker это sığınak"),
    (17061, "example_ru",
     "Поездка была красивая",
     "Поездка была приятная",
     "«красивая поездка» по-русски не говорят"),

    # --- грамматика -----------------------------------------------------------
    (7258, "example_uk",
     "Ти можеш винести мішки з сміттям",
     "Ти можеш винести мішки зі сміттям",
     "перед «см» нужен прийменник «зі»"),
    (8887, "example_uk",
     "Профспілка вимагає кращу зарплату для робітників",
     "Профспілка вимагає кращої зарплати для робітників",
     "«вимагати» требует родительного падежа"),
    (8440, "example_uk",
     "Мій ключ мені загубився",
     "Мій ключ десь загубився",
     "«мені загубився» — калька с немецкого"),
    (11899, "example_uk",
     "Люблю яйчицю на снідання",
     "Люблю яєчню-бовтанку на сніданок",
     "«яйчицю» и «на снідання» — обе формы неверны"),
    (9022, "example_tr",
     "Avcı tüfeğini ormanına götürüyor",
     "Avcı av tüfeğini ormana götürüyor",
     "«ormanına» — чужой притяжательный аффикс"),
    (2574, "example_tr",
     "Her kişi bireysel",
     "Her insan bireyseldir",
     "пропущена связка, и «kişi» вместо «insan»"),
    (6694, "example_tr",
     "Şömineye ait kül dışarı çıkarılmalı",
     "Şöminedeki külün dışarı çıkarılması gerek",
     "«ait» здесь не к месту"),
    (10638, "example_tr",
     "Zaferi aldıktan sonra zafer sevinci anlatılmazdı",
     "Zaferden sonraki zafer sevinci tarif edilemezdi",
     "«zafer» дважды и неверная форма сказуемого"),
    (7159, "example_tr",
     "Ne, onun yalan söylediğini ima ediyor",
     "Onun yalan söylediğini ne ima ediyor?",
     "запятая разрывает фразу, и потерян вопросительный знак"),
    (1047, "example_tr",
     "Neredesiniz",
     "Neredesin?",
     "в немецком «ты», и потерян вопросительный знак"),
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
