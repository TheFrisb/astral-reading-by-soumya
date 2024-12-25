/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './core/templates/core/*.html',
    './core/templates/core/**/*.html',
    './blog/templates/blog/*.html',
    './blog/templates/blog/**/*.html',
    './booking/templates/booking/*.html',
    './src/components/*.js',
    './src/components/**/*.js',
    './static/icons/*.svg',
  ],
  theme: {
    extend: {
      fontFamily: {
        'open-sans': ['Open Sans', 'sans-serif'],
        cormorant: ['Cormorant', 'serif'],
      },
      colors: {
        'textColor': '#1b110d',
        'backgroundColor': '#fdfcfb',
        'primary': '#c06d4a',
        'secondary': '#dfa58e',
        'accent': '#dd8d6b',
      },
    },
  },
  plugins: [],
}

