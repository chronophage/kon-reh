const Character = require('../models/character.model');
const { validationResult } = require('express-validator');

exports.getUserCharacters = async (req, res) => {
  try {
    const { userId } = req.params;
    
    // Security: only allow users to get their own characters or GMs
    if (req.userId !== userId) {
      // Here you could add GM permission check
      return res.status(403).json({ message: 'Access denied' });
    }

    const characters = await Character.findByUserId(userId);
    res.json(characters);
  } catch (error) {
    console.error('Get user characters error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.createCharacter = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const characterData = {
      userId: req.userId,
      name: req.body.name,
      archetype: req.body.archetype || '',
      xpTotal: 0,
      xpSpent: 0,
      attributes: req.body.attributes || { body: 0, wits: 0, spirit: 0, presence: 0 },
      skills: req.body.skills || [],
      followers: req.body.followers || [],
      assets: req.body.assets || [],
      talents: req.body.talents || [],
      complications: req.body.complications || [],
      boons: 0
    };

    const characterId = await Character.create(characterData);
    const newCharacter = await Character.findById(characterId);
    
    res.status(201).json(newCharacter);
  } catch (error) {
    console.error('Create character error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.getCharacter = async (req, res) => {
  try {
    const { id } = req.params;
    const character = await Character.findById(id);
    
    if (!character) {
      return res.status(404).json({ message: 'Character not found' });
    }

    // Security: check if user owns this character or is GM
    if (character.userid !== req.userId) {
      // Add GM permission check here
      return res.status(403).json({ message: 'Access denied' });
    }

    res.json(character);
  } catch (error) {
    console.error('Get character error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.updateCharacter = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const character = await Character.findById(id);
    
    if (!character) {
      return res.status(404).json({ message: 'Character not found' });
    }

    // Security: check if user owns this character
    if (character.userid !== req.userId) {
      return res.status(403).json({ message: 'Access denied' });
    }

    const updateData = {};
    const allowedFields = [
      'name', 'archetype', 'attributes', 'skills', 
      'followers', 'assets', 'talents', 'complications', 'boons'
    ];

    allowedFields.forEach(field => {
      if (req.body[field] !== undefined) {
        updateData[field] = req.body[field];
      }
    });

    await Character.update(id, updateData);
    const updatedCharacter = await Character.findById(id);
    
    res.json(updatedCharacter);
  } catch (error) {
    console.error('Update character error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.deleteCharacter = async (req, res) => {
  try {
    const { id } = req.params;
    const character = await Character.findById(id);
    
    if (!character) {
      return res.status(404).json({ message: 'Character not found' });
    }

    // Security: check if user owns this character
    if (character.userid !== req.userId) {
      return res.status(403).json({ message: 'Access denied' });
    }

    await Character.delete(id);
    res.json({ message: 'Character deleted successfully' });
  } catch (error) {
    console.error('Delete character error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.advanceCharacter = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const { xpSpent } = req.body;

    const character = await Character.findById(id);
    if (!character) {
      return res.status(404).json({ message: 'Character not found' });
    }

    // Security: check if user owns this character
    if (character.userid !== req.userId) {
      return res.status(403).json({ message: 'Access denied' });
    }

    // Check if character has enough XP
    if (character.xpspent + xpSpent > character.xptotal) {
      return res.status(400).json({ message: 'Not enough XP available' });
    }

    const newSpent = character.xpspent + xpSpent;
    await Character.update(id, { xpspent: newSpent });
    
    const updatedCharacter = await Character.findById(id);
    res.json({
      message: `Spent ${xpSpent} XP`,
      character: updatedCharacter
    });
  } catch (error) {
    console.error('Advance character error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

