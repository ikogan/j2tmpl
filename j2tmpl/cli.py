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
from __future__ import print_function

import os
import sys
import re
import base64

from argparse import ArgumentParser

from jinja2 import Environment, Undefined, FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError


# pylint: disable=too-few-public-methods
class PermissiveUndefined(Undefined):
    """
    A more permissive undefined that also also allows
    __getattr__. This allows `default` to work across
    the entire complex object.
    """
    def __getattr__(self, name):
        if name[:2] == '__':
            raise AttributeError(name)  # pragma: no cover (note sure how to test this)
        return self
# pylint: enable=too-few-public-methods


def read_file_filter(filename):
    """
    Jinja filter that reads the contents of a file into the template
    given the filename.
    """
    if isinstance(filename, Undefined):
        return filename

    with open(filename, encoding="utf-8") as j2filter:
        return j2filter.read()


def boolean_filter(value):
    """
    Jinja filter that returns a boolean value for a given
    string. The following values are truthy:

    true, yes, 1

    Note that this is case insensitive.
    """
    if isinstance(value, Undefined):
        return value

    return str(value).lower() in ['true', 'yes', 'on', '1']


def b64encode_filter(value):
    """
    Jinja filter that base64 encodes the given value.
    """
    if isinstance(value, Undefined):
        return value

    return base64.b64encode(value.encode('utf-8')).decode('utf-8')


def b64decode_filter(value):
    """
    Jinja filter that base64 decodes the given value.
    """
    if isinstance(value, Undefined):
        return value

    return base64.b64decode(value.encode('utf-8')).decode('utf-8')


ENVIRONMENT = Environment(
                 trim_blocks=True,
                 lstrip_blocks=True,
                 keep_trailing_newline=True,
                 undefined=PermissiveUndefined,
                 extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols']
)

ENVIRONMENT.filters['readfile'] = read_file_filter
ENVIRONMENT.filters['boolean'] = boolean_filter
ENVIRONMENT.filters['b64encode'] = b64encode_filter
ENVIRONMENT.filters['b64decode'] = b64decode_filter

# pylint: disable=too-many-nested-blocks
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

    for key, value in raw_context.items():
        original_key = key
        key = re.sub('_+', '_', re.sub('([a-z])([A-Z])', r'\1_\2', key).lower())
        keys = ['_'] if key == '_' else list(
            filter(lambda x: len(x) > 0, key.split('_')))

        current_level = context
        for level, level_key in enumerate(keys):
            level_key = level_key.lower()

            if level_key in current_level:
                if isinstance(current_level[level_key], dict):
                    if level == len(keys) - 1:
                        if '_' in current_level[level_key]:
                            raise ValueError(f'{original_key} is defined multiple times.')

                        current_level[level_key]['_'] = value
                else:
                    if level == len(keys) - 1:
                        raise ValueError(f'{original_key} is defined multiple times.')

                    current_value = current_level[level_key]
                    current_level[level_key] = {
                        '_': current_value
                    }
            elif level == len(keys) - 1:
                current_level[level_key] = value
            else:
                current_level[level_key] = {}

            current_level = current_level[level_key]

    return context
# pylint: enable=too-many-nested-blocks


def render_file(template, context, output=None, append=False, verbose=False):
    """
    Render a given template.
    """
    if verbose:  # pragma: no cover
        if output is None or template == output:
            print("Rendering", template)
        else:
            print("Rendering", template, "to", output)

    with open(template, encoding="utf-8") as template_file:
        output = open(output, 'a' if append else 'w', encoding="utf-8") \
            if output else sys.stdout # pylint: disable=consider-using-with

        try:
            ENVIRONMENT.from_string(template_file.read()).stream(context).dump(output)
        except TemplateSyntaxError as err:
            source = err.source.splitlines()
            columns = str(len(str(err.lineno + 1)))
            index = err.lineno - 1

            print(f"Error rendering {template}: {err.message}", file=sys.stderr)

            if index > 0:
                print(("%" + columns + "d:    %s") % (err.lineno - 1, source[index - 1]), file=sys.stderr)
            print(("%" + columns + "d: >> %s") % (err.lineno, source[index]), file=sys.stderr)
            if index < len(source)-1:
                print(("%" + columns + "d:    %s") % (err.lineno + 1, source[index + 1]), file=sys.stderr)

            raise err

    if output and output != sys.stdout:
        output.close()


