import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban a member from the guild")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Violation of rules"):
        await user.ban(reason=reason)
        embed = CoreEmbed.danger("Member Banned", f"**User:** {user.mention}\n**Reason:** {reason}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kick", description="Kick a member from the guild")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Violation of rules"):
        await user.kick(reason=reason)
        embed = CoreEmbed.warning("Member Kicked", f"**User:** {user.mention}\n**Reason:** {reason}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clear", description="Bulk clear messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Purged {len(deleted)} messages.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
  
