#!/bin/bash
set -e

python3 setup.py test
pyinstaller -F j2tmpl/cli.py -n j2tmpl
