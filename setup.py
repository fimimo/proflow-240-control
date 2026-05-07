#!/usr/bin/env python3

from setuptools import setup, find_packages
import os
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="proflow-240-control",
    version="1.0.0",
    author="fimimo",
    description="Aplicativo Linux para controlar Watercooler Jungle Leopard ProFlow 240",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fimimo/proflow-240-control",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "proflow-240=src.main:main",
        ],
    },
)
