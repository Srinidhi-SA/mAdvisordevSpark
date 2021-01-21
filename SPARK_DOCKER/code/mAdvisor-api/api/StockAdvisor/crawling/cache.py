from __future__ import print_function
from builtins import object
import hashlib
import os

from django.conf import settings

__author__ = "Vivekananda Tadala"
__copyright__ = "Copyright 2018, The mAdvisor Project"
__credits__ = ["Vivekananda", ]
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Vivekananda Tadala"
__email__ = "vivekananda.tadala@marlabs.com"
__status__ = "Development"


class Cache(object):
    """
    Class to manage cache
    """

    def __init__(self, namespace="default", base_dir=""):
        self.namespace = namespace
        if base_dir:
            self.base_dir = base_dir
        else:
            self.base_dir = settings.CACHE_BASE_DIR

    def __get_hash(self, key):
        """
        private method to generate md5 or sha1 hash of the key
        :return:
        """
        return hashlib.sha1(key.encode('utf-8')).hexdigest()

    def __get_file_path(self, key):
        return os.path.join(self.base_dir, self.namespace, self.__get_hash(key))

    def put(self, key, content):
        """
        Save the content in the cache with given key
        :param key:
        :param content:
        :return:
        """
        try:
            file_path = self.__get_file_path(key)
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))

            file_obj = open(file_path, "wb")
            file_obj.write(content)
            file_obj.close()
        except IOError:
            print("CACHE: not able to cache the content")
        pass

    def get(self, key):
        """
        Get the content from the cache
        :param key:
        :return: content if key exists
        """
        try:
            file_path = self.__get_file_path(key)
            if os.path.exists(file_path):
                print("CACHE HIT: " + key)
                # return open(file_path).read()
                with open(file_path, 'rb') as f:
                    return f.read()
        except IOError:
            pass
        return None
