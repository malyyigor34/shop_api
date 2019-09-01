

#from Rozetka import Rozetka
from Price import Price
from queue import Queue
q = Queue()
#

url = 'https://price.ua/samsung/samsung_galaxy_a50_sm-a505f_64gb/catc52t9m3929993.html'
p = Price(q)
p.set_text(url)
p.start()
p.join()
print(q.get())
#
# r = Rozetka(q)
# r.set_text('https://rozetka.com.ua/36325408/p36325408/')
# r.start()
