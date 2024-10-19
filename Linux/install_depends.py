#!/usr/bin/env python3

"""
Copyright © 2024 Serpenseth

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys               # sys.executable
import subprocess  # check_call

# main
def main():
    missing = []

    import os
    os.system('color')

    #https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    fail     = '\033[91m'
    good  = '\033[92m'
    mods = '\033[96m'
    endc  = '\033[0m'

    print("\nChecking if this system has the required dependencies...\n")

    # Is segno installed?
    try:
        import segno
        print(f"{good}segno found{endc}, continuing...")

    except ModuleNotFoundError:
        print(f"{fail}segno is missing... {endc}")
        missing.append('segno')

    # Is web3 installed?
    try:
        import web3
        print(f"{good}web3 found{endc}, continuing...")

    except ModuleNotFoundError:
        print(f"{fail}web3 is missing... {endc}")
        missing.append('web3')

    # Is eth-account installed?
    try:
        import eth_account
        print(f"{good}eth_account found{endc}, continuing...")

    except ModuleNotFoundError:
        print(f"{fail}eth_account is missing... {endc}")
        missing.append('eth_account')

    # Is urllib3 installed?
    try:
        import urllib3
        print(f"{good}urllib3 found{endc}, continuing...")

    except ModuleNotFoundError:
        print(f"{fail}urllib3 is missing... {endc}")
        missing.append('urllib3')

    # All dependencies are already installed
    if len(missing) == 0:
        print("\nThis system has all the modules required to run SimpleEtherWallet")
        exit()

    else:
        m = ", ".join(missing)

        print(f"\nThe following modules are missing, and will be installed: {mods}{m}{endc}")
        inp = input("Continue? (Y/n) ")

        # Install dependencies
        if inp == 'Y' or inp == 'y':
            python = sys.executable
            subprocess.check_call([python, '-m', 'pip', 'install', *missing])

        # User decided to jump ship
        elif inp == 'N' or inp == 'n':
            print(f"\n{fail}SimpleEtherWallet requires the dependencies listed above to run, sorry!{endc}")
            exit()

if __name__ == "__main__" :
    main()





