from __future__ import print_function
import csv
import simplejson as json
import sys

with open(sys.argv[2], 'wb') as f:
	i=0
	for line in open(sys.argv[1]).readlines():
		line=line.strip()
		#print line
		json_data=json.loads(line)
		#json_data.pop("review_url")
		#json_data.pop("blocks")
		remove=['final_url', 'blocks',  'block']
		for key in remove:
			json_data.pop(key)
		csv_headers=["stock","source","final_url1","date","title","desc","url"]
		if i==0:
			#w = csv.DictWriter(f, json_data.keys())
			w = csv.DictWriter(f, csv_headers)
			w.writeheader()
			i+=1
		try:
			w.writerow(json_data)
		except Exception as e:
			print(e)
