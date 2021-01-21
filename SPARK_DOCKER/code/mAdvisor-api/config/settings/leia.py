from base import *
import datetime


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
import environ
env = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env()

DEBUG = env('DEBUG')

MODE=env('MODE')
ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default1': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'madvisor2',
        'USER': 'root',
        'PASSWORD': 'Marlabs@123',
        'HOST': '172.31.53.141',
        'PORT': '',
        }
}

MODE = env('MODE')

PROJECT_APP = [
]

INSTALLED_APPS += PROJECT_APP


HADOOP_MASTER = env('HADOOP_MASTER')

YARN = {
    "host": env('YARN_HOST'),
    "port": env('YARN_PORT'),
    "timeout": env('YARN_TIMEOUT')
}

import os
import json
hdfs_config_key=json.loads(os.environ['HADOOP_CONFIG_KEY'])
hdfs_config_value=json.loads(os.environ['HADOOP_CONFIG_VALUE'])
HDFS=dict(zip(hdfs_config_key,hdfs_config_value))

EMR = {
    "emr_pem_path": "",
    "home_path": "/home/hadoop"
}

KAFKA = {
    'host': env('KAFKA_HOST'),
    'port': env('KAFKA_PORT'),
    'topic': 'my-topic'
}


JOBSERVER = {
    'host': env('JOBSERVER_HOST'),
    'port': env('JOBSERVER_PORT'),
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
    "port": env('THIS_SERVER_PORT'),
    "initail_domain": "/api"
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://"+env('REDIS_IP')+":"+env('REDIS_PORT')+"/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "local"
    }
}
CACHE_TTL = 60 * 15
REDIS_SALT = "123"


APPEND_SLASH=False
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024*1024*1024

SCORES_SCRIPTS_FOLDER = env('SCORES_SCRIPTS_DIR')

IMAGE_URL = "/api/get_profile_image/"

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.office365.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "madvisor.automl@marlabs.com"
EMAIL_HOST_PASSWORD = "Secure@123"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'madvisor.automl@marlabs.com'

JOBSERVER_FROM_EMAIL = env('JOBSERVER_FROM_EMAIL')
JOBSERVER_SENDTO_EMAIL_LIST = tuple(env.list('JOBSERVER_SENDTO_EMAIL_LIST', default=[]))
FUNNY_EMAIL_LIST = tuple(env.list('FUNNY_EMAIL_LIST', default=[]))


JOBSERVER_EMAIL_TEMPLATE = "Please restart jobserver- IP-"

DEPLOYMENT_ENV = env('DEPLOYMENT_ENV')

HADOOP_CONF_DIR= env.bool('HADOOP_CONF_DIR')
HADOOP_USER_NAME=env('HADOOP_USER_NAME')

CELERY_BROKER_URL = "redis://"+env('REDIS_IP')+":"+env('REDIS_PORT')+"/1"
CELERY_RESULT_BACKEND = "redis://"+env('REDIS_IP')+":"+env('REDIS_PORT')+"/1"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
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
KYLO_UI_AUTH_URL= env('KYLO_UI_AUTH_URL')

USE_YARN_DEFAULT_QUEUE=True
# USE_YARN_DEFAULT_QUEUE=False

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend'
)


# SUBMIT_JOB_THROUGH_CELERY = False
SUBMIT_JOB_THROUGH_CELERY = True

#CELERY_SCRIPTS_DIR="/home/hadoop/codebase/mAdvisor-api_2/scripts/"
CELERY_SCRIPTS_DIR=env('CELERY_SCRIPTS_DIR')
END_RESULTS_SHOULD_BE_PROCESSED_IN_CELERY = True

CELERY_ONCE_CONFIG = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': "edis://"+env('REDIS_IP')+":"env('REDIS_PORT')+'/',
    'default_timeout': 60 * 60
  }
}

KYLO_SERVER_DETAILS = {
    "host": env('KYLO_SERVER_HOST'),
    "port" : env('KYLO_SERVER_PORT'),
    "user":  env('KYLO_SERVER_USER'),
    "key_path": env('KYLO_SERVER_KEY'),
    "group_propertie_quote": "madvisor,user",
    "kylo_file_path":"/opt/kylo/"
}

USE_HTTPS=env.bool('USE_HTTPS',default=False)
#MOdel Summary dowload key_path
MODEL_SUMMARY_DOWNLOAD_PATH='/home/ubuntu/automlModelSummary'

###################  OUTLOOK EMAIL CONFIG  ##########
OUTLOOK_DETAILS = {
    "client_id": '2e36be5f-0040-4f0d-bbef-12787ddc158b',
    "client_secret": '=Ogz4[AHfGM[eBX.f1wtdkakrzTPht85',
    #"authority":'https://login.microsoftonline.com',
    #"authorize_url" : 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    "tenant_id" : 'cc6b2eea-c864-4839-85f5-94736facc3be',
    "redirect_uri" : 'http://localhost:8000/get_request/'
}
OUTLOOK_SCOPES = [ 'openid',
           'User.Read',
           'Mail.Read',
           'offline_access']


