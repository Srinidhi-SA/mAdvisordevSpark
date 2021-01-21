from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
import nltk
nltk.download('punkt')
nltk.download('wordnet')
standard_library.install_aliases()
from builtins import str
from builtins import range
from . import generic_crawler
from . import process
from . import common_utils
import simplejson as json
import urllib.request, urllib.parse, urllib.error
import sys
import os
from django.template.defaultfilters import slugify
import random
import string
import api.StockAdvisor.utils as myutils
from django.conf import settings

import pickle
import json
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import tensorflow.compat.v1 as tf

# tf.disable_v2_behavior()
import tensorflow_hub as hub
import numpy as np
import operator
from scipy.spatial.distance import cosine


def crawl_extract(url, regex_dict={}, remove_tags=[], slug=None):
    all_data = []
    crawl_obj = generic_crawler.GenericCrawler()

    content = crawl_obj.get_data(url, crawl_options={'fresh': True})
    json_list = process.process_data(url, content, regex_dict=regex_dict, remove_tags=remove_tags)

    for json_obj in json_list:
        if not json_obj.get("url"):
            continue
        if "date" in json_obj:
            json_obj["date"] = myutils.normalize_date_time(json_obj.get("date", "1 min ago")).strftime("%Y%m%d")
        all_data.append(json_obj)

    return all_data[4:]


def preprocess_keyword(text):
    text = text.lower()  # convert text to lower-case
    text = re.sub("(\\d)+", " ", text)  # remove digits
    text = text.replace("‘", '').replace("’", '').replace("'", '')  # remove apostrophe
    text = re.sub("(\\W)+", " ", text)  # remove special characters
    text = re.sub(r'^[^a-zA-Z]', r' ', text)  ##non words
    text = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    result = []
    for word in text:
        result.append(lemmatizer.lemmatize(word))
    text = " ".join(result)
    return text


def embed_useT():
    '''Function so that one session can be called multiple times.
    Useful while multiple calls need to be done for embedding.'''
    with tf.Graph().as_default():
        sentences = tf.placeholder(tf.string)
        embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-large/3")
        embeddings = embed(sentences)
        session = tf.train.MonitoredSession()
    return lambda x: session.run(embeddings, {sentences: x})


def sentence_encoder_for_concepts(universal_sentence_encoder):
    # create embedding matrix for each of the concepts
    embed_matrix_for_concepts = {}
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "/scripts/data/concepts.json"
    print(path)
    with open(path) as f:
        concepts = json.load(f)
    for key in concepts.keys():
        embed_matrix_for_concepts[key] = universal_sentence_encoder(concepts[key])
    return embed_matrix_for_concepts


def concept_mapping(test_text, embed_matrix_for_concepts, universal_sentence_encoder):
    test_embed = universal_sentence_encoder([test_text])
    similarity_score = {}
    for key in embed_matrix_for_concepts.keys():
        similarity_score[key] = max([1 - cosine(test_embed[0], i) for i in embed_matrix_for_concepts[key]])
    # use similrity score greater than 0.7 only
    similarity_score = {k: v for k, v in similarity_score.items() if v > 0.7}
    try:
        return max(similarity_score.items(), key=operator.itemgetter(1))[0]
    except:
        pass


def fetch_news_sentiments_from_newsapi(stock, domains):
    stock_news = process.fetch_stock_news_from_newsapi(stock, domains)
    stock_news_with_sentiments = []
    universal_sentence_encoder = embed_useT()
    embed_matrix_for_concepts = sentence_encoder_for_concepts(universal_sentence_encoder)
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Before IBM-watson hit, Time =", current_time)
    from api.StockAdvisor.crawling.cache import Cache
    bluemix_cache = Cache("bluemix")
    for i, news in enumerate(stock_news):
        # print("INDEX ---------- "+str(i)+"  articles --- "+str(len(stock_news)))
        short_desc = news["short_desc"]
        nl_understanding = None
        picled_content = bluemix_cache.get(news['final_url'])
        if picled_content:
            nl_understanding = pickle.loads(picled_content)
        else:
            nl_understanding = myutils.get_nl_understanding_from_bluemix(
                url=news['final_url'], content_of_the_url=short_desc)

        if nl_understanding:
            keywords = nl_understanding.result.get('keywords', [])
            for keyword in keywords:
                keyword['text'] = preprocess_keyword(keyword['text'])
                keyword['concept'] = concept_mapping(keyword['text'], embed_matrix_for_concepts,
                                                     universal_sentence_encoder)
            sentiment = nl_understanding.result.get('sentiment', [])

            if len(keywords) > 0 and len(sentiment) > 0:
                news['keywords'] = keywords

                if 'document' in sentiment:
                    sentiment['document']['score'] = float(sentiment['document']['score'])
                    news['sentiment'] = sentiment
                    stock_news_with_sentiments.append(news)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("After IBM-watson hit, Time =", current_time)
    return stock_news_with_sentiments


