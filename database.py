import os
import json
from debug import debug

async def isdatabase():

    db_list = ["vault.json", "daily_cooldown.json", "streak.json"]

    if not os.path.exists("database"):
        await debug("Папки database нету, создаем...")
        os.mkdir("database")

    for item in db_list:
        if not os.path.exists(f"database/{item}"):
            await debug(f"{item} отсутствует, создаем...")
            with open(f"database/{item}", "w", encoding="utf-8") as db:
                json.dump({}, db)

if __name__ == "__main__":
    print("Это модуль Gargoyle, который не предназначен для запуска напрямую.\nПожалуйста, запустите main.py для использования бота.")
    pass