#!/usr/bin/env python3
import os
import sys
import re

from jinja2 import Template
from argparse import ArgumentParser


def build_template_context(raw_context):
    context = {}

    for k, v in raw_context.items():
        originalKey = k
        k = re.sub('([a-z])([A-Z])', r'\1_\2', k).lower()
        keys = ['_'] if k == '_' else re.sub('_+', '_', k).split('_')

        currentLevel = context
        for level in range(0, len(keys)):
            levelKey = keys[level].lower()

            if len(levelKey) == 0:
                levelKey = '_'

            if levelKey in currentLevel.keys() and \
                    (type(currentLevel[levelKey]) != dict
                        or level == len(keys) - 1):
                raise ValueError('%s is defined multiple times or at a lower level at %s.' % (originalKey, levelKey))  # noqa: E501

            if level == len(keys) - 1:
                currentLevel[levelKey] = v
            elif levelKey not in currentLevel.keys():
                currentLevel[levelKey] = {}

            currentLevel = currentLevel[levelKey]

    return context


def render(args, raw_context=os.environ):
    with open(args.template) as templateFile:
        context = build_template_context(raw_context)
        template = templateFile.read()
        output = open(args.output, 'w', encoding=args.encoding) \
            if args.output else sys.stdout

        Template(template).stream(context).dump(output)

        if args.output:
            output.close()


def main():  # pragma: no cover
    parser = ArgumentParser()
    parser.add_argument("template", help="Jinja template file to render.")
    parser.add_argument("-o", "--output",
            help="Destination file to write. If omitted, will output to stdout.")  # noqa: E128,E501
    parser.add_argument("-e", "--encoding",
            help="File encoding to use for generating file (default: utf-8).", default="utf-8")  # noqa: E128,E501
    args = parser.parse_args()

    render(args)


if __name__ == "__main__":  # pragma: no cover
    main()
