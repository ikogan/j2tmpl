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
    $ j2tmpl --help
"""
from setuptools import find_packages, setup

install_requires = ["jinja2"]
tests_requires = ["pytest", "flake8", "pytest-cover", "pytest-flake8"]

setup(
    name="j2tmpl",
    version="0.0.2",
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
