#!/usr/bin/env python3
"""
Simple command line template renderer using
Jinja2.

This will parse the current environment into a dictionary
tree where each key is split along underscores or
camelcase and each element is added a sub-dictionary.

For example:

.. code-block:: shell

    DATABASE_ONE_URL=mysql:3306
    DATABASE_ONE_NAME=one
    databaseTwoUrl=mysql2:3306
    databaseTwoName=two
    AUTH_LDAP=true

Would result in:

.. code-block:: json

    {
        'database': {
            'one': {
                'url': 'mysql1:3306,
                'name': 'one'
            },
            'two': {
                'url': mysql2:3306,
                'name': 'two'
            }
        },
        'auth':
            'ldap': 'true'
    }

.. code-block:: shell

    $ j2tmpl template.jinja
    $ j2tmpl --help
"""
import os
import sys
import re

from jinja2 import Template
from argparse import ArgumentParser


def build_template_context(raw_context):
    """
    Build a template context from a given `raw_context`.

    A `raw_context` should be a flat list of variables
    each key may optionally be camelcase or have words
    separated with underscores. In either case, a dictionary
    is built by first splitting the variable keys buy
    underscores and casing, then constructing a tree along
    those splits.
    """
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
    """
    Render a template based on the arguments and
    the given `raw_context`, which, by default
    is the OS environment.
    """
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
