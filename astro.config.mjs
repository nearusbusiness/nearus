import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  site: 'https://nearus.com.au',
  integrations: [sitemap()],
  adapter: cloudflare(),
});