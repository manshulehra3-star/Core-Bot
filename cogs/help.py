import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed
from utils.pagination import PaginatorView

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Interactive Infinite Core Help Documentation")
    async def help_command(self, interaction: discord.Interaction):
        categories = [
            ("🎫 Tickets", ["/ticket setup", "/ticket close", "/ticket add", "/ticket rename"]),
            ("🧠 AI", ["/ai <prompt>", "Mention @InfiniteCore in chat"]),
            ("💳 Payments", ["/pay @user <amount>"]),
            ("📦 Plans", ["/plan list", "/plan create"]),
            ("🎟️ Promo", ["/promo list", "/promo create"]),
            ("🔗 Links", ["/link"]),
            ("📢 Announcements", ["/announce"]),
            ("🛠️ Moderation", ["/ban", "/kick", "/clear"]),
            ("👑 Owner", ["/add qr", "/view qr", "/owner status"])
        ]

        pages = []
        for cat, cmds in categories:
            embed = CoreEmbed.base(f"Help Category: {cat}", "Available Features and Slash Commands:")
            for c in cmds:
                embed.add_field(name=c, value="Production functionality enabled", inline=False)
            pages.append(embed)

        paginator = PaginatorView(pages, interaction.user.id)
        await interaction.response.send_message(embed=pages[0], view=paginator)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
  
