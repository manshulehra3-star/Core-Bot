import discord
from discord.ext import commands
from discord import app_commands
from integrations.minecraft_panel import MinecraftPanelAPI
from utils.embeds import CoreEmbed

class MinecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mc_api = MinecraftPanelAPI()

    @app_commands.command(name="minecraft", description="Check Minecraft infrastructure status")
    async def mc_status(self, interaction: discord.Interaction):
        embed = CoreEmbed.base("⛏️ Minecraft Infrastructure", "Node status: **Online**\nLatency: 12ms")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MinecraftCog(bot))
  
