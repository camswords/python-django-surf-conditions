#!/bin/bash

BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

cd $BASEDIR
./linux_venv/bin/activate
MAGIC_SEAWEED_API_KEY=02bbdcc179bb7e02d7903fce5dec92e3 python manage.py runserver 0.0.0.0:8000
