#!/usr/bin/env python
# encoding: utf-8
import os

from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'CheckmarxPythonSDK', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open("README.md", "r", 'utf-8') as fh:
    long_description = fh.read()

setup(
    name="CheckmarxPythonSDK",
    version=about['__version__'],
    author="Happy Yang",
    author_email="happy.yang@checkmarx.com",
    description="Checkmarx Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/checkmarx-ts/checkmarx-python-sdk",
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=[
        "urllib3>=1.26.12",
        "requests>=2.28.1",
        "requests-toolbelt>=0.9.1",
        "zeep>=4.1.0",
        "python-dateutil>=2.8.2",
        "keyring>=23.9.3",
        "Deprecated>=1.2.13",
    ],
    extras_require={
        "dotenv": ["python-dotenv"],
        "dev": [
            "pytest",
            "coverage"
        ],
    },
)
