import json
from datetime import datetime, timedelta
from config import MSK
import disnake
from debug import debug

streak_icon = "🔥"

async def streak_system(member):

    with open("database/streak.json", "r", encoding="utf-8") as streak_db_file:
        streak_db = json.load(streak_db_file)

    if str(member.id) in streak_db:

        if streak_db[str(member.id)]["enabled"] == False:
            return
        
        current_time = datetime.now(MSK)
        last_message = datetime.fromisoformat(streak_db[str(member.id)]["last_message"])

        if last_message.date() == current_time.date():
            return
        elif (current_time.date() - last_message.date()).days == 1:
            streak_db[str(member.id)]["last_message"] = current_time.isoformat()
            streak_db[str(member.id)]["streak"] += 1
            try:
                await member.edit(nick=streak_db[str(member.id)]["original_nick"] + " " + streak_icon + " " + str(streak_db[str(member.id)]["streak"]))
            except disnake.Forbidden as e:
                await debug(f"Не удалось изменить ник пользователю {member}: {e}")
        else:
            streak_db[str(member.id)]["last_message"] = current_time.isoformat()
            streak_db[str(member.id)]["streak"] = 1
            try:
                await member.edit(nick=streak_db[str(member.id)]["original_nick"] + " " + streak_icon + " " + str(streak_db[str(member.id)]["streak"]))
            except disnake.Forbidden as e:
                await debug(f"Не удалось изменить ник пользователю {member}: {e}")

    else:
        streak_db[str(member.id)] = {
            "streak": 1,
            "last_message": datetime.now(MSK).isoformat(),
            "original_nick": member.display_name,
            "enabled": True
        }
        try:
            await member.edit(nick=streak_db[str(member.id)]["original_nick"] + " " + streak_icon + " " + str(streak_db[str(member.id)]["streak"]))
        except disnake.Forbidden as e:
            await debug(f"Не удалось изменить ник новому пользователю: {e}")

    with open("database/streak.json", "w", encoding="utf-8") as streak_db_file:
        json.dump(streak_db, streak_db_file, ensure_ascii=False, indent=4)

async def streak_change(member, value: bool):

    with open("database/streak.json", "r", encoding="utf-8") as streak_db_file:
        streak_db = json.load(streak_db_file)
    
    if str(member.id) in streak_db:

        if streak_db[str(member.id)]["enabled"] != value:
            streak_db[str(member.id)]["enabled"] = value

            with open("database/streak.json", "w", encoding="utf-8") as streak_db_file:
                json.dump(streak_db, streak_db_file, ensure_ascii=False, indent=4)
        else:
            return 0