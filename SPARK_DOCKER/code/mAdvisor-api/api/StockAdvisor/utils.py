from __future__ import print_function
from __future__ import absolute_import
from builtins import range
import hashlib
import string

from django.conf import settings

# import watson_developer_cloud.natural_language_understanding.features.v1 \
#     as Features
# from watson_developer_cloud.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1

from ibm_watson import NaturalLanguageUnderstandingV1

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, ConceptsOptions, EmotionOptions, \
    EntitiesOptions, KeywordsOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions

from api.StockAdvisor.crawling.cache import Cache
from .settings import NUMBEROFTRIES, CACHESALT, TEMPDIR
from .settings import natural_language_understanding_settings as nlu_settings


def clean_key(key):
    return "".join([x if x in string.ascii_lowercase else "" for x in key.lower()])


def normalize_date_time(date_string):
    """
    Understand "6 hours ago, and other formats and return curret date in YYYYMMDD"
    :param date_string:
    :return:
    """
    from datetime import datetime
    date = datetime.today()

    if "ago" in date_string:
        date = datetime.today()
    else:
        try:
            # mm/dd/yyyy
            date = datetime.strptime(date_string, "%m/%d/%Y").date()
        except:
            pass

        try:
            # 'Sep 29, 2017'
            date = datetime.strptime(date_string, "%b %d, %Y").date()
        except:
            pass

    return date


def get_nl_understanding_from_bluemix(url="", content_of_the_url="", use_cache=True):
    """
    get Natural Language understanding using Bluemix APIs
    :param url:
    :param content_of_the_url:
    :param use_cache:
    :return:
    """

    # apikey = 'sK2KMSxYIyeQiYJpb9ugbMI5cjZRW6e2MSYLrWTtoINy' #Sivavamsi creds
    # service_url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/9945cca0-ece4-45c8-903e-efbf3fcc61ff'

    # apikey = "UXyQqWwT26Ruu_PgpAvehj_q0Lg3xFOCKMQ-IX2WTu1j" # Rahuls creds
    # service_url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/259e5cd0-ac42-45e9-86e8-b9c772d3131f"

    # apikey = '7bhl_NWHuTmL-wrIICRpKr-wvu0alPwNyhO8UAfvYLWC' #Dechamma's creds
    # service_url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/6cf4a4bd-8b59-407c-ae31-14fbfc889c65'

    apikey = settings.STOCK_SENSE_CREDS['ibm-watson']['api_key']
    service_url = settings.STOCK_SENSE_CREDS['ibm-watson']['service_url']

    authenticator = IAMAuthenticator(apikey)

    def __get_nl_analyzer():
        natural_language_understanding = NaturalLanguageUnderstandingV1(version='2019-07-12',
                                                                        authenticator=authenticator)
        natural_language_understanding.set_disable_ssl_verification(True)
        natural_language_understanding.set_service_url(service_url)
        return natural_language_understanding

    def __get_default_features():
        return Features(entities=EntitiesOptions(emotion=True, sentiment=True, limit=100),
                        keywords=KeywordsOptions(emotion=True, sentiment=True, limit=100),
                        categories=CategoriesOptions(),
                        concepts=ConceptsOptions(),
                        emotion=EmotionOptions(),
                        relations=RelationsOptions(),
                        semantic_roles=SemanticRolesOptions(),
                        sentiment=SentimentOptions()
                        )

    nl_understanding = None

    if not nl_understanding:
        natural_language_analyzer = __get_nl_analyzer()
        for i in range(NUMBEROFTRIES):
            if i % 2 == 0:
                features = __get_default_features()
            else:
                features = {"sentiment": {}, "keywords": {}}
            try:
                if content_of_the_url:
                    nl_understanding = natural_language_analyzer.analyze(
                        text=content_of_the_url, features=features)
                else:
                    nl_understanding = natural_language_analyzer.analyze(
                        url=url, features=features)
            except Exception as err:
                print("FAILED " * 10, err)

            if nl_understanding:
                break

    if nl_understanding:
        bluemix_cache = Cache("bluemix")
        bluemix_cache.put(url, pickle.dumps(nl_understanding))
    return nl_understanding


def get_cache_file_name(input_key):
    m = hashlib.md5(CACHESALT + input_key)
    return TEMPDIR + m.hexdigest()


import pickle
import os


def cache_get(key):
    cache_file_name = get_cache_file_name(key)
    if os.path.isfile(cache_file_name):
        return pickle.load(open(cache_file_name, "rb"))
    else:
        return None


def cache_put(key, obj):
    pickle.dump(obj, open(get_cache_file_name(key), "wb"))
