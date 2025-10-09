// Fate's Edge - Complete Implementation
// Version 1.0 - All Features Integrated

const FateEdgeComplete = (() => {
    'use strict';
    
    // ==================== CORE SYSTEM ====================
    
    const initialize = () => {
        log("Fate's Edge Complete System Initializing...");
        registerEventHandlers();
        createDefaultSettings();
        log("Fate's Edge Complete System Ready!");
    };
    
    const registerEventHandlers = () => {
        on('chat:message', handleChatMessage);
        on('change:attribute', handleAttributeChange);
        on('add:repeating_skill', handleSkillAdd);
        on('destroy:repeating_skill', handleSkillRemove);
    };
    
    const createDefaultSettings = () => {
        // Create campaign-level settings
        state.fateEdge = state.fateEdge || {
            campaignClocks: {},
            activeTravels: {},
            prestigeAbilities: {},
            deckCache: {}
        };
    };
    
    // ==================== CORE MECHANICS ====================
    
    const CoreMechanics = {
        rollChallenge: (pool, position, description, roller) => {
            const rolls = [];
            for (let i = 0; i < pool; i++) {
                rolls.push(randomInteger(10));
            }
            
            const successes = rolls.filter(r => r >= 6).length;
            const sbGenerated = rolls.filter(r => r === 1).length;
            
            const result = CoreMechanics.determineOutcome(successes, sbGenerated, position);
            
            return {
                rolls: rolls,
                successes: successes,
                sbGenerated: sbGenerated,
                result: result,
                position: position,
                description: description,
                roller: roller
            };
        },
        
        determineOutcome: (successes, sbGenerated, position) => {
            if (successes === 0) return "Miss - No progress";
            if (sbGenerated === 0 && successes > 0) return "Clean Success";
            if (sbGenerated > 0 && successes > 0) return "Success with Cost";
            if (successes > 0) return "Partial Success";
            return "Complication";
        },
        
        handleDescriptionLadder: (descriptionType, baseRoll) => {
            switch(descriptionType) {
                case 'Basic':
                    return baseRoll;
                case 'Detailed':
                    // Re-roll one 1
                    return baseRoll.map(die => die === 1 ? randomInteger(10) : die);
                case 'Intricate':
                    // Re-roll all 1s
                    return baseRoll.map(die => die === 1 ? randomInteger(10) : die);
                default:
                    return baseRoll;
            }
        }
    };
    
    // ==================== RESOURCE TRACKING ====================
    
    const ResourceTracker = {
        updateBoonLimit: (characterId) => {
            const boonCount = getAttrByName(characterId, 'boon_count') || 0;
            if (boonCount > 5) {
                setAttrByName(characterId, 'boon_count', 5);
                sendChat('FateEdge', `/w gm ${getCharName(characterId)} Boons automatically capped at 5`);
            }
        },
        
        handleSceneTransition: (partyCharacters) => {
            partyCharacters.forEach(charId => {
                const currentBoons = getAttrByName(charId, 'boon_count') || 0;
                if (currentBoons > 2) {
                    setAttrByName(charId, 'boon_count', 2);
                    sendChat('FateEdge', `/w gm ${getCharName(charId)} Boons trimmed to 2 for scene transition`);
                }
            });
        },
        
        convertBoonsToXP: (characterId) => {
            const currentBoons = getAttrByName(characterId, 'boon_count') || 0;
            const sessionXP = getAttrByName(characterId, 'session_xp_converted') || 0;
            
            if (currentBoons >= 2 && sessionXP < 2) {
                setAttrByName(characterId, 'boon_count', currentBoons - 2);
                setAttrByName(characterId, 'xp', (getAttrByName(characterId, 'xp') || 0) + 1);
                setAttrByName(characterId, 'session_xp_converted', sessionXP + 1);
                return true;
            }
            return false;
        },
        
        manageFatigue: (characterId, fatigueChange) => {
            const currentFatigue = getAttrByName(characterId, 'fatigue_count') || 0;
            const body = getAttrByName(characterId, 'body') || 1;
            const newFatigue = Math.max(0, currentFatigue + fatigueChange);
            
            if (newFatigue > body) {
                // Convert excess fatigue to harm
                const excess = newFatigue - body;
                setAttrByName(characterId, 'fatigue_count', 0);
                ResourceTracker.applyHarm(characterId, excess);
                return { converted: true, harmLevel: excess };
            } else {
                setAttrByName(characterId, 'fatigue_count', newFatigue);
                return { converted: false };
            }
        },
        
        applyHarm: (characterId, harmLevel) => {
            const currentHarm = getAttrByName(characterId, `harm_${harmLevel}`) || 0;
            if (currentHarm === 0) {
                setAttrByName(characterId, `harm_${harmLevel}`, 1);
                return true;
            }
            return false;
        }
    };
    
    // ==================== DECK SYSTEM ====================
    
    const TravelRegions = {
    'Acasia': {
        name: 'Broken Marches',
        suits: {
            'Spade': 'Places (passes, ruins, blackwoods, toll-towns)',
            'Heart': 'People & Factions (petty crowns, priests, companies)',
            'Club': 'Complications (feud, levy, weather, curse)',
            'Diamond': 'Rewards (papers, claims, safe-conduct)'
        },
        cards: {
            'Spade': ['Broken milestone', 'Vine-terrace hillside', 'Toll-bridge town', 'Wolfstairs Pass', 'Sootfall Abbey ruins', 'Hill-motte', 'Border-stone ring', 'Blackwood hollow', 'Salt-road ford', 'Iron mine adits', 'Margravine\'s lodge', 'War-camp city', 'Pale Causeway'],
            'Heart': ['Tithe-collector', 'Roadside prior', 'Hedge-witch', 'Free Company captain', 'River reeve', 'Salt-Baron', 'Blackwood matriarch', 'Ex-imperial surveyor', 'King of villages', 'Bride with no dowry', 'Margravine', 'Lame King', 'Cursed Child'],
            'Club': ['Peat-fog', 'Sudden levy', 'Bridge feud', 'Grain blight', 'Scree slide', 'Wedding ambush', 'Witch\'s tithe', 'Pox sign', 'Condotta breaks', 'Heretic preacher', 'Imperial pretender', 'River overrun', 'Curse stirs'],
            'Diamond': ['Toll-exemption plaque', 'Monastery letter', 'Wine-right', 'Condotta', 'Tithe-remission writ', 'Border-stone adjustment', 'Pass-key charm', 'Sealed dowry chest', 'Mine-share', 'Blood-peace charter', 'Marriage proxy', 'Lame King\'s writ', 'Curse-redemption rite']
        },
        specialRules: 'Curse motifs; every Ace adds a lingering omen'
    },
    
    'Aelaerem': {
        name: 'Hearth & Hollow',
        suits: {
            'Spade': 'Places (lanes, orchards, mills, downs, barrows)',
            'Heart': 'People & Factions (keepers, elders, mummers, quiet powers)',
            'Club': 'Complications (folk omens, rites, beasts, night)',
            'Diamond': 'Rewards (blessings, tokens, host-rights, exceptions)'
        },
        cards: {
            'Spade': ['Willow ford', 'Cider-press barn', 'Chalk sheep-downs', 'Millpond', 'Bluebell wood path', 'Hedge-tunnel lane', 'Cup-mark stone', 'Barrow-by-the-beech', 'Market green', 'Dovecote hill', 'Mother\'s Orchard', 'Moot Oak', 'Hollow Field'],
            'Heart': ['Hedge-witch midwife', 'Miller', 'Orchard reeve', 'Beekeeper', 'Shepherd', 'Lantern-warden', 'Mummers\' captain', 'Traveling tinker', 'Bailiff', 'Wold-Wardens', 'Apple-Matron', 'Thresher-King', 'Pale Shepherd'],
            'Club': ['Unseasonal fog', 'Scarecrow turns', 'Soured wassail', 'Black sow', 'Hive-swarm', 'Old song', 'Lanterns burn blue', 'Out-of-season mumming', 'Chalk maze', 'Church bell rings', 'Harvest tithe', 'Moot Oak bleeds', 'Hollow opens'],
            'Diamond': ['Guest-loaf & salt', 'Cider-mark', 'Hedge-pass ribbon', 'Bee-queen share', 'Shepherd\'s whistle', 'Lantern-writ', 'Mummers\' license', 'Orchard right', 'Mill token', 'Apple-Matron\'s blessing', 'Private moot', 'Thresher-King\'s guard', 'Pale Shepherd\'s clause']
        },
        specialRules: 'Red-thread motifs; Ace echoes quiet bells/watch-geese'
    },
    
    'Aeler': {
        name: 'Crowns & Under-Vaults',
        suits: {
            'Spade': 'Places (vaultmouths, descents, underways, crown seats)',
            'Heart': 'People & Factions (crowns, keepers, guilds, legates)',
            'Club': 'Complications (air, water, stone, rite, jurisdiction)',
            'Diamond': 'Rewards (keys, passes, breath, priority, precedent)'
        },
        cards: {
            'Spade': ['Vaultmouth Gate', 'Crown-Crypt Porch', 'Under-Market', 'Smoke-Shaft Stair', 'Gloam Cistern', 'Lamplighter\'s Mile', 'Measure Vault', 'Reliquary Arcade', 'Twin-Throne Gate', 'Deep Archive', 'Queen\'s Descent', 'Kingsmoot Cavern', 'Spine Underway'],
            'Heart': ['Lamplighter apprentice', 'Under-Mason', 'Vault Warden', 'Censer-Knight', 'Key-Sister', 'Under-Market assessor', 'Engineer', 'Oath-Keeper', 'Legate', 'White-Ribbon courier', 'Vault-Queen', 'High King', 'Lumenor'],
            'Club': ['Bad air pocket', 'Drip-flood', 'Gas flare', 'Seal misread', 'Under-mold quarantine', 'Settling crack', 'Stolen key', 'Bell-code conflict', 'Vault-right feud', 'Cave-in', 'Heresy inquest', 'General Under-Seal', 'White Flood'],
            'Diamond': ['Lamp-priority tally', 'Breath-measure allotment', 'Key-Writ', 'Underway Pass', 'Stall-Right', 'Engineer Shoring', 'Assay Mark', 'Crypt Asylum', 'Vault Inventory', 'Under-Guard', 'Private Descent', 'High King\'s Writ', 'Under-Seal Clause']
        },
        specialRules: 'Stone/breath motifs; Ace keys click, bells answer'
    },
    
    'Aelinnel': {
        name: 'Stone, Bough, and Bright Things',
        suits: {
            'Spade': 'Places (stone spires, sea-rock, deep woods)',
            'Heart': 'People & Factions (keepers, courts, craftsmen, hunters)',
            'Club': 'Complications (glamour, geasa, weather, neighbors)',
            'Diamond': 'Rewards (charms, passes, host-rights, exceptions)'
        },
        cards: {
            'Spade': ['Tide-rift steps', 'Moonwell basin', 'Dolmen stair', 'Charcoal coppice', 'Basalt organ cliffs', 'Stag Road', 'Quartz spring', 'Elf-causey', 'Root gallery', 'Barrow gallery', 'Thorn Court ring', 'Hall of Aelinnel', 'Green Gate'],
            'Heart': ['Goat-herd', 'Charcoal-burner', 'Hedge-witch', 'Stone-singer', 'Forester-warden', 'Reed-net fisher', 'Oath-carver', 'Way-keeper', 'Green-market broker', 'Green Knight', 'Lady of Thorns', 'Stone Prince', 'Huntsman'],
            'Club': ['Glamour fog', 'Iron offense', 'Root-slide', 'Wrong tide', 'Spoken geas', 'Green Market price', 'Stone-wight', 'Lost day', 'Thorn blight', 'Stag horn', 'Thorn Court tithe', 'Muster of Bough', 'Green Gate yawns'],
            'Diamond': ['Hazel token', 'Salt license', 'Dolmen carving', 'Guest-bough', 'Quarry allotment', 'Green Market voucher', 'Oath-bead', 'Tide-path key', 'Forest truce', 'Green Knight escort', 'Private audience', 'Stone Prince\'s seal', 'Wild Hunt clemency']
        },
        specialRules: 'Moonlight motifs; Ace adds a shortcut where none should be'
    },
    
    'BlackBanners': {
        name: 'Condotta & Crowns',
        suits: {
            'Spade': 'Places (camps, battlefields, fortresses, war-roads)',
            'Heart': 'People & Factions (captains, cadets, clans, tribes)',
            'Club': 'Complications (betrayals, weather, politics, war)',
            'Diamond': 'Rewards (contracts, claims, dispensations)'
        },
        cards: {
            'Spade': ['Burned village', 'Frozen ford', 'Latrine row', 'Crater pasture', 'Supply road', 'Siege tower', 'Salt-cured cache', 'Command tent', 'Watch-tower', 'Ancient march-keep', 'Bone Fields', 'Marcher\'s Fortress', 'Singing Wastes'],
            'Heart': ['Young cadet', 'Veteran sergeant', 'Banner-captain', 'Condotta broker', 'Ykrul emissary', 'Vilikari war-chief', 'Surgeon', 'Quartermaster', 'Tribune\'s aide', 'Black Colonel', 'Clan-Mother', 'High Chief', 'Bannerless One'],
            'Club': ['Payday delayed', 'False orders', 'Blizzard', 'Ykrul offer', 'Condotta unit flips', 'Camp-fever', 'Vilikari raiders', 'Honor vs. Pragmatism', 'Tribune captured', 'Black Colonel\'s banner', 'Clan-Mother\'s feast', 'High Chief\'s game', 'Singing Wastes awaken'],
            'Diamond': ['Emergency requisition', 'Dual contract', 'Honor dispensation', 'Condotta rider', 'Ykrul safe-conduct', 'Vilikari war-mark', 'Surgeon\'s debt-note', 'Tribune\'s cipher', 'Banner-captain\'s seal', 'Field promotion', 'Clan-Mother\'s braid', 'High Chief\'s charter', 'Bannerless Word']
        },
        specialRules: 'War & winter motifs; Ace: weapons remember, ice holds the dead'
    },
    
    'Ecktoria': {
        name: 'Marble & Fire',
        suits: {
            'Spade': 'Places (forums, arenas, roads, coin-houses)',
            'Heart': 'People & Factions (glory, law, pageant)',
            'Club': 'Complications (edicts, crowds, fault-lines)',
            'Diamond': 'Rewards (papers, favor, precedence)'
        },
        cards: {
            'Spade': ['Milk-stone steps', 'Tally-ford ferryhouse', 'Arena hypogeum', 'Everflame basilica', 'Shatterline bazaar', 'Coin-house floor', 'Surveyors\' Mile-Zero', 'Processional Way', 'Aqueduct arcades', 'Ducal loggia', 'Censor\'s Hall', 'Grand Forum', 'Imperial Arena'],
            'Heart': ['Torchbearer child', 'Ferrymaster', 'Coin-house factor', 'Lanista', 'Decumanus-master', 'Procession marshal', 'Grain-prefect', 'Censor\'s clerk', 'Veteran standard-bearer', 'Gladiatrix', 'Duchess-Regent', 'High Priest', 'Grand Magistrate'],
            'Club': ['Procession blocks', 'Sudden edict', 'Grain barges late', 'Arena riot', 'Rival dukes', 'Re-plat redraws', 'Coin-house calls', 'Inquisitorial visit', 'Aftershock', 'Counterfeit laurel', 'Church purge', 'Triumphal reroute', 'Red List'],
            'Diamond': ['Bread chit', 'Procession permit', 'Arena purse', 'Survey writ', 'Ducal safe-conduct', 'Coin-house credit', 'Magistrate\'s postponement', 'Laurel-deed', 'Grain allotment', 'Minor title', 'Basilica audience', 'Censor\'s indulgence', 'Golden Edict']
        },
        specialRules: 'Imperial forms; Ace carves precedent in marble'
    },
    
    'Kahfagia': {
        name: 'Pilot\'s Mirror',
        suits: {
            'Spade': 'Places (channels, lighthouses, pilot stations)',
            'Heart': 'People & Factions (pilots, admirals, merchants)',
            'Club': 'Complications (storms, reefs, jurisdiction)',
            'Diamond': 'Rewards (clearances, priority, safe passage)'
        },
        cards: {
            'Spade': ['Mirror channel', 'Lantern tower', 'Pilot station', 'Tide pool', 'Signal mast', 'Convoy harbor', 'Lighthouse rock', 'Navigation buoy', 'Shoal marker', 'Beacon chain', 'Admiral\'s anchorage', 'Mirror fleet', 'Infinite channel'],
            'Heart': ['Mirror pilot', 'Lantern keeper', 'Convoy master', 'Tide reader', 'Signal officer', 'Harbor master', 'Navigation scholar', 'Lantern-law clerk', 'Pilot\'s guildmaster', 'Admiral\'s aide', 'Mirror admiral', 'Lighthouse keeper', 'Infinite navigator'],
            'Club': ['Mirror fog', 'Channel shift', 'Reef migration', 'Lantern failure', 'Jurisdiction clash', 'Storm surge', 'Convoy scatter', 'Tide anomaly', 'Signal jam', 'Beacon fire', 'Admiral\'s court', 'Mirror breach', 'Infinite current'],
            'Diamond': ['Mirror clearance', 'Lantern priority', 'Pilot\'s token', 'Tide window', 'Signal pass', 'Harbor green', 'Navigation fix', 'Lantern writ', 'Convoy escort', 'Admiral\'s warrant', 'Mirror charter', 'Lighthouse beacon', 'Infinite passage']
        },
        specialRules: 'Lantern-law jurisdiction shifts; Ace redefines lanes'
    },
    
    'Linn': {
        name: 'Skerries & Storm-Oaths',
        suits: {
            'Spade': 'Places (fjords, skerries, halls, mistland routes)',
            'Heart': 'People & Factions (jarls, oar-crews, keepers, law)',
            'Club': 'Complications (weather, reefs, feud, pursuit)',
            'Diamond': 'Rewards (rights, tokens, escorts, priority)'
        },
        cards: {
            'Spade': ['Kelp-skerry gut', 'Tide-shed', 'Wave-gate reef', 'Runestone causey', 'Herring-stairs', 'Winter hall', 'Mistlands reed-maze', 'Boomed harbor', 'Aberderrin current', 'Dolmis waystation', 'Thing-holm', 'High Jarl\'s seat', 'Whale-road'],
            'Heart': ['Net-wife', 'Steersman', 'Shipwright', 'Oar-master', 'Mist-pilot', 'Skald', 'Shield-band', 'Foster-son', 'Thing-speaker', 'Sea-queen\'s hand', 'Sea-Queen', 'High Jarl', 'Volva'],
            'Club': ['Black squall', 'Fogfall', 'Chain up!', 'Levy clash', 'Keel-rot rumor', 'Feud token', 'Oath recalled', 'Mistlands miscount', 'Aberderrin race', 'Southron fire-pots', 'Thing injunction', 'General muster', 'Ground-sea'],
            'Diamond': ['Harbor-green mark', 'Oar-share', 'Pilot\'s token', 'Wharf-right', 'Salvage claim', 'Thing ruling', 'Raid-truce ribbon', 'Foster-bond', 'Herring allotment', 'Escort writ', 'Private audience', 'High Jarl\'s pennon', 'Storm-oath clause']
        },
        specialRules: 'Sea omens; Ace: horns on wind, white horses on swell'
    },
    
    'Mistlands': {
        name: 'Bells, Salt, and Breath',
        suits: {
            'Spade': 'Places (fens, levees, bell-lines, shoreworks)',
            'Heart': 'People & Factions (wardens, ferrymen, Aeler rule, neighbors)',
            'Club': 'Complications (undead, weather, law, neighbors)',
            'Diamond': 'Rewards (passes, seals, tokens, priority)'
        },
        cards: {
            'Spade': ['Reed-fen causey', 'Bell-Line levee', 'Ghost-ferry slip', 'Pall Watch-tower', 'Mist-chapel', 'Dead-cut canal', 'Drowned-copse', 'Fogmill ridge', 'Salt-pan terraces', 'Protectorate Fort-Stair', 'Witchlight Bridge', 'High-Mist Pass', 'Weeping Gate'],
            'Heart': ['Reed-cutter', 'Salt-monk', 'Bell-warden', 'Oath-ferryman', 'Lantern acolyte', 'Linn mist-pilot', 'Protectorate clerk', 'Shroud-diver', 'Direwood refugee', 'Fog-knight', 'Legate', 'Lord Warden', 'Mist-Seer'],
            'Club': ['Ground-mist', 'Witchlights', 'Ward-salt short', 'Wrong bell', 'Linn raid', 'Direwood moan', 'Valewood wind', 'Bell-line failure', 'Marsh-quake', 'Protectorate interdiction', 'Rite-purge', 'General alarm', 'Tide-mist'],
            'Diamond': ['Ward-salt allotment', 'Ferry token', 'Bell-key', 'Lantern writ', 'Exorcist\'s seal', 'Fog-beacon', 'Protectorate mark', 'Wraith-indemnity', 'Bone-field license', 'Refuge-right', 'Private audience', 'Warden\'s commission', 'Pall Indulgence']
        },
        specialRules: 'Breath/boundary motifs; Ace: bells answer across water'
    },
    
    'Silkstrand': {
        name: 'City of Bridges & Dyewater',
        suits: {
            'Spade': 'Places (bridges, canals, mills, counting floors)',
            'Heart': 'People & Factions (guilds, factors, crowns, crews)',
            'Club': 'Complications (flood, interdict, riot, curse)',
            'Diamond': 'Rewards (permits, seats, escorts, charters)'
        },
        cards: {
            'Spade': ['Mulberry garths', 'Filature hall', 'Redwater Dyeworks', 'Spindle Tower', 'Three-Queens Bridge', 'Salt Gate', 'Silk Exchange', 'Ropewalk sheds', 'Old Arsenal', 'Archivolt', 'Basilica', 'Palazzo', 'Flood-Stairs'],
            'Heart': ['Bobbin-runner', 'Mulberry steward', 'Foreign factor', 'Dyers\' Guildmistress', 'Bridge bailiff', 'Archivolt notary', 'Watch captain', 'Spinner-matron', 'Exchange caller', 'Night-boat smuggler', 'Matron', 'Lame King\'s envoy', 'Saint of Broken Warps'],
            'Club': ['Flood siren', 'Quarantine flag', 'Loom strike', 'Counterfeit seals', 'Bridge riot', 'Condottieri flip', 'Blackwood panic', 'Silk-fungus', 'Salt-tax doubled', 'Duel booked', 'Exchange corner', 'Procession', 'Curse wakes'],
            'Diamond': ['Bridge token', 'Dye-permit', 'Warehouse seal', 'Exchange pass', 'Watergate priority', 'Notarial indulgence', 'Wormhouse allotment', 'Ropewalk credit', 'Arsenal key', 'Condotta rider', 'Private audience', 'Tax-farm share', 'Golden Thread']
        },
        specialRules: 'Dye/bridge motifs; Ace adds a lingering omen'
    },
    
    'Theona': {
        name: 'Three Greens, No Ninth',
        suits: {
            'Spade': 'Places (ringforts, wells, cliffs, causeways)',
            'Heart': 'People & Factions (moots, keepers, courts, neighbors)',
            'Club': 'Complications (fog, feud, taboo, sea)',
            'Diamond': 'Rewards (blessings, tokens, rights, priority)'
        },
        cards: {
            'Spade': ['Basalt tide-stairs', 'Saint\'s Well', 'Fog-wick tower', 'Black Bog causeway', 'Cliff ringfort', 'Barrow field', 'Sea-cave harp', 'Uncounted Bridge', 'Ogham grove', 'Coracle harbor', 'Green Moot Hill', 'High Hall', 'Lookout'],
            'Heart': ['Peat-cutter', 'Well-keeper', 'Kelp-netter', 'Harp-satirist', 'Wick-warden', 'Taboo-witness', 'Island abbot', 'Green Neighbor', 'Coracle-captain', 'Bride-peacemaker', 'Matron', 'Three-Isles King', 'Lady Beneath'],
            'Club': ['Ground-mist', 'Bog-lights', 'Spoken geas', 'Salt-rot', 'Processions collide', 'Wave-count', 'Bone-judge', 'Ninth Law', 'Net-surge', 'Bride-theft', 'Exile returns', 'Green Host', 'Great Fog'],
            'Diamond': ['Well-blessing', 'Moot token', 'Harbor-green', 'Hawthorn pass', 'Bell-right', 'Coracle share', 'Ogham ruling', 'Unnumbered Right', 'Salt-cure', 'Bride-peace', 'Private moot', 'Whale-road', 'Green Favor']
        },
        specialRules: '"No Ninth" custom; Ace adds a telling omission'
    },
    
    'Thepyrgos': {
        name: 'City of a Thousand Stairs',
        suits: {
            'Spade': 'Places (towers, stairs, sea-walls, cisterns)',
            'Heart': 'People & Factions (archons, synod, guilds, watchers)',
            'Club': 'Complications (edicts, quakes, chains, wind)',
            'Diamond': 'Rewards (keys, rites, papers, priority)'
        },
        cards: {
            'Spade': ['Pilgrim\'s Stair', 'Tower Quarter', 'Chain-Harbor', 'Blue Cistern', 'Ropeyard Terrace', 'Storm-Wall Arcades', 'Beacon Crown', 'Library of Keys', 'Siege Foundry', 'Monastery', 'Synod Hall', 'Archon\'s Citadel', 'Sky-Bridge'],
            'Heart': ['Bell-runner', 'Master of Ropes', 'Icon-smith', 'Wall Strategos', 'Chain-keeper', 'Oath-examiner', 'Archive Sister', 'Salt-fish Syndic', 'Nomophylax', 'Palikar Captain', 'Matriarch', 'Archon', 'Lighthouse-Patriarch'],
            'Club': ['Tremor', 'Iconoclast riot', 'Chain jam', 'Black northerly', 'Cistern taint', 'Synod summons', 'Rope guild', 'Siege drill', 'Smugglers\' ladder', 'Ropeyard fire', 'Exarch\'s claim', 'General watch', 'Seaquake'],
            'Diamond': ['Stair token', 'Harbor pass', 'Cistern draw', 'Crane allotment', 'Icon license', 'Archive hour', 'Bellmark', 'Watchlight', 'Synod indulgence', 'Pronoia', 'Private audience', 'Archon\'s writ', 'Golden Key']
        },
        specialRules: 'Height/sound motifs; Ace echoes bells/wind/stair-steps'
    },
    
    'Ubral': {
        name: 'Stone Between Spears',
        suits: {
            'Spade': 'Places (tors, cairns, hill-forts, passes)',
            'Heart': 'People & Factions (clans, dwarves, reivers, law)',
            'Club': 'Complications (mist, feud, toll, weather)',
            'Diamond': 'Rewards (oaths, rights, tokens, priority)'
        },
        cards: {
            'Spade': ['Sheepwalk Ledge', 'Warden\'s Cairn', 'Wergild Ford', 'Droppers\' Bridge', 'Scree-Ladder', 'Moot Hollow', 'Reiver\'s Gate', 'Khaz-Vurim Steps', 'Grey Tor', 'Black Broom Bog', 'Bride\'s Causey', 'Three-Fires Ridge', 'Pass of Ashes'],
            'Heart': ['Hearth-aunt', 'Hill guide', 'Feud-broker', 'Reiver band', 'Watch-fire warden', 'Wergild counter', 'Dwarf road-warden', 'Oath-singer', 'Bride-carrier', 'Lady of the Tor', 'Council of Cairns', 'Stone-Speaker'],
            'Club': ['Upland mist', 'Feud rekindled', 'Bridge dropped', 'Black-rent', 'Wergild breach', 'Snow-squall', 'Dwarf toll hike', 'Cattle scatter', 'Watch-fire false', 'Bride-theft', 'Royal incursion', 'Clan muster', 'Hill-fall'],
            'Diamond': ['Guest-right', 'Guide\'s braid', 'Ford-tithe', 'Feud-peace', 'Bloom allotment', 'Watch-code', 'Vurim pass-ring', 'Bride-price', 'Hill-fort shelter', 'Oath-release', 'Council audience', 'Road-ward', 'Stone-Speaker\'s clause']
        },
        specialRules: 'Upland motifs; Ace echoes horns/heather/stone'
    },
    
    'Valewood': {
        name: 'Empire Under Leaves',
        suits: {
            'Spade': 'Places (phasing ruins, star-roads, living stone)',
            'Heart': 'People & Factions (Lethai-ar, fae, beast-kin, empire echoes)',
            'Club': 'Complications (glamour, ward-traps, imperial residue)',
            'Diamond': 'Rewards (charms, keys, truce-boughs, old rights)'
        },
        cards: {
            'Spade': ['Star-road shard', 'Rooted amphitheatre', 'Moon-cistern', 'Glyphed bridge', 'Glassleaf gallery', 'Hollow aqueduct', 'Calendar grove', 'Unfound arcade', 'City that Breathes', 'Amber ziggurat', 'Ivory observatory', 'Throne-bower', 'Valeheart Spire'],
            'Heart': ['Pathweaver', 'Fox-headed courier', 'Owl-sister', 'Antler-masked hunter', 'Moss-scribe', 'Lark-keeper', 'Green Neighbor', 'Warden-coterie', 'Echo-legionary', 'Shardwright', 'Hazel Queen', 'Alder King', 'Huntsman Between'],
            'Club': ['Sweet wind', 'Path reverses', 'Ward-trap', 'Oath-magnet', 'Geas catches', 'City phase', 'Name-theft', 'Ring claim', 'Mirror rain', 'Redcaps', 'Court tithe', 'Muster of Boughs', 'Empire wakes'],
            'Diamond': ['Way-cord', 'Dew-mirror', 'Hazel token', 'Honey-right', 'Name-bead', 'Wind-veil', 'City-key', 'Green truce', 'Oathsap', 'Shardwright\'s favor', 'Audience', 'Alder Writ', 'Valeheart Clause']
        },
        specialRules: 'Empire echoes (J/Q/K add relic-logic); Ace rearranges approach'
    },
    
    'Vhasia': {
        name: 'Fractured Sun',
        suits: {
            'Spade': 'Places (châteaux, cathedrals, forests, fairs, roads)',
            'Heart': 'People & Factions (lords, courts, companies, cloister)',
            'Club': 'Complications (chevauchée, law, church, weather)',
            'Diamond': 'Rewards (charters, patents, rights)'
        },
        cards: {
            'Spade': ['Wayside shrine', 'Vine-terraced clos', 'Bastide market', 'Royal Forest', 'Pont-du-Tithe', 'Great Fairground', 'Salt pans', 'Siege-scarred château', 'Cathedral works', 'Parlement Hall', 'Queen\'s Causeway', 'Sun Palace', 'King\'s High Road'],
            'Heart': ['Road warden', 'Vintner-guild', 'Abbess-chatelaine', 'Routier captain', 'Constable', 'Parlement clerk', 'Salt-farmer', 'Trouvère', 'Marshal', 'Heretic', 'Queen-Mother', 'Two Crowns', 'Last Dauphin'],
            'Club': ['Chevauchée', 'Interdict', 'Forest law', 'River in spate', 'Coin debasement', 'Parlement divided', 'Free-company', 'Relic dispute', 'Harvest blight', 'Tournament', 'Royalist', 'Feudal levy', 'Winter campaign'],
            'Diamond': ['Safe-conduct', 'Burgess charter', 'Bridge farm', 'Paréage', 'Wardship', 'Gabelle lease', 'Letters patent', 'Remission', 'Low-justice', 'Confiscation', 'Private audience', 'Sunburst Warrant', 'General Pardon']
        },
        specialRules: 'Broken-sun motifs; Ace blots medal/scratches milestone'
    },
    
    'Vilikari': {
        name: 'Laurels & Longhouses',
        suits: {
            'Spade': 'Places (march towns, villa-forts, old roads)',
            'Heart': 'People & Factions (federates, mixed courts, diaspora)',
            'Club': 'Complications (two laws, two fronts, old grudges)',
            'Diamond': 'Rewards (charters, rights, escorts, precedence)'
        },
        cards: {
            'Spade': ['Longhouse Quarter', 'Milefort XVII', 'Stone Ford', 'Villa Granary', 'Twin Court', 'Blackwood Road', 'Frontier Staple', 'Burial Field', 'Repaired Bridge', 'Hill-Palace', 'New Raivon', 'Dux\'s Palace', 'Foedus Stone'],
            'Heart': ['Hearth-Mother', 'Shield-Brother', 'March Notary', 'Horse-Reeve', 'Ykrul Envoy', 'Old Legionary', 'Ecktorian Factor', 'Kahfagian Pilot', 'Acasian Lord', 'War-Maiden', 'Queen of Marches', 'Federate King', 'Elder of Elders'],
            'Club': ['Annona late', 'Jurisdiction', 'Winter raid', 'Bridge levy', 'Succession feud', 'Foedus recall', 'Coin debasement', 'Grave offense', 'Port clash', 'Warband flips', 'Restoration', 'General levy', 'Spring melt'],
            'Diamond': ['Foedus Renewal', 'Mallus Right', 'Stipend', 'Roman Patent', 'Staple Right', 'Hostage Treaty', 'Remount', 'Wergild Table', 'Bridge Farm', 'Purple Warrant', 'Private Audience', 'Dux Commission', 'Great Law Day']
        },
        specialRules: 'Two-laws motifs; Ace shows wolf/eagle side-by-side'
    },
    
    'Viterra': {
        name: 'The Hedge-Law Realm',
        suits: {
            'Spade': 'Places (fens, dales, beacons, courts, Dolmis shore)',
            'Heart': 'People & Factions (reeves, guilds, knights, crown)',
            'Club': 'Complications (water, law, border-lace, weather)',
            'Diamond': 'Rewards (writs, charters, priority, labor)'
        },
        cards: {
            'Spade': ['Fen causeway', 'Hedgerow green', 'Beacon hill', 'Belworth ferry', 'Old quarry', 'Parish-stone maze', 'Fairport tideworks', 'Law Quarter', 'Tarlington fields', 'River dike', 'Valora Progress', 'Hall of Dawning', 'Queen\'s Highway'],
            'Heart': ['Fen reeve', 'River-carter', 'Parish surveyor', 'Quartermaster', 'Dales levy', 'Two-altars cleric', 'Fairport shipwright', 'Fenwood comptroller', 'Queen\'s Justiciar', 'Border routier', 'Warrior Queen', 'Crown in Council', 'Tarling-blood'],
            'Club': ['Dike breach', 'Feast-day clash', 'Quiet tolls', 'Counting-house', 'Border-lace', 'Isle moot', 'Delta spat', 'Routier arrears', 'Salt pinch', 'Dawn recall', 'Aberielist', 'Levy call', 'Dolmis gale'],
            'Diamond': ['Ferry priority', 'Dike-work', 'Market-day', 'Dawn escort', 'River-carter', 'Parish-map', 'Fairport seal', 'County Thing', 'Salt allotment', 'Wardship', 'Private audience', 'Ducal warrant', 'Coronation writ']
        },
        specialRules: 'Legacy, parishes, and final-stand themes'
    },
    
    'WaysBetween': {
        name: 'Spiritways & Veilways',
        suits: {
            'Spade': 'Places (paths, crossings, thresholds, waystations)',
            'Heart': 'People & Factions (wayfarers, spirits, dream-walkers)',
            'Club': 'Complications (veil-thin places, dream-bleed, wayward paths)',
            'Diamond': 'Rewards (true names, safe passages, waywisdom)'
        },
        cards: {
            'Spade': ['Mist-shrouded ford', 'Bone-lit corridor', 'Threshold arch', 'Spiral path', 'Bridge of whispers', 'Crossroads', 'Stone circle', 'Tunnel through memory', 'Staircase from fossil', 'Waystation', 'Junction', 'Long Mile', 'Thirteenth Milestone'],
            'Heart': ['Lost pilgrim', 'Toll-taker', 'Wayward spirit', 'Dream-merchant', 'Child-ghost', 'Wounded traveler', 'Merchant', 'Guide-dog', 'Pilgrim backwards', 'Ferryman', 'Road\'s Child', 'Keeper', 'Wayfinder'],
            'Club': ['Path loops back', 'Reality thins', 'Waymark points wrong', 'Dream-bleed', 'Toll demanded', 'Path splits', 'Gravity shifts', 'Time-sickness', 'Road remembers lies', 'Crossroads judgment', 'Memory-thief', 'Path That Should Not Be', 'Convergence Point'],
            'Diamond': ['Waymark', 'Token of passage', 'Dream-catcher', 'Truth-compass', 'Memory-anchor', 'Safe-haven', 'Guide-light', 'Path-shortener', 'Debt-clearing', 'Crossroads boon', 'Way-wisdom', 'Passage of Grace', 'Road\'s Own Name']
        },
        specialRules: 'Reskin palette for any biome'
    },
    
    'Wilds': {
        name: 'Roads, Ruins, and Weather',
        suits: {
            'Spade': 'Places (crossings, lookouts, old roads, shelters)',
            'Heart': 'People & Factions (foragers, guides, wardens, caravans)',
            'Club': 'Complications (weather, doublebacks, prowlers, blocks)',
            'Diamond': 'Rewards (caches, rights, favors, windows)'
        },
        cards: {
            'Spade': ['Crossing point', 'Lookout knoll', 'Old road trace', 'Shelter hollow', 'Water source', 'Windbreak', 'Ruined outpost', 'Bad ground', 'Gate gully', 'Boundary row', 'Abandoned worksite', 'Signal height', 'Trail nexus'],
            'Heart': ['Forager child', 'Guide', 'Warden patrol', 'Caravan crew', 'Pilgrims', 'Poachers', 'Hermit-healer', 'Prospectors', 'Roving war-band', 'Monster-hunter', 'Quartermaster', 'Claimant chief', 'The Stranger'],
            'Club': ['Weather turn', 'Doubleback', 'Prowlers shadow', 'Route blocked', 'Quarantine sign', 'Territorial beast', 'Elemental front', 'Paper vs spear', 'Supply pinch', 'Pursuit', 'Bad omen', 'General alarm', 'Catastrophe'],
            'Diamond': ['Cache token', 'Right-of-way', 'Warden\'s favor', 'Weather window', 'Water/fuel deed', 'Route song', 'Remount/boat', 'Truce cord', 'Toll waiver', 'Rescue debt', 'Private audience', 'Road-warden', 'Earth\'s Exception']
        },
        specialRules: 'Salt & serpent omens; Ace: tides remember, reefs shift, deep listens'
    },
    
    'Ykrul': {
        name: 'Wolf Standards, Winter Camps',
        suits: {
            'Spade': 'Places (steppe roads, winter rings, fords, cairns)',
            'Heart': 'People & Factions (hosts, envoys, riders, courts)',
            'Club': 'Complications (law, weather, feud, logistics)',
            'Diamond': 'Rewards (passes, remounts, truces, audiences)'
        },
        cards: {
            'Spade': ['Wolf Road', 'Remount station', 'Birch windbreak', 'Salt pan', 'Reed ford', 'Trading palisade', 'Winter camp', 'Kurgan field', 'Watch kopje', 'Pontoon crossing', 'Council hollow', 'Khagan\'s way-station', 'Sky Steppe'],
            'Heart': ['Herd-scout', 'Camp-mother', 'Banner youth', 'Salt-broker', 'Remount keeper', 'Bone-singer', 'Road-judge', 'Noyan envoy', 'Winter Host', 'Falcon courier', 'Khatun', 'Khagan\'s nephew', 'Sky-Speaker'],
            'Club': ['White squall', 'Rasputitsa', 'Remount sickness', 'Salt shortage', 'Hostage protocol', 'Feud spark', 'Grassfire', 'Foedus recall', 'River break-up', 'Raid shadow', 'Kurultai', 'Muster', 'Sky omen'],
            'Diamond': ['Camp token', 'Salt allotment', 'Ford-right', 'Remount chit', 'Escort braid', 'Safe-hostage', 'Paiza', 'Foedus seal', 'Market-green', 'Standard protection', 'Audience', 'Khagan\'s writ', 'Sky\'s Exception']
        },
        specialRules: 'Reskin palette for any biome'
    },
    
    'Zakov': {
        name: 'Salt & Serpent',
        suits: {
            'Spade': 'Places (harbors, bolt-holes, black markets, smuggling routes)',
            'Heart': 'People & Factions (syndicates, corsairs, fences, informants)',
            'Club': 'Complications (betrayals, storms, syndicate feuds, cursed cargo)',
            'Diamond': 'Rewards (passes, contracts, stolen goods, safe harbors)'
        },
        cards: {
            'Spade': ['Salt-cracked wharf', 'Bone-yard beach', 'Smuggler\'s Gate', 'The Shallows', 'Dregs Quarter', 'Iron Pier', 'Crow\'s Roost', 'Black Bazaar', 'Salt Marsh Maze', 'Sunken Quarter', 'Crimson Docks', 'Anchorhead', 'Serpent\'s Spine'],
            'Heart': ['Dock-rat', 'Fence', 'Tavern-keeper', 'Corsair', 'Dock-master', 'Smuggler', 'Poison-tongue', 'Exiled admiral', 'Pirate Queen', 'Silent Syndicate', 'Kraken\'s Tongue', 'Salt Prince', 'Drowned Admiral'],
            'Club': ['Tide turns', 'Rival syndicate', 'Cursed cargo', 'Storm warning', 'Double-cross', 'Salt Prince\'s Levy', 'Plague ship', 'Blood feud', 'Kraken rises', 'Contract voided', 'Syndicate splits', 'Naval blockade', 'Tide forgets'],
            'Diamond': ['Smuggler\'s token', 'Forged manifest', 'Safe berth', 'Corsair\'s charter', 'Salt Prince\'s writ', 'Black-market ledger', 'Salvage rights', 'Lighthouse key', 'Syndicate debt', 'Pirate Queen\'s blessing', 'Kraken\'s favor', 'Salt Prince\'s coin', 'Serpent\'s Mark']
        },
        specialRules: 'Salt & serpent omens; Ace: tides remember, reefs shift, deep listens'
    }
};

        
        drawCard: (region, suit = null) => {
            const regionData = DeckSystem.regions[region];
            if (!regionData) return null;
            
            const chosenSuit = suit || _.sample(Object.keys(regionData.cards));
            const cardOptions = regionData.cards[chosenSuit];
            const cardName = _.sample(cardOptions);
            const rank = _.sample(['2','3','4','5','6','7','8','9','10','J','Q','K','A']);
            
            const clockSize = DeckSystem.getClockSize(rank);
            
            return {
                region: region,
                suit: chosenSuit,
                rank: rank,
                cardName: cardName,
                meaning: regionData.suits[chosenSuit],
                clockSize: clockSize,
                isAce: rank === 'A',
                isFace: ['J','Q','K'].includes(rank)
            };
        },
        
        getClockSize: (rank) => {
            const sizes = { 
                '2':4, '3':4, '4':4, '5':4,
                '6':6, '7':6, '8':6, '9':6, '10':6,
                'J':8, 'Q':8, 'K':8, 
                'A':10 
            };
            return sizes[rank] || 6;
        },
        
        handleCombo: (cards) => {
            const ranks = cards.map(c => c.rank);
            const suits = cards.map(c => c.suit);
            
            // Check for pairs
            const rankCounts = _.countBy(ranks);
            const hasPair = _.some(rankCounts, count => count >= 2);
            
            // Check for flush
            const suitCounts = _.countBy(suits);
            const hasFlush = _.some(suitCounts, count => count >= 3);
            
            // Check for run
            const sortedRanks = ranks.sort();
            const hasRun = DeckSystem.isConsecutive(sortedRanks);
            
            return {
                pair: hasPair,
                flush: hasFlush,
                run: hasRun,
                faceAce: cards.some(c => c.isFace) && cards.some(c => c.rank === 'A')
            };
        },
        
        isConsecutive: (ranks) => {
            const rankOrder = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'];
            const indices = ranks.map(r => rankOrder.indexOf(r)).sort((a,b) => a-b);
            
            for (let i = 1; i < indices.length; i++) {
                if (indices[i] - indices[i-1] !== 1) return false;
            }
            return indices.length >= 3;
        }
    };
    
    // ==================== MAGIC SYSTEM ====================
    
    const MagicSystem = {
        paths: {
            'caster': { name: 'Freeform Magic', requirements: ['Caster\'s Gift'] },
            'runekeeper': { name: 'Rites Users', requirements: ['Thiasos', 'Codex'] },
            'invoker': { name: 'Symbol Path', requirements: ['Patron\'s Symbol'] },
            'summoner': { name: 'Pact-Whisperer', requirements: ['Lesser/Greater Pactwright'] }
        },
        
        calculateRiteDV: (obligationCost, spirit, tier) => {
            return Math.max(obligationCost - spirit, tier);
        },
        
        handleBacklash: (element, severity, sbCount) => {
            const backlashTable = {
                'Earth': {
                    'Minor': 'Rigidity/Collapse - Effect, -1 or Condition: Singed',
                    'Major': 'Structural Failure - Clock +1/2 or Condition'
                },
                'Fire': {
                    'Minor': 'Spread/Scorch - Heat flares, smoke blinds',
                    'Major': 'Conflagration - Spreading Fire clock +1'
                },
                'Air': {
                    'Minor': 'Dispersal/Whip - Effect reduced or scattered',
                    'Major': 'Storm Surge - Environmental Collapse clock +1'
                },
                'Water': {
                    'Minor': 'Flood/Contaminate - Area hazard or impurity',
                    'Major': 'Deluge - Flood clock +1'
                },
                'Fate': {
                    'Minor': 'Paradox/Closure - Unintended consequence',
                    'Major': 'Inevitable Outcome - Clock advances'
                },
                'Life': {
                    'Minor': 'Overgrowth/Fever - Growth becomes problematic',
                    'Major': 'Proliferation - Ecosystem Disruption clock +1'
                },
                'Luck': {
                    'Minor': 'Side-coincidence/Irony - Unexpected twist',
                    'Major': 'Karmic Reversal - Fortune turns against caster'
                },
                'Death': {
                    'Minor': 'Thin walls/Nightmares - Veil thins or dreams disturbed',
                    'Major': 'Threshold Breach - Ways Between opens unexpectedly'
                }
            };
            
            return backlashTable[element][severity] || 'Generic Backlash';
        },
        
        manageLeash: (spiritCap, actions) => {
            let leash = spiritCap + 2;
            let ticks = 0;
            
            actions.forEach(action => {
                if (action.takesHarm) ticks += 1;
                if (action.againstNature) ticks += 1;
                if (action.splitsFocus) ticks += 1;
                if (action.rivalContest) ticks += 1;
                if (action.quickMovement) ticks += 1;
                if (action.crossesWard) ticks += 1;
            });
            
            const newLeash = Math.max(0, leash - ticks);
            const departed = newLeash <= 0;
            
            return {
                current: newLeash,
                ticks: ticks,
                departed: departed,
                remaining: departed ? 0 : newLeash
            };
        },
        
        boonFinesse: (currentLeash, boonSpent) => {
            if (boonSpent && currentLeash > 0) {
                return Math.max(0, currentLeash - 1);
            }
            return currentLeash;
        }
    };
    
    // ==================== BOND SYSTEM ====================
    
    const BondSystem = {
        trackBondUsage: (characterId, bondName) => {
            const bondAttr = 'bond_${bondName.replace(/\s+/g, '_')}_used_this_session`;
            const used = getAttrByName(characterId, bondAttr) || 0;
            return used === 0;
        };
        
        generateBondBoon: (characterId, bondName, description) => {
            if (BondSystem.trackBondUsage(characterId, bondName)) {
                const bondAttr = `bond_${bondName.replace(/\s+/g, '_')}_used_this_session`;
                setAttrByName(characterId, bondAttr, 1);
                
                // Generate boon
                const currentBoons = getAttrByName(characterId, 'boon_count') || 0;
                setAttrByName(characterId, 'boon_count', Math.min(5, currentBoons + 1));
                
                return {
                    success: true,
                    boonGenerated: true,
                    bondName: bondName,
                    description: description
                };
            }
            return {
                success: false,
                reason: 'Bond already used this session'
            };
        },
        
        resetSessionBonds: (characterId) => {
            // This would be called at session end
            // Find all bond usage trackers and reset them
            // Implementation depends on how bonds are stored
        }
    };
    
    // ==================== TRAVEL SYSTEM ====================
    
    const TravelSystem = {
        createTravelClock: (destination, rank, partyId) => {
            const clockSize = DeckSystem.getClockSize(rank);
            
            const travelId = `${partyId}_${destination}_${Date.now()}`;
            
            state.fateEdge.activeTravels[travelId] = {
                id: travelId,
                destination: destination,
                size: clockSize,
                current: 0,
                partyId: partyId,
                startDate: new Date().toISOString(),
                complications: [],
                rewards: []
            };
            
            return state.fateEdge.activeTravels[travelId];
        },
        
        advanceClock: (travelId, segments = 1) => {
            const travel = state.fateEdge.activeTravels[travelId];
            if (!travel) return null;
            
            travel.current = Math.min(travel.size, travel.current + segments);
            
            const completed = travel.current >= travel.size;
            
            return {
                travel: travel,
                completed: completed,
                remaining: travel.size - travel.current
            };
        },
        
        handleRegionalRules: (region, card) => {
            const specialRules = {
                'Theona': (card) => {
                    if (card.rank === '9') {
                        return {
                            taboo: true,
                            omission: 'missing step/name/guest',
                            canBreak: false // Until special condition met
                        };
                    }
                    return null;
                },
                'Aeler': (card) => {
                    if (card.rank === 'A') {
                        return {
                            routeManipulation: true,
                            underground: true,
                            specialAccess: 'Aeler Ace Route Manipulation'
                        };
                    }
                    return null;
                },
                'Valewood': (card) => {
                    if (card.rank === '9') {
                        return {
                            taboo: true,
                            omission: 'unsaid name/unseen guest',
                            echo: 'empire echoes'
                        };
                    }
                    return null;
                }
            };
            
            return specialRules[region] ? specialRules[region](card) : null;
        }
    };
    
    // ==================== OVER-STACK SYSTEM ====================
    
    const OverStackSystem = {
        countAdvantages: (partyTokens) => {
            let advantages = 0;
            const advantageList = [];
            
            partyTokens.forEach(token => {
                // Count status markers that represent advantages
                if (token.get('status_blue')) { // Buff marker
                    advantages += 1;
                    advantageList.push('Active Buff');
                }
                if (token.get('status_green')) { // Terrain advantage
                    advantages += 1;
                    advantageList.push('Favorable Terrain');
                }
                if (token.get('status_purple')) { // Asset activation
                    advantages += 1;
                    advantageList.push('Asset Activation');
                }
                // Add more advantage detection as needed
            });
            
            return {
                count: advantages,
                list: advantageList
            };
        },
        
        triggerOverStack: (advantageCount, advantageList) => {
            if (advantageCount >= 3) {
                const effects = [
                    'Start challenge at +1 DV',
                    'Bank +1 SB for first Deck Twist'
                ];
                
                const chosenEffect = _.sample(effects);
                
                return {
                    triggered: true,
                    effect: chosenEffect,
                    advantages: advantageList,
                    count: advantageCount
                };
            }
            return { triggered: false };
        }
    };
    
    // ==================== PRESTIGE ABILITY SYSTEM ====================
    
    const PrestigeSystem = {
        abilities: {
            'Echo-Walker\'s Step': {
                tier: 'High',
                cost: 20,
                oncePer: 'arc',
                requirements: ['Wits 5', 'Arcana 4'],
                effects: [
                    'Step briefly into the Ways Between',
                    'Turn a complication into a boon',
                    'Observe perfect echo of past event',
                    'GM banks +2 SB',
                    'DV -1 on one action using revealed truth'
                ],
                tracking: 'per_arc'
            },
            'Warglord': {
                tier: 'High',
                cost: 18,
                oncePer: 'campaign',
                requirements: ['Body 5', 'Sway 3'],
                effects: [
                    'Unify scattered warbands into single host',
                    'Start Logistics clock',
                    'Start Grudge clock',
                    'Season-long effect'
                ],
                tracking: 'per_campaign'
            },
            'Spirit-Shield': {
                tier: 'High',
                cost: 15,
                oncePer: 'session',
                requirements: ['Spirit 4', 'Resolve 3'],
                effects: [
                    'Erase up to 3 SB from ally\'s roll',
                    'Caster marks Fatigue +1',
                    'GM banks +1 SB as backlash'
                ],
                tracking: 'per_session'
            }
        },
        
        trackUsage: (characterId, abilityName) => {
            const ability = PrestigeSystem.abilities[abilityName];
            if (!ability) return { canUse: false, reason: 'Ability not found' };
            
            const trackingAttr = `prestige_${abilityName.replace(/\s+/g, '_')}_last_used`;
            const lastUsed = getAttrByName(characterId, trackingAttr) || '';
            
            const canUse = PrestigeSystem.checkUsageTiming(ability, lastUsed);
            
            return {
                canUse: canUse,
                lastUsed: lastUsed,
                restriction: ability.oncePer
            };
        },
        
        checkUsageTiming: (ability, lastUsed) => {
            const now = new Date();
            const lastUsedDate = lastUsed ? new Date(lastUsed) : null;
            
            if (!lastUsedDate) return true;
            
            switch(ability.oncePer) {
                case 'session':
                    return lastUsedDate.toDateString() !== now.toDateString();
                case 'arc':
                    // Would need campaign tracking logic
                    return true;
                case 'campaign':
                    return true; // Always restrict these
                default:
                    return true;
            }
        },
        
        useAbility: (characterId, abilityName) => {
            const usageCheck = PrestigeSystem.trackUsage(characterId, abilityName);
            
            if (usageCheck.canUse) {
                const trackingAttr = `prestige_${abilityName.replace(/\s+/g, '_')}_last_used`;
                setAttrByName(characterId, trackingAttr, new Date().toISOString());
                
                return {
                    success: true,
                    ability: abilityName,
                    effects: PrestigeSystem.abilities[abilityName].effects
                };
            }
            
            return {
                success: false,
                reason: `Ability restricted: ${usageCheck.restriction}`
            };
        }
    };
    
    // ==================== CAMPAIGN CLOCK SYSTEM ====================
    
    const CampaignClock = {
        createClock: (name, size, description = '') => {
            const clockId = name.replace(/\s+/g, '_').toLowerCase();
            
            state.fateEdge.campaignClocks[clockId] = {
                id: clockId,
                name: name,
                size: size,
                current: 0,
                active: true,
                description: description,
                createdAt: new Date().toISOString()
            };
            
            return state.fateEdge.campaignClocks[clockId];
        },
        
        advanceClock: (clockId, segments = 1) => {
            const clock = state.fateEdge.campaignClocks[clockId];
            if (!clock || !clock.active) return null;
            
            clock.current = Math.min(clock.size, clock.current + segments);
            
            const completed = clock.current >= clock.size;
            
            if (completed) {
                CampaignClock.triggerCompletion(clockId);
            }
            
            return {
                clock: clock,
                completed: completed,
                remaining: clock.size - clock.current
            };
        },
        
        triggerCompletion: (clockId) => {
            const clock = state.fateEdge.campaignClocks[clockId];
            if (!clock) return;
            
            // Send notification about clock completion
            sendChat('FateEdge', `/w gm Campaign Clock "${clock.name}" has completed!`);
            
            // Here you could trigger specific campaign events
            // based on the clock name
        },
        
        getClock: (clockId) => {
            return state.fateEdge.campaignClocks[clockId] || null;
        },
        
        listClocks: () => {
            return Object.values(state.fateEdge.campaignClocks)
                .filter(clock => clock.active);
        }
    };
    
    // ==================== REGIONAL FEATURES ====================
    
    const RegionalFeatures = {
        'Theona': {
            name: 'Three Greens, No Ninth',
            handleTaboo: (cardDraw) => {
                if (cardDraw.rank === '9') {
                    return {
                        type: 'omission',
                        effect: 'missing step, unsaid name, or unseen guest',
                        canBreak: false,
                        consequence: 'Someone will come to collect later'
                    };
                }
                return null;
            },
            customRule: 'No Ninth custom - omit details when Ninth appears'
        },
        
        'Aeler': {
            name: 'Crowns & Under-Vaults',
            handleAce: (cardDraw) => {
                if (cardDraw.rank === 'A') {
                    return {
                        type: 'route_manipulation',
                        effect: 'rewrite routes beneath the mountains',
                        special: 'Aeler Ace Route Manipulation'
                    };
                }
                return null;
            },
            customRule: 'Keys click, bells answer, mountain listens'
        },
        
        'Valewood': {
            name: 'Empire Under Leaves',
            handleEcho: (cardDraw) => {
                if (cardDraw.isFace || cardDraw.rank === 'A') {
                    return {
                        type: 'empire_echo',
                        effect: 'relic-logic (floating stairs, singing locks)',
                        special: 'Empire wakes'
                    };
                }
                return null;
            },
            customRule: 'Paths remember, leaves whisper, light moves like water'
        }
    };
    
    // ==================== CHAT MESSAGE HANDLING ====================
    
    const handleChatMessage = (msg) => {
        if (msg.type !== 'api') return;
        
        const args = msg.content.split(/\s+/);
        const command = args[0].substring(1).toLowerCase();
        
        switch(command) {
            case 'fate-roll':
                handleRollCommand(args, msg);
                break;
                
            case 'fate-spend-sb':
                handleSBSpend(args, msg);
                break;
                
            case 'fate-gain-boon':
                handleBoonGain(args, msg);
                break;
                
            case 'fate-travel-draw':
                handleTravelDraw(args, msg);
                break;
                
            case 'fate-npc-gen':
                handleNPCGeneration(msg);
                break;
                
            case 'fate-convert-boons':
                handleBoonConversion(args, msg);
                break;
                
            case 'fate-prestige-use':
                handlePrestigeUse(args, msg);
                break;
                
            case 'fate-create-clock':
                handleCreateClock(args, msg);
                break;
                
            case 'fate-advance-clock':
                handleAdvanceClock(args, msg);
                break;
                
            case 'fate-bond-boon':
                handleBondBoon(args, msg);
                break;
                
            case 'fate-setup-complete':
                initialize();
                sendChat('FateEdge', '/w gm Fate\'s Edge Complete System initialized!');
                break;
        }
    };
    
    const handleRollCommand = (args, msg) => {
        const pool = parseInt(args[1]) || 2;
        const position = args[2] || 'Controlled';
        const description = args.slice(3).join(' ') || 'Unnamed action';
        
        const result = CoreMechanics.rollChallenge(pool, position, description, msg.who);
        
        const rollString = result.rolls.map(r => 
            r === 1 ? `[[${r}]]` : 
            r >= 6 ? `<strong>[[${r}]]</strong>` : 
            `[[${r}]]`
        ).join(', ');
        
        const output = `
        <div style="background: #f8f5f0; padding: 10px; border-radius: 5px; border-left: 4px solid #5d4037;">
            <h3>${msg.who} - ${result.description}</h3>
            <p><strong>Position:</strong> ${result.position}</p>
            <p><strong>Dice Pool:</strong> ${pool}d10</p>
            <p><strong>Rolls:</strong> ${rollString}</p>
            <p><strong>Successes:</strong> ${result.successes}</p>
            <p><strong>Story Beats:</strong> ${result.sbGenerated}</p>
            <p><strong>Result:</strong> ${result.result}</p>
        </div>
        `;
        
        sendChat('FateEdge', output);
        
        // Auto-generate SB if needed
        if (result.sbGenerated > 0) {
            handleAutoSB(result.sbGenerated, msg.who);
        }
    };
    
    const handleAutoSB = (sbCount, playerName) => {
        // This could automatically create SB tokens or track them
        sendChat('FateEdge', `/w gm ${playerName} generated ${sbCount} Story Beat(s)`);
    };
    
    const handleSBSpend = (args, msg) => {
        const sbCost = parseInt(args[1]) || 1;
        const effect = args.slice(2).join(' ') || 'Unnamed effect';
        
        const output = `
        <div style="background: #fff3cd; padding: 10px; border-radius: 5px; border: 1px solid #ffeaa7; border-left: 4px solid #ffc107;">
            <h3>Story Beat Spent</h3>
            <p><strong>Player:</strong> ${msg.who}</p>
            <p><strong>Cost:</strong> ${sbCost} SB</p>
            <p><strong>Effect:</strong> ${effect}</p>
        </div>
        `;
        
        sendChat('FateEdge', output);
    };
    
    const handleBoonGain = (args, msg) => {
        const reason = args.slice(1).join(' ') || 'Unspecified reason';
        
        const output = `
        <div style="background: #d4edda; padding: 10px; border-radius: 5px; border: 1px solid #c3e6cb; border-left: 4px solid #28a745;">
            <h3>Boon Gained</h3>
            <p><strong>Player:</strong> ${msg.who}</p>
            <p><strong>Reason:</strong> ${reason}</p>
            <p><strong>Effect:</strong> +1 Boon (Max 5)</p>
        </div>
        `;
        
        sendChat('FateEdge', output);
    };
    
    const handleTravelDraw = (args, msg) => {
        const region = args[1] || 'Acasia';
        const suit = args[2] || null;
        
        const card = DeckSystem.drawCard(region, suit);
        if (!card) {
            sendChat('FateEdge', `/w ${msg.who} Invalid region: ${region}`);
            return;
        }
        
        const regionalEffect = TravelSystem.handleRegionalRules(region, card);
        
        const output = `
        <div style="background: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #bbdefb; border-left: 4px solid #2196f3;">
            <h3>Travel Card Draw</h3>
            <p><strong>Region:</strong> ${region} (${DeckSystem.regions[region].name})</p>
            <p><strong>Card:</strong> ${card.rank} of ${card.suit}s - ${card.cardName}</p>
            <p><strong>Meaning:</strong> ${card.meaning}</p>
            <p><strong>Clock Size:</strong> ${card.clockSize} segments</p>
            ${regionalEffect ? `<p><strong>Regional Effect:</strong> ${regionalEffect.special || regionalEffect.effect}</p>` : ''}
            ${card.isAce ? '<p><strong style="color: #d32f2f;">ACE DRAWN - Special regional mechanics may apply!</strong></p>' : ''}
        </div>
        `;
        
        sendChat('FateEdge', output);
    };
    
    const handleNPCGeneration = (msg) => {
        const ambitions = [
            'Power', 'Wealth', 'Love', 'Knowledge', 'Survival', 
            'Fame', 'Freedom', 'Protection', 'Control', 'Recognition', 'Revenge'
        ];
        
        const beliefs = [
            'Might makes right', 'Ends justify means', 'Truth is sacred',
            'Loyalty is paramount', 'Family above all', 'Justice must prevail',
            'Fate can be changed', 'Tradition must be upheld', 
            'Change is necessary', 'The system works'
        ];
        
        const attitudes = [
            'Arrogant', 'Charismatic', 'Cold', 'Friendly', 'Paranoid',
            'Pious', 'Optimistic', 'Pessimistic', 'Calculating', 'Naive'
        ];
        
        const twists = [
            'Secretly insecure', 'Betraying their allies', 'Working for their enemy',
            'Hiding a dark past', 'Actually an impostor', 'Deeply compassionate',
            'Corrupted by power', 'Hopelessly cynical', 'Revolutionary at heart',
            'Acts on impulse', 'Cynical manipulator'
        ];
        
        const npc = {
            ambition: ambitions[randomInteger(ambitions.length) - 1],
            belief: beliefs[randomInteger(beliefs.length) - 1],
            attitude: attitudes[randomInteger(attitudes.length) - 1],
            twist: twists[randomInteger(twists.length) - 1]
        };
        
        const output = `
        <div style="background: #f3e5f5; padding: 10px; border-radius: 5px; border: 1px solid #e1bee7; border-left: 4px solid #9c27b0;">
            <h3>NPC Generated</h3>
            <p><strong>Ambition:</strong> ${npc.ambition}</p>
            <p><strong>Belief:</strong> ${npc.belief}</p>
            <p><strong>Attitude:</strong> ${npc.attitude}</p>
            <p><strong>Twist:</strong> ${npc.twist}</p>
        </div>
        `;
        
        sendChat('FateEdge', output);
    };
    
    const handleBoonConversion = (args, msg) => {
        // This would need to be tied to a specific character
        sendChat('FateEdge', `/w ${msg.who} Boon conversion handled through character sheet`);
    };
    
    const handlePrestigeUse = (args, msg) => {
        const abilityName = args.slice(1).join(' ') || 'Echo-Walker\'s Step';
        
        const output = `
        <div style="background: #fff3e0; padding: 10px; border-radius: 5px; border: 1px solid #ffcc80; border-left: 4px solid #ff9800;">
            <h3>Prestige Ability Check</h3>
            <p><strong>Player:</strong> ${msg.who}</p>
            <p><strong>Ability:</strong> ${abilityName}</p>
            <p><strong>Status:</strong> Please check character sheet for usage tracking</p>
        </div>
        `;
        
        sendChat('FateEdge', output);
    };
    
    const handleCreateClock = (args, msg) => {
        const name = args[1] || 'Unnamed Clock';
        const size = parseInt(args[2]) || 6;
        const description = args.slice(3).join(' ') || '';
        
        const clock = CampaignClock.createClock(name, size, description);
        
        const output = `
        <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; border: 1px solid #c8e6c8; border-left: 4px solid #4caf50;">
            <h3>Campaign Clock Created</h3>
            <p><strong>Name:</strong> ${clock.name}</p>
            <p><strong>Size:</strong> ${clock.size} segments</p>
            ${description ? `<p><strong>Description:</strong> ${description}</p>` : ''}
        </div>
        `;
        
        sendChat('FateEdge', output);
    };
    
    const handleAdvanceClock = (args, msg) => {
        const clockId = args[1] || 'default';
        const segments = parseInt(args[2]) || 1;
        
        const result = CampaignClock.advanceClock(clockId, segments);
        if (!result) {
            sendChat('FateEdge', `/w ${msg.who} Clock not found: ${clockId}`);
            return;
        }
        
        const output = `
        <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; border: 1px solid #c8e6c8; border-left: 4px solid #4caf50;">
            <h3>Clock Advanced</h3>
            <p><strong>Clock:</strong> ${result.clock.name}</p>
            <p><strong>Progress:</strong> ${result.clock.current}/${result.clock.size}</p>
            <p><strong>Remaining:</strong> ${result.remaining} segments</p>
            ${result.completed ? '<p><strong style="color: #d32f2f;">CLOCK COMPLETED!</strong></p>' : ''}
        </div>
        `;
        
        sendChat('FateEdge', output);
    };
    
    const handleBondBoon = (args, msg) => {
        const bondName = args[1] || 'Unspecified Bond';
        const description = args.slice(2).join(' ') || 'Bond-driven action';
        
        const output = `
        <div style="background: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #bbdefb; border-left: 4px solid #2196f3;">
            <h3>Bond-Driven Boon</h3>
            <p><strong>Player:</strong> ${msg.who}</p>
            <p><strong>Bond:</strong> ${bondName}</p>
            <p><strong>Action:</strong> ${description}</p>
            <p><strong>Status:</strong> Please track through character sheet</p>
        </div>
        `;
        
        sendChat('FateEdge', output);
    };
    
    // ==================== ATTRIBUTE HANDLING ====================
    
    const handleAttributeChange = (attr) => {
        const name = attr.get('name');
        const characterId = attr.get('characterid');
        
        switch(name) {
            case 'body':
                // Update fatigue track max
                break;
            case 'spirit':
            case 'presence':
                // Update obligation capacity
                updateObligationCapacity(characterId);
                break;
            case 'boon_count':
                ResourceTracker.updateBoonLimit(characterId);
                break;
        }
    };
    
    const updateObligationCapacity = (characterId) => {
        const spirit = getAttrByName(characterId, 'spirit') || 1;
        const presence = getAttrByName(characterId, 'presence') || 1;
        const capacity = spirit + presence;
        
        // This would update the character sheet display
    };
    
    const handleSkillAdd = (skill) => {
        // Handle new skill addition
        log(`New skill added: ${skill.get('name')}`);
    };
    
    const handleSkillRemove = (skill) => {
        // Handle skill removal
        log(`Skill removed: ${skill.get('name')}`);
    };
    
    // ==================== UTILITY FUNCTIONS ====================
    
    const getCharName = (characterId) => {
        const character = getObj('character', characterId);
        return character ? character.get('name') : 'Unknown Character';
    };
    
    const setAttrByName = (characterId, attrName, value) => {
        const attr = findObjs({
            _type: 'attribute',
            _characterid: characterId,
            name: attrName
        })[0];
        
        if (attr) {
            attr.set('current', value);
        } else {
            createObj('attribute', {
                name: attrName,
                current: value,
                characterid: characterId
            });
        }
    };
    
    const getAttrByName = (characterId, attrName) => {
        const attr = findObjs({
            _type: 'attribute',
            _characterid: characterId,
            name: attrName
        })[0];
        
        return attr ? parseInt(attr.get('current')) || attr.get('current') : null;
    };
    
    // ==================== PUBLIC INTERFACE ====================
    
    return {
        initialize: initialize,
        systems: {
            core: CoreMechanics,
            resources: ResourceTracker,
            deck: DeckSystem,
            magic: MagicSystem,
            bonds: BondSystem,
            travel: TravelSystem,
            overstack: OverStackSystem,
            prestige: PrestigeSystem,
            campaign: CampaignClock,
            regional: RegionalFeatures
        }
    };
})();

