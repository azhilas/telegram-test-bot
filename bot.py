from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from db import init_db
from handlers.start import start

async def on_startup(app):
    await init_db()

app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()
app.add_handler(CommandHandler("start", start))

print("🤖 Бот запущен и готов к работе!")
app.run_polling()
