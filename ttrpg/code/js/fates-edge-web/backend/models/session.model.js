const pool = require('../config/database');

exports.create = async (sessionData) => {
  const { campaignId, date, notes, attendance, xpAwards } = sessionData;

  const query = `
    INSERT INTO sessions (
      campaignid, date, notes, attendance, xprewards, createdat
    )
    VALUES ($1, $2, $3, $4, $5, NOW())
    RETURNING sessionid
  `;

  const values = [
    campaignId, date, notes, 
    attendance, 
    JSON.stringify(xpAwards)
  ];

  const result = await pool.query(query, values);
  return result.rows[0].sessionid;
};

exports.findById = async (sessionId) => {
  const query = `
    SELECT 
      sessionid, campaignid, date, notes, attendance, xprewards, createdat
    FROM sessions 
    WHERE sessionid = $1
  `;
  
  const result = await pool.query(query, [sessionId]);
  return result.rows[0];
};

exports.findByCampaignId = async (campaignId) => {
  const query = `
    SELECT 
      sessionid, campaignid, date, notes, attendance, xprewards, createdat
    FROM sessions 
    WHERE campaignid = $1
    ORDER BY date DESC
  `;
  
  const result = await pool.query(query, [campaignId]);
  return result.rows;
};

exports.update = async (sessionId, updateData) => {
  const fields = [];
  const values = [];
  let index = 1;

  Object.keys(updateData).forEach(key => {
    if (key === 'attendance' || key === 'xprewards') {
      fields.push(`${key} = $${index}`);
      values.push(updateData[key]);
    } else {
      fields.push(`${key} = $${index}`);
      values.push(updateData[key]);
    }
    index++;
  });

  const query = `
    UPDATE sessions 
    SET ${fields.join(', ')}
    WHERE sessionid = $${index}
  `;
  
  values.push(sessionId);
  
  await pool.query(query, values);
};

