from socket import socket
from staticData import videoStr
import time


s = socket()
s.connect(("localhost", 10086))
s.send("yes".encode())
data = s.recv(1024)
if bytes.decode(data) == videoStr.CONNECT_SUCCESS or bytes.decode(data) == videoStr.DEFAULT_CHECK_CONNECT_STRING_LISTENER:
    print("connected")
    time.sleep(5)
    s.send((videoStr.CHANGE_VIDEO_NAME + " " +
            "C:/Users/89749/Documents/Tencent Files/897494980/FileRecv/36721-2016-10-15-21-17-29.flv "
            +videoStr.CHANGE_VIDEO_NAME_EOF
            ).encode())
    while True:
        print(bytes.decode(data))
# data = s.recv(1024)
# print(bytes.decode(data))
# if bytes.decode(data) == videoStr.CONNECT_SUCCESS or bytes.decode(data) == videoStr.DEFAULT_CHECK_CONNECT_STRING_LISTENER:
#     s.send((videoStr.CHANGE_VIDEO_NAME+" "+ "C:\\Users\\89749\\Documents\\Tencent Files\\897494980\\FileRecv\\36721-2016-10-15-21-17-29.flv").encode())
#     while True:
#         data = s.recv(4096)
#         print(bytes.decode(data))

