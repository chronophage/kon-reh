# utils/clock_utils.py
def calculate_clock_size(rank):
    """Calculate clock size based on card rank"""
    if 2 <= rank <= 5:
        return 4  # Minor
    elif 6 <= rank <= 10:
        return 6  # Standard
    elif rank in [11, 12, 13]:  # J, Q, K
        return 8  # Major
    elif rank == 14:  # Ace
        return 10  # Pivotal

def get_fatigue_effect(level):
    """Return fatigue effect description"""
    effects = {
        0: "No penalty",
        1: "Re-roll one success on next roll",
        2: "Re-roll one success on each roll",
        3: "Re-roll two successes on each roll",
        4: "Collapse/KO - Out of scene until treated"
    }
    return effects.get(level, "Invalid fatigue level")
