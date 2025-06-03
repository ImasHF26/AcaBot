// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // Importez le module 'path' de Node.js

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // Définit '@' comme un alias pour le dossier src
    },
  },
})

// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [vue()],
// })
