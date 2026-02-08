import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: '/analizador_videos/', // Repository name for GitHub Pages
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Listen on all addresses (including LAN)
    port: 5173,
    proxy: {
      '/analyze': 'http://localhost:8000',
      '/history': 'http://localhost:8000',
      '/download': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    }
  }
})
