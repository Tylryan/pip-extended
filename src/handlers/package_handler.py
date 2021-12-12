#!/usr/bin/python3.9
import os
import json
import sys

from src import snippets


class Package_Handler:

	def __init__(self, env_management):
		self.environment = env_management
		self.current_env = env_management.current_env
		self.current_env_location = env_management.current_env_location
		self.env_location = env_management.env_location
		self.home = env_management.home
		self.config = env_management.config
		self.python_version = env_management.python_version

	def search_repository(self, package_name, pages):
		# os.system(f"pip_search {package_name}")
		# package_repo_handler = Package_Repo_Handler()
		# package_repo_handler.search(package_name, pages)
		pass

	def install_package(self, package_name, env_name):
		if env_name == None:
			env_location = f"{self.env_location}{self.current_env}/bin/activate"
			for package in package_name.split(","):
				os.system(
					f"source {env_location} && pip install {package}")
			return

		env_location = f"{self.env_location}{env_name}/bin/activate"
		for package in package_name.split(","):
			os.system(
				f"source {env_location} && pip install {package}")

	def uninstall_package(self, package_name, env_name):
		env_location = f"{self.env_location}{env_name}/bin/activate"
		for package in package_name.split(","):
			os.system(
				f"source {env_location} && pip uninstall {package}")

	def find_main_dir(self):
		dir_contents = os.listdir()
		is_main_dir = dir_contents.__contains__('src')
		while is_main_dir == False:
			os.chdir("..")
			dir_contents = os.listdir()
			is_main_dir = dir_contents.__contains__('src')
		cwd = os.getcwd()
		return cwd

	def find_main_file(self):
		# Find main directory via config.json
		dir_contents = os.listdir()
		is_main_dir = dir_contents.__contains__('config.json')
		while is_main_dir == False:
			os.chdir("..")
			dir_contents = os.listdir()
			is_main_dir = dir_contents.__contains__('config.json')

		try:
			with open("config.json") as file:
				data = json.load(file)
		except Exception as e:
			print("""
You're missing "config.json".
Soon there will be a command to fix this.
At the moment you can put this into your \"config.json\":

$ echo '{ "main_file":"path-to-your-actual-main-file" }' > config.json

Move this file inside your top most project directory.
					""")
			sys.exit()
		main_file = data["main_file"]
		return main_file

	def run_main_file(self):
		main_file_location = self.find_main_file()
		os.system(f"python {main_file_location}")

	def build(self):
		main_file_location = self.find_main_file()
		name = self.find_main_dir().split("/")[-1]
		# Default name is the name of your main directory
		os.system(f'pyinstaller {main_file_location} -F -n {name}')

	def uninstall_asu(self):
		os.system("rm ~/.local/bin/asu")

	def update_asu(self):
		"""Updates auto-setup (asu)"""
		# Install
		os.system("wget -O ~/asu \
				https://github.com/Tylryan/auto-setup/raw/main/dist/asud \
				&& chmod 744 ~/asu")
		# Remove old
		os.system("rm ~/.local/bin/asu")
		# Move In New
		os.system("mv ~/asu ~/.local/bin")

	# TODO Default app name == main.py name
	def install_app(self, app_name, dev_environment=""):
		"""Global install of your application"""
		project_name = self.find_main_dir().split(
			"/")[-1].replace("-", "_").replace(" ", "_")
		executable_location = f"{self.find_main_dir()}/dist/{project_name}"
		for app in app_name.split(","):
			self.track_app(app)
			install_location = f"~/.local/bin/{app}"
			if dev_environment != "":
				install_location = f"{self.env_location}{dev_environment}/bin/{app}"
			self.build()
			os.system(f"cp {executable_location} {install_location}")
		return

	def uninstall_app(self, app_names, dev_environment=""):
		for app in app_names.split(","):
			install_location = f"$HOME/.local/bin/{app}"
			if dev_environment != "":
				install_location = f"{self.env_location}{dev_environment}/bin/{app}"
			# TODO Fix this quick fix
			# is_installed = os.path.exists(install_location)
			# if is_installed == True:
			self.untrack_app(app)  # I think this is another guard
			os.system(f"rm {install_location}")
			# else:
			#     print(f"Error: {app_name} is not installed")

	def track_app(self, app_name):
		env = self.environment

		section, key = "app", "installed_apps"
		env.config_values_append(section, key, app_name)

	def untrack_app(self, app_name):
		env = self.environment
		installed_apps = self.list_installed_apps()
		if installed_apps.__contains__(app_name) != True:
			print(f"Error: {app_name} is either misspelled or not installed")
			print("Run `asu app list` to see all installed apps")
			return
		new_list = list(filter(lambda x: x != app_name, installed_apps))
		new_list_as_string = ' '.join(new_list)
		env.config['app']['installed_apps'] = new_list_as_string
		env.write_all_config_changes()

	def list_installed_apps(self):
		if self.config.sections().__contains__('app'):
			apps = self.config['app']['installed_apps']
			return apps.split(" ")
		else:
			print("You don't have any apps installed")
			return []

	def create_class_file(self, cli_input):
		cli_input = cli_input.split(".")[0].replace("-","_").lower()
		main_file = cli_input.split("/")[-1]
		class_name = main_file.title().replace("_","")
		directories = "/".join(cli_input.split("/")[:-1])
		command = f"mkdir -p {directories} && touch {cli_input}.py "
		if len(directories) < 1: 
			command = f"touch {main_file}.py"
		os.system(command)
		class_snippet = snippets.cli_create_class(class_name)

		file = open(f"{cli_input}.py", "w")
		file.write(class_snippet)
		file.close()

	def update_env_command(self, env_name):
		main_directory = self.find_main_dir()
		env_location = f"{self.env_location}{env_name}/bin/activate"
		os.system(
			f"source {env_location} && cd {main_directory} && pip install -e .")
	
	def add_test_directory(self):
		main_directory = self.find_main_dir()
		os.system("mkdir test")

	def run_tests(self):
		"""
		Runs any test in your test/ directory whose file starts with "test"
		Can be run from anywhere in your project directory
		"""
		main_directory = self.find_main_dir()
		# For this to work you have to have __init__.py in all subdirectories of test/
		command = f"python -m unittest discover test"
		os.system(command)

	# def list_installed_packages(self):


if __name__ == "__main__":
	from src.handlers.environment_handler import Environment_Handler

	# Using Package Handler
	# package_handler.install_app("something")
	# pip.pip_install_package("numpy")
	# pip.run_main_file()
	# ---------------------------------------------------------------------

	# Read config from Package Handler
	environment_handler = Environment_Handler()
	environment_handler.read_config()
	package_handler = Package_Handler(environment_handler)
	print(package_handler.current_env)
	# package_handler.create_class_file("dir1/dir2/andy")
	# package_handler.update_env_command("asu-dev")
	# print(environment_handler.current_env)
	# config = package_handler.config
	# virtual_envs = config['virtual_envs']
	# virtual_env_section = config.get(
	#     'virtual_envs', 'user_env_location')
	# -------------------------------------------------------------------
	# a = package_handler.list_installed_apps()
	# package_handler.track_app("you")
	# package_handler.track_app("there")
	# package_handler.track_app("how")
	# a = package_handler.list_installed_apps()
	# print(a)
	# package_handler.untrack_app("how")
	# a = package_handler.list_installed_apps()
	# print(a)
	# a = package_handler.list_installed_apps()
	# print(a)
