const pool = require('../config/database');

exports.create = async (macroData) => {
  const { userId, campaignId, name, command, description, isPublic = false, isApproved = false } = macroData;

  const query = `
    INSERT INTO macros (
      userid, campaignid, name, command, description, ispublic, isapproved, createdat
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
    RETURNING macroid
  `;

  const values = [userId, campaignId, name, command, description, isPublic, isApproved];
  const result = await pool.query(query, values);
  return result.rows[0].macroid;
};

exports.findById = async (macroId) => {
  const query = `
    SELECT 
      macroid, userid, campaignid, name, command, description, 
      ispublic, isapproved, createdat
    FROM macros 
    WHERE macroid = $1
  `;
  
  const result = await pool.query(query, [macroId]);
  return result.rows[0];
};

exports.findByCampaignId = async (campaignId) => {
  const query = `
    SELECT 
      m.macroid, m.userid, m.campaignid, m.name, m.command, m.description, 
      m.ispublic, m.isapproved, m.createdat,
      u.username as creatorname
    FROM macros m
    JOIN users u ON m.userid = u.userid
    WHERE m.campaignid = $1 
      AND (m.ispublic = true OR m.isapproved = true)
    ORDER BY m.createdat DESC
  `;
  
  const result = await pool.query(query, [campaignId]);
  return result.rows;
};

exports.findByUserId = async (userId) => {
  const query = `
    SELECT 
      macroid, userid, campaignid, name, command, description, 
      ispublic, isapproved, createdat
    FROM macros 
    WHERE userid = $1
    ORDER BY createdat DESC
  `;
  
  const result = await pool.query(query, [userId]);
  return result.rows;
};

exports.findByCampaignAndUser = async (campaignId, userId) => {
  const query = `
    SELECT 
      macroid, userid, campaignid, name, command, description, 
      ispublic, isapproved, createdat
    FROM macros 
    WHERE campaignid = $1 AND userid = $2
    ORDER BY createdat DESC
  `;
  
  const result = await pool.query(query, [campaignId, userId]);
  return result.rows;
};

exports.update = async (macroId, updateData) => {
  const fields = [];
  const values = [];
  let index = 1;

  Object.keys(updateData).forEach(key => {
    fields.push(`${key} = $${index}`);
    values.push(updateData[key]);
    index++;
  });

  const query = `
    UPDATE macros 
    SET ${fields.join(', ')}
    WHERE macroid = $${index}
  `;
  
  values.push(macroId);
  
  await pool.query(query, values);
};

exports.delete = async (macroId) => {
  const query = 'DELETE FROM macros WHERE macroid = $1';
  await pool.query(query, [macroId]);
};

exports.getPendingMacros = async (campaignId) => {
  const query = `
    SELECT 
      m.macroid, m.userid, m.campaignid, m.name, m.command, m.description, 
      m.ispublic, m.isapproved, m.createdat,
      u.username as creatorname
    FROM macros m
    JOIN users u ON m.userid = u.userid
    WHERE m.campaignid = $1 AND m.isapproved = false AND m.ispublic = false
    ORDER BY m.createdat ASC
  `;
  
  const result = await pool.query(query, [campaignId]);
  return result.rows;
};

