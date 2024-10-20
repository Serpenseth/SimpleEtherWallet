#!/usr/bin/env python3

"""
Copyright © 2024 Serpenseth

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#===Version 2.0===#

# NOTE I'm a Python newbie; the code is messy!!!!

import os.path # os.path.exists()
import sys # restart program in Windows


from tkinter import *  # tkiner
from tkinter.filedialog import * # file-related functions
from tkinter import messagebox  # message box
from tkinter import ttk # Combobox

import tkinter as tk # shortcut
import os.path # os.path.exists()
import json  # JSON file manipulation

import segno # QR code

from web3 import Web3 # main Web3 module
from eth_account import Account

# condensed version of
# https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens
# NOTE: That link uses division, but I personally prefer right shift by 1
def center_window(Y, X: int, window: tk):
    x = (window.winfo_screenwidth()  >> 1) - (Y >> 1)
    y = (window.winfo_screenheight()  >> 1) - (X  >> 1)

    window.geometry('%dx%d+%d+%d' % (Y, X, x, y))

if os.name == 'nt':
    dest_path = 'C:\\ProgramData\\SimpleEtherWallet\\'

else:
    import os  # os.getlogin()

    current_usr = os.getlogin()
    dest_path    = "/home/" + current_usr + "/.SimpleEtherWallet/"

abi_json_file = dest_path + 'abi_data.json'
conf_file = dest_path + 'conf.json'
assets_json = ''

conf_file_contents = {
        'version': '1.0',
        'wallets': [],
        'rpc': 'https://rpc.mevblocker.io',
        'currency': 'USD',
        'theme': 'default',
    }

# check for permissions
if not os.path.exists(dest_path):
    try:
        os.mkdir(dest_path)

    except Exception:
        w = tk.Tk()
        w.withdraw()

        messagebox.showerror(
            master = w,
            title = "Error",
            message = "Fatal error: Could not create SimpleEtherWallet folder.   \nMake sure that you have write permissions",
            icon = "error",
        )

        w.destroy()
        quit()

# JSON abi file, used for token contracts
elif not os.path.exists(abi_json_file) or os.stat(abi_json_file).st_size == 0:
    with open(abi_json_file, 'w') as jsonfile:
        jsonfile.write("""[{"inputs":[{"internalType":"uint256","name":"_totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"},{"internalType":"bool","name":"_isBlacklisting","type":"bool"}],"name":"blacklist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"blacklists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"limited","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxHoldingAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minHoldingAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_limited","type":"bool"},{"internalType":"address","name":"_uniswapV2Pair","type":"address"},{"internalType":"uint256","name":"_maxHoldingAmount","type":"uint256"},{"internalType":"uint256","name":"_minHoldingAmount","type":"uint256"}],"name":"setRule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]
    """)

# Conf.json file
if not os.path.exists(conf_file) or os.stat(conf_file).st_size == 0:
    with open(conf_file, 'w') as f:
        json.dump(conf_file_contents, f)

# Load conf.json file
with open(conf_file, 'r') as f:
    conf_file_contents = json.load(f)

def questionbox(msg):
    box = messagebox.askquestion(
        title = "SimplEthWallet",
        message = msg,
        icon = "info"
    )

    if box == "yes":
        return True

    return False

packoptions = {
    "fill": "both",
    "expand": True
}

def selall(event):
    entry.select_range(start = 0, end = tk.END)
    entry.select_adjust(index = 0)

def newline(master, pady = 4):
    tk.Label(
        master = master,
        text = '\n',
    ).pack(pady = pady)


position = {"pos": 0}
is_new  = {"state": True}
nameofwallet = {"name": None}
account_addr = {"text": None}
filechosen = {'state': 0}

global recovered
recovered = 0

global imgfolder

if os.name == 'nt':
    imgfolder = os.path.dirname(__file__) + '/images/'

else:
    imgfolder = os.path.dirname(__file__) + '/images/'

    if not os.path.exists(imgfolder):
        """ messagebox.showerror() will complain that
            it is too early to call it, as there's no root window.
            The ugly solution is to create a Tk() like with no dest_path """

        w = tk.Tk()
        w.withdraw()

        messagebox.showerror(
            master = w,
            title = "Error",
            message = f"images folder is missing. Copy it to: {sys.path[0]}",
            icon = "error",
        )

        w.destroy()
        quit()

# default RPC provider
w3 = Web3(
    Web3.HTTPProvider(
        'https://rpc.mevblocker.io',
        #'https://rpc.ankr.com/eth',
        request_kwargs = {'timeout': 4}
    )
)

w3.provider.cache_allowed_requests = True

USDT_price:float = 0.0
USDC_price:float = 0.0

from urllib.request import urlopen

page_data = ''

try:
    # Found this link here: https://ethereum.stackexchange.com/questions/38309/what-are-the-popular-api-to-get-current-exchange-rates-for-ethereum-to-usd
    page_data = urlopen('https://api.coinbase.com/v2/exchange-rates?currency=ETH').read()

except Exception:
    pass

page = page_data.decode('utf-8')

def fetch_eth_price_in(coin_symbol) -> float:
    start = page.find(coin_symbol)
    end  = page.find(',', start, len(page))

    pricedata = page[start:end]

    pricedata = pricedata.replace(":", '')
    pricedata = pricedata.replace(coin_symbol, '')
    pricedata = pricedata.replace('"', '')

    return float(pricedata)

""" Old def fetch_price_of_and_convert_to(coin_symbol_base, coin_symbol_to) -> float:
    page_data2 = ''

    try:
        # Coin
        page_data2 = urlopen(f"https://api.coinbase.com/v2/exchange-rates?currency={coin_symbol_base}").read()

    except Exception:
        pass

    page2 = page_data2.decode('utf-8')

    start = page2.find(coin_symbol_to)
    end  = page2.find(',', start, len(page2))

    pricedata2 = page2[start:end]
    pricedata2 = pricedata2.replace(":", '')
    pricedata2 = pricedata2.replace(coin_symbol_to, '')
    pricedata2 = pricedata2.replace('"', '')

    return float(pricedata2)
