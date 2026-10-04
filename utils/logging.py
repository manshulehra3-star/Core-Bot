import logging
import discord
from typing import Optional

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("./data/infinite_core.log")
        ]
    )

async def log_to_channel(bot: discord.Client, channel_id: Optional[int], embed: discord.Embed):
    if not channel_id:
        return
    channel = bot.get_channel(int(channel_id))
    if channel and isinstance(channel, discord.TextChannel):
        try:
            await channel.send(embed=embed)
        except Exception as e:
            logging.error(f"Failed to log to channel {channel_id}: {e}")
          
