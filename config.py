from dotenv import load_dotenv
import os


load_dotenv('.env')
bot_token = os.environ.get("bot_token")
chat_id = int(os.environ.get("chat_id"))
admin_id = int(os.environ.get("admin_id"))


bot_username = ""  # Само обновится
