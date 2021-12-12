#!/usr/bin/bash

home=$HOME
pyinstaller_compat_python=python3.6
install (){
    cd ~/pipe-dev
    python3 -m pip install virtualenv --user || exit 1;
    # Pyinstaller doesn't work for python3.10
    python3 -m virtualenv ~/.python_environs/default -p /usr/bin/$pyinstaller_compat_python || exit 1;
    mkdir ~/.config/pipe || exit 1;
    touch ~/.config/pipe/config.ini || exit 1;
    echo "user_env_location = $home/.python_environs/" > ~/.config/pipe/config.ini || exit 1 ;
    source ~/.python_environs/default/bin/activate || exit 1 ;
    pip install -e . || exit 1 ;
    pipe-dev app install pipe  || exit 1 ;
    echo
    echo
    pipe || exit 1 ;
    rm -rf ~/pipe-dev || exit 1 ;
    exit 0
}

install
