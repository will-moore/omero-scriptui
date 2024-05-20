import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  build: {
    sourcemap: true,
    // output into Django's static dir
    outDir: "./omero_scriptui/static/omero_scriptui/"
  },
})