"""

def fetch_price_of_and_convert_to(coin_symbol_base, coin_symbol_to: str) -> float:
    #https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    import ssl

    context = ssl._create_unverified_context()

    # A MUCH better API to fetch token price
    page_data2 = urlopen(
        f"https://min-api.cryptocompare.com/data/price?fsym={coin_symbol_base}&tsyms={coin_symbol_to}",
        context=context
    ).read()

    page2 = page_data2.decode('utf-8')
    page2 = page2.replace('{"USDT":', '')
    page2 = page2[:len(page2) - 1]

    if 'Response' in page2:
        return 0.0

    return float(page2)

# TODO: Group these into a class
class recover_acc(tk.Toplevel):
    def __init__(self = Toplevel):
        super().__init__()

        window.withdraw()

        self.title("SimpleEtherWallet  -  Recover account")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", quit)

        is_new["state"] = False

        if os.name == 'nt':
            center_window(560, 420, self)

        else:
            center_window(620, 420, self)

        wframe = LabelFrame(
            master = self,
            bd = 4
        )

        newline(self, pady = 0)

        global image_again

        image_again = PhotoImage(file = imgfolder + 'eth.png')

        tk.Label(
            master = self,
            text = "Recover your account ",
            image = image_again,
            compound = 'right',
            font = "bold 18"
        ).pack(
            pady = 20,
            anchor = "center"
        )

        tk.Label(
            master = wframe,
            text = "Your private key holds access to your crypto assets.\nKeep this key as safe as possible",
            font = 'bold 14'
        ).pack(pady = 10)

        tk.Label(
            master = wframe,
            text = "Enter your private key: ",
            font = "bold 12"
        ).pack(
            pady = 5,
            anchor = "center"
        )

        pentry = StringVar()

        private_key_recover = tk.Entry(
            master  = wframe,
            font = 'bold 10',
            width = 64,
            textvariable = pentry
        )

        def ch(event):
            pentry.set(pentry.get()[:66])

        private_key_recover.bind("<KeyRelease>", ch)

        private_key_recover.pack(
            padx = 30,
            pady = 20,
            ipady = 5
        )

        wframe.pack(
            padx = 10,
            pady = 10
        )

        def continue_or_not(*args):
            if len(private_key_recover.get()) < 48:
                messagebox.showerror(
                    title = "Error",
                    message = "Invalid private key",
                    icon = "error",
                )

                private_key_recover.delete(0, tk.END)
                return


            elif len(private_key_recover.get()) == 0:
                messagebox.showerror(
                    title = "Error",
                    message = "Private key cannot be empty",
                    icon = "error",
                )

                private_key_recover.delete(0, tk.END)
                return

            try:
                w3.eth.default_account = Account.from_key(private_key_recover.get())

                globals()['recovered'] = 1

                createfile()

                self.destroy()
                #window.destroy()

            except Exception:
                messagebox.showerror(
                    title = "Error",
                    message = "Invalid private key",
                    icon = "error",
                )

                private_key_recover.delete(0, tk.END)
                return

        frame2 = tk.Frame(master = self)

        btn =  tk.Button(
            master = frame2,
            text = "Continue",
            font = 'bold 14',
            command = continue_or_not
        )

        private_key_recover.bind("<Return>", continue_or_not)

        btn2 = tk.Button(
            master = frame2,
            text = 'Return',
            font = 'bold 14',
            command = lambda: \
            [
                self.destroy(),
                window.deiconify()
            ]
        )

        btn3 = tk.Button(
            master= frame2,
            text = 'Quit',
            font = 'bold 14',
            command = quit
        )

        btn3.pack(
            ipady = 7,
            ipadx = 7,
            padx = 40,
            side = 'left',
            anchor = 's'
        )

        btn2.pack(
            anchor = 's',
            side = "left",
            padx = 7,
            ipady = 7,
            ipadx = 7,
        )

        btn.pack(
            anchor = "s",
            ipady = 7,
            ipadx = 7,
        )

        frame2.pack(pady = 10)

# Enter password dialog
class passbox(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("SimpleEtherWallet")
        self.protocol("WM_DELETE_WINDOW", quit)
        self.resizable(False, False)

        window.withdraw()

        if is_new["state"] == False:
            center_window(580, 240, self)

        else:
            if os.name != 'nt':
                center_window(680, 480, self)

            else:
                center_window(540, 480, self)

        global someimg

        someimg   = PhotoImage(file = imgfolder + 'eth.png')

        global closed_eyes
        global opened_eyes

        closed_eyes = imgfolder + 'icons8-eyes-24-closed.png'
        opened_eyes = imgfolder + 'icons8-eyes-24.png'

        global showpass
        global hidepass

        hidepass = PhotoImage(file = closed_eyes)
        showpass = PhotoImage(file = opened_eyes)

        opt1 = IntVar()
        opt1.set(1)

        opt2 = IntVar()
        opt2.set(1)

        # BEGIN def unhide1() and unhide2() function
        def unhide1():
            if opt1.get() == 1:
                btn1.config(image = showpass)
                passentry.config(show = "")

                opt1.set(0)

            elif opt1.get() == 0:
                btn1.config(image = hidepass)
                passentry.config(show = "*")

                opt1.set(1)

        if is_new['state'] == True:
            def unhide2():
                if opt2.get() == 1:
                    btn2.config(image = showpass)
                    passentry2.config(show = "")

                    opt2.set(0)

                elif opt2.get() == 0:
                    btn2.config(image = hidepass)
                    passentry2.config(show = "*")

                    opt2.set(1)
        # END

        l = tk.Label(master = self)

        l.pack(
            padx = 15,
            pady = 22
        )

        if is_new["state"] == True:
            smallframe = tk.LabelFrame(
                master = self,
                bd = 4
            )

            l.config(
                text = "Create Wallet ",
                font = "bold 16",
                image = someimg,
                compound = RIGHT
            )

            tk.Label(
                master = smallframe,
                text = """This password is used to encrypt your wallet.\n
 The password does not leave your device.\n
 If you forget your password, you can only recover \nyour wallet with your Private Key.""",
                font = 'bold 12'
                ).pack(
                    fill = tk.Y,
                    expand = True
                )

            smallframe.pack(
            padx = 20,
            fill = tk.BOTH,
            expand = True
        )

        else:
            wname = ''

            if '\\' in nameofwallet['name']:
                self.start = nameofwallet['name'].rfind('\\') + 1
                self.end  = len(nameofwallet['name'])

                wname = nameofwallet['name'][self.start:self.end]

            else:
                self.start = nameofwallet['name'].rfind('/') + 1
                self.end  = len(nameofwallet['name'])

                wname = nameofwallet['name'][self.start:self.end]

            l.config(
                #image = someimg,
                text =  wname,
                font = 'bold 16'
             )

        if is_new["state"] == False:
            mframe = tk.LabelFrame(
                master = self,
                bd = 3
            )

        else:
            mframe = tk.Frame(master = self)

        btn1 = tk.Button(
            mframe,
            image = hidepass,
            command = unhide1
        )

        passentry = tk.Entry(
            mframe,
            bd = 2,
            highlightthickness = 1,
            exportselection = 0,
            width = 40,
            show = "*"
        )

        btn1.pack(
            side = "right",
            padx = 10,
        )

        tk.Label(
            master = mframe,
            text = "Enter your password:",
            font = 'bold 13'
        ).pack(side = 'left')

        passentry.pack(
            ipady = 5,
            side = 'right'
        )

        if is_new["state"] == True:
            mframe2 = tk.Frame(master = self)

            passentry2  = tk.Entry(
                master = mframe2,
                bd = 2,
                exportselection = 0,
                highlightthickness = 1,
                width = 40,
                show = "*"
            )


            btn2 = tk.Button(
                mframe2,
                image = hidepass,
                command = unhide2
            )

            btn2.pack(
                side = "right",
                padx = 10
            )

            if os.name != 'nt':
                tk.Label(
                    master = mframe2,
                    text = "Repeat the password:",
                    font = 'bold 13'
                ).pack(side = 'left')

            # The second entry field on
            #  Windows is off by 1 space

            else:
                tk.Label(
                        master = mframe2,
                        text = "Repeat the password: ",
                        font = 'bold 13'
                    ).pack(side = 'left')

            passentry2.pack(
                side = 'bottom',
                ipady = 5
            )

        mframe.pack(
            pady = 10,
            padx = 20
        )

        if is_new["state"] == True:
            mframe2.pack(
                pady = 2,
                anchor = 's',
                padx = 20
            )

        newline(mframe)

        def issame(*args):
            if is_new["state"] == True:
                if passentry.get() != passentry2.get():
                    messagebox.showerror(
                        title = "Error",
                        message = "Passwords did not match",
                        icon = "error",
                    )

                    passentry.delete(0, tk.END)
                    passentry2.delete(0, tk.END)
                    return

                elif len(passentry.get()) == 0 and len(passentry2.get()) == 0:
                    messagebox.showerror(
                        title = "Error",
                        message = "Password field is empty",
                        icon = "error",
                    )

                    passentry.delete(0, tk.END)
                    passentry2.delete(0, tk.END)
                    return

            else:
                if len(passentry.get()) == 0:
                    messagebox.showerror(
                        title = "Error",
                        message = "Password field is empty",
                        icon = "error",
                    )

                    passentry.delete(0, tk.END)
                    return

            if is_new["state"] == True:
                if recovered == 0:
                    w3.eth.default_account = Account.create()

                encrypted = Account.encrypt(
                    w3.eth.default_account.key,
                    password = passentry.get()
                )

                with open(conf_file, 'w') as ff:
                    conf_file_contents.update({"last": f"{nameofwallet['name']}"})

                    if not nameofwallet['name'] in conf_file_contents['wallets']:
                        conf_file_contents['wallets'].append(nameofwallet['name'])

                    json.dump(conf_file_contents, ff)

                    with open(nameofwallet["name"], "w") as f:
                        f.write(json.dumps(encrypted))

            else:
                if recovered == 1:
                    encrypted = Account.encrypt(
                        w3.eth.default_account.key,
                        password = passentry.get()
                    )

                    with open(conf_file, 'w') as ff:
                        conf_file_contents.update({"last": f"{nameofwallet['name']}"})

                        if not nameofwallet['name'] in conf_file_contents['wallets']:
                            conf_file_contents['wallets'].append(nameofwallet['name'])

                        json.dump(conf_file_contents, ff)

                        with open(nameofwallet["name"], "w") as f:
                            f.write(json.dumps(encrypted))

                if recovered == 0:
                    try:
                        with open(nameofwallet["name"], "r") as f:
                            w3.eth.default_account = Account.from_key(
                                Account.decrypt(
                                    json.load(f),
                                    password = passentry.get()
                                )
                            )

                            with open(conf_file, 'w') as ff:
                                conf_file_contents.update({"last": f"{nameofwallet['name']}"})

                                if not nameofwallet['name'] in conf_file_contents['wallets']:
                                    conf_file_contents['wallets'].append(nameofwallet['name'])

                                json.dump(conf_file_contents, ff)

                    except ValueError:
                        messagebox.showerror(
                            title = "Error",
                            message = "Incorrect password. Try again"
                        )

                        passentry.delete(0, tk.END)
                        return

            self.destroy()
            window.destroy()

        endframe = tk.Frame(master = self)

        tk.Button(
            master = endframe,
            text = "Quit",
            font = 'bold 12',
            command = quit
        ).pack(
            side = 'left',
            padx = 10,
            ipady = 7,
            ipadx = 5
        )

        tk.Button(
            master = endframe,
            text = 'Return',
            font = 'bold 12',
            command = lambda: \
            [
                openwalletwindow().deiconify(),
                self.destroy()
            ]
        ).pack(
            side = "left",
            padx = 10,
            ipady = 7,
            ipadx = 5
        )

        tk.Button(
            master = endframe,
            text = "Continue",
            font = 'bold 12',
            command = issame
        ).pack(
            ipady = 7,
            ipadx = 5
        )

        endframe.pack(pady = 20)

# create wallet
def createfile(*args):
    position["pos"] = 1
    is_new["state"] = True

    class filediag(tk.Toplevel):
        def __init__(self = tk.Toplevel):
            super().__init__()

            window.withdraw()
            #window.unbind( '<Lock-KeyRelease>')
            #window.unbind( '<Lock-KeyPress>')

            self.title("SimpleEtherWallet")
            self.protocol("WM_DELETE_WINDOW", quit)
            self.resizable(False, False)

            center_window(560,  500, self)

            framebox = tk.LabelFrame(
                master = self,
                bd = 5
            )

            tk.Label(
                master = self,
                text = "Create Wallet\n\nYour wallet is non-custodial,\n meaning that it is stored on your device",
                font = "bold 16",
            ).pack(pady = 20)

            tk.Label(
                master = framebox,
                text = "Enter desired wallet name: ",
                font = 'bold 14'
            ).pack(pady = 16)

            framebox.pack(
                pady = 10,
                padx = 5
            )

            frame = tk.Frame(master = self)

            tk.Label(
                master = framebox,
                text = "Wallet name:",
                font = 'bold 13'
            ).pack(
                pady = 10,
                padx = 10,
                side = "left"
            )

            enter = tk.Entry(
                master = framebox,
                width = 40,
                font = 'bold 10'
            )

            # file chooser
            def createf(*args):
                saveas = asksaveasfilename(
                    initialdir = dest_path,
                    title = "Create Wallet",
                    defaultextension = ".sew"
                )

                if not saveas:
                    return

                nameofwallet["name"] = saveas

                passbox()
                self.destroy()

            btn1 = tk.Button(
                master = framebox,
                text = "Pick location",
                font = 'bold 12',
                command = createf
            )

            btn1.bind("<Return>", createf)

            btn1.pack(
                padx = 20,
                side = "right",
                ipady = 2
            )

            def errbox(msg):
                enter.delete(0, tk.END)
                messagebox.showerror(
                    title = "Error",
                    message = msg,
                    icon = "error",
                )

            # create file
            def create(*args):
                fname = enter.get()

                # empty entry field
                if len(fname) == 0:
                    errbox("Name cannot be empty")
                    return

                # name too long
                elif len(fname) > 254:
                    errbox("Wallet name cannot be longer than 255 characters")
                    return

                elif not fname.startswith("C:\\") or not fname.startswith("C:/"):
                    tmp = dest_path + fname
                    fname = tmp

                # if directory
                if os.path.isdir(fname):
                    errbox("'" + fname + "' is a directory")
                    return

                if fname.find('.sew') != -1:
                    nameofwallet["name"] = fname

                nameofwallet["name"] = fname + ".sew"

                passbox()
                self.destroy()

            def select(event):
                enter.select_range(start = 0, end = tk.END)

            enter.bind("<Return>", create)
            enter.bind("<Up>", select)

            enter.pack(
                fill = tk.X,
                expand = True,
                ipady = 5,
                side = "right"
            )

            newline(framebox, pady = 20)

            capslockstat = tk.Label(
                master = self,
                text = '',
                font = '8',
                fg = 'red'
            )

            def oncaps2(event):
                capslockstat.config(text = 'Caps lock is on!')

            def offcaps2(event):
                capslockstat.config(text = '')

            self.bind( '<Lock-KeyRelease>', oncaps2)
            self.bind( '<Lock-KeyPress>',     offcaps2)

            capslockstat.pack(
                side = 'top',
                pady = 4
            )

            tk.Label(
                master = self,
                text = f"NOTE: If a path hasn't been specified, \nthe wallet will be saved to: {dest_path}",
                font = 'bold 12'
            ).pack(pady = 10)

            frame2 = tk.Frame(master = self)

            tk.Button(
                master = frame2,
                text = "Continue",
                font = 'bold 14',
                command = create
            ).pack(
                padx = 5,
                ipady = 7,
                ipadx = 5,
                side = "right"
            )

            tk.Button(
                master = frame2,
                text = "Return",
                font = 'bold 14',
                command  = lambda: [
                    self.destroy(),
                    #window.bind( '<Lock-KeyRelease>', oncaps),
                    #window.bind( '<Lock-KeyPress>', offcaps),
                    window.deiconify()
                ]
            ).pack(
                side = 'right',
                ipady = 7,
                ipadx = 5
            )

            tk.Button(
                master = frame2,
                text = "Quit",
                font = 'bold 14',
                command = quit
            ).pack(
                ipady = 7,
                ipadx = 8,
                padx = 20,
                side = "left"
            )

            tk.Label(
                master = frame2,
                text = ""
            ).pack(
                padx = 20,
            )

            frame2.pack(
                pady = 20,
                padx = 10,
                anchor = 'center'
            )

    filediag()

# open file
def openfile():
    openf = askopenfilename(
        initialdir = dest_path,
        title = "Open Wallet",
        defaultextension = ".sew"
    )

    if not openf:
        importwalletwindow().deiconify()
        return

    nameofwallet["name"] = openf

    filechosen['state'] = 1
    is_new['state'] = False

    passbox()

class openwalletwindow(tk.Toplevel):
    def __init__(self = Toplevel):
        def errbox(msg):
            entry.delete(0, tk.END)
            messagebox.showerror(
                title = "Error",
                message = msg,
                icon = "error",
            )

        def selecttxt(event):
            entry.select_range(start = 0, end = tk.END)
            entry.select_adjust(index = 0)

        # open existing wallet (manual)
        def openwallet(*args):
            fname = entry.get()

            # empty entry field
            if len(fname) == 0:
                errbox("Name cannot be empty")
                return

            # name too long
            elif len(fname) > 254:
                errbox("Wallet name cannot be longer than 255 characters")
                return

            # if directory
            if os.path.isdir(fname):
                errbox(f"{fname} is a directory")
                return

            if fname.startswith("C:/") or fname.startswith("C:\\"):
                if ".sew" in fname:
                    if not os.path.exists(fname):
                        errbox("Wallet not found")
                        return

                else:
                    if not os.path.exists(fname + ".sew"):
                        errbox("Wallet not found")
                        return


            elif not fname.startswith("C:/") or fname.startswith("C:\\"):
                tmp = dest_path + fname
                fname = tmp

                if ".sew" in fname:
                    if not os.path.exists(fname):
                        errbox("Wallet not found")
                        return

                else:
                    if not os.path.exists(fname + ".sew"):
                        errbox("Wallet not found")
                        return

            if not ".sew" in fname:
                nameofwallet["name"] = fname + ".sew"

            else:
                nameofwallet["name"] = fname

            entry.delete(0, tk.END)

            self.withdraw()

            pbox = passbox()
            pbox.mainloop()

        super().__init__()

        self.title("SimpleEtherWallet")
        self.protocol("WM_DELETE_WINDOW", quit)
        self.resizable(False, False)

        window.withdraw()

        center_window(550, 350, self)

        #img = PhotoImage(file = imgfolder + 'eth.png')

        global yetanotherimg

        yetanotherimg = PhotoImage(file = imgfolder + 'eth.png')

        tk.Label(
            master = self,
            text = 'Welcome! ',
            font = 'bold 22',
            image = yetanotherimg,
            compound = 'right'
        ).pack(pady = 26)

        frame1 = tk.LabelFrame(
            master = self,
            bd = 5
        )

        tk.Label(
            master = frame1,
            text = "Enter your wallet's name or click choose to select wallet\n",
            font = '12'
        ).pack(
            padx = 10,
            pady = 15
        )

        frame1.pack(
            fill = tk.BOTH,
            padx = 14
        )

        frame2 = tk.Frame(master = frame1)

        tk.Button(
            master = frame2,
            text = "Choose...",
            font = 'bold 12',
            width = 10,
            command = lambda: [
                openfile(),
                self.withdraw()
            ]
        ).pack(
            padx = 8,
            side = 'right',
            ipady = 4
        )

        tk.Label(
            master = frame2,
            text = "Wallet:",
            font = 'bold 12'
        ).pack(
            side = 'left'
        )

        entry = tk.Entry(
            frame2,
            width = 45,
            font = 'bold 12'
        )

        entry.bind("<Up>", selecttxt)
        entry.bind("<Return>", openwallet)

        entry.pack(side = 'right', ipady = 5)

        frame2.pack(anchor = 'center')

        is_new["state"] = False;

        frame4 = tk.Frame(frame1)
        capslockstatus = tk.Label(master = frame4)

        tk.Button(
            master = frame4,
            text = "Quit",
            font = 'bold 12',
            width = 5,
            command = quit
        ).pack(
            padx = 10,
            ipady = 7,
            ipadx = 5,
            side = 'left'
        )

        tk.Button(
            master = frame4,
            text = 'Continue',
            font = 'bold 12',
            width = 8,
            command = openwallet
        ).pack(
            padx = 3,
            ipady = 7,
            ipadx = 5,
            side = 'right'
        )

        tk.Button(
            master = frame4,
            text = 'Return',
            font = 'bold 12',
            width = 7,
            command = lambda: \
            [
                window.deiconify(),
                self.destroy()
            ]
        ).pack(
            side = 'right',
            padx = 3,
            ipady = 7,
            ipadx = 5
        )

        def oncaps(event):
            capslockstatus.config(
                text = 'Caps lock is on!',
                fg = 'red',
                font = 'bold 14'
            )

        def offcaps(event):
            capslockstatus.config(text = '')

        self.bind( '<Lock-KeyRelease>', oncaps)
        self.bind( '<Lock-KeyPress>',     offcaps)

        frame1.bind( '<Lock-KeyRelease>', oncaps)
        frame1.bind( '<Lock-KeyPress>',     offcaps)

        capslockstatus.pack(
            pady = 4,
            padx = 4
        )

        tk.Label(
            master = frame1,
            text = ''
        ).pack(ipady = 2)

        frame4.pack(pady = 18)

class importwalletwindow(tk.Toplevel):
    def __init__(self = Toplevel):
        super().__init__()

        self.title("SimpleEtherWallet  -  Import wallet")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", quit)

        window.withdraw()

        if os.name == 'nt':
            center_window(468, 440, self)

        else:
            center_window(500, 440, self)

        newline(self)

        tk.Label(
            master = self,
            text = 'Select how you want to import your wallet:\n',
            font = 'bold 14'
        ).pack(pady = 10)

        if os.name == 'nt':
            frm = tk.LabelFrame(
                master = self,
                bd = 13
            )

        else:
            frm = tk.LabelFrame(
                master = self,
                bd = 9,
                #bg = '#c0c0c0'
            )


        radiobtnopt = IntVar()

        def getradioopt():
            if  radiobtnopt.get() == 1:
                recover_acc()
                self.destroy()

            elif radiobtnopt.get() == 2:
                openfile()

            else:
                pass

        optsforRadiobtn = {
            'master': frm,
            'font': 'bold 14',
            'variable': radiobtnopt,
            'height': 4,
            'relief': 'raised',
            #'command': getradioopt
        }

        opt1 = tk.Radiobutton(
            **optsforRadiobtn,
            text = 'Import from Private Key',
            value = 1,
            cursor = 'cross'
        )

        opt1.pack(
            expand = True,
            fill = tk.X,
            pady = 2
        )

        opt2 = tk.Radiobutton(
            **optsforRadiobtn,
            text = 'Import from a file (only supports .sew files)',
            value = 2,
            cursor = 'cross'
        )

        opt2.pack(
            expand = True,
            fill = tk.X,
            pady = 2
        )

        frm.pack(
            padx = 10,
            fill = tk.X,
            expand = True
        )

        importbtnframe = tk.Frame(master = self)

        importbtnquit = tk.Button(
            master = importbtnframe,
            text = 'Quit',
            font = 'bold 12',
            command = quit
        )

        importbtnquit.pack(
            side = 'left',
            ipady = 3
        )

        tk.Label(
            master = importbtnframe,
            text = ''
        ).pack(
            padx = 10,
            side = 'left'
        )

        importbtnret = tk.Button(
            master = importbtnframe,
            text = 'Return',
            font = 'bold 12',
            command = lambda: [
                window.deiconify(),
                self.destroy()
            ]
        )

        importbtnret.pack(
            ipady = 3,
            side = 'left'
        )

        importbtncont = tk.Button(
            master = importbtnframe,
            text = 'Continue',
            font = 'bold 12',
            command = lambda: [
                self.withdraw(),
                getradioopt()
            ]
        )

        importbtncont.pack(
            ipady = 3,
            side = 'right',
            padx = 12
        )

        importbtnframe.pack(pady = 20)

        newline(self, pady = 1)



## @@FIRST SCREEN@@ ##
window = Tk()
window.title("SimpleEtherWallet")
window.protocol("WM_DELETE_WINDOW", quit)
window.resizable(False, False)

# Greeting window
with open(conf_file, 'r') as f:
    if os.name == 'nt':
        window.lift()

    contents = json.load(f)

    if len(contents['wallets']) != 0:
        if os.name == 'nt':
            center_window(720, 400, window)

        else:
            center_window(880, 400, window)

        ethimgload = ''
        ethimgload = imgfolder + 'eth.png'
        ethimg        = PhotoImage(file = ethimgload)

        newline(window, pady = 0)

        tk.Label(
            master = window,
            text = "Welcome back! Please select a wallet ",
            font = "bold 20",
            image = ethimg,
            compound = RIGHT
        ).pack(pady = 10)

        masterframe = tk.LabelFrame(
            master = window,
            bd = 4
        )

        masterframe.pack(
            padx = 40,
            fill = tk.BOTH,
            expand = True,
            pady = 30
        )

        wlist = []

        wlist = contents['wallets']

        wnames = []

        for i in range(0, len(wlist)):
            name = wlist[i]

            if '\\' in name:
                start = name.rfind('\\') + 1
                end  = len(name)

                wnames.append(name[start:end])

            else:
                start = name.rfind('/') + 1
                end  = len(name)

                wnames.append(name[start:end])

        wlist = wnames

        wbox = ttk.Combobox(
            master = masterframe,
            state = 'readonly',
            values = wlist,
            width = 30,
        )

        wbox.pack(
            padx = 19,
            ipady = 5,
            pady = 20
            #side = 'left'
        )

        selectedwallet = StringVar()

        def getboxopt(event):
            selectedwallet.set(contents['wallets'][wbox.current()])


        wbox.current(0)
        selectedwallet.set(contents['wallets'][0])

        wbox.bind("<<ComboboxSelected>>", getboxopt)

        passwdframe = tk.Frame(master = masterframe)

        btn1 = tk.Button(passwdframe)

        passentry = tk.Entry(
            passwdframe,
            bd = 3,
            highlightthickness = 1,
            exportselection = 0,
            width = 50,
            show = "*",
        )

        stat = IntVar()
        stat.set(1)

        global closed_eyes
        global opened_eyes

        closed_eyes  = imgfolder + 'icons8-eyes-24-closed.png'
        opened_eyes = imgfolder + 'icons8-eyes-24.png'

        global showpass
        global hidepass

        hidepass = PhotoImage(file = closed_eyes)
        showpass = PhotoImage(file = opened_eyes)

        def unhide():
            if stat.get() == 1:
                btn1.config(image = showpass)
                passentry.config(show = "")

                stat.set(0)

            elif stat.get() == 0:
                btn1.config(image = hidepass)
                passentry.config(show = "*")

                stat.set(1)

        btn1.configure(
            image = hidepass,
            command = unhide
        )

        tk.Label(
            master = passwdframe,
            text = "Password:",
            font = 'bold 12'
        ).pack(
            side = 'left',
            padx = 2,
        )

        btn1.pack(
            side =  'right',
            padx = 2
        )

        passentry.pack(
            ipady = 5,
            #fill = tk.X,
            #expand = True,
            padx = 10,
            side = 'right',
            pady = 4
        )

        passwdframe.pack(
            pady = 5,
        )

        capslockstat = tk.Label(
            master = masterframe,
            text = '',
            font = 'bold 13',
            fg = 'red'
        )

        def oncaps2(event):
            capslockstat.config(text = 'Caps lock is on!')

            if len(passentry.get()) == 0:
                capslockstat.config(text = '')

        def offcaps2(event):
            capslockstat.config(text = '')

        window.bind( '<Lock-KeyRelease>', oncaps2)
        window.bind( '<Lock-KeyPress>',     offcaps2)

        capslockstat.pack(pady = 4)

        def checkpasswd(*args):
            if len(passentry.get()) == 0:
                messagebox.showerror(
                    title = "Error",
                    message = "Password field is empty"
                )

                return

            try:
                with open(selectedwallet.get(), 'r') as ff:

                    w3.eth.default_account = Account.from_key(
                        Account.decrypt(
                            json.load(ff),
                            password = passentry.get()
                        )
                    )

            except ValueError:
                messagebox.showerror(
                    title = "Error",
                    message = "Incorrect password. Try again"
                )

                passentry.delete(0, tk.END)
                return

            window.destroy()

        passentry.bind('<Return>', lambda e: checkpasswd(e))

        btnframe = tk.Frame(master = masterframe)

        btnquit = tk.Button(
            master = btnframe,
            text = 'Quit',
            font = 'bold 12',
            command = quit
        )

        btnquit.pack(
            ipady = 2,
            ipadx = 16,
            padx = 20,
            side = 'left'
        )

        btncontinue = tk.Button(
            master = btnframe,
            text = 'Continue',
            font = 'bold 12',
            bd = 4,
            command = checkpasswd
        )

        btncontinue.pack(
            side = 'right',
            ipadx = 10,
            ipady = 3,
            padx = 10
        )

        def createawallet():
            createfile()

        btncreatewallet = tk.Button(
            master = btnframe,
            text = 'Create a wallet',
            font = 'bold 12',
            command = createawallet
        )

        btncreatewallet.pack(
            ipady = 3,
            ipadx = 10,
            side = 'left'
        )

        btnrecwallet = tk.Button(
            master = btnframe,
            text = 'Recover wallet',
            font = 'bold 12',
            command = recover_acc
        )

        btnrecwallet.pack(
            ipady = 3,
            ipadx = 10,
            side = 'left',
            padx = 4
        )

        btnframe.pack(
            side = 'top',
            pady = 10
        )

        def openawallet():
            openwalletwindow()

        btnselwallet = tk.Button(
            master = btnframe,
            text = 'Open a wallet',
            font = 'bold 12',
            command = openawallet
        )

        btnselwallet.pack(
            ipady = 3,
            ipadx = 10,
            side = 'left',
            padx = 4
        )

    else:
        if os.name == 'nt':
            center_window(540, 520, window)

        else:
            center_window(540, 600, window)

        tk.Label(
            master = window,
            text = "Welcome! ",
            font = "bold 20",
            #image = img,
            compound = RIGHT
        ).pack(pady = 10)

        smallframe = tk.LabelFrame(
            master = window,
            bd = 8
        )

        smallframe.pack(
            pady = 12,
            padx = 5
        )

        txt = tk.Label(
            master = smallframe,
            text = """
