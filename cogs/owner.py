import os
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed
from utils.permissions import is_owner

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    qr_group = app_commands.Group(name="qr", description="QR Payment configuration")

    @app_commands.command(name="add_qr", description="Configure server payment QR image URL")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_qr(self, interaction: discord.Interaction, image_url: str):
        await self.bot.db.execute(
            "INSERT OR REPLACE INTO qr_config (id, image_path_or_url) VALUES (1, ?)",
            (image_url,)
        )
        embed = CoreEmbed.success("QR Code Updated", f"New QR Image set to:\n{image_url}")
        embed.set_image(url=image_url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="view_qr", description="View active payment QR code")
    async def view_qr(self, interaction: discord.Interaction):
        qr = await self.bot.db.fetchone("SELECT image_path_or_url FROM qr_config WHERE id = 1")
        if not qr:
            await interaction.response.send_message("No QR Code configured.", ephemeral=True)
            return
        embed = CoreEmbed.base("💳 Active Payment QR Code")
        embed.set_image(url=qr["image_path_or_url"])
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description="View system resource statistics")
    async def botinfo(self, interaction: discord.Interaction):
        import psutil
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        embed = CoreEmbed.base(
            "💻 System Resource Usage",
            f"**CPU Load:** {cpu}%\n"
            f"**RAM Usage:** {mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB ({mem.percent}%)"
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
  
