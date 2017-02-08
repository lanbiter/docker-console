import threading
import time

class threadSend(threading.Thread):
    def __init__(self,ws,sock):
        threading.Thread.__init__(self)
        self.ws = ws
        self.sock = sock

    def run(self):
        while not self.ws.closed:
            try:
                resp = self.sock.recv(1024)
                if resp is not None:
                    self.ws.send(resp)
                else:
                    print 'sock close,ws'
                    self.ws.close()
            except:
                print 'exception sock close'
                self.ws.close()
                break

