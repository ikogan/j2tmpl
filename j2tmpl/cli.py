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
        k = re.sub('_+', '_', re.sub('([a-z])([A-Z])', r'\1_\2', k).lower())
        keys = ['_'] if k == '_' else list(
            filter(lambda x: len(x) > 0, k.split('_')))

        currentLevel = context
        for level in range(0, len(keys)):
            levelKey = keys[level].lower()

            if levelKey in currentLevel.keys():
                if type(currentLevel[levelKey]) == dict:
                    if level == len(keys) - 1:
                        if '_' in currentLevel[levelKey]:
                            raise ValueError('%s is defined multiple times.' % (originalKey))  # noqa: E501

                        currentLevel[levelKey]['_'] = v
                else:
                    if level == len(keys) - 1:
                        raise ValueError('%s is defined multiple times.' % (originalKey))  # noqa: E501

                    currentValue = currentLevel[levelKey]
                    currentLevel[levelKey] = {
                        '_': currentValue
                    }
            elif level == len(keys) - 1:
                currentLevel[levelKey] = v
            else:
                currentLevel[levelKey] = {}

            currentLevel = currentLevel[levelKey]

    return context


def render(args, raw_context=os.environ):
    with open(args.template) as templateFile:
        context = build_template_context(raw_context)
        template = templateFile.read()
        output = open(args.output, 'w') \
            if args.output else sys.stdout

        Template(template).stream(context).dump(output)

        if args.output:
            output.close()


def main():  # pragma: no cover
    parser = ArgumentParser()
    parser.add_argument("template", help="Jinja template file to render.")
    parser.add_argument("-o", "--output",
            help="Destination file to write. If omitted, will output to stdout.")  # noqa: E128,E501
    args = parser.parse_args()

    render(args)


if __name__ == "__main__":  # pragma: no cover
    main()
