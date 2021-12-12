#!/usr/bin/bash

home=$HOME
pyinstaller_compat_python=python3.6
binary_install() {
    cd ~/pipe_dev
    pip install virtualenv --user || exit 1;
    # Pyinstaller doesn't work for python3.10
    mkdir ~/.python_environs
    python3 -m virtualenv ~/.python_environs/default -p /usr/bin/$pyinstaller_compat_python || exit 1;
    mkdir ~/.config/pipe
    touch ~/.config/pipe/config.ini
    echo "[virtual_envs]" > ~/.config/pipe/config.ini || exit 1 ;
    echo "user_env_location = $home/.python_environs/" >> ~/.config/pipe/config.ini || exit 1 ;
    source ~/.python_environs/default/bin/activate || exit 1 ;
    wget -O pipe https://github.com/Tylryan/pip-extended/raw/main/dist/pipe_dev
    chmod 744 pipe && mv pipe ~/.local/bin
}

binary_install
