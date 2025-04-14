from telegram import ReplyKeyboardMarkup

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [["📨 Розсилка", "📊 Статистика"]],
        resize_keyboard=True
    )
