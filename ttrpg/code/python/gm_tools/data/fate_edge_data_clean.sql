-- fate_edge_data_clean.sql

-- Create consequence descriptors table
CREATE TABLE IF NOT EXISTS consequence_descriptors (
    id INTEGER PRIMARY KEY,
    suit TEXT,
    rank TEXT,
    domain TEXT,
    severity TEXT
);

-- Insert consequence descriptors
INSERT INTO consequence_descriptors (suit, rank, domain, severity) VALUES
-- Hearts (Emotional/Social)
('Hearts', '2-5', 'Emotional / Social fallout', 'Minor inconvenience or flavor complication'),
('Hearts', '6-10', 'Emotional / Social fallout', 'Moderate setback with some narrative teeth'),
('Hearts', 'J-K', 'Emotional / Social fallout', 'Significant consequence altering the course of action'),
('Hearts', 'Ace', 'Emotional / Social fallout', 'Catastrophic turn; reshapes narrative or mission goal'),

-- Diamonds (Resource/Wealth)
('Diamonds', '2-5', 'Resource / Wealth loss', 'Minor inconvenience or flavor complication'),
('Diamonds', '6-10', 'Resource / Wealth loss', 'Moderate setback with some narrative teeth'),
('Diamonds', 'J-K', 'Resource / Wealth loss', 'Significant consequence altering the course of action'),
('Diamonds', 'Ace', 'Resource / Wealth loss', 'Catastrophic turn; reshapes narrative or mission goal'),

-- Clubs (Physical harm/Obstacles)
('Clubs', '2-5', 'Physical harm / Obstacles', 'Minor inconvenience or flavor complication'),
('Clubs', '6-10', 'Physical harm / Obstacles', 'Moderate setback with some narrative teeth'),
('Clubs', 'J-K', 'Physical harm / Obstacles', 'Significant consequence altering the course of action'),
('Clubs', 'Ace', 'Physical harm / Obstacles', 'Catastrophic turn; reshapes narrative or mission goal'),

-- Spades (Mystical/Narrative)
('Spades', '2-5', 'Mystical / Narrative twists', 'Minor inconvenience or flavor complication'),
('Spades', '6-10', 'Mystical / Narrative twists', 'Moderate setback with some narrative teeth'),
('Spades', 'J-K', 'Mystical / Narrative twists', 'Significant consequence altering the course of action'),
('Spades', 'Ace', 'Mystical / Narrative twists', 'Catastrophic turn; reshapes narrative or mission goal');

-- Create NPC descriptors table
CREATE TABLE IF NOT EXISTS npc_descriptors (
    id INTEGER PRIMARY KEY,
    category TEXT,
    suit TEXT,
    rank TEXT,
    description TEXT,
    hook_suggestion TEXT
);

-- Insert NPC descriptors
INSERT INTO npc_descriptors (category, suit, rank, description, hook_suggestion) VALUES
-- Ambition (Hearts)
('Ambition', 'Hearts', '2', 'Acquire wealth', 'Desperate gambler, hoarder, thief'),
('Ambition', 'Hearts', '3', 'Gain prestige', 'Climbing hierarchy, faking noble blood'),
('Ambition', 'Hearts', '4', 'Secure power', 'Aims to control guild, militia, shrine'),
('Ambition', 'Hearts', '5', 'Discover truth', 'Hunts ancient ruins, pries into secrets'),
('Ambition', 'Hearts', '6', 'Protect someone/something', 'Bodyguard, sacred relic keeper'),
('Ambition', 'Hearts', '7', 'Destroy rival', 'Scheming, poisoning, hiring assassins'),
('Ambition', 'Hearts', '8', 'Escape obligation', 'Draft-dodger, runaway betrothed'),
('Ambition', 'Hearts', '9', 'Build legacy', 'Starting dynasty, monument, or school'),
('Ambition', 'Hearts', '10', 'Serve cause', 'Religious zealot, political revolutionary'),
('Ambition', 'Hearts', 'Jack', 'Pursue love', 'Entangled romance, doomed affair'),
('Ambition', 'Hearts', 'Queen', 'Seek revenge', 'Cold calculation, sudden violence'),
('Ambition', 'Hearts', 'King', 'Master a craft', 'Genius artisan, perfectionist'),
('Ambition', 'Hearts', 'Ace', 'Transcend mortality', 'Cultist, lich-aspirant, philosopher'),

