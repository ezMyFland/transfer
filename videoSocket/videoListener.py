from socket import socket
import threading
from staticData import buff,videoStr
from videoSocket.videoSender import videoSender
import time


class videoListener(threading.Thread):

    def run(self):
        threading.Thread(target=self.senderProtect).start()
        self.listen()

    def listen(self):
        print("videoListener is started! now listening " + self.ip + ":" + str(self.port))
        while True:
            client, _ = self.sock.accept()
            t = threading.Thread(target=self.handleConnect, args=(client,))
            t.start()

    def handleConnect(self, client):
        client.send(videoStr.DEFAULT_CHECK_CONNECT_STRING_LISTENER.encode())
        print("handling connecting now")
        data = []
        threading.Thread(target=self.getConnectData, args=(client, data,)).start()
        time.sleep(buff.DEFAULT_WAIT_TIME_FOR_CONNECT)
        if len(data) == 0 or not bytes.decode(data[0]) == videoStr.DEFAULT_CONNECT_STARTED_SUCCESS:
            client.shutdown(2)
            print("connected failed")
            return
        print("client " + str(self.connected) + " connected")
        vs = videoSender(client)
        vs.start()
        # client.send(videoStr.CONNECT_SUCCESS.encode())
        self.senderList.append(vs)

    def getConnectData(self, client, data):
        try:
            data.append(client.recv(buff.bufflen))
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print("connect shutdown")
        pass

    def senderProtect(self):
        print("sender protector is started!")
        while True:
            time.sleep(buff.DEFAULT_THREAD_SLEEP_TIME)
            self.connected = len(self.senderList)
            message = videoStr.DEFAULT_CHECK_CONNECT_STRING_LISTENER
            print(self.senderList)
            for sender in self.senderList:
                if sender.connectCheckTimeLeft > 0:
                    sender.connectCheckTimeLeft -= 1
                    continue
                try:
                    sender.client.send(message.encode())
                    sender.connectCheckTimeLeft = buff.DEFAULT_CONNECT_CHECK_TIME
                except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
                    self.senderList.remove(sender)
                    sender.client.shutdown(2)
                    sender.running.clear()

    def __init__(self, ip="localhost", port=10086, maxconnect=1):
        threading.Thread.__init__(self)
        self.sock = socket()
        self.ip = ip
        self.port = port
        self.sock.bind((ip, port))
        self.sock.listen(maxconnect)
        self.connected = 0
        self.senderList = []



