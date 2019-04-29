from threading import Thread
from staticData import buff, videoStr
import threading
from FLVHelper.FLVHelper import Flv


class videoSender(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.running = threading.Event()
        self.running.set()
        self.client = client
        self.ifConnected = 1
        self.connectCheckTimeLeft = buff.DEFAULT_CONNECT_CHECK_TIME
        self.FLV = Flv()
        self.FLVSize = 0
        self.tagPoint = 0

    def run(self):
        Thread(target=self.senderProtector).start()

        while True:
            try:
                if self.FLVSize == 0:
                    continue
                if self.tagPoint == 0:
                    self.client.send((videoStr.TAG_SUM_START + str(self.FLVSize) + videoStr.TAG_SUM_END + " ").encode())
                    self.client.send(
                        (videoStr.HEAD_START + bytes.decode(self.FLV.head.headInfo) + videoStr.HEAD_END).encode())
                if self.FLVSize <= self.tagPoint:
                    self.client.shutdown(2)
                    break
                # if self.tagPoint == 20:
                #     self.client.shutdown(2)
                #     break
                data = (str(videoStr.TAG_HEAD) + str(self.tagPoint) +
                                str(videoStr.TAG_START) + str(self.FLV.tags[self.tagPoint].data) + str(videoStr.TAG_END))
                print(data)
                self.client.send(data.encode())
                self.tagPoint += 1
            except (ConnectionResetError,ConnectionAbortedError) as e:
                self.client.shutdown(2)
                self._stop()


            pass

    def sendData(self):
        pass

    def senderProtector(self):
        print(str(self.client.getpeername()) + "'s protector started!")
        while True:
            try:
                data = bytes.decode(self.client.recv(buff.bufflen))
                self.optionHandler(data)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
                self.client.shutdown(2)

    def optionHandler(self, data):
        strList = data.split(" ")
        if videoStr.CHANGE_VIDEO_NAME in strList:
            index = strList.index(videoStr.CHANGE_VIDEO_NAME)
            index2 = strList.index(videoStr.CHANGE_VIDEO_NAME_EOF)
            if index + 2 < index2:
                path = ""
                for i in range(index2 - index - 1):
                    if i > 0:
                        path = path + " " + strList[index+i+1]
                    else:
                        path = path + strList[index+i+1]
            else:
                path = strList[index+1]
            # print(path)
            try:
                self.FLVSize = self.FLV.load(path)
                self.tagPoint = 0
            except FileNotFoundError as e:
                self.client.send(videoStr.NO_VIDEO_FILE.encode())
            print(self.FLVSize)
        if videoStr.CHANGE_PLAY_TIME in strList:
            print("changetime")

        pass
