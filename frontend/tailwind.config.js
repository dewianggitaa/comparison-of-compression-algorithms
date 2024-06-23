/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'press-start': ['"Press Start 2P"', 'cursive'],
      }
    },
    colors: {
      'blue': '#43AAAD',
      "dark-blue": "#08434A",
      'black': '#000000',
      'white': '#FFFFFF',
      'yellow': '#FFC857',
      'pink': '#E975A6',
      'cream': '#FFEACA'
    }
  },
  plugins: [],
}