#!/usr/bin/python

from setuptools import setup, find_packages
import os


setup(
    name='pipe extended',
    version='0.1.0',
    include_package_data=False,
    packages=find_packages(),
    install_requires=[
        "click", "virtualenv", "pyinstaller", "rich", "beautifulsoup4",
        "requests", "virtualenvwrapper"]
)

if os.path.exists("~/.config/asu") == False:
    print("Create a config file in ~/.config/asu")
    # Create directory for the config file
    os.system('mkdir ~/.config/asu')
    # creating the config file
    os.system("cp src/config.ini ~/.config/asu")
