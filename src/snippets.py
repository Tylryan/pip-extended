#!/usr/bin/python

def class_setup(project_details):
    project_name, executable_name, project_version, project_packages, \
        project_include_package_data, project_entry_point, \
        project_main_module, project_installs = project_details

    return f"""\
#!/usr/bin/python 
from setuptools import setup, find_packages 
setup(
    name='{project_name}',
    version='{project_version}',
    packages=find_packages(),
    include_package_data={project_include_package_data},
    install_requires={project_installs}
)"""


def function_setup(project_details):
    project_name, executable_name, project_version, project_packages, \
        project_include_package_data, project_entry_point, \
        project_main_module, project_installs = project_details

    return f"""\
#!/usr/bin/python 
from setuptools import setup, find_packages 
setup(
    name='{project_name}',
    version='{project_version}',
    packages=find_packages(),
    include_package_data={project_include_package_data},
    install_requires={project_installs}
)"""


def cli_create_class(file_name):
    class_snippet = f"""\
#!/usr/bin/python3

class {file_name}:
    def __init__(self):
        pass

    def main(self):
        print("Hello World!")

if __name__ == "__main__":
 {file_name.lower()} = {file_name}()
 {file_name.lower()}.main()
            """
    return class_snippet


def cli_create_function():
    function_snippet = f"""\
#!/usr/bin/python3

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
        """
    return function_snippet

def test_setup():
    test_snippet = f"""\
#!/usr/bin/python3

import unittest


def add(one, two):
    return one + two


class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 1), 2)
    """
    return test_snippet