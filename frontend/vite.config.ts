import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
/// <reference types="vitest" />

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      { find: '@', replacement: '/src' },
      { find: '@components', replacement: '/src/components' },
      { find: '@queries', replacement: '/src/queries' },
      { find: '@types', replacement: '/src/types' }
    ]
  },
  // @ts-expect-error - Vitest configuration
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
  },
})
