from config import DEBUG, LOG_CHANNEL, embed_placeholder

_bot = None

def init(bot):
    global _bot
    _bot = bot

# Функция для вывода отладочных сообщений, которая проверяет флаг DEBUG
async def debug(message, log=False):
    if DEBUG:
        print(f"DEBUG: {message}")

        if log:
            title = "LOG"
            desc = message

            embed = embed_placeholder(title, desc)

            if _bot:
                channel = _bot.get_channel(LOG_CHANNEL)
                await channel.send(embed=embed)

if __name__ == "__main__":
    print("Это модуль Gargoyle, который не предназначен для запуска напрямую.\nПожалуйста, запустите main.py для использования бота.")
    pass