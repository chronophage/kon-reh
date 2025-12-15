# Fate's Edge Discord Bot - Design Specification

## Overview
A Discord bot to facilitate Fate's Edge gameplay directly within Discord, focusing on dice rolling, resource tracking, and quick reference tools while maintaining the game's narrative-first approach.

## Core Features

### 1. Dice Rolling System
```python
# Command: /roll dice_pool=6 description="Intricate" action="Sneak past guards"
# Response: 
# 🎲 Kael rolls 6 dice for "Sneak past guards" (Intricate)
# Results: [9, 7, 5, 2, 1, 1] 
# Successes: 3 | Story Beats: 2
# 💡 Re-rolling 1s for Intricate description...
# Final: [9, 7, 5, 2, 6, 3] 
# Successes: 4 | Story Beats: 0
# ✅ Success with Cost - You sneak past but make some noise
```

### 2. Character Management
```python
# Commands:
# /character create name="Lyra" body=2 wits=3 spirit=2 presence=3
# /character add_skill name="Lyra" skill="Sway" level=2
# /character show name="Lyra"
# /character list

# Response for /character show:
"""
🧙‍ Lyra the Silver-Tongued
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Attributes: Body 2 | Wits 3 | Spirit 2 | Presence 3
Skills: Sway 2, Deception 1, Performance 1
Resources: Boons: 2/5 | Story Beats: 1
Conditions: Harm 1 (-1 die to related) | Fatigue 1
Assets: Safehouse (Maintained)
Followers: Scout (Cap 2, Steady)
Bonds: Kael (Adventuring Partner)
"""
```

### 3. Resource Tracking
```python
# Commands:
# /supply status
# /supply advance reason="Bad weather"
# /supply clear
# /fatigue add player="Kael" level=1 reason="Magic casting"
# /fatigue clear player="Kael"
# /harm set player="Lyra" level=2
# /boon add player="Kael" amount=1
# /boon spend player="Lyra" amount=2

# Response for /supply status:
"""
🏕️ Party Supply Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[■■□□□□] Low Supply (2/4 segments)
⚠️  Dangerously Low - Each character gains Fatigue 1
Next foraging: DV 2 Survival test
"""
```

### 4. Combat Assistant
```python
# Commands:
# /combat start
# /combat position set="Controlled"
# /combat range set="Near"
# /combat clock create name="Mob Overwhelm" size=6
# /combat clock advance name="Mob Overwhelm" segments=1
# /combat end

# Response for combat status:
"""
⚔️ Combat Active - Bandit Ambush
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Position: Controlled ⚠️  | Range: Near
Clocks:
  Mob Overwhelm: [■■□□□□] (2/6)
Party Conditions:
  Kael: Harm 1, Fatigue 2
  Lyra: Fatigue 1
Story Beats: 3 (Budget: 8)
"""
```

### 5. Magic System Support
```python
# Commands:
# /magic cast path="Runekeeper" rite="Ward of Protection"
# /magic obligation show player="Kael"
# /magic obligation add player="Kael" patron="Sealed Gate" segments=2
# /magic backlash element="Air" severity="Minor"

# Response for obligation:
"""
🔮 Kael's Obligation Tracks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Capacity: Spirit 2 + Presence 3 = 5
Current: 4 segments (80%)
  Sealed Gate: ■■□□□□□□ (2/8)
  Ikasha: ■■■□□□□□ (3/8)
Fatigue: 0 (Safe)
⚠️  Approaching capacity limit!
"""
```

### 6. Travel System
```python
# Commands:
# /travel start destination="Silkstrand"
# /travel clock show
# /travel clock advance segments=1 reason="Storm delay"
# /travel consequence draw
# /travel end

# Response for travel clock:
"""
🗺️ Journey to Silkstrand
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Clock: [■■■□□□] (3/6 segments)
Location: Approaching Three-Queens Bridge
Complications: 1 SB generated
Weather: Light rain, worsening Position by 1 step
Supplies: Low (2/4)
"""
```

