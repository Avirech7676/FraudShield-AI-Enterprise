#!/usr/bin/env sh
set -e

gunicorn app.api.main:app -c deployment/gunicorn.conf.py
