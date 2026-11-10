"""Import obsahu z pôvodného webu (ModerneObce.sk) do Astro content collections.

Použitie:
  python3 -I tools/import/import.py <data_dir> <kalendar.html> <out_project_dir>

<data_dir> obsahuje pages.json a news.json vytvorené crawlerom.
Skript prepíše src/content/pages, src/content/news a src/data/events.json.
"""
import sys, os, re, json, html, shutil, datetime

DATA, KAL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
OLD = 'https://www.mostpribratislave.sk'

# ---------------------------------------------------------------------------
# Nová informačná architektúra: starý identifikátor -> (sekcia, slug, skupina, poradie, titulok)
# None v slugu = stránka sa neprenáša (duplicita, prázdna, testovacia, len rozcestník)
# ---------------------------------------------------------------------------
M = {}
def m(old, section, slug, group=None, order=50, title=None):
    M[old] = dict(section=section, slug=slug, group=group, order=order, title=title)

# Úrad a služby
m('1401', 'urad', 'kontakty-na-referaty', 'Obecný úrad', 1, 'Kontakty na referáty')
m('13691/matricny-urad', 'urad', 'matrika', 'Doklady a osobné veci', 10, 'Matrika')
m('13700', 'urad', 'evidencia-obyvatelstva', 'Doklady a osobné veci', 11, 'Trvalý pobyt a evidencia obyvateľov')
m('26562', 'urad', 'dane-a-poplatky', 'Dane a financie', 20, 'Dane a poplatky')
m('22750', 'urad', 'socialne-veci', 'Dane a financie', 21, 'Sociálne veci a ekonomika')
m('14165', 'urad', 'stavebny-urad', 'Stavanie a územie', 30, 'Stavebný úrad')
m('31443', 'urad', 'uzemny-rozvoj', 'Stavanie a územie', 31, 'Územný rozvoj a plánovanie')
m('27764', 'urad', 'udrzba-verejnych-priestorov', 'Stavanie a územie', 32, 'Údržba verejných priestorov a zelene')
m('25860', 'urad', 'nefunkcne-osvetlenie', 'Stavanie a územie', 33, 'Nefunkčné osvetlenie a rozhlas')
m('25845', 'urad', 'podatelna', 'Obecný úrad', 2, 'Podateľňa a sekretariát')
m('25848', 'urad', 'priestupky', 'Obecný úrad', 3, 'Priestupky')
m('25846', 'urad', 'personalny-a-mzdovy', 'Obecný úrad', 4, 'Personálny a mzdový referát')
m('27761', 'urad', 'projekty-a-obstaravanie', 'Obecný úrad', 5, 'Projekty a verejné obstarávanie')
m('31268', 'urad', 'obecna-policia', 'Bezpečnosť', 40, 'Obecná polícia')
m('1450', 'urad', 'obecny-rozhlas', 'Obecný úrad', 6, 'Hlásenie v obecnom rozhlase')
for x in ('1405', '13690', '13691/matrika', '27762', '27763', '1445'):
    m(x, None, None)

# Odpady
m('14159', 'odpady', 'odpadove-hospodarstvo', 'Základné informácie', 1, 'Odpadové hospodárstvo v obci')
m('14161', 'odpady', 'harmonogram', 'Základné informácie', 0, 'Harmonogram vývozu odpadu')
m('14163', 'odpady', 'oznamy', 'Základné informácie', 2, 'Aktuálne oznamy k odpadom')
m('25729', 'odpady', 'reklamacia-vyvozu', 'Základné informácie', 3, 'Reklamácia vývozu a poškodených nádob')
m('25733', 'odpady', 'referat-odpadov', 'Základné informácie', 4, 'Referát odpadov a životného prostredia')
m('27635', 'odpady', 'objemny-odpad', 'Zber podľa druhu', 10, 'Objemný odpad')
m('29152', 'odpady', 'elektroodpad', 'Zber podľa druhu', 11, 'Elektroodpad')
m('29801', 'odpady', 'konare-a-stromy', 'Zber podľa druhu', 12, 'Konáre a stromy')
m('31144', 'odpady', 'nebezpecny-odpad', 'Zber podľa druhu', 13, 'Nebezpečný odpad')
m('25728', 'odpady', 'textil-na-opatovne-pouzitie', 'Zber podľa druhu', 14, 'Textil a šatstvo na opätovné použitie')
m('31145', 'odpady', 'textil-poskodeny', 'Zber podľa druhu', 15, 'Textil a šatstvo poškodené')
m('25739', 'odpady', 'baterie-a-akumulatory', 'Zber podľa druhu', 16, 'Batérie a akumulátory')
m('14160', 'odpady', 'letaky', 'Viac informácií', 20, 'Letáky a návody na triedenie')
m('14162', 'odpady', 'statistika', 'Viac informácií', 21, 'Štatistika zberu a vytriedenosť')
m('1715', 'odpady', 'zivotne-prostredie', 'Viac informácií', 22, 'Životné prostredie')

