from socket import socket
from staticData import videoStr,buff
import time
import re
from FLVHelper.TAGHelper.FLVHead import Head
from threading import Thread


class client(Thread):

    def __init__(self,addr = ("localhost", 10086),filepath = ""):
        Thread.__init__(self)
        self.s = socket()
        self.addr = addr
        self.data = ""
        self.filepath = filepath
        self.tag = []
        self.taglengthsum = None
        self.FLVhead = None

    def run(self):
        self.s.connect(("localhost", 10086))
        self.s.send("yes".encode())
        buff = self.s.recv(1024)
        if bytes.decode(buff) == videoStr.CONNECT_SUCCESS or bytes.decode(
                buff) == videoStr.DEFAULT_CHECK_CONNECT_STRING_LISTENER:
            print("connected")
            time.sleep(5)
            self.s.send((videoStr.CHANGE_VIDEO_NAME + " " +
                    "C:/Users/89749/Documents/Tencent Files/897494980/FileRecv/36721-2016-10-15-21-17-29.flv "
                    + videoStr.CHANGE_VIDEO_NAME_EOF
                    ).encode())
            i = 0
            while True:
                buff = self.s.recv(4096)
                self.data += bytes.decode(buff)
                self.data = self.data.replace(videoStr.DEFAULT_CHECK_CONNECT_STRING_LISTENER, "")
                if not self.taglengthsum:
                    lengthtag = re.findall(r"" + videoStr.TAG_SUM_START + "(.+?)" + videoStr.TAG_SUM_END, self.data)
                    if len(lengthtag) > 0:
                        self.taglengthsum = int(lengthtag[0])
                        self.tag = ["" for i in range(self.taglengthsum)]
                        self.data = self.data.replace(videoStr.TAG_SUM_START + lengthtag[0] + videoStr.TAG_SUM_END, "")
                    else:
                        continue
                if not self.FLVhead:
                    FLVheadtag = re.findall(r"" + videoStr.HEAD_START + "(.+?)" + videoStr.HEAD_END, self.data)
                    if len(FLVheadtag) > 0:
                        self.FLVhead = Head(FLVheadtag[0].encode())
                        self.data = self.data.replace(videoStr.HEAD_START + FLVheadtag[0] + videoStr.HEAD_END, "")
                        self.data = self.data[1:]
                    else:
                        continue

                rectags = re.findall(r"" + videoStr.TAG_HEAD + "(.+?)" + videoStr.TAG_END, self.data)
                if len(rectags) != 0:
                    for string in rectags:
                        # tag.append(string)
                        self.data = self.data.replace(videoStr.TAG_HEAD + string + videoStr.TAG_END, "")
                        start_tag_loc = string.find(videoStr.TAG_START)
                        tag_loc = int(string[:start_tag_loc])
                        self.tag[tag_loc] = string[start_tag_loc + len(videoStr.TAG_START):]
                        print(self.tag.index(""))

        pass