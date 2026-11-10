"""Prevezme posledné podnety občanov a odpovede obce z pôvodného webu do src/data/podnety.json.

Z ochrany osobných údajov sa NEprenáša text podnetu ani meno občana –
len názov, stav, dátumy a odpoveď obce.
Použitie: python3 tools/import/podnety.py <projekt> [počet strán]
"""
import sys, os, re, json, time, urllib.request
from bs4 import BeautifulSoup
from markdownify import markdownify as md

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
PAGES = int(sys.argv[2]) if len(sys.argv) > 2 else 3
BASE = 'https://www.mostpribratislave.sk'

def get(url):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode('utf-8', 'replace')
        except Exception as e:
            err = e; time.sleep(2)
    print('ZLYHALO', url, err, file=sys.stderr)

def iso(d):
    m = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', d or '')
    return f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}' if m else None

links = []
for p in range(1, PAGES + 1):
    t = get(f'{BASE}/podnety-a-otazky' + (f'?page={p}' if p > 1 else ''))
    if not t: break
    for u in re.findall(r'href="(https://www\.mostpribratislave\.sk/podnety-a-otazky/\d+/[^"]+)"', t):
        if u not in links: links.append(u)

stats = None
t0 = get(f'{BASE}/')
if t0:
    m = re.search(r'Podnety:\s*(\d+)\s*v riešení\s*(\d+)\s*vyriešených', re.sub(r'<[^>]+>|\s+', ' ', t0))
    if m: stats = {'open': int(m.group(1)), 'solved': int(m.group(2))}

items = []
for u in links:
    t = get(u)
    if not t: continue
    s = BeautifulSoup(t, 'html.parser')
    c = s.find(id='content')
    if not c: continue
    title = c.find('h1').get_text(' ', strip=True) if c.find('h1') else ''
    text = c.get_text('\n', strip=True)
    status = (re.search(r'Stav riešenia:\s*\n([^\n]+)', text) or [None, ''])[1]
    received = (re.search(r'Prijatý:\s*\n([0-9.]+)', text) or [None, None])[1]
    answered = (re.search(r'Zodpovedaný:\s*\n([0-9.]+)', text) or [None, None])[1]
    answer = ''
    h = c.find(lambda tag: tag.name in ('h2', 'h3') and tag.get_text(strip=True) == 'Odpoveď')
    if h:
        parts = []
        for sib in h.find_next_siblings():
            if sib.name in ('h2', 'h3'): break
            parts.append(str(sib))
        answer = md(''.join(parts), heading_style='ATX').strip()
        answer = re.sub(r'\n{3,}', '\n\n', answer)
        answer = answer.split('[Preskočiť na obsah]')[0].strip()
    title = title[:1].upper() + title[1:]
    items.append({'id': re.search(r'/(\d+)/', u.replace(BASE, '')).group(1), 'title': title, 'status': status,
                  'received': iso(received), 'answered': iso(answered), 'answer': answer, 'url': u})
    time.sleep(0.2)

json.dump({'stats': stats, 'items': items}, open(os.path.join(OUT, 'src/data/podnety.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'podnetov {len(items)}, štatistika {stats}', file=sys.stderr)
