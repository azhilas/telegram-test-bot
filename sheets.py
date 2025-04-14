import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def connect_sheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(
        "google-creds.json",
        scopes=scopes
    )
    return gspread.authorize(creds)

def get_broadcasts():
    client = connect_sheets()
    sheet = client.open("TelegramBotPanel").worksheet("Broadcasts")
    return sheet.get_all_records()

def add_user_to_sheet(user_id, username, first_name, category="default"):
    client = connect_sheets()
    sheet = client.open("TelegramBotPanel").worksheet("Users")
    users = sheet.get_all_records()

    user_ids = [str(row["user_id"]) for row in users]
    if str(user_id) not in user_ids:
        sheet.append_row([
            user_id,
            username or "",
            first_name or "",
            category,
            "yes",
            datetime.now().strftime("%Y-%m-%d")
        ])
def update_last_active(user_id):
    client = connect_sheets()
    sheet = client.open("TelegramBotPanel").worksheet("Users")
    users = sheet.get_all_records()

    for i, row in enumerate(users):
        if str(row["user_id"]) == str(user_id):
            sheet.update_cell(i + 2, 7, datetime.now().strftime("%Y-%m-%d %H:%M"))
            break
