from __future__ import print_function
from django.core.management.base import BaseCommand
from api.models import CustomApps
from api.utils import AppSerializer
import json
import os


class Command(BaseCommand):

    help = 'Populate CustomApps'

    def _create_apps(self):
        path = os.getcwd() + '/api/management/commands/' + 'abc.json'
        with open(path) as fp:
            jsondata = json.load(fp)

            for data in jsondata:
                print(data['fields'])
                serializer = AppSerializer(data=data['fields'])
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

    def handle(self, *args, **options):
        self._create_apps()