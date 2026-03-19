import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    globals: true,
    include: ['tests/components/**/*.test.{ts,tsx}'],
    exclude: ['tests/e2e/**'],
  },
  resolve: {
    alias: {
      '@site': path.resolve(__dirname),
      '@theme-original/MDXComponents': path.resolve(__dirname, 'tests/__mocks__/docusaurus.ts'),
      '@docusaurus/Link': path.resolve(__dirname, 'tests/__mocks__/docusaurusLink.tsx'),
    },
  },
});
