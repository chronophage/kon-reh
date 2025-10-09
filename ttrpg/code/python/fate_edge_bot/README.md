You're right! We need to update `main.py` to load all the managers and command modules. Let me create the updated version:

```python
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

class FateEdgeBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.synced = False
        
        # Initialize managers
        from bot.managers.character_manager import CharacterManager
        from bot.managers.dice_manager import DiceManager
        from bot.managers.resource_manager import ResourceManager
        from bot.managers.combat_manager import CombatManager
        from bot.managers.magic_manager import MagicManager
        from bot.managers.travel_manager import TravelManager
        from bot.managers.deck_manager import DeckManager
        
        self.character_manager = CharacterManager()
        self.dice_manager = DiceManager()
        self.resource_manager = ResourceManager()
        self.combat_manager = CombatManager()
        self.magic_manager = MagicManager()
        self.travel_manager = TravelManager()
        self.deck_manager = DeckManager()
        
    async def setup_hook(self):
        # Load command modules
        await self.load_extension('bot.commands.core_commands')
        await self.load_extension('bot.commands.character_commands')
        await self.load_extension('bot.commands.combat_commands')
        await self.load_extension('bot.commands.magic_commands')
        await self.load_extension('bot.commands.travel_commands')
        await self.load_extension('bot.commands.deck_commands')
        await self.load_extension('bot.commands.resource_commands')
        await self.load_extension('bot.commands.session_commands')
        
        # Sync commands with Discord
        if not self.synced:
            await self.tree.sync()
            self.synced = True
            logger.info("Commands synced!")
            
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        await self.change_presence(activity=discord.Game(name="Fate's Edge"))

# Initialize bot
bot = FateEdgeBot()

# Error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message("Command not found!", ephemeral=True)
    else:
        logger.error(f"Error in command {interaction.command}: {error}")
        try:
            await interaction.response.send_message("An error occurred while executing this command.", ephemeral=True)
        except:
            pass

if __name__ == "__main__":
    # Load token from environment variable
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        exit(1)
        
    bot.run(token)
```

And we need to create a `.env` template file:

```env
# .env
DISCORD_TOKEN=your_bot_token_here
```

We should also create a simple README.md to document the bot:

```markdown
# Fate's Edge Discord Bot

A Discord bot to facilitate playing Fate's Edge RPG directly in Discord.

## Setup

1. Create a Discord bot application at https://discord.com/developers/applications
2. Copy your bot token
3. Rename `.env.example` to `.env` and add your token:
   ```
   DISCORD_TOKEN=your_actual_bot_token_here
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the bot:
   ```
   python main.py
   ```

## Features

- **Character Management**: Create and manage Fate's Edge characters
- **Dice Rolling**: Full Fate's Edge dice mechanics with description ladder
- **Combat System**: Position, range, harm, and tactical clock tracking
- **Magic System**: Obligation, fatigue, and summoning management
- **Travel System**: Journey tracking with supply and waypoint management
- **Deck Integration**: Travel decks, consequences, and NPC generation
- **Resource Tracking**: Supply, story beats, and party conditions
- **Session Management**: Event logging and XP tracking

## Commands

Use `/` in Discord to see all available commands.

## License

This bot is designed for use with Fate's Edge RPG. See the Fate's Edge SRD for license information.
```

And finally, let's create a proper `.env.example` file:

```env
# .env.example
# Rename this file to .env and add your actual Discord bot token
DISCORD_TOKEN=your_discord_bot_token_here
