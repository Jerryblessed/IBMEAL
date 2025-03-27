import requests
import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "7512502677:AAEKKpOcMhQnFByRc09-d_YWHqcxbmchPGg"
REMOTE_DB_API = "https://ibtrosshuttle.pythonanywhere.com/register_user"
LOCAL_DB = "./database.sqlite"  # Change this to your actual local DB path

def get_local_users():
    """Reads users from the local SQLite database."""
    conn = sqlite3.connect(LOCAL_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, first_name, last_name, username FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return [{"user_id": u[0], "first_name": u[1], "last_name": u[2], "username": u[3] or ""} for u in users]

def sync_users(update: Update, context: CallbackContext):
    """Sends all local users to the cloud database."""
    users = get_local_users()
    if not users:
        update.message.reply_text("No users found in local database.")
        return
    
    success_count = 0
    for user in users:
        response = requests.post(REMOTE_DB_API, json=user)
        if response.status_code == 200:
            success_count += 1

    update.message.reply_text(f"Synced {success_count}/{len(users)} users to the cloud.")

def main():
    """Starts the bot."""
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("sync_users", sync_users))  # Command to manually sync users

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