### 7. Deck Integration
```python
# Commands:
# /deck draw type="Travel" region="Acasia"
# /deck draw_consequence severity="Moderate"
# /deck quick_hook region="Mistlands"
# /deck full_seed region="Valewood"

# Response for deck draw:
"""
🃏 Card Draw - Mistlands
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🂡 Spade (Place): Bell-Line levee
🂪 Heart (Actor): Bell-warden
🃝 Club (Pressure): Wrong bell—a cracked note opens a door
🃊 Diamond (Leverage): Bell-key—unlock one bell on the Line

Clock Size: 8-segment (based on Queen)
⚠️  Complication: Wrong bell creates 1 SB
💡 Leverage: Bell-key is position changer (no roll needed)
"""
```

### 8. Session Management
```python
# Commands:
# /session start
# /session log event="Discovered cursed crossroads"
# /session xp award player="Kael" amount=2 reason="Creative problem solving"
# /session show
# /session end

# Response for session show:
"""
📜 Session Log - The Cursed Crossroads
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Started: 2 hours ago
Active Players: Kael, Lyra, Theron
Key Events:
  • Discovered cursed crossroads
  • Negotiated with the Pale Shepherd
  • XP Awarded: Kael (+2), Lyra (+1)
Story Beats Generated: 6
Current Supply: Low (2/4)
"""
```

## Technical Architecture

### Bot Structure
```
fate_edge_bot/
├── main.py                 # Bot entry point
├── bot/
│   ├── commands/           # Slash command handlers
│   │   ├── core_commands.py
│   │   ├── character_commands.py
│   │   ├── combat_commands.py
│   │   ├── magic_commands.py
│   │   ├── travel_commands.py
│   │   ├── deck_commands.py
│   │   └── session_commands.py
│   ├── managers/
│   │   ├── dice_manager.py
│   │   ├── character_manager.py
│   │   ├── resource_manager.py
│   │   ├── combat_manager.py
│   │   ├── magic_manager.py
│   │   ├── travel_manager.py
│   │   └── session_manager.py
│   ├── utils/
│   │   ├── dice_roller.py
│   │   ├── deck_handler.py
│   │   ├── formatter.py
│   │   └── validators.py
│   └── data/
│       ├── characters.json
│       ├── sessions.json
│       └── decks/
├── config/
│   └── settings.py
└── requirements.txt
```

### Core Components

#### 1. Dice Manager
```python
class DiceManager:
    async def roll_pool(self, dice_count, description="Basic"):
        results = [random.randint(1, 10) for _ in range(dice_count)]
        initial_successes = sum(1 for r in results if r >= 6)
        initial_sb = sum(1 for r in results if r == 1)
        
        # Apply description ladder
        if description == "Detailed":
            results = self._reroll_ones(results, 1)
        elif description == "Intricate":
            results = self._reroll_ones(results, len([r for r in results if r == 1]))
            
        final_successes = sum(1 for r in results if r >= 6)
        final_sb = sum(1 for r in results if r == 1)
        
        return {
            'initial': {'results': results, 'successes': initial_successes, 'sb': initial_sb},
            'final': {'results': results, 'successes': final_successes, 'sb': final_sb}
        }
```

#### 2. Character Manager
```python
class CharacterManager:
    def __init__(self):
        self.characters = {}
        
    async def create_character(self, name, attributes, skills):
        character = {
            'name': name,
            'attributes': attributes,
            'skills': skills,
            'harm': 0,
            'fatigue': 0,
            'boons': 0,
            'story_beats': 0,
            'obligation': {},
            'assets': [],
            'followers': [],
            'bonds': []
        }
        self.characters[name] = character
        return character
        
    async def get_dice_pool(self, character_name, attribute, skill_level):
        char = self.characters.get(character_name)
        if not char:
            return 0
        return char['attributes'].get(attribute, 0) + skill_level
```

