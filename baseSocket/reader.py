import threading
from staticData import buff

class reader(threading.Thread):

    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True :
            data = self.client.recv(buff.BUFFSIZE)
            if data:
                string = bytes.decode(data, buff.encoding)
                print(string, end='')
                self.handleRecv(self.client)
            else:
                break

    def handleRecv(self, client, data):
        pass
