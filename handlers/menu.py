from telegram import Update
from telegram.ext import ContextTypes
import aiosqlite

# 📨 Кнопка "Розсилка"
async def handle_broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    context.user_data["awaiting_broadcast"] = True
    await update.message.reply_text("✍️ Введи текст розсилки:")

# Принятие текста и отправка
async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_broadcast") is not True:
        return

    message_text = update.message.text
    context.user_data["awaiting_broadcast"] = False
    sent = 0
    failed = 0

    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT id FROM users") as cursor:
            async for row in cursor:
                try:
                    await context.bot.send_message(chat_id=row[0], text=message_text)
                    sent += 1
                except Exception as e:
                    failed += 1

    await update.message.reply_text(f"✅ Розсилку завершено!\n📬 Надіслано: {sent}\n❌ Помилок: {failed}")
