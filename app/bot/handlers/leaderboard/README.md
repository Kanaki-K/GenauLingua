# 🏆 Система месячного и lifetime рейтинга

Полная документация модуля рейтингов для GenauLingua бота.

---

## 📁 Структура файлов

```
app/bot/handlers/leaderboard/
├── __init__.py              # Регистрация роутеров
├── monthly.py               # Месячный рейтинг
├── alltime.py               # Lifetime рейтинг
├── leaderboard_table.py     # Таблица лидеров
└── utils.py                 # Утилиты и форматирование

app/services/
└── monthly_leaderboard_service.py  # Бизнес-логика и БД
```

---

## 💰 Формула начисления баллов

### Месячные баллы:

Формула живёт в `MonthlyStats.calculate_monthly_score`, и числа ниже —
константы оттуда же. **Править здесь нечего**: этот файл описывает, а
считает код.

```python
monthly_score = (
    # за каждый верный ответ — по цене игры, 1 : 1 : 2 : 3
      correct_text    * 1     # карточка: узнать написанное
    + correct_reverse * 1     # припоминание: вспомнить слово по значению
    + correct_audio   * 2     # на слух: формы нет, различать на звук
    + correct_speech  * 3     # вслух: не узнавание, а производство
    # за доведённое до конца
    + monthly_quizzes * 10    # круг пройден целиком
    + monthly_words   * 3     # слово перешло в «выучено» В ЭТОМ МЕСЯЦЕ (learned_at)
    + streak_points(monthly_streak)   # серия растёт в цене, потолок 10/день
    + accuracy_points         # плавно от порога 60%, без обрыва на 90%
    + report_bonus            # подтверждённая жалоба → +15, одна оплата за слово, без потолка
)
```

**`monthly_words` считается по `user_words.learned_at`** — дате перехода в
«выучено» (`month_words`), на каждом занятии. Повторение уже выученного
слова в следующем месяце его не оплачивает снова.

**Кто стоит в рейтинге месяца** — одно правило `ranked_in_month()`:
хоть одно занятие и балл больше нуля. По нему считаются таблица, место и
«из N» в карточке и итоги при закрытии. Баллы за жалобы без занятия лежат
в ряду и идут в «за всё время», но места в месяце не дают, пока человек
не пройдёт занятие. Равные баллы — равное место и равная награда.

**`correct_text` своей колонки не имеет** — он выводится вычитанием:
`total_correct − audio − speech − reverse`. Отдельной колонкой его рано или
поздно обновили бы не вместе с остальными, и итог разошёлся бы с частями.

**`monthly_reverse` больше не платит** (`POINTS_PER_REVERSE = 0`). Колонка
платила 5 за круг, целиком сыгранный в обратную сторону, — а такого круга
не существует: обратная сторона стала **пятой игрой внутри круга** и платит
за ответ, как остальные. Ноль оставлен, а не удалён, чтобы закрытые сезоны
пересчитывались тем же кодом и давали те же числа.

### Lifetime баллы:
```python
# Считается из источника (get_user_lifetime_rank / get_lifetime_leaderboard),
# по изучаемому языку, текущий незакрытый месяц включительно:
lifetime = sum(monthly_stats.monthly_score) + sum(monthly_awards.lifetime_bonus)
# Колонка users.lifetime_score копит ТОЛЬКО бонусы и экранами не читается.
# 🥇 1 место → +100
# 🥈 2 место → +50
# 🥉 3 место → +25
# 4-10 место → +10
```

---

## 🗄️ Таблицы БД

| Таблица | Назначение |
|---------|-----------|
| `monthly_seasons` | Месячные сезоны соревнований |
| `monthly_stats` | Статистика пользователя за месяц |
| `monthly_quiz_events` | Идемпотентность (викторина учитывается 1 раз) |
| `monthly_awards` | Награды за места в топ-10 |
| `win_streaks` | Серии месячных побед |

---

## 🔄 Жизненный цикл сезона

1. **Начало месяца (1 число):** `create_new_season()` — новый сезон, предыдущий деактивируется
2. **В течение месяца:** после каждой викторины — `update_monthly_stats()` (инкрементально)
3. **Конец месяца:** `finalize_season()` — награды топ-10, обновление lifetime_score

---

## 🎨 Логика отображения

- **Топ-3:** только медали 🥇🥈🥉, без титулов
- **4-10 места:** номер + титул (win streak: 🔥, 👑, 💎 / по словам: 📚, 🎯, 🧠, 🌍)
- **Текущий пользователь:** жирный шрифт на любой позиции

---

## 🌍 Локализация

4 языка: RU, UK, EN, TR — названия месяцев, тексты кнопок, пояснения, формулы баллов.

---

## ⚙️ Критические моменты

1. **Порядок регистрации роутеров** — leaderboard ПЕРВЫМ в `main.py` (перехват `show_my_rating`)
2. **Идемпотентность** — через `UNIQUE(quiz_session_id)` в `monthly_quiz_events`
3. **`User.display_name`** — имя + фамилия, без @

---

## 📊 Использование

```python
# После завершения викторины:
from app.services.monthly_leaderboard_service import update_monthly_stats
await update_monthly_stats(user_id=user.id, session=session, quiz_session_id=session_id)

# Получить рейтинг:
from app.services.monthly_leaderboard_service import get_monthly_leaderboard
leaderboard = await get_monthly_leaderboard(session, season_id=season.id, limit=10)

# Подвести итоги:
from app.services.monthly_leaderboard_service import finalize_season
await finalize_season(season_id=season.id, session=session)
```