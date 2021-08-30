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
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isfunction):
        if name[:3] == "s2c":
            fullargs = inspect.getfullargspec(obj)
            d.setdefault(fullargs.defaults[0], name)
            # l = []
            # for i in eval(name).DESCRIPTOR.fields:
            #     l.append(i.name)
            # d.setdefault(name, l)
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

    return l.SerializeToString()


def heart(cmd=1002, method="C2SHeart"): # 心跳协议实例化
    data = protoData.get(method)
    h = C2SHeart()
    h.account = get_str_value(data.get("args").get("account"))

    return h.SerializeToString()


def s2c_login(data, cmd=1001):
    h = S2CLogin()
    h.ParseToString(data)
    print("服务器登陆返回：", h.account, h)
    return h


def s2c_heart(data, cmd=1002):
    h = S2CHeart()
    h.ParseToString(data)
    print("服务器心跳返回：", h.account, h)
    return h


# 协议发送的方法，传入数据，sock
def testgame_send(sock, protoID):
    proto = protoData.get(protoID).get("method")
    proto = eval(proto)()
    cmd = protoData.get(protoID).get("cmd")
    data = testgame_pack(cmd, proto)
    sock.send(data)


# 协议接收方法，接收回包，返回结果
def testgame_recv(sock, cmd):
    head_data = sock.recv(4)
    if not head_data:
        return
    size = struct.unpack(">i", head_data)[0]

    body_data = sock.recv(size)

    total_data = body_data
    current_size = size
    while body_data:
        try:
            body_data = sock.recv(1024)
            total_data += body_data
            current_size += len(body_data)
        except BaseException:
            body_data = b''
    else:
        print("接收数据完毕, 当前数据长度: %dB, 预计读取长度: %dB" % (current_size, size))

    next_package = data_unpack(size, total_data)
    while next_package:
        remain_len = len(next_package) - 4
        data_pair = struct.unpack(">i%ss" % remain_len, next_package)
        next_package = data_unpack(data_pair[0], data_pair[1])


#  传入body_data,size。解析成对应的协议值
def data_unpack(size, body_data):
    data_len = len(body_data) - 9
    fmt = ">ihhb%ss" % data_len
    result = struct.unpack(fmt, body_data)
    cmd = result[0]
    seqno = result[1]
    clino = result[2]
    resno = result[3]
    data_remain = result[4]

    proto_len = size - 9
    if len(data_remain) > proto_len:
        fmt = "%ss%ss" % (proto_len, data_len-proto_len)
        data_array = struct.unpack(fmt, data_remain)
        data_body = data_array[0]
        next_package = data_array[1]
    else:
        data_body = data_remain
        next_package = None

    handler = get_tests2c_protobuf()
    server_method = handler.get(cmd)
    if server_method is not None:
        result_data = server_method(data_body, cmd)
    else:
        print("没找找到%s协议" % cmd)

    return next_package


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
    get_tests2c_protobuf()
    # socket_client()