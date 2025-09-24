const Campaign = require('../models/campaign.model');
const Session = require('../models/session.model');
const User = require('../models/user.model');
const { validationResult } = require('express-validator');

exports.getUserCampaigns = async (req, res) => {
  try {
    const { userId } = req.params;
    
    // Security: only allow users to get their own campaigns
    if (req.userId !== userId) {
      return res.status(403).json({ message: 'Access denied' });
    }

    const campaigns = await Campaign.findByUser(userId);
    res.json(campaigns);
  } catch (error) {
    console.error('Get user campaigns error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.createCampaign = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const campaignData = {
      gmId: req.userId, // Only GMs can create campaigns
      name: req.body.name,
      description: req.body.description || '',
      players: [], // Start with empty player list
      status: 'active'
    };

    const campaignId = await Campaign.create(campaignData);
    const newCampaign = await Campaign.findById(campaignId);
    
    res.status(201).json(newCampaign);
  } catch (error) {
    console.error('Create campaign error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.getCampaign = async (req, res) => {
  try {
    const { id } = req.params;
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    // Security: check if user is GM or player in this campaign
    const isAuthorized = campaign.gmid === req.userId || 
                         campaign.players.includes(req.userId);
    
    if (!isAuthorized) {
      return res.status(403).json({ message: 'Access denied' });
    }

    res.json(campaign);
  } catch (error) {
    console.error('Get campaign error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.updateCampaign = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    // Security: only GM can update campaign
    if (campaign.gmid !== req.userId) {
      return res.status(403).json({ message: 'Access denied' });
    }

    const updateData = {};
    const allowedFields = ['name', 'description', 'status'];

    allowedFields.forEach(field => {
      if (req.body[field] !== undefined) {
        updateData[field] = req.body[field];
      }
    });

    await Campaign.update(id, updateData);
    const updatedCampaign = await Campaign.findById(id);
    
    res.json(updatedCampaign);
  } catch (error) {
    console.error('Update campaign error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.invitePlayer = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const { userId } = req.body;

    const campaign = await Campaign.findById(id);
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    // Security: only GM can invite players
    if (campaign.gmid !== req.userId) {
      return res.status(403).json({ message: 'Access denied' });
    }

    // Check if user exists
    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Check if user is already in campaign
    if (campaign.players.includes(userId)) {
      return res.status(400).json({ message: 'User already in campaign' });
    }

    // Add player to campaign
    const updatedPlayers = [...campaign.players, userId];
    await Campaign.update(id, { players: updatedPlayers });
    
    const updatedCampaign = await Campaign.findById(id);
    res.json({
      message: 'Player invited successfully',
      campaign: updatedCampaign
    });
  } catch (error) {
    console.error('Invite player error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.removePlayer = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const { userId } = req.body;

    const campaign = await Campaign.findById(id);
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    // Security: only GM can remove players
    if (campaign.gmid !== req.userId) {
      return res.status(403).json({ message: 'Access denied' });
    }

    // Check if user is in campaign
    if (!campaign.players.includes(userId)) {
      return res.status(400).json({ message: 'User not in campaign' });
    }

    // Remove player from campaign
    const updatedPlayers = campaign.players.filter(playerId => playerId !== userId);
    await Campaign.update(id, { players: updatedPlayers });
    
    const updatedCampaign = await Campaign.findById(id);
    res.json({
      message: 'Player removed successfully',
      campaign: updatedCampaign
    });
  } catch (error) {
    console.error('Remove player error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.createSession = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    // Security: only GM can create sessions
    if (campaign.gmid !== req.userId) {
      return res.status(403).json({ message: 'Access denied' });
    }

    const sessionData = {
      campaignId: id,
      date: req.body.date || new Date().toISOString().split('T')[0],
      notes: req.body.notes || '',
      attendance: [], // Will be updated later
      xpAwards: [] // Will be updated later
    };

    const sessionId = await Session.create(sessionData);
    const newSession = await Session.findById(sessionId);
    
    res.status(201).json(newSession);
  } catch (error) {
    console.error('Create session error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.getCampaignSessions = async (req, res) => {
  try {
    const { id } = req.params;
    const campaign = await Campaign.findById(id);
    
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    // Security: check if user is GM or player in this campaign
    const isAuthorized = campaign.gmid === req.userId || 
                         campaign.players.includes(req.userId);
    
    if (!isAuthorized) {
      return res.status(403).json({ message: 'Access denied' });
    }

    const sessions = await Session.findByCampaignId(id);
    res.json(sessions);
  } catch (error) {
    console.error('Get campaign sessions error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

