from gargoyle import consoletag, lang_detect
import disnake
from disnake.ext import commands
from membercount import update_member_count
from config import BOT_TOKEN, GUILD_ID, MEMBER_COUNT_CHANNEL_NEED, MEMBER_COUNT_CHANNEL, MEMBER_COUNT_UPDATE_INTERVAL, embed_placeholder
from datetime import datetime, timedelta, timezone
from database import isdatabase
from vault import balance_change, balance_view, daily_reward, m
import asyncio
import events
from streaks import streak_change, streak_icon
import json
from debug import debug, init

proxy = "http://127.0.0.1:6666"



bot = commands.InteractionBot(intents=disnake.Intents.all(), proxy=proxy)

# Текст ошибки при попытке применить какую либо команду к боту
bot_detection_text = {
    "eng": "You cant apply this command to bot",
    "ru": "Вы не можете применять данное действие к боту"
}



# =================================================================================================
# ----------------------================== ADMIN COMMANDS ==================-----------------------
# =================================================================================================

# VAULT SYSTEM

@bot.slash_command(guild_id=GUILD_ID, default_member_permissions=disnake.Permissions(administrator=True))
async def get(inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None, value: int = None):
    await inter.response.defer()
    
    if member is None:
        member = inter.author
    elif member.bot:
        embed = embed_placeholder("Error", lang_detect(bot_detection_text["ru"], bot_detection_text["eng"], inter.author))
        return await inter.edit_original_response(embed=embed)
    
    if value is None or value <= 0:
        embed = embed_placeholder(lang_detect("Ошибка", "Error", inter.author), lang_detect("Укажите правильное значение", "Write valid value", inter.author))
        return await inter.edit_original_response(embed=embed)

    await balance_change(member.id, value, "+")

    title = lang_detect(
        "Баланс успешно обновлен", 
        "Balance successfully updated", 
        inter.author
        )
    
    desc = lang_detect(
        f"Выдано **{value}** {m} пользователю: <@{member.id}>", 
        f"Gived **{value}** {m} for user: <@{member.id}>", 
        inter.author
        )

    embed = embed_placeholder(title, desc)

    return await inter.edit_original_response(embed=embed)

@bot.slash_command(guild_id=GUILD_ID, default_member_permissions=disnake.Permissions(administrator=True))
async def take(inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None, value: int = None):
    await inter.response.defer()
    
    if member is None:
        member = inter.author
    elif member.bot:
        embed = embed_placeholder("Error", lang_detect(bot_detection_text["ru"], bot_detection_text["eng"], inter.author))
        return await inter.edit_original_response(embed=embed)

    if value is None or value <= 0:
        embed = embed_placeholder(lang_detect("Ошибка", "Error", inter.author), lang_detect("Укажите правильное значение", "Write valid value", inter.author))
        return await inter.edit_original_response(embed=embed)

    await balance_change(member.id, value, "-")

    title = lang_detect(
        "Баланс успешно обновлен", 
        "Balance successfully updated", 
        inter.author
        )
    
    desc = lang_detect(
        f"Удалено **{value}** {m} у пользователя <@{member.id}>", 
        f"Taken **{value}** {m} for user: <@{member.id}>", 
        inter.author
        )

    embed = embed_placeholder(title, desc)

    return await inter.edit_original_response(embed=embed)

# CHAT CLEANER

@bot.slash_command(guild_id=GUILD_ID, default_member_permissions=disnake.Permissions(administrator=True))
async def clear(inter: disnake.ApplicationCommandInteraction, value = None):
    await inter.response.defer()

    try:
        value = int(value)
    except (ValueError, TypeError):
        pass

    title = lang_detect(
        "Очистка чата", 
        "Chat cleaner", 
        inter.author
    )
    
    desc = lang_detect(
        f"Успешно очищено `{value}` сообщений пользователем <@{inter.author.id}>", 
        f"Successfully cleaned `{value}` messages by <@{inter.author.id}>", 
        inter.author
    )
    if isinstance(value, int):
        await inter.channel.purge(limit=value+1)

    elif value != None and value.lower() == "all":
        await inter.channel.purge()

    else:
        desc = lang_detect(
                f"Введите количество сообщений, или `all` для полной очистки", 
                f"Write correct value, or `all` for clear all messages in chat", 
                inter.author
            )
        embed = embed_placeholder(title, desc)
        return await inter.edit_original_response(embed=embed)
                
    await asyncio.sleep(1)

    embed = embed_placeholder(title, desc)

    return await inter.channel.send(embed=embed)



# =================================================================================================
# ----------------------===================== COMMANDS =====================-----------------------
# =================================================================================================

