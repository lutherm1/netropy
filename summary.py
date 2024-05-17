#!/bin/python3

import requests, json, pprint
import sys, time
import xlsxwriter

eng = 1
#change port 1 2 3 4 according to the eng
port1 = 1
port2 = 2



with open('server.txt') as f:
    server = f.read().strip()

engine_url_preFix = "http://{}/api/apposite-wan-emulator:engine/{}/".format(server, eng)

#login the api
url = "http://{}/login".format(server)

s = requests.Session()
req_body = {
    'username': 'admin',
    'password': 'admin'

}

res = s.post(url, data=req_body)
# print(res.content)


##### for paths and summry

headers = {

    'accept': 'application/json',
    'content-type': 'application/json'
}

url = engine_url_preFix +"path"
res = s.get(url, headers = headers)
# print(res.text)

allpaths =  json.loads(res.text)
# pprint.pprint(allpaths)


path_list = allpaths['path']
# pprint.pprint(path_list)
path_map = {}
for path in path_list:
    path_map[path['index']] = path['label']
req_body = {"paths": list(path_map.keys())}
print (path_map)


url = engine_url_preFix + "summary"

res = s.post(url, json.dumps(req_body), headers=headers )
flows = json.loads(res.text)
# pprint.pprint(flows)

direction_map = []
for flow in flows['flow']:
    # flow['name'] = path_map[flow['index']]
    stats = {
        'Name': path_map[flow['index']],
        'Direction': flow['direction'],
        'Frame': flow['frames'],
        'Bytes': flow['bytes'],
        'Drops': flow['drops'],

    }
    direction_map.append(stats)

# print (direction_map)





# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Stats.xlsx')
worksheet = workbook.add_worksheet()

cell_format = workbook.add_format({'align': 'center'})

# Add a bold format to use to highlight cells.

font = workbook.add_format({'underline': True, 'bold': True, 'bg_color': '#5b9bd5', 'align': 'center'})

# Write some data headers.
worksheet.write('A1', 'Name', font)
worksheet.write('B1', 'Flow', font)
worksheet.write('C1', 'Frames', font)
worksheet.write('D1', 'Bytes', font)
worksheet.write('E1', 'Drops', font)


row = 1
col = 0
for stats in direction_map:
    for key, value in stats.items():
        worksheet.write(row, col, value, cell_format )
        worksheet.set_column(row,col, 20)
        col += 1

        # worksheet.write(row, col +1)
    row += 1 
    col = 0

workbook.close()
