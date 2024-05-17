#!/bin/python

# Written in python 2.7

import json
import requests
import sys

with open('server.txt') as f:
    server = f.read().strip()

toggle_state = sys.argv[1].lower()
toggle_state = toggle_state == "on"

url = "http://{}/login".format(server)

s = requests.Session()
req_body = {
    'username': 'admin',
    'password': 'admin'
}

res = s.post(url, data=req_body)

headers = { "content-type": "application/json" }
url = "http://{}/api/apposite-wan-emulator:engine/1".format(server)
result = s.get(url)
result_json = result.json()
#print(json.dumps(result_json, indent=4, sort_keys=True))
cur_state = result_json["apposite-wan-emulator:engine"]["status"]["emulation"]
#print cur_state

if cur_state == toggle_state:
    if cur_state:
        print "Emulation is already on!"
    else:
        print "Emulation is already off"

req_data = { "emulation": toggle_state }

url = "http://{}/api/apposite-wan-emulator:engine/1/toggle".format(server)
res = s.post(url, json.dumps(req_data), headers=headers)
#print res