# Samospráva
m('1402', 'samosprava', 'starosta', 'Vedenie obce', 1, 'Starostka obce')
m('1403', 'samosprava', 'obecne-zastupitelstvo', 'Vedenie obce', 2, 'Obecné zastupiteľstvo')
m('1406', 'samosprava', 'komisie', 'Vedenie obce', 3, 'Komisie obecného zastupiteľstva')
m('1407', 'samosprava', 'obecna-rada', 'Vedenie obce', 4, 'Obecná rada')
m('1404', 'samosprava', 'hlavny-kontrolor', 'Vedenie obce', 5, 'Hlavný kontrolór')
m('146', 'samosprava', 'uznesenia', 'Rokovania zastupiteľstva', 10, 'Uznesenia obecného zastupiteľstva')
m('2361', 'samosprava', 'zapisnice', 'Rokovania zastupiteľstva', 11, 'Zápisnice zo zasadnutí')
m('9854', 'samosprava', 'videa-zo-zasadnuti', 'Rokovania zastupiteľstva', 12, 'Videozáznamy zo zasadnutí')
m('141', 'samosprava', 'vzn', 'Predpisy a rozpočet', 20, 'Všeobecne záväzné nariadenia (VZN)')
m('1408', 'samosprava', 'rozpocet', 'Predpisy a rozpočet', 21, 'Rozpočet a záverečný účet')
m('27191', 'samosprava', 'participativny-rozpocet', 'Predpisy a rozpočet', 22, 'Participatívny rozpočet')
m('145', 'samosprava', 'program-rozvoja', 'Rozvoj obce', 30, 'Program rozvoja obce')
m('142', 'samosprava', 'uzemny-plan', 'Rozvoj obce', 31, 'Územný plán obce')
m('18218', 'samosprava', 'komunitny-plan', 'Rozvoj obce', 32, 'Komunitný plán obce')
m('1368', None, None)

# Úradná tabuľa a dokumenty
m('135', 'uradna-tabula', 'uradna-tabula', 'Úradná tabuľa', 0, 'Elektronická úradná tabuľa')
m('11149', 'uradna-tabula', 'dosle-zasielky', 'Úradná tabuľa', 1, 'Oznámenia o došlých zásielkach')
m('25619', 'uradna-tabula', 'vyzvy', 'Úradná tabuľa', 2, 'Výzvy')
m('164/zverejnovanie', 'uradna-tabula', 'peticie', 'Úradná tabuľa', 3, 'Výsledky vybavenia petícií')
m('138', 'uradna-tabula', 'zmluvy', 'Zmluvy, faktúry, objednávky', 10, 'Zmluvy')
m('137', 'uradna-tabula', 'faktury', 'Zmluvy, faktúry, objednávky', 11, 'Faktúry')
m('139', 'uradna-tabula', 'objednavky', 'Zmluvy, faktúry, objednávky', 12, 'Objednávky')
m('136', 'uradna-tabula', 'verejne-obstaravanie', 'Zmluvy, faktúry, objednávky', 13, 'Verejné obstarávanie')
m('31351', 'uradna-tabula', 'volby-2026', 'Voľby a referendá', 20, 'Komunálne a krajské voľby 2026')
m('30879', 'uradna-tabula', 'referendum-2026', 'Voľby a referendá', 21, 'Referendum 2026')
m('143', 'uradna-tabula', 'volby', 'Voľby a referendá', 22, 'Voľby – archív')
m('134', 'uradna-tabula', 'dokumenty-na-stiahnutie', 'Ďalšie dokumenty', 30, 'Dokumenty na stiahnutie')
m('1409', 'uradna-tabula', 'dokumenty', 'Ďalšie dokumenty', 31, 'Ostatné dokumenty')
m('232', 'uradna-tabula', 'info-211', 'Ďalšie dokumenty', 32, 'Sprístupňovanie informácií (zákon 211/2000)')
m('144', 'uradna-tabula', 'civilna-ochrana', 'Ďalšie dokumenty', 33, 'Civilná ochrana')
m('203', 'uradna-tabula', 'prevencia-kriminality', 'Ďalšie dokumenty', 34, 'Prevencia kriminality')
for x in ('140', '11467', '164/vysledok-vybavenia-peticie'):
    m(x, None, None)

