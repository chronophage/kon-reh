const { validationResult } = require('express-validator');
const Macro = require('../models/macro.model');
const Campaign = require('../models/campaign.model');
const { rollDice } = require('../utils/dice');

exports.createMacro = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { campaignId, name, command, description, isPublic = false } = req.body;
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

    // Create macro (needs GM approval unless public)
    const macroData = {
      userId,
      campaignId,
      name,
      command,
      description: description || '',
      isPublic,
      isApproved: isPublic || campaign.gmid === userId // Auto-approve if GM or public
    };

    const macroId = await Macro.create(macroData);
    const newMacro = await Macro.findById(macroId);

    res.status(201).json({
      message: isPublic || campaign.gmid === userId 
        ? 'Macro created successfully' 
        : 'Macro created and awaiting GM approval',
      macro: newMacro
    });
  } catch (error) {
    console.error('Create macro error:', error);
    res.status(500).json({ message: 'Server error creating macro' });
  }
};

exports.getCampaignMacros = async (req, res) => {
  try {
    const { campaignId } = req.params;

    // Verify user is in campaign
    const campaign = await Campaign.findById(campaignId);
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    const isAuthorized = campaign.gmid === req.userId || campaign.players.includes(req.userId);
    if (!isAuthorized) {
      return res.status(403).json({ message: 'Not authorized for this campaign' });
    }

    const macros = await Macro.findByCampaignId(campaignId);
    res.json(macros);
  } catch (error) {
    console.error('Get campaign macros error:', error);
    res.status(500).json({ message: 'Server error fetching macros' });
  }
};

exports.getUserMacros = async (req, res) => {
  try {
    const macros = await Macro.findByUserId(req.userId);
    res.json(macros);
  } catch (error) {
    console.error('Get user macros error:', error);
    res.status(500).json({ message: 'Server error fetching macros' });
  }
};

exports.updateMacro = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const macro = await Macro.findById(id);
    
    if (!macro) {
      return res.status(404).json({ message: 'Macro not found' });
    }

    // Only owner or GM can update
    const campaign = await Campaign.findById(macro.campaignid);
    const isAuthorized = macro.userid === req.userId || campaign.gmid === req.userId;
    
    if (!isAuthorized) {
      return res.status(403).json({ message: 'Not authorized to update this macro' });
    }

    const updateData = {};
    const allowedFields = ['name', 'command', 'description', 'isPublic'];

    allowedFields.forEach(field => {
      if (req.body[field] !== undefined) {
        updateData[field] = req.body[field];
      }
    });

    // If GM is updating, they can also approve
    if (campaign.gmid === req.userId && req.body.isApproved !== undefined) {
      updateData.isApproved = req.body.isApproved;
    }

    await Macro.update(id, updateData);
    const updatedMacro = await Macro.findById(id);
    
    res.json({
      message: 'Macro updated successfully',
      macro: updatedMacro
    });
  } catch (error) {
    console.error('Update macro error:', error);
    res.status(500).json({ message: 'Server error updating macro' });
  }
};

exports.deleteMacro = async (req, res) => {
  try {
    const { id } = req.params;
    const macro = await Macro.findById(id);
    
    if (!macro) {
      return res.status(404).json({ message: 'Macro not found' });
    }

    // Only owner or GM can delete
    const campaign = await Campaign.findById(macro.campaignid);
    const isAuthorized = macro.userid === req.userId || campaign.gmid === req.userId;
    
    if (!isAuthorized) {
      return res.status(403).json({ message: 'Not authorized to delete this macro' });
    }

    await Macro.delete(id);
    res.json({ message: 'Macro deleted successfully' });
  } catch (error) {
    console.error('Delete macro error:', error);
    res.status(500).json({ message: 'Server error deleting macro' });
  }
};

exports.getPendingMacros = async (req, res) => {
  try {
    const { campaignId } = req.params;

    // Only GM can see pending macros
    const campaign = await Campaign.findById(campaignId);
    if (!campaign) {
      return res.status(404).json({ message: 'Campaign not found' });
    }

    if (campaign.gmid !== req.userId) {
      return res.status(403).json({ message: 'Only GM can view pending macros' });
    }

    const pendingMacros = await Macro.getPendingMacros(campaignId);
    res.json(pendingMacros);
  } catch (error) {
    console.error('Get pending macros error:', error);
    res.status(500).json({ message: 'Server error fetching pending macros' });
  }
};

exports.approveMacro = async (req, res) => {
  try {
    const { id } = req.params;
    const macro = await Macro.findById(id);
    
    if (!macro) {
      return res.status(404).json({ message: 'Macro not found' });
    }

    // Only GM can approve
    const campaign = await Campaign.findById(macro.campaignid);
    if (campaign.gmid !== req.userId) {
      return res.status(403).json({ message: 'Only GM can approve macros' });
    }

    await Macro.update(id, { isApproved: true });
    const updatedMacro = await Macro.findById(id);
    
    res.json({
      message: 'Macro approved successfully',
      macro: updatedMacro
    });
  } catch (error) {
    console.error('Approve macro error:', error);
    res.status(500).json({ message: 'Server error approving macro' });
  }
};

