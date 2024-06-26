module.exports = {
  content: [
    'src/**/*.{ts,html}',
  ],
  theme: {
    container: {
      center: true,
    },
    extend: {},
  },
  plugins: [require('@tailwindcss/typography'), require('daisyui')],
}
