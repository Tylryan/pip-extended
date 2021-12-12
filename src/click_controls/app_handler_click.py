#!/usr/bin/python3.9
import click
from src.handlers.environment_handler import Environment_Handler
from src.handlers.setup_handler import Setup_Handler
from src.handlers.package_handler import Package_Handler

# environment_handler = Environment_Handler()
# package_handler = Package_Handler(environment_handler)

environment_handler = Environment_Handler()
environment_handler.read_config()
package_handler = Package_Handler(environment_handler)


@click.group()
def app_cli():
    pass


@app_cli.group(help="App Related Commands")
def app():
    pass


@app.command(help="Create Setup.py for an existing application")
@click.option("-c", "--class-snippet", is_flag=True,
              default=False,
              help="Create a setup.py file and environment executable",
              )
def setup(class_snippet):
    setup_handler = Setup_Handler()
    setup_handler.set_up_project(class_snippet)
    print("Project Setup")


# TODO Create --with-env option. Creates an env with the name of the project
@app.command(help="Bare Bones Application Boiler Code")
@click.argument('project_name')
@click.option('-e', '--with-virtual-environment', is_flag=True, default=False,
              help="Will setup a virtual environment with the same name as the project")
@click.option("-c", "--class-snippet", is_flag=True, default=False,
              help="Determines whether the main module contains a class. Default = Function")
@click.option("-t", "--unit-testing", is_flag=True, default=False,
              help="Will setup a unit test directory with a default test")
def new(project_name, class_snippet, with_virtual_environment, unit_testing):
    setup_handler = Setup_Handler()
    setup_handler.new_project(
        project_name,
        class_snippet,
        with_virtual_environment,
        unit_testing
    )


@app.command(help="Create a Python executable")
def build():
    package_handler.build()


@app.command(help="Install a build of your application.\
             Use it after `pipe app build`")
@click.argument('app_name')
@click.option('-e', '--environment_name', default="",
              help="""
Install the app in a specific environment. Insert an ENVIRONMENT_NAME """)
def install(app_name, environment_name):
    package_handler.install_app(app_name, environment_name)


@app.command(help="Uninstall an application build")
@click.option('-e', '--environment_name', default="",
              help="""
Install the app in a specific environment. Insert an ENVIRONMENT_NAME """)
@click.argument('app_name')
def uninstall(app_name, environment_name):
    package_handler.uninstall_app(app_name, environment_name)


@app.command(help="Create a requirements.txt for an existing application")
def requirements():
    print("You have not set this up in Click")


@app.command(help="List of all your currently downloaded exacutables/builds")
def list():
    installed_packages = package_handler.list_installed_apps()
    print(installed_packages)


@app.command("test", help="Run All Your of Your Unit Tests From Anywhere")
def run_unit_tests():
    package_handler.run_tests()


@app_cli.group(help="Code snippets and creation shortcuts")
def snip():
    pass


@snip.command("class", help="""\
Creates a class file and the directory to it \
input example: pipe snip class dir1/dir2/file"""
              )
@click.argument("path")
def class_(path):
    package_handler.create_class_file(path)


if __name__ == "__main__":
    app_cli()
