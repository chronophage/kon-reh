/em &{template:default} {{name=Fate's Edge Roll}} 
{{character_name=@{selected|token_name}}} 
{{Attribute=@{selected|attr_${attr1}}}}

{{Skill=@{selected|attr_${attr2}}}}

{{Dice Pool=[$[[ { @{selected|attr_${attr1}}, @{selected|attr_${attr2}} }cs1]]}} 
{{Position=@{selected|position}}} 
{{DV=@{selected|dv}}} 
{{-- 
  // CALCULATE SUCCESSES (6-9=1, 10=2)
  var successes = 0;
  var sb = 0;
  var dice = [];
  var pool = @{selected|attr_${attr1}} + @{selected|attr_${attr2}};
  for (var i=0; i<pool; i++) {
    var roll = randomInteger(10);
    dice.push(roll);
    if (roll >= 6 && roll <= 9) successes++;
    if (roll == 10) successes += 2;
    if (roll == 1) sb++;
  }
  // APPLY POSITION MODIFIERS
  if (selected|position == "Dominant") {
    // Re-roll one failure (die ≤5, 10s never re-rolled)
    var failures = dice.filter(d => d <=5 && d !==10).length;
    if (failures > 0) {
      var reroll = randomInteger(10);
      dice[dice.indexOf(dice.find(d=> d<=5 && d!==10))] = reroll;
      // Recalculate successes after reroll
      successes = 0;
      sb = 0;
      dice.forEach(d => {
        if (d >=6 && d <=9) successes++;
        if (d == 10) successes += 2;
        if (d == 1) sb++;
      });
    }
  } else if (selected|position == "Desperate") {
    // Re-roll one success (die ≥6, 10s never re-rolled)
    var successesToReroll = dice.filter(d => d >=6 && d !==10).length;
    if (successesToReroll > 0) {
      var reroll = randomInteger(10);
      dice[dice.indexOf(dice.find(d=> d>=6 && d!==10))] = reroll;
      // Recalculate successes after reroll
      successes = 0;
      sb = 0;
      dice.forEach(d => {
        if (d >=6 && d <=9) successes++;
        if (d == 10) successes += 2;
        if (d == 1) sb++;
      });
    }
  }
  // DETERMINE OUTCOME
  var outcome = "";
  var boonGain = 0;
  if (successes >= @{selected|dv} && sb == 0) {
    outcome = "Clean Success";
  } else if (successes >= @{selected|dv} && sb > 0) {
    outcome = "Success with SB";
  } else if (successes > 0 && successes < @{selected|dv}) {
    outcome = "Partial";
    boonGain = 1;
  } else if (successes == 0) {
    outcome = "Miss";
    boonGain = 2;
  }
  --}} 
{{Rolls=[[$[[dice]]]]}}
{{Successes=$[[successes]]}}
{{Story Beats=$[[sb]]}}
{{Outcome=$[[outcome]]}}
{{Boons Gained=$[[boonGain]]}}