#### 3. Resource Manager
```python
class ResourceManager:
    def __init__(self):
        self.supply_clock = 0
        self.fatigue = {}
        self.tactical_clocks = {}
        
    async def advance_supply(self, reason=""):
        self.supply_clock = min(4, self.supply_clock + 1)
        return {
            'level': self.supply_clock,
            'status': self._get_supply_status(),
            'effect': self._get_supply_effect()
        }
        
    def _get_supply_status(self):
        statuses = {
            0: "Full Supply",
            1: "Low Supply", 
            2: "Low Supply",
            3: "Dangerously Low",
            4: "Out of Supply"
        }
        return statuses.get(self.supply_clock, "Unknown")
```

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)
- Discord bot setup with basic command framework
- Character creation and management
- Dice rolling system
- Basic resource tracking

### Phase 2: Core Game Systems (Week 2)
- Combat assistant
- Magic system support
- Travel system integration
- Deck drawing functionality

### Phase 3: Advanced Features (Week 3)
- Session management
- Detailed character sheets
- Complex resource interactions
- Visual formatting improvements

### Phase 4: Polish & Deployment (Week 4)
- Error handling and validation
- User documentation
- Deployment scripts
- Testing and optimization

## Deployment Configuration

### Requirements.txt
```
discord.py>=2.3.0
python-dotenv>=1.0.0
jsonschema>=4.17.0
```

### Environment Variables (.env)
```
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=optional_guild_id_for_testing
DEBUG=true
```

### Main Bot Setup
```python
# main.py
import discord
from discord.ext import commands
from bot.commands import setup_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await setup_commands(bot)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    import os
    bot.run(os.getenv('DISCORD_TOKEN'))
```

## User Experience Features

### 1. Interactive Help System
```python
# Command: /help category="combat"
# Response: Detailed help for combat commands with examples
```

### 2. Quick Reference Cards
```python
# Command: /reference topic="position_effects"
# Response: Visual summary of Position state effects
```

### 3. Undo System
```python
# Command: /undo
# Response: Revert last action with confirmation
```

