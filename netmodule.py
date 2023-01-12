""" MODULE WITH PROXY CONTROLLER WHICH GETS PROXY ADDRESS IP:PORT """


from lxml import html
from requests import get
from colorama import Fore

class ProxyController:
      nextIndex : int = 1
      timesUsed : int = 0
      
      @classmethod
      def get_proxies(self) -> str:
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
