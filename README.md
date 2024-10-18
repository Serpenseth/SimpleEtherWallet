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


Linux users: To run SimpleEtherWallet on Linux, the program is ran like this:

1) open the terminal

2) `cd` into the simpleetherwallet folder

    cd /path/to/simplewallet

**Make sure to change** `/path/to/simpleetherwallet` **to the location where your simpleetherwallet folder is located**

3) Check if you have the proper dependencies installed by executing the following command:

    ./install-depends.sh

This will ask you if you want to install missing dependencies (SimpleEtherWallet cannot run without these dependencies)

4) Run SimpleEtherWallet by issuing the following command:

    python3 ./simpleetherwallet.py

Done!

Next time you want to launch SimpleEtherWallet, skip step 3.


The Windows source code comes bundled with the files that are used to build the installer `SimpleEtherWallet_installer`.
This gives you a look inside the installer, while also giving you the ability to customize the installer.

**In order to modify the contents of the installer,** `NSIS` **is required.**

For example; say you do not want the installer to create a desktop shortcut (which it does by default);
To change this, delete the following line from `installer.nsi`:

    CreateShortCut "$Desktop\SimpleEtherWallet.exe.lnk" "$INSTDIR\simpleetherwallet.pyw" \
      '' "$INSTDIR\eth.ico"

Once that is done, right click `installer.nsi`, and click `Compile NSIS Script`.
Then double-click `SimpleEtherWallet_installer`.

Now you will not have a desktop shortcut!


Donations cannot be made within the program, for now. However, the crypto that I accept via donations are listed in the "Donate" section of "Menu"

All comments, both positive, and negative, are welcome! Please email them to me!

[ TO THE MOON!!!! ]



