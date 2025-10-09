import random
from typing import List, Dict, Tuple
from enum import Enum

class DescriptionLevel(Enum):
    BASIC = "Basic"
    DETAILED = "Detailed"
    INTRICATE = "Intricate"

class DiceManager:
    def __init__(self):
        pass
        
    def roll_pool(self, dice_count: int) -> List[int]:
        """
        Roll a pool of d10 dice
        
        Args:
            dice_count: Number of dice to roll
            
        Returns:
            List of dice results (1-10)
        """
        if dice_count <= 0:
            return []
        return [random.randint(1, 10) for _ in range(dice_count)]
        
    def count_successes(self, results: List[int]) -> int:
        """
        Count successes (6 or higher)
        
        Args:
            results: List of dice results
            
        Returns:
            Number of successes
        """
        return sum(1 for result in results if result >= 6)
        
    def count_story_beats(self, results: List[int]) -> int:
        """
        Count Story Beats (1s rolled)
        
        Args:
            results: List of dice results
            
        Returns:
            Number of Story Beats
        """
        return sum(1 for result in results if result == 1)
        
    def apply_description_ladder(self, results: List[int], 
                               description_level: DescriptionLevel) -> Tuple[List[int], str]:
        """
        Apply the Description Ladder reroll rules
        
        Args:
            results: Initial dice results
            description_level: Level of description (Basic, Detailed, Intricate)
            
        Returns:
            Tuple of (final results, reroll description)
        """
        if description_level == DescriptionLevel.BASIC:
            return results, "No rerolls for Basic description"
            
        original_results = results.copy()
        reroll_count = 0
        reroll_description = ""
        
        if description_level == DescriptionLevel.DETAILED:
            # Reroll one 1
            if 1 in results:
                first_one_index = results.index(1)
                results[first_one_index] = random.randint(1, 10)
                reroll_count = 1
                reroll_description = "Rerolled one 1 for Detailed description"
                
        elif description_level == DescriptionLevel.INTRICATE:
            # Reroll all 1s
            ones_count = results.count(1)
            if ones_count > 0:
                for i in range(len(results)):
                    if results[i] == 1:
                        results[i] = random.randint(1, 10)
                reroll_count = ones_count
                reroll_description = f"Rerolled {ones_count} ones for Intricate description"
                
        return results, reroll_description
        
    def roll_with_description(self, dice_count: int, dv: int,
                            description_level: DescriptionLevel = DescriptionLevel.BASIC) -> Dict:
        """
        Roll dice pool with description ladder applied and DV comparison
        
        Args:
            dice_count: Number of dice to roll
            dv: Difficulty Value to beat
            description_level: Level of description
            
        Returns:
            Dictionary with roll results and analysis
        """
        # Initial roll
        initial_results = self.roll_pool(dice_count)
        initial_successes = self.count_successes(initial_results)
        initial_story_beats = self.count_story_beats(initial_results)
        
        # Apply description ladder
        final_results, reroll_description = self.apply_description_ladder(
            initial_results.copy(), description_level
        )
        
        final_successes = self.count_successes(final_results)
        final_story_beats = self.count_story_beats(final_results)
        
        # Determine outcome based on DV
        outcome = self._determine_outcome(final_successes, initial_story_beats, dv)
        boons_earned = self._calculate_boons(final_successes, dv, initial_story_beats)
        
        return {
            'dice_count': dice_count,
            'dv': dv,
            'description_level': description_level.value,
            'initial_results': initial_results,
            'initial_successes': initial_successes,
            'initial_story_beats': initial_story_beats,
            'final_results': final_results,
            'final_successes': final_successes,
            'final_story_beats': final_story_beats,
            'reroll_description': reroll_description,
            'outcome': outcome,
            'boons_earned': boons_earned
        }
        
    def _determine_outcome(self, successes: int, story_beats: int, dv: int) -> str:
        """
        Determine the narrative outcome based on successes vs DV and story beats
        
        Args:
            successes: Number of successes
            story_beats: Number of story beats generated
            dv: Difficulty Value
            
        Returns:
            Narrative outcome description
        """
        if successes == 0:
            return "Miss - No progress, but GM gains Story Beats to spend"
        elif successes >= dv and story_beats == 0:
            return "Clean Success - Achieve intent crisply"
        elif successes >= dv and story_beats > 0:
            return "Success & Cost - Achieve intent but with complications"
        elif 0 < successes < dv:
            return "Partial - Some progress with complications"
        else:
            return "Unknown outcome"
            
    def _calculate_boons(self, successes: int, dv: int, story_beats: int) -> int:
        """
        Calculate boons earned from the roll - only on miss or partial success
        
        Args:
            successes: Number of successes
            dv: Difficulty Value
            story_beats: Number of story beats
            
        Returns:
            Number of boons earned
        """
        # Boons are earned only on misses and partial successes
        if successes == 0:  # Miss
            return 2
        elif successes > 0 and successes < dv:  # Partial success
            return 1
        # Success & Cost and Clean Success earn no boons
        return 0
        
    def _get_narrative_suggestions(self, successes: int, story_beats: int, dv: int) -> List[str]:
        """
        Get narrative suggestions based on roll results
        
        Args:
            successes: Number of successes
            story_beats: Number of story beats
            dv: Difficulty Value
            
        Returns:
            List of narrative suggestions
        """
        suggestions = []
        
        if successes == 0:
            suggestions.append("No progress on your primary goal")
            suggestions.append("GM can spend Story Beats for complications")
            suggestions.append("Consider a different approach")
        elif successes >= dv and story_beats == 0:
            suggestions.append("Clean execution of your intent")
            suggestions.append("Minimal complications or fallout")
        elif successes >= dv and story_beats > 0:
            suggestions.append("Success achieved but with complications")
            if story_beats >= 1:
                suggestions.append("Minor noise, trace, or time loss")
            if story_beats >= 2:
                suggestions.append("Alarm raised or lesser foe appears")
        else:  # Partial success
            suggestions.append("Partial progress with complications")
            if story_beats >= 1:
                suggestions.append("Minor complication affects outcome")
            if story_beats >= 2:
                suggestions.append("Moderate setback impacts progress")
                
        return suggestions
        
    def simulate_backlash(self, story_beats: int, element: str = None) -> Dict:
        """
        Simulate elemental backlash based on Story Beats
        
        Args:
            story_beats: Number of Story Beats generated
            element: Optional elemental association
            
        Returns:
            Dictionary with backlash details
        """
        if story_beats == 0:
            return {'type': 'None', 'description': 'No backlash'}
            
        # Determine backlash severity
        if story_beats == 1:
            severity = "Minor"
        elif story_beats <= 3:
            severity = "Moderate"
        else:
            severity = "Major"
            
        # Element-specific backlashes (simplified)
        elements = {
            "Earth": ["Stability issues", "Structural weakness", "Rigidity or collapse"],
            "Fire": ["Heat or energy surge", "Spread or scorch", "Uncontrolled burning"],
            "Air": ["Dispersal or scattering", "Whipping winds", "Loss of control"],
            "Water": ["Flooding or contamination", "Flow disruption", "Corrosion"],
            "Fate": ["Paradox or closure", "Causality disruption", "Inevitable outcome"],
            "Life": ["Overgrowth or fever", "Vitality surge", "Uncontrolled growth"],
            "Luck": ["Side coincidence", "Irony or misfortune", "Fortune reversal"],
            "Death": ["Thinning walls", "Nightmares", "Threshold crossing"]
        }
        
        element_effects = elements.get(element, ["Generic complication", "Narrative twist"])
        effect = element_effects[min(story_beats - 1, len(element_effects) - 1)]
        
        return {
            'type': severity,
            'element': element,
            'description': effect,
            'story_beats_spent': story_beats
        }
        
    def format_roll_results(self, roll_data: Dict) -> str:
        """
        Format roll results for Discord display
        
        Args:
            roll_data: Dictionary from roll_with_description
            
        Returns:
            Formatted string for Discord
        """
        desc = roll_data['description_level']
        dv = roll_data['dv']
        initial = roll_data['initial_results']
        final = roll_data['final_results']
        init_succ = roll_data['initial_successes']
        final_succ = roll_data['final_successes']
        init_sb = roll_data['initial_story_beats']
        final_sb = roll_data['final_story_beats']
        outcome = roll_data['outcome']
        boons = roll_data['boons_earned']
        
        # Format dice results
        initial_str = ", ".join(map(str, initial))
        final_str = ", ".join(map(str, final))
        
        result = f"🎲 **Dice Roll** (DV {dv}, {desc} description)\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**Initial Roll:** [{initial_str}]\n"
        result += f"**Successes:** {init_succ} | **Story Beats:** {init_sb}\n\n"
        
        if desc != "Basic":
            result += f"**{roll_data['reroll_description']}**\n"
            result += f"**Final Results:** [{final_str}]\n"
            
        result += f"**Final Successes:** {final_succ} | **Final Story Beats:** {final_sb}\n"
        result += f"**Boons Earned:** {boons}\n\n"
        result += f"**Outcome:** {outcome}\n"
        
        # Add narrative suggestions
        suggestions = self._get_narrative_suggestions(final_succ, final_sb, dv)
        if suggestions:
            result += "\n**Narrative Suggestions:**\n"
            for suggestion in suggestions[:3]:  # Limit to 3 suggestions
                result += f"• {suggestion}\n"
                
        return result