### 4. Private Messaging
```python
# Commands can be used in private messages for sensitive actions
# like character sheet viewing or secret rolls

# Efficient Fate's Edge Discord Bot Development with Qwen-Coder

## Recommended Approach

The most efficient way to build this bot using Qwen-Coder is through an **iterative, component-based development strategy** that leverages Qwen-Coder's strengths in code generation and refactoring.

## Development Strategy

### 1. **Start with Core Infrastructure**
```bash
# Create project structure first
mkdir fate_edge_bot
cd fate_edge_bot
mkdir -p bot/{commands,managers,utils,data} config
touch main.py requirements.txt .env
```

Ask Qwen-Coder to generate:
- Basic `main.py` with Discord bot setup
- `requirements.txt` with dependencies
- `.env` template
- Basic project structure

### 2. **Component-by-Component Development**
Build each major component separately, testing as you go:

#### Phase 1: Core Framework
```
1. Basic bot connection and command framework
2. Character manager (JSON storage)
3. Dice rolling engine
4. Simple resource tracking
```

#### Phase 2: Game Systems
```
5. Combat system
6. Magic system
7. Travel system
8. Deck integration
```

#### Phase 3: Advanced Features
```
9. Session management
10. Help system
11. Error handling
12. Final integration
```

## Efficient Qwen-Coder Usage Patterns

### 1. **Use Specific, Focused Prompts**
Instead of "Create the entire bot", use:
```
"Create a Discord bot main.py file using discord.py 2.3 that:
1. Uses slash commands
2. Has a basic character management system
3. Can roll dice with /roll command
4. Stores data in JSON files
5. Includes proper error handling"
```

### 2. **Leverage Code Refinement**
```
"Refactor this dice roller to support the Description Ladder:
- Basic: No rerolls
- Detailed: Reroll one 1
- Intricate: Reroll all 1s"
```

### 3. **Incremental Expansion**
```
"Add these commands to the existing character system:
- /character show [name]
- /character list
- /character add_skill [name] [skill] [level]"
```

## Recommended Development Workflow

### Day 1-2: Foundation
1. **Project Setup**
   ```
   Prompt: "Create a complete Discord bot project structure for a Fate's Edge helper with directories for commands, managers, utils, and data"
   ```

2. **Basic Bot**
   ```
   Prompt: "Create main.py for a Discord bot that connects to Discord, uses slash commands, and has a simple ping command"
   ```

3. **Character System v1**
   ```
   Prompt: "Create a character manager class that can create, save, and load characters to/from JSON files. Characters should have name, attributes (Body/Wits/Spirit/Presence), and skills"
   ```

### Day 3-4: Core Mechanics
4. **Dice System**
   ```
   Prompt: "Create a dice manager class that can roll d10 pools, count successes (6+), count 1s as Story Beats, and support the Description Ladder (Basic, Detailed, Intricate)"
   ```

5. **Resource Tracking**
   ```
   Prompt: "Create a resource manager for Fate's Edge that tracks: supply clock (0-4), character fatigue, character harm, boons (0-5), and story beats"
   ```

### Day 5-6: Game Systems
6. **Combat System**
   ```
   Prompt: "Create a combat manager for Fate's Edge that tracks: position states (Dominant/Controlled/Desperate), range bands (Close/Near/Far), tactical clocks (Mob Overwhelm, etc.), and party conditions"
   ```

7. **Magic System**
   ```
   Prompt: "Create a magic manager for Fate's Edge that tracks: obligation segments per patron, character capacity (Spirit+Presence), and can calculate fatigue from overflow"
   ```

### Day 7-8: Integration & Polish
8. **Command Integration**
   ```
   Prompt: "Create Discord slash commands for: /roll, /character create, /character show, /supply status, /combat status"
   ```

9. **Deck System**
   ```
   Prompt: "Create a deck handler that can simulate drawing from Fate's Edge regional decks and the Deck of Consequences, returning formatted card results"
   ```

10. **Final Integration**
    ```
    Prompt: "Integrate all managers into a cohesive bot with proper error handling, help commands, and data persistence"
    ```

## Qwen-Coder Optimization Tips

### 1. **Provide Context**
Always include relevant existing code when asking for modifications:
```
"Given this dice manager class, add support for elemental backlash tracking:
[INSERT CURRENT CLASS CODE]"
```

### 2. **Use Incremental Refinement**
Start broad, then get specific:
```
"Create a character manager"
→ "Add JSON persistence to the character manager"
→ "Add validation to character creation"
→ "Add support for bonds and followers"
```

### 3. **Leverage Examples**
Reference existing patterns:
```
"Create a combat clock system similar to the supply clock but with named clocks like 'Mob Overwhelm' and 'Morale Collapse'"
```

### 4. **Request Documentation**
```
"For this character manager class, add docstrings explaining each method and include example usage"
```

## File-by-File Development Approach

### 1. **main.py** (Core bot setup)
### 2. **bot/managers/character_manager.py** (Characters)
### 3. **bot/managers/dice_manager.py** (Dice rolling)
### 4. **bot/managers/resource_manager.py** (Supply, fatigue, etc.)
### 5. **bot/managers/combat_manager.py** (Combat tracking)
### 6. **bot/managers/magic_manager.py** (Obligation, etc.)
### 7. **bot/managers/deck_manager.py** (Card drawing)
### 8. **bot/commands/core_commands.py** (Basic commands)
### 9. **bot/commands/character_commands.py** (Character commands)
### 10. **bot/commands/game_commands.py** (Combat, magic, travel)
### 11. **bot/utils/formatter.py** (Discord message formatting)
### 12. **Integration and testing**

## Testing Strategy with Qwen-Coder

After each component, ask:
```
"Create a simple test for this dice manager to verify it correctly:
1. Rolls the right number of dice
2. Counts successes properly
3. Handles the Description Ladder
4. Returns expected data structure"
