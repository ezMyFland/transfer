from socket import socket
from staticData import videoStr,buff
import time
import re
from FLVHelper.TAGHelper.FLVHead import Head
from videoSocket import videoClient

client = videoClient.client(filepath="C:/Users/89749/Documents/Tencent Files/897494980/FileRecv/36721-2016-10-15-21-17-29.flv ")
client.run()


# s = socket()
# s.connect(("localhost", 10086))
# s.send("yes".encode())
# buff = s.recv(1024)
# data = ""
# tag = []
# taglengthsum = None
# FLVhead = None
# if bytes.decode(buff) == videoStr.CONNECT_SUCCESS or bytes.decode(buff) == videoStr.DEFAULT_CHECK_CONNECT_STRING_LISTENER:
#     print("connected")
#     time.sleep(5)
#     s.send((videoStr.CHANGE_VIDEO_NAME + " " +
#             "C:/Users/89749/Documents/Tencent Files/897494980/FileRecv/36721-2016-10-15-21-17-29.flv "
#             +videoStr.CHANGE_VIDEO_NAME_EOF
#             ).encode())
#     i = 0
#     while True:
#         buff = s.recv(4096)
#         data += bytes.decode(buff)
#         data = data.replace(videoStr.DEFAULT_CHECK_CONNECT_STRING_LISTENER, "")
#         if not taglengthsum:
#             lengthtag = re.findall(r""+videoStr.TAG_SUM_START+"(.+?)"+videoStr.TAG_SUM_END, data)
#             if len(lengthtag) > 0:
#                 taglengthsum = int(lengthtag[0])
#                 tag = ["" for i in range(taglengthsum)]
#                 data = data.replace(videoStr.TAG_SUM_START+lengthtag[0]+videoStr.TAG_SUM_END,"")
#             else:
#                 continue
#         if not FLVhead:
#             FLVheadtag = re.findall(r""+videoStr.HEAD_START+"(.+?)"+videoStr.HEAD_END, data)
#             if len(FLVheadtag) > 0:
#                 FLVhead = Head(FLVheadtag[0].encode())
#                 data = data.replace(videoStr.HEAD_START+FLVheadtag[0]+videoStr.HEAD_END,"")
#                 data = data[1:]
#             else:
#                 continue
#
#         rectags = re.findall(r""+videoStr.TAG_HEAD+"(.+?)"+videoStr.TAG_END, data)
#         if len(rectags) != 0:
#             for string in rectags:
#                 # tag.append(string)
#                 data = data.replace(videoStr.TAG_HEAD+string+videoStr.TAG_END, "")
#                 start_tag_loc = string.find(videoStr.TAG_START)
#                 tag_loc = int(string[:start_tag_loc])
#                 tag[tag_loc] = string[start_tag_loc+len(videoStr.TAG_START):]
#                 print(tag.index(""))
#
