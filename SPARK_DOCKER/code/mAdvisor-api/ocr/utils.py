from json2xml import json2xml
from json2xml.utils import readfromjson, readfromstring
import lxml.etree as ET
import pandas as pd


def json_2_xml(data):
    data = readfromstring(data)
    response = json2xml.Json2xml(data).to_xml()
    return ET.tostring(ET.fromstring(response))


def json_2_csv(data):
    df = pd.DataFrame(data)
    return df.to_csv()


def error_message(err_cls):
    messages = {
        'PermissionError': 'Permission denied for the operation',
        'FileNotFoundError': 'Unable to locate the file in the server.',
        'ServiceUnavailable': 'Unable to connect to the recognition service.',
        'HTTPError': 'Bad request from the recognition service.'
    }
    return messages[err_cls] if err_cls in messages else "Please check your image for issues."
