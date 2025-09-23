-- Create clock reference table
CREATE TABLE IF NOT EXISTS clock_reference (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    segments INTEGER
);

-- Insert default clock references
INSERT OR IGNORE INTO clock_reference (name, segments) VALUES
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

