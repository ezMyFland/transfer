from FLVHelper.FLVHelper import Flv
from baseSocket import listener
from httpSocket.httpHandler import httpHandler
from videoSocket.videoListener import videoListener

# ls = listener.listener(8088, listener.MODE.LISTEN)
# ls1 = listener.listener(8188, listener.MODE.LISTEN)
# ls2 = listener.listener(8888, listener.MODE.TRANSFER, targetport="8188")
# ls2 = listener.listener(8888, listener.MODE.LISTEN)
# ls.start()
# ls1.start()
# ls2.start()

#
# ls = listener.listener(8888, listener.MODE.HTTPHANDLER)
# ls.start()


ls = videoListener()
ls.start()

# fl = Flv()
# ret = fl.load("C:\\Users\\89749\\Documents\\Tencent Files\\897494980\\FileRecv\\36721-2016-10-15-21-17-29.flv")
# print("共找到%d个tag" % ret)

