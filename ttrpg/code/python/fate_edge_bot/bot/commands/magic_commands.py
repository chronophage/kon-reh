import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class MagicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def _get_magic_manager(self):
        """Helper to get magic manager from bot"""
        return self.bot.magic_manager
        
    def _get_character_manager(self):
        """Helper to get character manager from bot"""
        return self.bot.character_manager
        
    @app_commands.command(name="magic_obligation", description="Manage character magical obligations")
    @app_commands.describe(
        character_name="Character name",
        action="Action to perform",
        patron="Patron name",
        segments="Number of segments to add/clear (default: 1)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Clear", value="clear"),
        app_commands.Choice(name="Status", value="status")
    ])
    async def magic_obligation(self, interaction: discord.Interaction, 
                              character_name: str,
                              action: app_commands.Choice[str],
                              patron: str = None,
                              segments: int = 1):
        """Manage character magical obligations"""
        try:
            magic_manager = self._get_magic_manager()
            action_value = action.value if hasattr(action, 'value') else action
            
            if action_value == "status":
                # Show obligation status
                result = magic_manager.get_obligation_status(character_name)
                if result["status"] == "success":
                    formatted_status = self._format_obligation_status(result)
                    await interaction.response.send_message(formatted_status, ephemeral=True)
                else:
                    await interaction.response.send_message(
                        f"❌ {result['message']}", 
                        ephemeral=True
                    )
                return
                
            # Validate patron for add/clear actions
            if not patron:
                await interaction.response.send_message(
                    "❌ Patron name required for add/clear actions", 
                    ephemeral=True
                )
                return
                
            if action_value == "add":
                result = magic_manager.add_obligation(character_name, patron, segments)
            elif action_value == "clear":
                result = magic_manager.clear_obligation(character_name, patron, segments)
            else:
                await interaction.response.send_message(
                    "❌ Invalid action specified", 
                    ephemeral=True
                )
                return
                
            if result["status"] == "success":
                if action_value == "add":
                    capacity_exceeded = result.get("capacity_exceeded", False)
                    fatigue = result.get("fatigue", 0)
                    
                    message = f"✅ Added {segments} obligation segment(s) to {character_name} for {patron}\n"
                    message += f"Total: {result['total_segments']} for this patron\n"
                    
                    if capacity_exceeded:
                        message += f"⚠️ **Capacity exceeded!** Fatigue: {fatigue}\n"
                        
                elif action_value == "clear":
                    message = f"✅ Cleared {result['segments_cleared']} obligation segment(s) for {patron}\n"
                    message += f"Remaining: {result['remaining_segments']} for this patron\n"
                    
                await interaction.response.send_message(message)
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in magic_obligation: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing obligations.", 
                ephemeral=True
            )
            
    @app_commands.command(name="magic_fatigue", description="Manage character magical fatigue")
    @app_commands.describe(
        character_name="Character name",
        action="Action to perform",
        amount="Amount of fatigue to add/clear (default: 1)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Clear", value="clear")
    ])
    async def magic_fatigue(self, interaction: discord.Interaction, 
                           character_name: str,
                           action: app_commands.Choice[str],
                           amount: int = 1):
        """Manage character magical fatigue"""
        try:
            magic_manager = self._get_magic_manager()
            action_value = action.value if hasattr(action, 'value') else action
            
            if amount <= 0:
                await interaction.response.send_message(
                    "❌ Amount must be positive", 
                    ephemeral=True
                )
                return
                
            if action_value == "add":
                result = magic_manager.add_fatigue(character_name, amount)
            elif action_value == "clear":
                result = magic_manager.clear_fatigue(character_name, amount)
            else:
                await interaction.response.send_message(
                    "❌ Invalid action specified", 
                    ephemeral=True
                )
                return
                
            if result["status"] == "success":
                if action_value == "add":
                    await interaction.response.send_message(
                        f"✅ Added {amount} magical fatigue to {character_name}\n"
                        f"Total fatigue: {result['fatigue']}\n"
                        f"Effect: {result['fatigue_effects']}"
                    )
                elif action_value == "clear":
                    await interaction.response.send_message(
                        f"✅ Cleared {amount if amount else 'all'} magical fatigue from {character_name}\n"
                        f"Remaining fatigue: {result['fatigue']}"
                    )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in magic_fatigue: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing fatigue.", 
                ephemeral=True
            )
            
    @app_commands.command(name="magic_backlash", description="Manage character backlash Story Beats")
    @app_commands.describe(
        character_name="Character name",
        action="Action to perform",
        sb_amount="Number of Story Beats to add/clear (default: 1)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Clear", value="clear")
    ])
    async def magic_backlash(self, interaction: discord.Interaction, 
                            character_name: str,
                            action: app_commands.Choice[str],
                            sb_amount: int = 1):
        """Manage character backlash Story Beats"""
        try:
            magic_manager = self._get_magic_manager()
            action_value = action.value if hasattr(action, 'value') else action
            
            if sb_amount <= 0 and action_value == "add":
                await interaction.response.send_message(
                    "❌ Story Beat amount must be positive", 
                    ephemeral=True
                )
                return
                
            if action_value == "add":
                result = magic_manager.add_backlash_sb(character_name, sb_amount)
            elif action_value == "clear":
                result = magic_manager.clear_backlash_sb(character_name, sb_amount)
            else:
                await interaction.response.send_message(
                    "❌ Invalid action specified", 
                    ephemeral=True
                )
                return
                
            if result["status"] == "success":
                if action_value == "add":
                    await interaction.response.send_message(
                        f"✅ Added {sb_amount} backlash Story Beat(s) to {character_name}\n"
                        f"Total backlash SB: {result['backlash_sb']}"
                    )
                elif action_value == "clear":
                    await interaction.response.send_message(
                        f"✅ Cleared {sb_amount if sb_amount else 'all'} backlash Story Beat(s) from {character_name}\n"
                        f"Remaining backlash SB: {result['backlash_sb']}"
                    )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in magic_backlash: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing backlash.", 
                ephemeral=True
            )
            
    @app_commands.command(name="magic_summon", description="Manage summoned entities")
    @app_commands.describe(
        character_name="Character name",
        action="Action to perform",
        entity_name="Entity name",
        cap="Entity capability (1-5, for summoning)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Summon", value="summon"),
        app_commands.Choice(name="Advance", value="advance"),
        app_commands.Choice(name="Dismiss", value="dismiss"),
        app_commands.Choice(name="Status", value="status")
    ])
    async def magic_summon(self, interaction: discord.Interaction, 
                          character_name: str,
                          action: app_commands.Choice[str],
                          entity_name: str = None,
                          cap: int = 1):
        """Manage summoned entities"""
        try:
            magic_manager = self._get_magic_manager()
            action_value = action.value if hasattr(action, 'value') else action
            
            # Validate entity name for actions that need it
            if action_value in ["summon", "advance", "dismiss"] and not entity_name:
                await interaction.response.send_message(
                    "❌ Entity name required for this action", 
                    ephemeral=True
                )
                return
                
            # Validate cap for summoning
            if action_value == "summon" and (cap < 1 or cap > 5):
                await interaction.response.send_message(
                    "❌ Entity capability must be between 1 and 5", 
                    ephemeral=True
                )
                return
                
            result = None
            if action_value == "summon":
                result = magic_manager.summon_entity(character_name, entity_name, cap)
            elif action_value == "advance":
                result = magic_manager.advance_leash(character_name, entity_name, 1)
            elif action_value == "dismiss":
                result = magic_manager.dismiss_summon(character_name, entity_name)
            elif action_value == "status":
                result = magic_manager.get_summons(character_name)
                
            if result and result["status"] == "success":
                if action_value == "summon":
                    await interaction.response.send_message(
                        f"✅ {character_name} summoned {entity_name}\n"
                        f"Capability: {cap} | Leash: {result['leash']} segments"
                    )
                elif action_value == "advance":
                    progress_bar = result.get('progress_bar', '')
                    departed = result.get('departed', False)
                    
                    message = f"✅ Advanced leash for {entity_name} by 1 segment\n{progress_bar}"
                    if departed:
                        message += f"\n🔔 **{entity_name} has departed!**"
                        
                    await interaction.response.send_message(message)
                elif action_value == "dismiss":
                    await interaction.response.send_message(
                        f"✅ Dismissed {entity_name}"
                    )
                elif action_value == "status":
                    summons = result.get("summons", [])
                    if summons:
                        message = f"🔮 **{character_name}'s Summons**\n"
                        message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        for summon in summons:
                            status = summon.get('status', 'unknown')
                            status_icon = "🟢" if status == "active" else "🔴"
                            progress_bar = magic_manager._create_progress_bar(
                                summon.get('current_leash', 0),
                                summon.get('leash', 1)
                            )
                            
                            message += f"{status_icon} **{summon['entity']}** (Cap {summon['cap']})\n"
                            message += f"   Leash: {progress_bar}\n"
                            if status == "departed":
                                message += "   ⚰️ Departed\n"
                        await interaction.response.send_message(message)
                    else:
                        await interaction.response.send_message(
                            f"🔮 {character_name} has no active summons"
                        )
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
            logger.error(f"Error in magic_summon: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing summons.", 
                ephemeral=True
            )
            
    @app_commands.command(name="magic_status", description="Show character's complete magic status")
    @app_commands.describe(character_name="Character name")
    async def magic_status(self, interaction: discord.Interaction, character_name: str):
        """Show character's complete magic status"""
        try:
            magic_manager = self._get_magic_manager()
            result = magic_manager.get_magic_status(character_name)
            
            if result["status"] == "success":
                formatted_status = self._format_magic_status(result)
                await interaction.response.send_message(formatted_status, ephemeral=True)
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in magic_status: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving magic status.", 
                ephemeral=True
            )
            
    @app_commands.command(name="magic_patron", description="Get information about a patron")
    @app_commands.describe(patron_name="Patron name")
    async def magic_patron(self, interaction: discord.Interaction, patron_name: str):
        """Get information about a patron"""
        try:
            magic_manager = self._get_magic_manager()
            result = magic_manager.get_patron_info(patron_name)
            
            if result:
                await interaction.response.send_message(
                    f"🏛️ **{patron_name}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Thematic Skill**: {result['thematic_skill']}\n"
                    f"**Gift/Domain**: {result['gift']}"
                )
            else:
                # List available patrons
                patrons_result = magic_manager.list_patrons()
                if patrons_result["status"] == "success":
                    patron_list = ", ".join(patrons_result["patrons"])
                    await interaction.response.send_message(
                        f"❌ Patron '{patron_name}' not found.\n"
                        f"**Available Patrons**: {patron_list}",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ Patron '{patron_name}' not found.",
                        ephemeral=True
                    )
                    
        except Exception as e:
            logger.error(f"Error in magic_patron: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving patron information.", 
                ephemeral=True
            )
            
    # Helper methods
    def _format_obligation_status(self, status_data: dict) -> str:
        """Format obligation status for Discord display"""
        result = f"🔮 **{status_data['character']}'s Obligations**\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**Total Obligation**: {status_data['total_obligation']}\n"
        result += f"**Capacity**: {status_data['capacity']}\n"
        result += f"**Fatigue**: {status_data['fatigue']}\n"
        result += f"**Status**: {status_data['obligation_status']}\n\n"
        
        if status_data['patron_breakdown']:
            result += "**By Patron**:\n"
            for patron, segments in status_data['patron_breakdown'].items():
                result += f"• {patron}: {segments} segment(s)\n"
                
        return result
        
    def _format_magic_status(self, status_data: dict) -> str:
        """Format magic status for Discord display"""
        char = status_data['character']
        obligation = status_data['obligation']
        result = f"🔮 **{char}'s Magic Status**\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**Spirit**: {status_data['spirit']} | **Presence**: {status_data['presence']}\n"
        result += f"**Capacity**: {status_data['capacity']}\n\n"
        
        # Obligation section
        result += f"**Obligation**: {obligation['total_obligation']}/{obligation['capacity']}\n"
        result += f"**Status**: {obligation['obligation_status']}\n"
        result += f"**Fatigue**: {status_data['fatigue']} ({status_data['fatigue_effects']})\n"
        result += f"**Backlash SB**: {status_data['backlash_sb']}\n\n"
        
        # Patron breakdown
        if obligation['patron_breakdown']:
            result += "**Patron Obligations**:\n"
            for patron, segments in obligation['patron_breakdown'].items():
                result += f"• {patron}: {segments}\n"
            result += "\n"
            
        # Summons
        summons = status_data['summons']
        if summons:
            result += "**Active Summons**:\n"
            for summon in summons:
                if summon['status'] == 'active':
                    progress_bar = self._get_magic_manager()._create_progress_bar(
                        summon['current_leash'], 
                        summon['leash']
                    )
                    result += f"• {summon['entity']} (Cap {summon['cap']}): {progress_bar}\n"
                    
        return result

async def setup(bot: commands.Bot):
    """Cog setup function"""
    await bot.add_cog(MagicCommands(bot))

