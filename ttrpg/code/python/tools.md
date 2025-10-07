Based on the Fate's Edge SRD and the existing tools you're building, here's a list of additional tools you can create to enhance the gaming experience:

## List of Tools to Create

### 1. **(SB) Spend Menu UI/Tab**
- Already identified - database schema provided
- Category-based spending options (Universal, Combat, Stealth, etc.)

### 2. **Dice Roller with Complication Tracking**
- Roll pools of d10s
- Auto-count successes (6+)
- Auto-count 1s as Story Beats
- Apply description ladder bonuses (re-roll 1s)
- Track banked (SB)

### 3. **Character Sheet Manager**
- Track Attributes (Body, Wits, Spirit, Presence)
- Track Skills and ratings
- Manage XP allocation
- Track Talents and Prestige Abilities
- Condition tracks (Fatigue, Harm)

### 4. **Follower/Asset Manager**
- Track On-Screen Followers (Cap ratings, specialties)
- Track Off-Screen Assets (Tiers, conditions)
- Upkeep tracking (Maintained/Neglected/Compromised)
- Activation tracking (Boons/XP spent)

### 5. **Supply Clock Tracker**
- Visual 4-segment clock
- Track Full → Low → Dangerously Low → Out of Supply
- Automatic Fatigue application
- Foraging/Recovery actions

### 6. **Magic/Spell Tracker**
- Casting Loop implementation (Channel → Weave → Backlash)
- Potential tracking
- Art-specific Backlash tables
- Ritual casting support

### 7. **Boon Manager**
- Track earned Boons (max 5)
- Boon spending (re-roll, asset activation, XP conversion)
- Backstory Boon tracking

### 8. **XP Calculator & Tracker**
- Calculate costs for:
  - Attribute increases (new rating × 3)
  - Skill increases (new level × 2)
  - Followers (Cap²)
  - Assets (Tier-based)
- Downtime tracking
- Haste clock tracking

### 9. **Talent/Prestige Ability Browser**
- Searchable database of Talents
- Filter by culture/race requirements
- Prerequisite checking
- Cost and effect descriptions

### 10. **Session Tracker**
- Award XP tracking
- Complication spotlight tracking
- Session objectives
- End-of-session checklist

### 11. **Campaign Clock Manager**
- Mandate/Crisis dials (0-6)
- Crown Spread tracking
- Campaign-specific clocks
- Finale preparation

### 12. **Familiar Manager**
- Track Familiar Bonds
- Role specialties
- Exposure/Harm tracking
- Solo Beat tracking

### 13. **Ritual Calculator**
- Multi-participant spell casting
- Combined dice pools
- Shared Story Beats
- Backlash severity scaling

### 14. **Gear/Kit Manager**
- Track owned gear
- Condition status (Compromised/Broken)
- Upkeep requirements
- Cultural/Regional specialties

### 15. **Scene Builder**
- Set Difficulty Ladder (DV 1-4+)
- Track stakes and consequences
- Pre-scene planning tools
- Cheat prompts integration

### 16. **Opposition Tracker**
- NPC/Monster stat tracking
- Threat clock management
- Complication spending for GM
- Scaling difficulty tools

### 17. **Faction/Relationship Tracker**
- Relationship clocks
- Faction influence tracking
- Loyalty metrics
- Political maneuvering tools

### 18. **Downtime Activity Planner**
- Training/mentorship tracking
- Research/crafting project clocks
- Asset maintenance scheduling
- Character growth planning

### 19. **Combat Tracker**
- Initiative tracking
- Position/Controlled status
- Harm/Injury tracking
- Battlefield condition management

### 20. **GM Toolkit**
- Deck of Consequences integration
- Complication spending guides
- Scaling guidance for mixed tiers
- Quick reference cards

## Implementation Priority

1. **(SB) Spend Menu** (done)
2. **Dice Roller** (done)

ui/follower_tracker_tab.py
ui/asset_management_tab.py
ui/condition_tracker_tab.py  # For tracking Maintained/Neglected/Compromised states


ui/fatigue_tracker_tab.py
ui/boon_tracker_tab.py
ui/xp_tracker_tab.py


ui/magic_tracker_tab.py
ui/backlash_generator_tab.py
ui/ritual_planner_tab.py


ui/campaign_clock_tab.py  # For Mandate/Crisis clocks
ui/crown_spread_tab.py    # For the finale system
ui/evidence_tracker_tab.py # For Immaculate/Scorched evidence


ui/timer_tab.py
ui/notes_tab.py
ui/player_dashboard_tab.py  # Overview for all player resources


.
├── data
│   ├── __init__.py
│   ├── database.py
│   ├── fate_edge_clocks.sql
│   └── fate_edge_data_clean.sql
├── gm_tools
│   ├── __init__.py
│   ├── main.py
│   ├── requirements.txt
│   ├── ui
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── supply_clock_tab.py
│   │   ├── fatigue_tracker_tab.py
│   │   ├── boon_tracker_tab.py
│   │   ├── xp_tracker_tab.py
│   │   ├── combat_tracker_tab.py
│   │   ├── scene_builder_tab.py
│   │   ├── cp_spend_tab.py
│   │   ├── consequence_tab.py
│   │   ├── campaign_clock_tab.py
│   │   ├── evidence_tracker_tab.py
│   │   ├── follower_tracker_tab.py
│   │   ├── dice_roller_tab.py
│   │   ├── npc_tab.py
│   │   ├── clocks_tab.py
│   │   ├── adventure_tab.py
│   │   └── settings_tab.py
│   └── utils
│       ├── __init__.py
│       ├── card_utils.py
│       ├── clock_utils.py
│       └── styles.py
├── player_tools
│   ├── __init__.py
│   ├── main.py
│   ├── requirements.txt
│   ├── ui
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── character_sheet_tab.py
│   │   ├── skill_tracker_tab.py
│   │   ├── asset_tracker_tab.py
│   │   ├── condition_tracker_tab.py
│   │   ├── xp_planner_tab.py
│   │   ├── dice_roller_tab.py
│   │   ├── boon_tracker_tab.py
│   │   ├── fatigue_tracker_tab.py
│   │   ├── supply_tracker_tab.py
│   │   ├── follower_tracker_tab.py
│   │   ├── talent_tracker_tab.py
│   │   ├── ritual_tracker_tab.py
│   │   └── settings_tab.py
│   └── utils
│       ├── __init__.py
│       ├── character_utils.py
│       └── validation_utils.py
└── shared
    ├── __init__.py
    ├── models
    │   ├── __init__.py
    │   ├── character.py
    │   ├── asset.py
    │   └── clock.py
    └── constants.py

