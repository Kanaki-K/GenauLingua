#!/usr/bin/env python3
"""
Рассылка обновления всем пользователям на их языке

Использование:
  python app/scripts/broadcast_april.py          — отправить всем
  python app/scripts/broadcast_april.py --dry-run — только показать кому отправит (без отправки)
  python app/scripts/broadcast_april.py --test 463491762 — отправить только одному юзеру (для теста)
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

MESSAGES = {
    "ru": """🚀 <b>GenauLingua — большое обновление!</b>

📚 База слов выросла в 4 раза — теперь <b>13 000 слов</b>, уровни A1–C2

🗂 <b>20 тематических категорий</b> — учи то, что нужно: еда, работа, путешествия, наука и другие

⚙️ <b>4 режима викторины</b> — по уровню, по категории, вся база или только сложные слова

📝 Нашёл ошибку в переводе? Сообщи прямо из викторины — за подтверждённый репорт <b>+1 балл</b> в рейтинг

Весь твой прогресс сохранён. Заходи и попробуй новые режимы!

💬 Подписывайся на наш чат — обновления, баги, идеи:
👉 t.me/genaulingua_chat""",

    "uk": """🚀 <b>GenauLingua — велике оновлення!</b>

📚 База слів зросла в 4 рази — тепер <b>13 000 слів</b>, рівні A1–C2

🗂 <b>20 тематичних категорій</b> — вчи те, що потрібно: їжа, робота, подорожі, наука та інші

⚙️ <b>4 режими вікторини</b> — за рівнем, за категорією, вся база або тільки складні слова

📝 Знайшов помилку в перекладі? Повідом прямо з вікторини — за підтверджений репорт <b>+1 бал</b> у рейтинг

Весь твій прогрес збережено. Заходь та спробуй нові режими!

💬 Приєднуйся до нашого чату — оновлення, баги, ідеї:
👉 t.me/genaulingua_chat""",

    "en": """🚀 <b>GenauLingua — major update!</b>

📚 Word base grew 4x — now <b>13,000 words</b>, levels A1–C2

🗂 <b>20 topic categories</b> — learn what you need: food, work, travel, science and more

⚙️ <b>4 quiz modes</b> — by level, by category, full database or difficult words only

📝 Found a translation error? Report it right from the quiz — get <b>+1 rating point</b> for confirmed reports

All your progress is saved. Come try the new modes!

💬 Join our community — updates, bugs, ideas:
👉 t.me/genaulingua_chat""",

    "tr": """🚀 <b>GenauLingua — büyük güncelleme!</b>

📚 Kelime tabanı 4 kat büyüdü — artık <b>13.000 kelime</b>, A1–C2 seviyeler

🗂 <b>20 konu kategorisi</b> — ihtiyacın olanı öğren: yemek, iş, seyahat, bilim ve daha fazlası

⚙️ <b>4 test modu</b> — seviyeye göre, kategoriye göre, tüm taban veya sadece zor kelimeler

📝 Çeviri hatası buldun? Testten bildir — onaylanan rapor için <b>+1 sıralama puanı</b>

Tüm ilerlemen kaydedildi. Gel ve yeni modları dene!

💬 Topluluğumuza katıl — güncellemeler, hatalar, fikirler:
👉 t.me/genaulingua_chat""",
}

DEFAULT_LANG = "ru"

async def run_broadcast(dry_run: bool = False, test_user_id: int = None):
    db_url = os.getenv("DATABASE_URL")
    bot_token = os.getenv("BOT_TOKEN")
    if not db_url:
        print("❌ DATABASE_URL не задан!")
        return
    if not bot_token:
        print("❌ BOT_TOKEN не задан!")
        return
    engine = create_async_engine(db_url, echo=False)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    async with Session() as session:
        from app.database.models import User
        if test_user_id:
            result = await session.execute(select(User).where(User.id == test_user_id))
            users = result.scalars().all()
            if not users:
                print(f"❌ Юзер {test_user_id} не найден!")
                return
        else:
            result = await session.execute(select(User))
            users = result.scalars().all()
        print(f"📨 Рассылка: {len(users)} пользователей")
        print(f"   Режим: {'DRY RUN (без отправки)' if dry_run else 'ОТПРАВКА'}")
        print()
        lang_stats = {}
        for user in users:
            lang = user.interface_language or DEFAULT_LANG
            lang_stats[lang] = lang_stats.get(lang, 0) + 1
        print("📊 По языкам:")
        for lang, count in sorted(lang_stats.items()):
            print(f"   {lang}: {count}")
        print()
        if dry_run:
            print("🔍 DRY RUN — показываю что будет отправлено:\n")
            for lang, text in MESSAGES.items():
                print(f"--- {lang.upper()} ---")
                preview = text.replace("<b>", "").replace("</b>", "")
                print(preview[:150] + "...")
                print()
            print("Для реальной отправки запусти без --dry-run")
            await bot.session.close()
            return
        success = 0
        failed = 0
        blocked = 0
        for i, user in enumerate(users, 1):
            lang = user.interface_language or DEFAULT_LANG
            text = MESSAGES.get(lang, MESSAGES[DEFAULT_LANG])
            try:
                await bot.send_message(chat_id=user.id, text=text)
                success += 1
                print(f"  ✅ [{i}/{len(users)}] {user.display_name} ({lang})")
            except Exception as e:
                error_str = str(e).lower()
                if "blocked" in error_str or "deactivated" in error_str:
                    blocked += 1
                    print(f"  🚫 [{i}/{len(users)}] {user.display_name} — заблокировал бота")
                else:
                    failed += 1
                    print(f"  ❌ [{i}/{len(users)}] {user.display_name} — {e}")
            if i % 25 == 0:
                await asyncio.sleep(1)
        print()
        print("=" * 40)
        print(f"📨 ИТОГО:")
        print(f"   ✅ Отправлено: {success}")
        print(f"   🚫 Заблокировали: {blocked}")
        print(f"   ❌ Ошибок: {failed}")
        print(f"   📊 Всего: {len(users)}")
    await bot.session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Рассылка обновления")
    parser.add_argument("--dry-run", action="store_true", help="Показать что отправит, без реальной отправки")
    parser.add_argument("--test", type=int, help="Отправить только одному юзеру (для теста)")
    args = parser.parse_args()
    asyncio.run(run_broadcast(dry_run=args.dry_run, test_user_id=args.test))