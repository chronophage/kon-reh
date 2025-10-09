import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SessionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def _get_resource_manager(self):
        """Helper to get resource manager from bot"""
        return self.bot.resource_manager
        
    def _get_character_manager(self):
        """Helper to get character manager from bot"""
        return self.bot.character_manager
        
    @app_commands.command(name="session_start", description="Start a new game session")
    @app_commands.describe(session_name="Name of the session (optional)")
    async def session_start(self, interaction: discord.Interaction, session_name: str = None):
        """Start a new game session"""
        try:
            resource_manager = self._get_resource_manager()
            result = resource_manager.start_session(session_name)
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"🎬 **Session Started**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Session**: {result['session_name']}\n"
                    f"**Story Beat Budget**: {result['story_beat_budget']}\n"
                    f"**Supply Status**: {result['supply_status']['status']['name']}\n\n"
                    f"Use `/session_log` to record events during the session!"
                )
            else:
                await interaction.response.send_message(
                    f"❌ {result['message']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in session_start: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while starting the session.", 
                ephemeral=True
            )
            
    @app_commands.command(name="session_end", description="End the current game session")
    async def session_end(self, interaction: discord.Interaction):
        """End the current game session"""
        try:
            resource_manager = self._get_resource_manager()
            result = resource_manager.end_session()
            
            if result["status"] == "success":
                await interaction.response.send_message(
                    f"🎬 **Session Ended**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Session**: {result['session_name']}\n"
                    f"Thanks for playing Fate's Edge!\n"
                    f"Use `/session_xp` to award experience points!"
                )
            elif "error" in result:
                await interaction.response.send_message(
                    f"❌ {result['error']}", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in session_end: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while ending the session.", 
                ephemeral=True
            )
            
    @app_commands.command(name="session_log", description="Log an event in the current session")
    @app_commands.describe(event="Description of the event")
    async def session_log(self, interaction: discord.Interaction, event: str):
        """Log an event in the current session"""
        try:
            resource_manager = self._get_resource_manager()
            success = resource_manager.log_event(event)
            
            if success:
                await interaction.response.send_message(
                    f"📝 **Event Logged**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Event**: {event}\n"
                    f"**Time**: {datetime.now().strftime('%H:%M')}"
                )
            else:
                await interaction.response.send_message(
                    "❌ No active session. Use `/session_start` first!", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in session_log: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while logging the event.", 
                ephemeral=True
            )
            
    @app_commands.command(name="session_status", description="Show current session status")
    async def session_status(self, interaction: discord.Interaction):
        """Show current session status"""
        try:
            resource_manager = self._get_resource_manager()
            
            # Get session info
            sessions = resource_manager.resources.get("sessions", [])
            if not sessions:
                await interaction.response.send_message(
                    "❌ No active session. Use `/session_start` to begin!", 
                    ephemeral=True
                )
                return
                
            current_session = sessions[-1]
            if current_session.get("end_time"):
                await interaction.response.send_message(
                    "❌ Current session has ended. Use `/session_start` to begin a new one!", 
                    ephemeral=True
                )
                return
                
            # Get resource status
            party_status = resource_manager.get_party_status()
            supply_status = party_status.get('supply', {})
            sb_budget = party_status.get('story_beat_budget', 0)
            
            # Format session duration
            start_time = datetime.fromisoformat(current_session["start_time"])
            duration = datetime.now() - start_time
            hours, remainder = divmod(int(duration.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            
            message = f"🎬 **Session Status**\n"
            message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            message += f"**Session**: {current_session['name']}\n"
            message += f"**Duration**: {duration_str}\n"
            message += f"**Events Logged**: {len(current_session.get('events', []))}\n\n"
            
            message += f"**🏕️ Supply**: {supply_status['status']['name']}\n"
            message += f"{supply_status['progress_bar']}\n\n"
            
            message += f"**🌀 Story Beats**: {sb_budget} available\n\n"
            
            # Active clocks
            active_clocks = party_status.get('active_clocks', {})
            if active_clocks:
                message += f"**⏱️ Active Clocks**:\n"
                for name, clock in active_clocks.items():
                    progress_bar = resource_manager._create_progress_bar(
                        clock['current'], clock['size']
                    )
                    message += f"• {name}: {progress_bar}\n"
                    
            await interaction.response.send_message(message)
            
        except Exception as e:
            logger.error(f"Error in session_status: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving session status.", 
                ephemeral=True
            )
            
    @app_commands.command(name="session_xp", description="Award XP to characters")
    @app_commands.describe(
        character_name="Name of character to award XP",
        amount="Amount of XP to award",
        reason="Reason for XP award"
    )
    async def session_xp(self, interaction: discord.Interaction, 
                        character_name: str, 
                        amount: int, 
                        reason: str = "General gameplay"):
        """Award XP to a character"""
        try:
            if amount <= 0:
                await interaction.response.send_message(
                    "❌ XP amount must be positive", 
                    ephemeral=True
                )
                return
                
            character_manager = self._get_character_manager()
            character = character_manager.get_character(character_name)
            
            if not character:
                await interaction.response.send_message(
                    f"❌ Character '{character_name}' not found!", 
                    ephemeral=True
                )
                return
                
            # In a real implementation, you would update the character's XP
            # For now, we'll just log it as an event
            resource_manager = self._get_resource_manager()
            resource_manager.log_event(f"Awarded {amount} XP to {character_name} for {reason}")
            
            await interaction.response.send_message(
                f"⭐ **XP Awarded**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"**Character**: {character_name}\n"
                f"**Amount**: {amount} XP\n"
                f"**Reason**: {reason}\n\n"
                f"Note: XP tracking would be implemented in a full version"
            )
            
        except Exception as e:
            logger.error(f"Error in session_xp: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while awarding XP.", 
                ephemeral=True
            )
            
    @app_commands.command(name="session_events", description="Show recent session events")
    @app_commands.describe(count="Number of recent events to show (default: 5)")
    async def session_events(self, interaction: discord.Interaction, count: int = 5):
        """Show recent session events"""
        try:
            resource_manager = self._get_resource_manager()
            
            # Get session info
            sessions = resource_manager.resources.get("sessions", [])
            if not sessions:
                await interaction.response.send_message(
                    "❌ No active session. Use `/session_start` first!", 
                    ephemeral=True
                )
                return
                
            current_session = sessions[-1]
            if current_session.get("end_time"):
                await interaction.response.send_message(
                    "❌ Current session has ended. Use `/session_start` to begin a new one!", 
                    ephemeral=True
                )
                return
                
            events = current_session.get("events", [])
            if not events:
                await interaction.response.send_message(
                    "📝 No events logged in this session yet."
                )
                return
                
            # Get recent events
            recent_events = events[-count:] if count > 0 else events
            
            message = f"📝 **Recent Session Events**\n"
            message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            message += f"**Session**: {current_session['name']}\n\n"
            
            for i, event in enumerate(reversed(recent_events), 1):
                timestamp = datetime.fromisoformat(event['time']).strftime('%H:%M')
                message += f"{i}. **[{timestamp}]** {event['event']}\n"
                
            await interaction.response.send_message(message)
            
        except Exception as e:
            logger.error(f"Error in session_events: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving session events.", 
                ephemeral=True
            )
            
    @app_commands.command(name="session_reset_sb", description="Reset party story beat budget")
    async def session_reset_sb(self, interaction: discord.Interaction):
        """Reset party story beat budget"""
        try:
            resource_manager = self._get_resource_manager()
            new_budget = resource_manager.reset_story_beat_budget()
            
            await interaction.response.send_message(
                f"🌀 **Story Beat Budget Reset**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"**New Budget**: {new_budget} Story Beats\n"
                f"Use these wisely for narrative tension!"
            )
            
        except Exception as e:
            logger.error(f"Error in session_reset_sb: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while resetting story beat budget.", 
                ephemeral=True
            )
            
    @app_commands.command(name="session_help", description="Show session management help")
    async def session_help(self, interaction: discord.Interaction):
        """Show help for session management commands"""
        try:
            help_text = (
                "🎬 **Session Management Help**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                
                "🔹 **Starting/Ending Sessions**\n"
                "`/session_start [name]` - Begin a new session\n"
                "`/session_end` - End the current session\n\n"
                
                "🔹 **Session Tracking**\n"
                "`/session_status` - Show current session info\n"
                "`/session_log <event>` - Record important events\n"
                "`/session_events [count]` - View recent events\n\n"
                
                "🔹 **Awards & Recognition**\n"
                "`/session_xp <character> <amount> [reason]` - Award XP\n"
                "`/session_reset_sb` - Reset story beat budget\n\n"
                
                "🔹 **Best Practices**\n"
                "• Start each session with `/session_start`\n"
                "• Log key events with `/session_log`\n"
                "• Award XP at session end with `/session_xp`\n"
                "• End sessions with `/session_end`"
            )
            
            await interaction.response.send_message(help_text)
            
        except Exception as e:
            logger.error(f"Error in session_help: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while showing help.", 
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    """Cog setup function"""
    await bot.add_cog(SessionCommands(bot))

