/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // otomochi ブランドカラー
        primary: {
          DEFAULT: '#de8f7d',
          light: '#e9a896',
          dark: '#d37a64',
        },
        background: {
          DEFAULT: '#FFF4E9',
          dark: '#f5e8d9',
        },
      },
    },
  },
  plugins: [],
}
