import sys,json,re
# Použitie: python3 crawl_subpages.py <index.html> <data_dir>
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crawl.py')).read().split('# menu pages')[0])
pages=json.load(open(out+'/pages.json'))
have={p['url'] for p in pages}
for depth in range(2):
    new=[]
    for p in pages:
        for u in re.findall(r'\((https://www\.mostpribratislave\.sk/\d+/[a-z0-9-]+)',p['body']):
            if u not in have: have.add(u); new.append((u,p['url']))
    for u,parent in new:
        t=get(u)
        if not t: continue
        title,upd,body=extract(t)
        pages.append({'url':u,'title':title,'updated':upd,'body':body,'parent':parent})
        print(len(body),u,file=sys.stderr)
json.dump(pages,open(out+'/pages.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('total',len(pages),file=sys.stderr)
