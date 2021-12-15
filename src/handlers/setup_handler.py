#!/usr/bin/python3.9

import json
import os
import subprocess as sp
from typing import List, Tuple

from setuptools import find_packages

from src import snippets
from src.handlers.environment_handler import Environment_Handler
from src.handlers.package_handler import Package_Handler

environment_handler = Environment_Handler()
environment_handler.read_config()
package_handler = Package_Handler(environment_handler)

# Create -l or -g for global or local
# Global will be what it is now
# Local will save a config file in the project directory that will contain the location of the main file
# Will be used for something like `asu project run`


class Setup_Handler:
    def __init__(self):
        self.project_details = ()
        self.new_project_details = ()

    # set_up_existing_project
    # TODO set up a verbose option for Click
    def set_up_project(self, class_snippet: bool, verbose=False) -> None:
        self.create_requirements_file()
        self.create_setup(self.get_info(), class_snippet)
        self.install_project(verbose)

    def new_project(self, project_name: str, class_snippet: bool, with_env: bool, unit_testing: bool) -> None:
        """ Create project structure from scratch """
        project_name = project_name.lower().replace(" ", "_").replace("-", "_")

        if with_env:
            environment_handler.create_environment(project_name)

        bare_bones_function_snippet: str = f"""\
#!/usr/bin/python3

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
        """
        bare_bones_class_snippet = f"""\
#!/usr/bin/python3

class {project_name.title()}:
    def __init__(self):
        pass

    @staticmethod
    def main():
        print("Hello World!")

if __name__ == "__main__":
 {project_name.title()}.main()
            """
        os.system(
            f"mkdir -p {project_name}/src && touch {project_name}/src/{project_name}.py")
        os.system(f"touch {project_name}/config.json")
        with open(f"{project_name}/config.json", "w") as file:
            config_json_data = {
                "main_file": f"src/{project_name}.py"
            }
            json.dump(config_json_data, file)
        file.close()

        if unit_testing:
            self.setup_unit_testing(project_name)

        if class_snippet is False:
            with open(f"{project_name}/src/{project_name}.py", "w") as file:
                file.write(bare_bones_function_snippet)
                file.close()
        else:
            with open(f"{project_name}/src/{project_name}.py", "w") as file:
                file.write(bare_bones_class_snippet)
                file.close()

    def get_info(self) -> None:
        """ Retrieves Project Information from the user and returns it in a Tuple """

        executable_name = input("cli executable DEV name: ").lower().replace(" ", "_") or \
            os.getcwd().split("/")[-1].replace(" ", "_").strip()
        print("=================================================================")
        print("\nWhen in doubt, leave the rest blank.\n")
        print("=================================================================")
        project_name = input("project name: ").lower().replace(" ", "_") or \
            os.getcwd().split("/")[-1].replace(" ", "_").strip()
        project_main_module = input("main file: ") or project_name
        project_entry_point = input(
            "main class/function name: ") or project_name
        project_version = input("version: ") or "0.0.1"
        project_include_package_data = input("include_package_data: ") or False
        project_packages = find_packages()[:-1]
        project_installs = self.get_install_requires()
        project_details = (
            project_name, executable_name, project_version, project_packages,
            project_include_package_data, project_entry_point, project_main_module,
            project_installs
        )
        print("\n")
        self.project_details = project_details

    def create_setup(self, project_details: Tuple[str,str,str,str,str,str,str,str], class_snippet: bool) -> None:
        """ Creates a setup.py file based of the given information """
        template = ""
        if class_snippet: 
            template = snippets.class_setup(self.project_details)
        else: 
            template = snippets.function_setup(self.project_details)

        file = open("setup.py", "w")
        file.write(template)
        file.close()

    def get_install_requires(self) -> List[str]:
        """ Returns the current environment's installed Pip packages """
        command: str = "pip freeze | grep -Ev '(#|home|git)' | cut -d'=' -f1"
        install_requires: List[str] = os.popen(command).read().split("\n")[:-1]
        return install_requires

    def create_requirements_file(self) -> None:
        command: str = "pip freeze | grep -Ev '(#|home|git)' | cut -d'=' -f1 > requirements.txt"
        os.system(command)

    def install_project(self, verbose: bool=False):
        """ Pip installs the project """
        command = "python setup.py develop . 1> /dev/null"
        # TODO figure out this command thing
        if verbose: 
            command = "pip install -e ."
        success = os.system("pip install -e .")
        if success != 0:
            sp.sys.exit()

    # TODO Code copied. Figure out how to not do that
    def find_main_dir(self) -> str:
        """Finds the main directory of the project tree"""
        dir_contents: List[str] = os.listdir()
        is_main_dir: bool = dir_contents.__contains__('src')
        while is_main_dir is False:
            os.chdir("..")
            dir_contents = os.listdir()
            is_main_dir = dir_contents.__contains__('src')
        cwd: str = os.getcwd()
        return cwd

    def setup_unit_testing(self, project_name: str) -> None:
        # main_directory = self.find_main_dir()
        os.system(f"mkdir {project_name}/test")
        os.system(f"touch {project_name}/test/test_default.py")

        test_snippet: str = snippets.test_setup()

        file = open(f"{project_name}/test/test_default.py", "w")
        file.write(test_snippet)
        file.close()

        # os.system

    def run_tests(self) -> None:
        """
        Runs any test in your test/ directory whose file starts with "test"
        Can be run from anywhere in your project directory
        """
        main_directory: str = self.find_main_dir()
        # For this to work you have to have __init__.py in all subdirectories of test/
        command:str = "python -m unittest discover test"
        os.system(command)


if __name__ == "__main__":
    sh = Setup_Handler()
    # sh.new_project("Hello THERE", False)
    print(sh.find_main_dir())
