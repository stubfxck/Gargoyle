from dotenv import load_dotenv
import os
from datetime import timedelta, timezone
import disnake
from datetime import datetime

# Загрузка переменных окружения из .env файла
load_dotenv("config/.env")

# Текущая таймзона
MSK = timezone(timedelta(hours=3))

# Получение переменных окружения
GUILD_ID = int(os.getenv("GUILD_ID"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
BOT_TOKEN = os.getenv("BOT_TOKEN")
MEMBER_COUNT_CHANNEL_NEED = os.getenv("MEMBER_COUNT_CHANNEL_NEED", "False").lower() == "true"
MEMBER_COUNT_CHANNEL = int(os.getenv("MEMBER_COUNT_CHANNEL"))
MEMBER_COUNT_UPDATE_INTERVAL = int(os.getenv("MEMBER_COUNT_UPDATE_INTERVAL"))
AUTO_SPAM_MOD_CHANNEL = int(os.getenv("AUTO_SPAM_MOD_CHANNEL"))
BAN_ROLE_ID = int(os.getenv("BAN_ROLE_ID"))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

# Шаблон Embed сообщения
def embed_placeholder(title, desc):
    embed = disnake.Embed(
                title=title,
                description=desc,
                color=0x040404,
                timestamp=datetime.now(MSK),
            )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1030797893101178960/1039223508242276383/Rectangle_369.png?ex=69e50ad0&is=69e3b950&hm=ad9e5381eb5f3a9087b20e9ff08780c4cd22fc16dc4fd579e79b17ac84924c7e")
    return embed

if __name__ == "__main__":
    print("Это модуль Gargoyle, который не предназначен для запуска напрямую.\nПожалуйста, запустите main.py для использования бота.")
    pass