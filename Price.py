from threading import Thread

from .IpBlocked import IpBlocked
from .Proxy import Proxy

from bs4 import BeautifulSoup
import re


class Price(Thread):
    def __init__(self, q):
        super(Price, self).__init__()
        self._q = q
        self._url = 'https://price.ua/search/?q={}'
        self._domain = 'https://price.ua/'
        self._name = 'price.ua'
        self._articles = []
        self._run = True
        self._proxy = Proxy(self._name)

    def _find_seller(self, price_soup):
        seller_url = price_soup.find('a', {'class': 'store-link'}).get('href')
        seller_response = self._proxy.get(seller_url).text
        seller_soup = BeautifulSoup(seller_response, 'html.parser')
        seller = seller_soup.find('h1', {'class': 'h2'}).text
        return seller

    def _search(self, page='', cookies={}):
        """set page with results"""
        if self._run:
            url = self._url.format(self._text + page)
            print(url)
            try:
                self._response = self._proxy.get(url, cookies=cookies).text
            except Exception:
                print(self._domain + ' blocked by IP')
                self._run = False
    def set_text(self, text):
        self._text = text

    def _find_img(self, soup):
        img = soup.find('img', {'id': 'model-big-photo-img'}).get('src')
        return img

    def parse(self):
        cookies = {'catalog_mode': 'list'}
        result = []
        for i in range(1, 10):
            self._search(i*'&'+ 'Propose_page='+str(i), cookies=cookies)
            soup = BeautifulSoup(self._response, 'html.parser')
            if self._response.find('Пожалуйста, подтвердите что Вы не робот') != -1:
                self._run = False
                print(self._domain, ' returned captcha')
            products = soup.find_all('div', {'class': 'product-item view-list catname-exist'})
            for product in products:
                try:
                    article = product.find('a', {'class': 'ga_card_mdl_pic'}).get('href')
                except AttributeError:
                    article = product.find('a', {'class': 'model-name clearer-block ga_card_mdl_title'}).get('href')
                category = product.find('a', {'class': 'model-category-name ga_card_mdl_cat'}).text
                name = product.find('a', {'class': 'model-name clearer-block ga_card_mdl_title'}).text
                try:
                    describe = product.find('div', {'class': 'dl'}).find_all('div', {'class': 'item'})
                    describe = list(map(lambda x: x.text, describe))
                    describe = '. '.join(describe).strip().replace('  ', '').replace('\n', '')
                except AttributeError:
                    describe = None

                try:
                    response = self._proxy.get(article).text
                    soup = BeautifulSoup(response, 'html.parser')
                    price_url = soup.find('li', {'class': 'block-wrapper simple3 prices noactive'}).find('a').get('onclick')
                    price_url = price_url.replace("this.href='", '').replace("'", '')

                    price_response = self._proxy.get(price_url).text
                    price_soup = BeautifulSoup(price_response, 'html.parser')

                    price = price_soup.find('span', {'class': 'price'}).text
                    price = re.sub('[a-zA-Zа-яА-Я\.\s]', '', price)
                except AttributeError:
                    price = None

                try:
                    img = self._find_img(soup).replace('//', '')

                except AttributeError:
                    img = None

                try:
                    seller = self._find_seller(price_soup)
                except AttributeError:
                    seller = None
                try:
                    result.append({
                        'source': self._name,
                        'name': name,
                        'category': category,
                        'describe': describe,
                        'seller': seller,
                        'link': article,
                        'price': int(price),
                        'img': img
                    })
                except TypeError:
                    continue
                if len(result) >= 30:
                    return result

            products_vip = soup.find_all('div', {'class': 'product-item view-list priceline catname-exist is-top-firm'})
            products_vip += soup.find_all('div', {'class': 'product-item view-list priceline catname-exist'})

            for product_vip in products_vip:
                name = product_vip.find('span', {'class': 'desc-title-wrap'}).text
                describe = product_vip.find('div', {'class': 'desc'}).text
                price = product_vip.find('div', {'class': 'price-wrap'}).text
                price = re.sub('[a-zA-Zа-яА-Я\.\s]', '', price)
                seller = product_vip.find('span', {'class': 'count'}).text
                #img = product_vip.find('div', {'class': 'photo-wrap'}).find('img').get('src').replace('//', '')
                category = product_vip.find('a', {'class': 'model-category-name ga_card_mdl_cat'}).text
                try:
                    article = self._domain + product_vip.find('div', {'class': 'model-name-wrap'}).find('a').get('href')
                except AttributeError:
                    article = product_vip.find('a', {'class': 'model-category-name ga_card_mdl_cat'}).get('href')

                try:
                    img = self._find_img(soup).replace('//', '')

                except AttributeError:
                    img = None

                result.append({
                    'source': self._name,
                    'name': name,
                    'category': category,
                    'describe': describe,
                    'seller': seller,
                    'link': article,
                    'price': int(price),
                    'img': img
                })
                if len(result) >= 30:
                    return result
            if i > 150:
                raise IpBlocked('IP blocked, attempt: {}, link: {}'.format(i, article))
            i += 1
        return result

    def parse_one(self):
        result = []
        response = self._proxy.get(self._text)
        response = response.text
        soup = BeautifulSoup(response, 'html.parser')
        try:
            name = soup.find('div', {'id': 'page-title'}).find('span').text
        except AttributeError:
            name = None

        try:
            category = soup.find('div', {'id': 'page-breadcrumbs'}).find_all('span')[1::2]
            category = list(map(lambda x: x.text, category))
            category = list(filter(lambda x: x != ' ', category))
            category = ', '.join(category)
        except AttributeError:
            category = None
        try:

            price_url = soup.find('a', {'class': 'border-radius-topline-6 ga_mdl_tab_price'}).get('href')
            price_url += '/?order=price_asc'

            price_repsonse = self._proxy.get(price_url).text
            price_soup = BeautifulSoup(price_repsonse, 'html.parser')
            shop = price_soup.find('div', {'id': 'table-prices'})

            price = shop.find('span', {'class': 'price'}).text
            price = re.sub('[a-zA-Zа-яА-Я\.\s]', '', price)
        except AttributeError:
            price = None
        try:
            describe = shop.find('span', {'class': 'descr-text'}).text.replace('Подробнее','')
        except AttributeError:
            describe = None
        try:
            seller = self._find_seller(shop)
        except AttributeError:
            seller = None
        try:
            img = soup.find('img', {'id': 'model-big-photo-img'}).get('src').replace('//', '')
        except AttributeError:
            img = None

        result.append({
            'source': self._name,
            'name': name,
            'category': category,
            'describe': describe,
            'seller': seller,
            'link': self._text,
            'price': int(price),
            'img': img
        })
        return result

    def run(self):
        if self._text.find(self._domain) != -1:
            try:
                result = self.parse_one()
            except Exception:
                result = {'error': 'Page not found, 404'}
            self._q.put(result)
            return
        elif self._text.find('https://') != -1:
            result = []
            return
        self._search()
        result = self.parse()
        print(result)
        self._q.put(result)

price_articles = {
    'block': 'a',
    'id': 'class',
    'name': 'photo-wrap'
}


