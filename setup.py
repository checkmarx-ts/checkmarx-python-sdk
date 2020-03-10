#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name="CheckmarxPythonSDK",
    version="0.0.2",
    author="Happy Yang",
    author_email="happy.yang@checkmarx.com",
    description="Checkmarx Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/checkmarx-ts/checkmarx-python-sdk",
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.22.0",
        "requests-toolbelt>=0.9.1",
    ],
    extras_require={
        "dotenv": ["python-dotenv"],
        "dev": [
            "pytest",
            "coverage",
        ],
    },
)
