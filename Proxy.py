from Proxy_settings import *
import requests
import time


class Proxy:
    def __init__(self, name):
        self._name = name
        while True:
            try:
                self.get_proxy_list()
            except Exception:
                print('Файл заблокирован другим процесом. Жду 2 сек.')
                time.sleep(2)
                continue

    def get_proxy_list(self):
        with open(PATH_TO_PROXY_FILE, 'r') as f:
            self._proxy = f.read().split()
            self._proxy = list(map(lambda x: x.split(':'), self._proxy))

    def _get_page(self, url, cookies, proxy={}):
        print(url)
        response = requests.get(url, proxies=proxy, timeout=4, cookies=cookies)
        return response

    def get(self, url, cookies={}):
        if settings.get(self._name).get('proxy') != '':
            for proxy in self._proxy:
                try:
                    proxy = {proxy[0]: '{}:{}'.format(proxy[1], proxy[2])}
                    return self._get_page(url, cookies, proxy)
                except Exception:
                    continue