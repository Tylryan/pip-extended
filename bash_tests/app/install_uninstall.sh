#!/usr/bin/bash




app_testing (){
    name_one='test1'
    name_two='test2'
    file_one_location=~/$name_one/src/$name_one.py
    test_one_location=~/$name_one/test/test_default.py
    file_two_location=~/$name_two/src/$name_two.py
    test_two_location=~/$name_two/test/test_default.py
    cd ~/ ;
    # Can't and shouldn't be able to create two apps at once
    echo "Creating New Apps"
    asu app new $name_one -c -t ;
    if [[ ! -f $file_one_location ]];then
        echo "Error: asu app new FAILED"
        exit 1
    fi

    if [[ ! -f $test_one_location ]];then
        echo "Error: asu app new -c -t FAILED"
        exit 1
    fi

    cd $name_one || exit 1 ;
    # This isn't how this actually works, but it works perfectly for testing
    # This just creates two aliases for the same project
    echo "Installing..."
    asu app install $name_one,$name_two || exit 1 ;

    echo "Checking if the executables were installed."
    # Check to see if both executables are there
    for executable in $name_one $name_two
    do 
        if [[ ! -f ~/.local/bin/$executable ]];then 
            echo "Executable $executable not there"
            echo "Installing FAILED"
            exit 1
        fi
    done

    # This also checks to see if the executables are there. Twice as secure
    asu app list ;
    output=`asu app list` || exit 1;
    if [[ $output != "['asu', '${name_one}', '${name_two}']" ]];then
        echo "asu app list failed"
        exit 1
    fi
    echo "Uninstalling..."
    asu app uninstall $name_one,$name_two
    if [[ -f ~/.local/bin/${name_one} || -f ~/.local/bin/${name_two} ]];then
        echo "Error: asu app uninstall FAILED"
        exit 1
    fi

    cd ~/ ; rm -rf $name_one $name_two
    asu app list ;
    exit 0
}

app_testing
