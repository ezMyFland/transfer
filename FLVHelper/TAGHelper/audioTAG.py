from FLVHelper.TAGHelper.TAG import Tag


class AudioTag(Tag):
    """音频tag"""
    format = None
    samplerate = None
    bits = 0
    sc = 0
    __flag = None
    __data = []

    def parse(self):
        data = super().getBytes()
        if len(data) != 0:
            self.__flag = data[0]
            self.__data = data[1:]
            # 前面4位为音频格式
            self.format = self.__flag >> 4
            # 5 6位是采样率 0000 0011&0010 1011= 0000 0011=3
            self.samplerate = (0x03 & self.__flag >> 2)
            # 7 位是采样长度 0 8bit 1 16bits
            self.bits = (self.__flag >> 1 & 0x01)
            # 单声道还是双声道 0单声道 1立体声
            self.sc = (self.__flag & 0x01)
        return self

    def getBytes(self):
        """获取字节数据"""
        return self.__data
