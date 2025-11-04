# Fate's Edge Roll20 Macros

## Core Mechanics Macros

### 1. Basic Challenge Roll
```javascript
!roll --template simple --{{name=Challenge Roll}} --{{description=@{selected|character_name} attempts @{selected|action_description}}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{roll=[[?{Dice Pool|4}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}}
```

### 2. Attribute + Skill Roll
```javascript
!roll --template simple --{{name=@{selected|skill_name} Check}} --{{description=@{selected|character_name} uses @{selected|skill_name}}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{pool=[[@{selected|attribute|max} + @{selected|skill_value}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}}
```

### 3. Spend Story Beat (SB)
```javascript
!setattr --sel --custom_controlled --mod --sb|-1 --silent
&{template:default} {{name=SB Spent}} {{effect=?{Effect|1 SB - Minor pressure (noise, trace, +1 Supply)|2 SB - Moderate setback (alarm, lose position, lesser foe)|3 SB - Serious trouble (reinforcements, gear breaks)|4+ SB - Major turn (trap springs, authority arrives)}}}
```

### 4. Generate Boon
```javascript
!setattr --sel --custom_controlled --mod --boon|+1 --silent
&{template:default} {{name=Boon Gained}} {{reason=?{Reason|Miss on significant action|Partial success|Creative solution|Bond-driven play}}}
```

### 5. Convert Boons to XP
```javascript
!setattr --sel --custom_controlled --boon|-2 --xp|+1 --silent
&{template:default} {{name=XP Conversion}} {{result=2 Boons converted to 1 XP (max 2 XP/session)}}
```

## Combat Macros

### 6. Melee Attack
```javascript
!roll --template simple --{{name=Melee Attack}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{pool=[[@{selected|body|max} + @{selected|melee}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}}
```

### 7. Ranged Attack
```javascript
!roll --template simple --{{name=Ranged Attack}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{pool=[[@{selected|wits|max} + @{selected|ranged}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}}
```

### 8. Defense Roll
```javascript
!roll --template simple --{{name=Defense}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{pool=[[@{selected|body|max} + @{selected|athletics}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}}
```

## Magic System Macros

### 9. Freeform Casting - Channel
```javascript
!roll --template simple --{{name=Channel Spell}} --{{element=?{Element|Earth|Fire|Air|Water|Fate|Life|Luck|Death}}} --{{pool=[[@{selected|wits|max} + @{selected|arcana}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}} --{{backlash=[[ones > 0]]}}
```

### 10. Freeform Casting - Weave
```javascript
!roll --template simple --{{name=Weave Spell}} --{{element=?{Element|Earth|Fire|Air|Water|Fate|Life|Luck|Death}}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{pool=[[@{selected|wits|max} + @{selected|arcana}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}} --{{backlash=[[ones > 0]]}}
```

### 11. Invoke Rite
```javascript
!roll --template simple --{{name=Invoke Rite}} --{{rite=?{Rite Name}}} --{{dv=?{Difficulty Value|2|3|4|5}}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{pool=[[@{selected|spirit|max} + @{selected|lore}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}} --{{obligation=+1}}
```

### 12. Summon Spirit
```javascript
!setattr --sel --custom_controlled --fatigue|+1 --silent
&{template:default} {{name=Summon Spirit}} {{spirit=?{Spirit Type}}} {{cap=?{Capacity|1|3}}} {{leash=[[?{Capacity} + @{selected|command|max}]] segments}}
```

## Resource Management Macros

### 13. Mark Fatigue
```javascript
!setattr --sel --custom_controlled --fatigue|+1 --silent
&{template:default} {{name=Fatigue Marked}} {{reason=?{Reason|Exertion|Magic|Travel}}} {{position_shift=?{Position Shift|Controlled->Risky|Risky->Desperate|Desperate->Harm}}}
```

### 14. Clear Fatigue
```javascript
!setattr --sel --custom_controlled --fatigue|-2 --silent
&{template:default} {{name=Fatigue Cleared}} {{result=2 Fatigue removed}}
```

### 15. Mark Harm
```javascript
!setattr --sel --custom_controlled --harm_?{Harm Level|1|2|3}|1 --silent
&{template:default} {{name=Harm Marked}} {{level=Harm ?{Harm Level|1|2|3}}} {{penalty=?{Penalty|-1 die related|-1 die most|-2 dice most}}}
```

### 16. Mark Supply Segment
```javascript
!setattr --sel --custom_controlled --supply_segment|+1 --silent
&{template:default} {{name=Supply Depleted}} {{segments=?{Segments|1|2|3|4} segments filled}}
```

## Deck-Based Generator Macros

### 17. Draw Travel Card
```javascript
&{template:default} {{name=Travel Card Draw}} {{region=?{Region|Acasia|Aeler|Valewood|Mistlands|Silkstrand}}} {{suit=?{Suit|Spade - Place|Heart - Actor|Club - Pressure|Diamond - Reward}}} {{rank=?{Rank|2|3|4|5|6|7|8|9|10|J|Q|K|A}}} {{clock=[[?{Rank|2|3|4|5} = 4, ?{Rank|6|7|8|9|10} = 6, ?{Rank|J|Q|K} = 8, ?{Rank|A} = 10]] segments}}
```

