# -*- coding: utf-8 -*-
import datetime
import http.client
import io
import sys
import urllib.error
import urllib.parse
import urllib.request

import backoff
import requests
import simplejson as json
from django.conf import settings
from google.cloud import vision
from google.protobuf.json_format import MessageToJson
from requests import HTTPError


class Api_Call:
    def __init__(self, doc_path):
        self.doc_path = doc_path
        self.text_from_Azure_API()

    @backoff.on_exception(backoff.expo, exception=HTTPError, max_tries=5)
    def text_from_Azure_API(self):

        print('#' * 50, '\n', datetime.datetime.now(), '\nAPI called\n', '#' * 50)
        api_gateway_url = 'https://74psiiujd1.execute-api.us-east-2.amazonaws.com/dev'

        data = open(self.doc_path, "rb").read()

        headers = {'Ocp-Apim-Subscription-Key': settings.SUBSCRIPTION_KEY,
                   'Content-Type': 'application/octet-stream',
                   'x-api-key': settings.API_KEY}

        analysis = {}
        poll = True

        response = requests.post(
            api_gateway_url,
            headers=headers,
            data=data)
        response.raise_for_status()

        while poll:
            response_final = requests.get(
                response.headers["Operation-Location"], headers=headers)
            analysis = response_final.json()

            if "status" in analysis and analysis['status'] == 'succeeded':
                poll = False

        self.doc_analysis = analysis

    def page_wise_response(self, page_number):
        return [i for i in self.doc_analysis["analyzeResult"]["readResults"]
                if (i["page"] == page_number)][0]


class Api_Call2:
    def __init__(self, doc_path, language_input):

        self.language_input = language_input
        self.doc_path = doc_path
        self.text_from_Azure_API()

    def text_from_Azure_API(self):

        lang = {"English": 'en', "Chinese-1": 'zh-Hans', "Chinese-2": 'zh-Hant', "Korean": 'ko', "Japanese": 'ja',
                "Portuguese": 'pt', "Italian": 'it'}

        try:
            lang_code = lang[self.language_input]
        except:
            print('Invalid language Input')
            sys.exit()

        body = open(self.doc_path, "rb").read()
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '8f6ad67b6c4344779e6148ddc48d96c0',
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'language': lang_code,
            'detectOrientation': 'true',
        })

        try:
            conn = http.client.HTTPSConnection('madvisor.cognitiveservices.azure.com')
            conn.request("POST", "/vision/v2.0/ocr?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            data = json.loads(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            data = None
            raise

        doc_analysis = self.clean_v2_analysis(data)
        self.doc_analysis = doc_analysis

    def page_wise_response(self, page_number):
        return self.doc_analysis

    def remake_bb(self, bb_str):

        x1, y1, w, h = [int(val) for val in bb_str.split(',')]
        return [x1, y1, x1 + w, y1, x1 + w, y1 + h, x1, y1 + h]

    def clean_v2_analysis(self, analysis_old):

        list_of_lines = [region['lines'] for region in analysis_old['regions']]
        lines_final = [line for lines in list_of_lines for line in lines]
        analysis_old['lines'] = lines_final

        del analysis_old['regions']

        for i, line in enumerate(analysis_old['lines']):

            text = ''
            bbox_line = line['boundingBox']

            line['boundingBox'] = self.remake_bb(bbox_line)

            for j, word in enumerate(line['words']):
                #                print(line)
                #                print('#'*5)
                bbox_word = line['words'][j]['boundingBox']
                line['words'][j]['boundingBox'] = self.remake_bb(bbox_word)
                text = text + ' ' + line['words'][j]['text']

            line['text'] = text
            analysis_old['lines'][i] = line

        return analysis_old


def fetch_google_response2(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    response = json.loads(MessageToJson(response))

    return response
