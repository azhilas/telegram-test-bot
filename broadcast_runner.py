from sheets import connect_sheets
from db import init_db
import asyncio
from telegram import Bot
from config import BOT_TOKEN

async def send_broadcasts():
    bot = Bot(token=BOT_TOKEN)
    client = connect_sheets()
    broadcast_sheet = client.open("TelegramBotPanel").worksheet("Broadcasts")
    user_sheet = client.open("TelegramBotPanel").worksheet("Users")

    broadcasts = broadcast_sheet.get_all_records()
    users = user_sheet.get_all_records()

    for i, row in enumerate(broadcasts):
        if row["status"] != "pending":
            continue

        category = row["filter_category"]
        message = row["message"]
        recipients = [u for u in users if u["category"] == category and u["active"] == "yes"]

        sent = 0
        for user in recipients:
            try:
                await bot.send_message(chat_id=user["user_id"], text=message)
                sent += 1
            except Exception as e:
                print(f"❌ Ошибка отправки {user['user_id']}: {e}")

        broadcast_sheet.update_cell(i + 2, 6, "yes")  # колонка "sent"
        broadcast_sheet.update_cell(i + 2, 4, "done")  # колонка "status"
        print(f"📬 Отправлено {sent} сообщений по категории {category}")

if __name__ == "__main__":
    asyncio.run(send_broadcasts())
