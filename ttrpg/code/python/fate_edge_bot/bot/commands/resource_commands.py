import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class ResourceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def _get_resource_manager(self):
        """Helper to get resource manager from bot"""
        return self.bot.resource_manager
        
    @app_commands.command(name="supply_status", description="Show party supply status")
    async def supply_status(self, interaction: discord.Interaction):
        """Show current party supply status"""
        try:
            resource_manager = self._get_resource_manager()
            status = resource_manager.get_supply_status()
            
            progress_bar = status.get('progress_bar', '')
            supply_info = status.get('status', {})
            
            await interaction.response.send_message(
                f"🏕️ **Party Supply Status**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{progress_bar}\n"
                f"**Status**: {supply_info.get('name', 'Unknown')}\n"
                f"**Effect**: {supply_info.get('effect', 'Unknown')}"
            )
            
        except Exception as e:
            logger.error(f"Error in supply_status: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving supply status.", 
                ephemeral=True
            )
            
    @app_commands.command(name="supply_advance", description="Advance supply clock")
    @app_commands.describe(reason="Reason for advancing supply clock")
    async def supply_advance(self, interaction: discord.Interaction, reason: str = "General depletion"):
        """Advance the party supply clock"""
        try:
            resource_manager = self._get_resource_manager()
            result = resource_manager.advance_supply_clock(reason)
            
            progress_bar = result.get('progress_bar', '')
            supply_info = result.get('status', {})
            changed = result.get('changed', False)
            warning = result.get('warning', '')
            
            message = f"⚠️ **Supply Clock Advanced**\n"
            message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            message += f"{progress_bar}\n"
            message += f"**Status**: {supply_info.get('name', 'Unknown')}\n"
            message += f"**Reason**: {reason}\n"
            
            if warning:
                message += f"\n🚨 **{warning}**"
                
            if changed:
                await interaction.response.send_message(message)
            else:
                await interaction.response.send_message(
                    f"{message}\n\n🔔 Supply clock is already at maximum!", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in supply_advance: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while advancing supply clock.", 
                ephemeral=True
            )
            
    @app_commands.command(name="supply_clear", description="Clear segments from supply clock")
    @app_commands.describe(segments="Number of segments to clear (default: 1)")
    async def supply_clear(self, interaction: discord.Interaction, segments: int = 1):
        """Clear segments from the party supply clock"""
        try:
            if segments <= 0:
                await interaction.response.send_message(
                    "❌ Segments must be positive", 
                    ephemeral=True
                )
                return
                
            resource_manager = self._get_resource_manager()
            result = resource_manager.clear_supply_clock(segments)
            
            new_status = result.get('status', {})
            progress_bar = new_status.get('progress_bar', '')
            supply_info = new_status.get('status', {})
            
            await interaction.response.send_message(
                f"✨ **Supply Clock Cleared**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"**Cleared**: {segments} segment(s)\n"
                f"**Previous**: {result.get('previous', 0)}\n"
                f"**Current**: {result.get('current', 0)}\n"
                f"{progress_bar}\n"
                f"**Status**: {supply_info.get('name', 'Unknown')}"
            )
            
        except Exception as e:
            logger.error(f"Error in supply_clear: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while clearing supply clock.", 
                ephemeral=True
            )
            
    @app_commands.command(name="supply_reset", description="Reset supply clock to full")
    async def supply_reset(self, interaction: discord.Interaction):
        """Reset the party supply clock to full"""
        try:
            resource_manager = self._get_resource_manager()
            result = resource_manager.reset_supply_clock()
            
            new_status = result.get('status', {})
            progress_bar = new_status.get('progress_bar', '')
            supply_info = new_status.get('status', {})
            
            await interaction.response.send_message(
                f"✅ **Supply Clock Reset**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{progress_bar}\n"
                f"**Status**: {supply_info.get('name', 'Unknown')}\n"
                f"**Effect**: {supply_info.get('effect', 'Unknown')}"
            )
            
        except Exception as e:
            logger.error(f"Error in supply_reset: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while resetting supply clock.", 
                ephemeral=True
            )
            
    @app_commands.command(name="story_beats", description="Manage party story beat budget")
    @app_commands.describe(
        action="Action to perform",
        amount="Amount to add/spend (default: 1)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Spend", value="spend"),
        app_commands.Choice(name="Status", value="status")
    ])
    async def story_beats(self, interaction: discord.Interaction, 
                         action: app_commands.Choice[str],
                         amount: int = 1):
        """Manage party story beat budget"""
        try:
            resource_manager = self._get_resource_manager()
            action_value = action.value if hasattr(action, 'value') else action
            
            if action_value == "status":
                budget = resource_manager.get_story_beat_budget()
                await interaction.response.send_message(
                    f"🌀 **Story Beat Budget**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Available**: {budget} Story Beats\n"
                    f"Use these for complications, twists, and narrative tension!"
                )
                return
                
            if amount <= 0:
                await interaction.response.send_message(
                    "❌ Amount must be positive", 
                    ephemeral=True
                )
                return
                
            if action_value == "add":
                new_budget = resource_manager.add_story_beats(amount)
                await interaction.response.send_message(
                    f"🌀 **Story Beats Added**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Added**: {amount}\n"
                    f"**Total Available**: {new_budget}"
                )
                
            elif action_value == "spend":
                success = resource_manager.spend_story_beats(amount)
                current_budget = resource_manager.get_story_beat_budget()
                
                if success:
                    await interaction.response.send_message(
                        f"🌀 **Story Beats Spent**\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"**Spent**: {amount}\n"
                        f"**Remaining**: {current_budget}"
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ **Insufficient Story Beats**\n"
                        f"**Requested**: {amount}\n"
                        f"**Available**: {current_budget}",
                        ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    "❌ Invalid action specified", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in story_beats: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing story beats.", 
                ephemeral=True
            )
            
    @app_commands.command(name="clock_manage", description="Manage tactical clocks")
    @app_commands.describe(
        action="Action to perform",
        clock_name="Name of the clock",
        segments="Number of segments to advance/clear (default: 1)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Advance", value="advance"),
        app_commands.Choice(name="Clear", value="clear"),
        app_commands.Choice(name="Status", value="status"),
        app_commands.Choice(name="Create", value="create"),
        app_commands.Choice(name="Remove", value="remove")
    ])
    async def clock_manage(self, interaction: discord.Interaction, 
                          action: app_commands.Choice[str],
                          clock_name: str = None,
                          segments: int = 1):
        """Manage tactical clocks"""
        try:
            resource_manager = self._get_resource_manager()
            action_value = action.value if hasattr(action, 'value') else action
            
            # Validate clock name for actions that need it
            if action_value in ["advance", "clear", "remove"] and not clock_name:
                await interaction.response.send_message(
                    "❌ Clock name required for this action", 
                    ephemeral=True
                )
                return
                
            # Validate segments for advance/clear actions
            if action_value in ["advance", "clear"] and segments <= 0:
                await interaction.response.send_message(
                    "❌ Segments must be positive", 
                    ephemeral=True
                )
                return
                
            result = None
            if action_value == "advance":
                result = resource_manager.advance_tactical_clock(clock_name, segments)
            elif action_value == "clear":
                result = resource_manager.clear_tactical_clock(clock_name, segments)
            elif action_value == "status":
                clocks = resource_manager.get_tactical_clocks()
                if clocks:
                    message = "⏱️ **Active Tactical Clocks**\n"
                    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    for name, clock in clocks.items():
                        if clock["current"] > 0:  # Only show active clocks
                            progress_bar = resource_manager._create_progress_bar(
                                clock["current"], clock["size"]
                            )
                            message += f"• **{name}**: {progress_bar}\n"
                    if not any(clock["current"] > 0 for clock in clocks.values()):
                        message += "No active clocks at the moment."
                    await interaction.response.send_message(message)
                else:
                    await interaction.response.send_message(
                        "⏱️ No tactical clocks currently active."
                    )
                return
            elif action_value == "create":
                if not clock_name:
                    await interaction.response.send_message(
                        "❌ Clock name required to create a clock", 
                        ephemeral=True
                    )
                    return
                if segments < 2:
                    segments = 6  # Default size
                result = resource_manager.create_custom_clock(clock_name, segments)
                if result:
                    await interaction.response.send_message(
                        f"⏱️ **Clock Created**\n"
                        f"**Name**: {clock_name}\n"
                        f"**Size**: {segments}-segment"
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Failed to create clock '{clock_name}'", 
                        ephemeral=True
                    )
                return
            elif action_value == "remove":
                result = resource_manager.remove_custom_clock(clock_name)
                if result:
                    await interaction.response.send_message(
                        f"⏱️ **Clock Removed**\n"
                        f"**Name**: {clock_name}"
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Failed to remove clock '{clock_name}'", 
                        ephemeral=True
                    )
                return
                
            if result and "error" in result:
                await interaction.response.send_message(
                    f"❌ {result['error']}", 
                    ephemeral=True
                )
            elif result:
                progress_bar = result.get('progress_bar', '')
                completed = result.get('completed', False)
                
                if action_value == "advance":
                    message = f"⏱️ **Clock Advanced**\n"
                    message += f"**Clock**: {result['name']}\n"
                    message += f"{progress_bar}\n"
                    message += f"**Segments Advanced**: {result['segments_advanced']}"
                    
                    if completed:
                        message += f"\n\n🔔 **{result['name']} has reached completion!**"
                        
                elif action_value == "clear":
                    message = f"⏱️ **Clock Cleared**\n"
                    message += f"**Clock**: {result['name']}\n"
                    message += f"{progress_bar}\n"
                    message += f"**Segments Cleared**: {result['segments_cleared']}"
                    
                await interaction.response.send_message(message)
            else:
                await interaction.response.send_message(
                    "❌ Invalid action specified", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in clock_manage: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing clocks.", 
                ephemeral=True
            )
            
    @app_commands.command(name="resource_status", description="Show overall party resource status")
    async def resource_status(self, interaction: discord.Interaction):
        """Show overall party resource status"""
        try:
            resource_manager = self._get_resource_manager()
            status = resource_manager.get_party_status()
            
            supply_status = status.get('supply', {})
            supply_progress = supply_status.get('progress_bar', '')
            supply_info = supply_status.get('status', {})
            
            sb_budget = status.get('story_beat_budget', 0)
            active_clocks = status.get('active_clocks', {})
            conditions = status.get('character_conditions', {})
            
            message = "📊 **Party Resource Status**\n"
            message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Supply
            message += f"**🏕️ Supply Status**\n"
            message += f"{supply_progress}\n"
            message += f"Status: {supply_info.get('name', 'Unknown')}\n\n"
            
            # Story Beats
            message += f"**🌀 Story Beats**\n"
            message += f"Available: {sb_budget}\n\n"
            
            # Active Clocks
            if active_clocks:
                message += f"**⏱️ Active Clocks**\n"
                for name, clock in active_clocks.items():
                    progress_bar = resource_manager._create_progress_bar(
                        clock['current'], clock['size']
                    )
                    message += f"• {name}: {progress_bar}\n"
                message += "\n"
                
            # Character Conditions
            if conditions:
                message += f"**👥 Character Conditions**\n"
                for char_name, char_conditions in conditions.items():
                    harm = char_conditions.get('harm', 0)
                    fatigue = char_conditions.get('fatigue', 0)
                    boons = char_conditions.get('boons', 0)
                    
                    harm_str = f"💔{harm} " if harm > 0 else ""
                    fatigue_str = f"😴{fatigue} " if fatigue > 0 else ""
                    boons_str = f"✨{boons} " if boons > 0 else ""
                    
                    message += f"• **{char_name}**: {harm_str}{fatigue_str}{boons_str}\n"
                    
            await interaction.response.send_message(message)
            
        except Exception as e:
            logger.error(f"Error in resource_status: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving resource status.", 
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    """Cog setup function"""
    await bot.add_cog(ResourceCommands(bot))

