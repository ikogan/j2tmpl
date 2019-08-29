#!/bin/bash
set -e

if [[ -e /proc/1/cgroup ]] && (grep -q docker /proc/1/cgroup || grep -q user.slice /proc/1/cgroup); then
    find . -name '*.pyc' -delete
    rm -Rf dist/*
    python3 setup.py test
    python3 setup.py build
    python3 -OO -m PyInstaller -F j2tmpl/cli.py -n j2tmpl
    staticx dist/j2tmpl dist/j2tmpl
else
    docker build -t $(whoami)/j2tmpl-build .
    docker run -ti --rm -v $(pwd)/dist:/app/dist:z $(whoami)/j2tmpl-build
fi
