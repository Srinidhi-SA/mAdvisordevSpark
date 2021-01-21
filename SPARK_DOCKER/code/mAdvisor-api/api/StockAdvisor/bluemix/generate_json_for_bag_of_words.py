from __future__ import print_function
from builtins import zip
import csv
import api.StockAdvisor.utils as myutils
import json

input_file_name = "data/stockCategories.csv"
output_file_name = "data/stockCategories_nl_understanding.json"

csv_reader = csv.reader(open(input_file_name, 'rb'))

csv_header = []
json_array = []

for (i, row) in enumerate(csv_reader):
    if i == 0:
        csv_header = row
    else:
        print(i, row)

        cur_dictionary = dict(list(zip(csv_header, row)))
        date_key = "time"
        if date_key in list(cur_dictionary.keys()):
            cur_dictionary[date_key] = myutils.normalize_date_time(cur_dictionary.get(date_key)).strftime("%Y%m%d")

        nl_understanding = myutils.get_nl_understanding_from_bluemix(row[2])
        if nl_understanding:
            cur_dictionary["sentiment"] = nl_understanding.get("sentiment", [])
            cur_dictionary["keywords"] = nl_understanding.get("keywords", [])
        json_array.append(cur_dictionary)

out_file = open(output_file_name, "wb")
json.dump(json_array, out_file)
out_file.close()
