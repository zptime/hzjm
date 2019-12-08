#!/usr/bin/env bash
source /opt/virt/hzjm/bin/activate
gunicorn --config gunicorn.conf hzjm.wsgi:application --daemon
