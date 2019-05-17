#!/bin/bash
set -e

python3 setup.py test
python3 -OO -m PyInstaller -F j2tmpl/cli.py -n j2tmpl
