#!/bin/python
# Written in python 2.7

import json
import requests
import sys
import time


count = 1

with open('server.txt') as f:
    server = f.read().strip()

# login the api
url = "http://{}/login".format(server)

s = requests.Session()
req_body = {
    'username': 'admin',
    'password': 'admin'
}

res = s.post(url, data=req_body)
#print (res.content)

url = "http://{}/api/apposite-wan-emulator:engine/1/path".format(server)
res = s.get(url)
#print (res.text)

allpaths = json.loads(res.text)
# print (allpaths)


ids=[]
for path in allpaths['path']:
        ids.append(path['id'])
        print path['id'], path['label']

while True:
    if not count in ids:
        break
    count += 1

req_body = {
     "engine": 1,
     "id": count,
     "label": "Apposite Lab 70ms 100mbps",
     "source": {
         "outbound": {
           "mode": "single",
           "bandwidth": {
             "rate": 100,
             "metric": "Mbps"
         }
       }
     },
       "destination": {
         "outbound": {
           "mode": "single",
           "bandwidth": {
             "rate": 100,
             "metric": "Mbps"
           }
         }
       },
       "wan": {
         "source-to-destination": {
           "delay": {
             "method": "constant",
             "reordering": False,
             "constant": {
               "latency": 35
             }
           }
         },
         "destination-to-source": {
           "delay": {
             "method": "constant",
             "reordering": False,
             "constant": {
               "latency": 35
             }
           }
         }
       }
   }

# print (json.dumps(req_body, indent=4))
url = "http://{}/api/apposite-wan-emulator:engine/1/path".format(server)
headers = { "content-type": "application/json" }
res = s.post(url, json.dumps(req_body), headers=headers)
print ("Building Path: - "+str(count))

time.sleep(1)

req_body = {
      "label": "Linux 1",
      "engine": 1,
      "port": 1,
      "ipaddrs": [
        "20.0.0.112"
      ],
      "action": count,
      "protocol": "tcp"
    }

url = "http://{}/api/apposite-wan-emulator:engine/1/endpoint".format(server)
res = s.post(url, json.dumps(req_body), headers=headers)
#print (res.text)
res = json.loads(res.text)
print ("Building Node-1 ID : - "+res['endpoint'][0]['id'])

time.sleep(1)

req_body = {
      "label": "Linux 2",
      "engine": 1,
      "port": 2,
      "ipaddrs": [
        "20.0.0.111"
      ],
      "action": count,
      "protocol": "tcp"
}
url = "http://{}/api/apposite-wan-emulator:engine/1/endpoint".format(server)
res = s.post(url, json.dumps(req_body), headers=headers)

res = json.loads(res.text)
print ("Building Node-2 ID : - "+res['endpoint'][0]['id'])

req_body = { "emulation": True }
url = "http://{}/api/apposite-wan-emulator:engine/1/toggle".format(server)
res = s.post(url, json.dumps(req_body), headers=headers)

print("Emulation ON")
