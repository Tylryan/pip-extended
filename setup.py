#!/usr/bin/python

from setuptools import setup, find_packages
import os


setup(
    name='pip extended',
    version='0.1.1',
    include_package_data=False,
    packages=find_packages(),
    install_requires=[
        "click", "virtualenv", "pyinstaller", "rich", "beautifulsoup4",
        "requests", "virtualenvwrapper"]
)

if os.path.exists("~/.config/pipe") == False:
    print("Create a config file in ~/.config/pipe")
    # Create directory for the config file
    os.system('mkdir ~/.config/pipe')
    # creating the config file
    os.system("cp src/config.ini ~/.config/pipe")
