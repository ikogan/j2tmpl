#!/usr/bin/env python
"""
j2tmpl
==========
.. code:: shell
  $ j2tmpl helloworld.tmpl helloworld.txt
"""

from setuptools import find_packages, setup

install_requires = ["jinja2"]
tests_requires = ["pytest", "flake8", "pytest-cover", "pytest-flake8"]

setup(
    name="j2tmpl",
    version="0.0.1",
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
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
)