-- Beliefs (Clubs)
('Beliefs', 'Clubs', '2', 'Pragmatism', 'Ends justify means'),
('Beliefs', 'Clubs', '3', 'Honor', 'Bound by oath or tradition'),
('Beliefs', 'Clubs', '4', 'Faith', 'Trust in divine, prophecy, or fate'),
('Beliefs', 'Clubs', '5', 'Rationalism', 'Demands proof, loves logic'),
('Beliefs', 'Clubs', '6', 'Hedonism', 'Pleasure first, consequences later'),
('Beliefs', 'Clubs', '7', 'Communalism', 'Group over individual'),
('Beliefs', 'Clubs', '8', 'Libertarianism', 'Freedom above all'),
('Beliefs', 'Clubs', '9', 'Fatalism', '"It is already written"'),
('Beliefs', 'Clubs', '10', 'Idealism', 'Believes world can be better'),
('Beliefs', 'Clubs', 'Jack', 'Cynicism', 'Distrusts everyone and everything'),
('Beliefs', 'Clubs', 'Queen', 'Self-determinism', 'Only I decide my path'),
('Beliefs', 'Clubs', 'King', 'Supremacism', 'One group or idea is superior'),
('Beliefs', 'Clubs', 'Ace', 'Paradoxical', 'Holds contradictory beliefs at once'),

-- Personality (Diamonds)
('Personality', 'Diamonds', '2', 'Cheerful', 'Disarms with optimism'),
('Personality', 'Diamonds', '3', 'Brooding', 'Always in shadow'),
('Personality', 'Diamonds', '4', 'Pompous', 'Full of grandeur'),
('Personality', 'Diamonds', '5', 'Humble', 'Soft-spoken, self-effacing'),
('Personality', 'Diamonds', '6', 'Cunning', 'Always scheming'),
('Personality', 'Diamonds', '7', 'Naive', 'Earnest, easily duped'),
('Personality', 'Diamonds', '8', 'Ruthless', 'Cold efficiency'),
('Personality', 'Diamonds', '9', 'Charming', 'Social magnet, honeyed words'),
('Personality', 'Diamonds', '10', 'Stoic', 'Unreadable, unflinching'),
('Personality', 'Diamonds', 'Jack', 'Erratic', 'Wild mood swings'),
('Personality', 'Diamonds', 'Queen', 'Nurturing', 'Maternal, protective'),
('Personality', 'Diamonds', 'King', 'Commanding', 'Projects authority'),
('Personality', 'Diamonds', 'Ace', 'Masked', 'Persona hides true face'),

-- Twist (Spades)
('Twist', 'Spades', '2', 'Debt', 'Owes someone dangerous'),
('Twist', 'Spades', '3', 'Betrayer', 'Will eventually turn on allies'),
('Twist', 'Spades', '4', 'Doomed', 'Prophecy or sickness awaits'),
('Twist', 'Spades', '5', 'Impostor', 'Not who they say they are'),
('Twist', 'Spades', '6', 'Haunted', 'Spirit, trauma, or guilt follows them'),
('Twist', 'Spades', '7', 'Pawn', 'Controlled by stronger hand'),
('Twist', 'Spades', '8', 'Double-life', 'Upright citizen + criminal underworld'),
('Twist', 'Spades', '9', 'Cursed', 'Literal or metaphorical affliction'),
('Twist', 'Spades', '10', 'Obsessed', 'Consumed by one idea'),
('Twist', 'Spades', 'Jack', 'Incompetent', 'Overestimates own ability'),
('Twist', 'Spades', 'Queen', 'Sympathetic flaw', 'Their vice endears them'),
('Twist', 'Spades', 'King', 'Secret noble/bloodline', 'Raises stakes'),
('Twist', 'Spades', 'Ace', 'Wild card', 'GM improvises unpredictable element');

