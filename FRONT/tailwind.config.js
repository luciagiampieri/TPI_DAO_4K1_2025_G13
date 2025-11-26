/** @type {import('tailwindcss').Config} */
export default {
  content: [
    // Asegúrate de que estas rutas coincidan con tu estructura:
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Esto le dice que busque en toda la carpeta src
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}