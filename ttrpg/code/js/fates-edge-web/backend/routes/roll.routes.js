const express = require('express');
const { body, param } = require('express-validator');
const rollController = require('../controllers/roll.controller');
const authMiddleware = require('../middleware/auth.middleware');

const router = express.Router();

// All routes require authentication
router.use(authMiddleware);

router.post('/', rollLimiter, [
  body('pool').isInt({ min: 1, max: 20 }),
  body('descriptionLevel').optional().isIn(['Basic', 'Detailed', 'Intricate']),
  body('characterId').optional().isUUID(),
  body('notes').optional().isLength({ max: 500 }).trim()
], rollController.rollDice);

// Get roll history for character
router.get('/history/:characterId', [
  param('characterId').isUUID()
], rollController.getRollHistory);

// Handle complications
router.post('/complications', complicationLimiter, [
  body('points').isInt({ min: 1, max: 10 }),
  body('gmSpends').optional().isArray()
], rollController.handleComplications);

module.exports = router;

