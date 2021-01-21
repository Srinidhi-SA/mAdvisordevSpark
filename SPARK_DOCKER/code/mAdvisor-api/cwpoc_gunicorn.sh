#!/usr/bin/env bash
IP=0.0.0.0
PORT=9016
WORKERS=16
TIMEOUT=300000
PID_FILE=gunicorn.pid
ACCESS_LOG=gunicorn-access.log
ACCESS_LOG_FORMAT='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
ERROR_LOG=gunicorn-error.log


gunicorn --bind $IP:$PORT \
         -w $WORKERS \
         -t $TIMEOUT config.wsgi:application \
         -p $PID_FILE \
         --access-logfile $ACCESS_LOG \
         --error-logfile $ERROR_LOG \
         --daemon \
         --max-requests 5
