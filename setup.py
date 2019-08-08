#!/usr/bin/env python
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
    $ j2tmpl templatedir/
    $ j2tmpl --help

This allows using things like iterations and others
for more dynamic templates.

While there are several command line Jinja2 template
renderers, they all share a single property that this
attempts to solve.

Of those that support environment variables (for Docker, typically),
those environment variables are presented to the template verbatum.
That is, given this environment:

.. code-block:: shell

    DATABASE_MAIN_URI=mysql:3306
    DATABASE_MAIN_USERNAME=app
    DATABASE_CACHE_URI=redis:6379
    DATABASE_CACHE_USERNAME=app

A template would have to use them in the following way:

.. code-clock:: jinja

    databases: {
        main: {
            uri: {{ DATABASE_MAIN_URI }}
            username: {{ DATABASE_MAIN_USERNAME }}
        },
        cache: {
            uri: {{ DATABASE_CACHE_URI }}
            username {{ DATABASE_CACHE_USERNAME }}
        }

Suppose, though, that you don't necessarily know how many
databases your container will have? This construct makes
it diffcult in those instances where you have to define N
things differently depending on a container deployment, or for base
images. With `j2tmpl`, since the variable are parsed out into
a dictionary-like structure, you can do the following:

.. code-block:: jinja

    databases: {
        {% for name,definition in databases.items() %}
        {{ name }}: {
            uri: {{ definition.uri }},
            username: {{ definition.username }}
        },
        {% endfor %}

Handling Collissions
********************

Environment variables can sometimes cause interesting problems when
building a tree structure. A `ValueError` will be thrown if a variable
is defined twice. Howver, the following is a valid set of environment
variables:

.. code-block:: shell

    AUTH_LDAP=true
    AUTH_LDAP_USERNAME=app

In the template context, `{{ auth.ldap }}` has to be an object as `username`
is a key inside of it. In this case, the value of `AUTH_LDAP` will be moved down
into a special `_` key. The two variables would then be:

.. code-block:: jinja

    {{ auth.ldap._ }}=true
    {{ auth.ldap.username }}=app

For this to work, almsot all `_` in environment keys are removed. So, `AUTH__LDAP_`
is still translated to `{{ auth.ldap }}`. The only exceoptions is a variable with
*just* underscores. In this case, a '_' is added to the root of the context with
that value. Note that all of the following would create this single underscore
value:

- `_`
- `__`
- `____________________`

If multiple solely-underscore environment variables exist, a `ValueError` is thrown.

Installation
************

This can be installed in two ways:

1. `pip3 install j2tmpl`
2. Download the prebuild binaries.

Note that the prebuilt binaries include the entire Python interpreter so that they
can be used just as easily as `confd <https://github.com/kelseyhightower/confd>`.

Usage
*****

This can be used in two ways: processing a single file, or an entire directory.

When a directory path is passed as the template, `j2tmpl` will scan the
directory for any files with an extension matching
`template-extensions`, an argument that defaults to `tmpl,jinja,jinja2,j2,jnj`.

.. note::

    Note that it will still output to stdout unless `-o` is used.
    If it is, then make sure it's a directory as well. If the target
    directory doesn't exist, it will be created.

In addition to files matching that pattern, any *directory* that matches that
pattern and also ends with `.d` will be scanned for template fragments.
Template files as well as files in `.d` directories that end in those extensions
will all be concatenated together and rendered into one output file that matches
the name of the directory without the template extension and without `.d`.

For example, given the following directory structure:

.. code-block:: shell

    foo.conf.jinja.d/
        foo-1.jinja
        foo-2.jinja
    bar.conf.jinja.d/
        bar-1.jinja
        bar-2.jinja
    foo.conf.jinja
    baz.conf.jinja

The output directory will contain the following:

.. code-block:: shell

    bar.conf
    baz.conf
    foo.conf

Built-In Filters and extensions
*******************************

Jinja's `do <http://jinja.pocoo.org/docs/2.10/extensions/#expression-statement>`
and `loopcontrols <http://jinja.pocoo.org/docs/2.10/extensions/#loop-controls>`
extensions are enabled by default as are the
`trim_blocks <http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment>`
and `lstrip_blocks` <http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment>`.

Finally, the following additional filters are available:

:readfile(str): Read in the contents of the file represented by `str`. This is particularly useful for container secrets.
:boolean(str): Convert the argument into a boolean. A case insensitive comparison to "true", "yes", and "1" will return `True`. Everything else is false.
:b64encode(str): Base 64 encode the value.
:b64decode(str): Base 64 decode the value.

Why not confd?
**************

Speaking of confd, why not just use it? While confd is great, it can be a bit
too verbose. Having to define a series of config files with all keys enurmated
for every single key can be daunting. For certain projects, it probably makes
sense, but I would often like to just barf some environment variables into a
configuration file with only a tiny amount complexity.

confd is a 5.5mb or so binary and this is still less than 10mb There are likely
ways to make this smaller that I would love to explore.
"""

# flake8: noqa

from setuptools import find_packages, setup

install_requires = ["jinja2"]
tests_requires = ["pytest", "flake8", "pytest-cover", "pytest-flake8"]

setup(
    name="j2tmpl",
    version="0.0.9",
    author="Ilya Kogan",
    author_email="kogan@ohio.edu",
    url="https://github.com/ikogan/j2tmpl",
    description="Jinja2 templating based on environment variables.",
    long_description=__doc__,
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    license="BSD",
    install_requires=install_requires,
    extras_require={
        "tests": install_requires + tests_requires,
        "build": "pyinstaller"
    },
    setup_requires=["pytest-runner"],
    tests_require=install_requires + tests_requires,
    include_package_data=True,
    entry_points={"console_scripts": ["j2tmpl = j2tmpl:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
