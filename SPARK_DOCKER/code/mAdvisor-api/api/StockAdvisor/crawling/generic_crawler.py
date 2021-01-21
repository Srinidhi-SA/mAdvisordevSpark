from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
import os
import random
from datetime import datetime

import requests
from deprecation import deprecated
from django.conf import settings

from . import common_utils
from .cache import Cache


class GenericCrawler(object):
    PREFIX = "GENERIC CRAWLER"
    PROXY_LIST = [
        {'http': u'http://46.225.241.6:8080'},
        {'http': u'http://66.119.180.104:80'},
        {'http': u'http://202.51.17.246:80'},
        {'http': u'http://202.179.190.210:8080'},
        {'http': u'http://103.94.64.90:8080'},
        {'http': u'http://202.138.254.29:8080'},
        {'http': u'http://197.159.16.2:8080'},
        {'http': u'http://host131-186-static.58-217-b.business.telecomitalia.it:8080'},
        {'http': u'http://182.253.142.16:8080'},
        {'http': u'http://152.231.29.210:8080'},
        {'http': u'http://103.234.137.158:8080'},
        {'http': u'http://131.161.124.36:3128'},
        {'http': u'http://195.138.91.117:8080'},
        {'http': u'http://185.36.172.190:8080'},
        {'http': u'http://client-90-123-107-176.kk-net.cz:8080'},
        {'http': u'http://46.209.25.1:8080'},
        {'http': u'http://165.16.113.210:8080'},
        {'http': u'http://168.232.157.142:8080'}
    ]
    USER_AGENT = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br"}

    REQUEST_CONNECTION_TIMEOUT = 10
    REQUEST_READ_TIMEOUT = 10
    REQUEST_RETRY_LIMIT = 10

    def __init__(self, crawl_options=None):
        if crawl_options is None:
            crawl_options = {}
        self.fdir = os.environ["HOME"] + "/html/" + crawl_options.get("source", "misc")
        self.crawl_options = crawl_options
        if hasattr(settings, "REQUEST_CONNECTION_TIMEOUT"):
            self.REQUEST_CONNECTION_TIMEOUT = settings.REQUEST_CONNECTION_TIMEOUT

        if hasattr(settings, "REQUEST_READ_TIMEOUT"):
            self.REQUEST_READ_TIMEOUT = settings.REQUEST_READ_TIMEOUT

        if hasattr(settings, "REQUEST_RETRY_LIMIT"):
            self.REQUEST_RETRY_LIMIT =  settings.REQUEST_RETRY_LIMIT

    def run(self):
        crawl_cache = Cache("stocksense")
        content = crawl_cache.get(self.url)
        if content:
            return content
        else:
            content = self.fetch_content(self.url)
            crawl_cache.put(self.url, content)
            return content

    def get_proxy(self):
        import random
        get_number = random.randint(0, len(self.PROXY_LIST) + 1)
        return self.PROXY_LIST[get_number]

    def download_using_proxy(self, url):
        temp_proxy = self.get_proxy()
        print(self.PREFIX, "Requesting New Page using proxy -->", temp_proxy, url)
        return requests.get(url, headers=self.USER_AGENT, proxies=temp_proxy, timeout=(
            self.REQUEST_CONNECTION_TIMEOUT,
            self.REQUEST_READ_TIMEOUT))

    def download_without_using_proxy(self, url):
        print(self.PREFIX, "Requesting New Page without proxy -->", url)
        return requests.get(url)

    def fetch_content(self, url, use_cache=False):
        """
        For a given url fetch content from the internet
        :param url:
        :return:
        """
        content = ""
        crawl_cache = Cache("stocksense")
        if use_cache:
            content = crawl_cache.get(url)

        if content:
            return content
        content = self.__download_content_with_retry(url)
        crawl_cache.put(url, content)
        return content

    def __download_content_with_retry(self, url):
        """
        Download content with
        :param url:
        :return:
        """
        for i in range(self.REQUEST_RETRY_LIMIT):
            print(self.PREFIX, "Trying for {0} time.".format(i), url)

            try:
                if 0 == i:
                    resp = self.download_without_using_proxy(url)
                else:
                    resp = self.download_using_proxy(url)
                content = resp.content

                if resp.status_code == 200:
                    break
            except Exception as err:
                print(self.PREFIX, err)
        return content

    @deprecated(details="use fetch content instead")
    def get_data(self, url="", crawl_options={}):
        if not crawl_options:
            crawl_options = self.crawl_options
        if not url:
            url = self.url

        if 'date_of_crawl' in crawl_options:
            if crawl_options['date_of_crawl'] == True:
                print("Asked today's Fresh Page?")
                fname = self.fdir + "/" + common_utils.get_sha(url + str(datetime.now().date()))
        elif "fresh" in crawl_options:
            if crawl_options['fresh'] == True:
                print("Asked Fresh Page?")
                fname = self.fdir + "/" + common_utils.get_sha(url + str(random.randint(99999999, 100000000000)))
        else:
            print("Asked for Archieved Page?")
            fname = self.fdir + "/" + common_utils.get_sha(url)

        content = ""
        if os.path.exists(fname):
            print("Cache hit")
            obj = open(fname)
            content = obj.read()
        else:
            for i in range(settings.REQUEST_RETRY_LIMIT):
                print("Trying for {0} time.".format(i))

                if 0 == i:
                    resp = self.download_without_using_proxy(url)
                else:
                    resp = self.download_using_proxy(url)
                try:
                    print("Got Response")
                    content = resp.content
                    html_dir = os.path.dirname(fname)
                    if not os.path.exists(html_dir):
                        os.makedirs(html_dir)
                    obj = open(fname, "w")
                    obj.write(content)
                    obj.close()
                    break
                except Exception as err:
                    print(err)
        return content
