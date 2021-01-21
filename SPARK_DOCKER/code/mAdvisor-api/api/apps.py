from __future__ import absolute_import
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from .signalreceivers import trigger_insight_creation_job, trigger_metadata_creation_job
