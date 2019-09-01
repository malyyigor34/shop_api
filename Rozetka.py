from .IpBlocked import IpBlocked
from bs4 import BeautifulSoup
import requests
import time
from .AbstractParser import AbstractParser


class Rozetka(AbstractParser):
    def __init__(self, q):
        super(Rozetka, self).__init__()
        self._q = q
        self._url = 'https://rozetka.com.ua/search/?text={}'
        self._domain = 'https://rozetka.com.ua'
        self._name = 'Rozetka'
        self._articles = []
        self._run = True


    def _find_articles(self):
        """find articles"""
        try:
            soup = BeautifulSoup(self._response, 'html.parser')
            articles = soup.find_all('div', {'class': 'g-i-tile g-i-tile-catalog'})
            self._articles += list(map(lambda x: x.find('a').get('href'), articles))
            print('articles', self._articles)
        except AttributeError:
            self._articles = []
            return

    def _parse_articles(self):
        result = []
        i = 0
        for article in self._articles[:32]:
            print(article)
            response = requests.get(article).text
            soup = BeautifulSoup(response, 'html.parser')

            try:
                category = soup.find_all('span', {'class': 'breadcrumbs-title ng-star-inserted'})
                category = list(map(lambda x: x.text, category))[1:]
                category = ', '.join(category)
            except AttributeError:
                continue

            try:
                name = soup.find('h1', {'class': 'ng-star-inserted'}).text

            except AttributeError:
                continue
            try:
                describe = soup.find('div', {'class': 'b-rich-text goods-description-content'}).text

            except AttributeError:
                describe = None

            try:
                seller = soup.find('span', {'class': 'seller-b-merchant-name ng-star-inserted'}).text
            except AttributeError:
                continue

            try:
                price = int(soup.find('span', {'class': 'detail-price-uah'}).find('span').text)

            except AttributeError:
                continue

            try:
                img = soup.find('a', {'class': 'detail-main-img-container responsive-img'}).get('href')
                if len(img) < 10:
                    img = soup.find('div', {'class': 'detail-main-img-inner'}).find('a').get('href')

            except AttributeError:
                continue

            result.append({
                'source': self._name,
                'name': name,
                'category': category,
                'describe': describe,
                'seller': seller,
                'link': article,
                'price': price,
                'img': img
            })
            if len(result) == 30:
                break
            if i > 50:
                raise IpBlocked('IP blocked, attempt: {}, link: {}'.format(i, article))
            time.sleep(0.1)
            i += 1
        return result


rozetka_articles = {
    'block': 'div',
    'id': 'class',
    'name': 'g-i-tile-i-box'
}
