const cssnano = require('cssnano')
const isProd = process.env.NODE_ENV === "production"

module.exports = {
  modules: true,
  plugins: [
    require('postcss-import'),
    require('@tailwindcss/nesting'),
    require('tailwindcss'),
    require('autoprefixer')(),
    require('postcss-url'),
    require('postcss-preset-env')({
      features: {
          'nesting-rules': false
      },
      browsers: [
          '> 1%',
          'last 2 versions',
          'Firefox ESR',
      ]
    }),

    isProd 
    ? cssnano({preset: 'default'}) 
    : null
  ],
};