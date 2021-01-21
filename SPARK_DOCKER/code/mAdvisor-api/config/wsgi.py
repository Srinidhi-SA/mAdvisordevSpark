"""
WSGI config for madvisor_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
from __future__ import absolute_import

import os

from django.core.wsgi import get_wsgi_application
from .settings.config_file_name_to_run import CONFIG_FILE_NAME

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings." + CONFIG_FILE_NAME)

application = get_wsgi_application()
