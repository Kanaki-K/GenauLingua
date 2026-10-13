"""
Сплошная вычитка, блоки 14 и 15: ряды 1301–1500 по рангу частотности.

Находки:

* `probieren` — в английском «To try – Would you like to try it?»: слово
  приклеено к фразе через тире. Это уже третий такой след в базе, и все
  три в английской колонке.
* `Gift`, `Hemd`, `Lügner`, `beinahe` — русизмы в украинских значениях:
  «яд», «рубашка», «обманщик», «чуть не».
* `Krebs` — в русском и украинском значении «Рак» с большой буквы, как
  созвездие, хотя ряд про болезнь.
* `wehtun`, `zuhören`, `Verräter`, `Chaos` — примеры про другое, причём
  обычно в трёх языках сразу.
* `Jacke`, `Hut` — в немецких примерах разговорные «'ne» и «'nen».
* `Sonntag`, `anziehen` — немецкий говорит «я», переводы «мы» или «она».
* `Baby` — украинское «у коляски» вместо «у колясці».

    python -m app.scripts.fix_block_0014            # показать
    python -m app.scripts.fix_block_0014 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- след правки: слово приклеено через тире -------------------------------
    (731, "example_en", "To try – Would you like to try it?",
     "Would you like to try it?",
     "слово приклеено к фразе через тире — след прежней правки"),

    # --- русизмы и неверные значения ------------------------------------------
    (12496, "translation_uk", "отрута, яд", "отрута",
     "«яд» — русизм"),
    (397, "translation_uk", "сорочка, рубашка", "сорочка",
     "«рубашка» — русизм"),
    (10178, "translation_uk", "брехун, обманщик", "брехун",
     "«обманщик» — русизм"),
    (6536, "translation_uk", "майже, ледве не, чуть не",
     "майже, ледве не", "«чуть не» — русизм"),
    (12498, "translation_ru", "Рак", "рак",
     "с большой буквы это созвездие, а ряд про болезнь"),
    (12498, "translation_uk", "Рак", "рак",
     "с большой буквы это созвездие, а ряд про болезнь"),
    (9444, "translation_pl", "uczeń, szkolniak", "uczeń",
     "«szkolniak» — просторечие"),

    # --- разговорная форма в немецком эталоне ---------------------------------
    (443, "example_de", "Sie trägt 'ne warme Jacke",
     "Sie trägt eine warme Jacke", "«'ne» — разговорное стяжение"),

    # --- опечатки и грамматика -------------------------------------------------
    (13457, "example_uk", "Зараз дванадцять годин дня",
     "Зараз дванадцята година дня", "«дванадцять годин» — не о времени"),
    (905, "example_uk", "Південь теплішій за північ",
     "Південь тепліший за північ", "«теплішій» — опечатка"),
    (6560, "example_tr", "Telefonum WiFiye bağlı", "Telefonum WiFi'ye bağlı",
     "пропущен апостроф в имени собственном"),
    (14957, "example_uk", "Немовлята сплять у коляски",
     "Немовлята сплять у колясці", "неверный падеж"),
    (6542, "example_uk", "Він можливо запізниться",
     "Він, можливо, запізниться", "вводное слово выделяется запятыми"),
    (6541, "example_en", "Lets get out of here quickly",
     "Let's get out of here quickly", "«Lets» без апострофа"),

    # --- пример переводит другую фразу ----------------------------------------
    (1416, "example_tr", "Bana hâlâ bir belge eksik",
     "Bir belgem daha eksik", "по-турецки так не говорят"),
    (359, "example_en", "What is your size?",
     "What size do you need?", "в немецком «какой размер тебе нужен»"),
    (359, "example_tr", "Bedeniniz kaç?",
     "Hangi bedene ihtiyacın var?", "в немецком «du» и «нужен»"),
    (2432, "example_tr", "Patrondan bir gün izin aldım",
     "Bir izne ihtiyacım var", "в немецком «мне нужно разрешение»"),
    (2216, "example_en", "Please open the door", "Open the door!",
     "в немецком повеление с восклицательным знаком"),
    (2216, "example_tr", "Lütfen kapıyı aç", "Kapıyı aç!",
     "в немецком повеление с восклицательным знаком"),
    (17069, "example_pl", "Możesz się tu zatrzymać na chwilę",
     "Autobus zatrzymuje się przy kościele",
     "в немецком автобус останавливается у церкви"),
    (10179, "example_tr", "Erkek arkadaşım çok kıskanç",
     "Kız kardeşini kıskanıyor",
     "в немецком она ревнует к сестре, а не про парня"),
    (15404, "example_uk", "Ми йдемо в похід в гори",
     "Ми йдемо в похід на гору", "в немецком одна гора"),
    (14947, "example_en", "Dogs love to bury bones",
     "The dog is buried in the garden",
     "в немецком собака похоронена, а не копает"),
    (1613, "example_uk", "Мені важко зосереджуватися на уроці",
     "Я не можу зосередитися", "в немецком «я не могу сосредоточиться»"),
    (12492, "example_tr", "Arı sokması kolumu şişirdi",
     "Sivrisinek sokması çok kaşınıyor",
     "в немецком комар, а не пчела"),
    (853, "example_en", "On Sunday we rest", "On Sunday I rest",
     "в немецком «я», а не «мы»"),
    (853, "example_uk", "У неділю ми відпочиваємо",
     "У неділю я відпочиваю", "в немецком «я», а не «мы»"),
    (853, "example_tr", "Pazar günü dinleniyoruz",
     "Pazar günü dinleniyorum", "в немецком «я», а не «мы»"),
    (3, "example_uk", "Увечері ми гуляємо в парку",
     "Увечері я вчу німецьку", "в немецком «вечерами я учу немецкий»"),
    (10184, "example_uk", "Я можу відчувати вітер", "Я відчуваю вітер",
     "«можу відчувати» — калька"),
    (1568, "example_uk", "Ти можеш мені дзвонити в будь-який час",
     "Ви можете дзвонити в будь-який час",
     "в немецком «Sie» — на «Вы»"),
    (2946, "example_uk", "Поліція почала арештовувати демонстрантів",
     "Поліція його арештовує", "в немецком «полиция его арестовывает»"),
    (6536, "example_uk", "Я майже б запізнився", "Я ледве не запізнився",
     "«майже б запізнився» по-украински не говорят"),
    (6537, "example_en", "I'd also like some coffee, please",
     "I'm also coming to the party", "в немецком про вечеринку"),
    (6537, "example_tr", "O aynı zamanda çok iyi bir aşçı",
     "Ben de partiye geliyorum", "в немецком про вечеринку"),
    (17488, "example_en", "Turn off the engine, please",
     "My car's engine is broken", "в немецком мотор сломан"),
    (10188, "example_en", "He was a traitor", "The traitor was arrested",
     "в немецком предателя арестовали"),
    (10188, "example_tr", "Sen hainsin, bana yalan söyledin",
     "Hain tutuklandı", "в немецком предателя арестовали"),
    (1305, "example_en", "There was total chaos at the airport",
     "My room is a mess", "в немецком про комнату, а не про аэропорт"),
    (2012, "example_uk", "Не підписуй договір без юриста",
     "Підпиши тут, будь ласка", "в немецком «подпиши здесь»"),
    (2012, "example_tr", "Lütfen burayı imzalayın",
     "Lütfen burayı imzala", "в немецком «Unterschreib» — ты"),
    (6542, "example_en", "Maybe we should call her first",
     "He may be late", "в немецком «он, возможно, опоздает»"),
    (831, "example_tr", "Buraya nadiren gidiyorum",
     "Buraya nadiren geliyorum", "в немецком «прихожу», а не «хожу»"),
    (14948, "example_tr", "Burnum tıkalı, nefes alamıyorum",
     "Köpeğin siyah bir burnu var", "в немецком про собачью морду"),
    (13896, "example_uk", "Напиши мені, коли доїдеш додому",
     "Я саме пишу листа своїй бабусі",
     "в немецком «я как раз пишу письмо бабушке»"),
    (2583, "example_uk", "Тим часом вона вже пішла",
     "Тим часом багато чого сталося", "в немецком «многое произошло»"),
    (905, "example_tr", "Balkonumuz güneye bakıyor",
     "Güney kuzeyden daha sıcak", "в немецком «юг теплее севера»"),
    (35, "example_en", "She gets dressed quickly", "I get dressed quickly",
     "в немецком «я», а не «она»"),
    (35, "example_uk", "Вона швидко одягається", "Я швидко одягаюся",
     "в немецком «я», а не «она»"),
    (35, "example_tr", "Hızlı giyinir", "Hızlıca giyiniyorum",
     "в немецком «я», а не «он»"),
    (15407, "example_tr", "Dikkat et, bu köpek çok vahşi",
     "Çocuklar bugün çok haşarı", "в немецком про детей, а не про собаку"),
    (1016, "example_en", "My head hurts", "Careful, this might hurt",
     "в немецком предупреждение, а не жалоба"),
    (1016, "example_uk", "У мене болить голова",
     "Обережно, зараз може бути боляче",
     "в немецком предупреждение, а не жалоба"),
    (1016, "example_tr", "Başım ağrıyor",
     "Dikkat et, bu birazdan acıyabilir",
     "в немецком предупреждение, а не жалоба"),
    (2271, "example_en", "I observe the birds",
     "I observe the birds in the park", "потеряно «в парке»"),
    (2271, "example_uk", "Я спостерігаю за птахами",
     "Я спостерігаю за птахами в парку", "потеряно «в парке»"),
    (2271, "example_tr", "Kuşları gözlemliyorum",
     "Parktaki kuşları gözlemliyorum", "потеряно «в парке»"),
    (2911, "example_uk", "Я з цим поводжуся", "Я з цим даю раду",
     "«з цим поводжуся» по-украински не говорят"),
    (13631, "example_tr", "Bebek çıplak",
     "Bebek çıplak ve kıyafete ihtiyacı var",
     "потеряна вторая половина фразы"),
    (1545, "example_uk", "Наш двір дуже затишний і зелений",
     "Діти граються у дворі", "в немецком дети играют во дворе"),
    (2760, "example_en", "I like to ride a horse",
     "I like to ride a horse in the park", "потеряно «в парке»"),
    (2760, "example_uk", "Я люблю їздити верхи",
     "Я люблю їздити верхи в парку", "потеряно «в парке»"),
    (2760, "example_tr", "At binmeyi severim",
     "Parkta ata binmeyi severim", "потеряно «в парке»; и нужен дательный"),
    (2128, "example_en", "Listen to me",
     "You have to listen to me carefully now",
     "в немецком «ты должен сейчас внимательно меня выслушать»"),
    (2128, "example_uk", "Послухай мене",
     "Ти мусиш зараз мене уважно слухати",
     "в немецком «ты должен сейчас внимательно меня выслушать»"),
    (2128, "example_tr", "Beni dinle",
     "Şimdi beni dikkatle dinlemelisin",
     "в немецком «ты должен сейчас внимательно меня выслушать»"),
    (1454, "example_uk", "Ми чекаємо народження першої дитини",
     "Пологи були складні", "в немецком «роды были сложные»"),
    (2860, "example_en", "The electricity went out last night",
     "The electricity is out", "«вчера ночью» в немецком нет"),
    (2860, "example_uk", "Електрика вимкнена", "Немає світла",
     "по-украински так и говорят, когда нет тока"),
    (6563, "example_en", "We must preserve the old town",
     "We must keep calm", "в немецком «мы должны сохранять спокойствие»"),
    (1065, "example_tr", "Sayı büyük",
     "42 sayısı benim en sevdiğim sayı", "в немецком про число 42"),
    (14957, "example_en", "The baby is sleeping right now",
     "The babies are sleeping in the pram",
     "в немецком младенцы во множественном и коляска"),
    (8770, "example_en", "The inspector is coming today for an inspection",
     "The inspector is coming for an inspection",
     "«сегодня» в немецком нет"),
    (8770, "example_tr", "Müfettiş bugün kontrole geliyor",
     "Müfettiş kontrole geliyor", "«сегодня» в немецком нет"),
    (2864, "example_uk", "Є буря", "Надворі буря",
     "«є буря» по-украински не говорят"),
    (18639, "example_en", "I'm running after you",
     "Come on, I'll run after you!", "потеряно «идём»"),
    (18639, "example_uk", "Собака біг слідом за нами",
     "Йди, я побіжу слідом за тобою!", "в немецком про говорящего"),
    (2192, "example_uk", "Замість навчання я граю",
     "Замість навчання я краще пограю у відеоігри",
     "потеряны видеоигры"),
    (12112, "example_uk", "Я хочу з тобою зробити ставку",
     "Я хочу з тобою закластися", "по-украински спорят «закластися»"),
    (361, "example_en", "Look", "Look how beautiful the sky is",
     "потеряна вторая половина фразы"),
    (361, "example_tr", "Baksana!", "Bak, gökyüzü ne kadar güzel",
     "потеряна вторая половина фразы"),
    (726, "example_uk", "Цей стілець дуже зручний",
     "Це практичне рішення проблеми",
     "в немецком про решение задачи, а не про стул"),
    (726, "example_tr", "Bu pratik bir çözüm",
     "Bu, sorun için pratik bir çözüm", "потеряна «задача»"),

    # --- неестественно и книжно -------------------------------------------------
    (6561, "example_pl", "To był twardy egzamin", "To był trudny egzamin",
     "«twardy egzamin» по-польски не говорят"),
    (18638, "example_pl", "Trochę pośpiechu! Autobus zaraz przyjedzie",
     "Pośpiesz się! Autobus zaraz przyjedzie",
     "«trochę pośpiechu» звучит книжно"),
    (6548, "example_tr", "Kutuyu taşımak çok ağır",
     "Bu kutu çok ağır, taşımak zor", "по-турецки так не говорят"),
    (10182, "example_ru", "Винт ещё свободный", "Винт ещё не затянут",
     "«свободный винт» по-русски не говорят"),
    (10182, "example_uk", "Гвинт ще вільний", "Гвинт ще не затягнутий",
     "«вільний гвинт» по-украински не говорят"),
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
