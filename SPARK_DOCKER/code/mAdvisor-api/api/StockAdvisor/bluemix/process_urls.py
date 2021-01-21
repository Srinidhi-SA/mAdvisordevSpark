from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import object
import csv
import unittest
import urllib.request, urllib.error, urllib.parse
import json
import api.StockAdvisor.utils as myutils

from watson_developer_cloud import SpeechToTextV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
    as Features
from watson_developer_cloud.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1

from api.StockAdvisor.settings import natural_language_understanding_settings as nlu_settings
from time import sleep
from bs4 import BeautifulSoup

DEBUG = True


class ProcessUrls(object):
    url_file_name = ""
    content = ""
    nl_understanding = None  # will store the understanding
    open_files = {}
    csv_header = []
    json_arrays = {}

    def __init__(self, url_file_name):
        self.url_file_name = url_file_name

    pass

    def get_json_array_for_stock_symbol(self, stock_symbol):
        if stock_symbol not in list(self.json_arrays.keys()):
            self.json_arrays[stock_symbol] = []
        return self.json_arrays[stock_symbol]

    def write_data(self):
        for key in list(self.json_arrays.keys()):
            out_file = open("data/{}.json".format(key), "wb")
            json.dump(self.json_arrays[key], out_file)
            out_file.close()

    def process(self):

        f = open(self.url_file_name, 'rb')
        reader = csv.reader(f)
        for (i, row) in enumerate(reader):

            if DEBUG and i > 5:
                break
            if i == 0:
                self.csv_header = row

            else:
                print(i, row)
                nl_understanding = ""
                cur_dictionary = dict(list(zip(self.csv_header, row)))
                date_key = "time"
                if date_key in list(cur_dictionary.keys()):
                    cur_dictionary[date_key] = myutils.normalize_date_time(cur_dictionary.get(date_key)).strftime("%Y%m%d")

                self.target_url = row[2]
                # content = ""
                # try:
                #     html_content = urllib2.urlopen(self.target_url).read()
                #     soup = BeautifulSoup(html_content, "html.parser")
                #     content = soup.get_text()
                # except:
                #     pass
                nl_understanding =myutils.get_nl_understanding_from_bluemix(row[2])

                if nl_understanding:
                    cur_dictionary["sentiment"] = nl_understanding.get("sentiment", [])
                    cur_dictionary["keywords"] = nl_understanding.get("keywords", [])

                cur_json_array = self.get_json_array_for_stock_symbol(myutils.clean_key(row[0]))
                cur_json_array.append(cur_dictionary)

        return self.json_arrays
        # self.write_data()


class TestProcessUrls(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testMet1(self):
        pu = ProcessUrls("/home/marlabs/codebase/stock-advisor/data/stock_info.csv")
        pu.process()
        pass


if __name__ == '__main__':
    unittest.main()