# Aktuality
m('31251', 'aktuality', 'projekty', 'Z obce', 10, 'Projekty obce')
m('166', 'aktuality', 'obecny-spravodaj', 'Z obce', 11, 'Obecný spravodaj')
m('1389', 'aktuality', 'kulturne-a-sportove-podujatia', 'Podujatia', 20, 'Kultúrne a športové podujatia')
m('1373', 'aktuality', 'nahlasene-podujatia', 'Podujatia', 21, 'Nahlásené podujatia (rušenie nočného kľudu)')
for x in ('1366', '1370'):
    m(x, None, None)

# Život v obci
m('1377', 'obec', 'zakladne-udaje', 'O obci', 1, 'Základné údaje')
m('1378', 'obec', 'historia', 'O obci', 2, 'História obce')
m('1452', 'obec', 'virtualna-prehliadka', 'O obci', 4, 'Virtuálna prehliadka obce')
m('1885', 'obec', 'mapa-obce', 'O obci', 5, 'Mapa obce s ulicami')
m('1382', 'obec', 'skolstvo-a-zdravotnictvo', 'Školy a zdravie', 10, 'Školstvo a zdravotníctvo')
m('1379', 'obec', 'sluzby', 'Služby a doprava', 20, 'Služby v obci')
m('24464', 'obec', 'kulturny-dom', 'Kultúra, šport, spolky', 30, 'Kultúrny dom a telocvičňa')
m('1380', 'obec', 'kultura', 'Kultúra, šport, spolky', 31, 'Kultúra a knižnica')
m('1383', 'obec', 'kluby', 'Kultúra, šport, spolky', 32, 'Kluby a spolky')
m('1381', 'obec', 'farnost', 'Kultúra, šport, spolky', 33, 'Farnosť')
m('1451', 'obec', 'cintorin', 'Služby a doprava', 21, 'Cintorín')
for x in ('1367', '1459', '2988'):
    m(x, None, None)

# Kontakt
m('2700', 'kontakt', 'dolezite-telefonne-cisla', 'Kontakty', 1, 'Dôležité telefónne čísla')

# Prepisy titulkov pre podstránky (ostatné sa dedia z pôvodného webu)
CHILD_TITLES = {
    '13691/matrika': None,
    '1400': 'Stolnotenisový klub TJ Slovan',
    '1398': 'DHZO Most pri Bratislave (hasiči)',
    '1462': 'Ples futbalistov 2012',
}
CHILD_SLUGS = {
    '28313': 'tlaciva-stary-zakon', '28314': 'portal-vystavby', '28315': 'tlaciva-novy-zakon',
    '13695': 'vypisy-z-matrik',
}

def key_of(url):
    parts = url.replace(OLD + '/', '').split('/')
    if parts[0] in ('zverejnovanie', 'novinky'):
        return parts[1], parts[1] + '/' + parts[2]
    return parts[0], parts[0] + '/' + parts[1]

def lookup(url):
    k1, k2 = key_of(url)
    if k2 in M: return M[k2]
    return M.get(k1)

# ---------------------------------------------------------------------------
# Čistenie markdownu
# ---------------------------------------------------------------------------
def fix_abs(u):
    u = html.unescape(u)
    if u.startswith('/'): return OLD + u
    return u

def size_fmt(s):
    return s.replace(' ', '\u00a0')