# pylint: disable=too-many-nested-blocks disable=too-many-branches
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

    # Modify the environment to include a loader if a template
    # base directory was specified.
    if args.template_base_directory is not None:
        ENVIRONMENT.loader = FileSystemLoader(args.template_base_directory)

    if os.path.isdir(path):
        if output_path is not None:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            elif not os.path.isdir(output_path):
                raise OSError(f"{output_path} already exists and is not a directory")

        # So we could use os.walk here but we need to control
        # what we do with directories based on the name so
        # it's actually easier not to.
        for entry in os.listdir(path):
            # Figure out the paths to the current file, the target
            # file, and the file extension of the current file.
            entry_path = os.path.realpath(os.path.join(path, entry))
            entry_name, extension = os.path.splitext(os.path.basename(entry))

            if output_path is not None:
                target_entry_path = os.path.realpath(os.path.join(output_path, entry_name))
            else:
                target_entry_path = None

            # For directories, we either have to descend into them, or
            # we need to process them as fragments, depending on their
            # name.
            if os.path.isdir(entry_path):
                if extension == '.d' and \
                   os.path.splitext(entry_name)[1] in args.template_extensions:
                    if target_entry_path is None:
                        fragment_target_path = None
                    else:
                        fragment_target_path = os.path.splitext(target_entry_path)[0]

                    fragment_base_template = os.path.splitext(entry_path)[0]
                    if os.path.isfile(fragment_base_template):
                        render_file(fragment_base_template, context,
                                    output=fragment_target_path, verbose=args.verbose)
                    elif fragment_target_path is not None and os.path.isfile(fragment_target_path):
                        os.unlink(fragment_target_path)

                    for fragment in sorted(os.listdir(entry_path)):
                        if os.path.splitext(fragment)[1] in args.template_extensions:
                            fragment_path = os.path.join(entry_path, fragment)
                            render_file(fragment_path, context,
                                        output=fragment_target_path,
                                        verbose=args.verbose, append=True)
                elif args.recursive:
                    render(entry_path,
                           os.path.join(output_path, entry) if output_path else None,
                           context, args)
            elif extension in args.template_extensions and not os.path.isdir(entry_path + ".d"):
                render_file(entry_path, context, output=target_entry_path, verbose=args.verbose)
    else:
        render_file(path, context, output=output_path, verbose=args.verbose)
# pylint: enable=too-many-nested-blocks enable=too-many-branches


def parse_arguments(argv):  # pragma: no cover
    """
    Parse all command line arguments.
    """

    parser = ArgumentParser()
    parser.add_argument("template", help="Jinja template file or directory to render.")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Render templates in subdirectories recursively.",
                        default=False)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("-o", "--output",
            help="Destination file to write. If omitted, will output to stdout.")  # noqa: E128,E501
    parser.add_argument("-b", "--template-base-directory",
                        help="Add a base directory to lookup templates when using includes.",
                        dest="template_base_directory", default=None)
    parser.add_argument("--template-extensions",
                        help="File extensions to interpret as template files (JINJA_TEMPLATE_EXTENSIONS).",  # pylint: disable=line-too-long
                        dest="template_extensions", default=getattr(
                            os.environ, 'JINJA_TEMPLATE_EXTENSIONS', 'tmpl,jinja,jinja2,jnj,j2'))

    args = parser.parse_args(args=argv)

    setattr(args, 'template_extensions', ["." + x for x in args.template_extensions.split(',')])

    return args


def main(argv):  # pragma: no cover
    """
    Render a given file as a jinja template with environment
    variables as context. See --help or README.md for details.
    """
    args = parse_arguments(argv)

    try:
        render(args.template, args.output, build_template_context(os.environ), args)
    except TemplateSyntaxError:
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) > 0:
        main(sys.argv[1:])
    else:
        main(sys.argv)
