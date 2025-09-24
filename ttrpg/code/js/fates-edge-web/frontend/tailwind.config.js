/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'fate-dark': '#1a202c',
        'fate-darker': '#161b22',
        'fate-accent': '#8b5cf6',
        'fate-success': '#10b981',
        'fate-warning': '#f59e0b',
        'fate-error': '#ef4444',
      }
    },
  },
  plugins: [],
}

