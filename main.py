from Rozetka import Rozetka
from Price import Price

from queue import Queue

q = Queue()

r = Rozetka(q)
r.set_text('iphone 8')
r.start()

p = Price(q)
p.set_text('iphone 8')
p.start()




