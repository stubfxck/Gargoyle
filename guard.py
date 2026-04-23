from config import BAN_ROLE_ID
import disnake
from debug import debug

async def auto_spam_mod(message):
    try:
        member = message.author
        for channel in message.guild.text_channels:
            await channel.purge(limit=100, check=lambda m: m.author.id == member.id)

        roles_to_remove = [r for r in member.roles if not r.is_default() and not r.managed]
        await member.remove_roles(*roles_to_remove)
        await member.add_roles(message.guild.get_role(BAN_ROLE_ID))

    except disnake.Forbidden as e:
        await debug(f"Не удалось забанить пользователя по причине: {e}")
        # desc = lang_detect(
        #         f"Не удалось изменить имя, по причине: {e}", 
        #         f"Name not changed. For reason: `{e}`", 
        #         inter.author
        #     )