-- Create adventure descriptors table
CREATE TABLE IF NOT EXISTS adventure_descriptors (
    id INTEGER PRIMARY KEY,
    category TEXT,
    suit TEXT,
    rank TEXT,
    description TEXT
);

-- Insert adventure descriptors
INSERT INTO adventure_descriptors (category, suit, rank, description) VALUES
-- Places (Spades)
('Place', 'Spades', '2', 'Toll bridge at a foggy ford'),
('Place', 'Spades', '3', 'Abandoned location, squatters within'),
('Place', 'Spades', '4', 'Wilderness path marked by strange cairns'),
('Place', 'Spades', '5', 'Lonely inn with too few patrons'),
('Place', 'Spades', '6', 'Old quarry turned smugglers'' pit'),
('Place', 'Spades', '7', 'Overgrown orchard or vineyard hiding a shrine'),
('Place', 'Spades', '8', 'Border outpost, undermanned and tense'),
('Place', 'Spades', '9', 'Collapsed mine, faint chanting below'),
('Place', 'Spades', '10', 'Fortress granary with suspicious activity'),
('Place', 'Spades', 'Jack', 'City undercroft used by syndicates'),
('Place', 'Spades', 'Queen', 'Island cloister where tides conceal secrets'),
('Place', 'Spades', 'King', 'High keep overlooking three borders'),
('Place', 'Spades', 'Ace', 'Sealed under-vault that hums at night'),

-- People/Factions (Hearts)
('People', 'Hearts', '2', 'Wary farmer seeking protection'),
('People', 'Hearts', '3', 'Young patrol captain seeking a break'),
('People', 'Hearts', '4', 'Ambitious scribe angling for promotion'),
('People', 'Hearts', '5', 'Traveling merchant juggling debts'),
('People', 'Hearts', '6', 'Sectarian monk with hidden doubts'),
('People', 'Hearts', '7', 'Temple advocate torn between creeds'),
('People', 'Hearts', '8', 'Caravan mistress guarding a secret cargo'),
('People', 'Hearts', '9', 'Disgraced noble clinging to relevance'),
('People', 'Hearts', '10', 'Guild factor balancing ledgers and lies'),
('People', 'Hearts', 'Jack', 'Street gang leader with local sway'),
('People', 'Hearts', 'Queen', 'Exiled courtier with dangerous friends'),
('People', 'Hearts', 'King', 'Kahfagian commodore off the books'),
('People', 'Hearts', 'Ace', '"Benefactor" whose money moves borders'),

-- Complications/Threats (Clubs)
('Complication', 'Clubs', '2', 'Slippery mudslide blocks the way'),
('Complication', 'Clubs', '3', 'Bad weather ruins supplies'),
('Complication', 'Clubs', '4', 'Hidden snare line across the approach'),
('Complication', 'Clubs', '5', 'Distracted allies miss a cue'),
('Complication', 'Clubs', '6', 'A rival party races you to the goal'),
('Complication', 'Clubs', '7', 'Local law arrives at the worst time'),
('Complication', 'Clubs', '8', 'Beast attack; mundane but dangerous'),
('Complication', 'Clubs', '9', 'Your plan leaks; ambush in the wings'),
('Complication', 'Clubs', '10', 'Magical hazard: wards failing, curses flaring'),
('Complication', 'Clubs', 'Jack', 'Insider betrayal during the action'),
('Complication', 'Clubs', 'Queen', 'Ally-of-convenience turns on you'),
('Complication', 'Clubs', 'King', 'Entire faction shifts allegiance mid-scene'),
('Complication', 'Clubs', 'Ace', 'The past returns to claim someone'),

