#!/usr/bin/env python3

"""
Copyright © 2024 Serpenseth

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#===Version2.1.0===#

import os
import os.path # os.path.exists()
import sys # restart program in Windows

from tkinter.filedialog import asksaveasfilename, askopenfilename # file-related functions
from tkinter import messagebox, ttk, PhotoImage, LabelFrame, StringVar, IntVar
#from tkinter import ttk # Combobox

import tkinter as tk # shortcut
import os.path # os.path.exists()
import json  # JSON file manipulation

import segno # QR code

from web3 import Web3 # main Web3 module
from eth_account import Account

def main():
    # BEGIN functions
    # Caused issues when included in Global.Var class
    def center_window(Y, X: int, window: tk) -> None:
        x = (window.winfo_screenwidth()  >> 1) - (Y >> 1)
        y = (window.winfo_screenheight()  >> 1) - (X  >> 1)

        window.geometry('%dx%d+%d+%d' % (Y, X, x, y))

    def newline(master, pady = 4) ->  None:
        tk.Label(
            master = master,
            text = '\n',
        ).pack(pady = pady)

    # default RPC provider
    w3 = Web3(
        Web3.HTTPProvider(
            'https://rpc.mevblocker.io',
            #'https://rpc.ankr.com/eth',
            request_kwargs = {'timeout': 4}
        )
    )

    def questionbox(self, msg) -> bool:
        self.box = messagebox.askquestion(
            master = self,
            title = "SimplEthWallet",
            message = msg,
            icon = "info"
        )

        if self.box == "yes":
            return True

        return False

    def fetchprice(From, To) -> float:
        from urllib.request import urlopen
        #https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
        import ssl

        context = ssl._create_unverified_context()

        try:
        # A MUCH better API to fetch token price
            page_data = urlopen(
                f"https://min-api.cryptocompare.com/data/price?fsym={From}&tsyms={To}",
                context = context
            ).read()

        except TypeError:
            pass

        page = page_data.decode('utf-8')
        page = page.replace(f'"{To}":', '')
        page = page[1:len(page) - 1]

        if 'Response' in page:
            return 0.0

        return float(page)

    def create_contract(address: str) -> type(w3.eth.contract):
        return w3.eth.contract(
            address = address,
            abi = globalvar.abi
        )

    def percent(percent, number) -> float:
        if number == 0 or percent == 0:
            return 0

            return (percent * number) / 100.0

    def check_balance() -> None:
        if w3.is_connected() == True:
            globalvar.assets_total.config(
                text =  f"Total asset value: {globalvar.total_balance_of_assets}",
                font = "10"
            )

        elif w3.is_connected() == False:
            globalvar.assets_total.config(
                text = "N/A (No internet connection)",
                font = "10"
            )
    # END    functions

    # Variables
    class globalvar:
        def __init__(self):
            self.dest_path = ''

            self.account = type(Account)

            if os.name == 'nt':
                self.dest_path = 'C:\\ProgramData\\SimpleEtherWallet\\'

            else:
                self.current_usr = os.getlogin()
                self.dest_path    = "/home/" + self.current_usr + "/.SimpleEtherWallet/"

            self.imgfolder = os.path.dirname(__file__) + '/images/'

            if not os.path.exists(self.imgfolder):
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

            self.abi_json_file = self.dest_path + 'abi_data.json'
            self.conf_file = self.dest_path + 'conf.json'
            self.assets_json = ''

            self.conf_file_contents = {
                'version': '3.0.0',
                'wallets': [],
                'rpc': 'https://rpc.mevblocker.io',
                'currency': 'USD',
                'theme': 'default',
            }

            # JSON abi file, used for token contracts
            if not os.path.exists(self.abi_json_file) or os.stat(self.abi_json_file).st_size == 0:
                with open(abi_json_file, 'w') as jsonfile:
                    jsonfile.write("""[{"inputs":[{"internalType":"uint256","name":"_totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"},{"internalType":"bool","name":"_isBlacklisting","type":"bool"}],"name":"blacklist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"blacklists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"limited","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxHoldingAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minHoldingAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_limited","type":"bool"},{"internalType":"address","name":"_uniswapV2Pair","type":"address"},{"internalType":"uint256","name":"_maxHoldingAmount","type":"uint256"},{"internalType":"uint256","name":"_minHoldingAmount","type":"uint256"}],"name":"setRule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]
                """)

            # Conf.json file
            if not os.path.exists(self.conf_file) or os.stat(self.conf_file).st_size == 0:
                with open(self.conf_file, 'w') as f:
                    json.dump(self.conf_file_contents, f)

            self.position = 0
            self.is_new = True
            self.nameofwallet = ''
            self.account_addr = ''
            self.filechosen = 0
            self.recovered = 0

            self.contactbook = {
                'name': [],
                'address': []
            }

            self.contactsjson = self.dest_path + 'contacts.json'

            # Balance
            self.total_balance_of_assets: float = 0.0
            # Contract-related
            self.abi = json.load(open(self.abi_json_file, 'r'))
            # Asset-related
            self.assets_json = self.dest_path + 'assets.json'
            # List of crypto to display #
            self.assets_addr = []
            # Default addresses
            self.addresses = []

            # If first run or assets_json got messed with
            if not os.path.exists(self.assets_json) or os.stat(self.assets_json).st_size == 0:
                self.addresses = [
                    # Tether USD (USDT)
                    '0xdAC17F958D2ee523a2206206994597C13D831ec7',
                    # USD Coin (USDC)
                    '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                    # DAI Stablecoin (DAI)
                    '0x6B175474E89094C44Da98b954EedeAC495271d0F',
                    # Polygon Ecosystem Token/MATIC (POL)
                    '0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6'
                ]

                with open(self.assets_json, 'w') as f:
                    json.dump(self.addresses, f)

            self.assets_addr = []

            with open(self.assets_json, 'r') as f:
                self.assets_addr = json.load(f)

            self.default_listbox_entries = [
                ' ' + 'Tether USD (USDT)',
                ' ' + 'USD Coin (USDC)',
                ' ' + 'Dai Stablecoin (DAI)',
                ' ' + 'Polygon Ecosystem Token (POL)',
            ]

    globalvar = globalvar()

    if not os.path.exists(globalvar.dest_path):
        try:
            os.mkdir(globalvar.dest_path)

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

    # Load conf.json file
    with open(globalvar.conf_file, 'r') as f:
        globalvar.conf_file_contents = json.load(f)

    # Main class
    class Master(tk.Tk):
        def __init__(self):
            super().__init__()

            self.withdraw()

            # Eth
            self.eth_img   = PhotoImage(file = globalvar.imgfolder + 'eth.png')
            # Hide pass image
            self.closed_eye = PhotoImage(file = globalvar.imgfolder+ 'icons8-eyes-24-closed.png')
            # Show pass image
            self.opened_eye = PhotoImage(file = globalvar.imgfolder + 'icons8-eyes-24.png')
            # Clipboard image
            self.clipboard = PhotoImage(file = globalvar.imgfolder + 'icons8-copy-24.png')
            # Refresh icon
            self.refresh_img = PhotoImage(file = globalvar.imgfolder + 'icons8-refresh-24.png')
            # Wallet icon
            self.change_wallet = PhotoImage(file = globalvar.imgfolder + 'icons8-wallet-50.png')
            # Address book 1
            self.address_book1 = PhotoImage(file = globalvar.imgfolder + 'icons8-open-book-50.png')
            # Address book 2
            self.address_book2 = PhotoImage(file = globalvar.imgfolder + 'icons8-open-book-24.png')
            # Send crypto icon
            self.receive_coins = PhotoImage(file = globalvar.imgfolder + 'icons8-reply-arrow-50.png')
            # Receive crypto icon
            self.send_coins = PhotoImage(file = globalvar.imgfolder + 'icons8-forward-arrow-50.png')
            # Delete contact icon
            self.delicon = PhotoImage(file = globalvar.imgfolder + 'icons8-cross-50.png')
            # Add contact icon
            self.plusicon = PhotoImage(file =  globalvar.imgfolder + 'icons8-plus-48.png')

            self.json_contents = {}
            self.first_time = True

            with open(globalvar.conf_file, 'r') as f:
                self.json_contents = json.load(f)

                if len(self.json_contents['wallets']) != 0:
                    self.first_time = False

                else:
                    self.first_time = True

    # Greeting window (main)
    class GreetingWindow(tk.Toplevel):
        def __init__(self, master):
            super().__init__()

            self.title("SimpleEtherWallet")
            self.protocol("WM_DELETE_WINDOW", quit)
            self.resizable(False, False)

    ## Greeting Window to new users ##
    class NotNewUser(tk.Toplevel):
        def __init__(self, master):
            super().__init__()

            self.withdraw()

            self = master

            if os.name == 'nt':
                center_window(720, 400, self)

            else:
                center_window(880, 400, self)

            self.ethimg = root.eth_img

            newline(self, pady = 0)

            tk.Label(
                master = self,
                text = "Welcome back! Please select a wallet ",
                font = "bold 20",
                image = self.ethimg,
                compound = 'right'
            ).pack(pady = 10)

            self.masterframe = tk.LabelFrame(
                master = self,
            )

            self.masterframe.pack(
                padx = 40,
                fill = tk.BOTH,
                expand = True,
                pady = 30
            )

            self.contents = root.json_contents
            self.wlist = []
            self.wlist = self.contents['wallets']
            self.wnames = []

            for i in range(0, len(self.wlist)):
                self.name = self.wlist[i]

                if '\\' in self.name:
                    self.start = self.name.rfind('\\') + 1
                    self.end  = len(self.name)

                    self.wnames.append(self.name[self.start:self.end])

                else:
                    self.start = self.name.rfind('/') + 1
                    self.end  = len(self.name)

                    self.wnames.append(self.name[self.start:self.end])

            self.wlist = self.wnames

            self.wbox = ttk.Combobox(
                master = self.masterframe,
                state = 'readonly',
                values = self.wlist,
                width = 30,
            )

            self.wbox.pack(
                padx = 19,
                ipady = 5,
                pady = 20
            )

            self.selectedwallet = StringVar()

            def getboxopt(event) -> None:
                self.selectedwallet.set(self.contents['wallets'][self.wbox.current()])

            self.wbox.current(0)
            self.selectedwallet.set(self.contents['wallets'][0])

            globalvar.nameofwallet = self.contents['wallets'][self.wbox.current()]

            self.wbox.bind("<<ComboboxSelected>>", getboxopt)

            self.passwdframe = tk.Frame(master = self.masterframe)

            self.btn1 = tk.Button(self.passwdframe)

            self.passentry = tk.Entry(
                self.passwdframe,
                highlightthickness = 1,
                exportselection = 0,
                width = 50,
                show = "*",
            )

            self.stat = IntVar()
            self.stat.set(1)
            self.hidepass = root.closed_eye
            self.showpass = root.opened_eye

            def unhide() -> None:
                if self.stat.get() == 1:
                    self.btn1.config(image = self.showpass)
                    self.passentry.config(show = "")

                    self.stat.set(0)

                elif self.stat.get() == 0:
                    self.btn1.config(image = self.hidepass)
                    self.passentry.config(show = "*")

                    self.stat.set(1)

            self.btn1.configure(
                image = self.hidepass,
                command = unhide
            )

            tk.Label(
                master = self.passwdframe,
                text = "Password:",
                font = 'bold 12'
            ).pack(
                side = 'left',
                padx = 2,
            )

            self.btn1.pack(
                side =  'right',
                padx = 2
            )

            self.passentry.pack(
                ipady = 5,
                padx = 10,
                side = 'right',
                pady = 4
            )

            self.passwdframe.pack(
                pady = 5,
            )

            self.capslockstat = tk.Label(
                master = self.masterframe,
                text = '',
                font = 'bold 13',
                fg = 'red'
            )

            def oncaps2(event) -> None:
                self.capslockstat.config(text = 'Caps lock is on!')

                if len(self.passentry.get()) == 0:
                    self.capslockstat.config(text = '')

            def offcaps2(event) -> None:
                self.capslockstat.config(text = '')

            self.bind( '<Lock-KeyRelease>', oncaps2)
            self.bind( '<Lock-KeyPress>',     offcaps2)

            self.capslockstat.pack(pady = 4)

            def checkpasswd(*args) -> None:
                if len(self.passentry.get()) == 0:
                    messagebox.showerror(
                        title = "Error",
                        message = "Password field is empty"
                    )

                    return

                try:
                    with open(self.selectedwallet.get(), 'r') as ff:

                        globalvar.account = Account.from_key(
                            Account.decrypt(
                                json.load(ff),
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

                self.destroy()
                UserWallet(globalvar.account.address)

            self.passentry.bind('<Return>', lambda e: checkpasswd(e))

            self.btnframe = tk.Frame(master = self.masterframe)

            self.btnquit = tk.Button(
                master = self.btnframe,
                text = 'Quit',
                font = 'bold 12',
                command = quit
            )

            self.btnquit.pack(
                ipady = 2,
                ipadx = 16,
                padx = 20,
                side = 'left'
            )

            self.btncontinue = tk.Button(
                master = self.btnframe,
                text = 'Continue',
                font = 'bold 12',
                #bd = 4,
                command = checkpasswd
            )

            self.btncontinue.pack(
                side = 'right',
                ipadx = 10,
                ipady = 3,
                padx = 10
            )

            #def createawallet(self):
                #createfile()

            self.createwalletbutton = tk.Button(
                master = self.btnframe,
                text = 'Create a wallet',
                font = 'bold 12',
                command = CreateWallet
            )

            self.createwalletbutton.pack(
                ipady = 3,
                ipadx = 10,
                side = 'left'
            )

            self.recoverwalletbutton = tk.Button(
                master = self.btnframe,
                text = 'Recover wallet',
                font = 'bold 12',
                command = RecoverAccount
            )

            self.recoverwalletbutton.pack(
                ipady = 3,
                ipadx = 10,
                side = 'left',
                padx = 4
            )

            self.btnframe.pack(
                side = 'top',
                pady = 10
            )

            self.openwalletbutton = tk.Button(
                master = self.btnframe,
                text = 'Open a wallet',
                font = 'bold 12',
                command = OpenWalletWindow
            )

            self.openwalletbutton.pack(
                ipady = 3,
                ipadx = 10,
                side = 'left',
                padx = 4
            )

    ## Greeting Window to users that aren't new ##
    class NewUser(tk.Toplevel):
        def __init__(self, master):
            super().__init__()

            self.withdraw()

            self = master

            if os.name == 'nt':
                center_window(540, 480, self)

            else:
                center_window(540, 500, self)

            tk.Label(
                master = self,
                text = "\nWelcome! ",
                font = "bold 20",
            ).pack(pady = 5)

            self.smallframe = tk.LabelFrame(master = self)

            self.smallframe.pack(
                pady = 7,
                padx = 5
            )

            self.txt = tk.Label(
                master = self.smallframe,
                text = """
 SimpleEtherWallet is a non-custodial wallet on the Ethereum blockchain. You own your crypto assets!\n
 Your private key never leaves this device. \nYour private key is encrypted.\n""",
                font = "bold 13",
                wraplength = 400,
                justify = 'center'
            )

            self.txt.pack(
                padx = 40,
                pady = 12
            )

            self.optframe = tk.LabelFrame(
                master = self
            )

            self.createwalletbutton = tk.Button(
                master = self.optframe,
                text = 'Create a wallet',
                font = 'bold 16',
                height = 2,
                command = CreateWallet
            )

            self.createwalletbutton.pack(
                fill = tk.BOTH,
                padx = 2,
            )

            self.openwalletbutton = tk.Button(
                master = self.optframe,
                text = 'Open a wallet',
                font = 'bold 16',
                height = 2,
                command = OpenWalletWindow
            )

            self.openwalletbutton.pack(
                fill = tk.BOTH,
                padx = 2,
                pady = 2,
            )

            self.importw = tk.Button(
                master = self.optframe,
                text = 'Import a wallet',
                font = 'bold 16',
                height = 2,
                command = ImportWallet
            )

            self.importw.pack(
                fill = tk.BOTH,
                padx = 2,
                pady = 2,
            )

            self.optframe.pack(
                fill = tk.BOTH,
                padx = 10
            )

    # Import wallet
    class ImportWallet(tk.Toplevel):
        def __init__(self):
            super().__init__()

            self.title("SimpleEtherWallet  -  Import wallet")
            self.resizable(False, False)
            self.protocol("WM_DELETE_WINDOW", quit)

            if os.name == 'nt':
                center_window(468, 380, self)

            else:
                center_window(500, 360, self)

            newline(self)

            tk.Label(
                master = self,
                text = '\nSelect how you want to import your wallet:\n',
                font = 'bold 14'
            ).pack(pady = 5)

            if os.name == 'nt':
                self.frm = tk.LabelFrame(
                    master = self
                )

            else:
                self.frm = tk.LabelFrame(
                    master = self
                )

            self.frm.pack(
                padx = 15,
                fill = tk.X,
                expand = True
            )

            self.radiobtnopt = IntVar()

            def filediag():
                self.openf = askopenfilename(
                    initialdir = globalvar.dest_path,
                    title = "Open Wallet",
                    defaultextension = ".sew"
                )

                if not self.openf:
                    #importwalletwindow().deiconify()
                    return

                globalvar.nameofwallet = self.openf
                globalvar.filechosen = 1
                globalvar.is_new = False

                PassBox()

            def getradioopt():
                if  self.radiobtnopt.get() == 1:
                    RecoverAccount()
                    self.destroy()

                elif self.radiobtnopt.get() == 2:
                    filediag()


            self.optsforRadiobtn = {
                'master': self.frm,
                'font': 'bold 13',
                'variable': self.radiobtnopt,
                'height': 2,
                'relief': 'raised'
            }

            self.opt1 = tk.Radiobutton(
                **self.optsforRadiobtn,
                text = 'Import from Private Key',
                value = 1,
                cursor = 'cross'
            )

            self.opt1.pack(
                expand = True,
                fill = tk.X,
                pady = 1
            )

            self.opt2 = tk.Radiobutton(
                **self.optsforRadiobtn,
                text = 'Import from a file (only supports .sew files)',
                value = 2,
                cursor = 'cross'
            )

            self.opt2.pack(
                expand = True,
                fill = tk.X,
                pady = 1
            )

            self.importbtnframe = tk.Frame(master = self)

            self.importbtnquit = tk.Button(
                master = self.importbtnframe,
                text = 'Quit',
                font = 'bold 12',
                command = quit
            )

            self.importbtnquit.pack(
                side = 'left',
                ipady = 7,
                ipadx = 14
            )

            tk.Label(
                master = self.importbtnframe,
                text = ''
            ).pack(
                padx = 10,
                side = 'left'
            )

            self.importbtnret = tk.Button(
                master = self.importbtnframe,
                text = 'Cancel',
                font = 'bold 12',
                command = lambda: [
                    self.deiconify(),
                    self.destroy()
                ]
            )

            self.importbtnret.pack(
                ipady = 7,
                side = 'left',
                ipadx = 7
            )

            self.importbtncont = tk.Button(
                master = self.importbtnframe,
                text = 'Continue',
                font = 'bold 12',
                command = lambda: [
                    self.withdraw(),
                    getradioopt()
                ]
            )

            self.importbtncont.pack(
                ipady = 7,
                side = 'right',
                padx = 12,
                ipadx = 7
            )

            self.importbtnframe.pack(pady = 8)

            newline(self, pady = 0)

    # Create wallet
    class CreateWallet(tk.Toplevel):
        def __init__(self):
            super().__init__()

            self.title("SimpleEtherWallet")
            self.protocol("WM_DELETE_WINDOW", quit)
            self.resizable(False, False)

            center_window(560,  500, self)

            self.framebox = tk.LabelFrame(
                master = self
            )

            tk.Label(
                master = self,
                text = "Create Wallet\n\nYour wallet is non-custodial,\n meaning that it is stored on your device",
                font = "bold 16",
            ).pack(pady = 20)

            tk.Label(
                master = self.framebox,
                text = "Enter desired wallet name: ",
                font = 'bold 14'
            ).pack(pady = 16)

            self.framebox.pack(
                pady = 10,
                padx = 5
            )

            self.frame = tk.Frame(master = self)

            tk.Label(
                master = self.framebox,
                text = "Wallet name:",
                font = 'bold 13'
            ).pack(
                pady = 10,
                padx = 10,
                side = "left"
            )

            self.enter = tk.Entry(
                master = self.framebox,
                width = 40,
                font = 'bold 10'
            )

            # file chooser
            def createf(*args):
                self.saveas = asksaveasfilename(
                    initialdir = globalvar.dest_path,
                    title = "Create Wallet",
                    defaultextension = ".sew"
                )

                if not self.saveas:
                    return

                globalvar.nameofwalle = self.saveas

                PassBox()
                self.destroy()

            self.btn1 = tk.Button(
                master = self.framebox,
                text = "Pick location",
                font = 'bold 12',
                command = createf
            )

            self.btn1.bind("<Return>", createf)

            self.btn1.pack(
                padx = 20,
                side = "right",
                ipady = 2
            )

            def errbox(msg):
                self.enter.delete(0, tk.END)
                messagebox.showerror(
                    title = "Error",
                    message = msg,
                    icon = "error",
                )

            # create file
            def create(*args):
                self.fname = self.enter.get()

                # empty entry field
                if len(self.fname) == 0:
                    errbox("Name cannot be empty")
                    return

                # name too long
                elif len(self.fname) > 254:
                    errbox("Wallet name cannot be longer than 255 characters")
                    return

                elif not self.fname.startswith("C:\\") or not self.fname.startswith("C:/"):
                    self.tmp = globalvar.dest_path + self.fname
                    self.fname = self.tmp

                # if directory
                if os.path.isdir(self.fname):
                    errbox("'" + self.fname + "' is a directory")
                    return

                if self.fname.find('.sew') != -1:
                    globalvar.nameofwallet = self.fname

                globalvar.nameofwallet = self.fname + ".sew"

                PassBox()
                self.destroy()

            self.enter.bind("<Return>", create)

            self.enter.pack(
                fill = tk.X,
                expand = True,
                ipady = 5,
                side = "right"
            )

            newline(self.framebox, pady = 20)

            self.capslockstat = tk.Label(
                master = self,
                text = '',
                font = '8',
                fg = 'red'
            )

            def oncaps2(event):
                self.capslockstat.config(text = 'Caps lock is on!')

            def offcaps2(event):
                self.capslockstat.config(text = '')

            self.bind( '<Lock-KeyRelease>', oncaps2)
            self.bind( '<Lock-KeyPress>',     offcaps2)

            self.capslockstat.pack(
                side = 'top',
                pady = 4
            )

            tk.Label(
                master = self,
                text = f"NOTE: If a path hasn't been specified, \nthe wallet will be saved to: {globalvar.dest_path}",
                font = 'bold 12'
            ).pack(pady = 10)

            self.frame2 = tk.Frame(master = self)

            tk.Button(
                master = self.frame2,
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
                master = self.frame2,
                text = "Return",
                font = 'bold 14',
                command  = lambda: [
                    self.destroy(),
                    #window.bind( '<Lock-KeyRelease>', oncaps),
                    #window.bind( '<Lock-KeyPress>', offcaps),
                    greetwindow.deiconify()
                ]
            ).pack(
                side = 'right',
                ipady = 7,
                ipadx = 5
            )

            tk.Button(
                master = self.frame2,
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
                master = self.frame2,
                text = ""
            ).pack(
                padx = 20,
            )

            self.frame2.pack(
                pady = 20,
                padx = 10,
                anchor = 'center'
            )

    # Recover account
    class RecoverAccount(tk.Toplevel):
        def __init__(self):
            super().__init__()

            greetwindow.withdraw()

            self.title("SimpleEtherWallet  -  Recover account")
            self.resizable(False, False)
            self.protocol("WM_DELETE_WINDOW", quit)

            globalvar.is_new = False

            if os.name == 'nt':
                center_window(560, 420, self)

            else:
                center_window(620, 420, self)

            self.wframe = LabelFrame(
                master = self
            )

            newline(self, pady = 0)

            tk.Label(
                master = self,
                text = "Recover your account ",
                image = root.eth_img,
                compound = 'right',
                font = "bold 18"
            ).pack(
                pady = 20,
                anchor = "center"
            )

            tk.Label(
                master = self.wframe,
                text = "Your private key holds access to your crypto assets.\nKeep this key as safe as possible",
                font = 'bold 14'
            ).pack(pady = 10)

            tk.Label(
                master = self.wframe,
                text = "Enter your private key: ",
                font = "bold 12"
            ).pack(
                pady = 5,
                anchor = "center"
            )

            self.pentry = StringVar()

            self.private_key_recover = tk.Entry(
                master  = self.wframe,
                font = 'bold 10',
                width = 64,
                textvariable = self.pentry
            )

            def ch(event):
                self.pentry.set(self.pentry.get()[:66])

            self.private_key_recover.bind("<KeyRelease>", ch)

            self.private_key_recover.pack(
                padx = 30,
                pady = 20,
                ipady = 5
            )

            self.wframe.pack(
                padx = 10,
                pady = 10
            )

            def continue_or_not(*args):
                if len(self.private_key_recover.get()) < 48:
                    messagebox.showerror(
                        title = "Error",
                        message = "Invalid private key",
                        icon = "error",
                    )

                    self.private_key_recover.delete(0, tk.END)
                    return


                elif len(self.private_key_recover.get()) == 0:
                    messagebox.showerror(
                        title = "Error",
                        message = "Private key cannot be empty",
                        icon = "error",
                    )

                    self.private_key_recover.delete(0, tk.END)
                    return

                else:
                    try:
                        globalvar.account = Account.from_key(self.private_key_recover.get())
                        globalvar.recovered = 1

                    except Exception:
                        messagebox.showerror(
                            title = "Error",
                            message = "Invalid private key",
                            icon = "error",
                        )

                        self.private_key_recover.delete(0, tk.END)
                        return

                    self.destroy()
                    CreateWallet()

            self.frame2 = tk.Frame(master = self)

            self.btn =  tk.Button(
                master = self.frame2,
                text = "Continue",
                font = 'bold 14',
                command = continue_or_not
            )

            self.private_key_recover.bind("<Return>", continue_or_not)

            self.btn2 = tk.Button(
                master = self.frame2,
                text = 'Return',
                font = 'bold 14',
                command = lambda: \
                [
                    self.destroy(),
                    greetwindow.deiconify()
                ]
            )

            self.btn3 = tk.Button(
                master= self.frame2,
                text = 'Quit',
                font = 'bold 14',
                command = quit
            )

            self.btn3.pack(
                ipady = 7,
                ipadx = 7,
                padx = 40,
                side = 'left',
                anchor = 's'
            )

            self.btn2.pack(
                anchor = 's',
                side = "left",
                padx = 7,
                ipady = 7,
                ipadx = 7,
            )

            self.btn.pack(
                anchor = "s",
                ipady = 7,
                ipadx = 7,
            )

            self.frame2.pack(pady = 10)

    # Open Wallet window
    class OpenWalletWindow(tk.Toplevel):
        def __init__(self):
            super().__init__()

            self.title("SimpleEtherWallet")
            self.protocol("WM_DELETE_WINDOW", quit)
            self.resizable(False, False)

            center_window(550, 350, self)

            def errbox(self, msg) -> None:
                self.entry.delete(0, tk.END)

                messagebox.showerror(
                    title = "Error",
                    message = msg,
                    icon = "error",
                )

            # open existing wallet (manual)
            def openwallet(*args) -> None:
                self.fname = self.entry.get()

                # empty entry field
                if len(self.fname) == 0:
                    errbox(self, "Name cannot be empty")
                    return

                # name too long
                elif len(self.fname) > 254:
                        errbox(self, "Wallet name cannot be longer than 255 characters")
                        return

                    # if directory
                if os.path.isdir(self.fname):
                    errbox(f"{self.fname} is a directory")
                    return

                if self.fname.startswith("C:/") or self.fname.startswith("C:\\"):
                    if ".sew" in self.fname:
                        if not os.path.exists(self.fname):
                            errbox(self,"Wallet not found")
                            return

                    else:
                        if not os.path.exists(self.fname + ".sew"):
                            errbox(self, "Wallet not found")
                            return


                elif not self.fname.startswith("C:/") or self.fname.startswith("C:\\"):
                    self.tmp = globalvar.dest_path + self.fname
                    self.fname = self.tmp

                    if ".sew" in self.fname:
                        if not os.path.exists(self.fname):
                            errbox(self, "Wallet not found")
                            return

                    else:
                        if not os.path.exists(self.fname + ".sew"):
                            errbox(self, "Wallet not found")
                            return

                if not ".sew" in self.fname:
                    globalvar.nameofwallet = self.fname + ".sew"

                else:
                    globalvar.nameofwallet = self.fname

                self.destroy()
                PassBox()

            self.title("SimpleEtherWallet")
            self.protocol("WM_DELETE_WINDOW", quit)
            self.resizable(False, False)

            center_window(550, 350, self)

            self.eth_img = root.eth_img

            tk.Label(
                master = self,
                text = 'Welcome! ',
                font = 'bold 22',
                image = self.eth_img,
                compound = 'right'
            ).pack(pady = 26)

            self.frame1 = tk.LabelFrame(
                master = self
            )

            tk.Label(
                master = self.frame1,
                text = "Enter your wallet's name or click choose to select wallet\n",
                font = '12'
            ).pack(
                padx = 10,
                pady = 15
            )

            self.frame1.pack(
                fill = tk.BOTH,
                padx = 14
            )

            self.frame2 = tk.Frame(master = self.frame1)

            # open file
            def openfile() -> None:
                self.openf = askopenfilename(
                    initialdir = globalvar.dest_path,
                    title = "Open Wallet",
                    defaultextension = ".sew"
                )

                if not self.openf:
                    if os.name == 'nt':
                        self.lift()
                    #importwalletwindow().deiconify()
                    return

                globalvar.nameofwallet = self.openf
                globalvar.filechosen = 1
                globalvar.is_new = False

                PassBox()

            tk.Button(
                master = self.frame2,
                text = "Choose...",
                font = 'bold 12',
                width = 10,
                command = lambda: [
                    openfile(),
                    #self.withdraw()
                ]
            ).pack(
                padx = 8,
                side = 'right',
                ipady = 4
            )

            tk.Label(
                master = self.frame2,
                text = "Wallet:",
                font = 'bold 12'
            ).pack(side = 'left')

            self.entry = tk.Entry(
                self.frame2,
                width = 45,
                font = 'bold 12'
            )

            self.entry.bind(
                "<Return>",
                openwallet
            )

            self.entry.pack(
                side = 'right',
                ipady = 5
            )

            self.frame2.pack(anchor = 'center')

            globalvar.is_new = False;

            self.frame4 = tk.Frame(self.frame1)
            self.capslockstatus = tk.Label(master = self.frame4)

            tk.Button(
                master = self.frame4,
                text = "Quit",
                font = 'bold 12',
                width = 5,
                command = quit
            ).pack(
                padx = 10,
                ipady = 3,
                ipadx = 5,
                side = 'left'
            )

            tk.Button(
                master = self.frame4,
                text = 'Continue',
                font = 'bold 12',
                width = 8,
                command = openwallet
            ).pack(
                padx = 3,
                ipady = 3,
                ipadx = 5,
                side = 'right'
            )

            tk.Button(
                master = self.frame4,
                text = 'Return',
                font = 'bold 12',
                width = 7,
                command = lambda: \
                [
                    #self.deiconify(),
                    self.destroy()
                ]
            ).pack(
                side = 'right',
                padx = 3,
                ipady = 3,
                ipadx = 5
            )

            def oncaps(event) -> None:
                self.capslockstatus.config(
                    text = 'Caps lock is on!',
                    fg = 'red',
                    font = 'bold 14'
                )

            def offcaps(event) -> None:
                self.capslockstatus.config(text = '')

            self.bind( '<Lock-KeyRelease>', oncaps)
            self.bind( '<Lock-KeyPress>',     offcaps)

            self.frame1.bind( '<Lock-KeyRelease>', oncaps)
            self.frame1.bind( '<Lock-KeyPress>',     offcaps)

            self.capslockstatus.pack(
                pady = 4,
                padx = 4
            )

            tk.Label(
                master = self.frame1,
                text = ''
            ).pack(ipady = 2)

            self.frame4.pack(pady = 18)

    # Passbox window
    # BEGIN class PassBox
    class PassBox(tk.Toplevel):
        def __init__ (self):
            super().__init__()

            self.title("SimpleEtherWallet")
            self.protocol("WM_DELETE_WINDOW", quit)
            self.resizable(False, False)

            if globalvar.is_new == False:
                center_window(580, 240, self)

            else:
                if os.name != 'nt':
                    center_window(680, 480, self)

                else:
                    center_window(540, 480, self)


            self.opt1 = IntVar()
            self.opt1.set(1)

            self.opt2 = IntVar()
            self.opt2.set(1)

            # BEGIN def unhide1() and unhide2() function
            def unhide1():
                if self.opt1.get() == 1:
                    self.btn1.config(image = root.opened_eye)
                    self.passentry.config(show = "")

                    self.opt1.set(0)

                elif self.opt1.get() == 0:
                    self.btn1.config(image = root.closed_eye)
                    self. passentry.config(show = "*")

                    self.opt1.set(1)

            if globalvar.is_new == True:
                def unhide2():
                    if self.opt2.get() == 1:
                        self.btn2.config(image = root.opened_eye)
                        self.passentry2.config(show = "")

                        self.opt2.set(0)

                    elif self.opt2.get() == 0:
                        self.btn2.config(image = root.closed_eye)
                        self.passentry2.config(show = "*")

                        self.opt2.set(1)
            # END

            self.l = tk.Label(master = self)

            self.l.pack(
                padx = 15,
                pady = 22
            )

            if globalvar.is_new == True:
                self.smallframe = tk.LabelFrame(
                    master = self,
                    #bd = 4
                )

                self.l.config(
                    text = "Create Wallet ",
                    font = "bold 16",
                    image = root.eth_img,
                    compound = 'right'
                )

                tk.Label(
                    master = self.smallframe,
                    text = """This password is used to encrypt your wallet.\n
    The password does not leave your device.\n
    If you forget your password, you can only recover \nyour wallet with your Private Key.""",
                    font = 'bold 12'
                ).pack(
                    fill = tk.Y,
                    expand = True
                )

                self.smallframe.pack(
                    padx = 20,
                    fill = tk.BOTH,
                    expand = True
                )

            else:
                self.wname = ''

                if '\\' in globalvar.nameofwallet:
                    self.start = globalvar.nameofwallet.rfind('\\') + 1
                    self.end  = len(globalvar.nameofwallet)

                    self.wname = globalvar.nameofwallet[self.start:self.end]

                else:
                    self.start = globalvar.nameofwallet.rfind('/') + 1
                    self.end  = len(globalvar.nameofwallet)

                    self.wname = globalvar.nameofwallet[self.start:self.end]

                self.l.config(
                    text =  self.wname,
                    font = 'bold 16'
                )

            if globalvar.is_new == False:
                self.mframe = tk.LabelFrame(
                    master = self
                )

            else:
                self.mframe = tk.Frame(master = self)

            self.btn1 = tk.Button(
                self.mframe,
                image = root.closed_eye,
                command = unhide1
            )

            self.passentry = tk.Entry(
                self.mframe,
                highlightthickness = 1,
                exportselection = 0,
                width = 40,
                show = "*"
            )

            self.btn1.pack(
                side = "right",
                padx = 10,
            )

            tk.Label(
                master = self.mframe,
                text = "Enter your password:",
                font = 'bold 13'
            ).pack(side = 'left')

            self.passentry.pack(
                ipady = 5,
                side = 'right'
            )

            if globalvar.is_new == True:
                self.mframe2 = tk.Frame(master = self)

                self.passentry2  = tk.Entry(
                    master = self.mframe2,
                    exportselection = 0,
                    highlightthickness = 1,
                    width = 40,
                    show = "*"
                )


                self.btn2 = tk.Button(
                    self.mframe2,
                    image = root.closed_eye,
                    command = unhide2
                )

                self.btn2.pack(
                    side = "right",
                    padx = 10
                )

                if os.name != 'nt':
                    tk.Label(
                        master = self.mframe2,
                        text = "Repeat the password:",
                        font = 'bold 13'
                    ).pack(side = 'left')

                else:
                    tk.Label(
                        master = self.mframe2,
                        text = "Repeat the password: ",
                        font = 'bold 13'
                    ).pack(side = 'left')

                self.passentry2.pack(
                    side = 'bottom',
                    ipady = 5
                )

            self.mframe.pack(
                pady = 10,
                padx = 20
            )

            if globalvar.is_new == True:
                self.mframe2.pack(
                    pady = 2,
                    anchor = 's',
                    padx = 20
                )

            newline(self.mframe)

            def issame(*args):
                if globalvar.is_new == True:
                    if self.passentry.get() != self.passentry2.get():
                        messagebox.showerror(
                            title = "Error",
                            message = "Passwords did not match",
                            icon = "error",
                        )

                        self.passentry.delete(0, tk.END)
                        self.passentry2.delete(0, tk.END)
                        return

                    elif len(self.passentry.get()) == 0 and len(self.passentry2.get()) == 0:
                        messagebox.showerror(
                            title = "Error",
                            message = "Password field is empty",
                            icon = "error",
                        )

                        self.passentry.delete(0, tk.END)
                        self.passentry2.delete(0, tk.END)
                        return

                else:
                    if len(self.passentry.get()) == 0:
                        messagebox.showerror(
                            title = "Error",
                            message = "Password field is empty",
                            icon = "error",
                        )

                        self.passentry.delete(0, tk.END)
                        return

                if globalvar.is_new == True:
                    if globalvar.recovered == 0:
                        globalvar.account = Account.create()

                    self.encrypted = Account.encrypt(
                        globalvar.account.key,
                        password = self.passentry.get()
                    )

                    with open(globalvar.conf_file, 'w') as ff:
                        if not globalvar.nameofwallet in globalvar.conf_file_contents['wallets']:
                            globalvar.conf_file_contents['wallets'].append(globalvar.nameofwallet)

                        json.dump(globalvar.conf_file_contents, ff)

                        with open(globalvar.nameofwallet, "w") as f:
                            f.write(json.dumps(self.encrypted))

                else:
                    if globalvar.recovered == 1:
                        self.encrypted = Account.encrypt(
                            globalvar.account.key,
                            password = self.passentry.get()
                        )

                        with open(globalvar.conf_file, 'w') as ff:
                            if not globalvar.nameofwallet in globalvar.conf_file_contents['wallets']:
                                globalvar.conf_file_contents['wallets'].append(globalvar.nameofwallet)

                            json.dump(globalvar.conf_file_contents, ff)

                            with open(globalvar.nameofwallet, "w") as f:
                                f.write(json.dumps(self.encrypted))

                    if globalvar.recovered == 0:
                        try:
                            with open(globalvar.nameofwallet, "r") as f:
                                globalvar.account = Account.from_key(
                                    Account.decrypt(
                                        json.load(f),
                                        password = self.passentry.get()
                                    )
                                )

                                with open(globalvar.conf_file, 'w') as ff:
                                    if not globalvar.nameofwallet in globalvar.conf_file_contents['wallets']:
                                        globalvar.conf_file_contents['wallets'].append(globalvar.nameofwallet)

                                    json.dump(globalvar.conf_file_contents, ff)

                        except ValueError:
                            messagebox.showerror(
                                title = "Error",
                                message = "Incorrect password. Try again"
                            )

                            self.passentry.delete(0, tk.END)
                            return

                self.destroy()
                greetwindow.destroy()
                UserWallet(globalvar.account.address)


            self.endframe = tk.Frame(master = self)

            tk.Button(
                master = self.endframe,
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
                master = self.endframe,
                text = 'Return',
                font = 'bold 12',
                command = lambda: \
                [
                    self.destroy(),
                    greetwindow.deiconify()
                ]
            ).pack(
                side = "left",
                padx = 10,
                ipady = 7,
                ipadx = 5
            )

            tk.Button(
                master = self.endframe,
                text = "Continue",
                font = 'bold 12',
                command = issame
            ).pack(
                ipady = 7,
                ipadx = 5
            )

            self.endframe.pack(pady = 20)
    # END class PassBox

    # Menu items
    class MenuItem:
        # Image links
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
                    font = 'Serif 11',
                    wrap = 'word',
                    height = 20,
                )

                self.textbox.insert(
                    tk.END,
                    "Copy icon by Icons8: https://icons8.com/icon/86236/copy\n"
                )

                self.textbox.insert(
                    tk.END,
                    "Cross icon by Icons8: https://icons8.com/icon/42223/cancel\n"
                )

                self.textbox.insert(
                    tk.END,
                    "Plus icon by Icons8: https://icons8.com/icon/42232/plus\n"
                )

                self.textbox.insert(
                    tk.END,
                    "Eye icon by Icons8: https://icons8.com/icon/7tg2iJatDNzj/eyes\n"
                )

                self.textbox.insert(
                    tk.END,
                    "Eye with line icon by Icons8: https://icons8.com/icon/oZFC4NAoTr5c/eyes\n"
                )

                self.textbox.insert(
                    tk.END,
                    "Open book icon by Icons8: https://icons8.com/icon/tgZbSpOhzqyY/open-book\n"
                )

                self.textbox.insert(
                    tk.END,
                    "Forward arrow icon by Icons8: https://icons8.com/icon/117017/forward-arrow\n"
                )

                self.textbox.insert(
                    tk.END,
                    "Back arrow icon by Icons8: https://icons8.com/icon/117018/reply-arrow\n"
                )

                self.textbox.insert(
                    tk.END,
                    "Refresh icon by Icons8: https://icons8.com/icon/42259/refresh\n"
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
                self.title("SimpleEtherWallet  -  License")
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
                    wrap = 'word',
                )

                with open(
                    os.path.dirname(__file__) + '/LICENSE.txt', 'r',
                    encoding = 'utf-8'
                ) as f:
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
                    wrap = 'word',
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

                self.passwdframe = tk.Frame(master = self)
                self.passwdframe.pack()

                self.btn1 = tk.Button(self.passwdframe)

                self.btn1.pack(
                    side =  'right',
                    padx = 2
                )

                self.passentry = tk.Entry(
                    self.passwdframe,
                    highlightthickness = 1,
                    exportselection = 0,
                    width = 50,
                    show = "*",
                )

                self.stat = IntVar()
                self.stat.set(1)

                def unhide():
                    if self.stat.get() == 1:
                        self.btn1.config(image = root.opened_eye)
                        self.passentry.config(show = "")

                        self.stat.set(0)

                    elif stat.get() == 0:
                        btn1.config(image = root.closed_eye)
                        self.passentry.config(show = "*")

                        stat.set(1)

                self.btn1.configure(
                    image = root.closed_eye,
                    command = unhide
                )

                tk.Label(
                    master = self.passwdframe,
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

                self.passwdframe.pack(
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
                            center_window(540, 520, self)

                        else:
                            center_window(600, 520, self)

                        tk.Label(
                            master = self,
                            text = '\nKeep your private key safe!',
                            font = 'bold 22'
                        ).pack(pady = 10)

                        self.qrcode = segno.make_qr(globalvar.account.address)
                        self.qrcode.save(
                            "p.png",
                            scale = 8,
                            border = 1
                        )

                        self.f_img = type(PhotoImage)
                        self.f_img =  PhotoImage(file = "p.png")

                        ttk.Label(
                            master = self,
                            image = self.f_img,
                            relief = 'groove',
                        ).pack(pady = 10)

                        self.pkey = StringVar()

                        self.t = tk.Entry(
                            master = self,
                            exportselection = False,
                            highlightthickness = 0,
                            font = 'bold 12',
                            relief = 'flat',
                            width = 68,
                            textvariable = self.pkey
                        )

                        self.pkey.set(globalvar.account.address)
                        self.t.pack(
                            pady = 20,
                            ipady = 4,
                            padx = 70
                        )

                        self.t.configure(state = 'readonly')

                        self.frm = tk.Frame(master = self)
                        self.frm.pack(pady = 5)

                        tk.Label(
                            master = self.frm,
                            text = '',
                        ).pack(
                            side = 'left',
                           # ipadx = 50
                        )

                        tk.Button(
                            master = self.frm,
                            text = 'Close',
                            font = 'bold 12',
                            command = self.destroy
                        ).pack(
                            ipadx = 12,
                            ipady = 7,
                            side = 'left',
                            padx = 30
                        )

                        tk.Button(
                            master = self.frm,
                            text = "Copy Address",
                            font = 'bold 12',
                            image = root.clipboard,
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
                        with open(globalvar.nameofwallet, 'r') as f:
                            self.useless = Account.from_key(
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
                    master = self
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
                    image = root.clipboard,
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

    # User Wallet
    class UserWallet(tk.Toplevel):
        def __init__(self, wallet_address):
            super().__init__()

            self.address = wallet_address

            # If first run or assets_json got messed with
            if not os.path.exists(globalvar.assets_json) or os.stat(globalvar.assets_json).st_size == 0:
                self.assetsnames = [
                    # Tether USD (USDT)
                    '0xdAC17F958D2ee523a2206206994597C13D831ec7',

                    # USD Coin (USDC)
                    '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',

                    # DAI Stablecoin (DAI)
                    '0x6B175474E89094C44Da98b954EedeAC495271d0F',

                    # Polygon Ecosystem Token/MATIC (POL)
                    '0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6'
                ]

                with open(globalvar.assets_json, 'w') as f:
                    json.dump(self.assetsnames, f)

            with open(globalvar.assets_json, 'r') as f:
                globalvar.assets_addr = json.load(f)

            self.default_listbox_entries = [
                ' ' + 'Tether USD (USDT)',
                ' ' + 'USD Coin (USDC)',
                ' ' + 'Dai Stablecoin (DAI)',
                ' ' + 'Polygon Ecosystem Token (POL)',
            ]

            total_balance_of_assets = (float(
                w3.from_wei(w3.eth.get_balance(self.address), 'ether')) * fetchprice('ETH', 'USDT'))

            self.title("SimpleEtherWallet")
            self.protocol("WM_DELETE_WINDOW", quit)
            self.resizable(False, False)

            center_window(700, 600, self)

            self.aboutbar = tk.Menu(master = self)

            self.aboutbar_opts = tk.Menu(
                master = self.aboutbar,
                tearoff = 0
            )

            self.aboutbar_opts.add_command(
                label = 'License',
                command = MenuItem.License
            )


            self.aboutbar_opts.add_command(
                label = 'Images',
                command = MenuItem.ImageLinks
            )

            self.aboutbar_opts.add_separator()

            self.aboutbar_opts.add_command(
                label = 'Show Private Key',
                command = MenuItem.ShowRecoveryKey
            )

            self.aboutbar_opts.add_separator()

            self.aboutbar_opts.add_command(
                label = 'Donate',
                command = MenuItem.DonateEther
            )

            self.aboutbar_opts.add_separator()

            self.aboutbar_opts.add_command(
                label = 'What is SimpleEtherWallet?',
                command = MenuItem.AboutWallet
            )

            self.aboutbar.add_cascade(
                label = 'Menu',
                font = 'bold 12',
                menu = self.aboutbar_opts
            )

            self.config(menu = self.aboutbar)

            if not os.path.exists(globalvar.contactsjson) or \
                os.stat(globalvar.contactsjson).st_size == 0:
                    with open(globalvar.contactsjson, 'w') as f:
                        json.dump(globalvar.contactbook, f)

            else:
                with open(globalvar.contactsjson, 'r') as f:
                    n = json.load(f)

                    globalvar.contactbook['name']     = n['name']
                    globalvar.contactbook['address'] = n['address']

            self.side_button_frame = tk.Frame(master = self)

            self.frame_button_opts = {
                "master": self.side_button_frame,
                "image": None,
                "compound": "top",
                "height": 61,
                "width":  2,
                "relief": "flat",
                "padx": 55
            }

            # send
            self.side_button1 = tk.Button(**self.frame_button_opts)

            def callsendwindow():
                SendCryptoWindow(self)

            self.side_button1.config(
                image = root.send_coins,
                text = "Send",
                command = callsendwindow
            )

            self.side_button1.pack(
                anchor = "s",
                side = "left"
            )

            # receive
            self.side_button2 = tk.Button(**self.frame_button_opts)

            self.side_button2.config(
                image = root.receive_coins,
                text = "Receive",
                command = QrWindow
            )

            self.side_button2.pack(
                anchor = "s",
                side = "left"
            )

            # address book
            self.side_button3 = tk.Button(**self.frame_button_opts)

            self.side_button3.config(
                image = root.address_book1,
                text = "Address Book",
                command = AddressBook
            )

            self.side_button3.pack(
                anchor = "s",
                side = "left"
            )

            """ History attempt was side_button4
                I will work on it in the future """

            # change wallet
            self.side_button5 = tk.Button(**self.frame_button_opts)

            if os.name == 'nt':
                self.side_button5.config(
                    image = root.change_wallet,
                    text = "Change Wallet",
                    command = lambda: \
                    [
                        self.destroy(),
                        os.execv(sys.executable, ['py'] + sys.argv)
                    ]
                )

            else:
                self.side_button5.config(
                    image = root.change_wallet,
                    text = "Change Wallet",
                )

            self.side_button5.pack(
                anchor = "s",
                side = "left"
            )

            """ RPC label coming in an update """

            self.middle = tk.Frame(master = self)

            self.assets_total = tk.Label(master = self.middle)

            w3.eth.default_account = self.address

            self.middle.pack(anchor = "center")

            self.refresh_btn = tk.Button(
                master = self.middle,
                relief = "flat",
                image = root.refresh_img
            )

            self.refresh_btn.pack(
                padx = 10,
                side = "right"
            )

            self.assets_total.pack(
                anchor = "center",
                pady = 8,
                fill = tk.Y,
                expand = True
            )

            #newline(self)

            self.asset_frame = tk.LabelFrame(
                master = self
            )

            self.asset_frame.pack(
                fill = tk.BOTH,
                expand = True,
                padx = 25,
                pady = 20
            )

            self.sbar = tk.Scrollbar(
                self.asset_frame,
                repeatdelay = 1
            )

            self.sbar.pack(
                side = 'right',
                fill = tk.Y
            )

            self.asset_list = tk.Listbox(
                master = self.asset_frame,
                font = 'bold 13'
            )

            self.asset_list2 = tk.Listbox(
                master = self.asset_frame,
                font = 'bold 13'
            )

            def stop_click_highlight_underscore(event):
                return 'break'

            self.asset_list.bind('<Button-1>',  stop_click_highlight_underscore)
            self.asset_list.bind('<Motion>', stop_click_highlight_underscore)
            self.asset_list.bind('<Leave>', stop_click_highlight_underscore)

            self.asset_list2.bind('<Button-1>',  stop_click_highlight_underscore)
            self.asset_list2.bind('<Motion>', stop_click_highlight_underscore)
            self.asset_list2.bind('<Leave>', stop_click_highlight_underscore)

            # ETH
            if os.name == 'nt':
                self.asset_list.insert('end', ' Ether (ETH)\n')

            else:
                self.asset_list.insert('end', ' Ether (ETH)')

            self.asset_list2.insert('end', ' ' + str(w3.from_wei(w3.eth.get_balance(self.address), 'ether')))

            globalvar.total_balance_of_assets = (
                float(w3.from_wei(w3.eth.get_balance(self.address), 'ether')) * fetchprice('ETH', 'USDT'))

            AssetLoadingBar(self)
            self.assetbalframe = tk.Frame(master = self.asset_frame)

            self.assetbalframe.pack(
                side = 'top',
                anchor = 'n',
                pady = 2
            )

            tk.Label(
                master = self.assetbalframe,
                text = 'Asset',
                font = 'bold 13'
            ).pack(side = 'left')

            tk.Label(
                master = self.assetbalframe,
                text = '       |   ',
                font = 'bold 13'
            ).pack(
                side = 'left',
                ipadx = 50,
                padx = 50,
                fill = tk.Y,
                expand = True
            )

            tk.Label(
                master = self.assetbalframe,
                text = 'Balance',
                font = 'bold 13'
            ).pack(side = 'left')

            self.sbar.config(command = self.asset_list.yview)

            self.asset_list.pack(
                pady = 2,
                side = 'left',
                fill = tk.BOTH,
                expand = True
            )

            self.asset_list2.pack(
                pady = 2,
                side = 'right',
                fill = tk.BOTH,
                expand = True
            )

            self.anotherbtn_frame = tk.Frame(master = self)

            def calladdcoinwindow():
                AddCoinWindow(self)

            self.add_coin_btn = tk.Button(
                master = self.anotherbtn_frame,
                text = "Add Coin",
                font = 'bold 14',
                command = calladdcoinwindow
            )

            self.add_coin_btn.pack(
                side = 'left',
                padx = 35,
            )

            def callrestorecoinwindow():
                RestoreDefaultCrypto(self)

            self.restore_default_coins_btn = tk.Button(
                master = self.anotherbtn_frame,
                text = "Restore default list",
                font = 'bold 16',
                command = callrestorecoinwindow
            )

            self.restore_default_coins_btn.pack(
                side = 'left',
                padx = 35
            )

            def calldelcoinwindow():
                DeleteCoinWindow(self)

            self.rm_coin_btn = tk.Button(
                master = self.anotherbtn_frame,
                text = "Remove Coin",
                font = 'bold 14',
               command = calldelcoinwindow
            )

            self.rm_coin_btn.pack(
                side = 'right',
                padx = 35
            )

            self.anotherbtn_frame.pack()

            self.side_button_frame.pack(
                pady = 20,
                side = 'bottom',
            )

            def check_balance():
                if w3.is_connected() == True:
                    self.assets_total.config(
                        text =  f"Total asset value: {globalvar.total_balance_of_assets}",
                        font = "10"
                    )

                elif w3.is_connected() == False:
                    self.assets_total.config(
                        text = "N/A (No internet connection)",
                        font = "10"
                    )

            self.refresh_btn.config(command = check_balance)

            check_balance()

    # Loading bar after typing password
    class AssetLoadingBar(tk.Toplevel):
        def __init__ (self, master):
            super().__init__()

            master.withdraw()

            self.protocol("WM_DELETE_WINDOW", quit)
            self.resizable(False, False)
            self.title('SimpleEtherWallet  -  Loading...')

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
                maximum = len(globalvar.assets_addr)
            )

            self.bar.pack(
                pady = 16
            )

            for i in range(0, len(globalvar.assets_addr)):
                contract = create_contract(globalvar.assets_addr[i])

                token_name    = contract.functions.name().call()
                token_symbol  = contract.functions.symbol().call()

                if os.name == 'nt':
                    master.asset_list.insert(
                        'end', ' ' + token_name + f" ({token_symbol})\n"
                    )

                else:
                    master.asset_list.insert(
                        'end', ' ' + token_name + f" ({token_symbol})"
                    )

                token_balance = contract.functions.balanceOf(master.address).call()

                if os.name == 'nt':
                        master.asset_list2.insert('end',  ' ' + str(w3.from_wei(token_balance, 'ether')) + '\n')

                else:
                    master.asset_list2.insert('end',  ' ' + str(w3.from_wei(token_balance, 'ether')))

                self.bar.step(percent(24, len(globalvar.assets_addr)))

                self.update()

                if float(token_balance) != 0.0:
                    globalvar.total_balance_of_assets += float(w3.from_wei(token_balance, 'ether'))

            with open(globalvar.assets_json, 'w') as f:
                    json.dump(globalvar.assets_addr, f)

            self.destroy()
            master.deiconify()

    # Address book
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
            self.clist = tk.Listbox(**self.boxconf)

            def noselect(event):
                return 'break'

            self.clist.bind('<Button-1>',  noselect)
            self.clist.bind('<Motion>', noselect)
            self.clist.bind('<Leave>', noselect)

            self.clist.bind('<Button-1>',  noselect)
            self.clist.bind('<Motion>', noselect)
            self.clist.bind('<Leave>', noselect)

            self.clist.insert('end', *globalvar.contactbook['name'])
            self.clist.pack(
                side = 'left',
                fill = tk.BOTH,
                expand = True
            )

            # Contact addresses
            self.clist2 = tk.Listbox(**self.boxconf)

            self.clist2.bind('<Button-1>',  noselect)
            self.clist2.bind('<Motion>', noselect)
            self.clist2.bind('<Leave>', noselect)

            self.clist2.bind('<Button-1>',  noselect)
            self.clist2.bind('<Motion>', noselect)
            self.clist2.bind('<Leave>', noselect)

            self.clist2.insert('end', *globalvar.contactbook['address'])
            self.clist2.pack(
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
                text = 'Close',
                font = 'bold 16',
                command = self.destroy
            ).pack(
                side = 'left',
                padx = 20,
                ipady = 7,
                ipadx = 11
            )

            # Remove contact button
            self.deletec = tk.Button(
                master = self.buttonframe,
                image = root.delicon,
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
                image = root.plusicon,
                width = 62,
                command = AddContact
            )

            self.addc.pack(
                side = 'left',
                padx = 20,
                ipadx = 11
            )

    # Add contact
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
                            AddressBook.clist.insert('end', *globalvar.contactbook['name'])

                            AddressBook.clist2.delete(0, tk.END)
                            AddressBook.clist2.insert('end', *globalvar.contactbook['address'])

                    self.destroy()


            tk.Label(
                master = self,
                text = '\nEnter a name for your contact. All characters are accepted\nContacts are stored on this device',
                font = 'font 12'
            ).pack(pady = 20)

            # Contact Name
            self.frm = tk.LabelFrame(
                master = self
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

    # Delete contact
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
                master = self
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

            self.alist.insert('end', *globalvar.contactbook['name'])

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

    # QR code window
    class QrWindow(tk.Toplevel):
        def __init__(self):
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

            self.qrcode = segno.make_qr(globalvar.account.address)
            self.qrcode.save(
                "p.png",
                scale = 8,
                border = 1
            )

            self.f_img = {"image": PhotoImage(file = "p.png")}

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

            self.f = LabelFrame(
                master = self,
            )

            tk.Label(
                master = self.f,
                image = self.f_img["image"],
                compound = 'top'
            ).pack()

            self.f.pack(pady = 15)

            self.usr_addr = StringVar()
            self.usr_addr.set(globalvar.account.address)

            if os.name != 'nt':
                lbl = tk.Entry(
                    master = self,
                    textvariable = self.usr_addr,
                    state = "readonly",
                    relief = "flat",
                    font = "14",
                    highlightthickness = 0,
                    width = 43
                )

            else:
                self.lbl = tk.Entry(
                    master = self,
                    textvariable = self.usr_addr,
                    state = "readonly",
                    relief = "flat",
                    font = "10",
                    highlightthickness = 0,
                    width = 43
                )

            self.lbl.pack(
                anchor = "center",
                padx = 10,
                pady = 15
            )

            self.frame = tk.Frame(master = self)

            tk.Button(
                master = self.frame,
                text = "Copy Address",
                font = 'bold 12',
                image = root.clipboard,
                compound = "left",
                command = lambda: \
                [
                    self.clipboard_clear(),
                    self.clipboard_append(globalvar.account.address),

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
                master = self.frame,
                text = "Close",
                font = 'bold 12',
                width = 7,
                command = self.destroy
            ).pack(
                side = "right",
                pady = 18,
                ipady = 7
            )

            self.frame.pack()

            try:
                os.remove("p.png")

            except Exception:
                pass

    # Add coin
    class AddCoinWindow(tk.Toplevel):
        def __init__(self, master):
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

            def errb():
                self.errbox = messagebox.showerror(
                    master = self,
                    title = "Error",
                    message = "The address that you have provided is either a wallet address, an invalid token address, or a token that isn't listed on centralized exhanges",
                    icon = "error"
                )

                if os.name == 'nt':
                    self.lift()

                self.addressvar.set('')

            def get_data(event):
                if len(self.addressvar.get()) == 0 or len(self.addressvar.get()) < 42:
                    pass

                elif not w3.is_address(self.addressvar.get()):
                    errb()
                    self.addressvar.set('')

                else:
                    self.validaddr = True

            self.assetname = StringVar()

            def get_name(event):
                if self.validaddr == False:
                    self.assetname.set('')

                elif self.validaddr == True:
                    self.name = create_contract(self.addressvar.get()).functions.name().call()
                    #self.name = self.name_contract.call()

                    self.assetname.set(self.name)

            tk.Label(
                master = self,
                text = 'Asset name',
                font = 'bold 14'
            ).grid(
                row = 3,
                sticky = 'w',
                padx = 30,
                pady = 6
            )

            self.name_entry = tk.Entry(
                master = self,
                textvariable = self.assetname,
                width = 44,
                font = 'bold 13',
                state = 'readonly',
                highlightthickness = 0
            ).grid(
                row = 4,
                sticky = 'w',
                padx = 32,
                pady = 3
            )

            self.symbol = StringVar()

            def get_symbol(event):
                if self.validaddr == False:
                    self.symbol.set('')

                elif self.validaddr == True:
                    self.symbol_name = create_contract(self.addressvar.get()).functions.symbol().call()
                    #self.symbol_name = self.symbol_contract.call()

                    self.symbol.set(self.symbol_name)

            tk.Label(
                master = self,
                text = 'Symbol',
                font = 'bold 14'
            ).grid(
                row = 5,
                sticky = 'w',
                padx = 30,
                pady = 3
            )

            self.symbol_entry = tk.Entry(
                master = self,
                textvariable = self.symbol,
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

            self.decvar = StringVar()

            def get_dec(event):
                if self.validaddr == False:
                    self.decvar.set('')

                elif self.validaddr == True:
                    self.decimals = create_contract(self.addressvar.get()).functions.decimals().call()
                    #self.decimals = self.decimals_contract.call()

                    self.decvar.set(str(self.decimals))

            tk.Label(
                master = self,
                text = 'Decimal',
                font = 'bold 14'
            ).grid(
                row = 7,
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
                row = 8,
                sticky = 'w',
                padx = 32,
                pady = 3
            )

            self.address_entry.bind(
                '<KeyRelease>',
                lambda e: [
                    get_data(e),
                    get_dec(e),
                    get_name(e),
                    get_symbol(e)
                ]
            )

            def add_asset_details():
                if self.validaddr == False:
                    pass

                elif len(self.address_entry.get()) == 0:
                    pass

                else:
                    if self.addressvar.get() in globalvar.assets_addr:
                        messagebox.showerror(
                            title = "Error",
                            message = 'Asset already in your list',
                            icon = "error",
                        )

                        self.addressvar.set('')
                        self.assetname.set('')
                        self.decvar.set('')
                        self.symbol.set('')
                        return

                    globalvar.assets_addr.append(self.addressvar.get())

                    master.asset_list.delete(0, 'end')
                    master.asset_list2.delete(0, 'end')

                    if os.name == 'nt':
                        master.asset_list.insert(tk.END, ' Ether (ETH)\n')
                        master.asset_list2.insert(
                            tk.END, ' ' + str(w3.from_wei(w3.eth.get_balance(globalvar.account.address), 'ether')) + '\n')

                    else:
                        master.asset_list.insert(tk.END, ' Ether (ETH)')
                        master.asset_list2.insert(
                            tk.END, ' ' + str(w3.from_wei(w3.eth.get_balance(globalvar.account.address), 'ether')))


                    for i in range(0, len(globalvar.assets_addr)):
                        self.contract = create_contract(globalvar.assets_addr[i])

                        self.token_name    = self.contract.functions.name().call()
                        self.token_symbol  = self.contract.functions.symbol().call()

                        if os.name == 'nt':
                            master.asset_list.insert(
                                'end', ' ' + self.token_name + f" ({self.token_symbol})\n"
                            )

                        else:
                            master.asset_list.insert(
                                'end', ' ' + self.token_name + f" ({self.token_symbol})"
                            )

                        self.token_balance = self.contract.functions.balanceOf(globalvar.account.address).call()

                        if os.name == 'nt':
                            master.asset_list2.insert(
                                'end', ' ' + self.token_name + f" ({self.token_balance})\n"
                            )

                        else:
                            master.asset_list2.insert(
                                'end', ' ' + self.token_name + f" ({self.token_balance})"
                            )

                        if float(self.token_balance) != 0.0:
                            globalvar.total_balance_of_assets += float(w3.from_wei(self.token_balance, 'ether'))

                    with open(globalvar.assets_json, 'w') as f:
                            json.dump(globalvar.assets_addr, f)



                    #AssetLoadingBar.loading = 0
                    #AssetLoadingBar.filluplists()

                    self.destroy()


            tk.Button(
                master = self,
                text = 'Continue',
                font = 'bold 14',
                command = add_asset_details
            ).grid(
                pady = 20,
                padx = 100,
                row = 9,
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
                row =  9,
                sticky = 'w'
            )

    # Delete coin
    class DeleteCoinWindow(tk.Toplevel):
        def __init__(self, master):
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
                master = self
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

            self.contract = type(create_contract)

            for i in range(0, len(globalvar.assets_addr)):
                self.contract = create_contract(globalvar.assets_addr[i])

                self.token_name_contract    = self.contract.functions.name()
                self.token_name                   = self.token_name_contract.call()

                self.alist.insert('end', self.token_name)

            self.token_name = StringVar()

            def get_choice(*args) -> None:
                self.inp = self.alist.curselection()
                self.token_name.set(self.inp)

            self.alist.bind('<<ListboxSelect>>', get_choice)

            def del_entry() -> None:
                self.choice = str(self.token_name.get()).replace('(', '').replace(',)', '')
                #choice = choice.replace(',)', '')

                self.num: int = int(self.choice)

                master.asset_list.delete(self.num+1)
                master.asset_list2.delete(self.num+1)

                #self.contract = create_contract(globals()['assets_addr'][self.num])

                self.token_balance = self.contract.functions.balanceOf(globalvar.account.address).call()

                globalvar.total_balance_of_assets -= float(self.token_balance)

                del globalvar.assets_addr[self.num]

                with open(globalvar.assets_json, 'w') as f:
                    json.dump(globalvar.assets_addr, f)

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

    # Restore crypto list
    class RestoreDefaultCrypto(tk.Toplevel):
        def __init__(self, master):
            super().__init__()

            self.title("SimpleEtherWallet  -  Restore default coins")
            self.resizable(False, False)
            self.protocol("WM_DELETE_WINDOW", quit)

            self.withdraw()

            self.tmp = questionbox(self, msg =
                """You are about to restore displayed assets back to the default. Continue?"""
            )

            def restore_default_coins_fn(self):
                if self.tmp == False:
                    self.destroy()

                else:
                    master.asset_list.delete(0, tk.END)
                    master.asset_list2.delete(0, tk.END)

                    if os.name == 'nt':
                        master.asset_list.insert(END, ' Ether (ETH)\n')
                        asset_list2.insert(END, ' ' + str(w3.from_wei(w3.eth.get_balance(globalvar.account.address), 'ether')) + '\n')

                    else:
                        master.asset_list.insert(END, ' Ether (ETH)')
                        master.asset_list2.insert(END, ' ' + str(w3.from_wei(w3.eth.get_balance(globalvar.account.address), 'ether')))

                    globalvar.assets_addr = [
                        '0xdAC17F958D2ee523a2206206994597C13D831ec7',
                        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                        '0x6B175474E89094C44Da98b954EedeAC495271d0F',
                        '0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6'
                    ]

                    master.asset_list.insert('end', *self.globalvar)

                    for i in range(0, len(globalvar.assets_addr)):
                        self.contract = create_contract(globalvar.assets_addr[i])
                        self.token_balance_contract = self.contract.functions.balanceOf(account.address).call()

                        if os.name == 'nt':
                            master.asset_list2.insert('end',  ' ' + str(w3.from_wei(self.token_balance, 'ether')) + '\n')

                        else:
                            mater.asset_list2.insert('end',  ' ' + str(w3.from_wei(self.token_balance, 'ether')))

                        with open(globalvar.assets_json, 'w') as f:
                            json.dump(globalvar.assets_addr, f)

            restore_default_coins_fn(self)

            self.destroy()

    # Send crypto window
    class SendCryptoWindow(tk.Toplevel):
        def __init__(self, master):
            super().__init__()

            master.withdraw()

            self.title("SimpleEtherWallet  -  Send")
            self.resizable(False, False)
            self.protocol(
                "WM_DELETE_WINDOW",
                lambda: [
                    master.deiconify(),
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
                master = self
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
            SendCryptoWindow.stringentry1 = StringVar()

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

            for i in range(0, len(globalvar.assets_addr)):
                self.contract          = create_contract(globalvar.assets_addr[i])
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

                self.assetlist = globalvar.assets_addr

                if self.selected == 0:
                    self.balance_text.configure(
                        text = f"Balance: ~{str(w3.from_wei(w3.eth.get_balance(globalvar.account.address), 'ether'))[:12]} ETH"
                    )

                else:
                    self.contract = create_contract(self.assetlist[self.selected - 1])
                    self.val          = self.contract.functions.balanceOf(globalvar.account.address).call()

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
                textvariable = self.stringentry1
            )

            def entry1event(event):
                self.stringentry1.set(self.stringentry1.get()[:42])

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

            class abookwindow(tk.Toplevel):
                def __init__(self, master):
                    super().__init__()

                    self.title("SimpleEtherWallet  -  Contacts")
                    self.resizable(False, False)
                    self.protocol(
                        "WM_DELETE_WINDOW",
                        lambda: [
                            self.destroy(),
                            master.destroy(),
                            SendCryptoWindow.master.deiconify()
                        ]
                    )

                    center_window(570, 480, self)

                    self.boxframe = tk.LabelFrame(
                        master = self
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

                    for i in range(0, len(globalvar.contactbook['name'])):
                        self.box.insert(
                            tk.END, globalvar.contactbook['name'][i] + ' (' + globalvar.contactbook['address'][i] + ')'
                        )

                    def get_choice(*args):
                        choice = str(self.box.curselection()).replace('(', '').replace(',)', '')

                        num: int = int(choice)

                        self.contactchoice = globalvar.contactbook['address'][num]

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
                            master.stringentry1.set(self.contactchoice),
                            self.destroy()
                        ]
                    )

                    b2.pack(
                        side = 'left',
                        ipady = 4,
                        ipadx = 12
                    )

                    newline(self)

            def callabookwindow():
                abookwindow(self)

            abookbtn = tk.Button(
                master = row2,
                image = root.address_book2,
                command = callabookwindow
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
                cursor = 'cross',
                variable = sc_percent,
            )

            self.sc_val:float = 0.0

            def sc_cmd(event):
                selected = box.current()

                if selected == 0:
                    self.user_balance = w3.from_wei(w3.eth.get_balance(globalvar.account.address), 'ether')

                else:
                    self.contract = create_contract(globalvar.assets_addr[selected - 1])
                    self.val          = self.contract.functions.balanceOf(globalvar.account.address).call()

                    self.user_balance = self.val

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
                    master.deiconify(),
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
                def __init__(self, master):
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
                    self.address          = master.stringentry1.get()
                    self.amount           = stringentry2.get()
                    self.contract          = create_contract(globalvar.assets_addr[box.current() - 1])

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
                        master = self
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
                        #self.contact = create_contract(globalvar.assets_addr[box.current() - 1])

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
                        self.valvar.set(str(fetchprice('ETH', 'USDT') * float(self.amount)))

                    else:
                        self.assetname = self.contract.functions.symbol().call()

                        self.priceofasset: float = 0.0
                        self.valvar.set(str(fetchprice(self.assetname, 'USDT') * float(self.amount)))
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

                    self.gasineth = float(entry3.get()) / fetchprice('ETH', 'USDT')

                    ConfirmSend.GAS = self.gasineth

                    self.gasinethSTR = str(self.gasineth)[:17]

                    #self.usdlabel5.configure(text = f"$  (~{self.gasinethSTR} ETH)")
                    self.usdlabel5.configure(text = f"~{entry3.get()} $")
                    self.gasvar.set(f"{self.gasinethSTR} ETH")
                    self.gasbox['width'] = len(self.gasvar.get())

                    ConfirmSend.v = float(entry3.get())

                    class FinalizeTransaction(tk.Toplevel):
                        def __init__(self, master):
                            super().__init__()

                            self.addr = SendCryptoWindow.stringentry1.get()

                            self.title('SimpleEtherWallet  -  Verify details')
                            self.resizable(False, False)
                            self.protocol("WM_DELETE_WINDOW", quit)

                            center_window(544, 288, self)

                            self.opt = IntVar()
                            self.opt.set(1)

                            self.transaction = {
                                # From
                                "from": globalvar.account.address,
                                # To
                                "to": w3.to_checksum_address(self.addr),
                                # Value
                                "value": w3.to_wei(ConfirmSend.v, 'ether'),
                                # Nounce
                                'nonce': w3.eth.get_transaction_count(globalvar.account.address),
                                # Gas
                                'gas': 0,
                                #  Max Gas
                                'maxFeePerGas': w3.to_wei(ConfirmSend.GAS, 'ether'),
                                # Miner Tip (priority fee)
                                'maxPriorityFeePerGas': w3.to_wei(ConfirmSend.GAS / 2, 'ether')
                            }

                            def unhide():
                                if self.opt.get() == 1:
                                    self.btn.config(image = root.opened_eye)
                                    self.passentry.config(show = "")

                                    self.opt.set(0)

                                elif self.opt.get() == 0:
                                    self.btn.config(image = root.closed_eye)
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
                                image = root.closed_eye,
                                command = unhide
                            )

                            self.btn.pack(
                                side = "right",
                                padx = 10,
                            )

                            self.password = StringVar()

                            self.passentry = tk.Entry(
                                master = self.frm2,
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
                                    with open(globalvar.nameofwallet, "r") as f:
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
                                    self.tx = w3.eth.get_transaction(self.tx_hash)

                                    messagebox.showmessage(
                                        master = self,
                                        details = f"Sent! Transaction hash: {self.tx}"
                                    )

                                    SendCryptoWindow.destroy()
                                    master.deiconify()

                                except Exception:
                                    messagebox.showerror(
                                        title = "Error",
                                        message = "Insufficient funds to complete the transaction"
                                    )

                                    self.destroy()

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
                                ipady = 4,
                                ipadx = 20
                            )

                            tk.Label(
                                master = self.frm3,
                                text = ' ',
                            ).pack(
                                side = 'left',
                                padx = 8
                            )

                            tk.Button(
                                master = self.frm3,
                                text = "Sign",
                                font = 'bold 12',
                                command = checkpass
                            ).pack(
                                side = "left",
                                padx = 10,
                                ipady = 4,
                                ipadx = 20
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

                    def callfinalizetransaction():
                        FinalizeTransaction(self)

                    tk.Button(
                        master = self,
                        text = 'Confirm',
                        font = 'bold 14',
                        command = callfinalizetransaction
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
                    ConfirmSend(self)

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

    root = Master()

    greetwindow = GreetingWindow(root)

    if root.first_time == False:
        NotNewUser(greetwindow)

    elif root.first_time == True:
        NewUser(greetwindow)

    root.mainloop()


if __name__ == "__main__" :
    main()