def files_table_to_html(m_):
    rows = [r for r in m_.group(0).strip().split('\n')[2:] if r.startswith('|')]
    items = []
    for r in rows:
        cells = [c.strip() for c in r.strip('|').split('|')]
        if len(cells) < 4: continue
        lm = re.search(r'\[([^\]]+)\]\(([^)\s]+)', cells[0])
        if not lm: continue
        name, url = re.sub(r'\\([_*\[\]#.-])', r'\1', lm.group(1)), fix_abs(lm.group(2))
        fmt = re.sub(r'Formát:\s*', '', cells[1]).strip().upper()
        size = re.sub(r'Veľkosť:\s*', '', cells[2]).strip()
        date = re.sub(r'Dátum:\s*', '', cells[3]).strip()
        items.append((name, url, fmt, size, date))
    if not items: return ''
    out = ['<ul class="file-list">']
    for name, url, fmt, size, date in items:
        out.append(f'<li><a href="{html.escape(url)}"><span class="file-ext">{html.escape(fmt or "SÚBOR")}</span>'
                   f'<span class="file-name">{html.escape(name)}</span></a>'
                   f'<span class="file-meta">{html.escape(size_fmt(size))} · {html.escape(date)}</span></li>')
    out.append('</ul>')
    return '\n'.join(out) + '\n'

def docs_table_to_html(m_):
    rows = [r for r in m_.group(0).strip().split('\n')[2:] if r.startswith('|')]
    out = ['<ul class="doc-list">']
    n = 0
    for r in rows:
        cells = [c.strip() for c in r.strip('|').split('|')]
        if len(cells) < 3: continue
        lm = re.match(r'\[([^\]]+)\]\(([^)\s]+)[^)]*\)(.*)', cells[0])
        if not lm: continue
        title, url, rest = re.sub(r'\\([_*\[\]#.-])', r'\1', lm.group(1)), fix_abs(lm.group(2)), lm.group(3)
        rest = re.sub(r'\s+', ' ', rest).strip(' •')
        meta = [p.strip() for p in rest.split('•') if p.strip()]
        files = cells[2]
        n += 1
        out.append('<li>'
                   f'<time>{html.escape(cells[1])}</time>'
                   f'<a href="{html.escape(url)}">{html.escape(title)}</a>'
                   + (f'<span class="doc-meta">{" · ".join(html.escape(x) for x in meta)}</span>' if meta else '')
                   + f'<span class="doc-files">{html.escape(re.sub(r"\s+", " ", files))}</span>'
                   '</li>')
    out.append('</ul>')
    return ('\n'.join(out) + '\n') if n else ''

PLACEHOLDER_ITEM = re.compile(r'^\* \[!\[\]\([^)]*\)\s*\n\s*\n\s*([^\]]+)\]\(([^)]+)\)\s*$', re.M)