// Initialize when ready
on('ready', () => {
    FateEdgeComplete.initialize();
});



/* ============================
 * Fate's Edge — Hotfix Overlay
 * Date: 2025-10-09
 * Notes:
 * - Repairs DeckSystem definition and region binding
 * - Fixes BondSystem.trackBondUsage template string
 * - Adjusts Detailed description reroll behavior
 * - Adds getCharName helper used in sendChat messages
 * - Corrects PrestigeSystem 'campaign' once-per logic
 * - Completes RegionalFeatures.Aeler.handleAce
 * These definitions override earlier ones where applicable.
 * ============================ */

(() => {
  'use strict';

  // Ensure state namespace exists
  state.fateEdge = state.fateEdge || {
    campaignClocks: {},
    activeTravels: {},
    prestigeAbilities: {},
    deckCache: {}
  };

  // ---------- Helper: get character name safely ----------
  const getCharName = (charId) => {
    try {
      const c = getObj && getObj('character', charId);
      return c ? c.get('name') : `Character ${charId}`;
    } catch (e) {
      return `Character ${charId}`;
    }
  };

  // ---------- Fix: CoreMechanics.handleDescriptionLadder (Detailed = reroll only one 1) ----------
  if (typeof FateEdgeComplete !== 'undefined' && FateEdgeComplete.CoreMechanics) {
    const CM = FateEdgeComplete.CoreMechanics;
    CM.handleDescriptionLadder = (descriptionType, baseRoll) => {
      switch (descriptionType) {
        case 'Basic':
          return baseRoll;
        case 'Detailed': {
          // Re-roll exactly one die showing 1 (if any)
          let used = false;
          return baseRoll.map(die => {
            if (!used && die === 1) {
              used = true;
              return randomInteger(10);
            }
            return die;
          });
        }
        case 'Intricate':
          // Re-roll all 1s
          return baseRoll.map(die => (die === 1 ? randomInteger(10) : die));
        default:
          return baseRoll;
      }
    };
  }

  // ---------- Fix: BondSystem.trackBondUsage template string bug ----------
  if (typeof FateEdgeComplete !== 'undefined' && FateEdgeComplete.BondSystem) {
    const BS = FateEdgeComplete.BondSystem;
    BS.trackBondUsage = (characterId, bondName) => {
      const bondAttr = `bond_${bondName.replace(/\\s+/g, '_')}_used_this_session`;
      const used = (getAttrByName && getAttrByName(characterId, bondAttr)) || 0;
      return Number(used) === 0;
    };
  }

  // ---------- Complete / Define DeckSystem with regions ----------
  // Use existing TravelRegions if present
  const regions = (typeof FateEdgeComplete !== 'undefined' && FateEdgeComplete.TravelRegions)
    ? FateEdgeComplete.TravelRegions
    : (typeof TravelRegions !== 'undefined' ? TravelRegions : {});

  const DeckSystemFixed = {
    regions,
    drawCard: (region, suit = null) => {
      const regionData = DeckSystemFixed.regions[region];
      if (!regionData) return null;

      const chosenSuit = suit || _.sample(Object.keys(regionData.cards));
      const cardOptions = regionData.cards[chosenSuit];
      const cardName = _.sample(cardOptions);
      const rank = _.sample(['2','3','4','5','6','7','8','9','10','J','Q','K','A']);

      const clockSize = DeckSystemFixed.getClockSize(rank);

      return {
        region,
        suit: chosenSuit,
        rank,
        cardName,
        meaning: regionData.suits[chosenSuit],
        clockSize,
        isAce: rank === 'A',
        isFace: ['J','Q','K'].includes(rank)
      };
    },
    getClockSize: (rank) => {
      const sizes = {
        '2':4, '3':4, '4':4, '5':4,
        '6':6, '7':6, '8':6, '9':6, '10':6,
        'J':8, 'Q':8, 'K':8,
        'A':10
      };
      return sizes[rank] || 6;
    },
    handleCombo: (cards) => {
      const ranks = cards.map(c => c.rank);
      const suits = cards.map(c => c.suit);

      const rankCounts = _.countBy(ranks);
      const hasPair = _.some(rankCounts, count => count >= 2);

      const suitCounts = _.countBy(suits);
      const hasFlush = _.some(suitCounts, count => count >= 3);

      const sortedRanks = ranks.slice().sort((a,b)=>{
        const order = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'];
        return order.indexOf(a) - order.indexOf(b);
      });
      const hasRun = DeckSystemFixed.isConsecutive(sortedRanks);

      return {
        pair: hasPair,
        flush: hasFlush,
        run: hasRun,
        faceAce: cards.some(c => c.isFace) && cards.some(c => c.rank === 'A')
      };
    },
    isConsecutive: (ranks) => {
      const rankOrder = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'];
      const indices = ranks.map(r => rankOrder.indexOf(r)).sort((a,b) => a-b);
      for (let i = 1; i < indices.length; i++) {
        if (indices[i] - indices[i-1] !== 1) return false;
      }
      return indices.length >= 3;
    }
  };

  // Expose/attach
  if (typeof FateEdgeComplete !== 'undefined') {
    FateEdgeComplete.DeckSystem = DeckSystemFixed;
    FateEdgeComplete.getCharName = getCharName;
  } else {
    // create minimal export if base module wasn't defined
    this.FateEdgeComplete = { DeckSystem: DeckSystemFixed, getCharName };
  }

  // ---------- Fix: TravelSystem reference to DeckSystem ----------
  if (typeof FateEdgeComplete !== 'undefined' && FateEdgeComplete.TravelSystem) {
    const TS = FateEdgeComplete.TravelSystem;
    TS.createTravelClock = (destination, rank, partyId) => {
      const clockSize = DeckSystemFixed.getClockSize(rank);
      const travelId = `${partyId}_${destination}_${Date.now()}`;

      state.fateEdge.activeTravels[travelId] = {
        id: travelId,
        destination,
        size: clockSize,
        current: 0,
        partyId,
        startDate: new Date().toISOString(),
        complications: [],
        rewards: []
      };
      return state.fateEdge.activeTravels[travelId];
    };
  }

  // ---------- Fix: PrestigeSystem once-per 'campaign' ----------
  if (typeof FateEdgeComplete !== 'undefined' && FateEdgeComplete.PrestigeSystem) {
    const PS = FateEdgeComplete.PrestigeSystem;
    PS.checkUsageTiming = (ability, lastUsed) => {
      const now = new Date();
      const lastUsedDate = lastUsed ? new Date(lastUsed) : null;
      if (!lastUsedDate) return true;

      switch (ability.oncePer) {
        case 'session':
          return lastUsedDate.toDateString() !== now.toDateString();
        case 'arc':
          // TODO: refine when campaign arc tracking is implemented
          return true;
        case 'campaign':
          // If it's ever been used, it's not usable again this campaign
          return false;
        default:
          return true;
      }
    };
  }

  // ---------- Complete RegionalFeatures.Aeler.handleAce ----------
  if (typeof FateEdgeComplete !== 'undefined' && FateEdgeComplete.RegionalFeatures) {
    const RF = FateEdgeComplete.RegionalFeatures;
    if (RF.Aeler) {
      RF.Aeler.handleAce = (cardDraw) => {
        if (cardDraw.rank === 'A') {
          return {
            type: 'routeManipulation',
            underground: true,
            specialAccess: 'Aeler Ace Route Manipulation',
            effect: 'Create/Reveal an underground shortcut; adjust route clocks by -1 (min 1)'
          };
        }
        return null;
      };
    }
  }

  // ---------- Ensure on('ready') boots system ----------
  if (typeof on !== 'undefined' && typeof initialize === 'function') {
    on('ready', initialize);
  }

})();
