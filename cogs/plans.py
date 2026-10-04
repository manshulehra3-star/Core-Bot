import discord
import json
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed
from utils.helpers import format_currency

class PlansCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    plan_group = app_commands.Group(name="plan", description="Manage hosting plans")

    @plan_group.command(name="create", description="Create a new server or VPS hosting plan")
    @app_commands.checks.has_permissions(administrator=True)
    async def plan_create(
        self, interaction: discord.Interaction, name: str, category: str, price: float,
        ram: str, cpu: str, disk: str, description: str
    ):
        await self.bot.db.execute(
            "INSERT INTO plans (name, category, price, ram, cpu, disk, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, category, price, ram, cpu, disk, description)
        )
        embed = CoreEmbed.success("Plan Created", f"Plan **{name}** ({category}) created at **{format_currency(price)}/mo**.")
        await interaction.response.send_message(embed=embed)

    @plan_group.command(name="list", description="Browse available hosting plans")
    async def plan_list(self, interaction: discord.Interaction):
        plans = await self.bot.db.fetchall("SELECT * FROM plans WHERE enabled = 1")
        if not plans:
            await interaction.response.send_message("No plans are currently published.", ephemeral=True)
            return

        embed = CoreEmbed.base("📦 INFINITE CORE HOSTING PLANS", "High performance infrastructure tailored for your needs.")
        for p in plans:
            embed.add_field(
                name=f"{p['name']} — {format_currency(p['price'])}/mo",
                value=f"**Category:** {p['category']}\n**RAM:** {p['ram']} | **CPU:** {p['cpu']} | **Disk:** {p['disk']}\n_{p['description']}_",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PlansCog(bot))
  
