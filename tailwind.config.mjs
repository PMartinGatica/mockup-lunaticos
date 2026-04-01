import animations from 'tailwindcss-animated'

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        oswald: ['Oswald', 'sans-serif'],
        dm: ['"DM Sans"', 'sans-serif'],
      },
      colors: {
        primary: '#00C040',       // verde neón del logo
        'primary-light': '#33DD66',
        'primary-dark': '#009930',
        danger: '#CC0000',        // rojo del logo
        'danger-light': '#EE2222',
        surface: '#111111',
        'surface-2': '#1A1A1A',
      },
    },
  },
  plugins: [
    animations,
    ({ addComponents }) => {
      addComponents({
        '.cp-v': {
          clipPath: 'polygon(0 0, 100% 0, 100% 85%, 50% 100%, 50% 100%, 0 85%)',
        },
      })
    },
  ],
}
