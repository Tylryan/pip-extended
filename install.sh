#!/usr/bin/bash

home=$HOME
pyinstaller_compat_python=python3.6
install (){
    cd ~/pipe_dev
    pip install virtualenv --user || exit 1;
    # Pyinstaller doesn't work for python3.10
    mkdir ~/.python_environs
    python3 -m virtualenv ~/.python_environs/default -p /usr/bin/$pyinstaller_compat_python || exit 1;
    mkdir ~/.config/pipe
    touch ~/.config/pipe/config.ini
    echo "user_env_location = $home/.python_environs/" > ~/.config/pipe/config.ini || exit 1 ;
    source ~/.python_environs/default/bin/activate || exit 1 ;
    pip install -e . || exit 1 ;
    pyinstaller src/pipe.py -F -n pipe_dev || exit 1
    mv dist/pipe_dev $home/.python_environs/default/bin || exit 1
    pipe_dev app install pipe  || exit 1 ;
    echo
    echo
    pipe || exit 1 ;
    rm -rf ~/pipe_dev || exit 1 ;
    cd
    exit 0
}

install
