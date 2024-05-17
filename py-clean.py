#!/bin/python

import json
import sys
import requests

with open('server.txt') as f:
    server = f.read().strip()

# print ('Server: '+server)

# login the api
url = "http://{}/login".format(server)

s = requests.Session()
req_body = {
    'username': 'admin',
    'password': 'admin'
}

res = s.post(url, data=req_body)

headers = { "content-type": "application/json" }
req_body = {}
url = "http://{}/api/apposite-wan-emulator:engine/1/reset".format(server)
res = s.post(url, json.dumps(req_body), headers=headers)

print "All clean sir"


