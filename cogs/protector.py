import discord
from discord.ext import commands
from utils.embeds import CoreEmbed
from utils.logging import log_to_channel

class ProtectorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_message_counts = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Simple Anti-Mention Spam Protection
        if len(message.mentions) > 5:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, mass mention detected and message purged.", delete_after=5)
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(ProtectorCog(bot))
  