def fetch_news_article_from_nasdaq(stock):
    crawl_obj = generic_crawler.GenericCrawler()
    stock_news = []
    urls = get_nasdaq_news_articles(stock)

    print(urls)
    content_array = []
    for url in urls:
        content = crawl_obj.fetch_content(url, use_cache=False)
        if content:
            content_array.append(
                {
                    "url": url,
                    "content": content
                }
            )


    for content in content_array:
        if content:
            json_list = process.process_nasdaq_news_article(
                content['url'],
                content['content'],
                stock=stock
            )
            if len(json_list) < 1:
                break
            for json_obj in json_list:
                if not json_obj.get("url"):
                    continue
                if "date" in json_obj:
                    date_string = json_obj.get("date").split(" ")[0]
                    json_obj["date"] = myutils.normalize_date_time(date_string).strftime("%Y%m%d")
                    json_obj["time"] = myutils.normalize_date_time(date_string).strftime("%Y%m%d")
                stock_news.append(json_obj)

    print("Let us do sentiment on {0}".format(len(stock_news)) * 2)
    stock_news_with_sentiments = []
    for news in stock_news:
        short_desc = news["short_desc"]
        nl_understanding = myutils.get_nl_understanding_from_bluemix(
            url=news['final_url'], content_of_the_url=short_desc)
        if nl_understanding:
            news['keywords'] = nl_understanding.get('keywords', [])
            news['sentiment'] = nl_understanding.get('sentiment', [])
            stock_news_with_sentiments.append(news)

    return stock_news_with_sentiments


def write_to_news_data_in_folder(stockName, data):
    import os
    import csv
    path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "/scripts/data/" + self.slug + "/"
    file_path = path + stockName + "." + type
    with open(file_path, "wb") as file_to_write_on:
        if 'csv' == type:
            writer = csv.writer(file_to_write_on)
            writer.writerow(data)
        elif 'json' == type:
            json.dump(data, file_to_write_on)


def generate_urls_for_historic_data(list_of_company_name):
    return ["http://www.nasdaq.com/symbol/{0}/historical".format(name) for name in list_of_company_name]


def generate_url_for_historic_data(name):
    return "http://www.nasdaq.com/symbol/{0}/historical".format(name)


def generate_urls_for_crawl_news(stock_symbols):
    return ["https://finance.google.com/finance/company_news?q=NASDAQ:{}".format(stock_symbol.upper()) for stock_symbol
            in stock_symbols]


def get_nasdaq_news_articles(stock_symbol):
    urls = ["https://www.nasdaq.com/symbol/{0}/news-headlines".format(stock_symbol)]
    urls.extend(["https://www.nasdaq.com/symbol/{0}/news-headlines?page={1}".format(stock_symbol, str(i)) for i in
                 range(1, settings.NASDAQ_NEWS_HEADLINE_COUNT)])
    return urls


def convert_crawled_data_to_metadata_format(news_data, other_details=None, slug=None, symbols=None,
                                            created_at=None, start_date=None):
    if other_details is None:
        type = 'news_data'
    else:
        type = other_details['type']

    headers = find_headers(news_data=news_data, type=type, slug=slug)
    headersUI = headers.copy()
    columnData = get_column_data_for_metadata(headers, slug=slug)
    columnDataUI = columnData.copy()
    sampleData = get_sample_data(news_data=news_data, type=type, slug=slug)
    sampleDataUI = get_sample_data_ui(news_data=news_data, type=type, slug=slug)
    metaData = get_metaData(news_data=news_data, slug=slug)
    metaData_UI = metaData.copy()
    transformation_settings = get_transformation_settings(slug=slug)
    headers_UI = []
    for case in headersUI:
        temp = {}
        temp['name'] = case['name'].capitalize() if case['name'] != 'short_desc' else 'Short description'
        temp['slug'] = case['slug']
        headers_UI.append(temp)
    startDate = start_date.date().strftime('%b %d,%Y') if start_date else '-'
    endDate = created_at.date().strftime('%b %d,%Y')
    for i in columnDataUI:
        i['name'] = i['name'].capitalize() if i['name'] != 'short_desc' else 'Short description'
    companyNames = {"displayName": "Company Names", "name": "companyNames", "value": symbols, "display": True}
    timeline = {"displayName": "Timeline", "name": "timeline", "value": str(startDate) + ' to ' + str(endDate), "display": True}
    metaData_UI.append(timeline)
    metaData_UI.append(companyNames)

    metadata_json = {
        'scriptMetaData': {
            'columnData': columnData,
            'headers': headers,
            'metaData': metaData,
            'sampleData': sampleData
        },
        'uiMetaData': {
            'advanced_settings': {},
            'columnDataUI': columnDataUI,
            'headersUI': headers_UI,
            'metaDataUI': metaData_UI,
            'possibleAnalysis': '',
            'sampleDataUI': sampleDataUI,
            'transformation_settings': transformation_settings,
            'varibaleSelectionArray': []
        }
    }

    return metadata_json


