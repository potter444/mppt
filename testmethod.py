import sys
import inspect
import os
import socket
import struct

from testproto.proto_py.testProtocolCode_pb2 import *
from testproto.proto_py.Test_pb2 import *



def get_testc2s_protobuf():
    d = {}
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name[:3] == "C2S":
            l = []
            for i in eval(name).DESCRIPTOR.fields:
                l.append(i.name)
            d.setdefault(name, l)
    print("客户端发送的协议及参数：", d)
    return d


def get_tests2c_protobuf():
    d = {}
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name[:3] == "S2C":
            l = []
            for i in eval(name).DESCRIPTOR.fields:
                l.append(i.name)
            d.setdefault(name, l)
    print("服务器返回的协议及参数：", d)
    return d


def send_pack(sock, cmd, data):
    length = len(data)
    fmt = ">iih%ss" % length
    d = struct.pack(fmt, (length + 6), cmd, 0, data)
    print("发送的协议号：", cmd)
    sock.send(d)


def login(sock):
    login = C2SLogin()
    login.account = "po001"
    login.connectKey = "fxltsbl"
    print(login)
    data = login.SerializeToString()
    print(data)
    send_pack(sock, 1001, data)


def heart(sock):
    h = C2SHeart()
    h.account = "po001"
    data = h.SerializeToString()
    send_pack(sock, 1002, data)


def socker_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.10.143", 21566))
    while True:

        num = int(input("输入数字："))
        if num == 1:
            login(sock)
        elif num == 2:
            heart(sock)
        elif num == 4:
            continue
        else:
            sock.close()
            break


if __name__ == "__main__":
    socker_client()