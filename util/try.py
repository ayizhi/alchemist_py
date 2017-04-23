import Queue as queue
import pprint

q = queue.Queue()

q.put(11)

print q.get


symbol_list = [11,22,33,44,55,66]
d = dict( (k,v) for k,v in  [(s,0) for s in symbol_list])
d['datetime'] = '20120302'
pprint.pprint(d)