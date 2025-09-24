const pool = require('../config/database');

exports.create = async (campaignData) => {
  const { gmId, name, description, players, status } = campaignData;

  const query = `
    INSERT INTO campaigns (gmid, name, description, players, status, createdat)
    VALUES ($1, $2, $3, $4, $5, NOW())
    RETURNING campaignid
  `;

  const values = [gmId, name, description, players, status];
  const result = await pool.query(query, values);
  return result.rows[0].campaignid;
};

exports.findById = async (campaignId) => {
  const query = `
    SELECT 
      campaignid, gmid, name, description, players, status, createdat
    FROM campaigns 
    WHERE campaignid = $1
  `;
  
  const result = await pool.query(query, [campaignId]);
  return result.rows[0];
};

exports.findByUser = async (userId) => {
  // Find campaigns where user is GM or player
  const query = `
    SELECT 
      campaignid, gmid, name, description, players, status, createdat
    FROM campaigns 
    WHERE gmid = $1 OR $1 = ANY(players)
    ORDER BY createdat DESC
  `;
  
  const result = await pool.query(query, [userId]);
  return result.rows;
};

exports.update = async (campaignId, updateData) => {
  const fields = [];
  const values = [];
  let index = 1;

  Object.keys(updateData).forEach(key => {
    if (key === 'players') {
      fields.push(`${key} = $${index}`);
      values.push(updateData[key]);
    } else {
      fields.push(`${key} = $${index}`);
      values.push(updateData[key]);
    }
    index++;
  });

  const query = `
    UPDATE campaigns 
    SET ${fields.join(', ')}
    WHERE campaignid = $${index}
  `;
  
  values.push(campaignId);
  
  await pool.query(query, values);
};

