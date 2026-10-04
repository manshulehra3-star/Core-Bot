import os
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import CoreEmbed
from utils.helpers import generate_payment_id, format_currency
from utils.logging import log_to_channel

class PaymentApprovalView(discord.ui.View):
    def __init__(self, bot, payment_id: str):
        super().__init__(timeout=None)
        self.bot = bot
        self.payment_id = payment_id

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success, emoji="✅", custom_id="pay_approve_btn")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = self.bot.db
        pay = await db.fetchone("SELECT * FROM payments WHERE payment_id = ?", (self.payment_id,))
        if not pay:
            await interaction.response.send_message("Payment record not found.", ephemeral=True)
            return

        await db.execute("UPDATE payments SET status = 'approved' WHERE payment_id = ?", (self.payment_id,))
        await db.execute("UPDATE payment_submissions SET status = 'approved', reviewed_by = ? WHERE payment_id = ?", (interaction.user.id, self.payment_id))

        # Notify User
        user = self.bot.get_user(pay["user_id"])
        if user:
            try:
                await user.send(embed=CoreEmbed.success("Payment Verified!", f"Your payment of **{format_currency(pay['amount'])}** (`{self.payment_id}`) was approved! Server provisioning initiated."))
            except:
                pass

        # Trigger Provisioning job record
        await db.execute(
            "INSERT INTO provisioning_jobs (payment_id, user_id, status) VALUES (?, ?, 'pending')",
            (self.payment_id, pay["user_id"])
        )

        await interaction.response.send_message(f"✅ Payment `{self.payment_id}` approved. Customer notified & provisioning queued.", ephemeral=False)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger, emoji="❌", custom_id="pay_reject_btn")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = self.bot.db
        await db.execute("UPDATE payments SET status = 'rejected' WHERE payment_id = ?", (self.payment_id,))
        await db.execute("UPDATE payment_submissions SET status = 'rejected', reviewed_by = ? WHERE payment_id = ?", (interaction.user.id, self.payment_id))

        pay = await db.fetchone("SELECT * FROM payments WHERE payment_id = ?", (self.payment_id,))
        user = self.bot.get_user(pay["user_id"]) if pay else None
        if user:
            try:
                await user.send(embed=CoreEmbed.danger("Payment Rejected", f"Your payment proof for `{self.payment_id}` was rejected by staff. Please open a ticket if you believe this is an error."))
            except:
                pass

        await interaction.response.send_message(f"❌ Payment `{self.payment_id}` rejected.", ephemeral=False)

class SubmitScreenshotModal(discord.ui.Modal, title="Submit Payment Proof"):
    transaction_ref = discord.ui.TextInput(label="Transaction / UTR ID", placeholder="e.g. 123456789012", required=True)
    image_url = discord.ui.TextInput(label="Screenshot Image Direct Link", placeholder="https://cdn.discordapp.com/...", required=True)

    def __init__(self, bot, payment_id: str):
        super().__init__()
        self.bot = bot
        self.payment_id = payment_id

    async def on_submit(self, interaction: discord.Interaction):
        db = self.bot.db
        await db.execute(
            "INSERT INTO payment_submissions (payment_id, user_id, screenshot_url) VALUES (?, ?, ?)",
            (self.payment_id, interaction.user.id, self.image_url.value)
        )
        await db.execute("UPDATE payments SET status = 'waiting_approval' WHERE payment_id = ?", (self.payment_id,))

        pay = await db.fetchone("SELECT * FROM payments WHERE payment_id = ?", (self.payment_id,))

        # Send to PAYMENT_LOG_CHANNEL_ID
        log_chan_id = os.getenv("PAYMENT_LOG_CHANNEL_ID")
        embed = CoreEmbed.payment(
            f"PAYMENT VERIFICATION REQUIRED: {self.payment_id}",
            f"**Customer:** {interaction.user.mention} ({interaction.user.id})\n"
            f"**Amount:** {format_currency(pay['amount']) if pay else 'N/A'}\n"
            f"**Payment ID:** `{self.payment_id}`\n"
            f"**Transaction Ref:** {self.transaction_ref.value}\n"
            f"**Screenshot Link:** [View Attachment]({self.image_url.value})"
        )
        embed.set_image(url=self.image_url.value)

        await log_to_channel(self.bot, log_chan_id, embed)
        log_channel = self.bot.get_channel(int(log_chan_id)) if log_chan_id else None
        if log_channel:
            await log_channel.send(view=PaymentApprovalView(self.bot, self.payment_id))

        await interaction.response.send_message("Screenshot submitted! Staff will review your payment shortly.", ephemeral=True)

class PaymentMethodSelectView(discord.ui.View):
    def __init__(self, bot, payment_id: str, amount: float, target_user: discord.User):
        super().__init__(timeout=300)
        self.bot = bot
        self.payment_id = payment_id
        self.amount = amount
        self.target_user = target_user

    @discord.ui.select(
        placeholder="Select your preferred Payment Method...",
        options=[
            discord.SelectOption(label="Google Pay", value="Google Pay", emoji="💳"),
            discord.SelectOption(label="PhonePe", value="PhonePe", emoji="📱"),
            discord.SelectOption(label="Paytm", value="Paytm", emoji="💰"),
            discord.SelectOption(label="PayPal", value="PayPal", emoji="🌐"),
            discord.SelectOption(label="UPI", value="UPI", emoji="⚡"),
            discord.SelectOption(label="QR Code", value="QR", emoji="📷"),
            discord.SelectOption(label="Bank Transfer", value="Bank Transfer", emoji="🏦"),
        ]
    )
    async def select_method(self, interaction: discord.Interaction, select: discord.ui.Select):
        method = select.values[0]
        db = self.bot.db
        await db.execute("UPDATE payments SET method = ? WHERE payment_id = ?", (method, self.payment_id))

        embed = CoreEmbed.payment(
            f"Payment Request: {self.payment_id}",
            f"**Selected Method:** {method}\n"
            f"**Amount Due:** {format_currency(self.amount)}\n\n"
            f"Please complete payment using instructions below and submit screenshot proof."
        )

        qr_rec = await db.fetchone("SELECT image_path_or_url FROM qr_config WHERE id = 1")
        if method == "QR" and qr_rec:
            embed.set_image(url=qr_rec["image_path_or_url"])

        view = discord.ui.View()
        submit_btn = discord.ui.Button(label="Submit Payment Screenshot", style=discord.ButtonStyle.success, emoji="📥")

        async def submit_callback(sub_interaction: discord.Interaction):
            await sub_interaction.response.send_modal(SubmitScreenshotModal(self.bot, self.payment_id))

        submit_btn.callback = submit_callback
        view.add_item(submit_btn)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class PaymentsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pay", description="Initiate a payment request")
    async def pay(self, interaction: discord.Interaction, user: discord.User, amount: float):
        if amount <= 0:
            await interaction.response.send_message("Amount must be greater than 0.", ephemeral=True)
            return

        payment_id = generate_payment_id()
        await self.bot.db.execute(
            "INSERT INTO payments (payment_id, user_id, amount, original_amount, target_user_id) VALUES (?, ?, ?, ?, ?)",
            (payment_id, interaction.user.id, amount, amount, user.id)
        )

        embed = CoreEmbed.payment(
            "Payment Invoice Created",
            f"**Invoice ID:** `{payment_id}`\n"
            f"**Recipient:** {user.mention}\n"
            f"**Total Amount:** {format_currency(amount)}\n\n"
            "Select a payment method below to proceed."
        )

        view = PaymentMethodSelectView(self.bot, payment_id, amount, user)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PaymentsCog(bot))
  
