# Pipe (pip extended)
Only works for Linux when I can get it to work :)
![Pipe Example](./assets/basic-functionality.gif)
## About
### Imagine Rust's **Cargo** or Javascript's **NPM** for Python
## Common Commands
## Run Python Program From Anywhere In The Project Tree
- `pip run`
## Search Pip Repository for Packages
- `pipe search <package>`
## Create A Virtual Environment
- `pipe env new <env-name>`
## Build A Python Executable File From Anywhere In The Project Tree
- `pipe app build`
## Create A Setup.py File
- `pipe app setup`
## Pip (Un)Install Packages
- `pipe (un)install <package-name>`


# Python3.6 is required before installing

# Install And Build (Recommended)
- `git clone https://github.com/Tylryan/pip-extended.git ~/pipe_dev && bash ~/pipe_dev/install.sh && cd`
# Binary Install
- Stable-ish
    - `wget https://github.com/Tylryan/pip-extended/raw/main/stable_binary_install.sh && chmod 744 stable_binary_install.sh && bash stable_binary_install.sh`

- Nightly
    - `wget https://github.com/Tylryan/pip-extended/raw/main/nightly_binary_install.sh && chmod 744 nightly_binary_install.sh && bash nightly_binary_install.sh`

# Updating Pipe
To update to the most recent version of Pipe run:
- `pipe pipe update`
# Uninstall Pipe
- `pipe pipe uninstall`