def clean(body, link_map, self_url=None):
    b = body.replace('\u00ad', '')
    b = re.sub(r'\[!\[[^\]]*\]\([^)]*nahradny-obrazok[^)]*\)\]\([^)]*\)', '', b)
    b = re.sub(r'!\[[^\]]*\]\([^)]*nahradny-obrazok[^)]*\)', '', b)
    b = localize_all(b)
    # kartové zoznamy podstránok (obrázok + odkaz) - podstránky vypisuje šablóna sama
    b = re.sub(r'^\* \[!\[[^\]]*\]\([^)]*\)\s*\n\s*\n\s*[^\]]+\]\([^)]+\)\s*\n?', '', b, flags=re.M)
    b = re.sub(r'^(\s*)\* \[\s*\n\s*\n\s*([^\]\n]+)\]\(', r'\1* [\2](', b, flags=re.M)
    if self_url:
        b = re.sub(r'^\s*(?:web:\s*)?<?' + re.escape(self_url) + r'/?>?\s*$', '', b, flags=re.M)
    b = re.sub(r'Načítava sa\s*\n', '', b)
    b = re.sub(r'## Kategórie dokumentov\s*\n(\s*\* \[[^\n]*\n?)+', '', b)
    b = re.sub(r'^Vytvorené:\s*\n•\s*(\n|$)', '', b, flags=re.M)
    b = re.sub(r'\A(?:(?:Dátum:|Autor:|•|\d+|min\. čítania|[0-9.]+|Obec Most pri Bratislave)\s*\n)+', '', b)
    b = re.sub(r'## Komentáre\s*\n+Komentáre sú dostupné[^\n]*\n?', '', b)
    b = re.sub(r'\s*PDF bolo automaticky vygenerované OCR systémom Moderných obcí[^|]*?(?=\|)', ' ', b)
    b = re.sub(r' ?Odkaz sa otvorí na novej karte\.?', '', b)
    b = re.sub(r' "Odkaz smeruje na externú stránku\.?"', '', b)
    b = b.replace('Podstránka nie je momentálne naplnená obsahom', '')
    b = re.sub(r'^\s*```\s*\n\s*\n?\s*```\s*$', '', b, flags=re.M)
    # tabuľky súborov a zverejňovania
    b = re.sub(r'(?:^|\n)## Súbory na stiahnutie\s*\n', '\n## Súbory na stiahnutie\n', b)
    b = re.sub(r'\| Názov \| Formát \| Veľkosť \| Dátum \|\n\| --- \| --- \| --- \| --- \|\n(?:\|[^\n]*\|\n?)+', files_table_to_html, b)
    b = re.sub(r'\| Dokument \| Dátum \| Súbory \|\n\| --- \| --- \| --- \|\n(?:\|[^\n]*\|\n?)+', docs_table_to_html, b)
    # odkazy: interné -> nové URL, relatívne /data -> pôvodný server
    def relink(mm):
        url = mm.group(1)
        u = fix_abs(url)
        base = u.split('#')[0].split('?')[0].rstrip('/')
        if base in link_map: return '(' + link_map[base]
        return '(' + u
    b = re.sub(r'<(https?://(?:www\.)?mostpribratislave\.sk[^>\s]*)>', r'[Viac informácií](\1)', b)
    b = re.sub(r'\((/(?!media/)[^)\s]+|https?://(?:www\.)?mostpribratislave\.sk[^)\s]*)', relink, b)
    selfnew = link_map.get(self_url.rstrip('/')) if self_url else None
    def oldtext(mm):
        tgt = mm.group(1)
        return '' if tgt == selfnew else f'[Viac informácií]({tgt})'
    b = re.sub(r'\[https?://(?:www\.)?mostpribratislave\.sk[^\]]*\]\(([^)\s]+)[^)]*\)', oldtext, b)
    b = re.sub(r'href="(/data/[^"]+)"', lambda mm: 'href="' + OLD + mm.group(1) + '"', b)
    # zdvojené odseky (perex sa na starom webe opakuje)
    paras = b.split('\n\n'); out = []
    for p in paras:
        if out and p.strip() and p.strip() == out[-1].strip(): continue
        out.append(p)
    b = '\n\n'.join(out)
    # nadpisy: h1 v tele -> h2; nadpisy celé VEĽKÝMI nechávame (obsah obce)
    b = re.sub(r'^# ', '## ', b, flags=re.M)
    b = re.sub(r'\n{3,}', '\n\n', b).strip()
    return b

# ---------------------------------------------------------------------------
# Obrázky: stiahnu sa k webu (pôvodný server nepovoľuje vkladanie na cudzie weby)
# ---------------------------------------------------------------------------
import hashlib, urllib.request, urllib.parse
MEDIA = os.path.join(OUT, 'public/media')
_media_cache = {}
# všetky podpísané varianty obrázkov z uložených HTML (niektoré varianty server odmieta)
_variants = {}
for _f in os.listdir(os.path.join(DATA, 'raw')):
    for _u in re.findall(r'https://picturium\.moderneobce\.sk/[^"\s,]*token=[0-9a-f]+', open(os.path.join(DATA, 'raw', _f), encoding='utf-8', errors='replace').read()):
        _u = html.unescape(_u)
        _variants.setdefault(_u.split('?')[0], set()).add(_u)
def _rank(u):
    w = re.search(r'[?&]w=(\d+)', u)
    if 'dpr=' in u: return 3
    if w: return 0 if 600 <= int(w.group(1)) <= 1000 else 1
    if 'h=2000' in u: return 2
    return 4
