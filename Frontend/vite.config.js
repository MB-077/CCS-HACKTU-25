import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
<<<<<<< Updated upstream
import { resolve } from 'path';
=======
>>>>>>> Stashed changes

export default defineConfig({
<<<<<<< Updated upstream
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'), // Set up the alias
    },
  },
});
=======
  css: {
    postcss: {
      plugins: [],
    },
  },
  //  plugins: [react()],
  // resolve: {
  //   alias: {
  //     "@": path.resolve(__dirname, "./src"),
  //   },
  // },
});
>>>>>>> Stashed changes
