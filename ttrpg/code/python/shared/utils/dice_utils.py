# shared/utils/dice_utils.py
import random
from typing import List, Tuple

class DiceRoller:
    """Utility class for Fate's Edge dice mechanics"""
    
    @staticmethod
    def roll_dice_pool(pool_size: int) -> List[int]:
        """Roll a pool of d10 dice"""
        return [random.randint(1, 10) for _ in range(pool_size)]
    
    @staticmethod
    def count_successes(dice: List[int]) -> int:
        """Count successes (6 or higher)"""
        return sum(1 for die in dice if die >= 6)
    
    @staticmethod
    def count_complications(dice: List[int]) -> int:
        """Count complications (1s)"""
        return dice.count(1)
    
    @staticmethod
    def apply_description_rerolls(dice: List[int], description_quality: str) -> List[int]:
        """Apply rerolls based on description quality"""
        rerolled_dice = dice.copy()
        
        if description_quality == "Detailed" and 1 in rerolled_dice:
            # Reroll one 1
            index = rerolled_dice.index(1)
            rerolled_dice[index] = random.randint(1, 10)
            
        elif description_quality == "Intricate":
            # Reroll all 1s
            for i in range(len(rerolled_dice)):
                if rerolled_dice[i] == 1:
                    rerolled_dice[i] = random.randint(1, 10)
                    
        return rerolled_dice
    
    @staticmethod
    def resolve_roll(pool_size: int, difficulty: int, description_quality: str = "Basic") -> dict:
        """Resolve a complete Fate's Edge roll"""
        # Initial roll
        dice = DiceRoller.roll_dice_pool(pool_size)
        
        # Apply description rerolls
        final_dice = DiceRoller.apply_description_rerolls(dice, description_quality)
        
        # Calculate results
        successes = DiceRoller.count_successes(final_dice)
        complications = DiceRoller.count_complications(dice)  # Complications based on original roll
        
        # Determine outcome
        if successes >= difficulty and complications == 0:
            outcome = "Clean Success"
        elif successes >= difficulty and complications > 0:
            outcome = "Success with Cost"
        elif 0 < successes < difficulty:
            outcome = "Partial Success"
        elif successes == 0:
            outcome = "Miss"
        else:
            outcome = "Unknown"
            
        return {
            "dice": final_dice,
            "original_dice": dice,
            "successes": successes,
            "complications": complications,
            "outcome": outcome,
            "description_quality": description_quality
        }

