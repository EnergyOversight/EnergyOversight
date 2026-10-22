import json
import pathlib
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

now = datetime.now(ZoneInfo('Europe/Copenhagen'))
start = (now.date() - timedelta(days=1)).isoformat()
end = (now.date() + timedelta(days=2)).isoformat()
params = urllib.parse.urlencode({
    'start': start,
    'end': end,
    'filter': json.dumps({'PriceArea': ['DK2']}),
    'sort': 'TimeDK',
    'limit': 500,
})
url = 'https://api.energidataservice.dk/dataset/DayAheadPrices?' + params
request = urllib.request.Request(url, headers={'User-Agent': 'EnergyOversight/1.1'})
with urllib.request.urlopen(request, timeout=45) as response:
    data = json.load(response)
records = data.get('records', [])
if not records:
    raise RuntimeError('No DK2 day-ahead prices returned; preserving existing prices.json')
# Normalize names for compatibility with the dashboard's previous Elspotprices format.
for record in records:
    record['HourDK'] = record['TimeDK']
    record['HourUTC'] = record['TimeUTC']
    record['SpotPriceDKK'] = record['DayAheadPriceDKK']
    record['SpotPriceEUR'] = record['DayAheadPriceEUR']
pathlib.Path('prices.json').write_text(
    json.dumps({'records': records}, ensure_ascii=False), encoding='utf-8'
)
print(f'Saved {len(records)} DK2 price intervals')
