Based on the Fate's Edge Essentials and SRD documents, here's a focused implementation plan for a Roll20 module, prioritizing **core playability** while respecting the system's narrative-first design. This plan avoids over-engineering and focuses on what enables smooth table play.

---

### **I. Core Implementation Priorities (Must-Have for Play)**
These elements are non-negotiable for running the game. Implement these first—they form the engine.

#### **A. Automated Resolution Engine (The Heart of the Module)**
*Replace manual dice math with one-click rolls that enforce all core mechanics.*
- **Roll Template** (`!fe-roll` or sheet button):
  - Inputs: `Attribute` (dropdown), `Skill` (dropdown), `DV` (number field, default=3), `Position` (dropdown: Dominant/Controlled/Desperate, default=Controlled)
  - Auto-calculates dice pool = `Attribute + Skill`
  - Rolls `d10s` equal to pool size
  - **Counts successes**: 6-9 = 1 success, 10 = 2 successes
  - **Counts Story Beats (SB)**: each die showing `1` = 1 SB for GM
  - **Applies Position modifiers**:
    - *Dominant*: Re-roll one failure (die ≤5; 10s never re-rolled)
    - *Desperate*: Re-roll one success (die ≥6; 10s never re-rolled)
    - *Controlled*: No re-rolls
  - **Determines outcome** using Outcome Matrix:
    - Successes ≥ DV, SB=0 → **Clean Success** (intent achieved, no complication)
    - Successes ≥ DV, SB>0 → **Success with SB** (intent achieved; GM spends SB for complication)
    - 0 < Successes < DV → **Partial** (progress made; player gains 1 Boon)
    - Successes = 0 → **Miss** (no progress; player gains 2 Boons; GM escalates with SB)
  - **Auto-awards Boons** (tracked on sheet):
    - Partial: +1 Boon
    - Miss: +2 Boons
  - **Outputs formatted chat message** showing:
    - Dice pool (e.g., `Wits 4 + Stealth 2 = [9,6,4,2,1]`)
    - Successes/SB count
    - Position applied
    - Final outcome
    - Boons awarded (if any)
    - *Example*: `Partial! You gain 1 Boon. GM gains 1 SB (from the 1 rolled).`

*Why this works*: Eliminates 90% of mechanical overhead. Players declare intent/approach → GM sets DV/Position → click roll → outcome is clear. GM focuses on narrating consequences, not math.

#### **B. Resource Trackers (Player-Facing Automation)**
*Track Boons, Fatigue, and Harm with scene/session limits enforced automatically.*
- **Boons Tracker**:
  - Current value (0-5, starts at 0)
  - **Max 5 enforced** (cannot exceed)
  - **Auto-reduce to 2 at scene end** (via GM button: "End Scene → Trim Boons to 2")
  - Spend actions:
    - `Spend 1 Boon → Re-roll one die` (prompts to select which die to re-roll from last roll)
    - `Spend 1 Boon → Improve Position by 1 step` (before next roll)
    - `Spend 1 Boon → Activate Asset` (prompts for asset name)
    - `Spend 2 Boons → Convert to 1 XP` (once/session max; tracks session use)
- **Fatigue/Harm Tracker**:
  - Fatigue (0 to Body attribute)
  - Harm (0-3)
  - **Armor Conversion Auto-applied** when taking Harm:
    - Prompt: `Take Harm? [1/2/3]` + `Armor Type? [None/Light/Medium/Heavy]`
    - Uses SRD Armor Conversion Table to convert Harm → Fatigue
    - Implements "Roller-Coaster" (Taking Harm clears all existing Fatigue first)
    - Fatigue overflow → auto-increases Harm + clears Fatigue
  - Recovery actions:
    - `Short Rest (1hr) → Remove 2 Fatigue`
    - `Long Rest → Remove all Fatigue`
    - *Harm recovery requires external GM adjudication* (medical/magical healing)

*Why this works*: Players see resources update in real-time. GM doesn't need to bookkeep Fatigue/Harm conversion—math happens automatically. Scene-end Boon trim is one click.

