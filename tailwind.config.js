module.exports = {
  purge: ['./heatmaps/static/js/*.{js,jsx,ts,tsx}', './heatmaps/templates/*.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'orange-red': '#F53500'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
