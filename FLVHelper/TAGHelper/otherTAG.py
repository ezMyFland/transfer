from FLVHelper.TAGHelper.TAG import Tag


class OtherTag(Tag):
    """其他标签不予处理"""

    def parse(self):
        """获取字节数据,这部分暂不处理"""
        return self
