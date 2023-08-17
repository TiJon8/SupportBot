import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = str(os.getenv("TOKEN"))
SUPPORT_CHAT_ID = int(os.getenv("SUPPORT_CHAT_ID"))
BOT_ID = int(os.getenv("BOT_ID"))
ADMINS = os.getenv("ADMINS")