#!/bin/bash
set -e

if [[ "${1}" = "build" ]]; then
    find . -name '*.pyc' -delete
    rm -Rf dist/*
    python3 setup.py test
    python3 setup.py bdist_egg bdist_wheel
    python3 -OO -m PyInstaller -F j2tmpl/cli.py -n j2tmpl
    staticx dist/j2tmpl dist/j2tmpl
else
    docker build -t $(whoami)/j2tmpl-build .
    docker run -ti --rm -v $(pwd)/dist:/app/dist:z $(whoami)/j2tmpl-build
fi
