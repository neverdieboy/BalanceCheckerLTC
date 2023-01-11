#!/usr/bin/env python3

from mimetypes import init
from lxml import html
from requests import get
from secrets import token_hex
from colorama import Fore, init
from hdwallet import HDWallet
from hdwallet.symbols import LTC as SYMBOL

class ProxyController:
      nextIndex : int = 1
      timesUsed : int = 0
      
      @classmethod
      def get_proxies(self) -> list:
            if self.timesUsed == 2:
                  self.nextIndex += 1
                  self.timesUsed = 0
            urlblock = "https://free-proxy-list.net/"
            ipAdressPass = f'/html/body/section/div/div[2]/div/table/tbody/tr[{self.nextIndex}]/td'
            ipPortPass = f'/html/body/section/div/div[2]/div/table/tbody/tr[{self.nextIndex}]/td[2]'
            respone_block = get(urlblock)
            byte_string = respone_block.content
            source_code = html.fromstring(byte_string)
            ipId = source_code.xpath(ipAdressPass)
            portId = source_code.xpath(ipPortPass)
            ipAdress = ipId[0].text_content()
            ipPort = portId[0].text_content()
            proxy = f"http://{ipAdress}:{ipPort}"

            print(Fore.YELLOW + 'PROXY ADDRESS  : ' + Fore.RED + proxy)
            self.timesUsed += 1
            return proxy

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

class WalletGenerator:
      @classmethod
      def createWallets(self) -> dict:
            w = WalletObj()
            return w.walletData

class RequestGenerator():
      @classmethod
      def make_request(self, data : dict, proxy):
            adresses = data["Adresses"]
            for i in adresses.items():
                  url = "https://litecoin.atomicwallet.io/address/" + i[1]
                  xpatch_txid = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[3]/td[2]'
                  respone_block = get(url, proxies={"http": proxy[0]}, timeout=30)
                  byte_string = respone_block.content
                  source_code = html.fromstring(byte_string)
                  treetxid = source_code.xpath(xpatch_txid)
                  bal = str(treetxid[0].text_content())
                  if BalanceChecker.check_balance(bal):
                        FileWriter.write_to_file(i[0], i[1], data["privKey"], data["wif"], bal)
                  print(f"{Fore.BLUE}{i[0]}: {Fore.WHITE}{bal} {Fore.MAGENTA}Address: {i[1]}")


class BalanceChecker():
      @classmethod
      def check_balance(self, input) ->  bool:
            if input != "0 LTC":
                  return True

class FileWriter():
      @classmethod
      def write_to_file(self, addrType : str, addres : str, privateKey : str, wif: str, bal: str) -> None:
            with open("wifData.txt", "a") as file:
                  file.write(f"\n\nPrivKey: {privateKey}")
                  file.write(f"\nWIF: {wif}")
                  file.write(f"\n{addrType} address: {addres}")
                  file.write(f"\nBalance: {bal}")

 
def main():
      print("Amount of keys you want to request: ")
      i = int(input())
      b = 0
      while b < i:
            RequestGenerator.make_request(WalletGenerator.createWallets(), ProxyController.get_proxies())
            b += 1

init()
init(main())