import { defineConfig } from 'astro/config';

// Pri nasadení na GitHub Pages je web v podpriečinku (/<repozitár>/).
// Pri vlastnej doméne (napr. mostpribratislave.sk) nechajte BASE prázdne.
const base = process.env.BASE_PATH || '/';
const site = process.env.SITE_URL || 'https://www.mostpribratislave.sk';

// Doplní base path pred interné odkazy v markdown obsahu (/urad/... -> /repo/urad/...)
function rehypeBase() {
  const prefix = base.replace(/\/$/, '');
  return (tree) => {
    if (!prefix) return;
    const walk = (node) => {
      if (node.type === 'element') {
        for (const attr of ['href', 'src']) {
          const v = node.properties?.[attr];
          if (typeof v === 'string' && v.startsWith('/') && !v.startsWith('//') && !v.startsWith(prefix + '/')) {
            node.properties[attr] = prefix + v;
          }
        }
      }
      if (node.type === 'raw' && typeof node.value === 'string') {
        node.value = node.value.replace(/(href|src)="\/(?!\/)/g, `$1="${prefix}/`);
      }
      (node.children || []).forEach(walk);
    };
    walk(tree);
  };
}

export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  markdown: { rehypePlugins: [rehypeBase] },
  build: { format: 'directory' },
  // Stabilné názvy súborov (bez hashu): stránka uložená v pamäti prehliadača počas
  // aktualizácie webu nikdy neodkazuje na zmazaný súbor dizajnu.
  vite: {
    build: {
      rollupOptions: {
        output: {
          assetFileNames: '_astro/[name][extname]',
        },
      },
    },
  },
});
