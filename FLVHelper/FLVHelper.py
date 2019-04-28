from staticData.FLV.TAG import staticTAG
from util import bytesutil
import traceback
from FLVHelper.TAGHelper import FLVHead, audioTAG, videoTAG, scriptTAG, otherTAG
from staticData import buff


class Flv(object):
    head = None
    tags = []
    previousTagSize = 0
    # 内部缓冲区
    __buffer = None

    # 加载flv文件
    def load(self, filePath, buffSize=buff.FLV_BUFF_SIZE):
        ret = 0
        assert filePath != ""
        try:
            with open(filePath, 'rb') as io:
                preTag = None
                while 1:
                    if self.__buffer is not None:
                        # 当缓冲区达到指定buffer时不再读取文件，先处理缓冲区
                        buffLen = len(self.__buffer)
                        if buffLen >= buffSize:
                            ctx = self.__buffer
                        else:
                            ctx = io.read(buffSize)
                            if len(ctx) != 0:
                                ctx = self.__buffer + ctx
                            else:
                                ctx = self.__buffer
                        self.__buffer = None
                    else:
                        ctx = io.read(buffSize)
                    size = len(ctx)
                    if size > 0:
                        # 处理文件头
                        if self.head is None:
                            if size >= 9:
                                self.head = FLVHead.Head(ctx)
                                ctx = ctx[self.head.len():]
                                size -= self.head.len()
                            else:
                                self.__buffer = ctx
                        # 处理标签数据(最后一个循环会遗留4个字节为最后一个tag的大小)
                        if size >= 4:
                            # 最后那一个previousTagsSize为4字节
                            self.previousTagSize = bytesutil.bytes2int(ctx[0:4])
                            if size >= 15:
                                if preTag is None:
                                    previousTagType = ctx[4]
                                    if previousTagType == staticTAG.TagType.FLV_TAG_AUDIO:
                                        preTag = audioTAG.AudioTag()
                                    elif previousTagType == staticTAG.TagType.FLV_TAG_VIDEO:
                                        preTag = videoTAG.VideoTag()
                                    elif previousTagType == staticTAG.TagType.FLV_TAG_SCRIPT:
                                        preTag = scriptTAG.ScriptTag()
                                    else:
                                        preTag = otherTAG.OtherTag()
                                    # 处理基本信息，最后才处理数据
                                    preTag.previousTagsSize = self.previousTagSize
                                    preTag.type = previousTagType
                                    preTag.length = bytesutil.bytes2int(ctx[5:8])
                                    preTag.timestamp = bytesutil.bytes2int(ctx[8:11])
                                    preTag.exTimestamp = bytesutil.bytes2int(ctx[11:12])
                                    preTag.streamsId = bytesutil.bytes2int(ctx[12:15])
                                    size -= 15
                                    ctx = ctx[15:]
                                    if size > 0:
                                        if size >= preTag.length:
                                            preTag.data = ctx[:preTag.length]
                                            self.__buffer = ctx[preTag.length:]
                                            size -= preTag.length
                                            self.tags.append(preTag.parse())
                                            ret += 1
                                            preTag = None
                                        else:
                                            preTag.data = ctx[:size]
                                            self.__buffer = None
                                    else:
                                        self.__buffer = None
                                else:
                                    # 补充剩下的数据
                                    calcSize = preTag.length - len(preTag.data)
                                    if size >= calcSize:
                                        preTag.data = preTag.data + ctx[:calcSize]
                                        size -= calcSize
                                        if size > 0:
                                            self.__buffer = ctx[calcSize:]
                                        else:
                                            self.__buffer = None
                                        self.tags.append(preTag.parse())
                                        ret += 1
                                        preTag = None
                                    else:
                                        preTag.data = preTag.data + ctx[:calcSize]
                                        self.__buffer = None
                        else:
                            self.__buffer = ctx
                    else:
                        break
                # end while
        except Exception as e:
            print("Exception:\n%s\n" % traceback.format_exc())
        return ret
