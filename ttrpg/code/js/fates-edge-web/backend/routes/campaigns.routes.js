const express = require('express');
const { body, param } = require('express-validator');
const campaignController = require('../controllers/campaign.controller');
const authMiddleware = require('../middleware/auth.middleware');

const router = express.Router();

// All routes require authentication
router.use(authMiddleware);

// Get all campaigns for a user (player or GM)
router.get('/:userId', [
  param('userId').isUUID()
], campaignController.getUserCampaigns);

// Create new campaign
router.post('/', [
  body('name').isLength({ min: 1, max: 100 }).trim(),
  body('description').optional().isLength({ max: 1000 }).trim()
], campaignController.createCampaign);

// Get specific campaign
router.get('/:id', [
  param('id').isUUID()
], campaignController.getCampaign);

// Update campaign
router.put('/:id', [
  param('id').isUUID(),
  body('name').optional().isLength({ min: 1, max: 100 }).trim(),
  body('description').optional().isLength({ max: 1000 }).trim(),
  body('status').optional().isIn(['active', 'inactive'])
], campaignController.updateCampaign);

// Invite player to campaign
router.post('/:id/invite', [
  param('id').isUUID(),
  body('userId').isUUID()
], campaignController.invitePlayer);

// Remove player from campaign
router.post('/:id/remove', [
  param('id').isUUID(),
  body('userId').isUUID()
], campaignController.removePlayer);

// Create session for campaign
router.post('/:id/sessions', [
  param('id').isUUID(),
  body('date').optional().isISO8601(),
  body('notes').optional().isLength({ max: 5000 }).trim()
], campaignController.createSession);

// Get campaign sessions
router.get('/:id/sessions', [
  param('id').isUUID()
], campaignController.getCampaignSessions);

module.exports = router;

