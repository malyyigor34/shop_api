import requests
from bs4 import BeautifulSoup

FILE_WITH_PROXY = 'proxy_list.txt'


class Proxy:
	def __init__(self):
		self._url = 'https://www.xroxy.com/proxy-country-ua'
		self._headers = {
            	'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
      	  }
		self._proxy = []
		self._good_proxy = []
		self._allowed_types = ['Socks4', 'Socks5']#, 'Anonymous']
	def get_page(self):
		i = 0
		while True:
			try:
				response = requests.get(self._url, headers=self._headers)
				yield response.text
				i += 1
				if i == 3:
					break
			except Exception:
				i += 1
				continue

	def get_proxy(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		table = soup.find('table', {'class': 'dttable table table-striped table-bordered dt-responsive nowrap dataTable dtr-inline'})
		for tr in table.find_all('tr'):
			try:
				tds = tr.find_all('td')
				if tds[2].text not in self._allowed_types:
					continue
				type = tds[2].text.lower()
				ip = tds[0].text
				port = tds[1].text
				self._proxy.append([type, ip, port])
			except (AttributeError, IndexError):
				print('Ошибка при парсинге строки. Найден прокси не разрешённого типа или в строке нет информации о прокси или тип прокси не разрешён.')
				continue

	def check(self):
		with open(FILE_WITH_PROXY, 'w') as f:
			f.write('')

		for proxy in self._proxy:
			try:
				response = requests.get(self._url, proxies={'{}': '{}:{}'.format(proxy[0], proxy[1], proxy[2])}, timeout=2)
				if response.status_code != 200:
					continue
				self.save(proxy)
				print('Работает: ', proxy)
				self.save(proxy)
			except Exception:
				print('Прокси {} не рабочий'.format(proxy))
				continue

	def save(self, proxy):
		try:
			proxy = '{}:{}:{}'.format(proxy[0], proxy[1], proxy[2])
			with open(FILE_WITH_PROXY, 'a') as f:
				f.write(proxy+'\n')
		except Exception:
			print('Неизвестная ошибка при записи в файл. Возможно файл открыт другим процессом.')

def main():
	proxy = Proxy()
	for page in proxy.get_page():
		proxy.get_proxy(page)
	proxy.check()


if __name__ == '__main__':
	while True:
		try:
			main()
		except Exception:
			print('Произошла ошибка в главном цикле')