import discord
from discord import app_commands
from discord.ext import commands

class CoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="ping", description="Check if the bot is responding")
    async def ping(self, interaction: discord.Interaction):
        """Simple ping command to check bot responsiveness"""
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(
            f"🏓 Pong! Latency: {latency}ms", 
            ephemeral=True
        )
        
    @app_commands.command(name="help", description="Show help information for Fate's Edge Bot")
    async def help(self, interaction: discord.Interaction):
        """Display help information"""
        help_text = """
🤖 **Fate's Edge Discord Bot Help**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Core Commands:**
• `/ping` - Check bot responsiveness
• `/help` - Show this help message

**Character Management:**
• `/character create` - Create a new character
• `/character show` - Display character sheet
• `/character list` - List all characters

**Dice Rolling:**
• `/roll` - Roll a dice pool with modifiers

**Resource Tracking:**
• `/supply status` - Check party supply status
• `/supply advance` - Advance supply timer
• `/supply clear` - Clear supply timer

**Coming Soon:**
• Combat tracking
• Magic system
• Travel system
• Deck integration

*Use `/` to see all available commands!*
        """
        
        await interaction.response.send_message(help_text, ephemeral=True)
        
    @app_commands.command(name="info", description="Show information about the bot")
    async def info(self, interaction: discord.Interaction):
        """Display bot information"""
        info_text = """
📜 **Fate's Edge Companion Bot**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A helper bot for playing Fate's Edge RPG on Discord.

**Features:**
• Character management
• Dice rolling with Fate's Edge mechanics
• Resource tracking (Supply, Harm, Fatigue)
• Combat assistance
• Magic system support
• Travel system integration
• Deck drawing simulation

**Version:** 1.0.0
**Developer:** Community Project
**Based on:** Fate's Edge RPG System

For more information, visit the Fate's Edge SRD.
        """
        
        await interaction.response.send_message(info_text, ephemeral=True)

async def setup(bot: commands.Bot):
    """Cog setup function"""
    await bot.add_cog(CoreCommands(bot))

