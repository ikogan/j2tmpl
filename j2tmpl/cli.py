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

from jinja2 import Environment, Undefined
from argparse import ArgumentParser


class PermissiveUndefined(Undefined):
    """
    A more permissive undefined that also also allows
    __getattr__. This allows `default`to work across
    the entire complex object.
    """
    def __getattr__(self, name):
        if name[:2] == '__':
            raise AttributeError(name)
        return self


def read_file_filter(filename):
    """
    Jinja filter that reads the contents of a file into the template
    given the filename.
    """
    with open(filename) as f:
        return f.read()


ENVIRONMENT = Environment(
                 trim_blocks=True,
                 lstrip_blocks=True,
                 undefined=PermissiveUndefined,
                 extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols']
)

ENVIRONMENT.filters['readfile'] = read_file_filter


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


def render_file(template, context, output=None, verbose=False):
    if verbose:
        print("Rendering", template, "to", output if output else "standard out")  # pragma: no cover

    output = open(output, 'w') \
        if output else sys.stdout

    ENVIRONMENT.from_string(template).stream(context).dump(output)

    if output:
        output.close()


def render(path, output, context, args):
    """
    Render a template based on the arguments and
    the given `raw_context`, which, by default
    is the OS environment.
    """
    # Make sure we have the full real path for later
    # comparisons.
    path = os.path.realpath(path)
    output_path = os.path.realpath(output) if output is not None else None

    if os.path.isdir(path):
        if output_path is not None:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            elif not os.path.isdir(output_path):
                raise OSError("%s already exists and is not a directory" % (output_path))

        # So we could use os.walk here but we need to control
        # what we do with directories based on the name so
        # it's actually easier not to.
        for entry in os.listdir(path):
            # Figure out the paths to the current file, the target
            # file, and the file extension of the current file.
            entry_path = os.path.realpath(os.path.join(path, entry))
            target_entry, extension = os.path.splitext(entry)
            target_entry_path = os.path.realpath(os.path.join(path, target_entry))

            # For directories, we either have to descend into them, or
            # we need to process them as fragments, depending on their
            # name.
            if os.path.isdir(entry_path):
                if extension == '.d' and \
                   os.path.splitext(target_entry)[1] in args.template_extensions:
                    # First, we'll read in the template if it exists, then
                    # each fragment in the fragment directory.
                    template = ""

                    if os.path.isfile(target_entry_path):
                        with open(target_entry_path) as templateFile:
                            template += templateFile.read()

                    for fragment in os.listdir(entry_path):
                        if os.path.splitext(fragment)[1] in args.template_extensions:
                            fragment_path = os.path.join(entry_path, fragment)
                            with open(fragment_path) as templateFile:
                                template += templateFile.read()

                    # Our target path still has the template extension on it since we're processing
                    # a fragment directory, need to split it off again.
                    render_file(template, context,
                                output=os.path.splitext(target_entry_path)[0],
                                verbose=args.verbose)
                elif args.recursive:
                    render(entry_path,
                           os.path.join(output_path, entry) if output_path else None,
                           context, args)
            elif extension in args.template_extensions and not os.path.isdir(entry_path + ".d"):
                with open(entry_path) as templateFile:
                    render_file(templateFile.read(), context, output=target_entry_path, verbose=args.verbose)
    else:
        with open(path) as templateFile:
            render_file(templateFile.read(), context, output=output_path, verbose=args.verbose)


def parse_arguments(args=sys.argv):  # pragma: no cover
    parser = ArgumentParser()
    parser.add_argument("template", help="Jinja template file or directory to render.")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Render templates in subdirectories recursively.",
                        default=False)
    parser.add_argument("-v", "--verbose", default=False)
    parser.add_argument("-o", "--output",
            help="Destination file to write. If omitted, will output to stdout.")  # noqa: E128,E501
    parser.add_argument("--template-extensions",
                        help="File extensions to interpret as template files (JINJA_TEMPLATE_EXTENSIONS).",  # noqa: E128,E501
                        dest="template_extensions", default=getattr(
                            os.environ, 'JINJA_TEMPLATE_EXTENSIONS', 'tmpl,jinja,jinja2,jnj,j2'))

    args = parser.parse_args(args=args)

    setattr(args, 'template_extensions', ["." + x for x in args.template_extensions.split(',')])

    return args


def main():  # pragma: no cover
    args = parse_arguments()

    render(args.template, args.output, build_template_context(os.environ), args)


if __name__ == "__main__":  # pragma: no cover
    main()
