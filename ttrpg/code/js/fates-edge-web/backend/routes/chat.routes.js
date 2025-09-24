const express = require('express');
const { body, param } = require('express-validator');
const chatController = require('../controllers/chat.controller');
const authMiddleware = require('../middleware/auth.middleware');

const router = express.Router();

// All routes require authentication
router.use(authMiddleware);

// Send message
router.post('/messages', [
  body('campaignId').isUUID(),
  body('content').isLength({ min: 1, max: 2000 }).trim(),
  body('channel').optional().isIn(['general', 'ooc', 'private']),
  body('targetUserId').optional().isUUID(),
  body('characterId').optional().isUUID()
], chatController.sendMessage);

// Get campaign messages
router.get('/messages/:campaignId', [
  param('campaignId').isUUID()
], chatController.getCampaignMessages);

// Get channel messages
router.get('/messages/:campaignId/:channel', [
  param('campaignId').isUUID(),
  param('channel').isIn(['general', 'ooc', 'private'])
], chatController.getChannelMessages);

module.exports = router;

