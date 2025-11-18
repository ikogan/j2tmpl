#!/bin/bash
set -e

find . -name '*.pyc' -delete
rm -Rf dist
mkdir -p dist &>/dev/null
pytest
python3 -m build . --sdist --wheel
python3 -OO -m PyInstaller -F j2tmpl/cli.py -n j2tmpl
