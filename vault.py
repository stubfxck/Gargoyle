from debug import debug
import json
import random
from datetime import datetime, timedelta
from config import MSK

m = "✨"

# Изменения баланса в бд, удаление/добавления баланса и детект нового пользователя в бд.
async def balance_change(name, value, f):

    name = str(name)

    with open("database/vault.json", "r", encoding="utf-8") as db:
        db_data = json.load(db)
        if name in db_data:
            match f:
                case "+":
                    db_data[name] += value
                    await debug(f"Баланс у <@{name}> успешно обновлен, текущий баланс: {db_data[name]} {m}", log=True)
                case "-":
                    db_data[name] -= value
                    await debug(f"Баланс у <@{name}> успешно обновлен, текущий баланс: {db_data[name]} {m}", log=True)
                case _:
                    await debug("Введено неизвестное значение")
        else:
            match f:
                case "+":
                    db_data[name] = value
                    await debug(f"Новый пользователь в бд! Выдано {db_data[name]} {m}, пользователю <@{name}>", log=True)
                case "-":
                    db_data[name] = 0
                    await debug(f"Новый пользователь в бд! Ничего не списано")
                case _:
                    db_data[name] = 0
                    await debug("Новый пользователь в бд! Введено неизвестное значение")

    with open("database/vault.json", "w", encoding="utf-8") as db:
        json.dump(db_data, db, ensure_ascii=False, indent=4)

async def balance_view(name):
    name = str(name)

    with open("database/vault.json", "r", encoding="utf-8") as db:
        db_data = json.load(db)
        if name in db_data:
            balance = db_data[name]

            await debug(f"Запросился баланс пользователя <@{name}>. Он составил {balance} {m}", log=True)

            return balance
        else:
            await debug(f"Запросился баланс пользователя <@{name}>. Это новый пользователь")

            with open("database/vault.json", "w", encoding="utf-8") as db:
                db_data[name] = 0
                json.dump(db_data, db, ensure_ascii=False, indent=4)

            return 0

async def daily_reward(name):
    name = str(name)

    with open("database/daily_cooldown.json", "r", encoding="utf-8") as cooldowns_db:
        data = json.load(cooldowns_db)
    
    if name not in data or datetime.fromisoformat(data[name]) <= datetime.now(MSK):
        reward = 50 + random.randint(1, 100)
        await debug(f"Пользователь <@{name}> получил награду {reward} {m}", log=True)

        await balance_change(name, reward, "+")

        data[name] = (datetime.now(MSK) + timedelta(days=1)).isoformat()

        with open("database/daily_cooldown.json", "w", encoding="utf-8") as cooldowns_db:
            data = json.dump(data, cooldowns_db, ensure_ascii=False, indent=4)

        return reward
    else:
        return data[name]

if __name__ == "__main__":
    print("Это модуль Gargoyle, который не предназначен для запуска напрямую.\nПожалуйста, запустите main.py для использования бота.")
    pass