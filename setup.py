#!/usr/bin/env python
from setuptools import setup, find_packages
import os

version = ""
with open(os.path.join("OpenRCSimulator", "version.txt"), "r") as file:
    version = file.read().strip()

readme = ""
with open("README.md", "r") as file:
    readme = file.read()

with open("requirements.txt", "r") as file:
    requirements = [_.strip() for _ in file.readlines() if len(_.strip()) > 0]

setup(
    author="Huntler",
    python_requires=">=3.9",
    classifiers=[],
    description="Simulator of the OpenRC with interfaces for machine learning.",
    entry_points={
        "console_scripts": [
            "openrc-sim=OpenRCSimulator.main:main"
        ]
    },
    install_requirements=requirements,
    keywords="OpenRC",
    name="OpenRC-Simulator",
    packages=find_packages(include=[
        "OpenRCSimulator", "OpenRCSimulator.*"
    ]),
    package_dir={"OpenRCSimulator": "OpenRCSimulator"},
    package_data={"OpenRCSimulator": ["resources/*.png"]},
    include_package_data=True,
    url="https://github.com/Huntler/OpenRC-Simulator",
    version=version,
    zip_safe=True
)