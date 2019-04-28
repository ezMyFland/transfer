from baseSocket.reader import reader
from staticData import buff,http


class httpHandler(reader):

    def __init__(self, client):
        reader.__init__(self, client)
        self.initSuccess()

    def run(self):
        while True:
            if self.client.fileno() >= 0:
                data = self.client.recv(buff.BUFFSIZE)
                # print(raddr)
                if data:
                    # print(data)
                    self.handleRecv(self.client, data)
                else:
                    break

    def handleRecv(self, client, data):
        print("handling http requests")
        if "HTTP" not in bytes.decode(data, buff.encoding):
            message = http.successHttpHead+ \
                "\r\n<html>" \
                "\n<body>" \
                "<p>error http request</p>" \
                "</body>" \
                "\n</html>\n"
            client.send(message.encode('utf8'))
            client.shutdown(2)
            client.close()
            return
        raddr = self.client.getpeername()
        str1 = str(client.getsockname())
        str2 = str(raddr)
        message = http.successHttpHead + \
            "\r\n<html>" \
            "\n<body>" \
            "<p>from: " + str2 + "</p>" \
            "<p>to: " + str1 + "</p>" \
            "</body>" \
            "\n</html>\n"
        json = "" +\
               http.jsonHttpHead +\
               "\r\n{\"Test\":\"test\"}"
        client.send(json.encode('utf8'))
        client.shutdown(2)
        client.close()

    def initSuccess(self):
        # print("httpHandler created!")
        pass
