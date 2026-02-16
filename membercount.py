import asyncio
import re

async def update_member_count(bot, GUILD_ID, channel_id, update_interval):
    from debug import debug
    await debug(f"Получили GUILD_ID: {GUILD_ID}, Тип: {type(GUILD_ID)}")

    while True:
        # Проверяем гильдию
        guild = bot.get_guild(GUILD_ID)
        if guild is None:
            await debug(f"Ошибка: Не удалось найти сервер с ID {GUILD_ID}.")
            await asyncio.sleep(update_interval)
            continue
        
        await debug(f"Сервер найден: {guild.name} (ID: {guild.id}).")
        member_count = guild.member_count
        
        channel = bot.get_channel(channel_id)
        if channel is None:
            await debug(f"Ошибка: Не удалось найти канал с ID {channel_id}.")
            await asyncio.sleep(update_interval)
            continue
        
        await debug(f"Канал найден: {channel.name} (ID: {channel.id}).")
        
        # Проверяем, нужно ли обновлять
        template = r"Members:\s*(\d+)"
        match = re.search(template, channel.name)
        
        if match:
            current_count = int(match.group(1))
            if current_count == member_count:
                await debug(f"Количество не изменилось: {member_count}. Пропускаем.")
                await asyncio.sleep(update_interval)
                continue
        
        
        try:
            await channel.edit(name=f"Members: {member_count}")
            await debug(f"Успешно обновлено: {member_count}")
        except Exception as e:
            await debug(f"Ошибка при обновлении: {e}")
        
        
        await asyncio.sleep(update_interval)

if __name__ == "__main__":
    print("Это модуль Gargoyle, который не предназначен для запуска напрямую.\nПожалуйста, запустите main.py для использования бота.")
    pass