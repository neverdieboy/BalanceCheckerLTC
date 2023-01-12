""" MODULE WHICH CONTAINS WALLET AND ITS DATA """


from hdwallet import HDWallet
from secrets import token_hex
from hdwallet.symbols import LTC as SYMBOL

class WalletObj:
      def __init__(self) -> None:
            self.walletData = self.create_wallet()
      def create_wallet(self) -> dict:
            hex = token_hex(32)
            PRIVATE_KEY = str(hex)
            hdwallet: HDWallet = HDWallet(symbol=SYMBOL)
            hdwallet.from_private_key(private_key=PRIVATE_KEY)
            wif = hdwallet.wif()
            t = {"Adresses" : 
                  {"p2wsh" : hdwallet.p2wsh_address(), 
                  "p2pkh" : hdwallet.p2pkh_address(), 
                  "p2wpkh_in_p2sh": hdwallet.p2wpkh_in_p2sh_address(), 
                  "p2wpkh": hdwallet.p2wpkh_address()},
                  "privKey" : PRIVATE_KEY, 
                  "wif" : wif}
            return t