-- Rewards/Leverage (Diamonds)
('Reward', 'Diamonds', '2', 'Trinket or token worth 1 Boon'),
('Reward', 'Diamonds', '3', 'Favor marker from a minor official'),
('Reward', 'Diamonds', '4', 'Small cache of supplies (1 free Supply segment)'),
('Reward', 'Diamonds', '5', 'Local renown; 1 Boon usable in this region'),
('Reward', 'Diamonds', '6', 'Pouch of coin; enough to offset upkeep once'),
('Reward', 'Diamonds', '7', 'Access to training: reduce XP cost of 1 skill by 1'),
('Reward', 'Diamonds', '8', 'A Cap 2 follower offers service'),
('Reward', 'Diamonds', '9', 'A minor holding (workshop, stall, shack)'),
('Reward', 'Diamonds', '10', 'Letters of credit with a guild (worth 2 Boons)'),
('Reward', 'Diamonds', 'Jack', 'Blackmail dossier (usable as leverage)'),
('Reward', 'Diamonds', 'Queen', 'Land deed or minor title (Asset)'),
('Reward', 'Diamonds', 'King', 'Noble charter or mercantile license (Standard Asset)'),
('Reward', 'Diamonds', 'Ace', 'Artifact-grade leverage (4 XP to keep)');

-- Create clock reference table
CREATE TABLE IF NOT EXISTS clock_reference (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    segments INTEGER
);

-- Insert clock reference data
INSERT INTO clock_reference (name, segments) VALUES
('Action / Task', 4),
('Stealth / Alert / Heat', 4),
('Recovery / Healing', 4),
('Resource Depletion', 4),
('Environmental Hazard', 6),
('Investigation / Cluework', 6),
('Negotiation / Social Contest', 6),
('Travel / Journey Leg', 6),
('Craft / Research / Downtime Project', 6),
('Trace / Manhunt / Security Response', 6),
('Threat / Boss (single phase)', 8),
('Heist Layer / Access', 8),
('Countdown / Doom / Catastrophe', 8),
('Setpiece Objective', 8),
('Faction Progress / Territory Shift', 8),
('Relationship / Trust / Influence', 6),
('Major Project / Arc Goal', 12),
('Campaign-Level Change', 12);

-- Add to your SQL file
CREATE TABLE IF NOT EXISTS cp_spend_menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cp_cost INTEGER NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Insert the (SB) spend options
INSERT OR IGNORE INTO cp_spend_menu (cp_cost, category, description) VALUES
(1, 'Universal', 'Noise, tell, or trace left; +1 segment on the party Supply clock; a tool or item becomes Compromised; +1 round of time passes; a bystander notices something off.'),
(1, 'Combat', 'Lose footing (next defense -1d).'),
(1, 'Stealth', 'Footstep/squeak; shadow seen.'),
(2, 'Universal', 'Alarmed attention (not full alarm); lose position/cover; add a lesser foe or lock; advance a Threat clock by 1; traveler gains Fatigue 1.'),
(2, 'Combat', 'Weapon or gear becomes Compromised.'),
(2, 'Stealth', 'Patrol pattern changes; lock resists (extra test).'),
(3, 'Universal', 'Reinforcements en route; Out of Supply; key gear breaks now; split the party''s options (e.g., fire, flood, collapse); escalate a faction clock by 1.'),
(3, 'Combat', 'Pinned, disarmed, or separated; battlefield shifts (fireline, cave-in, cavalry arrives).'),
(3, 'Stealth', 'Partial alarm (search begins).'),
(4, 'Universal', 'Major turn: trap springs, rival claims the prize first, authority arrives with mandate; convert saved (SB) into a scene-defining twist (one big thing, not many small).'),
(4, 'Social', 'Patron turns, audience turns; binding oath invoked.'),
(4, 'Stealth', 'Full alarm and lockdown protocol.');

-- Player character tracking
CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name TEXT,
    fatigue INTEGER DEFAULT 0,
    supply_segments INTEGER DEFAULT 0
);

-- Campaign tracking
CREATE TABLE campaign_clocks (
    id INTEGER PRIMARY KEY,
    mandate INTEGER DEFAULT 0,
    crisis INTEGER DEFAULT 0,
    primary_clock INTEGER DEFAULT 0
);

-- Evidence tracking
CREATE TABLE evidence (
    id INTEGER PRIMARY KEY,
    description TEXT,
    type TEXT, -- 'Immaculate' or 'Scorched'
    scene_id INTEGER
);


