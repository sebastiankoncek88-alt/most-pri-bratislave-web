"""Stiahne fotoalbumy z pôvodného webu obce do public/media/galeria a zapíše src/data/gallery.json.

Použitie: python3 tools/import/gallery.py <projekt>
Už stiahnuté fotky sa preskočia, takže opakované spustenie stiahne len nové albumy.
"""
import sys, os, re, json, html, io, time, hashlib, urllib.request, urllib.parse
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
BASE = 'https://www.mostpribratislave.sk'
MEDIA = os.path.join(OUT, 'public/media/galeria')
UA = {'User-Agent': 'Mozilla/5.0', 'Accept': 'image/jpeg,image/png,image/*'}

def get(url, binary=False):
    for i in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(urllib.parse.quote(url, safe=':/?&=%'), headers=UA), timeout=40)
            d = r.read()
            return d if binary else d.decode('utf-8', 'replace')
        except Exception as e:
            err = e; time.sleep(1.5)
    print('ZLYHALO', url[:110], err, file=sys.stderr)
    return None

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

# 1) zoznam albumov (aj s ďalšími stranami)
albums = []
seen = set()
page = 1
while True:
    t = get(f'{BASE}/fotogalerie' + (f'?page={page}' if page > 1 else ''))
    if not t: break
    found = [u for u in re.findall(r'href="(https://www\.mostpribratislave\.sk/fotogaleria/\d+/[^"]+)"', t) if u not in seen]
    if not found: break
    for u in found:
        seen.add(u); albums.append(u)
    page += 1
    if page > 20: break

MON = {}
result = []
done_ids = set()
for au in albums:
    aid, aslug = re.search(r'/fotogaleria/(\d+)/([^/?#]+)', au).groups()
    if aid in done_ids: continue
    done_ids.add(aid)
    t = get(au)
    if not t: continue
    c = t[t.find('id="content"'):]
    # fotky albumu sú len v hlavnej časti stránky (<main id="main">); bočné bloky obsahujú náhodné fotky iných albumov
    mi = t.find('id="main"')
    if mi != -1:
        me = t.find('</main>', mi)
        main_part = t[mi:me if me != -1 else None]
    else:
        main_part = c
    title = html.unescape(re.sub(r'<[^>]+>', '', (re.findall(r'<h1[^>]*>(.*?)</h1>', c, re.S) or [aslug])[0])).strip()
    for a_, b_ in (('Deň Obce', 'Deň obce'), ('Suťaž', 'Súťaž'), ('Gulášu', 'gulášu'), ('topánok?', 'topánok')):
        title = title.replace(a_, b_)
    dm = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', c)
    date = f'{dm.group(3)}-{int(dm.group(2)):02d}-{int(dm.group(1)):02d}' if dm else None
    # varianty: _lg (veľká, h=2000) a _sm (náhľad)
    urls = [html.unescape(x) for x in re.findall(r'https://picturium\.moderneobce\.sk/data/gallery/[^"\s,]+token=[0-9a-f]+', main_part)]
    photos = {}
    for u in urls:
        path = u.split('?')[0]
        m = re.match(r'(.*)_(lg|sm|md|xs)\.(\w+)$', path)
        if not m: continue
        key = m.group(1)
        photos.setdefault(key, {'order': len(photos)})
        photos[key].setdefault(m.group(2), []).append(u)
    items = []
    adir = os.path.join(MEDIA, aid)
    os.makedirs(adir, exist_ok=True)
    for key, v in sorted(photos.items(), key=lambda kv: kv[1]['order']):
        name = hashlib.sha1(key.encode()).hexdigest()[:12]
        big, thumb = os.path.join(adir, name + '.jpg'), os.path.join(adir, name + '-n.jpg')
        if not (os.path.exists(big) and os.path.exists(thumb)):
            cands = sorted(v.get('lg', []), key=lambda u: 0 if 'h=2000' in u else 1) + v.get('md', []) + sorted(v.get('sm', []), key=lambda u: -int((re.search(r'w=(\d+)', u) or [0, 0])[1]))
            data = None
            for cu in cands:
                data = get(cu, binary=True)
                if data and len(data) > 1000: break
            if not data: continue
            try:
                im = Image.open(io.BytesIO(data)).convert('RGB')
            except Exception as e:
                print('NEPLATNÝ OBRÁZOK', key, e, file=sys.stderr); continue
            im2 = im.copy(); im2.thumbnail((1600, 1600)); im2.save(big, 'JPEG', quality=80, optimize=True, progressive=True)
            im3 = im.copy(); im3.thumbnail((520, 520)); im3.save(thumb, 'JPEG', quality=74, optimize=True, progressive=True)
        with Image.open(big) as bi:
            w, h = bi.size
        items.append({'src': f'/media/galeria/{aid}/{name}.jpg', 'thumb': f'/media/galeria/{aid}/{name}-n.jpg', 'w': w, 'h': h})
    if not items: continue
    result.append({'id': aid, 'slug': aslug, 'title': title, 'date': date, 'photos': items})
    print(f'{title}: {len(items)} fotiek', file=sys.stderr)

result.sort(key=lambda a: a['date'] or '', reverse=True)
# zmazať fotky, ktoré už nepatria do žiadneho albumu (album zmazaný alebo upravený na starom webe)
if result:
    keep = {p[k].split('/')[-1] for a in result for p in a['photos'] for k in ('src', 'thumb')}
    keep_dirs = {a['id'] for a in result}
    removed = 0
    for d in os.listdir(MEDIA):
        dp = os.path.join(MEDIA, d)
        if not os.path.isdir(dp): continue
        for f in os.listdir(dp):
            if d not in keep_dirs or f not in keep:
                os.remove(os.path.join(dp, f)); removed += 1
        if not os.listdir(dp): os.rmdir(dp)
    if removed: print(f'zmazaných starých fotiek: {removed}', file=sys.stderr)
json.dump(result, open(os.path.join(OUT, 'src/data/gallery.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'albumov {len(result)}, fotiek {sum(len(a["photos"]) for a in result)}', file=sys.stderr)
