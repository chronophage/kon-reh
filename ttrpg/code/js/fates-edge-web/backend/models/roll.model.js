const pool = require('../config/database');

exports.create = async (rollData) => {
  const { userId, characterId, pool, descriptionLevel, dice, successes, complications, notes } = rollData;

  const query = `
    INSERT INTO roll_history (
      userid, characterid, pool, descriptionlevel, dice, successes, complications, notes, rolledat
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
    RETURNING rollid
  `;

  const values = [
    userId, characterId, pool, descriptionLevel,
    JSON.stringify(dice), successes, complications, notes || ''
  ];

  const result = await pool.query(query, values);
  return result.rows[0].rollid;
};

exports.findByCharacterId = async (characterId) => {
  const query = `
    SELECT 
      rollid, userid, characterid, pool, descriptionlevel, dice, 
      successes, complications, notes, rolledat
    FROM roll_history 
    WHERE characterid = $1
    ORDER BY rolledat DESC
    LIMIT 50
  `;
  
  const result = await pool.query(query, [characterId]);
  return result.rows;
};

exports.findByUserId = async (userId, limit = 20) => {
  const query = `
    SELECT 
      rollid, userid, characterid, pool, descriptionlevel, dice, 
      successes, complications, notes, rolledat
    FROM roll_history 
    WHERE userid = $1
    ORDER BY rolledat DESC
    LIMIT $2
  `;
  
  const result = await pool.query(query, [userId, limit]);
  return result.rows;
};

