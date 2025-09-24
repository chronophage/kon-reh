const { validationResult } = require('express-validator');
const Chat = require('../models/chat.model');
const Campaign = require('../models/campaign.model');
const Character = require('../models/character.model');

exports.sendMessage = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { campaignId, content, channel = 'general', targetUserId = null, characterId = null } = req.body;
    const userId = req.userId;

    // Verify user is in campaign
    const campaign = await Campaign.findById(campaignId);
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    const isAuthorized = campaign.gmid === userId || campaign.players.includes(userId);
    if (!isAuthorized) {
      return res.status(403).json({ message: 'Not authorized for this campaign' });
    }

    // Verify character ownership if provided
    if (characterId) {
      const character = await Character.findById(characterId);
      if (!character || character.userid !== userId) {
        return res.status(403).json({ message: 'Not authorized to use this character' });
      }
    }

    // Verify target user for whispers
    if (channel === 'private' && targetUserId) {
      const targetInCampaign = campaign.gmid === targetUserId || campaign.players.includes(targetUserId);
      if (!targetInCampaign) {
        return res.status(400).json({ message: 'Target user not in campaign' });
      }
    }

    const messageData = {
      campaignId,
      userId,
      characterId,
      content,
      channel,
      targetUserId
    };

    const messageId = await Chat.createMessage(messageData);
    
    // Get the full message with user/character info
    const messages = await Chat.getMessagesByCampaign(campaignId, 1);
    const newMessage = messages[messages.length - 1];

    res.status(201).json(newMessage);
  } catch (error) {
    console.error('Send message error:', error);
    res.status(500).json({ message: 'Server error sending message' });
  }
};

exports.getCampaignMessages = async (req, res) => {
  try {
    const { campaignId } = req.params;
    const { limit = 50 } = req.query;

    // Verify user is in campaign
    const campaign = await Campaign.findById(campaignId);
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    const isAuthorized = campaign.gmid === req.userId || campaign.players.includes(req.userId);
    if (!isAuthorized) {
      return res.status(403).json({ message: 'Not authorized for this campaign' });
    }

    const messages = await Chat.getMessagesByCampaign(campaignId, parseInt(limit));
    res.json(messages);
  } catch (error) {
    console.error('Get campaign messages error:', error);
    res.status(500).json({ message: 'Server error fetching messages' });
  }
};

exports.getChannelMessages = async (req, res) => {
  try {
    const { campaignId, channel } = req.params;
    const { limit = 50 } = req.query;

    // Verify user is in campaign
    const campaign = await Campaign.findById(campaignId);
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    const isAuthorized = campaign.gmid === req.userId || campaign.players.includes(req.userId);
    if (!isAuthorized) {
      return res.status(403).json({ message: 'Not authorized for this campaign' });
    }

    const messages = await Chat.getMessagesByChannel(campaignId, channel, parseInt(limit));
    res.json(messages);
  } catch (error) {
    console.error('Get channel messages error:', error);
    res.status(500).json({ message: 'Server error fetching messages' });
  }
};

