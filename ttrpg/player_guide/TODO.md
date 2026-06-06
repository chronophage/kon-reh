# Revision Plan for Fate's Edge Player’s Guide (Preserving File Structure)

This plan follows the same approach as the GM Guide revision: **clarity, usability, and philosophical alignment**, without reorganizing the existing 17 `.tex` files. Each section gets targeted improvements.

---

## Section 01: Introduction (`01_intro.tex`)

**Current weaknesses:** Dense philosophy, no explicit Session Zero guidance, safety tools buried, no “Flavor is Free” emphasis for players.

**Revisions:**

1. **Add a prominent “Session Zero” subsection** (after safety tools) that covers:
   - The game’s core philosophy for players: *“Optimal play = most fun. Spend Boons. Embrace failure. Courting Patron attention leads to better stories.”*
   - Player-GM contract: “We are co-creators, not adversaries.”
   - Resource mindset: “Boons are not XP tokens – spend them.”
   - Patron expectation: “They demand payment – embrace it as story fuel.”
   - Sample Session Zero checklist (player‑facing version – what to discuss, what to ask).
2. **Clarify “Flavor is Free” box:** Add note that this applies to **all** descriptive actions, not just magic – encourage narration of even mundane successes.
3. **Safety tools:** Keep as is, but add reminder that the GM can use the X‑card too.
4. **Add a “How to Use This Guide” quick reference** – one‑page summary of where to find core rules, magic, advancement, assets, etc.

---

## Section 02: Core Mechanics (`02_core_mechanics.tex`)

**Current weaknesses:** Core loop clear but initiative options presented as default (should be narrative first). Boon hoarding not discouraged enough. Player‑managed modules mentioned but not emphasised.

**Revisions:**

1. **Re‑order subsections** (without changing file structure):
   - 2.1 The 90‑Second Play Loop (keep)
   - **2.2 The Core Resolution Cycle** (move earlier, right after loop)
   - 2.3 Player‑Managed Modules (expand with clear “your job” bullet points)
   - 2.4 Basic Dice Mechanics (keep)
   - 2.5 Difficulty Value (keep)
   - 2.6 Outcome Matrix (keep)
   - 2.7 Boons – add “Why you should spend Boons” sidebar
   - 2.8 Position (keep)
   - 2.9 Story Beats – player‑facing advice (“don’t fear SB – they make the story exciting”)
   - 2.10 Harm and Fatigue – keep, but add “roller‑coaster” note (taking Harm clears Fatigue)
   - 2.11 Initiative – move optional systems (popcorn, side, speed) to end, **state first: “Default is narrative initiative”**
2. **Add a “Golden Rule” call‑out box:** “When in doubt, make the choice that serves the story.”
3. **Clarify DV 3 as default** and warn against DV inflation (reference GM Guide).
4. **Add a short example** of a player using a Boon to re‑roll a critical failure (turning a Miss into a Partial).
5. **Player‑Managed Modules:** Add a clear table of what players track (Obligation, Corruption, Leash, Asset States) with tick triggers – similar to GM Guide but player‑facing.

---

## Section 03: Magic and Special Abilities (`04_magic.tex` – note numbering)

**Current weaknesses:** Dense, assumes player knows all Patron rites; no guidance on “active vs passive” Patron presence based on campaign length; Obligation/Corruption tracking explained but not tied to player fun.

**Revisions:**

1. **Add “Patron as Co‑Star” subsection** (after 3.1 The Nature of Magic):
   - Explain that Patrons can be passive (long campaigns) or active (short campaigns/one‑shots).
   - Encourage players to lean into Patron demands as story hooks, not punishments.
2. **Adjudicating Magic (player advice):** Add a quick reference table for DV by spell scope (cantrip, combat, ritual, epic) and another for backlash severity by Position – adapted from GM Guide.
3. **Story Beats and Backlash:** Add an example of a player accepting a GM’s SB spend to create a *choice* (e.g., “You can succeed, but your Patron will demand a task – accept or let the spell fizzle”).
4. **Managing Obligation and Corruption:** Add player guidance: *“Track your own Obligation (player‑managed modules). When a Patron intrudes, treat it as a plot hook, not a penalty.”*
5. **Summoning:** Clarify that the spirit’s independent action on a Miss should be *interesting* – add a d6 table of spirit whims (adapted from GM Guide).
6. **Cantors and Corruption:** Add a note that neglected chorus cults can become **rival factions** – players should keep an eye on their followers.
7. **Psionics (optional):** Keep optional, but add a warning: “Psionics generates SB quickly – be prepared for the GM to spend them.”