#### **C. Minimal Viable Character Sheet**
*Enables creation and core stat tracking without bloat.*
- **Tabs**: Attributes | Skills | Talents | Bonds/Complications | Gear | Resources
- **Key Fields**:
  - Attributes (Body/Wits/Spirit/Presence): 1-5, auto-calculates XP cost if editing (optional)
  - Skills: 0-5 (dropdowns), grouped by type (Combat/Physical/Social/etc.)
  - Talents: List with XP cost (auto-sums total spent)
  - Bonds: Text field + checkbox for "once/session Boon available"
  - Complications: Text field + checkbox for "adds +1 SB to scene start"
  - Gear: Free-text (abstracted per SRD—no tracking needed)
  - Resources: Boons/Fatigue/Harm trackers (as above)
- **Auto-calculations** (optional but helpful):
  - Dice pool for any Attribute+Skill (shown on hover/click)
  - Current XP spent (if tracking creation)

*Why this works*: Matches SRD's "abstracted gear" philosophy. Focuses on narrative hooks (Bonds/Complications) and core stats. Avoids overwhelming players with unused fields.

#### **D. GM Tools for Narrative Flow**
*Enables the GM to spend SB and manage timers without breaking immersion.*
- **SB Spend Button**:
  - Prompt: `Spend SB? [1/2/3/4+]` 
  - Outputs narrative cue based on SRD SB Spend Menu:
    - 1 SB: *"Minor pressure: [noise/trace/tick timer +1]"* 
    - 2 SB: *"Moderate setback: [alarm raised/lose Position/lesser foe appears]"
    - 3+ SB: *"Major turn: [trap springs/authority arrives/environment shifts]"*
  - *GM then narrates the specific complication* (system provides framework, not rigid output)
- **Timer Tracker** (simple counter):
  - Create via `/timer name [segments]` (e.g., `/timer Barrow Collapse 6`)
  - Buttons: `Tick +1`, `Tick -1`, `Reset`
  - Auto-announces when timer fills (e.g., `Barrow Collapse timer filled! Entrance seals.`)

*Why this works*: Gives GM mechanical tools to escalate tension (per SRD guidelines) while keeping focus on narrative description. Timers make pressure visible.

---

### **II. Secondary Implementation (Add After Core is Stable)**
These enhance depth but aren't needed for Session 1. Add based on playgroup needs.

#### **A. Magic Systems (Optional but Recommended for Casters)**
*Implement the simplest path first (Free Caster), then expand.*
- **Free Caster (Spellcasting) Macro** (`!fe-cast`):
  - Inputs: `Tags` (free-text, e.g., `[FIRE][STRIKE]`), `DV` (auto-calculated: `1 + number of tags`; dangerous tags add +2)
  - Rolls `Spirit + Arcana` (or relevant Attribute)
  - Applies same Resolution Engine (Position/DV/Outcome Matrix)
  - **Backlash Menu** on Partial/Miss or ≥2 SB:
    - Prompt: `Backlash Severity? [Minor/Moderate/Major]` 
    - Outputs thematic effect based on dominant element (e.g., Fire backlash: *"Smoke triggers lantern; room starts catching fire (Clock: Fire Spread [4])*")
- **Runekeeper/Invoker/Cantor** can be added later as:
  - Runekeeper: Tracks Obligation per Patron (simple counter), DV = max(Obligation Cost - Spirit, Rite Tier)
  - Invoker: Tracks Symbol status (Maintained/Neglected/Compromised)
  - Cantor: Tracks Corruption Timer (segments = Spirit), triggers blooms on fill

*Why staged*: Free Caster covers 80% of magic use. Complex paths add value only if players take them.

#### **B. Compendium Integration**
*Essential for rules reference—use Roll20's Compendium feature.*
- **Must-Include SRD Content** (CC BY-NC-SA compliant):
  - Core Resolution Loop (quick reference)
  - Outcome Matrix
  - Position/Effect table
  - Boon/SB spend menus
  - Fatigue/Harm/Armor Conversion tables
  - Core Skill List (with common uses)
  - Talent Cost Tiers (Minor/Major/etc.)
  - Armor Conversion Examples
- **Optional (Proprietary Content)**: 
  - Only include if you have license (e.g., pre-generated characters from Essentials)
  - *Never* include setting lore, original NPCs, or adventure modules without permission