def localize(u):
    u = html.unescape(u)
    path = u.split('?')[0]
    if path in _media_cache: return _media_cache[path]
    if 'token=' not in u: return None
    ext = os.path.splitext(path)[1].lower() or '.jpg'
    name = hashlib.sha1(path.encode()).hexdigest()[:16] + ext
    fn = os.path.join(MEDIA, name)
    if not os.path.exists(fn):
        os.makedirs(MEDIA, exist_ok=True)
        cands = sorted(_variants.get(path, set()), key=_rank) + [u]
        data = None
        for c in cands:
            try:
                req = urllib.request.Request(urllib.parse.quote(c, safe=':/?&=%'), headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'image/png,image/jpeg,image/*'})
                data = urllib.request.urlopen(req, timeout=30).read(); break
            except Exception as e:
                last = e
        if data is None:
            print('OBRÁZOK ZLYHAL', u[:100], last, file=sys.stderr); return None
        open(fn, 'wb').write(data)
    _media_cache[path] = '/media/' + name
    return _media_cache[path]

def localize_all(b):
    # najprv URL s tokenom (stiahnuť), potom ostatné (napr. odkaz na zväčšeninu) podľa cesty
    b = re.sub(r'https://picturium\.moderneobce\.sk/[^)\s"]*token=[0-9a-f]+', lambda m_: localize(m_.group(0)) or m_.group(0), b)
    def rest(m_):
        loc = _media_cache.get(m_.group(0).split('?')[0])
        return loc or m_.group(0)
    b = re.sub(r'https://picturium\.moderneobce\.sk/[^)\s"]*', rest, b)
    # zástupné obrázky bez obsahu preč
    b = re.sub(r'!\[[^\]]*\]\(/media/[^)]*\)', lambda m_: m_.group(0), b)
    return b

def yq(s):
    return json.dumps(s, ensure_ascii=False)

def title_case_fix(t):
    t = re.sub(r'\s+', ' ', t.replace('\u00ad', '')).strip()
    if t.isupper() and len(t) > 4:
        t = t[0] + t[1:].lower()
    return t

# ---------------------------------------------------------------------------
pages = json.load(open(os.path.join(DATA, 'pages.json'), encoding='utf-8'))
news = json.load(open(os.path.join(DATA, 'news.json'), encoding='utf-8'))

# 1) priradenie nových ciest
assigned = {}   # old url -> dict
by_url = {p['url']: p for p in pages}
for p in pages:
    if p.get('parent'): continue
    info = lookup(p['url'])
    if info is None:
        print('NEMAPOVANÉ', p['url'], file=sys.stderr); continue
    if info['slug'] is None: continue
    assigned[p['url']] = dict(info, title=info['title'] or title_case_fix(p['title']), parent=None)

for _ in range(3):
    for p in pages:
        par = p.get('parent')
        if not par or p['url'] in assigned: continue
        k1, k2 = key_of(p['url'])
        if k2 in M and M[k2]['slug'] is None: continue
        if k1 in M and M[k1]['slug'] is None: continue
        if k2 in M or k1 in M:
            # podstránka má vlastné mapovanie
            info = lookup(p['url'])
            assigned[p['url']] = dict(info, title=info['title'] or title_case_fix(p['title']), parent=None)
            continue
        pi = assigned.get(par)
        if not pi:
            # rodič bol zrušený (rozcestník) – prevezmi z mapy rodiča, ak existuje
            continue
        slug = CHILD_SLUGS.get(k1) or p['url'].rstrip('/').split('/')[-1]
        title = CHILD_TITLES.get(k1) or title_case_fix(p['title'])
        assigned[p['url']] = dict(section=pi['section'], slug=pi['slug'] + '/' + slug,
                                  group=pi['group'], order=pi['order'] + 0.5, title=title,
                                  parent=pi['slug'])

