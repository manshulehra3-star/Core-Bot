import os
import discord
from discord.ext import commands

def is_owner():
    async def predicate(ctx_or_interaction) -> bool:
        owner_id = int(os.getenv("OWNER_ID", "0"))
        user_id = ctx_or_interaction.author.id if isinstance(ctx_or_interaction, commands.Context) else ctx_or_interaction.user.id
        if user_id == owner_id:
            return True
        raise commands.NotOwner("Only the bot owner can execute this command.")
    return commands.check(predicate)

def is_staff():
    async def predicate(ctx_or_interaction) -> bool:
        member = ctx_or_interaction.author if isinstance(ctx_or_interaction, commands.Context) else ctx_or_interaction.user
        if isinstance(member, discord.User):
            return False
        if member.guild_permissions.administrator or member.guild_permissions.manage_guild:
            return True
        owner_id = int(os.getenv("OWNER_ID", "0"))
        if member.id == owner_id:
            return True
        staff_roles = ["Staff", "Admin", "Support Team", "Moderator"]
        return any(role.name in staff_roles for role in member.roles)
    return commands.check(predicate)
