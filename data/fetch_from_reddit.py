import requests
import json
import time
from datetime import datetime
url = 'https://api.reddit.com/r/artificial/hot?count=25'

count = 1
res = requests.get(url)
obj = res.json()

while obj.get('error'):
    time.sleep(.1)
    res = requests.get(url)
    obj = res.json()

with open(f'./db/files/{datetime.now().strftime("%Y-%m-%d")}_{count}.json', 'w') as f:
    json.dump(obj, f, indent=2)
    print(f'Done! File: {count}')
    count +=1

while obj['data'].get('after'):
    new_url = url + f"&after={obj['data'].get('after')}"
    res = requests.get(new_url)
    obj = res.json()
    
    while obj.get('error'):
        time.sleep(.1)
        res = requests.get(new_url)
        obj = res.json()

    with open(f'./db/files/{datetime.now().strftime("%Y-%m-%d")}_{count}.json', 'w') as f:
        json.dump(obj, f, indent=2)
        print(f'Done! File: {count}')
        count +=1
    

    
    
