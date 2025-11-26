import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  // 1. Plugins: Añade la funcionalidad para compilar código React (JSX)
  plugins: [react()], 
  
  // 2. Servidor: Configuración para el entorno de desarrollo
  server: {
    // Especifica el puerto para el frontend. 
    // Por defecto es 5173, pero si necesitas otro, lo defines aquí.
    port: 5173, 
    
    proxy: {
      '/api': { 
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  },

  // 3. Configuración para el build de producción
  build: {
    // Directorio de salida. Aquí se genera la carpeta 'dist'
    outDir: 'dist', 
    // Otras opciones de optimización
  },
});