import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def _get_character_manager(self):
        """Helper to get character manager from bot"""
        return self.bot.character_manager
        
    def _get_resource_manager(self):
        """Helper to get resource manager from bot"""
        return self.bot.resource_manager
        
    @app_commands.command(name="character_create", description="Create a new Fate's Edge character")
    @app_commands.describe(
        name="Character name",
        body="Body attribute (1-5)",
        wits="Wits attribute (1-5)",
        spirit="Spirit attribute (1-5)",
        presence="Presence attribute (1-5)"
    )
    async def character_create(self, interaction: discord.Interaction, name: str, 
                              body: int = 2, wits: int = 2, spirit: int = 2, presence: int = 2):
        """Create a new character"""
        try:
            # Validate attributes
            for attr_name, attr_value in [("Body", body), ("Wits", wits), ("Spirit", spirit), ("Presence", presence)]:
                if attr_value < 1 or attr_value > 5:
                    await interaction.response.send_message(
                        f"❌ {attr_name} must be between 1 and 5", 
                        ephemeral=True
                    )
                    return
                    
            # Create character
            char_manager = self._get_character_manager()
            success = char_manager.create_character(
                name=name,
                player_id=str(interaction.user.id),
                attributes={
                    "Body": body,
                    "Wits": wits,
                    "Spirit": spirit,
                    "Presence": presence
                }
            )
            
            if success:
                # Initialize magic tracking
                magic_manager = self._get_magic_manager()
                magic_manager.initialize_character(name, spirit, presence)
                
                await interaction.response.send_message(
                    f"✅ Successfully created character **{name}**!\n"
                    f"Attributes: Body {body} | Wits {wits} | Spirit {spirit} | Presence {presence}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"❌ Character **{name}** already exists!", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in character_create: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while creating the character.", 
                ephemeral=True
            )
            
    @app_commands.command(name="character_show", description="Display a character sheet")
    @app_commands.describe(name="Character name to display")
    async def character_show(self, interaction: discord.Interaction, name: str):
        """Show character sheet"""
        try:
            char_manager = self._get_character_manager()
            character = char_manager.get_character(name)
            
            if not character:
                await interaction.response.send_message(
                    f"❌ Character **{name}** not found!", 
                    ephemeral=True
                )
                return
                
            # Check if user owns character or is GM
            if character.get('player_id') != str(interaction.user.id) and not self._is_gm(interaction):
                await interaction.response.send_message(
                    "❌ You don't have permission to view this character sheet!", 
                    ephemeral=True
                )
                return
                
            # Format character sheet
            sheet = self._format_character_sheet(character)
            await interaction.response.send_message(sheet, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error in character_show: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while retrieving the character sheet.", 
                ephemeral=True
            )
            
    @app_commands.command(name="character_list", description="List all your characters")
    async def character_list(self, interaction: discord.Interaction):
        """List all characters belonging to the user"""
        try:
            char_manager = self._get_character_manager()
            characters = char_manager.get_player_characters(str(interaction.user.id))
            
            if not characters:
                await interaction.response.send_message(
                    "You don't have any characters yet. Use `/character_create` to create one!", 
                    ephemeral=True
                )
                return
                
            # Format character list
            char_list = "**Your Characters:**\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            for char in characters:
                name = char.get('name', 'Unknown')
                attrs = char.get('attributes', {})
                body = attrs.get('Body', 0)
                wits = attrs.get('Wits', 0)
                spirit = attrs.get('Spirit', 0)
                presence = attrs.get('Presence', 0)
                
                char_list += f"**{name}** - Body {body} | Wits {wits} | Spirit {spirit} | Presence {presence}\n"
                
            await interaction.response.send_message(char_list, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error in character_list: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while listing your characters.", 
                ephemeral=True
            )
            
    @app_commands.command(name="character_add_skill", description="Add or update a skill for your character")
    @app_commands.describe(
        character_name="Name of your character",
        skill_name="Name of the skill",
        level="Skill level (0-5)"
    )
    async def character_add_skill(self, interaction: discord.Interaction, character_name: str, 
                                 skill_name: str, level: int):
        """Add or update a skill for a character"""
        try:
            # Validate skill level
            if level < 0 or level > 5:
                await interaction.response.send_message(
                    "❌ Skill level must be between 0 and 5", 
                    ephemeral=True
                )
                return
                
            char_manager = self._get_character_manager()
            character = char_manager.get_character(character_name)
            
            if not character:
                await interaction.response.send_message(
                    f"❌ Character **{character_name}** not found!", 
                    ephemeral=True
                )
                return
                
            # Check ownership
            if character.get('player_id') != str(interaction.user.id) and not self._is_gm(interaction):
                await interaction.response.send_message(
                    "❌ You don't have permission to modify this character!", 
                    ephemeral=True
                )
                return
                
            # Add skill
            success = char_manager.add_skill(character_name, skill_name, level)
            
            if success:
                await interaction.response.send_message(
                    f"✅ Skill **{skill_name}** set to level **{level}** for **{character_name}**",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"❌ Failed to add skill to **{character_name}**", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in character_add_skill: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while adding the skill.", 
                ephemeral=True
            )
            
    @app_commands.command(name="character_roll", description="Roll dice for your character")
    @app_commands.describe(
        character_name="Name of your character",
        attribute="Attribute to use",
        skill_name="Skill to use (optional)",
        dv="Difficulty Value (default: 2)",
        description="Description level (Basic, Detailed, Intricate)"
    )
    @app_commands.choices(description=[
        app_commands.Choice(name="Basic", value="Basic"),
        app_commands.Choice(name="Detailed", value="Detailed"),
        app_commands.Choice(name="Intricate", value="Intricate")
    ])
    async def character_roll(self, interaction: discord.Interaction, character_name: str,
                            attribute: str, skill_name: Optional[str] = None, dv: int = 2,
                            description: app_commands.Choice[str] = "Basic"):
        """Roll dice using character's attributes and skills"""
        try:
            char_manager = self._get_character_manager()
            character = char_manager.get_character(character_name)
            
            if not character:
                await interaction.response.send_message(
                    f"❌ Character **{character_name}** not found!", 
                    ephemeral=True
                )
                return
                
            # Validate attribute
            valid_attributes = ["Body", "Wits", "Spirit", "Presence"]
            if attribute not in valid_attributes:
                await interaction.response.send_message(
                    f"❌ Invalid attribute. Valid attributes: {', '.join(valid_attributes)}", 
                    ephemeral=True
                )
                return
                
            # Get dice pool
            dice_pool = char_manager.get_dice_pool(character_name, attribute, skill_name)
            
            if dice_pool <= 0:
                await interaction.response.send_message(
                    f"❌ Invalid dice pool calculation for {attribute}" + 
                    (f" + {skill_name}" if skill_name else ""), 
                    ephemeral=True
                )
                return
                
            # Roll dice
            dice_manager = self._get_dice_manager()
            from bot.managers.dice_manager import DescriptionLevel
            desc_level = DescriptionLevel(description.value if hasattr(description, 'value') else description)
            
            roll_result = dice_manager.roll_with_description(dice_pool, dv, desc_level)
            
            # Format result
            formatted_result = dice_manager.format_roll_results(roll_result)
            
            # Add character context
            full_result = f"🎲 **{character_name}** rolls for **{attribute}" + \
                         (f" + {skill_name}**" if skill_name else "**") + \
                         f" (DV {dv})\n" + formatted_result
            
            # Award boons if applicable
            boons_earned = roll_result.get('boons_earned', 0)
            if boons_earned > 0:
                char_manager.add_boon(character_name, boons_earned)
                full_result += f"\n✨ **Awarded {boons_earned} boon(s)** to {character_name}"
                
            # Generate Story Beats if applicable
            story_beats = roll_result.get('final_story_beats', 0)
            if story_beats > 0:
                resource_manager = self._get_resource_manager()
                resource_manager.add_story_beats(story_beats)
                full_result += f"\n🌀 **Generated {story_beats} Story Beat(s)** for the party"
                
            await interaction.response.send_message(full_result)
            
        except Exception as e:
            logger.error(f"Error in character_roll: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while rolling dice.", 
                ephemeral=True
            )
            
    @app_commands.command(name="character_boon", description="Manage character boons")
    @app_commands.describe(
        character_name="Name of your character",
        action="Add or spend boons",
        amount="Number of boons to add/spend (default: 1)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Spend", value="spend")
    ])
    async def character_boon(self, interaction: discord.Interaction, character_name: str,
                            action: app_commands.Choice[str], amount: int = 1):
        """Add or spend boons for a character"""
        try:
            char_manager = self._get_character_manager()
            character = char_manager.get_character(character_name)
            
            if not character:
                await interaction.response.send_message(
                    f"❌ Character **{character_name}** not found!", 
                    ephemeral=True
                )
                return
                
            # Check ownership
            if character.get('player_id') != str(interaction.user.id) and not self._is_gm(interaction):
                await interaction.response.send_message(
                    "❌ You don't have permission to modify this character!", 
                    ephemeral=True
                )
                return
                
            if action.value == "add":
                char_manager.add_boon(character_name, amount)
                new_boons = character.get('boons', 0) + amount
                await interaction.response.send_message(
                    f"✅ Added **{amount}** boon(s) to **{character_name}**. Total: **{min(5, new_boons)}/5**",
                    ephemeral=True
                )
            else:  # spend
                current_boons = character.get('boons', 0)
                if current_boons >= amount:
                    success = char_manager.spend_boon(character_name, amount)
                    if success:
                        await interaction.response.send_message(
                            f"✅ Spent **{amount}** boon(s) from **{character_name}**. Remaining: **{current_boons - amount}/5**",
                            ephemeral=True
                        )
                    else:
                        await interaction.response.send_message(
                            f"❌ Failed to spend boons from **{character_name}**", 
                            ephemeral=True
                        )
                else:
                    await interaction.response.send_message(
                        f"❌ **{character_name}** doesn't have enough boons! Current: **{current_boons}/5**",
                        ephemeral=True
                    )
                    
        except Exception as e:
            logger.error(f"Error in character_boon: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while managing boons.", 
                ephemeral=True
            )
            
    @app_commands.command(name="character_harm", description="Set character harm level")
    @app_commands.describe(
        character_name="Name of your character",
        level="Harm level (0-3)"
    )
    async def character_harm(self, interaction: discord.Interaction, character_name: str, level: int):
        """Set character harm level"""
        try:
            if level < 0 or level > 3:
                await interaction.response.send_message(
                    "❌ Harm level must be between 0 and 3", 
                    ephemeral=True
                )
                return
                
            char_manager = self._get_character_manager()
            character = char_manager.get_character(character_name)
            
            if not character:
                await interaction.response.send_message(
                    f"❌ Character **{character_name}** not found!", 
                    ephemeral=True
                )
                return
                
            # Check ownership or GM status
            if character.get('player_id') != str(interaction.user.id) and not self._is_gm(interaction):
                await interaction.response.send_message(
                    "❌ You don't have permission to modify this character!", 
                    ephemeral=True
                )
                return
                
            # Set harm
            success = char_manager.set_harm(character_name, level)
            
            if success:
                harm_effects = {
                    0: "No effect",
                    1: "-1 die to related actions",
                    2: "-1 die to most actions",
                    3: "Incapacitated or dying"
                }
                
                await interaction.response.send_message(
                    f"✅ Set harm level for **{character_name}** to **{level}**\n"
                    f"**Effect**: {harm_effects.get(level, 'Unknown')}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"❌ Failed to set harm for **{character_name}**", 
                    ephemeral=True
                )
                
        except Exception as e:
            logger.error(f"Error in character_harm: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while setting harm.", 
                ephemeral=True
            )
            
    # Helper methods
    def _get_dice_manager(self):
        """Helper to get dice manager from bot"""
        return self.bot.dice_manager
        
    def _get_magic_manager(self):
        """Helper to get magic manager from bot"""
        return self.bot.magic_manager
        
    def _is_gm(self, interaction: discord.Interaction) -> bool:
        """Check if user has GM permissions (simplified)"""
        # In a real implementation, this would check roles or a GM list
        return interaction.user.guild_permissions.administrator
        
    def _format_character_sheet(self, character: dict) -> str:
        """Format character data into a readable sheet"""
        name = character.get('name', 'Unknown')
        attrs = character.get('attributes', {})
        skills = character.get('skills', {})
        harm = character.get('harm', 0)
        fatigue = character.get('fatigue', 0)
        boons = character.get('boons', 0)
        story_beats = character.get('story_beats', 0)
        
        # Attribute effects
        harm_effects = {
            0: "No effect",
            1: "-1 die to related actions",
            2: "-1 die to most actions",
            3: "Incapacitated or dying"
        }
        
        fatigue_effects = {
            0: "No effect",
            1: "Re-roll one success",
            2: "Re-roll one success per roll",
            3: "Re-roll two successes per roll",
            4: "Collapse/KO"
        }
        
        sheet = f"🧙 **{name}**\n"
        sheet += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        sheet += f"**Attributes:** Body {attrs.get('Body', 0)} | Wits {attrs.get('Wits', 0)} | Spirit {attrs.get('Spirit', 0)} | Presence {attrs.get('Presence', 0)}\n\n"
        
        if skills:
            sheet += "**Skills:**\n"
            for skill_name, skill_level in skills.items():
                sheet += f"  • {skill_name}: {skill_level}\n"
            sheet += "\n"
            
        sheet += "**Conditions:**\n"
        sheet += f"  • Harm: {harm}/3 ({harm_effects.get(harm, 'Unknown')})\n"
        sheet += f"  • Fatigue: {fatigue} ({fatigue_effects.get(fatigue, 'No effect')})\n"
        sheet += f"  • Boons: {boons}/5\n"
        sheet += f"  • Story Beats: {story_beats}\n\n"
        
        # Assets and followers if they exist
        assets = character.get('assets', [])
        followers = character.get('followers', [])
        bonds = character.get('bonds', [])
        
        if assets:
            sheet += "**Assets:**\n"
            for asset in assets:
                sheet += f"  • {asset.get('name', 'Unknown')} ({asset.get('condition', 'Unknown')})\n"
            sheet += "\n"
            
        if followers:
            sheet += "**Followers:**\n"
            for follower in followers:
                sheet += f"  • {follower.get('name', 'Unknown')} (Cap {follower.get('cap', 0)}, {follower.get('condition', 'Unknown')})\n"
            sheet += "\n"
            
        if bonds:
            sheet += "**Bonds:**\n"
            for bond in bonds:
                sheet += f"  • {bond.get('name', 'Unknown')}\n"
                
        return sheet

async def setup(bot: commands.Bot):
    """Cog setup function"""
    await bot.add_cog(CharacterCommands(bot))

