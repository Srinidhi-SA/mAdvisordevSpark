from __future__ import print_function
from builtins import str
from builtins import object
from django.conf import settings
REDIS_SALT = settings.REDIS_SALT
from django.core.cache import cache
import json
from api.models import SaveAnyData

REDIS_TIMEOUT = 60*60


class AccessFeedbackMessage(object):

    # def __init__(self, obj=None):
    #     if obj is None:
    #         self.key = None
    #     else:
    #         self.key = self.get_cache_name(obj)

    def get_cache_name(self, object):
        return type(object).__name__ + "_" + str(object.slug) + "_" + REDIS_SALT

    # ------------------------

    def get_using_obj(self, obj, default_value=list()):
        key = self.get_cache_name(obj)
        data = self.get_using_key(key)
        return data

    def get_using_key(self, key):
        try:
            data = self.get_using_key_cache(key)
            if data is None:
                data =  self.get_using_key_db(key)
                self.set_using_key_cache(key, data) # --------------------------------->
            return data
        except:
            data = self.get_using_key_db(key)
            self.set_using_key_cache(key, data)
            return data

    def get_using_key_cache(self, key):
        data = cache.get(key)
        return data

    def get_using_key_db(self, key):
        try:
            sd = SaveAnyData.objects.get(slug=key)
        except:
            sd = None

        if sd is not None:
            return sd.get_data()
        else:
            return None

    # ------------------------

    def get_or_set_using_key(self, key, default_value=None):
        data = self.get_using_key(key)

        if data is None:
            if default_value:
                data = default_value
            else:
                data = list()
            self.set_using_key(key, data)
        return data

    # ------------------------

    def set_using_obj(self, obj, value):
        key = self.get_cache_name(obj)
        return self.set_using_key(key, value)

    def set_using_key(self, key, value):
        try:
            self.set_using_key_cache(key, value)
            self.set_using_key_db(key, value)
        except:
            self.set_using_key_db(key, value)

        return value

    def set_using_key_cache(self, key, value):
        return cache.set(key, value)

    def set_using_key_db(self, key, value):

        try:
            sd = SaveAnyData.objects.get(slug=key)
        except:
            sd = SaveAnyData()
            sd.set_slug(slug=key)

        sd.set_data(data=value)
        sd.save()

    def append_using_key(self, key, value):
        data = self.get_or_set_using_key(key)
        if isinstance(value, list):
            data = data + value
        elif isinstance(value, dict):
            data.append(value)

        self.set_using_key(key=key, value=data)
        return self.get_using_key(key)

    def delete_this_key(self, key):
        try:
            sd = SaveAnyData.objects.get(slug=key)
            sd.delete()
            return cache.__delattr__(key)
        except:
            print("No instance.")
            return None

