# -*- coding: utf-8 -*-

import sys
import os
import re

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

here = os.path.dirname(__file__)

with open(os.path.join(here, 'goolabs', '__init__.py'), 'r') as f:
    version = re.compile(
        r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

readme = open(os.path.join(here, 'README.rst')).read()

requires = [
    "requests",
    "six",
    "click",
]

tests_require = [
    "pytest-cov",
    "pytest",
    "testfixtures",
    "responses",
]

if sys.version_info < (2, 7):
    tests_require.append("mock==1.0.1")
else:
    tests_require.append("mock")

entry_points = {
    "console_scripts": [
        "goolabs=goolabs.commands:main",
    ]
}

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries",
]

setup(
    name="goolabs",
    version=version,
    description="Goo labs API client for python. And provide some command line tools.",  # NOQA
    long_description=readme,
    url="https://github.com/tell-k/goolabs",
    author="tell-k",
    author_email="ffk2005 at gmail.com",
    classifiers=classifiers,
    keywords=['goolabs', 'web', 'api', 'client'],
    install_requires=requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    packages=find_packages(exclude=["tests"]),
    entry_points=entry_points,
    license='MIT',
)
