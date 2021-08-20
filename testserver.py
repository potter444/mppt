
"""模拟服务器
 * 游戏TCP前后端通信包头信息
 *
 * 客户端发给服务端的信息
 *
 * Length  包长度, 4个字节
 * Protocol  协议号, 4个字节
 * SequenceNO  包流水号, 测试可以随便设值, 2个字节
 * Content  包内容, protobuf字节流
 *
 * +----------+----------+----------------+----------------+
 * |  Length  | Protocol |   SequenceNO   |    Content     |
 * |   100    |   1001   |      123       |    protobuf    |
 * +----------+----------+----------------+----------------+
 *
 *
 * 服务端推送给客户端的信息
 * Length  包长度, 4个字节
 * Protocol  协议号, 4个字节
 * ServerSequenceNO  服务端流水号, 2个字节
 * ClientSequenceNO  客户端流水号, 2个字节
 * Result  处理结果, 0:成功 1:失败 1个字节
 * Content  包内容, protobuf字节流
 *
 * +--------+----------+------------------+------------------+--------+-----------+
 * | Length | Protocol | ServerSequenceNO | ClientSequenceNO | Result |  Content  |
 * |   100  |   1001   |       123        |       123        |    0   |  protobuf |
 * +--------+----------+------------------+------------------+--------+-----------+
"""

import socket
import struct
from testproto.proto_py.Test_pb2 import *


print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))


class SocketServer:

    def __init__(self):
        self._computer = socket.gethostname()
        self._host = socket.gethostbyname(self._computer)
        self._port = 21566

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.severSequenceNO = 0
        self.clientSequenceNO = 0

    def start(self):
        self.server.bind((self._host, self._port))
        self.server.listen(50)
        while True:
            print("服务器启动，监听客户端链接")
            client, addr = self.server.accept()
            print("连接的客户端：", addr)
            while True:
                try:
                    # data = client.recv(1024).decode()
                    cmd, proto_data = self.server_unpack(client)
                    cmd = int(cmd)
                except Exception as e:
                    print("错误：", e)
                    print("客户端断开:", addr)
                    break
                print("客户端发送的内容：", cmd)

                if not cmd:
                    break
                if cmd == 1001:
                    self.login(client, proto_data)
                elif cmd == 1002:
                    self.heart(client, proto_data)
                else:
                    data = "没有这个协议"
                    self.send_data(client, cmd, data.encode(), result=1)
                # client.send(data.encode())

            client.close()

    # 收包，先收4个字节，解出长度，再接收剩下的.解客户端的包
    def server_unpack(self, client):

        (length,) = struct.unpack(">i", client.recv(4))
        data = client.recv(int(length))
        fmt = ">ih%ss" % (length - 6)
        (cmd, SequenceNO, proto_data) = struct.unpack(fmt, data)
        return cmd, proto_data

    def login(self, client, proto_data):  # 登陆协议

        loginproto = C2SLogin()
        loginproto.ParseFromString(proto_data)
        print("收到登陆请求:", loginproto, loginproto.account)

        c2slogin = S2CLogin()
        c2slogin.account = loginproto.account
        c2slogin.result = "success"
        data = c2slogin.SerializeToString()
        self.send_data(client, 1001, data)

    def heart(self, client, proto_data):  # 心跳协议

        heartproto = C2SHeart()
        heartproto.ParseFromString(proto_data)
        print("收到心跳请求:", heartproto, heartproto.account)

        c2sheart = S2CHeart()
        c2sheart.account = heartproto.account
        data = c2sheart.SerializeToString()

        self.send_data(client, 1002, data)

    def send_data(self, client, cmd, data, result=0):  # 发送格式封装
        length = len(data)
        fmt = ">iihhb%ss" % length
        pack = struct.pack(fmt, (length+9), cmd, self.severSequenceNO+1, self.clientSequenceNO+1, result, data)
        client.send(pack)


if __name__ == "__main__":

    sock = SocketServer()
    sock.start()
    sock.server.close()