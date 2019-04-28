class Tag(object):
    previousTagsSize = 0
    type = 0
    length = 0
    timestamp = 0
    exTimestamp = 0
    streamsId = 0
    data = []

    def parse(self):
        pass

    def __str__(self):
        return "%s previousTagsSize:%d type:%d length:%d timestamp:%d exTimestamp:%d streamsId:%d" % (
            self.__class__, self.previousTagsSize, self.type, self.length, self.timestamp, self.exTimestamp,
            self.streamsId)

    def getBytes(self):
        return self.data
