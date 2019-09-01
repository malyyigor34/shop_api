from rest_framework.response import Response
from rest_framework.views import APIView

from queue import Queue

from .Rozetka import Rozetka
from .Price import Price


class ArticleView(APIView):
    def get(self, request):
        try:
            search = request.GET.get('search')

        except Exception:
            return Response({'error': 'Incorrect request', "articles": []})
        print(search)
        q = Queue()

        try:
            price = Price(q)
            price.set_text(search)
            price.start()


        except Exception:
            response = {
                'error': 'Error on parsing data from Rozetka',
                'articles': []
            }


        try:
            rozetka = Rozetka(q)
            rozetka.set_text(search)
            rozetka.start()

        except Exception:
            response = {
                'error': 'Error on parsing data from Rozetka',
                'articles': []
            }

        rozetka.join()
        price.join()
        try:
            response = []
            response += q.get()
            response += q.get()
            response = sorted(response, key=lambda x: int(x.get('price')))
            response += {'error': 'no'}

        except Exception:
            response = {
                'error': 'Error on get from queue',
                'articles': []
            }
       # response += q.get()
        return Response(response)
