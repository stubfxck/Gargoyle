from gargoyle import consoletag
import disnake
from disnake.ext import commands
from membercount import update_member_count
from config import BOT_TOKEN, GUILD_ID, MEMBER_COUNT_CHANNEL_NEED, MEMBER_COUNT_CHANNEL, MEMBER_COUNT_UPDATE_INTERVAL
import asyncio
import datetime

# Инициализируем бота с префиксом "!" и всеми необходимыми интентами
bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

@bot.slash_command(guild_id=GUILD_ID)
async def detect_language(inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
    if member is None:
        member = inter.author

    role_ids = [role.id for role in member.roles]

    if 1371106230831026256 in role_ids:
        title = "Детект языка"
        desc = f"Ваш язык: РУ"
    elif 1371106275370471484 in role_ids:
        title = "Lang detect"
        desc = f"Your language: EN"
    else:
        title = "Lang detect"
        desc = f"Your language: EN"

    embed = disnake.Embed(
             title=title,
             description=desc,
             color=0x040404,
             timestamp=datetime.datetime.now(),
             )
    
    return await inter.response.send_message(embed=embed)

if __name__ == "__main__":

    # Показываем красивую картинку в консоли при запуске
    print(consoletag())

    # Проверяем, что токен бота был успешно загружен
    if not BOT_TOKEN:
        print("Ошибка: Не найден токен бота. \n\nПожалуйста, установите переменную окружения BOT_TOKEN в файле .env.")
        exit(1)

    else:
        print(f"{BOT_TOKEN[:4]}...{BOT_TOKEN[-4:]} - Токен бота успешно загружен.")

    @bot.event
    async def on_ready():
        print("Gargoyle инициализирован и готов к работе!")
        if MEMBER_COUNT_CHANNEL_NEED:
            bot.loop.create_task(update_member_count(bot, GUILD_ID, MEMBER_COUNT_CHANNEL, MEMBER_COUNT_UPDATE_INTERVAL))

    bot.run(BOT_TOKEN)