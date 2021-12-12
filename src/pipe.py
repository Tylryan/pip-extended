#!/usr/bin/python3.9
import click
import os
import subprocess as sp
from setuptools import find_packages
from time import sleep

from src.click_controls.app_handler_click import app_cli

from src.click_controls.environment_handler_click import env_cli
from src.click_controls.package_handler_click import package_cli


main = click.CommandCollection(sources=[app_cli, env_cli, package_cli])

if __name__ == "__main__":
    main()
