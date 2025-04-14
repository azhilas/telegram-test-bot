from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from db import init_db
from handlers.start import start
from handlers.menu import handle_broadcast_start, handle_broadcast_message
from sheets import update_last_active

async def on_startup(app):
    await init_db()

app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^📨 Розсилка$"), handle_broadcast_start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_broadcast_message))

print("🤖 Бот запущен и готов к работе!")

async def update_user_activity(update, context):
    user = update.effective_user
    update_last_active(user.id)

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), update_user_activity))

app.run_polling()
