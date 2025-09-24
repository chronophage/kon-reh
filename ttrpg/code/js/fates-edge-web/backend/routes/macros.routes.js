// backend/routes/macros.routes.js (updated)
const express = require('express');
const router = express.Router();
const { pool } = require('../config/database');
const macroService = require('../services/macro.service');
const { validateInput } = require('../middleware/security.middleware');

// Get all macros for a campaign
router.get('/campaign/:campaignId', async (req, res) => {
  try {
    const { campaignId } = req.params;
    
    // Validate campaign ID
    if (!validateInput(campaignId, 'uuid')) {
      return res.status(400).json({ message: 'Invalid campaign ID' });
    }
    
    const result = await pool.query(
      `SELECT m.*, u.username as createdby_username
       FROM macros m
       JOIN users u ON m.createdby = u.userid
       WHERE m.campaignid = $1 AND m.isapproved = true
       ORDER BY m.createdat DESC`,
      [campaignId]
    );
    
    res.json(result.rows);
  } catch (error) {
    console.error('Get macros error:', error);
    res.status(500).json({ message: 'Failed to fetch macros' });
  }
});

// Create new macro
router.post('/', async (req, res) => {
  try {
    const { campaignId, name, command, description, isPublic } = req.body;
    const userId = req.user.userid; // From auth middleware
    
    // Validate input
    if (!validateInput(campaignId, 'uuid')) {
      return res.status(400).json({ message: 'Invalid campaign ID' });
    }
    
    if (!validateInput(name, 'string', { min: 1, max: 50 })) {
      return res.status(400).json({ message: 'Invalid macro name' });
    }
    
    if (!validateInput(command, 'string', { min: 1, max: 20 })) {
      return res.status(400).json({ message: 'Invalid macro command' });
    }
    
    const result = await pool.query(
      `INSERT INTO macros (campaignid, name, command, description, createdby, ispublic, isapproved, createdat, updatedat)
       VALUES ($1, $2, $3, $4, $5, $6, false, NOW(), NOW())
       RETURNING *`,
      [campaignId, name, command, description || '', userId, isPublic ?? true]
    );
    
    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error('Create macro error:', error);
    res.status(500).json({ message: 'Failed to create macro' });
  }
});

// Update macro (GM only)
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { name, command, description, isPublic, isApproved } = req.body;
    const userId = req.user.userid;
    
    // Validate macro ID
    if (!validateInput(id, 'uuid')) {
      return res.status(400).json({ message: 'Invalid macro ID' });
    }
    
    // Check if user is GM of the campaign
    const macroResult = await pool.query(
      `SELECT m.*, c.gmuserid
       FROM macros m
       JOIN campaigns c ON m.campaignid = c.campaignid
       WHERE m.macroid = $1`,
      [id]
    );
    
    if (macroResult.rows.length === 0) {
      return res.status(404).json({ message: 'Macro not found' });
    }
    
    const macro = macroResult.rows[0];
    const isGM = macro.gmuserid === userId;
    
    // Only GM can approve macros or update other users' macros
    if (!isGM && macro.createdby !== userId) {
      return res.status(403).json({ message: 'Permission denied' });
    }
    
    // Build update query based on permissions
    const updates = [];
    const values = [];
    let index = 1;
    
    if (name !== undefined) {
      updates.push(`name = $${index}`);
      values.push(name);
      index++;
    }
    
    if (command !== undefined) {
      updates.push(`command = $${index}`);
      values.push(command);
      index++;
    }
    
    if (description !== undefined) {
      updates.push(`description = $${index}`);
      values.push(description);
      index++;
    }
    
    if (isPublic !== undefined && isGM) {
      updates.push(`ispublic = $${index}`);
      values.push(isPublic);
      index++;
    }
    
    if (isApproved !== undefined && isGM) {
      updates.push(`isapproved = $${index}`);
      values.push(isApproved);
      index++;
    }
    
    updates.push(`updatedat = NOW()`);
    values.push(id);
    
    const result = await pool.query(
      `UPDATE macros 
       SET ${updates.join(', ')}
       WHERE macroid = $${index}
       RETURNING *`,
      values
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ message: 'Macro not found' });
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Update macro error:', error);
    res.status(500).json({ message: 'Failed to update macro' });
  }
});

// Delete macro
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userid;
    
    // Validate macro ID
    if (!validateInput(id, 'uuid')) {
      return res.status(400).json({ message: 'Invalid macro ID' });
    }
    
    // Check if user is GM or owner of the macro
    const macroResult = await pool.query(
      `SELECT m.*, c.gmuserid
       FROM macros m
       JOIN campaigns c ON m.campaignid = c.campaignid
       WHERE m.macroid = $1`,
      [id]
    );
    
    if (macroResult.rows.length === 0) {
      return res.status(404).json({ message: 'Macro not found' });
    }
    
    const macro = macroResult.rows[0];
    const isGM = macro.gmuserid === userId;
    const isOwner = macro.createdby === userId;
    
    if (!isGM && !isOwner) {
      return res.status(403).json({ message: 'Permission denied' });
    }
    
    await pool.query('DELETE FROM macros WHERE macroid = $1', [id]);
    
    res.json({ message: 'Macro deleted successfully' });
  } catch (error) {
    console.error('Delete macro error:', error);
    res.status(500).json({ message: 'Failed to delete macro' });
  }
});

// Execute macro
router.post('/execute', async (req, res) => {
  try {
    const { campaignId, macroCommand, characterId } = req.body;
    const userId = req.user.userid;
    const io = req.app.get('io'); // Get Socket.IO instance
    
    // Validate input
    if (!validateInput(campaignId, 'uuid')) {
      return res.status(400).json({ message: 'Invalid campaign ID' });
    }
    
    if (!validateInput(macroCommand, 'string', { min: 1, max: 200 })) {
      return res.status(400).json({ message: 'Invalid macro command' });
    }
    
    // Validate permissions
    const hasPermission = await macroService.validateMacroPermissions(userId, campaignId, macroCommand);
    if (!hasPermission) {
      return res.status(403).json({ message: 'Permission denied' });
    }
    
    // Execute the macro
    const executionResult = await macroService.executeMacro(
      { macroCommand, characterId },
      userId,
      campaignId,
      io
    );
    
    if (!executionResult.success) {
      return res.status(400).json({
        message: 'Macro execution failed',
        error: executionResult.error
      });
    }
    
    res.json({
      message: 'Macro executed successfully',
      result: executionResult.result
    });
  } catch (error) {
    console.error('Execute macro error:', error);
    res.status(500).json({ message: 'Failed to execute macro' });
  }
});

module.exports = router;

