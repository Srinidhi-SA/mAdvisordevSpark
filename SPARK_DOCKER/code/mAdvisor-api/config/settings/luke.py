from __future__ import absolute_import
from builtins import zip
from .base import *
import datetime

import environ

env = environ.Env(DEBUG=(bool, False), )  # set default values and casting
environ.Env.read_env()

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DEBUG = env('DEBUG')

MODE = env('MODE')
ALLOWED_HOSTS = ['madvisor-stg.marlabsai.com', '*']
DATABASES = {
    'default1': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    "default": env.db(),
    'TEST': {
        'NAME': 'test_madvisor',
    },
}

PROJECT_APP = [
]

INSTALLED_APPS += PROJECT_APP

HADOOP_MASTER = env('HADOOP_MASTER')

YARN = {
    "host": HADOOP_MASTER,
    "port": env.int('YARN_PORT'),  # 8088,
    "timeout": env.int('YARN_TIMEOUT')  # 30
}

import os
import json

hdfs_config_key = json.loads(os.environ['HADOOP_CONFIG_KEY'])
hdfs_config_value = json.loads(os.environ['HADOOP_CONFIG_VALUE'])
HDFS = dict(list(zip(hdfs_config_key, hdfs_config_value)))

EMR = {
    "emr_pem_path": "",
    "home_path": "/home/hadoop"
}

KAFKA = {
    'host': env('KAFKA_HOST'),  # 'localhost',
    'port': env('KAFKA_PORT'),  # '9092',
    'topic': 'my-topic'
}

JOBSERVER = {
    'host': env('JOBSERVER_HOST'),  # '172.31.50.84',
    'port': env('JOBSERVER_PORT'),  # '8090',
    'app-name': 'luke',
    'context': 'pysql-context',
    'master': 'bi.sparkjobs.JobScript',
    'metadata': 'bi.sparkjobs.JobScript',
    'model': 'bi.sparkjobs.JobScript',
    'score': 'bi.sparkjobs.JobScript',
    'filter': 'bi.sparkjobs.filter.JobScript',
    'robo': 'bi.sparkjobs.JobScript',
    'subSetting': 'bi.sparkjobs.JobScript',
    'stockAdvisor': 'bi.sparkjobs.JobScript'
}

THIS_SERVER_DETAILS = {
    "host": env('THIS_SERVER_HOST'),
    "port": env.int('THIS_SERVER_PORT'),
    "initail_domain": "/api"
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://" + env('REDIS_IP') + ":" + env('REDIS_PORT') + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "local"
    }
}
CACHE_TTL = 60 * 15
REDIS_SALT = "123"

APPEND_SLASH = False
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 1024

SCORES_SCRIPTS_FOLDER = env('SCORES_SCRIPTS_DIR')
IMAGE_URL = "/api/get_profile_image/"

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
# DEFAULT_FROM_EMAIL = 'madvisor.automl@marlabs.com'

JOBSERVER_FROM_EMAIL = env('JOBSERVER_FROM_EMAIL')
JOBSERVER_SENDTO_EMAIL_LIST = tuple(env.list('JOBSERVER_SENDTO_EMAIL_LIST', default=[]))

FUNNY_EMAIL_LIST = tuple(env.list('FUNNY_EMAIL_LIST', default=[]))

JOBSERVER_EMAIL_TEMPLATE = "Please restart jobserver- IP-"

DEPLOYMENT_ENV = env('DEPLOYMENT_ENV')

HADOOP_CONF_DIR = False
HADOOP_USER_NAME = "hduser"

CELERY_BROKER_URL = "redis://" + env('REDIS_IP') + ":" + env('REDIS_PORT') + "/"
# CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_BACKEND = "redis://" + env('REDIS_IP') + ":" + env('REDIS_PORT') + "/"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
# load related settings
CELERYD_MAX_TASKS_PER_CHILD = 4
CELERYD_CONCURRENCY = 2
# queue related settings
CELERY_DEFAULT_QUEUE = config_file_name_to_run.CONFIG_FILE_NAME
CELERY_QUEUES = {
    config_file_name_to_run.CONFIG_FILE_NAME: {
        "binding_key": "task.#",
        "exchange": config_file_name_to_run.CONFIG_FILE_NAME,
        "routing": config_file_name_to_run.CONFIG_FILE_NAME
    }
}

