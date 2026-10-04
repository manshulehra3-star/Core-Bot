import os
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

from database.database import Database
from utils.logging import setup_logger
from cogs.tickets import TicketActionButtons

load_dotenv()
setup_logger()
logger = logging.getLogger("InfiniteCore.Main")

class InfiniteCoreBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        self.db = Database(os.getenv("DATABASE_PATH", "./data/infinite_core.db"))

    async def setup_hook(self):
        await self.db.init_db()

        # Register Persistent Views for Tickets across reboots
        self.add_view(TicketActionButtons(self))

        # Dynamically Load Cogs
        initial_extensions = [
            "cogs.tickets",
            "cogs.ai",
            "cogs.payments",
            "cogs.promos",
            "cogs.plans",
            "cogs.links",
            "cogs.welcome",
            "cogs.announcements",
            "cogs.protector",
            "cogs.moderation",
            "cogs.help",
            "cogs.panel",
            "cogs.minecraft",
            "cogs.owner",
        ]

        for ext in initial_extensions:
            try:
                await self.load_extension(ext)
                logger.info(f"Loaded extension: {ext}")
            except Exception as e:
                logger.error(f"Failed to load extension {ext}: {e}")

        # Sync Slash Commands
        guild_id = os.getenv("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"Synced commands to Guild ID: {guild_id}")
        else:
            await self.tree.sync()
            logger.info("Synced global commands.")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="INFINITE CORE Infrastructure | /help"
            )
        )

async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.critical("DISCORD_TOKEN environment variable missing in .env!")
        return

    bot = InfiniteCoreBot()
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
  
