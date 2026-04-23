from streaks import streak_system
from config import AUTO_SPAM_MOD_CHANNEL
from guard import auto_spam_mod

def message_handler(bot):
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        
        if message.channel.id == AUTO_SPAM_MOD_CHANNEL:
            await auto_spam_mod(message)

        
        await streak_system(message.author)