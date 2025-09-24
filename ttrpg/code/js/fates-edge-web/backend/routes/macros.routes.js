const express = require('express');
const { body, param } = require('express-validator');
const macroController = require('../controllers/macro.controller');
const authMiddleware = require('../middleware/auth.middleware');

const router = express.Router();

// All routes require authentication
router.use(authMiddleware);

// Create macro
router.post('/', [
  body('campaignId').isUUID(),
  body('name').isLength({ min: 1, max: 50 }).trim(),
  body('command').isLength({ min: 1, max: 500 }).trim(),
  body('description').optional().isLength({ max: 200 }).trim(),
  body('isPublic').optional().isBoolean()
], macroController.createMacro);

// Get campaign macros
router.get('/campaign/:campaignId', [
  param('campaignId').isUUID()
], macroController.getCampaignMacros);

// Get user macros
router.get('/user', macroController.getUserMacros);

// Get pending macros (GM only)
router.get('/pending/:campaignId', [
  param('campaignId').isUUID()
], macroController.getPendingMacros);

// Update macro
router.put('/:id', [
  param('id').isUUID(),
  body('name').optional().isLength({ min: 1, max: 50 }).trim(),
  body('command').optional().isLength({ min: 1, max: 500 }).trim(),
  body('description').optional().isLength({ max: 200 }).trim(),
  body('isPublic').optional().isBoolean(),
  body('isApproved').optional().isBoolean()
], macroController.updateMacro);

// Approve macro (GM only)
router.patch('/:id/approve', [
  param('id').isUUID()
], macroController.approveMacro);

// Delete macro
router.delete('/:id', [
  param('id').isUUID()
], macroController.deleteMacro);

module.exports = router;

