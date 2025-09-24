const { validationResult } = require('express-validator');
const Roll = require('../models/roll.model');
const Character = require('../models/character.model');
const { rollDice, drawComplications } = require('../utils/dice');

exports.rollDice = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { pool, descriptionLevel = 'Basic', characterId, notes } = req.body;
    const userId = req.userId;

    // Validate character ownership if provided
    let character = null;
    if (characterId) {
      character = await Character.findById(characterId);
      if (!character) {
        return res.status(404).json({ message: 'Character not found' });
      }
      if (character.userid !== userId) {
        return res.status(403).json({ message: 'Access denied to this character' });
      }
    }

    // Perform the roll
    const rollResult = rollDice(pool, descriptionLevel);

    // Save roll to history
    const rollData = {
      userId,
      characterId: characterId || null,
      pool,
      descriptionLevel,
      dice: rollResult.dice,
      successes: rollResult.successes,
      complications: rollResult.complications,
      notes: notes || ''
    };

    const rollId = await Roll.create(rollData);

    res.status(201).json({
      rollId,
      ...rollResult,
      pool,
      descriptionLevel,
      notes
    });
  } catch (error) {
    console.error('Dice roll error:', error);
    res.status(500).json({ message: 'Server error during dice roll' });
  }
};

exports.getRollHistory = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { characterId } = req.params;
    
    // Verify character ownership
    const character = await Character.findById(characterId);
    if (!character) {
      return res.status(404).json({ message: 'Character not found' });
    }
    
    if (character.userid !== req.userId) {
      return res.status(403).json({ message: 'Access denied to this character' });
    }

    const history = await Roll.findByCharacterId(characterId);
    res.json(history);
  } catch (error) {
    console.error('Get roll history error:', error);
    res.status(500).json({ message: 'Server error fetching roll history' });
  }
};

exports.handleComplications = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { points, gmSpends = [] } = req.body;

    // Draw complications
    const complications = drawComplications(points);

    res.json({
      message: `Drew ${points} complication(s)`,
      complications,
      gmSpends
    });
  } catch (error) {
    console.error('Handle complications error:', error);
    res.status(500).json({ message: 'Server error handling complications' });
  }
};