### 18. Draw Consequence Card
```javascript
&{template:default} {{name=Consequence Card}} {{suit=?{Suit|Heart - Social|Spade - Harm|Club - Material|Diamond - Magical}}} {{rank=?{Rank|2|3|4|5|6|7|8|9|10|J|Q|K|A}}} {{severity=?{Severity|Minor|Moderate|Major|Pivotal}}}
```

### 19. NPC Generator
```javascript
&{template:default} {{name=NPC Profile}} {{ambition=?{Ambition|Power|Wealth|Love|Knowledge|Survival|Fame|Freedom|Protection|Control|Recognition|Revenge}}} {{belief=?{Belief|Might makes right|Ends justify means|Truth is sacred|Loyalty is paramount|Family above all|Justice must prevail|Fate can be changed|Tradition must be upheld|Change is necessary|The system works}}} {{attitude=?{Attitude|Arrogant|Charismatic|Cold|Friendly|Paranoid|Pious|Optimistic|Pessimistic|Calculating|Naive}}} {{twist=?{Twist|Secretly insecure|Betraying their allies|Working for their enemy|Hiding a dark past|Actually an impostor|Deeply compassionate|Corrupted by power|Hopelessly cynical|Revolutionary at heart|Acts on impulse|Cynical manipulator}}}
```

## Travel System Macros

### 20. Start Travel Leg
```javascript
&{template:default} {{name=Travel Leg Started}} {{destination=?{Destination}}} {{clock_size=?{Clock Size|4|6|8|10} segments}} {{mode=?{Travel Mode|Road|River|Sea|Mountain|Underground|Shadow}}}
```

### 21. Advance Travel Clock
```javascript
!setattr --sel --custom_controlled --travel_segment|+?{Segments|1|2|3} --silent
&{template:default} {{name=Travel Progress}} {{segments=+?{Segments|1|2|3} segments}} {{total=@{selected|travel_segment} segments completed}}
```

## Social Conflict Macros

### 22. Sway Roll
```javascript
!roll --template simple --{{name=Sway Attempt}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{pool=[[@{selected|presence|max} + @{selected|sway}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}}
```

### 23. Command Roll
```javascript
!roll --template simple --{{name=Command}} --{{position=?{Position|Controlled|Risky|Desperate}}} --{{effect=?{Effect|Limited|Standard|Great}}} --{{pool=[[@{selected|presence|max} + @{selected|command}]]}} --{{roll=[[@{pool}d10]]}} --{{successes=[[count(roll, 6, 10)]]}} --{{ones=[[count(roll, 1, 1)]]}}
```

## Quick Utility Macros

### 24. Initiative (Narrative)
```javascript
&{template:default} {{name=Initiative}} {{order=?{Action Order|Player choice|Position-based|GM adjudicated}}}
```

### 25. Over-Stack Check
```javascript
&{template:default} {{name=Over-Stack Check}} {{advantages=?{Structural Advantages|0}}} {{trigger=[[?{Advantages} >= 3]]}} {{effect=?{Effect|Start challenge at +1 DV|Bank +1 SB}}}
```

### 26. Bond-Driven Boon
```javascript
!setattr --sel --custom_controlled --boon|+1 --silent
&{template:default} {{name=Bond-Driven Boon}} {{bond=?{Which Bond?}}} {{reason=?{How did the bond help?}}}
```

### 27. Obligation Tracker
```javascript
!setattr --sel --custom_controlled --obligation_current|+?{Segments|1} --silent
&{template:default} {{name=Obligation Marked}} {{patron=?{Patron}}} {{total=@{selected|obligation_current}/@{selected|obligation_capacity}}}
```

### 28. Clear Obligation
```javascript
!setattr --sel --custom_controlled --obligation_current|-?{Segments|1} --silent
&{template:default} {{name=Obligation Cleared}} {{patron=?{Patron}}} {{total=@{selected|obligation_current}/@{selected|obligation_capacity}}}
```

### 29. Asset Upkeep
```javascript
&{template:default} {{name=Asset Upkeep}} {{asset=?{Asset Name}}} {{type=?{Type|Efficient (XP)|Intensive (Action)}}} {{status=?{New Status|Maintained|Wary/Neglected|Seized/Compromised}}}
```

### 30. Quick Reference
```javascript
&{template:default} {{name=Quick Reference}} {{dv=?{DV|2 - Routine|3 - Pressured|4 - Hard|5+ - Extreme}}} {{position=?{Position|Controlled - Minor consequences|Risky - Moderate consequences|Desperate - Severe consequences}}} {{effect=?{Effect|Limited - Minor impact|Standard - Expected impact|Great - Major impact}}}
```