@bot.slash_command(guild_id=GUILD_ID)
async def balance(inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
    await inter.response.defer()
    
    if member is None:
        member = inter.author

        member_balance = await balance_view(member.id)

        desc = lang_detect(
            f"Ваш баланс: **{member_balance}** {m}", 
            f"Your balance: **{member_balance}** {m}", 
            inter.author
        )

    elif member.bot:
        embed = embed_placeholder("Error", lang_detect(bot_detection_text["ru"], bot_detection_text["eng"], inter.author))
        return await inter.edit_original_response(embed=embed)
    
    else:
        member_balance = await balance_view(member.id)
        
        desc = lang_detect(
            f"Баланс пользователя <@{member.id}> составляет **{member_balance}** {m}", 
            f"<@{member.id}> balance: **{member_balance}** {m}", 
            inter.author
        )

    title = lang_detect(
        "Баланс", 
        "Balance", 
        inter.author
    )

    embed = embed_placeholder(title, desc)

    return await inter.edit_original_response(embed=embed)

@bot.slash_command(guild_id=GUILD_ID)
async def daily(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()

    reward = await daily_reward(inter.author.id)

    title = lang_detect(
        "Ежедневная награда", 
        "Daily reward", 
        inter.author
        )

    if type(reward) == int:
        desc = lang_detect(
            f"Вы успешно получили **{reward}** {m}", 
            f"You successfully get **{reward}** {m}", 
            inter.author
            )
    else:
        desc = lang_detect(
            f"Вы уже получали награду ранее. Подождите до: {f"<t:{int(datetime.fromisoformat(reward).timestamp())}:f>"}", 
            f"You already get reward. Come back in {f"<t:{int(datetime.fromisoformat(reward).timestamp())}:f>"}", 
            inter.author
            )
    

    embed = embed_placeholder(title, desc)

    return await inter.edit_original_response(embed=embed)

@bot.slash_command(guild_id=GUILD_ID)
async def streak(inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=["enable", "disable"])):
    await inter.response.defer()

    desc = lang_detect(
            f"Ошибка, стрик уже `включен/выключен`", 
            f"Error, streak already `enabled/disabled`", 
            inter.author
        )

    match action:
        case "enable":
            data = await streak_change(inter.author, True)
            if data != 0:
                desc = lang_detect(
                    f"Стрик успешно `включен`", 
                    f"Streak successfully `enabled`", 
                    inter.author
                )
        case "disable":
            data = await streak_change(inter.author, False)
            if data != 0:
                desc = lang_detect(
                    f"Стрик успешно `выключен`", 
                    f"Streak successfully `disabled`", 
                    inter.author
                )

    title = lang_detect(
        "Стрики сообщений", 
        "Message streaks", 
        inter.author
    )

    embed = embed_placeholder(title, desc)

    return await inter.edit_original_response(embed=embed)

@bot.slash_command(guild_id=GUILD_ID)
async def nick(inter: disnake.ApplicationCommandInteraction, name: str, member: disnake.Member = None):
    await inter.response.defer()

    desc = lang_detect(
                f"Имя успешно изменено на `{name}`", 
                f"Name successfully changed. New name: `{name}`", 
                inter.author
            )

    if member is None:
        member = inter.author

    with open("database/streak.json", "r", encoding="utf-8") as streak_db_file:
        streak_db = json.load(streak_db_file)
    
    if str(member.id) not in streak_db:
        streak_db[str(member.id)] = {
            "original_nick": member.display_name
        }
    try:
        old_name = streak_db[str(member.id)]["original_nick"]
        await member.edit(nick=name + " " + streak_icon + " " + str(streak_db[str(member.id)].get("streak", 1)))
        await debug(f"Пользователь сменил никнейм:\n\nДо: {old_name}\nПосле: {name}", log=True)

    except disnake.Forbidden as e:
        await debug(f"Не удалось изменить ник пользователю `{member.display_name}`: {e}", log=True)
        desc = lang_detect(
                f"Не удалось изменить имя, по причине: {e}", 
                f"Name not changed. For reason: `{e}`", 
                inter.author
            )
        
    streak_db[str(member.id)]["original_nick"] = name
        

    with open("database/streak.json", "w", encoding="utf-8") as streak_db_file:
        json.dump(streak_db, streak_db_file, ensure_ascii=False, indent=4)
    
    title = lang_detect(
        "Изменить никнейм", 
        "Change nickname", 
        inter.author
    )

    embed = embed_placeholder(title, desc)

    return await inter.edit_original_response(embed=embed)

    


# =================================================================================================
# ----------------------======================= INIT =======================-----------------------
# =================================================================================================

if __name__ == "__main__":

    # Показываем красивую картинку в консоли при запуске
    print(consoletag())

    # Проверяем, что токен бота был успешно загружен
    if not BOT_TOKEN:
        print("Ошибка: Не найден токен бота. \n\nПожалуйста, установите переменную окружения BOT_TOKEN в файле .env.")
        exit(1)

    else:
        print(f"{BOT_TOKEN[:4]}...{BOT_TOKEN[-4:]} - Токен бота успешно загружен.")
    
    events.message_handler(bot)

    @bot.event
    async def on_ready():
        init(bot)
        await isdatabase()
        print("Gargoyle инициализирован и готов к работе!")
        if MEMBER_COUNT_CHANNEL_NEED:
            bot.loop.create_task(update_member_count(bot, GUILD_ID, MEMBER_COUNT_CHANNEL, MEMBER_COUNT_UPDATE_INTERVAL))
    
    bot.run(BOT_TOKEN)