link_map = {u.rstrip('/'): f"/{a['section']}/{a['slug']}/" for u, a in assigned.items()}
link_map[OLD + '/novinky/1370/novinky-v-obci'] = '/aktuality/'
link_map[OLD + '/1366/obec-aktualne'] = '/aktuality/'
link_map[OLD + '/1445/kontakty'] = '/kontakt/'
link_map[OLD + '/13690/obecny-urad'] = '/kontakt/'
link_map[OLD + '/1405/obecny-urad'] = '/kontakt/'
link_map[OLD + '/1368/samosprava-obce'] = '/samosprava/'
link_map[OLD + '/1367/most-pri-bratislave'] = '/obec/'
link_map[OLD + '/13691/matrika'] = '/urad/matrika/'
link_map[OLD + '/podnety-a-otazky'] = '/nahlasit-problem/'
link_map[OLD + '/podnety-a-otazky/pridat'] = '/nahlasit-problem/'
link_map[OLD + '/kalendar'] = '/aktuality/podujatia/'
link_map[OLD] = '/'
link_map[OLD + '/27762/referat-verejneho-obstaravania'] = '/urad/projekty-a-obstaravanie/'
link_map[OLD + '/27763/referat-projektov'] = '/urad/projekty-a-obstaravanie/'
link_map[OLD + '/2988/jednota-dochodcov-slovenska'] = '/obec/kluby/'

# news link map
def news_slug(n):
    s = n['url'].rstrip('/').split('/')[-1]
    return s[:80].rstrip('-')
for n in news:
    link_map[n['url'].rstrip('/')] = f"/aktuality/spravy/{news_slug(n)}/"

# 2) zápis stránok
pdir = os.path.join(OUT, 'src/content/pages')
# vymažú sa len importované stránky (majú 'source:'), vlastné stránky obce zostávajú
for dp, _, fs in os.walk(pdir):
    for f in fs:
        fp = os.path.join(dp, f)
        if f.endswith('.md') and '\nsource: ' in open(fp, encoding='utf-8').read(2000):
            os.remove(fp)
redirects = {}
for u, a in assigned.items():
    p = by_url[u]
    body = clean(p['body'], link_map, u)
    fn = os.path.join(pdir, a['section'], a['slug'] + '.md')
    if any(x['parent'] == a['slug'] and x['section'] == a['section'] for x in assigned.values()):
        fn = os.path.join(pdir, a['section'], a['slug'], 'index.md')
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    upd = None
    if p.get('updated'):
        mm = re.match(r'(\d+)\.(\d+)\.(\d+)', p['updated'])
        if mm: upd = f"{mm.group(3)}-{int(mm.group(2)):02d}-{int(mm.group(1)):02d}"
    fm = ['---', f"title: {yq(a['title'])}", f"section: {a['section']}"]
    if a['group']: fm.append(f"group: {yq(a['group'])}")
    fm.append(f"order: {a['order']}")
    if a['parent']: fm.append(f"parent: {yq(a['parent'])}")
    if upd: fm.append(f"updated: {upd}")
    fm.append(f"source: {yq(u)}")
    fm.append('---')
    open(fn, 'w', encoding='utf-8').write('\n'.join(fm) + '\n\n' + body + '\n')
    redirects[u.replace(OLD, '')] = f"/{a['section']}/{a['slug']}/"

