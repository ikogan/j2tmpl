#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = ["jinja2"]
tests_requires = ["pytest", "flake8", "pytest-cover", "pytest-flake8"]

setup(
    name="j2tmpl",
    version="0.0.12",
    author="Ilya Kogan",
    author_email="kogan@ohio.edu",
    url="https://github.com/ikogan/j2tmpl",
    description="Jinja2 templating based on environment variables.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    license="BSD",
    install_requires=install_requires,
    extras_require={
        "tests": install_requires + tests_requires,
        "build": ["pyinstaller", "staticx"]
    },
    setup_requires=["pytest-runner"],
    tests_require=install_requires + tests_requires,
    include_package_data=True,
    entry_points={"console_scripts": ["j2tmpl = j2tmpl:entrypoint"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
