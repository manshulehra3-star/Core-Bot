import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed
from utils.permissions import is_staff

class PromosCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    promo_group = app_commands.Group(name="promo", description="Manage promotional discount codes")

    @promo_group.command(name="create", description="Create a new promotional code")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_promo(
        self, interaction: discord.Interaction, code: str, discount_value: float,
        discount_type: str = "percentage", usage_limit: int = 100, min_amount: float = 0.0
    ):
        code_upper = code.upper()
        await self.bot.db.execute(
            "INSERT INTO promo_codes (code, discount_type, discount_value, usage_limit, min_amount) VALUES (?, ?, ?, ?, ?)",
            (code_upper, discount_type, discount_value, usage_limit, min_amount)
        )
        embed = CoreEmbed.success("Promo Code Created", f"Code: **{code_upper}**\nDiscount: {discount_value}{'%' if discount_type=='percentage' else '$'}\nLimit: {usage_limit}")
        await interaction.response.send_message(embed=embed)

    @promo_group.command(name="list", description="List active promo codes")
    async def list_promos(self, interaction: discord.Interaction):
        codes = await self.bot.db.fetchall("SELECT * FROM promo_codes WHERE enabled = 1")
        if not codes:
            await interaction.response.send_message("No active promo codes available.", ephemeral=True)
            return

        desc = ""
        for c in codes:
            desc += f"• **{c['code']}**: {c['discount_value']}{'%' if c['discount_type']=='percentage' else '$'} off (Uses: {c['used_count']}/{c['usage_limit']})\n"
        
        embed = CoreEmbed.base("🎟️ Active Promo Codes", desc)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PromosCog(bot))
  
