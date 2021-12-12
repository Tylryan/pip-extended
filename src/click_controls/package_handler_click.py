#!/usr/bin/python3.9
import click
from src.handlers.package_handler import Package_Handler
from src.handlers.environment_handler import Environment_Handler
from src.handlers.package_repo_handler import Package_Repo_Handler


environment_handler = Environment_Handler()
environment_handler.read_config()
package_handler = Package_Handler(environment_handler)


@click.group()
def package_cli():
    pass


@package_cli.command(help="Pip: Install a package")
@click.argument('package_name')
@click.option("-e", "--env-name",
              help="The environment in which you would like to install this package",
              default=None)
def install(package_name, env_name):
    package_handler.install_package(package_name, env_name)


@package_cli.command(help="Pip: Uninstall a package")
@click.argument('package_name')
@click.option("-e", "--env-name",
              help="The environment in which you would like to uninstall this package",
              required=True)
def uninstall(package_name, env_name):
    package_handler.uninstall_package(package_name, env_name)


@package_cli.command(help="Pip: Search for a package")
@click.argument('package_name')
@click.option('-p', '--pages', type=int, default=1,
              help="Specify the number of pages to search")
def search(package_name, pages):
    # package_handler.search_repository(package_name)
    package_repo_handler = Package_Repo_Handler()
    package_repo_handler.search(package_name, pages)


@package_cli.command(help="Runs your program from anywhere inside your project directory")
def run():
    package_handler.run_main_file()


@package_cli.group(help="Update or Uninstall PIPE")
def pipe():
    pass


@pipe.command(help="Update PIPE")
def update():
    package_handler.update_asu()


@pipe.command(help="Uninstall PIPE")
def uninstall():
    package_handler.uninstall_asu()


if __name__ == "__main__":
    package_cli()
