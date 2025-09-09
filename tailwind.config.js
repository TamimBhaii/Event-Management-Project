/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./system/templates/**/*.html",
    "./system/templates/*.html",
    "./system/**/*.py",
  ],
  safelist: [
    { pattern: /.*/ }, // keep all classes (force include)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
