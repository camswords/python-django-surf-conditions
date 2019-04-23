#!/bin/bash

BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

cd $BASEDIR
source ./linux_venv/bin/activate
pylint surf --load-plugins=pylint_django | grep -v docstring | grep -v too-few | grep -v too-long
