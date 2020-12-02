#!/usr/bin/env python
# encoding: utf-8

from codecs import open

from setuptools import setup, find_packages

with open("README.md", "r", 'UTF-8') as fh:
    long_description = fh.read()

setup(
    name="CheckmarxPythonSDK",
    version="0.1.5",
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
        "requests>=2.22.0",
        "requests-toolbelt>=0.9.1",
        "zeep>=3.4.0",
    ],
    extras_require={
        "dotenv": ["python-dotenv"],
        "dev": [
            "pytest",
            "coverage"
        ],
    },
)
