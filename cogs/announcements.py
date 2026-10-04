import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed

class AnnouncementsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Broadcast an official server announcement")
    @app_commands.checks.has_permissions(administrator=True)
    async def announce(self, interaction: discord.Interaction, title: str, channel: discord.TextChannel, message: str):
        embed = CoreEmbed.base(f"📢 {title}", message)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Announcement posted in {channel.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AnnouncementsCog(bot))
  