---

## Section 04: Character Advancement (`03_advancement.tex` – note numbering)

**Current weaknesses:** Good but lacks guidance on spending XP for narrative growth (assets, followers) vs. personal stats; no explicit mention of Legacy Engine yet.

**Revisions:**

1. **Add “Philosophy of Growth” box:** “Every XP spent is a choice about who your character becomes – invest in yourself, your network, or your legacy.”
2. **Clarify Attribute/Skill costs** (already clear) but add a **“When to invest in Assets/Followers”** table (see Section 5.4–5.6).
3. **Add a cross‑reference to Legacy Engine (Chapter 13)** – “Planning for succession? Consider investing in a Cap 3+ follower early.”
4. **XP Award guidelines:** Keep but add a note: “Boons convert to XP at 2:1, but spending Boons during play is almost always more fun.”

---

## Section 05: Experience Paths and Character Building (`05_xp_paths.tex`)

**Current weaknesses:** Good conceptual material but could use more explicit links to the three archetypes (Solo, Balanced, Mastermind) from the GM Guide. No guidance on building for group synergy.

**Revisions:**

1. **Add “Player Archetypes” subsection** (after 5.3 Three Career Paths):
   - Solo, Mixed, Mastermind – describe each and suggest XP splits.
   - Help players identify their own style.
2. **Add “Building for Group Synergy”** – advice on ensuring the party covers key roles (combat, social, exploration, magic, assets).
3. **Enhance the “Start‑to‑Mid‑to‑Late Game” progression tables** with concrete examples of when to take a Follower vs. an Asset vs. a Talent.

---

## Section 06: Talents and Special Abilities (`06_talents.tex`)

**Current weaknesses:** Large talent list, but no guidance on talent synergy (e.g., Backstab + Shadow Dance + Deathblow). Costs are correct but layout is dense.

**Revisions:**

1. **Add a “Talent Synergies” sidebar** – show 2‑3 example chains (e.g., stealth assassin, magic blaster, protective tank).
2. **Clarify activation types** (Passive / Active / Reactive) with icons or bold labels.
3. **Add a “When to Take” recommendation** for each talent tier (Early Game: minor talents; Mid Game: major; Late Game: prestige/epic).
4. **Cross‑reference magic access talents** (Spellcraft, Familiar, Codex, Patron’s Symbol) to Chapter 3.

---

## Section 07: Assets and Followers (`07_assets_follower.tex` and also `13_assets.tex`, `14_followers.tex` – these appear duplicated/separate)

**Current weaknesses:** Asset and follower rules are split across multiple files (`07_assets_follower.tex`, `13_assets.tex`, `14_followers.tex`). Some duplication. No clear “when to invest” guidance.

**Revisions:**

1. **Consolidate into a single logical section** (but preserve file structure by cross‑referencing). In each file, add a note: “For full rules see Section X.”
2. **Add a “When to Invest” table** based on player archetype (Solo: 0‑10% XP; Mixed: 15‑25%; Mastermind: 35‑55%).
3. **Clarify upkeep costs** with examples (Efficient vs. Intensive).
4. **Add a “Succession” note:** “A loyal Follower (Cap 3+) can become your successor – see Legacy Engine, Chapter 13.”

---

## Section 08: World Interaction (`08_world_interaction.tex`)

**Current weaknesses:** Good travel and social rules, but lacks explicit tie to the regional subgenres (from Chapter 11).

**Revisions:**

1. **Add a cross‑reference to Chapter 11 (World Regions and Cultures)** – “Each region has a dominant fantasy subgenre. The travel rules let you blend them.”
2. **Clarify the travel roles** (Guide, Scout, Quartermaster, Watch) with a quick example.
3. **Add a “Using Assets and Followers During Travel” subsection** – spend Boons to activate an asset for a dramatic shortcut, etc.

---

## Section 09: Archetypes (`09_archetypes.tex`)

**Current weaknesses:** Example character concepts are fine, but no guidance on how to evolve them over tiers.

**Revisions:**

1. **Add a “Progression Path” paragraph** for each archetype – what to buy at Tier I, Tier II, Tier III.
2. **Cross‑reference the Legacy Engine** – “This character could be succeeded by their follower.”
3. **Add a note that these are examples, not restrictions** – encourage reskinning and mixing.

---

## Section 10: World and Cultures (`10_world_and_cultures.tex` and `11_world_powers.tex`)

