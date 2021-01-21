from __future__ import absolute_import
from .base import *
import datetime


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DEBUG = True

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# DATABASES = {
#     'default1': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     },
#     "default": {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'madvisor2',
#         'USER': 'root',
#         'PASSWORD': 'Marlabs@123',
#         'HOST': '172.31.53.141',
#         'PORT': '',
#         }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'madvisor',
        # 'USER': 'marlabs',
        # 'PASSWORD': 'Password@123',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PROJECT_APP = [
]

INSTALLED_APPS += PROJECT_APP


HADOOP_MASTER = 'localhost'


YARN = {
    "host": HADOOP_MASTER,
    "port": 8088,
    "timeout": 30
}

HDFS = {

    # Give host name without http
    'host': HADOOP_MASTER,
    'port': '50070', #webhdfs port
    'uri': '/webhdfs/v1',
    'user.name': 'hduser',
    'hdfs_port': '9000', #hdfs port
    'base_path' : '/dev/dataset/'
}


EMR = {
    "emr_pem_path": "",
    "home_path": "/home/hadoop"
}

KAFKA = {
    'host': 'localhost',
    'port': '9092',
    'topic': 'my-topic'
}


THIS_SERVER_DETAILS = {
    "host": "localhost",
    "port": "9012",
    "initail_domain": "/api"
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
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

SCORES_SCRIPTS_FOLDER = '/home/ubuntu/mAdvisorScores/'
IMAGE_URL = "/api/get_profile_image/"


DEPLOYMENT_ENV = "prod"

HADOOP_CONF_DIR= False
HADOOP_USER_NAME="hduser"

CELERY_BROKER_URL = 'redis://localhost:6379/'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/'
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

PEM_KEY = "/keyfiles/TIAA.pem"
ENABLE_KYLO = False
KYLO_UI_URL = "http://data-management.marlabsai.com"


USE_YARN_DEFAULT_QUEUE=True
# USE_YARN_DEFAULT_QUEUE=False

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend'
)


# SUBMIT_JOB_THROUGH_CELERY = False
SUBMIT_JOB_THROUGH_CELERY = True

CELERY_SCRIPTS_DIR="/home/hadoop/codebase/mAdvisor-api_2/scripts/"
END_RESULTS_SHOULD_BE_PROCESSED_IN_CELERY = True

CELERY_ONCE_CONFIG = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': 'redis://localhost:6379/',
    'default_timeout': 60 * 60
  }
}

KYLO_SERVER_DETAILS = {
    "host": "localhost",
    "port" : 8088,
    "user": "ankush",
    "key_path": "~/.ssh/ankush.pem",
    "group_propertie_quote": "madvisor,user",
    "kylo_file_path":"/opt/kylo/"
}