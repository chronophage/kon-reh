-- Create tables
CREATE TABLE IF NOT EXISTS users (
    userid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwordhash VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'player' CHECK (role IN ('player', 'gm')),
    createdat TIMESTAMP DEFAULT NOW(),
    lastlogin TIMESTAMP
);

CREATE TABLE IF NOT EXISTS characters (
    characterid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    userid UUID REFERENCES users(userid),
    name VARCHAR(100) NOT NULL,
    archetype VARCHAR(50),
    xptotal INTEGER DEFAULT 0,
    xpspent INTEGER DEFAULT 0,
    attributes JSONB,
    skills JSONB,
    followers JSONB,
    assets JSONB,
    talents JSONB,
    complications JSONB,
    boons INTEGER DEFAULT 0,
    lastupdated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS campaigns (
    campaignid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gmid UUID REFERENCES users(userid),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    players UUID[],
    status VARCHAR(10) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    createdat TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sessions (
    sessionid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaignid UUID REFERENCES campaigns(campaignid),
    date DATE,
    notes TEXT,
    attendance UUID[],
    xprewards JSONB,
    createdat TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_characters_userid ON characters(userid);
CREATE INDEX IF NOT EXISTS idx_campaigns_gmid ON campaigns(gmid);

-- Create tables
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    userid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwordhash VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'player' CHECK (role IN ('player', 'gm')),
    createdat TIMESTAMP DEFAULT NOW(),
    lastlogin TIMESTAMP
);

CREATE TABLE IF NOT EXISTS characters (
    characterid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    userid UUID REFERENCES users(userid),
    name VARCHAR(100) NOT NULL,
    archetype VARCHAR(50),
    xptotal INTEGER DEFAULT 0,
    xpspent INTEGER DEFAULT 0,
    attributes JSONB,
    skills JSONB,
    followers JSONB,
    assets JSONB,
    talents JSONB,
    complications JSONB,
    boons INTEGER DEFAULT 0,
    lastupdated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS campaigns (
    campaignid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gmid UUID REFERENCES users(userid),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    players UUID[] DEFAULT '{}',
    status VARCHAR(10) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    createdat TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sessions (
    sessionid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaignid UUID REFERENCES campaigns(campaignid),
    date DATE,
    notes TEXT,
    attendance UUID[] DEFAULT '{}',
    xprewards JSONB DEFAULT '[]',
    createdat TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_characters_userid ON characters(userid);
CREATE INDEX IF NOT EXISTS idx_campaigns_gmid ON campaigns(gmid);
CREATE INDEX IF NOT EXISTS idx_campaigns_players ON campaigns USING GIN(players);

-- Create tables
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    userid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwordhash VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'player' CHECK (role IN ('player', 'gm')),
    createdat TIMESTAMP DEFAULT NOW(),
    lastlogin TIMESTAMP
);

CREATE TABLE IF NOT EXISTS characters (
    characterid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    userid UUID REFERENCES users(userid),
    name VARCHAR(100) NOT NULL,
    archetype VARCHAR(50),
    xptotal INTEGER DEFAULT 0,
    xpspent INTEGER DEFAULT 0,
    attributes JSONB,
    skills JSONB,
    followers JSONB,
    assets JSONB,
    talents JSONB,
    complications JSONB,
    boons INTEGER DEFAULT 0,
    lastupdated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS campaigns (
    campaignid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gmid UUID REFERENCES users(userid),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    players UUID[] DEFAULT '{}',
    status VARCHAR(10) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    createdat TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sessions (
    sessionid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaignid UUID REFERENCES campaigns(campaignid),
    date DATE,
    notes TEXT,
    attendance UUID[] DEFAULT '{}',
    xprewards JSONB DEFAULT '[]',
    createdat TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS roll_history (
    rollid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    userid UUID REFERENCES users(userid),
    characterid UUID REFERENCES characters(characterid),
    pool INTEGER NOT NULL,
    descriptionlevel VARCHAR(20) DEFAULT 'Basic' CHECK (descriptionlevel IN ('Basic', 'Detailed', 'Intricate')),
    dice INTEGER[] NOT NULL,
    successes INTEGER NOT NULL,
    complications INTEGER NOT NULL,
    notes TEXT,
    rolledat TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_characters_userid ON characters(userid);
CREATE INDEX IF NOT EXISTS idx_campaigns_gmid ON campaigns(gmid);
CREATE INDEX IF NOT EXISTS idx_campaigns_players ON campaigns USING GIN(players);
CREATE INDEX IF NOT EXISTS idx_roll_history_characterid ON roll_history(characterid);
CREATE INDEX IF NOT EXISTS idx_roll_history_userid ON roll_history(userid);
CREATE INDEX IF NOT EXISTS idx_roll_history_rolledat ON roll_history(rolledat);

-- Create tables
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    userid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwordhash VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'player' CHECK (role IN ('player', 'gm')),
    createdat TIMESTAMP DEFAULT NOW(),
    lastlogin TIMESTAMP
);

CREATE TABLE IF NOT EXISTS characters (
    characterid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    userid UUID REFERENCES users(userid),
    name VARCHAR(100) NOT NULL,
    archetype VARCHAR(50),
    xptotal INTEGER DEFAULT 0,
    xpspent INTEGER DEFAULT 0,
    attributes JSONB,
    skills JSONB,
    followers JSONB,
    assets JSONB,
    talents JSONB,
    complications JSONB,
    boons INTEGER DEFAULT 0,
    lastupdated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS campaigns (
    campaignid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gmid UUID REFERENCES users(userid),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    players UUID[] DEFAULT '{}',
    status VARCHAR(10) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    createdat TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sessions (
    sessionid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaignid UUID REFERENCES campaigns(campaignid),
    date DATE,
    notes TEXT,
    attendance UUID[] DEFAULT '{}',
    xprewards JSONB DEFAULT '[]',
    createdat TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS roll_history (
    rollid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    userid UUID REFERENCES users(userid),
    characterid UUID REFERENCES characters(characterid),
    pool INTEGER NOT NULL,
    descriptionlevel VARCHAR(20) DEFAULT 'Basic' CHECK (descriptionlevel IN ('Basic', 'Detailed', 'Intricate')),
    dice INTEGER[] NOT NULL,
    successes INTEGER NOT NULL,
    complications INTEGER NOT NULL,
    notes TEXT,
    rolledat TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS macros (
    macroid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    userid UUID REFERENCES users(userid),
    campaignid UUID REFERENCES campaigns(campaignid),
    name VARCHAR(50) NOT NULL,
    command TEXT NOT NULL,
    description TEXT,
    ispublic BOOLEAN DEFAULT false,
    isapproved BOOLEAN DEFAULT false,
    createdat TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_messages (
    message

-- Add googleid column to users table (run this in your init.sql or as a migration)
ALTER TABLE users
ADD COLUMN IF NOT EXISTS googleid VARCHAR(255) UNIQUE,
ADD COLUMN IF NOT EXISTS avatar TEXT;

-- Add index for better performance
CREATE INDEX IF NOT EXISTS idx_users_googleid ON users(googleid);

