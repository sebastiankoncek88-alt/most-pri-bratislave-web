import sys, re, json, os, time, html, urllib.request
from bs4 import BeautifulSoup
from markdownify import markdownify as md
BASE='https://www.mostpribratislave.sk'
out=sys.argv[2]; os.makedirs(out+'/raw',exist_ok=True)
idx=open(sys.argv[1],encoding='utf-8').read()
def get(url):
    fn=out+'/raw/'+re.sub(r'[^a-z0-9]+','_',url.lower())[-120:]+'.html'
    if os.path.exists(fn): return open(fn,encoding='utf-8').read()
    for i in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30)
            t=r.read().decode('utf-8','replace'); open(fn,'w',encoding='utf-8').write(t); time.sleep(0.3); return t
        except Exception as e: err=e; time.sleep(2)
    print('FAIL',url,err,file=sys.stderr); return None
def extract(t):
    s=BeautifulSoup(t,'html.parser'); c=s.find(id='content')
    if not c: return None,None,''
    for x in c(['script','style','svg','form','nav','button']): x.decompose()
    h=c.find('h1'); title=h.get_text(' ',strip=True) if h else ''
    m=md(str(c),heading_style='ATX')
    m=m.split('[Preskočiť na obsah](#main)')[0]
    upd=re.search(r'Upravené:\s*\n?\s*([0-9.]+ o [0-9:]+)',m)
    lines=[l for l in m.split('\n') if not re.match(r'^\s*(\[Preskočiť[^\]]*\]\(#\w+\)|Prečítať|Upravené:|[0-9.]+ o [0-9:]+)\s*$',l)]
    m='\n'.join(lines); m=re.sub(r'^# .*\n','',m,count=1)
    pass
    m=re.sub(r'\n{3,}','\n\n',m).strip()
    return title,(upd.group(1) if upd else None),m
# menu pages
links=re.findall(r'<a[^>]+href="(https://www\.mostpribratislave\.sk/(?:\d+|zverejnovanie/\d+|novinky/\d+)/[^"]+)"',idx)
links=list(dict.fromkeys(links))
pages=[]
for u in links:
    t=get(u)
    if not t: continue
    title,upd,body=extract(t)
    pages.append({'url':u,'title':title,'updated':upd,'body':body})
    print(len(body),u,file=sys.stderr)
json.dump(pages,open(out+'/pages.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
# news
news=[]
nl=list(dict.fromkeys(re.findall(r'href="(https://www\.mostpribratislave\.sk/novinka/\d+/[^"]+)"',idx)))
for u in nl:
    t=get(u)
    if not t: continue
    title,upd,body=extract(t)
    d=re.search(r'(\d{1,2}\.\d{1,2}\.20\d\d)',t[t.find('id="content"'):])
    news.append({'url':u,'title':title,'date':d.group(1) if d else None,'body':body})
json.dump(news,open(out+'/news.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('pages',len(pages),'news',len(news),file=sys.stderr)
