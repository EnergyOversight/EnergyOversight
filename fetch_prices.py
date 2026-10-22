import json, urllib.request, urllib.parse, datetime, pathlib
from zoneinfo import ZoneInfo
now=datetime.datetime.now(ZoneInfo('Europe/Copenhagen'))
start=(now.date()-datetime.timedelta(days=1)).isoformat()
end=(now.date()+datetime.timedelta(days=3)).isoformat()
params=urllib.parse.urlencode({'start':start,'end':end,'filter':json.dumps({'PriceArea':['DK2']}),'sort':'HourDK asc','limit':300})
url='https://api.energidataservice.dk/dataset/Elspotprices?'+params
with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'EnergyOversight/1.0'}),timeout=30) as r:
    data=json.load(r)
if not data.get('records'):
    raise RuntimeError('No prices returned; keep previous prices.json')
pathlib.Path('prices.json').write_text(json.dumps({'records':data['records']},ensure_ascii=False),encoding='utf-8')
