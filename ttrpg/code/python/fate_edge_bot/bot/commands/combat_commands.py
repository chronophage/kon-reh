import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class CombatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def _get_combat_manager(self):
        """Helper to get combat manager from bot"""
        return self.bot.combat_manager
        
    def _get_character_manager(self):
        """Helper to get character manager from bot"""
        return self.bot.character_manager
        
    @app_commands.command(name="combat_start", description="Start a new combat session")
    @app_commands.describe(scene_name="Name of the combat scene")
    async def combat_start(self, interaction: discord.Interaction, scene_name: str = "Combat"):
        """Start a new combat session"""
        try:
            combat_manager = self._get_combat_manager()
            result = combat_manager.start_combat(scene_name)
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"⚔️ **Combat Started**: {scene_name}\n"
                    f"Round: {result['round']}\n"
                    f"Use `/combat_add` to add participants!"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_start: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while starting combat.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_end", description="End the current combat session")
    async def combat_end(self, interaction: discord.Interaction):
        """End the current combat session"""
        try:
            combat_manager = self._get_combat_manager()
            result = combat_manager.end_combat()
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"⚔️ **Combat Ended**: {result['scene_name']}\n"
                    f"Rounds completed: {result['rounds']}"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_end: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while ending combat.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_add", description="Add a participant to combat")
    @app_commands.describe(
        name="Participant name",
        is_character="Is this a player character? (true/false)",
        position="Starting position (Dominant/Controlled/Desperate)",
        range_band="Starting range (Close/Near/Far/Absent)"
    )
    @app_commands.choices(
        position=[
            app_commands.Choice(name="Controlled", value="Controlled"),
            app_commands.Choice(name="Controlled", value="Controlled"),
            app_commands.Choice(name="Desperate", value="Desperate")
        ],
        range_band=[
            app_commands.Choice(name="Close", value="Close"),
            app_commands.Choice(name="Near", value="Near"),
            app_commands.Choice(name="Far", value="Far"),
            app_commands.Choice(name="Absent", value="Absent")
        ]
    )
    async def combat_add(self, interaction: discord.Interaction, name: str, 
                        is_character: bool = True,
                        position: app_commands.Choice[str] = "Controlled",
                        range_band: app_commands.Choice[str] = "Near"):
        """Add a participant to combat"""
        try:
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session. Use `/combat_start` first!", 
                    ephemeral=True
                )
                return
                
            pos_value = position.value if hasattr(position, 'value') else position
            range_value = range_band.value if hasattr(range_band, 'value') else range_band
            
            result = combat_manager.add_participant(
                name=name,
                is_character=is_character,
                position=pos_value,
                range_band=range_value
            )
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"✅ Added **{name}** to combat\n"
                    f"Position: {pos_value} | Range: {range_value}"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_add: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while adding participant.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_remove", description="Remove a participant from combat")
    @app_commands.describe(name="Participant name to remove")
    async def combat_remove(self, interaction: discord.Interaction, name: str):
        """Remove a participant from combat"""
        try:
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            result = combat_manager.remove_participant(name)
            
            if result["status"] == "success":
                await interaction.response.send_message(f"✅ {result['message']}")
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_remove: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while removing participant.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_status", description="Show current combat status")
    async def combat_status(self, interaction: discord.Interaction):
        """Show current combat status"""
        try:
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            status = combat_manager.get_combat_status()
            
            if status["status"] == "success":
                formatted_status = self._format_combat_status(status)
                await interaction.response.send_message(formatted_status)
            else:
                await interaction.response.send_message(
                    f"❌ {status['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_status: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving combat status.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_position", description="Set a participant's position")
    @app_commands.describe(
        participant_name="Participant name",
        position="New position state"
    )
    @app_commands.choices(position=[
        app_commands.Choice(name="Controlled", value="Controlled"),
        app_commands.Choice(name="Controlled", value="Controlled"),
        app_commands.Choice(name="Desperate", value="Desperate")
    ])
    async def combat_position(self, interaction: discord.Interaction, participant_name: str,
                             position: app_commands.Choice[str]):
        """Set a participant's position state"""
        try:
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            pos_value = position.value if hasattr(position, 'value') else position
            result = combat_manager.set_position(participant_name, pos_value)
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"✅ {result['message']}\n"
                    f"Effect: {result['effects']}"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_position: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while setting position.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_range", description="Set a participant's range band")
    @app_commands.describe(
        participant_name="Participant name",
        range_band="New range band"
    )
    @app_commands.choices(range_band=[
        app_commands.Choice(name="Close", value="Close"),
        app_commands.Choice(name="Near", value="Near"),
        app_commands.Choice(name="Far", value="Far"),
        app_commands.Choice(name="Absent", value="Absent")
    ])
    async def combat_range(self, interaction: discord.Interaction, participant_name: str,
                          range_band: app_commands.Choice[str]):
        """Set a participant's range band"""
        try:
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            range_value = range_band.value if hasattr(range_band, 'value') else range_band
            result = combat_manager.set_range(participant_name, range_value)
            
            if result["status"] == "success":
                await interaction.response.send_message(f"✅ {result['message']}")
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_range: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while setting range.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_move", description="Move a participant's range")
    @app_commands.describe(
        participant_name="Participant name",
        direction="Direction to move"
    )
    @app_commands.choices(direction=[
        app_commands.Choice(name="Closer", value="closer"),
        app_commands.Choice(name="Farther", value="farther")
    ])
    async def combat_move(self, interaction: discord.Interaction, participant_name: str,
                         direction: app_commands.Choice[str]):
        """Move a participant one range band closer or farther"""
        try:
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            dir_value = direction.value if hasattr(direction, 'value') else direction
            result = combat_manager.move_participant(participant_name, dir_value)
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"✅ {result['message']}\n"
                    f"Moved from {result['from']} to {result['to']}"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_move: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while moving participant.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_harm", description="Set harm level for a participant")
    @app_commands.describe(
        participant_name="Participant name",
        level="Harm level (0-3)"
    )
    async def combat_harm(self, interaction: discord.Interaction, participant_name: str, level: int):
        """Set harm level for a participant"""
        try:
            if level < 0 or level > 3:
                await interaction.response.send_message(
                    "❌ Harm level must be between 0 and 3", 
                    ephemeral=True
                )
                return
                
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            result = combat_manager.set_harm(participant_name, level)
            
            if result["status"] == "success":
                harm_effects = {
                    0: "No effect",
                    1: "-1 die to related actions",
                    2: "-1 die to most actions",
                    3: "Incapacitated or dying"
                }
                
                await interaction.response.send_message(
                    f"✅ Set harm for **{participant_name}** to level **{level}**\n"
                    f"Effect: {harm_effects.get(level, 'Unknown')}"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_harm: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while setting harm.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_fatigue", description="Add fatigue to a participant")
    @app_commands.describe(
        participant_name="Participant name",
        amount="Amount of fatigue to add (default: 1)"
    )
    async def combat_fatigue(self, interaction: discord.Interaction, participant_name: str, amount: int = 1):
        """Add fatigue to a participant"""
        try:
            if amount <= 0:
                await interaction.response.send_message(
                    "❌ Fatigue amount must be positive", 
                    ephemeral=True
                )
                return
                
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            result = combat_manager.add_fatigue(participant_name, amount)
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"✅ Added **{amount}** fatigue to **{participant_name}**\n"
                    f"Total fatigue: {result['value']}"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_fatigue: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while adding fatigue.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_clock", description="Manage tactical clocks")
    @app_commands.describe(
        action="Action to perform",
        clock_name="Clock name",
        segments="Number of segments to advance/clear (default: 1)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Advance", value="advance"),
        app_commands.Choice(name="Clear", value="clear")
    ])
    async def combat_clock(self, interaction: discord.Interaction, action: app_commands.Choice[str],
                          clock_name: str, segments: int = 1):
        """Manage tactical clocks"""
        try:
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            action_value = action.value if hasattr(action, 'value') else action
            result = None
            
            if action_value == "add":
                result = combat_manager.add_tactical_clock(clock_name, segments)
            elif action_value == "advance":
                result = combat_manager.advance_clock(clock_name, segments)
            elif action_value == "clear":
                result = combat_manager.clear_clock(clock_name, segments)
                
            if result and result["status"] == "success":
                if action_value == "add":
                    await interaction.response.send_message(f"✅ {result['message']}")
                else:
                    progress_bar = result.get('progress_bar', '')
                    completed = result.get('completed', False)
                    
                    message = f"✅ {result['message']}\n{progress_bar}"
                    if completed:
                        message += "\n🔔 **Clock completed!**"
                        
                    await interaction.response.send_message(message)
            elif result:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "❌ Invalid action specified", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_clock: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing combat clock.", 
                ephemeral=True
            )
            
    @app_commands.command(name="combat_next", description="Advance to next turn")
    async def combat_next(self, interaction: discord.Interaction):
        """Advance to next turn"""
        try:
            combat_manager = self._get_combat_manager()
            
            if not combat_manager.is_active():
                await interaction.response.send_message(
                    "❌ No active combat session!", 
                    ephemeral=True
                )
                return
                
            result = combat_manager.next_turn()
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"✅ {result['message']}\n"
                    f"Current participant: **{result['current_participant']}**"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in combat_next: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while advancing turn.", 
                ephemeral=True
            )
            
    # Helper methods
    def _format_combat_status(self, status_data: dict) -> str:
        """Format combat status for Discord display"""
        journey = status_data["journey"]
        participants = status_data["participants"]
        clocks = status_data["active_clocks"]
        
        result = f"⚔️ **{journey['scene_name']}**\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**Round**: {journey['round']} | **Turn**: {journey['turn_status']['turn']}\n"
        result += f"**Current**: {journey['turn_status']['current_participant']}\n\n"
        
        if participants:
            result += "**Participants:**\n"
            for name, participant in participants.items():
                pos_icon = {"Controlled": "🛡️", "Controlled": "⚔️", "Desperate": "⚠️"}.get(participant['position'], "❓")
                range_icon = {"Close": " melee", "Near": " near", "Far": " far", "Absent": " absent"}.get(participant['range_band'], "")
                
                harm = participant['conditions'].get('harm', 0)
                fatigue = participant['conditions'].get('fatigue', 0)
                harm_str = f"💔{harm} " if harm > 0 else ""
                fatigue_str = f"😴{fatigue} " if fatigue > 0 else ""
                
                result += f"• {pos_icon} **{name}**{range_icon} {harm_str}{fatigue_str}\n"
            result += "\n"
            
        if clocks:
            result += "**Active Clocks:**\n"
            for name, clock in clocks.items():
                progress_bar = self._get_combat_manager()._create_progress_bar(
                    clock['current'], clock['size']
                )
                result += f"• {name}: {progress_bar}\n"
                
        return result

async def setup(bot: commands.Bot):
    """Cog setup function"""
    await bot.add_cog(CombatCommands(bot))

