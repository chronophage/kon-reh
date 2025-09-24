// backend/services/macro.service.js
class MacroService {
  constructor() {
    // Define macro commands and their handlers
    this.macroHandlers = {
      // Dice rolling macros
      '/roll': this.handleRoll.bind(this),
      '/r': this.handleRoll.bind(this),
      
      // Character macros
      '/xp': this.handleXP.bind(this),
      '/boon': this.handleBoon.bind(this),
      
      // Campaign macros
      '/clock': this.handleClock.bind(this),
      '/session': this.handleSession.bind(this),
      
      // Utility macros
      '/whisper': this.handleWhisper.bind(this),
      '/w': this.handleWhisper.bind(this),
      '/me': this.handleEmote.bind(this)
    };
    
    // Define macro syntax patterns
    this.patterns = {
      roll: /^\/(roll|r)\s+(\d+)(?:\s+(basic|detailed|intricate))?(?:\s+(.*))?$/i,
      xp: /^\/xp\s+([+-]\d+)(?:\s+(.*))?$/i,
      boon: /^\/boon\s+(convert|spend)(?:\s+(.*))?$/i,
      clock: /^\/clock\s+(tick|reset)\s+(\w+)(?:\s+(\d+))?$/i,
      session: /^\/session\s+(start|end)(?:\s+(.*))?$/i,
      whisper: /^\/(whisper|w)\s+<@(\w+)> (.*)$/i,
      emote: /^\/me\s+(.*)$/i
    };
  }

  // Parse and execute macro
  async executeMacro(macroData, userId, campaignId, io) {
    try {
      const { macroCommand, characterId } = macroData;
      
      // Validate input
      if (!macroCommand || typeof macroCommand !== 'string') {
        throw new Error('Invalid macro command');
      }
      
      // Parse the macro command
      const parsedMacro = this.parseMacro(macroCommand);
      if (!parsedMacro) {
        throw new Error('Unrecognized macro command');
      }
      
      // Execute the appropriate handler
      const result = await this.macroHandlers[parsedMacro.command]({
        ...parsedMacro,
        userId,
        campaignId,
        characterId,
        io
      });
      
      return {
        success: true,
        result,
        executedCommand: macroCommand
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        executedCommand: macroData.macroCommand
      };
    }
  }

  // Parse macro command
  parseMacro(command) {
    // Clean the command
    const cleanCommand = command.trim();
    
    // Try to match against known patterns
    if (this.patterns.roll.test(cleanCommand)) {
      const match = cleanCommand.match(this.patterns.roll);
      return {
        command: '/roll',
        dicePool: parseInt(match[2]),
        descriptionLevel: match[3] ? match[3].toLowerCase() : 'basic',
        notes: match[4] || ''
      };
    }
    
    if (this.patterns.xp.test(cleanCommand)) {
      const match = cleanCommand.match(this.patterns.xp);
      return {
        command: '/xp',
        amount: parseInt(match[1]),
        reason: match[2] || ''
      };
    }
    
    if (this.patterns.boon.test(cleanCommand)) {
      const match = cleanCommand.match(this.patterns.boon);
      return {
        command: '/boon',
        action: match[1].toLowerCase(),
        details: match[2] || ''
      };
    }
    
    if (this.patterns.clock.test(cleanCommand)) {
      const match = cleanCommand.match(this.patterns.clock);
      return {
        command: '/clock',
        action: match[1].toLowerCase(),
        clockName: match[2],
        amount: match[3] ? parseInt(match[3]) : 1
      };
    }
    
    if (this.patterns.session.test(cleanCommand)) {
      const match = cleanCommand.match(this.patterns.session);
      return {
        command: '/session',
        action: match[1].toLowerCase(),
        details: match[2] || ''
      };
    }
    
    if (this.patterns.whisper.test(cleanCommand)) {
      const match = cleanCommand.match(this.patterns.whisper);
      return {
        command: '/whisper',
        target: match[2],
        message: match[3]
      };
    }
    
    if (this.patterns.emote.test(cleanCommand)) {
      const match = cleanCommand.match(this.patterns.emote);
      return {
        command: '/me',
        action: match[1]
      };
    }
    
    return null;
  }

