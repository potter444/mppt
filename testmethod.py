import sys
import inspect
import os
import socket
import struct

from testproto.proto_py.testProtocolCode_pb2 import *
from testproto.proto_py.Test_pb2 import *

"""
获取游戏的协议，参数，协议号，实例方法，返回一个字典
格式：protoData={"C2SLogin":{"cmd":1001, "args": {"account": "", "connectKey": ""}, "method": "login"},
                    "C2SHeart": {"cmd": 1002, "args": {"account": ""}, "method": "heart"}
                    }
"""
protoData = {}


def get_testgame_protobuf():
    global protoData
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if name[:3] == "C2S":
                l = {}
                for i in eval(name).DESCRIPTOR.fields:
                    l.setdefault(i.name, "")
                if name not in protoData:
                    protoData.setdefault(name, {"args": l})
                else:
                    protoData[name]["args"] = l

        elif inspect.isfunction(obj):
            fullargs = inspect.getfullargspec(obj)

            if len(fullargs.args) == 2 and fullargs.args == ['cmd', 'method']:
                if fullargs.defaults[1] not in protoData:
                    protoData.setdefault(fullargs.defaults[1], {})
                    protoData[fullargs.defaults[1]]["cmd"] = fullargs.defaults[0]
                    protoData[fullargs.defaults[1]]["method"] = name
                else:
                    protoData[fullargs.defaults[1]]["cmd"] = inspect.getfullargspec(obj).defaults[0]
                    protoData[fullargs.defaults[1]]["method"] = name

    print("客户端发送的协议及参数：", protoData)
    return protoData


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

# 数据格式解析
def get_int_value(data: str):
    return int(data)

def get_str_value(data: str):
    return data


# 按照格式，封包，发送
def testgame_pack(cmd, data):
    length = len(data)
    fmt = ">iih%ss" % length
    d = struct.pack(fmt, (length + 6), cmd, 0, data)
    print("发送的协议号：", cmd)
    return d


def login(cmd=1001, method="C2SLogin"):  # 登陆协议实例化
    l = C2SLogin()
    data = protoData.get(method)
    l.account = get_str_value(data.get("args").get("account"))
    l.connectKey = get_str_value(data.get("args").get("connectKey"))
    data = l.SerializeToString()
    return data


def heart(cmd=1002, method="C2SHeart"): # 心跳协议实例化
    data = protoData.get(method)
    h = C2SHeart()
    h.account = get_str_value(data.get("args").get("account"))
    data = h.SerializeToString()
    return data


# 协议发送的方法，传入数据，sock
def testgame_send(sock, protoID):
    proto = protoData.get(protoID).get("method")
    proto = eval(proto)()
    cmd = protoData.get(protoID).get("cmd")
    data = testgame_pack(cmd, proto)
    sock.send(data)


# 协议接收方法，接收回包，返回结果
def testgame_recv(sock, cmd):
    pass


def socket_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.10.143", 21566))
    while True:

        num = int(input("输入数字："))
        if num == 1:
            testgame_send(sock, "C2SHeart")
        elif num == 2:
            testgame_send(sock, "C2SLogin")
        elif num == 4:
            continue
        else:
            sock.close()
            break


if __name__ == "__main__":

    # get_all_proto()
    get_testgame_protobuf()
    socket_client()