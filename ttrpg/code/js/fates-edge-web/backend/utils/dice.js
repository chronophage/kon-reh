/**
 * Roll Fate's Edge dice
 * @param {number} pool - Number of d10s to roll
 * @param {string} descriptionLevel - Basic, Detailed, or Intricate
 * @returns {Object} Roll results
 */
exports.rollDice = (pool, descriptionLevel = 'Basic') => {
  // Roll the dice (1-10)
  const dice = Array.from({ length: pool }, () => Math.floor(Math.random() * 10) + 1);
  
  // Count successes (6+)
  let successes = dice.filter(d => d >= 6).length;
  
  // Count complications (1s)
  let complications = dice.filter(d => d === 1).length;
  
  // Apply description ladder benefits
  if (descriptionLevel === 'Detailed' && complications > 0) {
    // Re-roll one 1
    const oneIndex = dice.indexOf(1);
    if (oneIndex !== -1) {
      const newRoll = Math.floor(Math.random() * 10) + 1;
      dice[oneIndex] = newRoll;
      
      // Update counts
      if (newRoll >= 6) successes++;
      if (newRoll === 1) complications++; // Still a 1
      else complications--; // Removed one 1
    }
  } else if (descriptionLevel === 'Intricate' && complications > 0) {
    // Re-roll all 1s
    for (let i = 0; i < dice.length; i++) {
      if (dice[i] === 1) {
        const newRoll = Math.floor(Math.random() * 10) + 1;
        dice[i] = newRoll;
        
        // Update counts
        if (newRoll >= 6) successes++;
        if (newRoll === 1) complications++; // Still a 1
        else complications--; // Removed one 1
      }
    }
  }
  
  return {
    dice,
    successes,
    complications,
    description: getDescription(successes, complications)
  };
};

/**
 * Get result description
 * @param {number} successes 
 * @param {number} complications 
 * @returns {string} Description of the result
 */
function getDescription(successes, complications) {
  if (successes === 0 && complications > 0) {
    return "Failure with Complications";
  } else if (successes === 0) {
    return "Failure";
  } else if (successes >= 1 && complications > 0) {
    return "Success with Complications";
  } else if (successes >= 1 && successes <= 2) {
    return "Marginal Success";
  } else if (successes >= 3 && successes <= 4) {
    return "Moderate Success";
  } else if (successes >= 5 && successes <= 6) {
    return "Major Success";
  } else if (successes >= 7) {
    return "Exceptional Success";
  }
  return "Unknown Result";
}

/**
 * Draw complication cards
 * @param {number} points - Number of complication points to draw
 * @returns {Array} Array of complication descriptions
 */
exports.drawComplications = (points) => {
  const complications = [];
  for (let i = 0; i < points; i++) {
    complications.push(getRandomComplication());
  }
  return complications;
};

/**
 * Get random complication description
 * @returns {string} Complication description
 */
function getRandomComplication() {
  const complications = [
    "Unexpected arrival of an enemy or rival",
    "A trusted ally acts against you",
    "Something you possess is stolen or damaged",
    "A secret is revealed at the worst possible moment",
    "The environment turns against you",
    "A crucial piece of equipment fails",
    "An innocent person is endangered",
    "Your reputation suffers",
    "A past mistake comes back to haunt you",
    "Resources become scarce or unavailable",
    "Time pressure intensifies",
    "A key ally becomes unavailable",
    "Misinformation spreads",
    "A hidden threat is revealed",
    "Personal relationships become strained"
  ];
  
  return complications[Math.floor(Math.random() * complications.length)];
}

