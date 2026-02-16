from config import DEBUG

# Функция для вывода отладочных сообщений, которая проверяет флаг DEBUG
async def debug(message):
    if DEBUG:
        print(f"DEBUG: {message}")
    else:
        pass

if __name__ == "__main__":
    print("Это модуль Gargoyle, который не предназначен для запуска напрямую.\nПожалуйста, запустите main.py для использования бота.")
    pass