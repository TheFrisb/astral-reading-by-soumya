/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './core/templates/core/*.html',
    './core/templates/core/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        'open-sans': ['Open Sans', 'sans-serif'],
        cormorant: ['Cormorant', 'serif'],
      }
    },
  },
  plugins: [],
}

