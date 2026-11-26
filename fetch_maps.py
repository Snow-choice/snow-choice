import json, urllib.request, urllib.parse, pathlib, time
root=pathlib.Path(__file__).parent/'maps'; root.mkdir(exist_ok=True)
boxes={'happo':'36.675,137.76,36.735,137.85','goryu47':'36.60,137.76,36.70,137.87','washigatake':'35.88,136.99,35.96,137.10','tateyama':'36.545,137.385,36.605,137.460'}
failed=[]
for name,box in boxes.items():
 q=f'[out:json][timeout:60];(way["piste:type"="downhill"]({box});relation["piste:type"="downhill"]({box}););out geom;'
 for endpoint in ['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter']:
  try:
   req=urllib.request.Request(endpoint,data=urllib.parse.urlencode({'data':q}).encode(),headers={'User-Agent':'SNOW-CHOICE map snapshot updater'})
   with urllib.request.urlopen(req,timeout=90) as r: data=json.load(r)
   arr=[]
   for e in data['elements']:
    tags=e.get('tags',{}); names=[n for k,v in tags.items() if k.split(':')[0] in ('name','alt_name','official_name') or k.startswith('piste:name') for n in v.split(';')]
    for m in ([e] if e['type']=='way' else e.get('members',[])):
     if len(m.get('geometry',[]))>1: arr.append(dict(id=str(e['id'])+'-'+str(m.get('ref','')),name=tags.get('piste:name',tags.get('name','')),names=names,geom=m['geometry']))
   if not arr: raise ValueError('empty map')
   (root/(name+'.json')).write_text(json.dumps(arr,ensure_ascii=False,separators=(',',':'))); print(name,len(arr)); break
  except Exception as exc: print(name,endpoint,exc)
 else: failed.append(name)
 time.sleep(2)
if failed: print('Failed (existing files retained):',failed); raise SystemExit(1)
