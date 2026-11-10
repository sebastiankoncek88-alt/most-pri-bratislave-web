import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const pages = defineCollection({
  loader: glob({
    pattern: '**/*.md',
    base: './src/content/pages',
    generateId: ({ entry }) => entry.replace(/\.md$/, '').replace(/\/index$/, ''),
  }),
  schema: z.object({
    title: z.string(),
    section: z.enum(['urad', 'odpady', 'samosprava', 'uradna-tabula', 'aktuality', 'obec', 'kontakt']),
    group: z.string().optional(),
    order: z.number().default(50),
    parent: z.string().optional(),
    description: z.string().optional(),
    updated: z.coerce.date().optional(),
    source: z.string().optional(),
  }),
});

const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    category: z.string().default('Oznam'),
    time: z.string().optional(),
    image: z.string().optional(),
    excerpt: z.string().optional(),
    important: z.boolean().default(false),
    source: z.string().optional(),
  }),
});

export const collections = { pages, news };
