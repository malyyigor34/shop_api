from .Proxy_settings import *
import requests
import time
import random
import socket
import socks

class Proxy:
    def __init__(self, name):
        self._name = name

        while True:
            try:
                self.get_proxy_list()
                break
            except Exception:
                print('Файл заблокирован другим процесом. Жду 2 сек.')
                time.sleep(2)
                continue

    def get_proxy_list(self):
        with open(PATH_TO_PROXY_FILE, 'r') as f:
            self._proxy = f.read().split()
            self._proxy = list(map(lambda x: x.split(':'), self._proxy))

    def _get_page(self, url, cookies, proxy={}, headers={}):
        proxy_type = proxy[0]
        proxy_ip = proxy[1]
        port = int(proxy[2])

        if proxy_type == 'socks4':
            proxy_type = socks.PROXY_TYPE_SOCKS4
        if proxy_type == 'socks5':
            proxy_type = socks.PROXY_TYPE_SOCKS5

        socks.setdefaultproxy(proxy_type, proxy_ip, port)
        socket.socket = socks.socksocket

        print('used proxy: {} for url: {}'.format(proxy, url))
        response = requests.get(url, timeout=4, cookies=cookies, headers={})
        return response

    def get(self, url, cookies={}, headers={}):
        if settings.get(self._name).get('proxy') != '':
            while True:
                proxy_id = random.randint(0, len(self._proxy)-1)
                proxy = self._proxy[proxy_id]
      #          proxy = proxy.split(':')
                try:
#                    proxy = {proxy[0]: '{}:{}'.format(proxy[1], proxy[2])}
                    response = self._get_page(url, cookies, proxy, headers=headers)
                    break
                except Exception as err:
                    print(err)
                    continue
        return response