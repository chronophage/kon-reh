// Fate's Edge Comprehensive Setup
// Run this once to set up your campaign

const FateEdgeCampaignSetup = (() => {
    'use strict';
    
    const createMacros = () => {
        const macros = [
            {
                name: "Fate Setup",
                action: "!setup-fate",
                visibleto: "all",
                description: "Initialize Fate's Edge character sheets"
            },
            {
                name: "Roll Challenge",
                action: "!roll ?{Dice Pool|4} ?{Position|Controlled|Risky|Desperate} ?{Action Description|Generic Action}",
                visibleto: "all",
                description: "Make a basic challenge roll"
            },
            {
                name: "Spend SB",
                action: "!spend-sb ?{SB Cost|1} ?{Effect|Describe the complication}",
                visibleto: "all",
                description: "Spend Story Beats for complications"
            },
            {
                name: "Gain Boon",
                action: "!gain-boon ?{Reason|How was this earned?}",
                visibleto: "all",
                description: "Award a Boon to a character"
            },
            {
                name: "Travel Draw",
                action: "!travel-draw",
                visibleto: "all",
                description: "Draw a random travel card"
            },
            {
                name: "NPC Generator",
                action: "!npc-gen",
                visibleto: "all",
                description: "Generate a random NPC profile"
            },
            {
                name: "Magic Channel",
                action: "!roll ?{Pool|3} ?{Position|Controlled|Risky|Desperate} Channel Spell",
                visibleto: "all",
                description: "Channel potential for magic"
            },
            {
                name: "Magic Weave",
                action: "!roll ?{Pool|3} ?{Position|Controlled|Risky|Desperate} Weave Spell",
                visibleto: "all",
                description: "Weave magical effect"
            }
        ];
        
        _.each(macros, (macro) => {
            createObj('macro', {
                name: macro.name,
                action: macro.action,
                visibleto: macro.visibleto,
                description: macro.description
            });
        });
        
        sendChat('FateEdge', '/w gm Created Fate\'s Edge macros');
    };
    
    const createHandouts = () => {
        const handouts = [
            {
                name: "Fate's Edge Quick Reference",
                content: createQuickReference()
            },
            {
                name: "SB Spend Menu",
                content: createSBSpendMenu()
            },
            {
                name: "Travel Regions",
                content: createTravelRegionsGuide()
            }
        ];
        
        _.each(handouts, (handout) => {
            createObj('handout', {
                name: handout.name,
                notes: handout.content
            });
        });
        
        sendChat('FateEdge', '/w gm Created Fate\'s Edge handouts');
    };
    
    const createQuickReference = () => {
        return `
        <div style="font-family: sans-serif;">
            <h2>Fate's Edge Quick Reference</h2>
            
            <h3>Core Mechanic</h3>
            <ul>
                <li><strong>Approach:</strong> Describe intent and method</li>
                <li><strong>Position:</strong> Dominant/Controlled/Desperate</li>
                <li><strong>Roll:</strong> Attribute + Skill d10s</li>
                <li><strong>Count:</strong> 6+ = Success, 1 = Story Beat</li>
            </ul>
            
            <h3>Outcome Matrix</h3>
            <ul>
                <li><strong>Clean Success:</strong> S ≥ DV, 0 SB</li>
                <li><strong>Success & Cost:</strong> S ≥ DV, 1+ SB</li>
                <li><strong>Partial:</strong> 0 < S < DV</li>
                <li><strong>Miss:</strong> S = 0</li>
            </ul>
            
            <h3>Position Effects</h3>
            <ul>
                <li><strong>Controlled:</strong> Advantage, minor consequences</li>
                <li><strong>Risky:</strong> Even footing, moderate consequences</li>
                <li><strong>Desperate:</strong> Disadvantaged, severe consequences</li>
            </ul>
        </div>
        `;
    };
    
    const createSBSpendMenu = () => {
        return `
        <div style="font-family: sans-serif;">
            <h2>Story Beat Spend Menu</h2>
            
            <h3>Universal Options</h3>
            <ul>
                <li><strong>1 SB:</strong> Minor pressure - noise, trace, +1 Supply segment</li>
                <li><strong>2 SB:</strong> Moderate setback - alarm, lose position, lesser foe</li>
                <li><strong>3 SB:</strong> Serious trouble - reinforcements, gear break</li>
                <li><strong>4+ SB:</strong> Major turn - trap, authority arrival</li>
            </ul>
            
            <h3>Combat Options</h3>
            <ul>
                <li><strong>1 SB:</strong> Lose footing (-1 defense)</li>
                <li><strong>2 SB:</strong> Weapon jam or momentum shift</li>
                <li><strong>3 SB:</strong> Pinned, disarmed, separated</li>
                <li><strong>4+ SB:</strong> Special ability reveal, terrain collapse</li>
            </ul>
        </div>
        `;
    };
    
    const createTravelRegionsGuide = () => {
        return `
        <div style="font-family: sans-serif;">
            <h2>Travel Regions Guide</h2>
            
            <h3>Major Regions</h3>
            <ul>
                <li><strong>Acasia:</strong> Broken Marches - curses, warlords</li>
                <li><strong>Aeler:</strong> Crowns & Under-Vaults - dwarven engineering</li>
                <li><strong>Valewood:</strong> Empire Under Leaves - fae magic</li>
                <li><strong>Mistlands:</strong> Bells, Salt, Breath - supernatural boundaries</li>
                <li><strong>Silkstrand:</strong> City of Bridges - intrigue and trade</li>
            </ul>
            
            <h3>Travel Deck Meanings</h3>
            <ul>
                <li><strong>Spade:</strong> Place/Location</li>
                <li><strong>Heart:</strong> Actor/Faction</li>
                <li><strong>Club:</strong> Pressure/Complication</li>
                <li><strong>Diamond:</strong> Reward/Leverage</li>
            </ul>
        </div>
        `;
    };
    
    const setupCampaign = () => {
        createMacros();
        createHandouts();
        sendChat('FateEdge', '/w gm Fate\'s Edge campaign setup complete!');
    };
    
    return {
        setup: setupCampaign
    };
})();

// To run the setup, use:
// !setup-fate-campaign
on('chat:message', (msg) => {
    if (msg.type === 'api' && msg.content === '!setup-fate-campaign') {
        FateEdgeCampaignSetup.setup();
    }
});

