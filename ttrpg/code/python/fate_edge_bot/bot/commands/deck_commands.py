import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class DeckCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def _get_deck_manager(self):
        """Helper to get deck manager from bot"""
        return self.bot.deck_manager
        
    @app_commands.command(name="deck_travel", description="Draw cards from a travel deck")
    @app_commands.describe(
        region="Travel region",
        draw_type="Type of draw",
        suit="Specific suit to draw (for single card draw)"
    )
    @app_commands.choices(
        draw_type=[
            app_commands.Choice(name="Quick Hook (2 cards)", value="quick_hook"),
            app_commands.Choice(name="Full Seed (4 cards)", value="full_seed"),
            app_commands.Choice(name="Single Card", value="single")
        ],
        suit=[
            app_commands.Choice(name="Spade ♠", value="spade"),
            app_commands.Choice(name="Heart ♥", value="heart"),
            app_commands.Choice(name="Club ♣", value="club"),
            app_commands.Choice(name="Diamond ♦", value="diamond")
        ]
    )
    async def deck_travel(self, interaction: discord.Interaction, 
                         region: str,
                         draw_type: app_commands.Choice[str],
                         suit: app_commands.Choice[str] = None):
        """Draw cards from a travel deck"""
        try:
            deck_manager = self._get_deck_manager()
            draw_type_value = draw_type.value if hasattr(draw_type, 'value') else draw_type
            
            if draw_type_value == "quick_hook":
                result = deck_manager.draw_quick_hook(region)
                formatted_result = deck_manager.format_travel_draw(result)
                
            elif draw_type_value == "full_seed":
                result = deck_manager.draw_full_seed(region)
                formatted_result = deck_manager.format_travel_draw(result)
                
            elif draw_type_value == "single":
                if not suit:
                    await interaction.response.send_message(
                        "❌ Suit required for single card draw", 
                        ephemeral=True
                    )
                    return
                    
                suit_value = suit.value if hasattr(suit, 'value') else suit
                result = deck_manager.draw_travel_card(region, suit_value)
                
                if result:
                    # Format as a single card draw
                    formatted_result = f"🃏 **Travel Card Draw** - {region}\n"
                    formatted_result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    suit_symbol = {"spade": "♠", "heart": "♥", "club": "♣", "diamond": "♦"}[suit_value]
                    formatted_result += f"{suit_symbol} **{result['suit']}**: {result['card']}\n"
                    formatted_result += f"**Rank**: {result['rank_name']} | **Clock**: {result['clock_size']}-segment"
                else:
                    await interaction.response.send_message(
                        f"❌ Failed to draw card from {region} {suit_value}", 
                        ephemeral=True
                    )
                    return
            else:
                await interaction.response.send_message(
                    "❌ Invalid draw type specified", 
                    ephemeral=True
                )
                return
                
            if "error" in result:
                await interaction.response.send_message(
                    f"❌ {result['error']}", 
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(formatted_result)
                
        except Exception as e:
            logger.error(f"Error in deck_travel: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while drawing from the travel deck.", 
                ephemeral=True
            )
            
    @app_commands.command(name="deck_consequence", description="Draw from the Deck of Consequences")
    @app_commands.describe(
        severity="Severity of consequences (default: moderate)"
    )
    @app_commands.choices(severity=[
        app_commands.Choice(name="Minor", value="minor"),
        app_commands.Choice(name="Moderate", value="moderate"),
        app_commands.Choice(name="Major", value="major")
    ])
    async def deck_consequence(self, interaction: discord.Interaction,
                              severity: app_commands.Choice[str] = "moderate"):
        """Draw from the Deck of Consequences"""
        try:
            deck_manager = self._get_deck_manager()
            severity_value = severity.value if hasattr(severity, 'value') else severity
            
            result = deck_manager.draw_consequence_card(severity_value)
            formatted_result = deck_manager.format_consequence_draw(result)
            
            await interaction.response.send_message(formatted_result)
            
        except Exception as e:
            logger.error(f"Error in deck_consequence: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while drawing from the consequences deck.", 
                ephemeral=True
            )
            
    @app_commands.command(name="deck_npc", description="Generate a random NPC")
    async def deck_npc(self, interaction: discord.Interaction):
        """Generate a random NPC using the NPC deck"""
        try:
            deck_manager = self._get_deck_manager()
            result = deck_manager.generate_npc()
            formatted_result = deck_manager.format_npc_generation(result)
            
            await interaction.response.send_message(formatted_result)
            
        except Exception as e:
            logger.error(f"Error in deck_npc: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while generating an NPC.", 
                ephemeral=True
            )
            
    @app_commands.command(name="deck_regions", description="List available travel regions")
    async def deck_regions(self, interaction: discord.Interaction):
        """List all available travel regions"""
        try:
            deck_manager = self._get_deck_manager()
            result = deck_manager.list_regions()
            
            if result["status"] == "success":
                message = "🌍 **Available Travel Regions**\n"
                message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                
                for region in result["regions"]:
                    message += f"• **{region['name']}** - {region['theme']}\n"
                    
                message += "\nUse `/deck_travel` with any of these regions!"
                
                await interaction.response.send_message(message)
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in deck_regions: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while listing regions.", 
                ephemeral=True
            )
            
    @app_commands.command(name="deck_info", description="Get information about a specific region")
    @app_commands.describe(region="Name of the region")
    async def deck_info(self, interaction: discord.Interaction, region: str):
        """Get information about a specific travel region"""
        try:
            deck_manager = self._get_deck_manager()
            result = deck_manager.get_region_info(region)
            
            if result:
                suits = result['suits']
                await interaction.response.send_message(
                    f"🌍 **{region}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Theme**: {result['theme']}\n\n"
                    f"**Deck Contents**:\n"
                    f"• ♠ Spades: {suits['spades']} cards\n"
                    f"• ♥ Hearts: {suits['hearts']} cards\n"
                    f"• ♣ Clubs: {suits['clubs']} cards\n"
                    f"• ♦ Diamonds: {suits['diamonds']} cards\n\n"
                    f"Use `/deck_travel` to draw cards from this region!"
                )
            else:
                # List available regions
                regions_result = deck_manager.list_regions()
                if regions_result["status"] == "success":
                    region_list = ", ".join([r['name'] for r in regions_result["regions"]])
                    await interaction.response.send_message(
                        f"❌ Region '{region}' not found.\n"
                        f"**Available Regions**: {region_list}",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Region '{region}' not found.",
                        ephemeral=True
                    )
                    
        except Exception as e:
            logger.error(f"Error in deck_info: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving region information.", 
                ephemeral=True
            )
            
    @app_commands.command(name="deck_example", description="Show examples of deck draws")
    async def deck_example(self, interaction: discord.Interaction):
        """Show examples of different deck draws"""
        try:
            examples = (
                "📘 **Deck Draw Examples**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                
                "🔹 **Travel - Quick Hook**\n"
                "`/deck_travel region:Acasia draw_type:Quick Hook`\n"
                "Draws 1 Spade + 1 Heart for a quick scene seed\n\n"
                
                "🔹 **Travel - Full Seed**\n"
                "`/deck_travel region:Valewood draw_type:Full Seed`\n"
                "Draws 1 card of each suit for detailed adventure planning\n\n"
                
                "🔹 **Consequences**\n"
                "`/deck_consequence severity:Major`\n"
                "Draws 3 cards for significant complications\n\n"
                
                "🔹 **NPC Generation**\n"
                "`/deck_npc`\n"
                "Creates a complete NPC profile with ambition/belief/twist\n\n"
                
                "🔹 **Single Card**\n"
                "`/deck_travel region:Mistlands draw_type:Single suit:Heart`\n"
                "Draws one specific card for focused inspiration"
            )
            
            await interaction.response.send_message(examples)
            
        except Exception as e:
            logger.error(f"Error in deck_example: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while showing examples.", 
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    """Cog setup function"""
    await bot.add_cog(DeckCommands(bot))

