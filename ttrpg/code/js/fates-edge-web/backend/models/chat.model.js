const pool = require('../config/database');

exports.createMessage = async (messageData) => {
  const { campaignId, userId, characterId, content, channel = 'general', targetUserId = null } = messageData;

  const query = `
    INSERT INTO chat_messages (
      campaignid, userid, characterid, content, channel, targetuserid, createdat
    )
    VALUES ($1, $2, $3, $4, $5, $6, NOW())
    RETURNING messageid
  `;

  const values = [campaignId, userId, characterId, content, channel, targetUserId];
  const result = await pool.query(query, values);
  return result.rows[0].messageid;
};

exports.getMessagesByCampaign = async (campaignId, limit = 50) => {
  const query = `
    SELECT 
      cm.messageid, cm.campaignid, cm.userid, cm.characterid, cm.content, 
      cm.channel, cm.targetuserid, cm.createdat,
      u.username,
      c.name as charactername
    FROM chat_messages cm
    JOIN users u ON cm.userid = u.userid
    LEFT JOIN characters c ON cm.characterid = c.characterid
    WHERE cm.campaignid = $1
    ORDER BY cm.createdat DESC
    LIMIT $2
  `;
  
  const result = await pool.query(query, [campaignId, limit]);
  return result.rows.reverse(); // Return in chronological order
};

exports.getMessagesByChannel = async (campaignId, channel, limit = 50) => {
  const query = `
    SELECT 
      cm.messageid, cm.campaignid, cm.userid, cm.characterid, cm.content, 
      cm.channel, cm.targetuserid, cm.createdat,
      u.username,
      c.name as charactername
    FROM chat_messages cm
    JOIN users u ON cm.userid = u.userid
    LEFT JOIN characters c ON cm.characterid = c.characterid
    WHERE cm.campaignid = $1 AND cm.channel = $2
    ORDER BY cm.createdat DESC
    LIMIT $3
  `;
  
  const result = await pool.query(query, [campaignId, channel, limit]);
  return result.rows.reverse();
};