PEM_KEY = env('PEM_KEY')
ENABLE_KYLO = env.bool('ENABLE_KYLO')
KYLO_UI_URL = env('KYLO_UI_URL')
KYLO_UI_AUTH_URL = env('KYLO_UI_AUTH_URL')
END_RESULTS_SHOULD_BE_PROCESSED_IN_CELERY = True
KYLO_SERVER_DETAILS = {
    "host": env('KYLO_SERVER_HOST'),
    "port": env('KYLO_SERVER_PORT'),
    "user": env('KYLO_SERVER_USER'),
    "key_path": env('KYLO_SERVER_KEY'),
    "group_propertie_quote": "madvisor,user",
    "kylo_file_path": "/opt/kylo/"
}

CELERY_ONCE_CONFIG = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': "redis://" + env('REDIS_IP') + ":" + env('REDIS_PORT') + "/",
        'default_timeout': 60 * 60
    }
}

SUBMIT_JOB_THROUGH_CELERY = True
CELERY_SCRIPTS_DIR = env('CELERY_SCRIPTS_DIR')
USE_YARN_DEFAULT_QUEUE = True
USE_HTTPS = env.bool('USE_HTTPS', default=False)

SEND_WELCOME_MAIL = env('SEND_WELCOME_MAIL')
SEND_INFO_MAIL = env('SEND_INFO_MAIL')

OCR_SECONDARY_TASK_PERCENTAGE = 100
###################  OUTLOOK EMAIL CONFIG  ##########
OUTLOOK_DETAILS = {
    "client_id": '2e36be5f-0040-4f0d-bbef-12787ddc158b',
    "client_secret": '.5JwU-O9E_lY~uYUha5.3~dAUx3_0p_wu2',
    # "authority":'https://login.microsoftonline.com',
    # "authorize_url" : 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    "tenant_id": 'cc6b2eea-c864-4839-85f5-94736facc3be',
    "redirect_uri": 'http://localhost:8000/get_request/'
}
OUTLOOK_SCOPES = ['openid',
                  'User.Read',
                  'Mail.Read',
                  'offline_access']

OUTLOOK_TOKEN_URL = 'https://login.microsoftonline.com/' + OUTLOOK_DETAILS['tenant_id'] + '/oauth2/v2.0/token'

# OUTLOOK_AUTH_CODE =  '''OAQABAAIAAACQN9QBRU3jT6bcBQLZNUj73VtUUkVft_y8E3LBiK5eHMgCAKSe2DofhiCUf_WNN-a_l1cbKsyOBMw9JLKR0dl7olaPOw7331ZLCyfHnQpqZdpxHb8sTqubDX9P-0bISqCH7Ytp-kujV1M7ZEoB689Vvw1dR9hJRpRpMkKoXdOTivVbIp1e3vjLt5gRf_mnJ9-azGdRGmSjscq8-13gwS_WA35S9NTikCjxnIft8FrlkVwvBzRknSxzdtLWVwQfhQ3C0CjRa3PCijwSUwuTyy2cyq2aBdUv50xJN3pPKqh3_kYSmrNjGnp1dbg1xl-63uLW9j2Qv3R6pI2KcutxbBIbZAlk95ptRA2hICepkkLZiXca93B0MiCPRr2L2HL5S9ZK0IbL9wZi4CiOTL3_jXSqpK72VmXIO6scrOYFyz-8vdxTF-5eIO4pvtE0FeHbeX5s7c-EhrVAtrrG7N9Ccs5DyA1Zv8DkP3mjl72NLmgEJc9GxRMKrtNr2yLaGPg8sQ1_H-2Fe8L0unmTYMQ9ln_JGA3mMmBz9VqWB7XGKcZuOBzUi-G0WxehMD7o5oP9oGagsbZ9ZEJUHY3r-V2QPdpyq4M9CEY79O8UgWLcZ5kiTg7RJzsUS3jvZL38mWFzYvUG-gn3vi9Lv9w9xrkxXWEKO5jokN8hVYXUpKkCQIPWNUuIjF_iZbUq1cmaw7mNvzDvBiAi3ilnFRj_MIe7Q9D474ZcDP9pj8IBFkdCR-sA74SbN8nMAKmvkIwpABbpAgfQoqYtGeEDwietHjLCuipuRogqW2RApJ3HWw7UdK3KP8pr1iOapnRfPsX0XRRNqW31B6KCcljLPBrcNwsjnatIS42scxy9NQTNhXvFfMmvuv_fIQUmzcPkCBbyBDTZEPIgAA'''
OUTLOOK_AUTH_CODE = env('OUTLOOK_AUTH_CODE')

