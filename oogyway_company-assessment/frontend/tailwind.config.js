/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f7ff',
          100: '#e0effe',
          500: '#0284c7',
          600: '#0369a1',
          700: '#075985',
          900: '#0c4a6e',
        },
        dark: {
          bg: '#0b0f19',
          card: '#111827',
          sidebar: '#0d1322',
          border: '#1f293d',
        }
      }
    },
  },
  plugins: [],
}
