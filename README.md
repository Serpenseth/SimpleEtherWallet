# SimpleEtherWallet

What is SimpleEtherWallet?

SimpleEtherWallet is a non-custodial wallet, 100% built in Python, that aims to be user-friendly, minimalistic, and easy to use.

It operates on the Ethereum mainnet, meaning that all ERC-20 tokens can be sent from/sent to SimpleEtherWallet.

SimpleEtherWallet currently does **not** support connecting to dApps, but this could change in the future.

*Benefits of using SimpleEtherWallet*:
1. Non-custodial. You own your crypto assets. Your private key is stored on your device, and it is also encrypted. Your private key does not leave your device while using SimpleEtherWallet as well.

2. Simple. The design choices were all geared towards simplicity.

3. Lightweight. SimpleEtherWallet barely comsumes any resources. It is very light, and easy to run.
    On my Windows 10 laptop that is running hardware that is a few years old, only 52.4 MB of ram is used!

4. SimpleEtherWallet runs on both Windows, and Linux!

# Windows:

## Requirements:
SimpleEtherWallet is a Python program. You will need at least `python v3.7.0`.

You can find the latest Python version here: [www.python.org/downloads/](www.python.org/downloads/)

Install Python and make sure it is installed correctly by opening the `cmd prompt` and issuing the following command:

```
py --version
```

This will print `Python 3.12.6` (your version may be different)

Now that you have `Python`, you will to issue a few commands with `Python`'s package manager called `pip`.

The following packages are required to execute SimpleEtherWallet:

`segno` version >= 1.6.1

`web3` version >= 7.2.0

`eth-account` version >= 0.13.3

`urllib3` version >= 2.2.3

To do this, issue the following string of commands in the terminal:

```
pip install segno && pip install web3 && pip install eth-account && pip install urllib3
```

Now you have everything!

## Final steps
Move the `images` folder and `simpleetherwallet-win.pyw` into a folder of your choice (for example `C:\Users\Bob\SimpleEtherWallet`)

To run SimpleEtherWallet, double click `simpleetherwallet-win.pyw`.

# Linux:

## Requirements:
`python v3.8.0`+ is needed on Linux.

If you are on a distro that uses  `apt`, I have created the `install-depends.sh` script which takes care of all the dependencies for you. 

Simply `cd` to where you have downloaded simpleetherwallet, and run

```
./install-depends.sh
```

Then, you run SimpleEtherWallet by executing the following command:

```
python3 ./simpleetherwallet.py
```

***If you prefer to do everything manually***
If you do not have Python installed, or if your Python version is too old; issue the following command:

```
sudo apt install python3
```
**Change** `apt` **to your distro's package manager**

Now that you have Python, issue

```
python3 --version
```

if it does not result in an error, you have successfully installed Python3.

Now you need the dependencies via `pip`.

Simply execute the following string of commands:

```
pip install segno && pip install web3 && pip install eth-account && pip install urllib3
```

## Final steps
Make sure the `images` folder is in the same folder as `simpleetherwallet.py`. Otherwise, the program will fail to run.

To run SimpleEtherWallet, execute:

```
python3 ./simpleetherwallet.py
```

# Donate

ETH address: 0x508547c4Bac880C1f4A2336E39C55AB520d43F59

Donations cannot be made within the program, for now. However, the crypto that I accept (other than `ETH` via donations are listed in the "Donate" section of "Menu"

# Contact me

All comments, both positive, and negative, are welcome! Please email them to me!

Contact me at: <enkisaur@tutanota.com>

[ TO THE MOON!!!! ]


