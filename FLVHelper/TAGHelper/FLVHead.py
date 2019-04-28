from exception.FLVexception import UnSupportAmfValFormat, UnSupportFileFormat
from util import bytesutil


class Head(object):
    signature = None
    version = None
    flag = None
    length = 0
    headInfo = None

    def __init__(self, data):
        self.signature = (data[0:3])
        self.signature = bytes.decode(self.signature)
        if self.signature != "FLV":
            raise UnSupportFileFormat("文件格式不被支持")
        self.version = data[3]
        self.flag = data[4]  # 此处101为视频+音频，100为视频，001为音频
        self.length = bytesutil.bytes2int(data[5:9])
        self.headInfo = data[0:9]

    def has_audio(self):
        return self.flag & 1

    def has_video(self):
        return self.flag >> 2

    def len(self):
        return self.length