**Current weaknesses:** Much duplicated from GM Guide. Player‑facing version should be lighter – focus on what players need to know for character creation and roleplay.

**Revisions:**

1. **Trim repetitive lore** – keep only player‑relevant details (cultural attitudes toward magic, common factions, typical dress, customs).
2. **Add a “How to Use This Section” box:** “Read only the region your character is from or where the campaign starts.”
3. **For each culture, add a one‑line “Player Hook”** – e.g., “Acasia: you owe a blood‑debt to a free company captain.”
4. **Remove GM‑only secrets** (hidden agendas, faction timers) – keep those in GM Guide.

---

## Section 11: World Powers (`11_world_powers.tex`) – likely merged with above

**Revisions:** Keep brief – just major factions and their public reputation. Move detailed faction timers to GM Guide.

---

## Section 12: Backgrounds (`12_backgrounds.tex`)

**Current weaknesses:** Good system but lacks integration with the Legacy Engine and Bonds.

**Revisions:**

1. **Add a “Backgrounds and Legacy” sidebar** – “Your background’s contact could become your successor.”
2. **Clarify that the Signature Contact is a free Cap 1 Follower** (cannot take independent actions but can assist).
3. **Add examples of background‑specific Boons** (already present, but could be expanded).
4. **Cross‑reference Bonds (Section 12.12)** – how background influences bond creation.

---

## Section 13: Legacy Engine (`13_legacy.tex`)

**Current weaknesses:** Excellent but placed late; players may not read it until end of campaign.

**Revisions:**

1. **Add a note in earlier sections (Advancement, Assets/Followers) pointing to this chapter** – “Thinking long‑term? Read about succession.”
2. **Clarify that a successor inherits Faction Standing, one Unresolved Burden, and a Legacy Bond** – with an example.
3. **Add a player‑facing “Legacy Planning” checklist** – what to do before your character retires (name a successor, settle debts, pass on an asset).

---

## Section 14: Enhanced Player Play (`15_enhanced_play.tex` – numbering off)

**Current weaknesses:** Optional systems (Momentum, Information Trading, Complication Bargaining) are great but could be more clearly marked as optional.

**Revisions:**

1. **Add a “Optional Rules” heading** – clearly separate core from optional.
2. **Add a “When to Use” recommendation** for each advanced technique.
3. **Cross‑reference the Threat Pool (GM Guide)** – players should know it exists but not rely on it.
4. **Add a “Player Tips for High‑Tier Play” subsection** – Boon scarcity, Bond transfers, using Assets.

---

## Appendices (`appendix_quick_reference.tex` and `witch_hunter.tex`)

**Current weaknesses:** Appendices X, Y, Z (tools, magic reference, pre‑made spells) are useful but could be better organised.

**Revisions:**

1. **Standardise appendix labels** (A, B, C, D) – not X, Y, Z.
2. **Add a “Quick Reference” one‑page summary** similar to GM screen but player‑facing (Outcome Matrix, Boon spending, Position, Fatigue/Harm, Magic DV).
3. **Witch Hunter appendix** – keep as optional expansion, but add a note that it’s GM‑dependent.

---

## Cross‑Sectional Consistency Fixes

- **Indexing:** Ensure every term in the index appears; run `makeindex`.
- **Cross‑references:** Use `\ref` and `\pageref` liberally (e.g., from Advancement to Legacy Engine).
- **Box styling:** Use `\begin{infobox}{Title}` for examples, `\begin{warningbox}` for common pitfalls, `\begin{fatebox}{Fate's Edge}` for philosophical asides.
- **Numbering:** Keep subsection numbers as they are but reorder content within subsections as described.

---

## Implementation Order (Player’s Guide)

1. **Start with Section 01** – add Session Zero and philosophy clarification.
2. **Section 02** – reorder core mechanics, add Boon spending encouragement.
3. **Section 03 (Magic)** – add Patron as co‑star, player advice for Obligation.
4. **Section 05 (XP Paths)** – add player archetypes and group synergy.
5. **Section 13 (Legacy Engine)** – add early pointers from other sections.
6. **Section 07/13/14 (Assets/Followers)** – consolidate and add investment guidance.
7. **Remaining sections** (04, 06, 08, 09, 10, 11, 12, 15, appendices) – apply targeted tweaks.
8. **Final pass:** Update all cross‑references and index entries.

This plan respects the existing file structure while making the Player’s Guide more actionable, player‑friendly, and better integrated with the GM Guide and SRD.
