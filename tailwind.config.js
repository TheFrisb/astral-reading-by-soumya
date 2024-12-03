/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './core/templates/core/*.html',
    './core/templates/core/**/*.html',
    './blog/templates/blog/*.html',
    './blog/templates/blog/**/*.html',
    './src/components/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        'open-sans': ['Open Sans', 'sans-serif'],
        cormorant: ['Cormorant', 'serif'],
      },
      colors: {
        "gold": '#FFD700',
        "softLavender": '#E0E0FF',

        // Background Colors
        "deepNavy": '#1A1A2E',
        "mutedIndigo": '#3E497A',
        "mysticalTeal": '#008080',

        // Text Colors
        "white": '#FFFFFF',
        "lightGrayishBlue": '#D9D9E8',
        "goldAccent": '#FFD700',

        // Accent Colors
        "cosmicCoral": '#FF6F61',
        "emeraldGreen": '#4CAF50',
        "skyBlue": '#64B5F6',

        // Borders & Dividers
        "softGold": '#FFC300',
        "mutedSilver": '#B3B3CC',
      },

      backgroundImage: {
        'star-pattern': "url('/static/assets/star-pattern.png')",

        'galactic-breeze': 'linear-gradient(120deg, #008080 0%, #3E497A 100%)',
        // Stellar Radiance
        'stellar-radiance': 'linear-gradient(135deg, #FFD700 0%, #E0E0FF 100%)',
        'test': 'radial-gradient( circle 815px at 23.4% -21.8%,  rgba(9,29,85,1) 0.2%, rgba(0,0,0,1) 100.2% )',
        'test2': 'linear-gradient( 109.6deg,  rgba(68,50,41,1) 11.2%, rgba(83,63,52,1) 47.7%, rgba(153,86,15,1) 100.2% )',
        // Aurora Glow
        'aurora-glow': 'linear-gradient(45deg, #4CAF50 0%, #1A1A2E 100%)',
        // Cosmic Sunset
        'cosmic-sunset': 'linear-gradient(135deg, #FF6F61 0%, #FFD700 100%)',
      }
    },
  },
  plugins: [],
}