OUTLOOK_AUTH_CODE =  '''OAQABAAIAAACQN9QBRU3jT6bcBQLZNUj73VtUUkVft_y8E3LBiK5eHMgCAKSe2DofhiCUf_WNN-a_l1cbKsyOBMw9JLKR0dl7olaPOw7331ZLCyfHnQpqZdpxHb8sTqubDX9P-0bISqCH7Ytp-kujV1M7ZEoB689Vvw1dR9hJRpRpMkKoXdOTivVbIp1e3vjLt5gRf_mnJ9-azGdRGmSjscq8-13gwS_WA35S9NTikCjxnIft8FrlkVwvBzRknSxzdtLWVwQfhQ3C0CjRa3PCijwSUwuTyy2cyq2aBdUv50xJN3pPKqh3_kYSmrNjGnp1dbg1xl-63uLW9j2Qv3R6pI2KcutxbBIbZAlk95ptRA2hICepkkLZiXca93B0MiCPRr2L2HL5S9ZK0IbL9wZi4CiOTL3_jXSqpK72VmXIO6scrOYFyz-8vdxTF-5eIO4pvtE0FeHbeX5s7c-EhrVAtrrG7N9Ccs5DyA1Zv8DkP3mjl72NLmgEJc9GxRMKrtNr2yLaGPg8sQ1_H-2Fe8L0unmTYMQ9ln_JGA3mMmBz9VqWB7XGKcZuOBzUi-G0WxehMD7o5oP9oGagsbZ9ZEJUHY3r-V2QPdpyq4M9CEY79O8UgWLcZ5kiTg7RJzsUS3jvZL38mWFzYvUG-gn3vi9Lv9w9xrkxXWEKO5jokN8hVYXUpKkCQIPWNUuIjF_iZbUq1cmaw7mNvzDvBiAi3ilnFRj_MIe7Q9D474ZcDP9pj8IBFkdCR-sA74SbN8nMAKmvkIwpABbpAgfQoqYtGeEDwietHjLCuipuRogqW2RApJ3HWw7UdK3KP8pr1iOapnRfPsX0XRRNqW31B6KCcljLPBrcNwsjnatIS42scxy9NQTNhXvFfMmvuv_fIQUmzcPkCBbyBDTZEPIgAA'''

OUTLOOK_REFRESH_TOKEN='''OAQABAAAAAACQN9QBRU3jT6bcBQLZNUj7Iwl5V8AGkybAwtdu9572_B0HHMxUiJIqK33bUTwj7rcjkKfpQecDWXovafEKiZNRdBxKMpeSUHFVGI95UetISlWDrZzRVjKPQV46SlqoFIrNn-H9BVno8ucMgGz16_v2hz86VgsvZ0E30BtaFU0GQBEiM0eQB-A7vSJ0Hah05v7Fil4SRXdN5CLMGCge3cec6Fptg446cKf544V6ErKJgHdxGQjnmvM_eCMi4uLBpFWHNwqdgYo-Ctn0uxb0GxcLo1JlmiiWk0WMP2YQxnzvC2A3jg34kwEdWSOiSKaXl-2rmszsIH0iPcvavaJ1JzmwhqSJjfr1pMr_np6TxV0r-A1fn7_e6FBrQOhXQTGBhc5FYSiPan-J-LO2B-LN5-wMXQSMJBIcpr1LvZvFY2L06WcdcDq_PuA6C_qsVhARc9sEA5BXtN_jF0-k-s3QqQs82OejW1NcjmrQWV-8GvKAwqcrANC6W0Dp1h6moZOvoezUdCVFqbRcUaDE05taKYKkhdmfHtRWMx0tAw2eQzDjSPoQXxhX_0QClfEdCaj-RVPh8SPTs8rBO8QHSv4ybnsTo1Qnu2dy_saAChth2ccuv93xEUuNIpB6ETrem0tuyclZCG_A7_-9N14214OkLWGnUzwqwADTxEdZZg2qgPNat0lg8n4bVAhz-wBl9H36lkRoxlxHh4AODvtAYZ6QmsImahRku_R6oEu90U-RSUNyuuq9DP4-dIjye1d6TNlPEQpDyTR5iTW1bgPUO-Io_BNcEw6PMgR2_uyU3GMIQ8KPJUWI-pFBWL8CwkIlZa3ixViY2kFzejJe1UvRlpDGzWRXqBJ7v7q39HvYHIPQpFZIXSAA'''