# OUTLOOK_REFRESH_TOKEN='''OAQABAAAAAACQN9QBRU3jT6bcBQLZNUj74AdP-GpiUTsBoBG1m4y3NTkUymq4ac3KU_YPhtVb1PesVm9n2Mos3NvulsjtmvInD49GdFkw3g4MMibA4UpXyO5bzCF4bCx6k7HQd-eoa4EbbgmgP_UpMXX2iK4UlWTCxiAOvJoa7Gzh6f6uy5BNexo_db2-_pHuSyxgWvqU_oV5SoO2eDnGHP1KYoNiaLWhapxRSUT5yULNGHO2Se--D6k_qUA8Q-AvSwr5Rrcza5Qh7VsYA3trPN8GiaWI_3OntYZO45R8b8EANO1QL9SITJIA9jdjiJPO8igczouk0_QHtd-epIaM2bTdbNSwOqSPARpKus7uNod1fScsqa8dvS85zVvpHs1WRHl_Rhxc9mo7hFKEo_ansWmpUwySc2YWppwzRa1bwolBoCcrxbmrdXy58YgBIo-kIejobUFD1TzQdUxY4XByasg18Ozy0W0YbgFvD2fR6_-xV6olzvCEOJFb_QQ381xWuRiDiwEH1BP4WWxD_bMjGlWgg_EPXNCRhYL9w9LPIs8wGMv4hZvFc7IJWMzkf5cHqfELIWQy-fmXxF-_PmoOsAs_5ilXgbVWPngBmB8hZZd70KUjEgkNDjjhS9syJ_FyciBIeTFigEzuQUmSR6_K3w8io0WrVzuH9rYkk5ttKgLcLbkpYP__7TddhUg_pjB3kGLEcM9m7tckB7a5_7CvXAjvn5scI_0k8SoeSv1IAzTmWk4ORv9bSlqksNS2GbBsDZXRHG6IqUqqvCOZIFrXjIYd9eOMvbhKcHQdSmJqlt60hcfx8JqT0CAA'''
OUTLOOK_REFRESH_TOKEN = env('OUTLOOK_REFRESH_TOKEN')

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'guardian.backends.ObjectPermissionBackend')

AUTOML_EMAIL_SERVICE_FLAG = env('AUTOML_EMAIL_SERVICE_FLAG')

STOCK_SENSE_CREDS = {
    "alphavantage": {
        "api_key": env("ALPHA_VANTAGE_API_KEY"),
        "function": env("ALPHA_VANTAGE_FUNCTION")
    },
    "newsapi": {
        "api_key": env("NEWSAPI_API_KEY")
    },
    "ibm-watson": {
        "api_key": env("IBM_WATSON_API_KEY"),
        "service_url": env("IBM_WATSON_SERVICE_URL")
    }
}

API_KEY = env('API_KEY')
SUBSCRIPTION_KEY = env('SUBSCRIPTION_KEY')
