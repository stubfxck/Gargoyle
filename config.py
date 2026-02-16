from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение переменных окружения
GUILD_ID = int(os.getenv("GUILD_ID"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
BOT_TOKEN = os.getenv("BOT_TOKEN")
MEMBER_COUNT_CHANNEL_NEED = os.getenv("MEMBER_COUNT_CHANNEL_NEED", "False").lower() == "true"
MEMBER_COUNT_CHANNEL = int(os.getenv("MEMBER_COUNT_CHANNEL"))

if __name__ == "__main__":
    print("Это модуль Gargoyle, который не предназначен для запуска напрямую.\nПожалуйста, запустите main.py для использования бота.")
    pass