import { marked as m } from 'marked';
import redirects from '../data/redirects.json';

/** Markdown -> HTML; odkazy na pôvodný web obce sa prepíšu na nové adresy. */
export function marked(src: string) {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const html = m.parse(src, { async: false }) as string;
  return html.replace(/href="https?:\/\/(?:www\.)?mostpribratislave\.sk(\/[^"#?]*)?([^"]*)"/g, (all, path = '/', rest) => {
    const p = (path || '/').replace(/\/$/, '');
    const hit = (redirects as Record<string, string>)[p];
    return hit ? `href="${base}${hit}"` : all;
  });
}
