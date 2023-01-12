#!/usr/bin/env python3

from mimetypes import init
from colorama import init
from lxml import html
from requests import get
from colorama import Fore
from walletobj import WalletObj
from netmodule import ProxyController


class WalletGenerator:
      @staticmethod
      def createWallets() -> dict:
            w = WalletObj()
            return w.walletData

class RequestGenerator():
      @staticmethod
      def make_request(data : dict, proxy : str) -> None:
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
      @staticmethod
      def check_balance(input : str) ->  bool:
            if input != "0 LTC":
                  return True

class FileWriter():
      @staticmethod
      def write_to_file(addrType : str, addres : str, privateKey : str, wif: str, bal: str) -> None:
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


init(main())