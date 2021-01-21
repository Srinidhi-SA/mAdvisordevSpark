#!/usr/bin/env bash


gunicorn -c gunicorn_config.py config.wsgi:application --enable-stdio-inheritance