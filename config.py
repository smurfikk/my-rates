from dotenv import load_dotenv
import os

load_dotenv('.env')
bot_token = os.environ.get("bot_token")
chat_id = int(os.environ.get("chat_id"))
admin_id = int(os.environ.get("admin_id"))
channel_url = os.environ.get("channel_url")
cryptobot_token = os.environ.get("cryptobot_token")

bot_username = ""  # Само обновится
