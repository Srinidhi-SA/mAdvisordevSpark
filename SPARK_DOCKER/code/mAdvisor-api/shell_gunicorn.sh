#!/usr/bin/env bash
IP=0.0.0.0
PORT=$1
WORKERS=5
TIMEOUT=300000
PID_FILE=gunicorn.pid


gunicorn --bind $IP:$PORT \
         -w $WORKERS \
         -t $TIMEOUT config.wsgi:application \
         -p $PID_FILE \
         --max-requests 5