*Why this works*: Players/GM can `@{compendium}` references mid-game without breaking flow. SRD content is free to share.

#### **C. Starter Adventure Support**
*For groups using The Lantern at Dusk (Essentials Ch. 5).*
- **Handouts**: 
  - Maps (Entrance, Spirit Corridor, Lantern Chamber)
  - Pre-generated Characters (Levi, Lyra, Sera, Mira, Kael) as journal entries
  - Timer Trackers: Barrow Collapse [6], Lena’s Agenda [4]
- **Scene Macros**:
  - `!fe-scene Entry`: Sets DV=3, Position=Controlled for Body+Athletics roll
  - `!fe-spirit-corridor`: Presence+Sway roll (DV=3, Controlled)
  - etc.
- **Advancement Tracker**: 
  - Simple counter for XP earned (6-10/session per SRD)
  - Lists spend options (Attribute/Skill/Talent costs)

*Why this works*: Reduces prep for new GMs. Lets groups jump straight into play.

---

### **III. What to AVOID (Common Pitfalls)**
*These create bloat without improving narrative focus—per SRD design philosophy.*
- ❌ **Fixed Initiative Tracker**: Fate's Edge uses fiction-first spotlighting. *Use Roll20's turn tracker manually* (GM adjusts order based on scene).
- ❌ **Opposed Roll Enforcer**: System uses DV set by GM (not opposed rolls) for most actions. *Only enforce for specific cases* (e.g., Stealth vs Notice)—let GM decide.
- ❌ **Complex Asset/Follower Automation**: Tracking Asset Status/Follower States adds bookkeeping. *Start with free-text fields*; add automation only if group uses these heavily.
- ❌ **Pre-rolling all 1s for SB**: SB generation is automatic in the roll template. *No need for extra steps*.
- ❌ **Forcing Boon-to-XP Conversion**: SRD explicitly says this is suboptimal. *Make it possible but not prominent* (e.g., small button labeled "Convert Boons → XP (once/session)").

---

### **IV. Roll20-Specific Technical Notes**
*Optimize for performance and ease of use.*
- **Use Sheet Workers** for:
  - Auto-calculating dice pools when Attribute/Skill changes
  - Enforcing Boon max (5) and scene-end trim (→2)
  - Updating XP cost during creation (if implemented)
- **Roll Templates** for:
  - Clean, formatted roll output (critical for readability)
  - Consistent SB/Boon award messaging
  - Color-coding outcomes (e.g., Green=Clean Success, Yellow=Partial, Red=Miss)
- **API Scripts (Pro Tier Only)**:
  - *Only* consider for: 
    - Auto-trimming Boons at scene end (via `!fe-end-scene` command)
    - Tracking once/session Bond Boon usage (reset at downtime)
  - *Avoid* over-automation—GM should retain narrative control.
- **Mobile-Friendly Design**: 
  - Keep roll template compact (prioritize essential info)
  - Use collapsible sections for advanced options (Talents, Gear)

---

### **V. Implementation Roadmap**
1. **Week 1**: Core Resolution Engine + Resource Trackers (Boons/Fatigue/Harm) + Minimal Character Sheet
   - *Test*: Run a 1-skill check (e.g., Stealth) with all outcomes.
2. **Week 2**: GM Tools (SB Spend, Timer Tracker) + Compendium (SRD core rules)
   - *Test*: Run Scene 1 of Lantern at Dusk (Entry obstacle).
3. **Week 3**: Free Caster Magic + Starter Adventure Handouts
   - *Test*: Sera casting a spell during Spirit Corridor scene.
4. **Optional**: Add Runekeeper/Invoker/Cantor paths or Deck of Consequences based on group interest.

> **Key Philosophy**: The module should *disappear* during play—letting the story shine. If players/GMs are staring at the sheet instead of each other, you've over-engineered. Fate's Edge thrives when mechanics serve the narrative, not the reverse.

This plan delivers **90% of the play value with 10% of the work**—exactly what a narrative-first system like Fate's Edge needs. Start small, let the table discover complexity through play (per SRD Section 2.1), and expand only when the story demands it. 

*"The road remembers. Every broken wheel leaves a mark, every lit lamp bears witness. The only question is: what are you willing to owe?"*—Let your module help answer that question, not distract from it.
