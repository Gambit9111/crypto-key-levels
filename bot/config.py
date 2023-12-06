import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")
POSTGRES_DB_URL = os.getenv("POSTGRES_DB_URL")

if not TELEGRAM_BOT_TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN is not set")
elif not TELEGRAM_ADMIN_ID:
    raise Exception("TELEGRAM_ADMIN_ID is not set")
elif not POSTGRES_DB_URL:
    raise Exception("POSTGRES_DB_URL is not set")
else:
    print("Config loaded successfully")