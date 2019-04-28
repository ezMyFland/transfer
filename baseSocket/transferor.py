import socket
import threading
from staticData import buff


class transferor(threading.Thread):

    def __init__(self, ip, port, targetIP, targetport, client):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.targetip = targetIP
        self.targetport = targetport
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client = client
        # self.sock.bind((self.targetip, self.targetport))

    def run(self):
        while True:
            buff = self.client.recv(buff.bufflen)
            if buff:
                print(self.sock.connect((self.targetip, int(self.targetport))))
                self.sock.send(buff)
                print("success transfer content from " + self.ip + ":" + str(self.port)
                      + " to " + self.targetip + ":" + str(self.targetport))

            else:
                print("error data")
                self.sock.shutdown(2)
                self.sock.close()
                break


