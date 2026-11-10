import sys,json,re
sys.argv=[sys.argv[0],'src/index.html','data']
exec(open('tools/import/crawl.py').read().split('# menu pages')[0])
pages=json.load(open('data/pages.json'))
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
json.dump(pages,open('data/pages.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('total',len(pages),file=sys.stderr)
