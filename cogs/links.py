import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed

class LinksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="link", description="Manage official links panel")
    async def link_command(self, interaction: discord.Interaction):
        links = await self.bot.db.fetchall("SELECT * FROM links WHERE enabled = 1")
        embed = CoreEmbed.base("🔗 Official Infinite Core Links", "Access our key portals and platforms below:")
        
        view = discord.ui.View()
        if not links:
            view.add_item(discord.ui.Button(label="Website", url="https://infinitecore.net", style=discord.ButtonStyle.link))
            view.add_item(discord.ui.Button(label="Client Panel", url="https://panel.infinitecore.net", style=discord.ButtonStyle.link))
        else:
            for l in links:
                view.add_item(discord.ui.Button(label=l["title"], url=l["url"], style=discord.ButtonStyle.link))

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(LinksCog(bot))
  
