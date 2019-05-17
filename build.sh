#!/bin/bash
set -e

./test.sh
pyinstaller -F j2tmpl/cli.py -n j2tmpl
