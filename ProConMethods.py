from Queue

class proCon():

    pro = Queue.Queue(maxsize=10)
    con = Queue.Queue(maxsize=10)
    
    def consume():
        con.put()
    def produce():
        pro.put()
