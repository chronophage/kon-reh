const pool = require('../config/database');

exports.create = async (userData) => {
  const { username, email, passwordHash, role = 'player' } = userData;
  
  const query = `
    INSERT INTO users (username, email, passwordhash, role, createdat)
    VALUES ($1, $2, $3, $4, NOW())
    RETURNING userid
  `;
  
  const values = [username, email, passwordHash, role];
  const result = await pool.query(query, values);
  return result.rows[0].userid;
};

exports.findByEmail = async (email) => {
  const query = 'SELECT * FROM users WHERE email = $1';
  const result = await pool.query(query, [email]);
  return result.rows[0];
};

exports.findById = async (userId) => {
  const query = 'SELECT userid, username, email, role FROM users WHERE userid = $1';
  const result = await pool.query(query, [userId]);
  return result.rows[0];
};

