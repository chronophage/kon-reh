import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class TravelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def _get_travel_manager(self):
        """Helper to get travel manager from bot"""
        return self.bot.travel_manager
        
    def _get_deck_manager(self):
        """Helper to get deck manager from bot"""
        return self.bot.deck_manager
        
    def _get_resource_manager(self):
        """Helper to get resource manager from bot"""
        return self.bot.resource_manager
        
    @app_commands.command(name="travel_start", description="Start a new journey")
    @app_commands.describe(
        party_name="Name of the traveling party",
        starting_region="Starting region (default: Civilization)"
    )
    async def travel_start(self, interaction: discord.Interaction, 
                          party_name: str, 
                          starting_region: str = "Civilization"):
        """Start a new journey for a party"""
        try:
            travel_manager = self._get_travel_manager()
            result = travel_manager.start_journey(
                party_name=party_name,
                channel_id=str(interaction.channel_id),
                starting_region=starting_region
            )
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"🗺️ **Journey Started**\n"
                    f"**Party**: {party_name}\n"
                    f"**Starting Region**: {starting_region}\n"
                    f"Use `/travel_leg` to add travel legs!"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in travel_start: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while starting the journey.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_leg", description="Add a travel leg to the journey")
    @app_commands.describe(
        destination="Destination of this travel leg",
        clock_size="Size of travel clock (default: 6)"
    )
    async def travel_leg(self, interaction: discord.Interaction, 
                        destination: str, 
                        clock_size: int = 6):
        """Add a travel leg to the current journey"""
        try:
            travel_manager = self._get_travel_manager()
            result = travel_manager.add_travel_leg(
                channel_id=str(interaction.channel_id),
                destination=destination,
                clock_size=clock_size
            )
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"🛣️ **Travel Leg Added**\n"
                    f"**#{result['leg']['leg_number']}**: {destination}\n"
                    f"**Clock Size**: {clock_size}-segment\n"
                    f"Use `/travel_advance` to make progress!"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in travel_leg: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while adding travel leg.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_advance", description="Advance progress on current travel leg")
    @app_commands.describe(
        segments="Number of segments to advance (default: 1)",
        complication="Optional complication description"
    )
    async def travel_advance(self, interaction: discord.Interaction, 
                            segments: int = 1,
                            complication: str = None):
        """Advance progress on the current travel leg"""
        try:
            if segments <= 0:
                await interaction.response.send_message(
                    "❌ Segments must be positive", 
                    ephemeral=True
                )
                return
                
            travel_manager = self._get_travel_manager()
            result = travel_manager.advance_travel_leg(
                channel_id=str(interaction.channel_id),
                segments=segments,
                complication=complication
            )
            
            if result["status"] == "success":
                progress_bar = result.get('progress_bar', '')
                completed = result.get('completed', False)
                
                message = f"🧭 **Travel Progress**\n"
                message += f"**Leg #{result['leg_number']}**: {result['destination']}\n"
                message += f"{progress_bar}\n"
                message += f"Advanced by {segments} segment(s)\n"
                
                if complication:
                    message += f"⚠️ **Complication**: {complication}\n"
                    
                if completed:
                    message += f"\n🏁 **Travel leg completed!**\n"
                    message += f"Use `/travel_leg` to add the next leg or `/travel_end` to end the journey."
                    
                await interaction.response.send_message(message)
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in travel_advance: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while advancing travel.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_status", description="Show current journey status")
    async def travel_status(self, interaction: discord.Interaction):
        """Show current journey status"""
        try:
            travel_manager = self._get_travel_manager()
            result = travel_manager.get_journey_status(str(interaction.channel_id))
            
            if result["status"] == "success":
                formatted_status = travel_manager.format_journey_status(result)
                await interaction.response.send_message(formatted_status)
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in travel_status: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving journey status.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_supply", description="Manage party supply status")
    @app_commands.describe(
        party_name="Name of the traveling party",
        change="Change in supply (-1 to decrease, 1 to increase, 0 to view)"
    )
    async def travel_supply(self, interaction: discord.Interaction, 
                           party_name: str,
                           change: int = 0):
        """Manage party supply status"""
        try:
            travel_manager = self._get_travel_manager()
            
            if change == 0:
                # View current supply
                result = travel_manager.get_party_resources(party_name)
                if result["status"] == "success":
                    supply_level = result["resources"].get("supply_clock", 0)
                    progress_bar = travel_manager._create_progress_bar(supply_level, 4)
                    
                    supply_status = {
                        0: "Full Supply - No penalties",
                        1: "Low Supply - Minor complications",
                        2: "Low Supply - Minor complications", 
                        3: "Dangerously Low - Each character gains Fatigue 1",
                        4: "Out of Supply - Severe penalties, starvation risk"
                    }
                    
                    await interaction.response.send_message(
                        f"🏕️ **{party_name} Supply Status**\n"
                        f"{progress_bar}\n"
                        f"**Status**: {supply_status.get(supply_level, 'Unknown')}"
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ {result['message']}", 
                        ephemeral=True
                    )
            else:
                # Update supply
                result = travel_manager.update_supply(party_name, change)
                if result["status"] == "success":
                    await interaction.response.send_message(
                        f"✅ **Supply Updated**\n"
                        f"**Party**: {party_name}\n"
                        f"{result['progress_bar']}\n"
                        f"**Status**: {result['status_text']}"
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ {result['message']}", 
                        ephemeral=True
                    )
                    
        except Exception as e:
            logger.error(f"Error in travel_supply: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing supply.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_fatigue", description="Manage character travel fatigue")
    @app_commands.describe(
        party_name="Name of the traveling party",
        character_name="Name of the character",
        action="Action to perform",
        amount="Amount of fatigue to add/clear (default: 1)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Clear", value="clear")
    ])
    async def travel_fatigue(self, interaction: discord.Interaction, 
                            party_name: str,
                            character_name: str,
                            action: app_commands.Choice[str],
                            amount: int = 1):
        """Manage character travel fatigue"""
        try:
            travel_manager = self._get_travel_manager()
            action_value = action.value if hasattr(action, 'value') else action
            
            if amount <= 0:
                await interaction.response.send_message(
                    "❌ Amount must be positive", 
                    ephemeral=True
                )
                return
                
            if action_value == "add":
                result = travel_manager.add_party_fatigue(party_name, character_name, amount)
            elif action_value == "clear":
                result = travel_manager.clear_party_fatigue(party_name, character_name, amount)
            else:
                await interaction.response.send_message(
                    "❌ Invalid action specified", 
                    ephemeral=True
                )
                return
                
            if result["status"] == "success":
                if action_value == "add":
                    await interaction.response.send_message(
                        f"😴 **Fatigue Added**\n"
                        f"**Character**: {character_name}\n"
                        f"**Party**: {party_name}\n"
                        f"**Amount**: {amount}\n"
                        f"**Total Fatigue**: {result['fatigue']}\n"
                        f"**Effect**: {result['fatigue_effects']}"
                    )
                elif action_value == "clear":
                    await interaction.response.send_message(
                        f"✨ **Fatigue Cleared**\n"
                        f"**Character**: {character_name}\n"
                        f"**Party**: {party_name}\n"
                        f"**Cleared**: {amount if amount else 'all'}\n"
                        f"**Remaining**: {result['fatigue']}"
                    )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in travel_fatigue: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing fatigue.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_waypoint", description="Add or view waypoints")
    @app_commands.describe(
        party_name="Name of the traveling party",
        waypoint_name="Name of waypoint (to add)",
        description="Description of waypoint (to add)"
    )
    async def travel_waypoint(self, interaction: discord.Interaction, 
                             party_name: str,
                             waypoint_name: str = None,
                             description: str = ""):
        """Add or view waypoints for a party"""
        try:
            travel_manager = self._get_travel_manager()
            
            if waypoint_name:
                # Add waypoint
                result = travel_manager.add_waypoint(party_name, waypoint_name, description)
                if result["status"] == "success":
                    await interaction.response.send_message(
                        f"📍 **Waypoint Added**\n"
                        f"**Party**: {party_name}\n"
                        f"**Waypoint**: {waypoint_name}\n"
                        f"**Description**: {description}"
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ {result['message']}", 
                        ephemeral=True
                    )
            else:
                # View waypoints
                result = travel_manager.get_waypoints(party_name)
                if result["status"] == "success":
                    waypoints = result["waypoints"]
                    if waypoints:
                        message = f"📍 **{party_name}'s Waypoints**\n"
                        message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        for wp in waypoints:
                            message += f"• **{wp['name']}** - {wp['description']}\n"
                        await interaction.response.send_message(message)
                    else:
                        await interaction.response.send_message(
                            f"📍 **{party_name}** has no waypoints recorded."
                        )
                else:
                    await interaction.response.send_message(
                        f"❌ {result['message']}", 
                        ephemeral=True
                    )
                    
        except Exception as e:
            logger.error(f"Error in travel_waypoint: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing waypoints.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_end", description="End the current journey")
    async def travel_end(self, interaction: discord.Interaction):
        """End the current journey"""
        try:
            travel_manager = self._get_travel_manager()
            result = travel_manager.end_journey(str(interaction.channel_id))
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"🏁 **Journey Completed**\n"
                    f"**Party**: {result['party_name']}\n"
                    f"**Legs Completed**: {result['legs_completed']}\n"
                    f"Thanks for traveling with Fate's Edge!"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in travel_end: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while ending the journey.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_complication", description="Draw a travel complication")
    @app_commands.describe(
        severity="Severity of complication (default: moderate)"
    )
    @app_commands.choices(severity=[
        app_commands.Choice(name="Minor", value="minor"),
        app_commands.Choice(name="Moderate", value="moderate"),
        app_commands.Choice(name="Major", value="major")
    ])
    async def travel_complication(self, interaction: discord.Interaction,
                                 severity: app_commands.Choice[str] = "moderate"):
        """Draw a travel complication from the Deck of Consequences"""
        try:
            deck_manager = self._get_deck_manager()
            severity_value = severity.value if hasattr(severity, 'value') else severity
            
            result = deck_manager.draw_consequence_card(severity_value)
            formatted_result = deck_manager.format_consequence_draw(result)
            
            await interaction.response.send_message(
                f"🧭 **Travel Complication** ({severity_value.title()} Severity)\n"
                f"{formatted_result}"
            )
            
        except Exception as e:
            logger.error(f"Error in travel_complication: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while drawing a complication.", 
                ephemeral=True
            )
            
    @app_commands.command(name="travel_region", description="Get information about a travel region")
    @app_commands.describe(region="Name of the region")
    async def travel_region(self, interaction: discord.Interaction, region: str):
        """Get information about a travel region"""
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
            logger.error(f"Error in travel_region: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving region information.", 
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    """Cog setup function"""
    await bot.add_cog(TravelCommands(bot))

