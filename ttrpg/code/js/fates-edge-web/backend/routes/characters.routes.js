// backend/routes/characters.routes.js (security enhanced)
const express = require('express');
const router = express.Router();
const { pool } = require('../config/database');
const { validateInput } = require('../middleware/security.middleware');

// Get all characters for user
router.get('/user/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    
    // Validate user ID
    if (!validateInput(userId, 'uuid')) {
      return res.status(400).json({ message: 'Invalid user ID' });
    }
    
    const result = await pool.query(
      `SELECT characterid, userid, name, description, species, background, archetype, 
              experience, createdat, updatedat
       FROM characters 
       WHERE userid = $1 
       ORDER BY createdat DESC`,
      [userId]
    );
    
    res.json(result.rows);
  } catch (error) {
    console.error('Get characters error:', error);
    res.status(500).json({ message: 'Failed to fetch characters' });
  }
});

// Get character by ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Validate character ID
    if (!validateInput(id, 'uuid')) {
      return res.status(400).json({ message: 'Invalid character ID' });
    }
    
    const result = await pool.query(
      `SELECT c.*, 
              json_agg(a.*) as attributes,
              json_agg(s.*) as skills,
              json_agg(t.*) as talents
       FROM characters c
       LEFT JOIN attributes a ON c.characterid = a.characterid
       LEFT JOIN skills s ON c.characterid = s.characterid
       LEFT JOIN talents t ON c.characterid = t.characterid
       WHERE c.characterid = $1
       GROUP BY c.characterid`,
      [id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ message: 'Character not found' });
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Get character error:', error);
    res.status(500).json({ message: 'Failed to fetch character' });
  }
});

// Create character
router.post('/', async (req, res) => {
  try {
    const { userid, name, description, species, background, archetype } = req.body;
    
    // Validate input
    if (!validateInput(userid, 'uuid')) {
      return res.status(400).json({ message: 'Invalid user ID' });
    }
    
    if (!validateInput(name, 'string', { min: 1, max: 100 })) {
      return res.status(400).json({ message: 'Invalid character name' });
    }
    
    const result = await pool.query(
      `INSERT INTO characters (userid, name, description, species, background, archetype, createdat, updatedat)
       VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
       RETURNING *`,
      [userid, name, description || '', species || '', background || '', archetype || '']
    );
    
    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error('Create character error:', error);
    res.status(500).json({ message: 'Failed to create character' });
  }
});

// Update character
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { name, description, species, background, archetype } = req.body;
    
    // Validate character ID
    if (!validateInput(id, 'uuid')) {
      return res.status(400).json({ message: 'Invalid character ID' });
    }
    
    // Validate input
    if (name && !validateInput(name, 'string', { min: 1, max: 100 })) {
      return res.status(400).json({ message: 'Invalid character name' });
    }
    
    const result = await pool.query(
      `UPDATE characters 
       SET name = $1, description = $2, species = $3, background = $4, archetype = $5, updatedat = NOW()
       WHERE characterid = $6
       RETURNING *`,
      [name, description, species, background, archetype, id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ message: 'Character not found' });
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Update character error:', error);
    res.status(500).json({ message: 'Failed to update character' });
  }
});

// Delete character
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Validate character ID
    if (!validateInput(id, 'uuid')) {
      return res.status(400).json({ message: 'Invalid character ID' });
    }
    
    const result = await pool.query(
      'DELETE FROM characters WHERE characterid = $1 RETURNING *',
      [id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ message: 'Character not found' });
    }
    
    res.json({ message: 'Character deleted successfully' });
  } catch (error) {
    console.error('Delete character error:', error);
    res.status(500).json({ message: 'Failed to delete character' });
  }
});

module.exports = router;

