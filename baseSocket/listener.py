import threading
import socket

from baseSocket import reader, transferor
from enum import Enum

from httpSocket.httpHandler import httpHandler
from staticData import buff


class listener(threading.Thread):

    def run(self):
        info = self.getModeStr()
        print(info)
        if self.mode == MODE.READER:
            self.listen()
        if self.mode == MODE.TRANSFER:
            self.tansfer()
        if self.mode == MODE.HTTPHANDLER:
            self.httphandler()

    def httphandler(self):
        while True:
            client, _ = self.sock.accept()
            print("port " + str(self.port) + " reader catch something")
            httpHandler(client).start()

    def listen(self):
        while True:
            client, _ = self.sock.accept()
            print("port " + str(self.port) + " reader catch something")
            reader.reader(client).start()


    def tansfer(self):
        while True:
            # print(123)
            client, _ = self.sock.accept()
            transferor.transferor(self.ip, self.port, self.targetip, self.targetport, client).start()

    def getModeStr(self):
        info = self.ip + " " + str(self.port)

        if self.mode == MODE.READER:
            info += (" transfer start successfully! "+"target ip is " + self.targetip + " target port is " + str(self.targetport))
        if self.mode == MODE.TRANSFER:
            info += " reader start successfully! "
        if self.mode == MODE.HTTPHANDLER:
            info += " httpHandler start successfully! "
        return info

    def __init__(self, port, mode, ip="127.0.0.1", targetIP="127.0.0.1", targetport=80, maxconnection=100):
        threading.Thread.__init__(self)
        self.ip = ip
        self.targetip = targetIP
        self.targetport = targetport
        self.mode = mode
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(maxconnection)
        # self.transfer = transferor.transferor()


class MODE(Enum):
    READER = 1
    TRANSFER = 2
    HTTPHANDLER = 3
