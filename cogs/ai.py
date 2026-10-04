import os
import discord
from discord.ext import commands
from discord import app_commands
from integrations.ollama_ai import OllamaAI
from utils.embeds import CoreEmbed

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai = OllamaAI()

    @app_commands.command(name="ai", description="Ask local Ollama AI host any question")
    async def ai_command(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        response = await self.ai.generate_response(prompt)
        embed = CoreEmbed.base("🧠 INFINITE CORE AI", f"**Prompt:** {prompt}\n\n**Response:**\n{response}")
        await interaction.followup.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            clean_content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not clean_content:
                clean_content = "Hello!"
            
            async with message.channel.typing():
                response = await self.ai.generate_response(clean_content)
                await message.reply(response)

async def setup(bot):
    await bot.add_cog(AICog(bot))
  
