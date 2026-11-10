import { getCollection, type CollectionEntry } from 'astro:content';

export type Page = CollectionEntry<'pages'>;
export type News = CollectionEntry<'news'>;

const collator = new Intl.Collator('sk');

export async function sectionPages(section: string) {
  const all = await getCollection('pages', (p) => p.data.section === section);
  return all.sort((a, b) => a.data.order - b.data.order || collator.compare(a.data.title, b.data.title));
}

/** Stránky sekcie zoskupené podľa skupiny (len hlavné stránky, bez podstránok). */
export function groupPages(pages: Page[]) {
  const groups = new Map<string, { top: Page; children: Page[] }[]>();
  const tops = pages.filter((p) => !p.data.parent);
  for (const top of tops) {
    const g = top.data.group || 'Ďalšie';
    if (!groups.has(g)) groups.set(g, []);
    const slug = top.id.split('/').slice(1).join('/');
    const children = sortChildren(pages.filter((c) => c.data.parent === slug));
    groups.get(g)!.push({ top, children });
  }
  return groups;
}

export type NavItem = { id: string; title: string; href: string; order: number; group: string; children: NavItem[] };

/** Strom navigácie sekcie: importované/vlastné stránky + špeciálne stránky (fotogaléria, podujatia…). */
export async function sectionTree(section: string) {
  const { extraLinks } = await import('../data/site');
  const pages = await sectionPages(section);
  const toItem = (p: Page): NavItem => ({ id: p.id, title: p.data.title, href: pageUrl(p), order: p.data.order, group: p.data.group || 'Ďalšie', children: [] });
  const tops: NavItem[] = pages.filter((p) => !p.data.parent).map((top) => {
    const slug = top.id.split('/').slice(1).join('/');
    return { ...toItem(top), children: sortChildren(pages.filter((c) => c.data.parent === slug)).map(toItem) };
  });
  for (const x of extraLinks[section] || []) tops.push({ id: x.href, title: x.title, href: x.href, order: x.order, group: x.group, children: [] });
  tops.sort((a, b) => a.order - b.order || collator.compare(a.title, b.title));
  const groups = new Map<string, NavItem[]>();
  for (const t of tops) {
    if (!groups.has(t.group)) groups.set(t.group, []);
    groups.get(t.group)!.push(t);
  }
  return groups;
}

/** Podstránky: ak všetky obsahujú rok, zoradia sa od najnovšieho, inak abecedne. */
export function sortChildren(list: Page[]) {
  const year = (p: Page) => Number(p.data.title.match(/(19|20)\d\d/)?.[0] || 0);
  if (list.length && list.every((p) => year(p))) return [...list].sort((a, b) => year(b) - year(a));
  return [...list].sort((a, b) => collator.compare(a.data.title, b.data.title));
}

export function pageUrl(p: Page) {
  return `/${p.id}/`;
}

export async function allNews() {
  return (await getCollection('news')).sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export function newsUrl(n: News) {
  return `/aktuality/spravy/${n.id}/`;
}

export function fmtDate(d: Date, opts: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'numeric', year: 'numeric' }) {
  return new Intl.DateTimeFormat('sk-SK', { ...opts, timeZone: 'Europe/Bratislava' }).format(d);
}

/** Výťah najnovších položiek z úradnej tabule (z importovaného obsahu). */
export async function boardItems(limit = 5) {
  const all = await getCollection('pages', (p) => p.id === 'uradna-tabula/uradna-tabula');
  const body = all[0]?.body || '';
  const items = [...body.matchAll(/<li><time>([^<]+)<\/time><a href="([^"]+)">([^<]+)<\/a>/g)].map((m) => ({
    date: m[1], href: m[2], title: m[3].replace(/&amp;/g, '&').replace(/&quot;/g, '"'),
  }));
  return items.slice(0, limit);
}

export const eventId = (e: { url: string; date: string }) => 'e-' + e.date + '-' + e.url.split('/').pop();