SimpleEtherWallet is a non-custodial wallet on the Ethereum blockchain. You own your crypto assets!\n
Your private key never leaves this device. \nYour private key is encrypted.\n""",
            font = "bold 13",
            wraplength = 400,
            justify = 'center'
        )

        txt.pack(
            padx = 40,
            pady = 14
        )

        optframe = LabelFrame(
            master = window,
            bd = 2
        )

        tk.Button(
            master = optframe,
            text = 'Create a wallet',
            font = 'bold 16',
            height = 3,
            command = createfile
        ).pack(
            fill = tk.BOTH,
            padx = 2,
            pady = 2
        )

        tk.Button(
            master = optframe,
            text = 'Open a wallet',
            font = 'bold 16',
            height = 3,
            command = openwalletwindow
        ).pack(
            fill = tk.BOTH,
            padx = 2,
            pady = 2,
        )

        tk.Button(
            master = optframe,
            text = 'Import a wallet',
            font = 'bold 16',
            height = 3,
            command = importwalletwindow
        ).pack(
            fill = tk.BOTH,
            padx = 2,
            pady = 2,
        )

        optframe.pack(
            fill = tk.BOTH,
            padx = 10
        )

window.mainloop()

##@@ init main @@##
main = tk.Tk()
main.resizable(False, False)
main.title("SimpleEtherWallet")
main.protocol("WM_DELETE_WINDOW", quit)

if os.name == 'nt':
    center_window(700, 600, main)


aboutbar = tk.Menu(master = main)

aboutbar_opts = tk.Menu(
    master = aboutbar,
    tearoff = 0
)


# TODO: Group these into a class
# Images
class ImageLinks(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title("SimpleEtherWallet  -  Images")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        center_window(600, 580, self)

        tk.Label(
            master = self,
            text = '\nImages',
            font = 'bold 14'
        ).pack(pady = 20)

        self.frm = tk.Frame(master = self)
        self.frm.pack(
            padx = 20,
            pady = 7
        )

        self.textbox = tk.Text(
            master = self.frm,
            font = 'Serif 12',
            wrap = WORD,
            height = 20
        )

        self.textbox.insert(
            tk.END,
            "Copy icon by Icons8: https://icons8.com/icon/86236/copy\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Cross icon by Icons8: https://icons8.com/icon/42223/cancel\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Plus icon by Icons8: https://icons8.com/icon/42232/plus\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Eye icon by Icons8: https://icons8.com/icon/7tg2iJatDNzj/eyes\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Eye with line icon by Icons8: https://icons8.com/icon/oZFC4NAoTr5c/eyes\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Open book icon by Icons8: https://icons8.com/icon/tgZbSpOhzqyY/open-book\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Forward arrow icon by Icons8: https://icons8.com/icon/117017/forward-arrow\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Back arrow book icon by Icons8: https://icons8.com/icon/117018/reply-arrow\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Refresh icon by Icons8: https://icons8.com/icon/42259/refresh\n\n"
        )

        self.textbox.insert(
            tk.END,
            "Wallet icon by Icons8: https://icons8.com/icon/42316/wallet\n"
        )

        self.textbox.pack(pady = 8)

        tk.Button(
            master = self,
            text = 'Close',
            font = 'bold 16',
            command = self.destroy
        ).pack(
            pady = 2,
            ipadx = 14
        )

        self.textbox.configure(state = 'disabled')

# License class
class License(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title("SimpleEtherWallet  -  Credits")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        center_window(600, 620, self)

        tk.Label(
            master = self,
            text = '\nLicense',
            font = 'bold 14'
        ).pack(pady = 20)

        self.frm = tk.Frame(master = self)
        self.frm.pack(
            padx = 20,
            pady = 7
        )

        self.textbox = tk.Text(
            master = self.frm,
            font = 'Serif 12',
            wrap = WORD,
        )

        with open(
            os.path.dirname(__file__) + '/LICENSE.txt', 'r', encoding = 'utf-8') as f:
            self.text = f.read()

            self.textbox.insert(
                tk.END,
                self.text
            )

        self.textbox.pack(pady = 8)

        tk.Button(
            master = self,
            text = 'Close',
            font = 'bold 16',
            command = self.destroy
        ).pack(
            pady = 2,
            ipadx = 14
        )

        self.textbox.configure(state = 'disabled')

# About wallet
class AboutWallet(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title("SimpleEtherWallet  -  About")
        self.protocol("WM_DELETE_WINDOW", quit)

        center_window(600, 720, self)

        tk.Label(
            master = self,
            text = '\nWhat the heck is SimpleEtherWallet?',
            font = 'bold 14'
        ).pack(pady = 20)

        self.frm = tk.Frame(master = self)
        self.frm.pack(
            padx = 20,
            pady = 7
        )

        self.textbox = tk.Text(
            master = self.frm,
            font = 'Serif 12',
            wrap = WORD,
            height = 30
        )

        with open(
            os.path.dirname(__file__) + '/README.md', 'r', encoding = 'utf-8') as f:
            self.text = f.read()

            self.textbox.insert(
                tk.END,
                self.text
            )

        self.textbox.pack(pady = 8)

        tk.Button(
            master = self,
            text = 'Close',
            font = 'bold 16',
            command = self.destroy
        ).pack(
            pady = 2,
            ipadx = 14
        )

        self.textbox.configure(state = 'disabled')

# Show recovery key
class ShowRecoveryKey(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title("SimpleEtherWallet  -  Recovery Key")
        self.protocol("WM_DELETE_WINDOW", quit)

        center_window(600, 230, self)

        tk.Label(
            master = self,
            text = '\nPassword required to view your private key',
            font = 'bold 12'
        ).pack(pady = 20)

        passwdframe = tk.Frame(master = self)
        passwdframe.pack()

        btn1 = tk.Button(passwdframe)

        btn1.pack(
            side =  'right',
            padx = 2
        )

        self.passentry = tk.Entry(
            passwdframe,
            bd = 3,
            highlightthickness = 1,
            exportselection = 0,
            width = 50,
            show = "*",
        )

        stat = IntVar()
        stat.set(1)

        global closed_eyes
        global opened_eyes

        closed_eyes  = imgfolder + 'icons8-eyes-24-closed.png'
        opened_eyes = imgfolder + 'icons8-eyes-24.png'

        global showpass
        global hidepass

        hidepass   = PhotoImage(file = closed_eyes)
        showpass = PhotoImage(file = opened_eyes)

        def unhide():
            if stat.get() == 1:
                btn1.config(image = showpass)
                self.passentry.config(show = "")

                stat.set(0)

            elif stat.get() == 0:
                btn1.config(image = hidepass)
                self.passentry.config(show = "*")

                stat.set(1)

        btn1.configure(
            image = hidepass,
            command = unhide
        )

        tk.Label(
            master = passwdframe,
            text = "Password:",
            font = 'bold 12'
        ).pack(
            side = 'left',
            padx = 2,
        )

        self.passentry.pack(
            ipady = 5,
            #fill = tk.X,
            #expand = True,
            padx = 10,
            side = 'right',
            pady = 4
        )

        passwdframe.pack(
            pady = 5,
        )

        class DisplayPrivateKey(tk.Toplevel):
            def __init__(self):
                super().__init__()

                self.resizable(False, False)
                self.title("SimpleEtherWallet  -  Recovery Key")

                def rm_p():
                    try:
                        os.remove("p.png")

                    except Exception:
                        return

                    return

                self.protocol(
                    "WM_DELETE_WINDOW",
                    lambda: \
                    [
                        rm_p(),
                        self.destroy()
                    ]
                )

                if os.name == 'nt':
                    center_window(620, 570, self)

                else:
                    center_window(700, 570, self)

                tk.Label(
                    master = self,
                    text = '\nKeep your private key safe!',
                    font = 'bold 22'
                ).pack(pady = 10)

                qrcode = segno.make_qr(w3.to_hex(account.key))
                qrcode.save(
                    "p.png",
                    scale = 8,
                    border = 1
                )

                self.f_img = type(PhotoImage)
                self.f_img =  PhotoImage(file = "p.png")

                tk.Label(
                    master = self,
                    image = self.f_img,
                    relief = 'groove',
                    bd = 4
                ).pack(pady = 10)

                self.pkey = StringVar()

                self.t = tk.Entry(
                    master = self,
                    exportselection = False,
                    highlightthickness = 0,
                    font = 'bold 12',
                    relief = 'flat',
                    width = 64,
                    textvariable = self.pkey
                )

                self.pkey.set(w3.to_hex(account.key))
                self.t.pack(
                    pady = 20,
                    ipady = 4,
                    padx = 4
                )

                self.t.configure(state = 'readonly')

                global clipboardimg

                self.clipboardimg = PhotoImage(file = imgfolder + 'icons8-copy-24.png')

                tk.Label(
                    master = self,
                    text = '',
                ).pack(
                    side = 'left',
                    ipadx = 50
                )

                tk.Button(
                    master = self,
                    text = 'Close',
                    font = 'bold 12',
                    command = self.destroy
                ).pack(
                    ipadx = 12,
                    ipady = 7,
                    side = 'left',
                    padx = 70
                )

                tk.Button(
                    master = self,
                    text = "Copy Address",
                    font = 'bold 12',
                    image = self.clipboardimg,
                    compound = "left",
                    command = lambda: \
                    [
                        self.clipboard_clear(),
                        self.clipboard_append(self.pkey.get()),

                        messagebox.showinfo(
                            master = self,
                            title = "SimpleEtherWallet",
                            message = "Private key copied to clipboard"
                        ),

                        self.destroy()
                    ]
                ).pack(
                    side = "left",
                    padx = 20,
                    ipady = 7,
                    ipadx = 7
                )

        def checkpasswd(*args):
            if len(self.passentry.get()) == 0:

                if os.name == 'nt':
                    self.lift()

                messagebox.showerror(
                    title = "Error",
                    message = "Password field is empty"
                )

                return

            try:
                with open(selectedwallet.get(), 'r') as f:
                    useless = Account.from_key(
                        Account.decrypt(
                            json.load(f),
                            password = self.passentry.get()
                        )
                    )

                self.destroy()
                DisplayPrivateKey()

            except ValueError:
                messagebox.showerror(
                    title = "Error",
                    message = "Incorrect password. Try again"
                )

                self.passentry.delete(0, tk.END)

                self.lift()
                return

        self.passentry.bind('<Return>', lambda e: checkpasswd(e))

        tk.Button(
            master = self,
            text = 'Cancel',
            font = 'bold 12',
            command = self.destroy
        ).pack(
            ipadx = 7,
            ipady = 3,
            padx = 70,
            side = 'left'
        )

        tk.Button(
            master = self,
            text = 'Show private key',
            font = 'bold 12',
            command = checkpasswd
        ).pack(
            ipadx = 7,
            ipady = 3,
            padx = 70,
            side = 'right'
        )

# Donate ETH
class DonateEther(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title("SimpleEtherWallet  -  Donate")

        def rm_p():
            try:
                os.remove("p.png")

            except Exception:
                return

            return

        self.protocol(
            "WM_DELETE_WINDOW",
            lambda: \
            [
                rm_p(),
                self.destroy()
            ]
        )

        center_window(680, 710, self)

        tk.Label(
            master = self,
            text = '\nDonate',
            font = 'bold 12'
        ).pack(pady = 10)

        self.donomsgframe = tk.LabelFrame(
            master = self,
            bd = 3
        )

        self.donomsgframe.pack(
            pady = 20,
            padx = 30,
            side = 'top'
        )

        tk.Label(
            master = self.donomsgframe,
            text = "I have made this program with care, and have dedicated a lot of time, and effort, into creating SimpleEtherWallet.\n\n" "Donations are not required, of course! They are a personal decision.\n"
            "If, you wish to send me a crypto asset in another blockchain, click 'Send via another blockchain. Thank you!!!!'",
            font = 'bold 12',
            wrap = 525
        ).pack(
            padx = 40,
            pady = 20
        )

        qrcode = segno.make_qr('0x508547c4Bac880C1f4A2336E39C55AB520d43F59')
        qrcode.save(
            "p.png",
            scale = 8,
            border = 1
        )

        self.f_img = type(PhotoImage)
        self.f_img =  PhotoImage(file = "p.png")

        tk.Label(
            master = self,
            image = self.f_img,
            relief = 'groove',
            bd = 4
        ).pack(pady = 10)

        self.addr = StringVar()

        self.t = tk.Entry(
            master = self,
            exportselection = False,
            highlightthickness = 0,
            font = 'bold 12',
            relief = 'flat',
            width = 64,
            textvariable = self.addr
        )

        self.addr.set('0x508547c4Bac880C1f4A2336E39C55AB520d43F59')
        self.t.pack(
            ipady = 4,
            padx = 140
        )

        self.t.configure(state = 'readonly')

        global clipboardimg

        self.clipboardimg = PhotoImage(file = imgfolder + 'icons8-copy-24.png')

        tk.Label(
            master = self,
            text = ' '
        ).pack(
            padx = 20,
            side = 'left'
        )

        tk.Button(
            master = self,
            text = 'Close',
            font = 'bold 12',
            command = self.destroy
        ).pack(
            ipadx = 18,
            ipady = 7,
            side = 'left',
            padx = 20,
            pady = 40
        )

        try:
            os.remove("p.png")

        except Exception:
            pass

        class AnotherBlockchain(tk.Toplevel):
            def __init__(self):
                super().__init__()

                self.resizable(False, False)
                self.title("SimpleEtherWallet  -  Donate")

                center_window(610, 340, self)

                newline(self, pady = 8)

                self.eopts = {
                    'font': 'bold 12',
                    'width': 44,
                    'state': 'readonly'
                }

                """ BTC """
                self.row1 = tk.Frame(master = self)
                self.row1.pack(
                    padx = 20,
                    pady = 10
                )

                tk.Label(
                    master = self.row1,
                    text = 'BTC:',
                    font = 'bold 12',
                ).pack(
                    padx = 10,
                    side = 'left'
                )

                self.btcaddr = StringVar()

                self.e1 = tk.Entry(
                    **self.eopts,
                    master = self.row1,
                    textvariable = self.btcaddr
                )

                self.e1.pack(
                    padx = 2,
                )

                self.btcaddr.set('bc1q0twjllj6wae3uxawe6h4yunzww7evp9r5l9hpy')


                """ ARB """
                self.row2 = tk.Frame(master = self)
                self.row2.pack(
                    padx = 20,
                    pady = 10
                )

                tk.Label(
                    master = self.row2,
                    text = 'ARB:',
                    font = 'bold 12',
                ).pack(
                    padx = 10,
                    side = 'left'
                )

                self.arbaddr = StringVar()

                self.e2 = tk.Entry(
                    **self.eopts,
                    master = self.row2,
                    textvariable = self.arbaddr
                )

                self.e2.pack(
                    padx = 2,
                )

                self.arbaddr.set('0x508547c4Bac880C1f4A2336E39C55AB520d43F59')

                """ ETC """
                self.row3 = tk.Frame(master = self)
                self.row3.pack(
                    padx = 20,
                    pady = 10
                )

                tk.Label(
                    master = self.row3,
                    text = 'ETC:',
                    font = 'bold 12',
                ).pack(
                    padx = 10,
                    side = 'left'
                )

                self.etcaddr = StringVar()

                self.e3 = tk.Entry(
                    **self.eopts,
                    master = self.row3,
                    textvariable = self.etcaddr
                )

                self.e3.pack(
                    padx = 2,
                )

                self.etcaddr.set('0x7a37a759bec9eD277c113F44Be86DbbFb3707eCe')

                """ SOL """
                self.row4 = tk.Frame(master = self)
                self.row4.pack(
                    padx = 20,
                    pady = 10
                )

                tk.Label(
                    master = self.row4,
                    text = 'SOL:',
                    font = 'bold 12',
                ).pack(
                    padx = 10,
                    side = 'left'
                )

                self.soladdr = StringVar()

                self.e4 = tk.Entry(
                    **self.eopts,
                    master = self.row4,
                    textvariable = self.soladdr
                )

                self.e4.pack(
                    padx = 2,
                )

                self.soladdr.set('8TrSGinmesMxQQCJL4eMKP6AfYcbtpiXktpiRtjaG4eQ')

                """ TRC-20 """
                self.row5 = tk.Frame(master = self)
                self.row5.pack(
                    padx = 20,
                    pady = 10
                )

                tk.Label(
                    master = self.row5,
                    text = 'TRX:',
                    font = 'bold 12',
                ).pack(
                    padx = 10,
                    side = 'left'
                )

                self.trxaddr = StringVar()

                self.e5 = tk.Entry(
                    **self.eopts,
                    master = self.row5,
                    textvariable = self.trxaddr
                )

                self.e5.pack(
                    padx = 2,
                )

                self.trxaddr.set('TJyonFv58FKedY7tryztppuGLKhpZRUHH9')

        tk.Button(
            master = self,
            text = 'Send via another blockchain',
            font = 'bold 12',
            command = AnotherBlockchain
        ).pack(
            side = 'left',
            ipadx = 25,
            ipady = 7,
            pady = 40
        )

        tk.Button(
            master = self,
            text = "Copy Address",
            font = 'bold 12',
            image = self.clipboardimg,
            compound = "left",
            command = lambda: \
            [
                #self.lift(),
                self.clipboard_clear(),
                self.clipboard_append(self.addr.get()),

                messagebox.showinfo(
                    master = self,
                    title = "SimpleEtherWallet",
                    message = "Address copied to clipboard"
                ),

                self.destroy()
            ]
        ).pack(
            side = "left",
            padx = 20,
            ipady = 7,
            ipadx = 7,
            pady = 40
        )


aboutbar_opts.add_command(
    label = 'License',
    command = License
)

aboutbar_opts.add_command(
    label = 'Images',
    command = ImageLinks
)

aboutbar_opts.add_separator()

aboutbar_opts.add_command(
    label = 'Show Private Key',
    command = ShowRecoveryKey
)

aboutbar_opts.add_separator()

aboutbar_opts.add_command(
    label = 'Donate',
    command = DonateEther
)

aboutbar_opts.add_separator()

aboutbar_opts.add_command(
    label = 'What is SimpleEtherWallet?',
    command = AboutWallet
)

aboutbar.add_cascade(
    label = 'Menu',
    font = 'bold 12',
    menu = aboutbar_opts
)

main.config(menu = aboutbar)

total_balance_of_assets: float = 0.0

# QR code window
class qrwindow(tk.Toplevel):
    def __init__(self = Toplevel):
        super().__init__()

        def rm_p():
            try:
                os.remove("p.png")

            except Exception:
                return

            return

        self.title("SimpleEtherWallet  -  Receive")
        self.resizable(False, False)
        self.protocol(
            "WM_DELETE_WINDOW",
            lambda: \
            [
                rm_p(),
                self.destroy()
            ]
        )

        center_window(550, 610, self)

        qrcode = segno.make_qr(account.address)
        qrcode.save(
            "p.png",
            scale = 8,
            border = 1
        )

        f_img = {"image": PhotoImage(file = "p.png")}

        tk.Label(
            master = self,
            text = "\nReceive ERC-20 asset \n",
            font = "bold 18"
        ).pack(pady = 4)

        tk.Label(
            master = self,
            text = "Only send ERC-20 assets to this address\n"
                   "NFTs are currently *not* supported"
        ).pack(pady = 4)

        f = LabelFrame(
            master = self,
            bd = 5
        )

        tk.Label(
            master = f,
            image = f_img["image"],
            compound = TOP
        ).pack()

        f.pack(pady = 15)

        usr_addr = StringVar()
        usr_addr.set(account.address)

        if os.name != 'nt':
            lbl = tk.Entry(
                master = self,
                textvariable = usr_addr,
                state = "readonly",
                relief = "flat",
                font = "14",
                highlightthickness = 0,
                width = 43
            )

        else:
            lbl = tk.Entry(
                master = self,
                textvariable = usr_addr,
                state = "readonly",
                relief = "flat",
                font = "10",
                highlightthickness = 0,
                width = 43
            )

        lbl.pack(
            anchor = "center",
            padx = 10,
            pady = 15
        )

        frame = tk.Frame(master = self)

        global clipboardimg

        clipboardimg = PhotoImage(file = imgfolder + 'icons8-copy-24.png')

        tk.Button(
            master = frame,
            text = "Copy Address",
            font = 'bold 12',
            image = clipboardimg,
            compound = "left",
            command = lambda: \
            [
                self.clipboard_clear(),
                self.clipboard_append(account.address),

                messagebox.showinfo(
                    master = self,
                    title = "SimpleEtherWallet",
                    message = "Address copied to clipboard"
                ),

                self.destroy()
            ]
        ).pack(
            side = "left",
            pady = 18,
            padx = 20,
            ipady = 7,
            ipadx = 7
        )

        tk.Button(
            master = frame,
            text = "Close",
            font = 'bold 12',
            width = 7,
            command = self.destroy
        ).pack(
            side = "right",
            pady = 18,
            ipady = 7
        )

        frame.pack()

        try:
            os.remove("p.png")

        except Exception:
            pass

        self.mainloop()

global contactbook

contactbook = {
    'name': [],
    'address': []
}

global contactsjson

contactsjson = dest_path + 'contacts.json'

if not os.path.exists(contactsjson) or \
    os.stat(contactsjson).st_size == 0:
        with open(contactsjson, 'w') as f:
            json.dump(contactbook, f)

else:
    with open(contactsjson, 'r') as f:
        n = json.load(f)

        contactbook['name']     = n['name']
        contactbook['address'] = n['address']


global plusicon
plusicon = PhotoImage(file =  imgfolder + 'icons8-plus-48.png')

global delicon
delicon = PhotoImage(file = imgfolder + 'icons8-cross-50.png')

# Add a contact to address book
class AddContact(tk.Toplevel):
    def __init__(self):
        super().__init__()

        if os.name == 'nt':
            self.lift()

        self.title('SimpleEtherWallet  -  Add Contact')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        if os.name == 'nt':
            center_window(560, 340, self)

        else:
            center_window(640, 340, self)

        self.cname = StringVar()
        self.caddr   = StringVar()

        def close(*args):
            self.destroy()

        def cont(*args):
            if len(self.cname.get()) == 0 or len(self.caddr.get()) == 0:
                pass

            else:
                if self.invalidaddr['text'] == 'Invalid address':
                    pass

                else:
                    contactbook['name'].append(self.cname.get())
                    contactbook['address'].append(self.caddr.get())

                    with open(dest_path + 'contacts.json', 'w') as f:
                        json.dump(contactbook, f)

                        AddressBook.clist.delete(0, tk.END)
                        AddressBook.clist.insert(END, *contactbook['name'])

                        AddressBook.clist2.delete(0, tk.END)
                        AddressBook.clist2.insert(END, *contactbook['address'])

                self.destroy()


        tk.Label(
            master = self,
            text = '\nEnter a name for your contact. All characters are accepted\nContacts are stored on this device',
            font = 'font 12'
        ).pack(pady = 20)

        # Contact Name
        self.frm = tk.LabelFrame(
            master = self,
            bd = 4
        )

        self.frm.pack(
            #pady = 10,
            padx = 30,
            fill = tk.X,
            expand = True
        )

        self.frm1 = tk.Frame(master = self.frm)
        self.frm1.pack(
            pady = 20,
            anchor = 'w'
        )

        tk.Label(
            master = self.frm1,
            text = 'Contact name:',
            font = 'bold 12'
        ).pack(
            side = 'left',
            padx = 7
        )

        self.name_entry = tk.Entry(
            master = self.frm1,
            textvariable = self.cname,
            font = 'bold 12',
            width = 33
        )

        self.name_entry.bind('<Return>', cont)

        self.name_entry.pack(
            side = 'left',
            padx = 17,
            ipady = 4
        )

        # Contact Address
        self.frm2 = tk.Frame(master = self.frm)
        self.frm2.pack(anchor = 'w')

        tk.Label(
            master = self.frm2,
            text = 'Contact address:',
            font = 'bold 12'
        ).pack(
            side = 'left',
            padx = 7
        )

        self.addr_entry = tk.Entry(
            master = self.frm2,
            textvariable = self.caddr,
            font = 'bold 10',
            width = 42
        )

        self.addr_entry.bind('<Return>', cont)

        self.addr_entry.pack(
            side = 'left',
            ipady = 4
        )

        # Invallid address msg
        self.invalidframe = tk.Frame(master = self.frm)
        self.invalidframe.pack(pady = 5)

        self.invalidaddr = tk.Label(
            master = self.invalidframe,
            text = '',
            font = 'bold 13',
            fg = 'black'
        )

        self.invalidaddr.pack()

        def isvalid(event):
            if len(self.caddr.get()) == 0:
                self.invalidaddr.configure(
                    text = '',
                    fg = 'black'
                )

            if w3.is_address(self.caddr.get()) == False:
                self.invalidaddr.configure(
                    text = 'Invalid address',
                    fg = 'red'
                )

            else:
                self.invalidaddr.configure(
                    text = '',
                    fg = 'black'
                )

        self.addr_entry.bind('<KeyRelease>', isvalid)

        # Buttons
        self.btnframe = tk.Frame(master = self)
        self.btnframe.pack(
            padx = 40,
            pady = 30
        )

        self.btnok = tk.Button(
            master = self.btnframe,
            text = 'Continue',
            font = 'bold 14',
            command = cont
        )

        self.btnok.pack(
            side = 'right',
            ipadx = 4
        )

        self.btncancel = tk.Button(
            master = self.btnframe,
            text = 'Cancel',
            font = 'bold 14',
            command = self.destroy
        )

        self.btncancel.pack(
            side = 'left',
            padx = 20,
            ipadx = 4
        )

       # self.addcontact  = AddContact

# Remove a contact from address book
class DelContact(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("SimpleEtherWallet  -  Delete contact")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        center_window(400, 370, self)

        tk.Label(
            master = self,
            text = '\nSelect the contact that you wish to remove',
            font = 'bold 14'
        ).pack(
            pady = 10,
            padx = 20
        )

        self.cframe = tk.LabelFrame(
            master = self,
            bd = 5
        )

        self.cframe.pack(
            fill = tk.BOTH,
            expand = True,
            padx = 25,
            pady = 20
        )

        #choice = StringVar()

        self.alist = tk.Listbox(
            master = self.cframe,
            font = 'bold 13',
            #listvariable = choice,
            selectmode = 'single'
        )

        self.alist.pack(
            fill = tk.BOTH,
            expand = True
        )

        self.sbar = tk.Scrollbar(
            master = self.alist,
            repeatdelay = 1
        )

        self.sbar.pack(
            side = 'right',
            fill = tk.Y,
        )

        self.alist.insert(END, *contactbook['name'])

        self.name = StringVar()

        def get_choice(*args):
            #inp = self.alist.curselection()
            self.name.set(self.alist.curselection())

        self.alist.bind('<<ListboxSelect>>', get_choice)

        def del_entry():
            if len(contactbook['name']) == 0:
                if os.name == 'nt':
                    self.lift()

                messagebox.showerror(
                    title = 'Error',
                    message = 'Contact book is empty',
                    icon = 'error'
                )

                self.lift()
                return

            self.choice = str(self.name.get()).replace('(', '').replace(',)', '')

            self.num: int = int(self.choice)

            del contactbook['name'][self.num]
            del contactbook['address'][self.num]

            with open(contactsjson, 'w') as f:
                json.dump(contactbook, f)

                AddressBook.clist.delete(self.num)
                AddressBook.clist2.delete(self.num)

            self.destroy()

        tk.Button(
            master = self.cframe,
            text = 'Cancel',
            font = 'bold 12',
            command = self.destroy
        ).pack(
            pady = 30,
            padx = 60,
            ipady = 4,
            side = 'left',
        )

        tk.Button(
            master = self.cframe,
            text = 'Continue',
            font = 'bold 12',
            command = del_entry
        ).pack(
            pady = 30,
            padx = 4,
            ipady = 4,
            side = 'left',
        )

# Address book class
class AddressBook(tk.Toplevel):
    def __init__(self):
        super().__init__()

        # https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front
        # Causes a weird graphical problem on Linux Mint
        if os.name == 'nt':
            self.lift()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.row_configs = {
            'padx': 22,
            'pady': 7,
            'anchor': 'w',
            'fill': 'x',
            'expand': True
        }

        self.title("SimpleEtherWallet  -  Address Book")
        self.resizable(False, False)

        if os.name == 'nt':
            center_window(670, 470, self)

        else:
            center_window(720, 470, self)

        tk.Label(
            master = self,
            text = '\nContacts',
            font = 'bold 20'
        ).pack(anchor = 'center')

        self.frame_p = tk.LabelFrame(
            master = self,
            bd = 5
        )

        self.sbar = tk.Scrollbar(
            self.frame_p,
            repeatdelay = 1
        )

        self.sbar.pack(
            side = 'right',
            fill = tk.Y,
            padx = 2
        )

        self.upframe = tk.Frame(master = self.frame_p)
        self.upframe.pack()

        self.upframe_name = tk.Frame(master = self.upframe)
        self.upframe_name.pack(side = 'left')

        tk.Label(
            master = self.upframe_name,
            text = ' '
        ).pack(
            side = 'right',
            ipadx = 120
        )

        tk.Label(
            master = self.upframe_name,
            text = 'Name',
        ).pack(side = 'left')

        self.upframe_address = tk.Frame(master = self.upframe)
        self.upframe_address.pack(side = 'right')

        tk.Label(
            #master = self.upframe,
            master = self.upframe_address,
            text = 'Address'
        ).pack(side = 'left')

        self.frame_p.pack(
            fill = tk.BOTH,
            expand = True,
            padx = 25,
            pady = 20
        )

        self.Master = {'master': self.frame_p}

        self.boxframe = tk.Frame(**self.Master)

        self.boxframe.pack(
            fill = tk.BOTH,
            expand = True,
        )

        self.boxconf = {
            'master': self.boxframe,
            'font':  'bold 10'
        }

        # Contact names
        AddressBook.clist = tk.Listbox(**self.boxconf)

        def noselect(event):
            return 'break'

        AddressBook.clist.bind('<Button-1>',  noselect)
        AddressBook.clist.bind('<Motion>', noselect)
        AddressBook.clist.bind('<Leave>', noselect)

        AddressBook.clist.bind('<Button-1>',  noselect)
        AddressBook.clist.bind('<Motion>', noselect)
        AddressBook.clist.bind('<Leave>', noselect)

        AddressBook.clist.insert(END, *contactbook['name'])
        AddressBook.clist.pack(
            side = 'left',
            fill = tk.BOTH,
            expand = True
        )

        # Contact addresses
        AddressBook.clist2 = tk.Listbox(**self.boxconf)

        AddressBook.clist2.bind('<Button-1>',  noselect)
        AddressBook.clist2.bind('<Motion>', noselect)
        AddressBook.clist2.bind('<Leave>', noselect)

        AddressBook.clist2.bind('<Button-1>',  noselect)
        AddressBook.clist2.bind('<Motion>', noselect)
        AddressBook.clist2.bind('<Leave>', noselect)

        AddressBook.clist2.insert(END, *contactbook['address'])
        AddressBook.clist2.pack(
            side = 'left',
            fill = tk.BOTH,
            expand = True,
        )

        self.buttonframe = tk.Frame(
            master = self.frame_p,
            relief = 'raised'
        )

        self.buttonframe.pack(
            fill = tk.BOTH,
            expand = True,
            pady = 5
        )

        # Space
        tk.Label(
            master = self.buttonframe,
            text = ' '
        ).pack(
            side = 'left',
            padx = 50
        )

        tk.Button(
            master = self.buttonframe,
            text = 'Cancel',
            font = 'bold 16',
            command = lambda: [
                main.deiconify(),
                self.destroy()
            ]
        ).pack(
            side = 'left',
            padx = 20,
            ipady = 7,
            ipadx = 11
        )

        # Remove contact button
        self.deletec = tk.Button(
            master = self.buttonframe,
            image = delicon,
            width = 58,
            command = DelContact
        )

        self.deletec.pack(
            side = 'left',
            padx = 20,
            ipadx = 11
        )

        # Add contact button
        self.addc = tk.Button(
            master = self.buttonframe,
            image = plusicon,
            width = 62,
            command = AddContact
        )

        self.addc.pack(
            side = 'left',
            padx = 20,
            ipadx = 11
        )

##@ Icons taken from: https://icons8.com/icons/ @##

side_button_frame = tk.Frame(
    master = main,
    pady = 20,
    padx = 10
)

frame_button_opts = {
    "master": side_button_frame,
    "image": None,
    "compound": "top",
    "height": 61,
    "width":  2,
    "relief": "flat",
    "padx": 55
}

# send
side_button1 = tk.Button(**frame_button_opts)

global sendcoins

sendcoins = PhotoImage(file = imgfolder + 'icons8-forward-arrow-50.png')

side_button1.config(
    image = sendcoins,
    text = "Send"
)

side_button1.pack(
    anchor = "s",
    side = "left"
)

# receive
side_button2 = tk.Button(**frame_button_opts)

global receivecoins

receivecoins = PhotoImage(file = imgfolder + 'icons8-reply-arrow-50.png')

side_button2.config(
    image = receivecoins,
    text = "Receive",
    command = qrwindow
)

side_button2.pack(
    anchor = "s",
    side = "left"
)

# address book
side_button3 = tk.Button(**frame_button_opts)

global address_book

address_book = PhotoImage(file = imgfolder + 'icons8-open-book-50.png')

AddressBook = AddressBook

side_button3.config(
    image = address_book,
    text = "Address Book",
    command = AddressBook
)

side_button3.pack(
    anchor = "s",
    side = "left"
)

""" History attempt was side_button4
    I will work on it in the future """

# change wallet
side_button5 = tk.Button(**frame_button_opts)

global changewallet

changewallet = PhotoImage(file = imgfolder + 'icons8-wallet-50.png')

if os.name == 'nt':
    side_button5.config(
        image = changewallet,
        text = "Change Wallet",
        command = lambda: \
        [
            main.destroy(),
            os.execv(sys.executable, ['py'] + sys.argv)
        ]
    )

else:
    side_button5.config(
        image = changewallet,
        text = "Change Wallet",
    )

side_button5.pack(
    anchor = "s",
    side = "left"
)

""" RPC label coming in an update """

middle = tk.Frame(master = main)

assets_total = tk.Label(master = middle)

account = Account.from_key(w3.eth.default_account.key)
w3.eth.default_account = account.address

global refresh_img

refresh_img = PhotoImage(file = imgfolder + 'icons8-refresh-24.png')

middle.pack(anchor = "center")

refresh_btn = tk.Button(
    master = middle,
    relief = "flat",
    image = refresh_img
)

refresh_btn.pack(
    padx = 10,
    side = "right"
)

assets_total.pack(
    anchor = "center",
    pady = 8,
    fill = tk.Y,
    expand = True
)

newline(main)

asset_frame = tk.LabelFrame(
    master = main,
    bd = 4
)

asset_frame.pack(
    fill = tk.BOTH,
    expand = True,
    padx = 25
)

sbar = tk.Scrollbar(
    asset_frame,
    repeatdelay = 1
)

sbar.pack(
    side = 'right',
    fill = tk.Y
)

asset_list = tk.Listbox(
    master = asset_frame,
    font = 'bold 13'
)

#abi_file = open(abi_json_file, 'r')
abi = json.load(open(abi_json_file, 'r'))

assets_json = dest_path + 'assets.json'
assets_addr = []

# If first run or assets_json got messed with
if not os.path.exists(assets_json) or os.stat(assets_json).st_size == 0:
    assetsnames = [
        # Tether USD (USDT)
        '0xdAC17F958D2ee523a2206206994597C13D831ec7',

        # USD Coin (USDC)
        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',

        # DAI Stablecoin (DAI)
        '0x6B175474E89094C44Da98b954EedeAC495271d0F',

        # Polygon Ecosystem Token/MATIC (POL)
        '0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6'
    ]

    with open(assets_json, 'w') as f:
        json.dump(assetsnames, f)

with open(assets_json, 'r') as f:
    assets_addr = json.load(f)

default_listbox_entries = [
    ' ' + 'Tether USD (USDT)',
    ' ' + 'USD Coin (USDC)',
    ' ' + 'Dai Stablecoin (DAI)',
    ' ' + 'Polygon Ecosystem Token (POL)',
]

asset_list2 = tk.Listbox(
    master = asset_frame,
    font = 'bold 13'
)

def stop_click_highlight_underscore(event):
    return 'break'

asset_list.bind('<Button-1>',  stop_click_highlight_underscore)
asset_list.bind('<Motion>', stop_click_highlight_underscore)
asset_list.bind('<Leave>', stop_click_highlight_underscore)

asset_list2.bind('<Button-1>',  stop_click_highlight_underscore)
asset_list2.bind('<Motion>', stop_click_highlight_underscore)
asset_list2.bind('<Leave>', stop_click_highlight_underscore)

# ETH
if os.name == 'nt':
    asset_list.insert(END, ' Ether (ETH)\n')
else:
    asset_list.insert(END, ' Ether (ETH)')

asset_list2.insert(END, ' ' + str(w3.from_wei(w3.eth.get_balance(account.address), 'ether')))

total_balance_of_assets = (float(
    w3.from_wei(w3.eth.get_balance(account.address), 'ether')) * fetch_eth_price_in('USDT'))

def create_contract(address: str):
    return w3.eth.contract(
        address = address,
        abi = abi
    )

# BEGIN class CoinFunctions
class CoinFunctions:

    # Send crypto window
    class SendCryptoWindow(tk.Toplevel):
        def __init__(self):
            super().__init__()

            main.withdraw()

            self.title("SimpleEtherWallet  -  Send")
            self.resizable(False, False)
            self.protocol(
                "WM_DELETE_WINDOW",
                lambda: [
                    main.deiconify(),
                    self.destroy()
                ]
            )

            if os.name == 'nt':
                center_window(600, 520, self)

            else:
                center_window(640, 520, self)

            tk.Label(
                master = self,
                text = '\nSend ERC-20 asset',
                font = 'bold 14'
            ).pack(pady = 10)

            self.frame_p = tk.LabelFrame(
                master = self,
                bd = 5
            )

            self.frame_p.pack(
                pady = 20,
                padx = 20,
                anchor = 'center',
                fill = tk.BOTH,
                expand = True
            )

            self.stuff = [
                "Asset: ",
                "Address: ",
                "Amount: ",
                "Gas fee: ",
                "Priority fee:"
            ]

            self.row_configs = {
                'padx': 22,
                'pady': 7,
                'anchor': 'w',
                'fill': 'x',
                'expand': True
            }

            # Address
            stringentry1 = StringVar()

            # Amount
            stringentry2 = StringVar()

            gasfee_entry = StringVar()

            # BEGIN Asset
            self.row1 = tk.Frame(master = self.frame_p)
            self.row1.pack(**self.row_configs)

            tk.Label(
                master = self.row1,
                text = self.stuff[0],
                font = 'bold 13'
            ).pack(
                side = 'left',
                padx = 5,
            )

            self.values = []

            box = ttk.Combobox(
                master = self.row1,
                state = 'readonly',
                values = self.values,
                width = 7
            )

            box['values'] = 'ETH'

            for i in range(0, len(assets_addr)):
                self.contract          = create_contract(assets_addr[i])
                self.token_symbol = self.contract.functions.symbol().call()

                # https://stackoverflow.com/questions/51590357/appending-values-to-ttk-comboboxvalues-without-reloading-combobox
                # note: I needed a way to update combobox; reload or not isn't important
                box['values'] = (*box['values'], self.token_symbol)

            box.pack(
                padx = 19,
                ipady = 5,
                side = 'left'
            )

            balance = StringVar()

            self.balance_text = tk.Label(
                master = self.row1,
                text = '',
                font = 'bold 12'
            )

            self.balance_text.pack(
                side = 'left',
            )

            def get_asset_val(event):
                self.selected = box.current()

                self.assetlist = assets_addr

                if self.selected == 0:
                    self.balance_text.configure(
                        text = f"Balance: ~{str(w3.from_wei(w3.eth.get_balance(account.address), 'ether'))[:12]} ETH"
                    )

                else:
                    self.contract = create_contract(self.assetlist[self.selected - 1])
                    self.val          = self.contract.functions.balanceOf(account.address).call()

                    self.balance_text.configure(
                        text = f"Balance: ~{str(w3.from_wei(self.val, 'ether'))[:12]} {self.contract.functions.symbol().call()}"
                    )

            box.bind("<<ComboboxSelected>>", get_asset_val)
            # END Asset

            # BEGIN Address
            row2 = tk.Frame(master = self.frame_p)
            row2.pack(**self.row_configs)

            label1 = tk.Label(
                master = row2,
                text = self.stuff[1],
                font = 'bold 13'
            )

            label1.pack(
                padx = 5,
                pady = 7,
                side = 'left'
            )

            entry1 = tk.Entry(
                master = row2,
                width = 40,
                font = 'bold 9',
                textvariable = stringentry1
            )

            def entry1event(event):
                stringentry1.set(stringentry1.get()[:42])

                if len(entry1.get()) == 0:
                    entry1.config(
                        highlightbackground = 'black',
                        highlightthickness = 0
                    )

                elif not w3.is_address(entry1.get()):
                    entry1.config(
                        highlightbackground = 'red',
                        highlightthickness = 1
                    )

                else:
                    entry1.config(
                        highlightbackground = 'black',
                        highlightthickness = 0
                    )

            entry1.bind('<KeyRelease>', entry1event)
            entry1.bind('<Button-1>', entry1event)

            entry1.pack(
                ipady = 5,
                pady = 7,
                ipadx = 2,
                side = 'left'
            )

            global abook

            abook = PhotoImage(file = imgfolder + 'icons8-open-book-24.png')

            class abookwindow(tk.Toplevel):
                def __init__(self):
                    super().__init__()

                    self.title("SimpleEtherWallet  -  Contacts")
                    self.resizable(False, False)
                    self.protocol(
                        "WM_DELETE_WINDOW",
                        self.destroy
                    )

                    center_window(570, 480, self)

                    self.boxframe = tk.LabelFrame(
                        master = self,
                        bd = 4
                    )

                    self.boxframe.pack(
                        pady = 20,
                        padx = 20,
                        fill = tk.BOTH,
                        expand = True,
                    )

                    self.box = tk.Listbox(
                        master = self.boxframe,
                        font = 'bold 11'
                    )

                    self.box.pack(
                        padx = 4,
                        pady = 4,
                        fill = tk.BOTH,
                        expand = True,
                    )

                    sbar = tk.Scrollbar(
                        self.box,
                        repeatdelay = 1
                    )

                    sbar.pack(
                        side = 'right',
                        fill = tk.Y
                    )


                    self.contactchoice = ''

                    for i in range(0, len(contactbook['name'])):
                        self.box.insert(END, contactbook['name'][i] + ' (' + contactbook['address'][i] + ')')

                    def get_choice(*args):
                        choice = str(self.box.curselection()).replace('(', '').replace(',)', '')

                        num: int = int(choice)

                        self.contactchoice = contactbook['address'][num]

                        #sendcryptowindow.stringentry1.set(contactbook['address'][num])
                        #self.destroy()

                    self.box.bind('<<ListboxSelect>>', get_choice)

                    self.btnframe = tk.Frame(master = self)
                    self.btnframe.pack(
                        pady = 10,
                        padx = 30
                    )

                    b1 = tk.Button(
                        master = self.btnframe,
                        text = 'Cancel',
                        font = 'bold 16',
                        command = self.destroy
                    )

                    b1.pack(
                        side = 'left',
                        padx = 20,
                        ipady = 4,
                        ipadx = 12
                    )

                    b2 = tk.Button(
                        master = self.btnframe,
                        text = 'Done',
                        font = 'bold 16',
                        command = lambda: [
                            stringentry1.set(self.contactchoice),
                            self.destroy()
                        ]
                    )

                    b2.pack(
                        side = 'left',
                        ipady = 4,
                        ipadx = 12
                    )

                    newline(self)

            abookbtn = tk.Button(
                master = row2,
                image = abook,
                command = abookwindow
            )

            abookbtn.pack(
                side = 'left',
                padx = 14
            )

            # END Address

            # BEGIN Amount
            row3 = tk.Frame(master = self.frame_p)
            row3.pack(**self.row_configs)

            label2 = tk.Label(
                master = row3,
                text = self.stuff[2],
                font = 'bold 12'
            )

            label2.pack(
                padx = 5,
                side = 'left'
            )

            entry2 = tk.Entry(
                master = row3,
                width = 25,
                font = 'bold 12',
                textvariable = stringentry2
            )

            entry2.pack(
                ipady = 5,
                padx = 8,
                side = 'left'
            )

            def validamount(event):
                if len(entry2.get()) == 0:
                    entry2.config(
                        highlightbackground = 'black',
                        highlightthickness = 0
                    )

                elif entry2.get().count('.') == 0:
                    if entry2.get().isdigit() == False:
                        entry2.config(
                            highlightbackground = 'red',
                            highlightthickness = 1
                        )

                    elif entry2.get().isdigit() == True:
                        if entry2.get() == '0':
                            entry2.config(
                            highlightbackground = 'red',
                            highlightthickness = 1
                        )

                        else:
                            entry2.config(
                                highlightbackground = 'green',
                                highlightthickness = 1
                            )

                elif entry2.get().count('.') == 1:
                    if entry2.get().startswith('.'):
                        entry2.config(
                            highlightbackground = 'red',
                            highlightthickness = 1
                        )

                    else:
                        n = entry2.get().replace('.', '')

                        if n.isdigit() == False:
                            entry2.config(
                                highlightbackground = 'red',
                                highlightthickness = 1
                            )

                        else:
                            entry2.config(
                                highlightbackground = 'black',
                                highlightthickness = 0
                            )

                elif entry2.get().count('.') > 1:
                    entry2.config(
                        highlightbackground = 'red',
                        highlightthickness = 1
                    )

            entry2.register(validamount)
            entry2.bind('<KeyRelease>', validamount)

            sc_percent = IntVar()

            sc_amount = tk.Scale(
                master = row3,
                from_ = 0,
                to = 100,
                resolution = 25,
                orient = 'horizontal',
                length = 100,
                digits = 3,
                bd = 4,
                cursor = 'cross',
                variable = sc_percent,
            )

            self.sc_val:float = 0.0

            def sc_cmd(event):
                selected = box.current()

                if selected == 0:
                    self.user_balance = w3.from_wei(w3.eth.get_balance(account.address), 'ether')

                else:
                    contract = create_contract(assets_addr[selected - 1])
                    val          = contract.functions.balanceOf(account.address).call()

                    self.user_balance = val

                #if sc_amount.get() == 25:
                if sc_percent.get() == 100:
                    self.sc_val = self.user_balance
                    stringentry2.set('ALL')

                elif sc_percent.get() == 0:
                    stringentry2.set('')

                elif sc_percent.get() == 25:
                    self.sc_val = float(self.user_balance) * 0.25
                    stringentry2.set(str(self.sc_val))

                elif sc_percent.get() == 50:
                    self.sc_val = float(self.user_balance) * 0.5
                    stringentry2.set(str(self.sc_val))

                elif sc_percent.get() == 75:
                    self.sc_val = float(self.user_balance) * 0.75
                    stringentry2.set(str(self.sc_val))

            sc_amount.bind('<ButtonRelease-1>', sc_cmd)
            sc_amount.bind('<Button-1>', sc_cmd)

            sc_amount.set(0)

            sc_amount.pack(
                ipady = 8,
                padx = 7,
                side = 'left'
            )
            # END Amount

            # BEGIN Gas fee
            row4 = tk.Frame(master = self.frame_p)
            row4.pack(**self.row_configs)

            label3 = tk.Label(
                master = row4,
                text = self.stuff[3],
                font = 'bold 12'
            )

            label3.pack(
                padx = 4,
                side = 'left'
            )

            entry3 = tk.Entry(
                master = row4,
                width = 20,
                font = 'bold 12',
                textvariable = gasfee_entry,
                state = 'readonly'
            )

            entry3.pack(
                ipady = 5,
                padx = 8,
                side = 'left'
            )

            checkbox_gasopt = IntVar()

            gasfee_entry.set(str(w3.eth.gas_price / 10000000000)[:23])

            def updategas():
                if checkbox_gasopt.get() == 0:
                    gasfee_entry.set(str(w3.eth.gas_price / 10000000000)[:23])

                self.after(14000, updategas)

            loop = self.after(14000, updategas)

            self.after(14000, updategas)

            def customgasfee():
                if checkbox_gasopt.get() == 1:
                    entry3.config(
                        state = 'normal',
                        highlightbackground = 'black',
                        highlightthickness = 0
                    )

                    entry3.delete(0, tk.END)

                else:
                    entry3.config(
                        state = 'readonly',
                        highlightbackground = 'black',
                        highlightthickness = 0
                    )

                    self.after_cancel(loop)
                    updategas()

            checkbox_gas = tk.Checkbutton(
                master = row4,
                text = 'custom gas',
                variable = checkbox_gasopt,
                command = customgasfee
            )

            checkbox_gas.pack(
                padx = 20,
                side = 'left'
            )

            def validgas(event):
                if checkbox_gasopt.get() == 1:
                    if len(entry3.get()) == 0:
                        entry3.config(
                            highlightbackground = 'black',
                            highlightthickness = 0
                        )

                    elif entry3.get().count('.') == 0:
                        if entry3.get().isdigit() == False:
                            entry3.config(
                                highlightbackground = 'red',
                                highlightthickness = 1
                            )

                        elif entry3.get().isdigit() == True:
                            if entry3.get() == '0':
                                entry3.config(
                                highlightbackground = 'red',
                                highlightthickness = 1
                            )

                            else:
                                entry3.config(
                                    highlightbackground = 'green',
                                    highlightthickness = 1
                                )

                    elif entry3.get().count('.') == 1:
                        if entry3.get().startswith('.'):
                            entry3.config(
                                highlightbackground = 'red',
                                highlightthickness = 1
                            )

                        else:
                            n = entry3.get().replace('.', '')

                            if n.isdigit() == False:
                                entry3.config(
                                    highlightbackground = 'red',
                                    highlightthickness = 1
                                )

                            else:
                                entry3.config(
                                    highlightbackground = 'black',
                                    highlightthickness = 0
                                )

                    elif entry3.get().count('.') > 1:
                        entry3.config(
                            highlightbackground = 'red',
                            highlightthickness = 1
                        )

                elif checkbox_gasopt.get() == 0:
                    entry3.config(
                        highlightbackground = 'black',
                        highlightthickness = 0
                    )

                else:
                    entry3.config(
                        highlightbackground = 'black',
                        highlightthickness = 0
                    )

            entry3.register(validgas)
            entry3.bind('<KeyRelease>', validgas)
            # END end gas fee

            # Cancel/Continue frame
            row5 = tk.Frame(master = self.frame_p)
            row5.pack(pady = 30)

            btn1 = tk.Button(
                master = row5,
                text = 'Cancel',
                font = 'bold 14',
                command = lambda: [
                    main.deiconify(),
                    self.destroy()
                ]
            )

            btn1.pack(
                ipady = 7,
                ipadx = 7,
                padx = 30,
                side = 'left'
            )

            class ConfirmSend(tk.Toplevel):
                def __init__(self):
                    super().__init__()

                    self.rowconf = {
                        'padx': 22,
                        'anchor': 'w',
                        'fill': 'x',
                        'expand': True,
                        'pady': 8
                    }

                    self.entryconf = {
                        'font': 'bold 12',
                        'state': 'readonly',
                        'width': 41,
                        'bd': 1,
                    }

                    #self.balance          = float(self.user_balance)
                    self.address          = stringentry1.get()
                    self.amount           = stringentry2.get()
                    self.contract          = create_contract(assets_addr[box.current() - 1])

                    self.get_symbol     = self.contract.functions.symbol().call()
                    self.get_name       = self.contract.functions.name().call()

                    self.final_amount  = 0.0

                    if self.amount == 'ALL':
                        self.amount = SendCryptoWindow.sc_val

                    self.title('SimpleEtherWallet  -  Verify details')
                    self.resizable(False, False)
                    self.protocol("WM_DELETE_WINDOW", self.destroy)

                    center_window(544, 580, self)

                    tk.Label(
                        master = self,
                        text = '\nVerify send details',
                        font = 'bold 16'
                    ).pack(pady = 10)

                    self.frame = tk.LabelFrame(
                        master = self,
                        bd = 4
                    )

                    self.frame.pack(
                        fill = tk.X,
                        expand = True,
                        padx = 14,
                        pady = 30,
                        anchor = 'n'
                    )

                    # Asset
                    self.row1 = tk.Frame(master = self.frame)
                    self.row1.pack(**self.rowconf)

                    self.asset_label = tk.Label(
                        master = self.row1,
                        text = 'Asset: ',
                        font = 'bold 12'
                    )

                    self.asset_label.pack(
                        side = 'left',
                        pady = 4,
                        ipadx = 9
                    )

                    self.avar = StringVar()

                    self.assetbox = tk.Entry(
                        master = self.row1,
                        textvariable = self.avar,
                        **self.entryconf
                    )

                    self.assetbox.pack(side = 'left')

                    if box.current() == 0:
                        self.avar.set('Ether (ETH)')

                    else:
                        #self.contact = create_contract(assets_addr[box.current() - 1])

                        self.avar.set(f'{self.get_name} ({self.get_symbol}) ')
                        self.assetbox['width'] = len(self.avar.get())

                    # Address
                    self.row2 = tk.Frame(master = self.frame)
                    self.row2.pack(**self.rowconf)

                    self.addr = tk.Label(
                        master = self.row2,
                        text = "Address: ",
                        font = 'bold 12'
                    )

                    self.addr.pack(
                        side = 'left',
                        pady = 4
                    )

                    self.addrvar = StringVar()

                    self.addrbox = tk.Entry(
                        master = self.row2,
                        textvariable = self.addrvar,
                        **self.entryconf
                    )

                    self.addrbox.pack(side = 'left')
                    self.addrvar.set(self.address)

                    # Amount
                    self.row3 = tk.Frame(master = self.frame)
                    self.row3.pack(**self.rowconf)

                    self.am = tk.Label(
                        master = self.row3,
                        text = "Amount: ",
                        font = 'bold 12'
                    )

                    self.am.pack(
                        side = 'left',
                        pady = 4,
                        ipadx = 3
                    )

                    self.amvar = StringVar()

                    self.ambox = tk.Entry(
                        master = self.row3,
                        textvariable = self.amvar,
                        **self.entryconf
                    )

                    self.ambox.pack(side = 'left')
                    self.amvar.set(self.amount)

                    self.ambox['width'] = len(self.amvar.get()) + 1

                    self.txt = tk.Label(
                        master = self.row3,
                        #text = self.contract.functions.symbol().call(),
                        font = 'bold 12'
                    )

                    if box.current() == 0:
                        self.txt['text'] = 'ETH'

                    else:
                        self.txt['text'] = self.contract.functions.symbol().call()

                    self.txt.pack(side = 'left')


                    # Value
                    self.row4 = tk.Frame(master = self.frame)
                    self.row4.pack(**self.rowconf)

                    self.val = tk.Label(
                        master = self.row4,
                        text = "Value: ",
                        font = 'bold 12'
                    )

                    self.val.pack(
                        side = 'left',
                        pady = 4,
                        ipadx = 9
                    )

                    self.valvar = StringVar()

                    self.valbox = tk.Entry(
                        master = self.row4,
                        textvariable = self.valvar,
                        **self.entryconf
                    )

                    self.valbox.pack(side = 'left')

                    if self.avar.get() == 'Ether (ETH)':
                        self.valvar.set(str(fetch_eth_price_in('USDT') * float(self.amount)))

                    else:
                        self.assetname = self.contract.functions.symbol().call()

                        self.priceofasset: float = 0.0
                        self.priceofasset = fetch_price_of_and_convert_to(self.assetname, 'USDT')

                        self.valvar.set(str(self.priceofasset * float(self.amount)))
                        self.valvar.set("{:.12f}".format(float(self.valvar.get())))

                    self.valbox['width'] = len(self.valvar.get())

                    if self.valvar.get() != 0.0:
                        tk.Label(
                            master = self.row4,
                            text = '$',
                            font = 'bold 12'
                        ).pack(side = 'left')

                    else:
                        self.valbox.destroy()

                        self.valbox = tk.Label(
                            text = 'Cannot fetch token price (not listed on major exchanges)',
                            font = 'bold 10',
                            fg = 'red'
                        )

                        self.valbox.pack(side = 'left')


                    # Gas Fee
                    self.row5 = tk.Frame(master = self.frame)
                    self.row5.pack(**self.rowconf)

                    self.gas = tk.Label(
                        master = self.row5,
                        text = 'Gas fee: ',
                        #text = f"Gas fee: {self.gas} USD",
                        font = 'bold 12'
                    )

                    self.gas.pack(
                        side = 'left',
                        pady = 4,
                        ipadx = 2
                    )

                    self.gasvar = StringVar()

                    self.gasbox = tk.Entry(
                        master = self.row5,
                        textvariable = self.gasvar,
                        **self.entryconf
                    )

                    self.gasbox.pack(side = 'left')
                    #self.gasvar.set(entry3.get())

                    #self.gasbox['width'] = len(self.gasvar.get()) + 1

                    self.usdlabel5 = tk.Label(
                        master = self.row5,
                        text = '',
                        font = 'bold 12'
                    )

                    self.usdlabel5.pack(side = 'left')

                    # Priority fee
                    self.row6 = tk.Frame(master = self.frame)
                    self.row6.pack(**self.rowconf)

                    self.pfee = tk.Label(
                        master = self.row6,
                        text = "Priority: ",
                        font = 'bold 12'
                    )

                    self.pfee.pack(
                        side = 'left',
                        pady = 4,
                        ipadx = 5
                    )

                    self.feevar = StringVar()

                    self.feebox = tk.Entry(
                        master = self.row6,
                        textvariable = self.feevar,
                        **self.entryconf
                    )

                    self.feebox.pack(side = 'left')
                    self.feevar.set(float(entry3.get()) / 2)

                    self.feebox['width'] = len(self.feevar.get()) + 1

                    tk.Label(
                        master = self.row6,
                        text = '$',
                        font = 'bold 12'
                    ).pack(side = 'left')

                    # Total fee
                    self.total = tk.Frame(master = self.frame)
                    self.total.pack(**self.rowconf)

                    self.total_label = tk.Label(
                        master = self.total,
                        text = '',
                        font = 'bold 16'
                    )

                    self.total_label.pack(
                        side = 'left',
                        pady = 14
                    )


                    self.final_amount = float(self.valvar.get()) + float(entry3.get())  + float(float(entry3.get()) / 2)

                    self.total_label.configure(text = f"Total (in USD): ~{self.final_amount}")

                    self.gasineth = float(entry3.get()) / fetch_eth_price_in('USDT')

                    ConfirmSend.GAS = self.gasineth

                    self.gasinethSTR = str(self.gasineth)[:17]

                    #self.usdlabel5.configure(text = f"$  (~{self.gasinethSTR} ETH)")
                    self.usdlabel5.configure(text = f"~{entry3.get()} $")
                    self.gasvar.set(f"{self.gasinethSTR} ETH")
                    self.gasbox['width'] = len(self.gasvar.get())

                    ConfirmSend.v = float(entry3.get())

                    class FinalizeTransaction(tk.Toplevel):
                        def __init__(self):
                            super().__init__()

                            self.title('SimpleEtherWallet  -  Verify details')
                            self.resizable(False, False)
                            self.protocol("WM_DELETE_WINDOW", quit)

                            center_window(544, 288, self)

                            self.someimg       = PhotoImage(file = imgfolder + 'eth.png')

                            self.closed_eyes  = imgfolder + 'icons8-eyes-24-closed.png'
                            self.hidepass        = PhotoImage(file = closed_eyes)

                            self.opened_eyes = imgfolder + 'icons8-eyes-24.png'
                            self.showpass      = PhotoImage(file = opened_eyes)

                            self.opt = IntVar()
                            self.opt.set(1)

                            self.transaction = {
                                # From
                                "from": account.address,
                                # To
                                "to": w3.to_checksum_address(SendCryptoWindow.stringentry1.get()),
                                # Value
                                "value": w3.to_wei(ConfirmSend.v, 'ether'),
                                # Nounce
                                'nonce': w3.eth.get_transaction_count(account.address),
                                # Gas
                                'gas': 0,
                                #  Max Gas
                                'maxFeePerGas': w3.to_wei(ConfirmSend.GAS, 'ether'),
                                # Miner Tip (priority fee)
                                'maxPriorityFeePerGas': w3.to_wei(ConfirmSend.GAS / 2, 'ether')
                            }

                            def unhide():
                                if self.opt.get() == 1:
                                    self.btn.config(image = self.showpass)
                                    self.passentry.config(show = "")

                                    self.opt.set(0)

                                elif self.opt.get() == 0:
                                    self.btn.config(image = self.hidepass)
                                    self.passentry.config(show = "*")

                                    self.opt.set(1)

                            self.frm = tk.LabelFrame(master = self)
                            self.frm.pack(
                                pady = 20,
                                padx = 20,
                                fill = tk.BOTH,
                                expand = True
                            )

                            self.frm2 = tk.Frame(master = self.frm)
                            self.frm2.pack(
                                pady = 10,
                                padx = 10
                            )

                            newline(self.frm2, pady = 4)

                            tk.Label(
                                master = self.frm2,
                                text = 'Enter your password to complete the transaction',
                                font = 'bold 14'
                            ).pack(pady = 7)

                            self.btn = tk.Button(
                                master = self.frm2,
                                image = self.hidepass,
                                command = unhide
                            )

                            self.btn.pack(
                                side = "right",
                                padx = 10,
                            )

                            self.password = StringVar()

                            self.passentry = tk.Entry(
                                master = self.frm2,
                                bd = 2,
                                highlightthickness = 1,
                                exportselection = 0,
                                width = 40,
                                show = "*",
                                textvariable = self.password
                            )

                            self.passentry.pack(
                                ipady = 5,
                                pady = 10,
                                side = 'right'
                            )

                            tk.Label(
                                master = self.frm2,
                                text = "Password:",
                                font = 'bold 13'
                            ).pack(side = 'left')

                            self.pkey = type(Account.from_key)

                            def checkpass():
                                if len(self.passentry.get()) == 0:
                                    messagebox.showerror(
                                        title = "Error",
                                        message = "Password field is empty"
                                    )

                                    return

                                try:
                                    nameofwallet['name'] = conf_file_contents['last']

                                    with open(nameofwallet["name"], "r") as f:
                                        self.pkey = Account.from_key(
                                            Account.decrypt(
                                                json.load(f),
                                                password = self.passentry.get()
                                            )
                                        )

                                except ValueError:
                                    messagebox.showerror(
                                        title = "Error",
                                        message = "Incorrect password. Try again"
                                    )

                                    self.passentry.delete(0, tk.END)
                                    return

                                try:
                                    self.gasp = w3.eth.estimate_gas(self.transaction)
                                    self.transaction.update({'gas': self.gasp})

                                    self.signed = w3.eth.account.sign_transaction(
                                        self.transaction,
                                        self.pkey
                                    )

                                    self.tx_hash = w3.eth.send_raw_transaction(self.signed.raw_transaction)
                                    tx = w3.eth.get_transaction(self.tx_hash)

                                except Exception:
                                    messagebox.showerror(
                                        title = "Error",
                                        message = "Insufficient funds to complete the transaction"
                                    )

                                    self.passentry.delete(0, tk.END)
                                    return

                            self.frm3 = tk.Frame(master = self.frm)
                            self.frm3.pack(
                                pady = 20,
                                anchor = 'n',
                                side = 'top'
                            )

                            tk.Button(
                                master = self.frm3,
                                text = 'Cancel',
                                font = 'bold 12',
                                command = self.destroy
                            ).pack(
                                side = "left",
                                padx = 10,
                                ipady = 4
                            )

                            tk.Button(
                                master = self.frm3,
                                text = "Sign",
                                font = 'bold 12',
                                command = checkpass
                            ).pack(
                                side = "left",
                                padx = 10,
                                ipady = 4
                            )

                    tk.Label(
                        master = self,
                        text = '',
                        font = 'bold 14',
                    ).pack(
                        ipady = 7,
                        ipadx = 7,
                        pady = 10,
                        padx = 50,
                        side = 'left'
                    )

                    tk.Button(
                        master = self,
                        text = 'Cancel',
                        font = 'bold 14',
                        command = self.destroy
                    ).pack(
                        ipady = 9,
                        ipadx = 7,
                        pady = 15,
                        side = 'left'
                    )

                    tk.Label(
                        master = self,
                        text = '',
                        font = 'bold 14',
                    ).pack(
                        ipady = 7,
                        ipadx = 7,
                        pady = 10,
                        padx = 40,
                        side = 'left'
                    )

                    tk.Button(
                        master = self,
                        text = 'Confirm',
                        font = 'bold 14',
                        command = FinalizeTransaction
                    ).pack(
                        ipady = 9,
                        ipadx = 7,
                        pady = 15,
                        side = 'left'
                    )

                    #newline(self, pady = 7)

            def check_send_details():
                if entry1['highlightbackground'] == 'red' or \
                    entry2['highlightbackground'] == 'red':
                        pass

                elif entry3['state'] != 'readonly' and \
                    entry3['highlightbackground'] == 'red':
                        pass

                elif len(entry1.get()) == 0 or len(entry2.get()) == 0:
                    pass

                else:
                    ConfirmSend()

            btn2 = tk.Button(
                master = row5,
                text = 'Continue',
                font = 'bold 14',
                command = check_send_details
            )

            btn2.pack(
                ipady = 7,
                ipadx = 7,
                padx = 30,
                side = 'left'
            )

    # Add a custom cryptocurrency
    class AddCoinWindow(tk.Toplevel):
        def __init__(self):
            super().__init__()

            self.title("SimpleEtherWallet  -  Add asset")
            self.resizable(False, False)
            self.protocol("WM_DELETE_WINDOW", quit)

            if os.name == 'nt':
                center_window(490, 400, self)

            else:
                center_window(550, 390, self)

            tk.Label(
                master = self,
                text = '\n'
            ).grid(row = 0)


            tk.Label(
                master = self,
                text = 'Enter the address of the ERC-20 you want to add:',
                font = 'bold 14'
            ).grid(
                row = 1,
                padx = 24
            )

            self.addressvar = StringVar()

            self.address_entry = tk.Entry(
                master = self,
                textvariable = self.addressvar,
                width = 44,
                font = 'bold 13'
            )

            if os.name == 'nt':
                self.address_entry.grid(
                    row = 2,
                    padx = 32,
                    sticky = 'w',
                    pady = 3
                )

            # off by 2, ugh
            else:
                self.address_entry.grid(
                    row = 2,
                    padx = 30,
                    sticky = 'w',
                    pady = 3
                )

            self.validaddr = False

            def errb(self):
                self.errbox = messagebox.showerror(
                    master = self,
                    title = "Error",
                    message = "The address that you have provided is either a wallet address, an invalid token address, or a token that isn't listed on centralized exhanges",
                    icon = "error"
                )

                if os.name == 'nt':
                    self.lift()

            def get_data(self, event):
                if len(self.addressvar.get()) == 0 or len(self.addressvar.get()) < 42:
                    pass

                elif not w3.is_address(self.addressvar.get()):
                    errb(self)

                elif w3.is_address(self.addressvar.get()):
                    self.addressvar.set(self.address_entry.get())

                    try:
                        self.token_name_contract = create_contract(self.addressvar.get()).functions.name()
                        self.token_name = self.token_name_contract.call()

                    except Exception:
                        errb(self)

                else:
                    self.validaddr = True

            self.decvar = StringVar()

            def get_dec(self, event):
                if self.validaddr == False:
                    self.decvar.set('')

                elif self.validaddr == True:
                    self.decimals_contract = create_contract(self.addressvar.get()).functions.decimals()
                    self.decimals = self.decimals_contract.call()

                    self.decvar.set(str(self.decimals))

                else:
                    self.decvar.set('')

            tk.Label(
                master = self,
                text = 'Decimal',
                font = 'bold 14'
            ).grid(
                row = 5,
                sticky = 'w',
                padx = 30,
                pady = 3
            )

            self.dec_entry = tk.Entry(
                master = self,
                textvariable = self.decvar,
                width = 44,
                font = 'bold 13',
                state = 'readonly',
                highlightthickness = 0
            ).grid(
                row = 6,
                sticky = 'w',
                padx = 32,
                pady = 3
            )

            tk.Label(
                master = self,
                text = 'Asset name',
                font = 'bold 14'
            ).grid(
                row = 7,
                sticky = 'w',
                padx = 30,
                pady = 6
            )

            self.assetname = StringVar()

            self.name_entry = tk.Entry(
                master = self,
                textvariable = self.assetname,
                width = 44,
                font = 'bold 13',
                state = 'readonly',
                highlightthickness = 0
            ).grid(
                row = 8,
                sticky = 'w',
                padx = 32,
                pady = 3
            )

            def get_name(self, event):
                if self.validaddr == False:
                    self.assetname.set('')

                elif self.validaddr == True:
                    self.name_contract = create_contract(self.addressvar.get()).functions.name()
                    self.name = self.name_contract.call()

                    self.assetname.set(self.name)

                else:
                    self.assetname.set('')

            tk.Label(
                master = self,
                text = 'Symbol',
                font = 'bold 14'
            ).grid(
                row = 9,
                sticky = 'w',
                padx = 30,
                pady = 3
            )

            self.symbol = StringVar()

            self.name_entry = tk.Entry(
                master = self,
                textvariable = self.symbol,
                width = 44,
                font = 'bold 13',
                state = 'readonly',
                highlightthickness = 0
            ).grid(
                row = 10,
                sticky = 'w',
                padx = 32,
                pady = 3
            )

            def get_symbol(self, event):
                if self.validaddr == False:
                    self.symbol.set('')

                elif self.validaddr == True:
                    self.symbol_contract = create_contract(self.addressvar.get()).functions.symbol()
                    self.symbol_name = self.symbol_contract.call()

                    self.symbol.set(self.symbol_name)

                else:
                    self.symbol.set('')

            self.address_entry.bind(
                '<KeyRelease>',
                lambda e: [
                    get_data(self, e),
                    get_dec(self, e),
                    get_name(self, e),
                    get_symbol(self, e)
                ]
            )

            def add_asset_details():
                if self.validaddr == False:
                    pass

                elif len(self.address_entry.get()) == 0:
                    pass

                else:
                    if self.addressvar.get() in assets_addr:
                        messagebox.showerror(
                            title = "Error",
                            message = 'Asset already in your list',
                            icon = "error",
                        )

                        self.destroy()
                        return

                    assets_addr.append(self.addressvar.get())

                    asset_list.delete(0, tk.END)
                    asset_list2.delete(0, tk.END)

                    asset_list.insert(END, ' Ether (ETH)\n')
                    asset_list2.insert(END, ' ' + str(w3.from_wei(w3.eth.get_balance(account.address), 'ether')))

                    globals()['loading'] = 0
                    filluplists()

                    self.destroy()


            tk.Button(
                master = self,
                text = 'Continue',
                font = 'bold 14',
                command = add_asset_details
            ).grid(
                pady = 20,
                padx = 100,
                row = 11,
                sticky = 'e'
            )

            tk.Button(
                master = self,
                text = 'Cancel',
                font = 'bold 14',
                command = self.destroy
            ).grid(
                pady = 20,
                padx = 100,
                row = 11,
                sticky = 'w'
            )

    # Remove a cryptocurrency from list
    class RemoveCoinWindow(tk.Toplevel):
        def __init__(self):
            super().__init__()

            self.title("SimpleEtherWallet  -  Add asset")
            self.resizable(False, False)
            self.protocol("WM_DELETE_WINDOW", quit)

            if os.name == 'nt':
                center_window(400, 370, self)

            else:
                center_window(460, 370, self)

            tk.Label(
                master = self,
                text = '\nSelect the asset that you wish to remove',
                font = 'bold 14'
            ).pack(
                pady = 10,
                padx = 20
            )

            self.asset_frame = tk.LabelFrame(
                master = self,
                bd = 5
            )

            self.asset_frame.pack(
                fill = tk.BOTH,
                expand = True,
                padx = 25,
                pady = 20
            )

            self.alist = tk.Listbox(
                master = self.asset_frame,
                font = 'bold 13',
                selectmode = 'single'
            )

            self.alist.pack(
                fill = tk.BOTH,
                expand = True
            )

            self.sbar = tk.Scrollbar(
                master = self.alist,
                repeatdelay = 1
            )

            self.sbar.pack(
                side = 'right',
                fill = tk.Y,
            )

            for i in range(0, len(assets_addr)):
                self.contract = create_contract(assets_addr[i])

                self.token_name_contract    = self.contract.functions.name()
                self.token_name                   = self.token_name_contract.call()

                self.alist.insert(END, self.token_name)

            self.token_name = StringVar()

            def get_choice(*args):
                self.inp = self.alist.curselection()
                self.token_name.set(self.inp)

            self.alist.bind('<<ListboxSelect>>', get_choice)

            def del_entry():
                self.choice = str(self.token_name.get()).replace('(', '').replace(',)', '')
                #choice = choice.replace(',)', '')

                self.num: int = int(self.choice)

                asset_list.delete(self.num+1)
                asset_list2.delete(self.num+1)

                self.contract = create_contract(globals()['assets_addr'][self.num])

                self.token_balance_contract = self.contract.functions.balanceOf(account.address)
                self.token_balance                = self.token_balance_contract.call()

                globals()['total_balance_of_assets'] = globals()['total_balance_of_assets'] - float(self.token_balance)

                del assets_addr[self.num]

                with open(assets_json, 'w') as f:
                    json.dump(assets_addr, f)

                self.destroy()

            tk.Button(
                master = self.asset_frame,
                text = 'Cancel',
                font = 'bold 12',
                command = self.destroy
            ).pack(
                pady = 30,
                padx = 60,
                ipady = 4,
                side = 'left',
            )

            tk.Button(
                master = self.asset_frame,
                text = 'Continue',
                font = 'bold 12',
                command = del_entry
            ).pack(
                pady = 30,
                padx = 4,
                ipady = 4,
                side = 'left',
            )

    # Restore default list of cryptocurrencies
    class RestoreDefaultCrypto(tk.Toplevel):
        def __init__(self):
            super().__init__()

            self.title("SimpleEtherWallet  -  Restore default coins")
            self.resizable(False, False)
            self.protocol("WM_DELETE_WINDOW", quit)

            self.withdraw()

            self.tmp = questionbox(
                """You are about to restore displayed assets back to the default. Continue?"""
            )

            def restore_default_coins_fn(self):
                if self.tmp == False:
                    self.destroy()

                else:
                    asset_list.delete(0, tk.END)
                    asset_list2.delete(0, tk.END)

                    if os.name == 'nt':
                        asset_list.insert(END, ' Ether (ETH)\n')
                        asset_list2.insert(END, ' ' + str(w3.from_wei(w3.eth.get_balance(account.address), 'ether')) + '\n')

                    else:
                        asset_list.insert(END, ' Ether (ETH)')
                        asset_list2.insert(END, ' ' + str(w3.from_wei(w3.eth.get_balance(account.address), 'ether')))

                    globals()['assets_addr'] = [
                        '0xdAC17F958D2ee523a2206206994597C13D831ec7',
                        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                        '0x6B175474E89094C44Da98b954EedeAC495271d0F',
                        '0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6'
                    ]

                    asset_list.insert(END, *default_listbox_entries)

                    for i in range(0, len(assets_addr)):
                        self.contract = create_contract(assets_addr[i])

                        self.token_balance_contract = self.contract.functions.balanceOf(account.address)
                        token_balance = self.token_balance_contract.call()

                        if os.name == 'nt':
                            asset_list2.insert(END,  ' ' + str(w3.from_wei(token_balance, 'ether')) + '\n')

                        else:
                            asset_list2.insert(END,  ' ' + str(w3.from_wei(token_balance, 'ether')))

                        with open(assets_json, 'w') as f:
                            json.dump(globals()['assets_addr'], f)

            restore_default_coins_fn(self)

            self.destroy()


# END    class CoinFunctions

coinfuncts = CoinFunctions()

# Send button config
side_button1.config(command = coinfuncts.SendCryptoWindow)

def percent(percent, number: int) -> float:
    if number == 0 or percent == 0:
        return 0

    return (percent * number) / 100.0

class AssetsLoadingBar (tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("SimpleEtherWallet  -  Loading assets")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", quit)

        center_window(330, 170, self)

        tk.Label(
            master = self,
            text = '\nLoading your crypto assets...',
            font = 'bold 16'
        ).pack(pady = 5)

        self.c = IntVar()

        self.bar = ttk.Progressbar(
            master = self,
            orient = 'horizontal',
            variable = self.c,
            length = 180,
            maximum = len(assets_addr)
        )

        self.bar.pack(
            pady = 16
        )

loading = 1

AssetsLoadingBar = AssetsLoadingBar()

def filluplists():
    total_balance_of_assets = (float(
        w3.from_wei(w3.eth.get_balance(account.address), 'ether')) * fetch_eth_price_in('USDT'))

    if loading == 1:
        main.withdraw()

    for i in range(0, len(assets_addr)):
        contract = create_contract(assets_addr[i])

        token_name_contract    = contract.functions.name()
        token_name                   = token_name_contract.call()

        token_symbol_contract  = contract.functions.symbol()
        token_symbol                 = token_symbol_contract.call()

        if os.name == 'nt':
            asset_list.insert(END, ' ' + token_name + f" ({token_symbol})\n")

        else:
            asset_list.insert(END, ' ' + token_name + f" ({token_symbol})")

        token_balance_contract = contract.functions.balanceOf(account.address)
        token_balance                = token_balance_contract.call()

        if os.name == 'nt':
            asset_list2.insert(END,  ' ' + str(w3.from_wei(token_balance, 'ether')) + '\n')

        else:
            asset_list2.insert(END,  ' ' + str(w3.from_wei(token_balance, 'ether')))

        if float(token_balance) != 0.0:
            globals()['total_balance_of_assets'] += float(w3.from_wei(token_balance, 'ether'))

        if loading == 1:
            AssetsLoadingBar.bar.step(percent(24, len(assets_addr)))

            AssetsLoadingBar.update()

    with open(assets_json, 'w') as f:
            json.dump(assets_addr, f)

filluplists()

if loading == 1:
    #AssetsLoadingBar.bar.stop()
    AssetsLoadingBar.destroy()
    main.deiconify()

assetbalframe = tk.Frame(master = asset_frame)

assetbalframe.pack(
    side = 'top',
    anchor = 'n',
    pady = 2
)

tk.Label(
    master = assetbalframe,
    text = 'Asset',
    font = 'bold 13'
).pack(side = 'left')

tk.Label(
    master = assetbalframe,
    text = '      |  ',
    font = 'bold 13'
).pack(
    side = 'left',
    ipadx = 50,
    padx = 50,
    fill = tk.Y,
    expand = True
)

tk.Label(
    master = assetbalframe,
    text = 'Balance',
    font = 'bold 13'
).pack(side = 'left')

sbar.config(command = asset_list.yview)

asset_list.pack(
    pady = 2,
    side = 'left',
    fill = tk.BOTH,
    expand = True
)

asset_list2.pack(
    pady = 2,
    side = 'right',
    fill = tk.BOTH,
    expand = True
)

newline(main, pady = 1)


anotherbtn_frame = tk.Frame(master = main)

add_coin_btn = tk.Button(
    master = anotherbtn_frame,
    text = "Add Coin",
    font = 'bold 16',
    command = coinfuncts.AddCoinWindow
)

add_coin_btn.pack(
    side = 'left',
    padx = 35
)

restore_default_coins_btn = tk.Button(
    master = anotherbtn_frame,
    text = "Restore default list",
    font = 'bold 16',
    command = coinfuncts.RestoreDefaultCrypto
)

restore_default_coins_btn.pack(
    side = 'left',
    padx = 35
)

rm_coin_btn = tk.Button(
    master = anotherbtn_frame,
    text = "Remove Coin",
    font = 'bold 16',
    command = coinfuncts.RemoveCoinWindow
)

rm_coin_btn.pack(
    side = 'right',
    padx = 35
)

anotherbtn_frame.pack()

side_button_frame.pack(
    pady = 20,
    anchor = "s",
    expand = True,
    fill = tk.Y
)

def check_balance():
    if w3.is_connected() == True:

        assets_total.config(
            text =  f"Total asset value: {total_balance_of_assets}",
            font = "10"
        )

    elif w3.is_connected() == False:
        assets_total.config(
            text = "N/A (No internet connection)",
            font = "10"
        )

    #main.after(7000, check_balance)


refresh_btn.config(command = check_balance)

check_balance()

main.mainloop()