# 3) novinky
ndir = os.path.join(OUT, 'src/content/news')
os.makedirs(ndir, exist_ok=True)  # staršie novinky zostávajú, nové sa pridajú
for n in news:
    dm_ = re.search(r'Dátum:\s*\n\s*(\d{1,2}\.\d{1,2}\.\d{4})', n['body'])
    if dm_:
        d = dm_.group(1)
    else:  # bez dátumu: odhad z časovej pečiatky nahraného súboru, inak starý dátum
        ts = re.search(r'\?(1[4-7]\d{11})\b', n['body'])
        d = datetime.datetime.fromtimestamp(int(ts.group(1)) / 1000).strftime('%d.%m.%Y') if ts else '1.1.2020'
    dd, mo, yy = [int(x) for x in d.split('.')]
    iso = f"{yy}-{mo:02d}-{dd:02d}"
    body = clean(n['body'], link_map)
    img = None
    im = re.search(r'\[!\[[^\]]*\]\((/media/[^)\s]+)\)\]\([^)]*\)', body)
    if im:
        img = im.group(1)
        body = body.replace(im.group(0), '', 1).strip()
    if img and 'nahradny-obrazok' in img: img = None
    title = n['title']
    if title.isupper(): title = title[0] + title[1:].lower()
    # perex = prvý textový odsek
    perex = ''
    for para in body.split('\n\n'):
        t = re.sub(r'[*_#>\[\]]', '', para).strip()
        t = re.sub(r'\(https?://[^)]+\)', '', t)
        if len(t) > 40 and not t.startswith('|') and not t.startswith('<'):
            perex = re.sub(r'\s+', ' ', t)[:220]
            break
    cat = 'Oznam'
    tl = n['title'].lower()
    if any(w in tl for w in ('elektrin', 'slovnaft', 'rafinér', 'deratiz', 'dron', 'hnojen', 'prerušen', 'výpad', 'odstávk', 'upozornen', 'podvod', 'varovan', 'povodň', 'požiar', 'pitnej vody', 'plyn', 'dlžník', 'zrušen')): cat = 'Upozornenie'
    elif any(w in tl for w in ('uzávier', 'neprejazd', 'rekonštruk', 'cest', 'ulic', 'chodník', 'doprav', 'stojisk')): cat = 'Doprava a stavby'
    elif any(w in tl for w in ('odpad', 'vývoz', 'kontajner', 'zber')): cat = 'Odpady'
    elif any(w in tl for w in ('voľb', 'referend', 'volič')): cat = 'Voľby'
    elif any(w in tl for w in ('pozvánk', 'bál', 'maratón', 'aktivit', 'múze', 'knižnic', 'cvičen', 'walking', 'koncert', 'deň obce')): cat = 'Kultúra a šport'
    elif any(w in tl for w in ('zatvoren', 'zastupiteľ', 'referát', 'matrik', 'pracovná ponuka')): cat = 'Obecný úrad'
    fm = ['---', f"title: {yq(title)}", f"date: {iso}", f"category: {yq(cat)}"]
    if img: fm.append(f"image: {yq(img)}")
    if perex: fm.append(f"excerpt: {yq(perex)}")
    fm.append(f"source: {yq(n['url'])}")
    fm.append('---')
    open(os.path.join(ndir, f"{news_slug(n)}.md"), 'w', encoding='utf-8').write('\n'.join(fm) + '\n\n' + body + '\n')
    redirects[n['url'].replace(OLD, '')] = f"/aktuality/spravy/{news_slug(n)}/"

# 4) podujatia z kalendára
from bs4 import BeautifulSoup
s = BeautifulSoup(open(KAL, encoding='utf-8').read(), 'html.parser')
events = []
MON = {'január':1,'február':2,'marec':3,'apríl':4,'máj':5,'jún':6,'júl':7,'august':8,'september':9,'október':10,'november':11,'december':12}
seen = set()
for a in s.select('a[href*="/kalendar/"]'):
    href = a.get('href', '')
    if not re.search(r'/kalendar/\d+/', href) or href in seen: continue
    h3 = a.find('h3')
    if not h3: continue
    seen.add(href)
    txt = a.get_text('\n', strip=True)
    flat = re.sub(r'\s+', ' ', txt)
    dm = re.search(r'(\d{1,2})\. (\w+) (\d{4})(?: od)? ?(\d{1,2}:\d{2})?(?: - (\d{1,2}:\d{2}))?', flat)
    if not dm: continue
    day, mon, yr = int(dm.group(1)), MON.get(dm.group(2), 1), int(dm.group(3))
    lines = [l for l in txt.split('\n') if l.strip()]
    ti = lines.index(h3.get_text(strip=True)) if h3.get_text(strip=True) in lines else 0
    desc = ' '.join(lines[ti + 1:])[:260]
    place = None
    pm = re.search(r'Kde: ?(.*?)(?:Vstup|Palice|Organiz|\.|$)', desc)
    if pm: place = pm.group(1).strip()[:90]
    events.append(dict(title=h3.get_text(strip=True), date=f"{yr}-{mon:02d}-{day:02d}",
                       time=dm.group(4), end=dm.group(5), place=place, excerpt=desc, url=href))
events.sort(key=lambda e: e['date'])
os.makedirs(os.path.join(OUT, 'src/data'), exist_ok=True)
json.dump(events, open(os.path.join(OUT, 'src/data/events.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(dict(sorted(redirects.items())), open(os.path.join(OUT, 'src/data/redirects.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"stránok {len(assigned)}, noviniek {len(news)}, podujatí {len(events)}", file=sys.stderr)
