#!/usr/bin/python3

import os
import click
from src.handlers.environment_handler import Environment_Handler
from src.handlers.package_handler import Package_Handler

em = Environment_Handler()
em.read_config()
package_handler = Package_Handler(em)


@click.group()
def env_cli():
    pass


@env_cli.group(help="Manage Virtual Environments")
def env():
    pass


@env.command("new", help="Setup a new virtual environment")
@click.argument('env_name')
@click.option("-p","--python-version",  default = "", type=float,
help = """
Specify which python version you would like to install
pipe help python will list all python version installed.
EXAMPLE: pipe env new <env-name> -p 3.6
""")
def new_env(env_name, python_version):
    em.create_environment(env_name,python_version)


@env.command(help="Gives you the command to start up an environment")
@click.argument('environment_name')
def start(environment_name):
    em.activate_environment(environment_name)


@env.command(help="Remove Virtual Environment Entirely")
@click.argument('env_name')
def remove(env_name):
    """Removes an entire virtual environment from virtual_env"""
    em.remove_environment(env_name)


# Remove Command from Virtual Env


@env.command(name="list", help="List all Virtual Environments")
def list_envs():
    return em.get_all_environments(True)


# @env.command(help="Start up a Virtual Environment")
# @click.argument('env_name')
# def start(env_name):
#     print("Still a work in progress. Doesn't work just yet")
    # em.activate_environment(env_name)


@env.command(help="Stop the current Virtual Environment")
def stop():
    print("Still a work in progress. Doesn't work just yet")
    # em.deactivate_environment()
    #------------------------- COMMANDS


@env_cli.group(help="Manage Your Shell Commands")
def command():
    pass


# Put this back under the "env" group
@command.command(help="Remove Command from Virtual Environment")
@click.argument('command_name')
def remove(command_name):
    """Removes just the executable and library from the virtual environment """
    em.remove_multiple_command_from_environment(command_name)
    print(f"Removed Command: {command_name}")


@command.command(help="Updates your application's executable in the current environment")
@click.argument('env_name')
def update(env_name):
    package_handler.update_env_command(env_name)


    # @command.command(help="NI: Will update app command in env 'pip install -e .'")
    # @click.argument()
    # def update():
    # """Pip Install -e <location of setup.py"""
    # # find config.json
    # # os.system('pip install -e')
    # print(f"Error: This command has yet to be implemented")
    # project = click.CommandCollection(sources=[project])
if __name__ == "__main__":
    env_cli()
