
import sys, subprocess, json
#sys.path.insert(0, '/home/dcback')
from monero.wallet import Wallet
from monero.daemon import Daemon
from monero.backends.jsonrpc.wallet import JSONRPCWallet
from monero.backends.jsonrpc.daemon import JSONRPCDaemon
from monero.seed import Seed
from monero.address import address

def genSeed(e=None):
    res = Seed().hex if e == 'hex' else Seed().phrase
    return res

g = genSeed('hex')
# print(g)

jsn = {
    "version": 1,
    "filename": "/home/user/Monero/wallets/test3/test3",
    "password": "Od_290178",
    "language":"English",
    "seed": Seed(g).phrase
}

# res = subprocess.check_output(['monero-wallet-cli', '--testnet', '--generate-new-wallet', '/home/user/Monero/wallets/test3/test3'])

# print(res)

# w = Wallet(OfflineWallet('test_1'))
# w = Daemon(JSONRPCDaemon(protocol="http",
#         host="127.0.0.1",
#         port=18081))
# print(w.block())
# s = Seed()
# with open('/home/user/Monero/wallets/test_1/test_1.address.txt', 'r') as f:
    # adres = f.read()
# a = address(adres)
# print(a.net)