def transform_into_uiandscripts_metadata():
    return {
        'scriptMetaData': {
            'columnData': '',
            'headers': '',
            'metaData': '',
            'sampleData': ''
        },
        'uiMetaData': {
            'advanced_settings': '',
            'columnDataUI': '',
            'headersUI': '',
            'metaDataUI': '',
            'possibleAnalysis': '',
            'sampleDataUI': '',
            'transformation_settings': '',
            'varibaleSelectionArray': ''
        }
    }


def get_transformation_settings(slug=None):
    existingColumn = {
        "existingColumns": []
    }
    return existingColumn


def find_headers(news_data, type='historical_data', slug=None):
    if len(news_data) < 1:
        return []
    headers_name = list(news_data[0].keys())
    required_fields = get_required_fields(type)
    headers_name = list(set(required_fields).intersection(set(headers_name)))
    headers = []
    for header in headers_name:
        temp = {}
        temp['name'] = header
        temp['slug'] = generate_slug(header)
        headers.append(temp)
    return headers


def get_column_data_for_metadata(headers, slug=None):
    import copy
    sample_column_data = {
        "ignoreSuggestionFlag": False,
        "name": None,
        "chartData": None,
        "dateSuggestionFlag": False,
        "columnStats": None,
        "columnType": None,
        "ignoreSuggestionMsg": None,
        "slug": None,
        "consider": True
    }

    columnData = []
    for header in headers:
        temp = copy.deepcopy(sample_column_data)
        temp['name'] = header['name']
        temp['slug'] = header['slug']
        columnData.append(temp)
    return columnData


def get_sample_data(news_data, type='historical_data', slug=None):
    required_fields = get_required_fields(type)
    headers_name = list(news_data[0].keys())
    headers_name = list(set(required_fields).intersection(set(headers_name)))
    sampleData = []
    for row in news_data:
        row_data = []
        for key in headers_name:
            row_data.append(row[key])
        sampleData.append(row_data)
    return sampleData


def get_sample_data_ui(news_data, type='historical_data', slug=None):
    required_fields = get_required_fields(type)
    headers_name = list(news_data[0].keys())
    headers_name = list(set(required_fields).intersection(set(headers_name)))
    sampleData = []
    for row in news_data:
        row_data = []
        for key in headers_name:
            if key == 'date':
                from datetime import datetime
                date = datetime.strptime(row[key], "%Y%m%d").date().strftime('%b %d,%Y')
                row[key] = date
            row_data.append(row[key])
        sampleData.append(row_data)
    return sampleData


def get_metaData(news_data, slug=None):
    metaData = [
        {"displayName": "News source", "name": "newsSource", "value": "NASDAQ", "display": True},
        {"displayName": "Stock Prices", "name": "stockPrices", "value": "NASDAQ", "display": True},
        {"displayName": "Number of Articles", "name": "numberOfArticles", "value": len(news_data), "display": True},
    ]
    return metaData


def get_required_fields(type='historical_data'):
    matching = {
        'historical_data': ['url', 'source', 'date', 'time'],
        'news_data': ['url', 'source', 'date', 'title', 'short_desc'],
    }

    return matching[type]


def generate_slug(name=None):
    return slugify(str(name) + "-" + ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))


def write_to_a_file(slug=None, data=None):
    with open('/tmp/temp_{0}'.format(slug), 'w') as temp:
        json.dump(data, temp)


def read_from_a_file(slug=None):
    temp = open('/tmp/temp_{0}'.format(slug), 'r')
    return json.loads(temp.read())