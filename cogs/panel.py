import discord
from discord.ext import commands
from discord import app_commands
from integrations.svm_api import SVMPanelAPI
from utils.embeds import CoreEmbed

class PanelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.svm = SVMPanelAPI()

    @app_commands.command(name="panel", description="Check status of hosting control panel")
    async def panel_status(self, interaction: discord.Interaction):
        status = await self.svm.check_status()
        embed = CoreEmbed.base("🖥️ Control Panel Integration Status", f"**Status:** {status.get('status')}\n**Details:** {status}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PanelCog(bot))
  
