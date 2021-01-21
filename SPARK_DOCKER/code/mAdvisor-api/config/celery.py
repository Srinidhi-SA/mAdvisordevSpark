from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from config.settings.config_file_name_to_run import CONFIG_FILE_NAME


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings." + CONFIG_FILE_NAME)

app = Celery('proj')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# #
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))


if 'leia' == CONFIG_FILE_NAME:
  from config.settings.leia import CELERY_ONCE_CONFIG
elif 'local' == CONFIG_FILE_NAME:
  from config.settings.luke import CELERY_ONCE_CONFIG
elif 'luke' == CONFIG_FILE_NAME:
  from config.settings.luke import CELERY_ONCE_CONFIG
elif 'development' == CONFIG_FILE_NAME:
  from config.settings.development import CELERY_ONCE_CONFIG

app.conf.ONCE = CELERY_ONCE_CONFIG