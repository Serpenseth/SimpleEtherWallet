#!/bin/bash

declare misspy
declare missseg
declare missw3
declare missulib

# Is python3 installed?
if [[ -z $(command -v python3) ]]; then
    printf "Python3 is not installed on this device\n"
    misspy=1
    
else
    # Is python version good enough?
    py=$(python3 --version)
    version=$(echo $py | cut -d ' ' -f 2)
    
    if [[ $version < "3.8.10" ]]; then
        printf "Python version is too old... have: $version, requires: python3 version >= 3.8.10\n"
    fi
fi

# segno
pip show segno &> /dev/null || {
    missseg=1

    egno=$(pip show segno | sed -n '2p')
    version=$(echo $segno | cut -d ' ' -f 2)

    # Checking segno version to see if it's too old
    if [[ $version < "1.6.1" ]]; then
        printf "Package segno is too old... have: $version, requires: segno >= 1.6.1\n"
    fi
}

# web3
pip show web3 &> /dev/null || { 
    missw3=1
    
    w3=$(pip show web3 | sed -n '2p')
    version=$(echo w3 | cut -d ' ' -f 2)

    # Checking web3 version to see if it's too old
    if [[ $version < "7.2.0" ]]; then
        printf "Package web3 is too old... have: $version, requires: web3 >= 7.2.0\n"
    fi
}

# eth-account
# It is required by web3, so if web3 is not installed, 
# then eth-account is most definitely not installed, either

if [[ $missw3 -eq 1 ]]; then
    printf "Package eth-accounts is most likely missing\n"

else
    ethacc=$(pip show eth-account | sed -n '2p')
    version=$(echo $ethacc | cut -d ' ' -f 2)

    # Checking eth-account version to see if it's too old
    if [[ $version < "0.13.3" ]]; then
        printf "Package web3 is too old... have: $version, requires: eth-account >= 0.13.3\n"
    fi
fi

# urllib3
pip show urllib3 &> /dev/null || {
    missulib=1
    
    urllib=$(pip show urllib3 | sed -n '2p')
    version=$(echo $urllib | cut -d ' ' -f 2)

    # Checking urllib3 version to see if it's too old
    if [[ $version < "2.2.2" ]]; then
        printf "Package urllib is too old... have: $version, requires: urllib >= 2.2.2\n"
    fi
}

if [[ $misspy -eq 1 ]];   then echo "Python3 is not installed"; fi
if [[ $missseg -eq 1 ]];  then echo "segno is not installed";   fi
if [[ $missw3 -eq 1 ]];   then echo "web3 is not installed";    fi
if [[ $missulib -eq 1 ]]; then echo "urllib3 is not installed"; fi


if [[ $misspy -eq 1 ]] || [[ $missseg -eq 1 ]] || [[ $missw3 -eq 1 ]] || [[ $missulib -eq 1 ]]; then
    echo "This script can install these dependencies for you. Is this ok? (Y/n) "
    read rep

    case $rep in 
        Y|Yes|yes|y) 
            if [[ $misspy -eq 1 ]];   then sudo apt install python3; fi
            if [[ $missseg -eq 1 ]];  then pip install segno; fi
            if [[ $missw3 -eq 1 ]];   then pip install web3 && pip install eth-account; fi
            if [[ $missulib -eq 1 ]]; then pip install urllib3; fi
        ;;
        
        N|No|no|n) 
            local fpath="$(dirname "$(readlink -f "$0")")"
            local fname="$fpath.requirements.txt"
            
            echo "The list of required packages has been saved to $fname"
        
            if [[ $misspy -eq 1 ]]; then 
                echo "python3 (>= 3.8.10)" >> $fname
            fi
            
            if [[ $missseg -eq 1 ]]; then 
                echo "segno (>= 1.6.1)" >> $fname
            fi
            
            if [[ $missw3 -eq 1 ]]; then 
                echo "web3 (>= 7.2.0)" >> $fname 
                echo "eth-account (>= 0.13.3)" >> $fname
            fi
            
            if [[ $missulib -eq 1 ]]; then 
                echo "urllib (>= 2.2.2)" >> $fname
            fi
        ;;
        
        *) echo "Invalid input"
    esac
fi    
    
    
    
    
    
    
    
    
    
