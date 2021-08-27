import socket


class GameSocket:
    """
    socket 客户端重新实现
    """

    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._addr
        self._addr = ""

    def getaddr(self):
        return self._addr

    def connect(self, addr: tuple, blocking=True):
        self._client.setblocking(blocking)
        self._addr = addr
        return self._client.connect_ex(addr)

    def send(self, data):
        return self._client.send(data)

    def recv(self, length):
        return self._client.recv(length)

    def close(self):
        self._client.close()

    def getfileno(self):
        return self._client.fileno()