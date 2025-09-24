const pool = require('../config/database');

exports.create = async (characterData) => {
  const {
    userId, name, archetype, xpTotal, xpSpent, attributes, skills,
    followers, assets, talents, complications, boons
  } = characterData;

  const query = `
    INSERT INTO characters (
      userid, name, archetype, xptotal, xpspent, attributes, skills,
      followers, assets, talents, complications, boons
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    RETURNING characterid
  `;

  const values = [
    userId, name, archetype, xpTotal, xpSpent,
    JSON.stringify(attributes), JSON.stringify(skills),
    JSON.stringify(followers), JSON.stringify(assets),
    JSON.stringify(talents), JSON.stringify(complications), boons
  ];

  const result = await pool.query(query, values);
  return result.rows[0].characterid;
};

exports.findById = async (characterId) => {
  const query = `
    SELECT 
      characterid, userid, name, archetype, xptotal, xpspent,
      attributes, skills, followers, assets, talents, complications, boons,
      lastupdated
    FROM characters 
    WHERE characterid = $1
  `;
  
  const result = await pool.query(query, [characterId]);
  return result.rows[0];
};

exports.findByUserId = async (userId) => {
  const query = `
    SELECT 
      characterid, userid, name, archetype, xptotal, xpspent,
      attributes, skills, followers, assets, talents, complications, boons,
      lastupdated
    FROM characters 
    WHERE userid = $1
    ORDER BY lastupdated DESC
  `;
  
  const result = await pool.query(query, [userId]);
  return result.rows;
};

exports.update = async (characterId, updateData) => {
  const fields = [];
  const values = [];
  let index = 1;

  Object.keys(updateData).forEach(key => {
    if (key === 'attributes' || key === 'skills' || key === 'followers' || 
        key === 'assets' || key === 'talents' || key === 'complications') {
      fields.push(`${key} = $${index}`);
      values.push(JSON.stringify(updateData[key]));
    } else {
      fields.push(`${key} = $${index}`);
      values.push(updateData[key]);
    }
    index++;
  });

  // Always update lastupdated
  fields.push(`lastupdated = NOW()`);
  
  const query = `
    UPDATE characters 
    SET ${fields.join(', ')}
    WHERE characterid = $${index}
  `;
  
  values.push(characterId);
  
  await pool.query(query, values);
};

exports.delete = async (characterId) => {
  const query = 'DELETE FROM characters WHERE characterid = $1';
  await pool.query(query, [characterId]);
};

