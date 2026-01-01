#!/usr/bin/env bash
   # exit on error
   set -o errexit

   pip install -r requirements.txt

   python manage.py collectstatic --no-input --settings=notehaven.settings.production
   python manage.py migrate --settings=notehaven.settings.production