  // Handle dice rolling macros
  async handleRoll(params) {
    const { dicePool, descriptionLevel, notes, userId, campaignId, characterId, io } = params;
    
    // Validate dice pool
    if (dicePool < 1 || dicePool > 20) {
      throw new Error('Dice pool must be between 1 and 20');
    }
    
    // Roll the dice
    const dice = Array.from({ length: dicePool }, () => Math.floor(Math.random() * 10) + 1);
    let successes = dice.filter(d => d >= 6).length;
    let complications = dice.filter(d => d === 1).length;
    
    // Apply description ladder benefits
    if (descriptionLevel === 'detailed' && complications > 0) {
      const oneIndex = dice.indexOf(1);
      if (oneIndex !== -1) {
        const newRoll = Math.floor(Math.random() * 10) + 1;
        dice[oneIndex] = newRoll;
        if (newRoll >= 6) successes++;
        if (newRoll === 1) complications++;
        else complications--;
      }
    } else if (descriptionLevel === 'intricate' && complications > 0) {
      for (let i = 0; i < dice.length; i++) {
        if (dice[i] === 1) {
          const newRoll = Math.floor(Math.random() * 10) + 1;
          dice[i] = newRoll;
          if (newRoll >= 6) successes++;
          if (newRoll === 1) complications++;
          else complications--;
        }
      }
    }
    
    const rollResult = {
      dice,
      successes,
      complications,
      pool: dicePool,
      descriptionLevel,
      characterId,
      notes,
      userId,
      timestamp: new Date()
    };
    
    // Emit roll result to campaign
    if (io) {
      io.to(`campaign_${campaignId}`).emit('dice_rolled', rollResult);
    }
    
    return {
      type: 'roll',
      result: rollResult,
      message: `${userId} rolled ${dicePool} dice (${descriptionLevel}): ${successes} successes, ${complications} complications`
    };
  }

  // Handle XP macros
  async handleXP(params) {
    const { amount, reason, userId, characterId } = params;
    
    // In a real implementation, this would update the character's XP
    // For now, we'll just return a message
    const action = amount > 0 ? 'gained' : 'spent';
    const absAmount = Math.abs(amount);
    
    return {
      type: 'xp',
      amount: amount,
      reason: reason,
      message: `${userId} ${action} ${absAmount} XP${reason ? ` for ${reason}` : ''}`
    };
  }

  // Handle Boon macros
  async handleBoon(params) {
    const { action, details, userId, characterId } = params;
    
    if (action === 'convert') {
      return {
        type: 'boon_convert',
        message: `${userId} converted a boon${details ? `: ${details}` : ''}`
      };
    } else if (action === 'spend') {
      return {
        type: 'boon_spend',
        message: `${userId} spent a boon${details ? `: ${details}` : ''}`
      };
    }
    
    throw new Error('Invalid boon action');
  }

  // Handle Clock macros
  async handleClock(params) {
    const { action, clockName, amount, userId, campaignId, io } = params;
    
    if (action === 'tick') {
      // In a real implementation, this would update the campaign clock
      const ticks = amount || 1;
      return {
        type: 'clock_tick',
        clockName,
        ticks,
        message: `${userId} ticked clock "${clockName}" by ${ticks}`
      };
    } else if (action === 'reset') {
      return {
        type: 'clock_reset',
        clockName,
        message: `${userId} reset clock "${clockName}"`
      };
    }
    
    throw new Error('Invalid clock action');
  }

  // Handle Session macros
  async handleSession(params) {
    const { action, details, userId, campaignId, io } = params;
    
    if (action === 'start') {
      return {
        type: 'session_start',
        message: `${userId} started a new session${details ? `: ${details}` : ''}`
      };
    } else if (action === 'end') {
      return {
        type: 'session_end',
        message: `${userId} ended the session${details ? `: ${details}` : ''}`
      };
    }
    
    throw new Error('Invalid session action');
  }

  // Handle Whisper macros
  async handleWhisper(params) {
    const { target, message, userId, campaignId, io } = params;
    
    const whisperResult = {
      type: 'whisper',
      target,
      message,
      from: userId,
      timestamp: new Date()
    };
    
    // Emit whisper to target user (in a real implementation)
    // For now, we'll just return the result
    return whisperResult;
  }

  // Handle Emote macros
  async handleEmote(params) {
    const { action, userId } = params;
    
    return {
      type: 'emote',
      action,
      message: `${userId} ${action}`
    };
  }

  // Validate macro permissions
  async validateMacroPermissions(userId, campaignId, macroCommand) {
    // In a real implementation, this would check:
    // - User role (GM vs player)
    // - Macro permissions
    // - Campaign settings
    // For now, we'll allow all macros
    return true;
  }
}

module.exports = new MacroService();

