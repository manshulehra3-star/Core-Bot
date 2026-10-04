import os
import discord
from discord.ext import commands
from utils.embeds import CoreEmbed

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        chan_id = os.getenv("WELCOME_CHANNEL_ID")
        if chan_id:
            channel = member.guild.get_channel(int(chan_id))
            if channel:
                embed = CoreEmbed.base(
                    f"👋 Welcome to {member.guild.name}!",
                    f"Hello {member.mention}, welcome aboard!\nMember count: **{member.guild.member_count}**\n\nNeed assistance? Open a ticket or talk to our AI."
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=embed)

        dm_enabled = os.getenv("WELCOME_DM_ENABLED", "true").lower() == "true"
        if dm_enabled:
            try:
                dm_embed = CoreEmbed.base(
                    f"Welcome to Infinite Core!",
                    f"Hi {member.name}, thanks for joining **{member.guild.name}**!\nExplore our plans with `/plan list` or get instant support via `/ai`."
                )
                await member.send(embed=dm_embed)
            except:
                pass

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
  
