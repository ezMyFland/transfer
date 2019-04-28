from FLVHelper.TAGHelper.TAG import Tag


class VideoTag(Tag):
    """视频tag"""
    frameType = None
    codec = None
    __flag = None
    __data = []

    def parse(self):
        """解析视频tag信息"""
        data = super().getBytes()
        if len(data) != 0:
            self.__flag = data[0]
            self.__data = data[1:]
            # 前4位为帧类型
            self.frameType = (self.__flag >> 4)
            # 后4位位编码类型（发现python左偏移貌似有些问题,不会自动补位，所以不能用左偏移）
            self.codec = (self.__flag & 0x0f)
        return self

    def getBytes(self):
        """获取字节数据"""
        return self.__data

