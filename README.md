# SimpleEtherWallet

What is SimpleEtherWallet?

SimpleEtherWallet is a non-custodial wallet, 100% built in Python, that aims to be user-friendly, minimalistic, and easy to use.

It operates on the Ethereum mainnet, meaning that all ERC-20 tokens can be sent from/sent to SimpleEtherWallet.

SimpleEtherWallet currently does **not** support connecting to dApps, but this could change in the future.

SimpleEtherWallet currently does **not** support NFTs, but this could change in the future.

**Note on current limitations**:
1. The API that is used to fetch coin price data is a free API. This comes with the limitation of not being able to get the price data of all ERC-20 cryptocurrencies.
    If, you are a memecoin master/hunter/hoarder, I would suggest you hold off using SimpleEtherWallet, until I am able to afford a paid API, or find some other way around this.
    
3. There is no built-in swap at the moment. This *might* come in a future update.
4. There is no built-in browser at the moment. This *might* come in a future update.
5. There is no WalletConnect feature at the moment. This *might* come in a future update.
6. There is no way to scan a QR code right now. This *is* coming in a future update.

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

Now that you have `Python`, you can either execute the `install-depends.py`, or
you will have to issue a few commands with `Python`'s package manager called `pip`.

### install-depends.py route:
1. `cd` into the SimpleEtherWallet that you have installed

```
cd /path/to/simpleetherwallet
```

2. Run the `install-depends.py` script by issuing the following command

```
py ./insta-depends.py
```

Once you have installed every dependency, you are ready to run SimpleEtherWallet (skip to Final Steps)

### Manual route:
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

If you do not have Python installed, issue the following command:

```
sudo apt install python3
```

**Change** `apt` **to your distro's package manager**

Now that you have `Python`, you can either execute the `install-depends.py`, or
you will have to issue a few commands with `Python`'s package manager called `pip`.

### install-depends.py route:
1. `cd` into the SimpleEtherWallet that you have installed

```
cd /path/to/simpleetherwallet
```

2. Run the `install-depends.py` script by issuing the following command

```
python3 ./insta-depends.py
```

Once you have installed every dependency, you are ready to run SimpleEtherWallet (skip to Final Steps)

### Manual route:
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


