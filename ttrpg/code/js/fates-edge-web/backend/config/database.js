const { Pool } = require('pg');
const dotenv = require('dotenv');

dotenv.config();

// For Docker environment
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://fateuser:fatepass@localhost:5432/fatesedge',
  ssl: false
});

pool.on('connect', () => {
  console.log('Connected to PostgreSQL database');
});

pool.on('error', (err) => {
  console.error('Database connection error:', err);
});

module.exports = pool;

