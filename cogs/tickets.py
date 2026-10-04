import os
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed
from utils.permissions import is_staff, is_owner
from utils.helpers import generate_ticket_id, sanitize_channel_name
from utils.logging import log_to_channel

class TicketActionButtons(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.primary, emoji="✋", custom_id="ticket_btn_claim")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = self.bot.db
        ticket = await db.fetchone("SELECT * FROM tickets WHERE channel_id = ?", (interaction.channel_id,))
        if not ticket:
            await interaction.response.send_message("This channel is not an active ticket.", ephemeral=True)
            return

        if ticket["claimed_by"]:
            await interaction.response.send_message(f"Ticket already claimed by <@{ticket['claimed_by']}>.", ephemeral=True)
            return

        await db.execute("UPDATE tickets SET claimed_by = ? WHERE channel_id = ?", (interaction.user.id, interaction.channel_id))
        embed = CoreEmbed.success("Ticket Claimed", f"This ticket is now handled by {interaction.user.mention}.")
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="ticket_btn_close")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = self.bot.db
        ticket = await db.fetchone("SELECT * FROM tickets WHERE channel_id = ?", (interaction.channel_id,))
        if not ticket:
            await interaction.response.send_message("This channel is not an active ticket.", ephemeral=True)
            return

        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await db.execute("UPDATE tickets SET status = 'closed', closed_at = CURRENT_TIMESTAMP WHERE channel_id = ?", (interaction.channel_id,))

        # Log Ticket Close
        log_chan_id = os.getenv("TICKET_LOG_CHANNEL_ID")
        log_embed = CoreEmbed.warning("Ticket Closed", f"Ticket **{ticket['ticket_id']}** closed by {interaction.user.mention}.")
        await log_to_channel(self.bot, log_chan_id, log_embed)

        await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(seconds=5))
        await interaction.channel.delete(reason="Ticket Closed")

    @discord.ui.button(label="Add User", style=discord.ButtonStyle.secondary, emoji="👤", custom_id="ticket_btn_add")
    async def add_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Use `/ticket add @user` to add someone to this ticket.", ephemeral=True)

    @discord.ui.button(label="Rename", style=discord.ButtonStyle.secondary, emoji="✏️", custom_id="ticket_btn_rename")
    async def rename_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Use `/ticket rename new-name` to rename this ticket.", ephemeral=True)

class TicketSelectCategoryView(discord.ui.View):
    def __init__(self, bot, categories):
        super().__init__(timeout=None)
        self.bot = bot
        options = []
        for cat in categories:
            options.append(discord.SelectOption(
                label=cat["name"],
                description=cat["description"][:100],
                emoji=cat["emoji"],
                value=cat["name"]
            ))

        select = discord.ui.Select(
            placeholder="Choose a support ticket category...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_category_select"
        )
        select.callback = self.category_selected
        self.add_item(select)

    async def category_selected(self, interaction: discord.Interaction):
        cat_name = interaction.data["values"][0]
        db = self.bot.db

        user_tickets = await db.fetchall("SELECT * FROM tickets WHERE user_id = ? AND status = 'open'", (interaction.user.id,))
        if len(user_tickets) >= 3:
            await interaction.response.send_message("You already have 3 open tickets. Please resolve them first.", ephemeral=True)
            return

        ticket_id = generate_ticket_id()
        guild = interaction.guild
        cat_id = os.getenv("TICKET_CATEGORY_ID")
        discord_cat = guild.get_channel(int(cat_id)) if cat_id else None

        channel_name = sanitize_channel_name(f"{cat_name}-{interaction.user.name}")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        channel = await guild.create_text_channel(name=channel_name, category=discord_cat, overwrites=overwrites)
        
        await db.execute(
            "INSERT INTO tickets (ticket_id, channel_id, guild_id, user_id, category_name) VALUES (?, ?, ?, ?, ?)",
            (ticket_id, channel.id, guild.id, interaction.user.id, cat_name)
        )

        embed = CoreEmbed.ticket(
            f"Ticket Created: {ticket_id}",
            f"Welcome {interaction.user.mention}!\nCategory: **{cat_name}**\n\nOur support team will assist you shortly. Use buttons below to manage."
        )
        await channel.send(content=f"{interaction.user.mention}", embed=embed, view=TicketActionButtons(self.bot))
        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)

class TicketsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ticket_group = app_commands.Group(name="ticket", description="Ticket management system")

    @ticket_group.command(name="setup", description="Deploy the primary ticket panel embed")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_setup(self, interaction: discord.Interaction):
        categories = await self.bot.db.fetchall("SELECT * FROM ticket_categories")
        embed = CoreEmbed.ticket(
            "INFINITE CORE • Support & Ordering Panel",
            "Select the category below that best describes your inquiry to open a dedicated support channel."
        )
        view = TicketSelectCategoryView(self.bot, categories)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Ticket panel deployed.", ephemeral=True)

    @ticket_group.command(name="close", description="Close the current ticket")
    async def ticket_close(self, interaction: discord.Interaction):
        ticket = await self.bot.db.fetchone("SELECT * FROM tickets WHERE channel_id = ?", (interaction.channel_id,))
        if not ticket:
            await interaction.response.send_message("This channel is not a ticket.", ephemeral=True)
            return
        await interaction.response.send_message("Closing ticket...")
        await self.bot.db.execute("UPDATE tickets SET status = 'closed' WHERE channel_id = ?", (interaction.channel_id,))
        await interaction.channel.delete()

    @ticket_group.command(name="add", description="Add a user to the ticket")
    async def ticket_add(self, interaction: discord.Interaction, user: discord.Member):
        ticket = await self.bot.db.fetchone("SELECT * FROM tickets WHERE channel_id = ?", (interaction.channel_id,))
        if not ticket:
            await interaction.response.send_message("This is not a ticket channel.", ephemeral=True)
            return
        await interaction.channel.set_permissions(user, read_messages=True, send_messages=True)
        await interaction.response.send_message(f"Added {user.mention} to the ticket.")

    @ticket_group.command(name="rename", description="Rename current ticket channel")
    async def ticket_rename(self, interaction: discord.Interaction, new_name: str):
        ticket = await self.bot.db.fetchone("SELECT * FROM tickets WHERE channel_id = ?", (interaction.channel_id,))
        if not ticket:
            await interaction.response.send_message("This is not a ticket channel.", ephemeral=True)
            return
        clean_name = sanitize_channel_name(new_name)
        await interaction.channel.edit(name=clean_name)
        await interaction.response.send_message(f"Ticket channel renamed to `{clean_name}`.")

async def setup(bot):
    await bot.add_cog(TicketsCog(bot))
  
