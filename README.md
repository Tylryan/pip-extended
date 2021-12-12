# Asu Python Package Manager
## About
### Imagine Rust's **Cargo** or Javascript's **NPM**
    - I'm trying give modern functionality to Pip
## Common Commands
## Run Python Program From Anywhere In The Project Tree
- `asu run`
## Search Pip Repository for Packages
- `asu search <package>`
## Create A Virtual Environment
- `asu env new <env-name>`
## Build A Python Executable File From Anywhere In The Project Tree
- `asu app build`
## Create A Setup.py File
- `asu app setup`
## Pip (Un)Install Packages
- `asu (un)install <package-name>`


# Python3.6 is required before installing

# Install And Build (Recommended)
- `git clone https://github.com/Tylryan/auto-setup.git ~/asud && bash ~/asud/install.sh && cd`

# Install Asu (Executable Only)
- `wget -O ~/requirements.txt https://github.com/Tylryan/auto-setup/raw/main/requirements.txt && pip install -r ~/requirements.txt --user && rm ~/requirements.txt`
- `wget -O ~/.local/bin/asu https://github.com/Tylryan/auto-setup/raw/main/dist/asud && chmod 744 ~/.local/bin/asu`


# Updating Asu
To update to the most recent version of Asu run:
- `asu asu update`
# Uninstall Asu
- `asu asu uninstall`
