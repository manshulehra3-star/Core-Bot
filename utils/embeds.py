import discord
from datetime import datetime

class CoreEmbed:
    COLOR_PRIMARY = 0x5865F2    # Blurple / Infinite Core Blue
    COLOR_SUCCESS = 0x57F287    # Green
    COLOR_WARNING = 0xFEE75C    # Yellow
    COLOR_DANGER = 0xED4245     # Red
    COLOR_DARK = 0x2B2D31       # Hosting Dark Panel

    @staticmethod
    def base(title: str, description: str = "", color: int = COLOR_PRIMARY) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="INFINITE CORE • Next-Gen Infrastructure", icon_url=None)
        return embed

    @classmethod
    def success(cls, title: str, description: str) -> discord.Embed:
        return cls.base(f"✅ {title}", description, cls.COLOR_SUCCESS)

    @classmethod
    def danger(cls, title: str, description: str) -> discord.Embed:
        return cls.base(f"❌ {title}", description, cls.COLOR_DANGER)

    @classmethod
    def warning(cls, title: str, description: str) -> discord.Embed:
        return cls.base(f"⚠️ {title}", description, cls.COLOR_WARNING)

    @classmethod
    def ticket(cls, title: str, description: str) -> discord.Embed:
        return cls.base(f"🎫 {title}", description, cls.COLOR_PRIMARY)

    @classmethod
    def payment(cls, title: str, description: str) -> discord.Embed:
        return cls.base(f"💳 {title}", description, cls.COLOR_PRIMARY)
      
