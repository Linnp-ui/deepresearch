import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5174
  },
  build: {
    target: 'es2015',
    minify: 'terser',
    cssCodeSplit: true,
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue'],
          axios: ['axios']
        }
      }
    }
  },
  optimizeDeps: {
    include: ['vue', 'axios']
  }
});
