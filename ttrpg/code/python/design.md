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
# /combat position set="Risky"
# /combat range set="Near"
# /combat clock create name="Mob Overwhelm" size=6
# /combat clock advance name="Mob Overwhelm" segments=1
# /combat end

# Response for combat status:
"""
⚔️ Combat Active - Bandit Ambush
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Position: Risky ⚠️  | Range: Near
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
