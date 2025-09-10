module.exports = {
  content: [
    './gavel/templates/**/*.{html,js}',
    './gavel/templates/*.{html,js}',
    './gavel/static/js/admin/*.{html,js}',
  ],
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [],
  prefix: 'hc-',
}
