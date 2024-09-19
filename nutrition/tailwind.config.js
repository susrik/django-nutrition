/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/nutrition/*.html',
    '*.py'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
}

