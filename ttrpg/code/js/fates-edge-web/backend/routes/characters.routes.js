const express = require('express');
const { body, param } = require('express-validator');
const characterController = require('../controllers/character.controller');
const authMiddleware = require('../middleware/auth.middleware');

const router = express.Router();

// All routes require authentication
router.use(authMiddleware);

// Get all characters for a user
router.get('/:userId', [
  param('userId').isUUID()
], characterController.getUserCharacters);

// Create new character
router.post('/', [
  body('name').isLength({ min: 1, max: 100 }).trim(),
  body('archetype').optional().isLength({ max: 50 }).trim(),
  body('attributes').optional().isObject(),
  body('skills').optional().isArray(),
  body('followers').optional().isArray(),
  body('assets').optional().isArray(),
  body('talents').optional().isArray(),
  body('complications').optional().isArray()
], characterController.createCharacter);

// Get specific character
router.get('/:id', [
  param('id').isUUID()
], characterController.getCharacter);

// Update character
router.put('/:id', [
  param('id').isUUID(),
  body('name').optional().isLength({ min: 1, max: 100 }).trim(),
  body('archetype').optional().isLength({ max: 50 }).trim(),
  body('attributes').optional().isObject(),
  body('skills').optional().isArray(),
  body('followers').optional().isArray(),
  body('assets').optional().isArray(),
  body('talents').optional().isArray(),
  body('complications').optional().isArray()
], characterController.updateCharacter);

// Delete character
router.delete('/:id', [
  param('id').isUUID()
], characterController.deleteCharacter);

// Advance character (XP spending)
router.post('/:id/advance', [
  param('id').isUUID(),
  body('xpSpent').isInt({ min: 1 })
], characterController.advanceCharacter);

module.exports = router;

