from telegram import Update
from telegram.ext import ContextTypes
from db import add_user
from keyboards.main_keyboard import get_main_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await add_user(user)
    await update.message.reply_text(
        f"👋 Привіт, {user.first_name}! Обери дію:",
        reply_markup=get_main_keyboard()
    )
