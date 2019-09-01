from threading import Thread
import requests


class AbstractParser(Thread):
    def __init__(self):
        super(AbstractParser, self).__init__()

    def _search(self, page='', cookies={}):
        """set page with results"""
        if self._run:
            url = self._url.format(self._text+page)
            print(url)
            try:
                self._response = requests.get(url, cookies=cookies, timeout=6).text
            except Exception:
                print(self._domain+' blocked by IP')
                self._run = False

    def set_text(self, text):
        self._text = text

    def run(self):
        if self._text.find(self._domain) != -1:
            self._articles = [self._text]
        else:
            self._search()
            self._find_articles()

        result = self._parse_articles()
        self._q.put(result)

