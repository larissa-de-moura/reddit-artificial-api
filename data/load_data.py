import os
import json
from datetime import datetime
from contextlib import closing
import requests
import time

HOST = 'http://127.0.0.1:5000'
endpoint = '/hot_posts'
files_dir = './files/'

chunk = []
supra_count = 1
total_recs = 0

for json_file in os.listdir(files_dir):
    count=1
    file_path = f'{files_dir}{json_file}'

    obj = json.loads(open(file_path).read())
    records = obj['data']['children']

    for rec in records:
        creat = rec['data'].get('created')
    
        selected_fields = {
            "title": rec['data'].get('title'),
            "author": rec['data'].get('author'),
            "ts_creation": creat,
            "num_ups": int(rec['data'].get('ups')),
            "num_comments": int(rec['data'].get('num_comments')),
        }

        res = requests.post(HOST + endpoint, selected_fields)
            #chunk.append(tuple(selected_fields.values()))
        try:
            res = res.json() # means that is a valid response
            count+=1
        except:
            print(res)

    print('Sleeping..')
    time.sleep(.1)

    supra_count += count

print(f'Posted successfully {count} records')




