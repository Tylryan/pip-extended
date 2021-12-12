#!/usr/bin/python3.9
import os
import configparser
import subprocess as sp
from src.handlers.package_handler import Package_Handler
from src.handlers.static_helpers import Static_Helpers as sh


# package_handler = Package_Handler(env_management)


class Environment_Handler:

    def __init__(self):
        self.config = ""
        # Start using this ya dummy
        self.home = os.popen("echo $HOME").read().strip()
        self.user = os.popen("echo $USER").read().strip()
        # or "config.ini"
        self.config_file_location = f"/home/{self.user}/.config/asu/config.ini" or "../config.ini"
        self.env_location = ""
        self.current_env_location = os.popen( "echo $VIRTUAL_ENV").read().strip()
        self.python_version = os.popen("python --version | cut -d'.' -f1-2 | tr -d ' '").read().strip().lower()
        self.current_env = os.getenv("VIRTUAL_ENV")

    def read_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_location)
        self.env_location = self.config["virtual_envs"]["user_env_location"]

    def config_values_append(self, section, key, value):
        """ Assuming you have already created the section,key and value"""
        try:
            if self.config[section][key].split(" ").__contains__(value):
                pass
            else:
                changed = self.config[section][key] + f" {value}"
                self.config[section][key] = changed
                self.write_all_config_changes()

        except:
            self.change_config_values(section, key, "")
            if self.config[section][key].split(" ").__contains__(value):
                pass
            else:
                changed = self.config[section][key] + f" {value}"
                self.config[section][key] = changed
                self.write_all_config_changes()

    def change_config_values(self, section, key, value):
        """Can add new values or change existing values"""

        try:
            self.config[section][key] = value
            self.write_all_config_changes()
        except:
            self.config[section] = {}
            self.config[section][key] = value
            self.write_all_config_changes()

    def write_all_config_changes(self):
        with open(self.config_file_location, 'w') as configfile:
            self.config.write(configfile)

    # TODO add a "verbose" option for the Click command
    def create_environment(self, env_name,python_version):
        env_location = self.config['virtual_envs']['user_env_location']
        for env in env_name.split(","):
            command = f"cd {env_location} ; virtualenv {env}"
            if python_version != "": command += f" --python /usr/bin/python{python_version}"

            os.system(command)
            if self.check_env_presence(env_name): print(f"Virtual Environment Created: {env}")
            else: print( f"Virtual Environment Updated: {env}")

    def check_env_presence(self, env_name):
        return True if self.get_all_environments().__contains__(env_name) else False

    # def remove_multiple_environments(self, env_name):

    def remove_environment(self, env_name):
        env_location = self.config['virtual_envs']['user_env_location']
        for env in env_name.split(","):
            if self.check_env_presence(env):
                result = os.system(
                    f'cd {env_location} ; rm -rf {env}')
                print(f"Virtual Environment Removed: {env}")
            else:
                print(f"Virtual Environment Not Found: {env}")

    def remove_multiple_command_from_environment(self, commands):
        for command in commands.split(","):
            self.remove_command_from_pip_environment(command)

    def remove_command_from_pip_environment(self, command):
        env_location = self.config['virtual_envs']['user_env_location']
        list_of_envs = self.get_all_environments(command)
        # Because it searches all envs, it can bypass asking the user to specify
        for env in list_of_envs:
            command_lib_location = f"{env_location}{env}/lib/{self.python_version}" + \
                f"/site-packages/{command}.egg-link"
            command_bin_location = f"{env_location}{env}/bin/{command}"
            # TODO put back == True if it messes up!
            if (os.path.exists(command_lib_location)):
                os.system(f"rm {command_lib_location}")
            if (os.path.exists(command_bin_location)):
                os.system(f"rm {command_bin_location}")

    def get_all_environments(self, to_console=False):
        env_location = self.config['virtual_envs']['user_env_location']
        if to_console == True:
            """Just Prints to console"""
            environments_list = os.system(
                f'ls {env_location} --format=single-column --color=auto')
            return 0
        else:
            """Returns a list"""
            environments_list = os.popen(
                f'ls {env_location} --format=single-column').read().split("\n")[:-1]
            return environments_list

    def activate_environment(self, env_name):
        print("Copy and paste the following code")
        command = f"source {self.env_location}{env_name}/bin/activate"
        # One day I'd like to use this
        # vew = "source ~/.local/bin/virtualenvwrapper.sh"
        # command = f"{vew} ; workon {env_name}"  # Virtualenvwrapper
        print(command)

    def deactivate_environment(self):
        print("Copy and paste the following")
        print("deactivate")


if __name__ == "__main__":
    import sys

    env = Environment_Handler()
    env.read_config()
    print(env.config_file_location)

    # env.activate_environment("asu-dev")
    # env.create_environment("two")
    # env.create_environment("three,four")
    # env.remove_environment("three,four")
    # env.activate_environment("temp")
    # env.start_env_tracking()
    # env.deactivate_environment()
    # sections = config.sections()
    # virtual_envs_section = config['virtual_envs']
    # virtual_env_location = config.get('virtual_envs', 'user_env_location')
    # env.config_values_append('apps', 'testing', 'doing')
    # new_list = old_list.append("hello")
    # self.config[section][key] = new_list

    # alist.append(1)
    # print(new_list)
    # print(alist)
    # env.config_values_append('and', 'alist', 'app_name')
    # print(config['and']['alist'])

    # print(config.get_all_environments(True))
    # config.remove_command_from_pip_environment('testly')
    # config.create_environment("env_test")
    # config.remove_command_from_pip_environment(arg)
    # config.change_config_values("virtual_envs", "name", "Ryan")
    # config.write_all_config_changes()
    # print(config.config['virtual_envs']['name'])
