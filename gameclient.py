'''
游戏机器人实现
创建线程池
流程：
1、生成一个线程，作为主体，显示GUI，登陆游戏，发送协议
2、生成第二个线程，监听服务器返回
3、生成第三个线程，负责心跳发送，维持tcp链接
'''

from concurrent.futures.thread import ThreadPoolExecutor
from config import *

_threadExecutors = []
_networkExecutor = ThreadPoolExecutor(1, 'boss-t')


def init_executor():
    for i in range(3):
        executor = ThreadPoolExecutor(1, 'worker-' + str(i))
        _threadExecutors.append(executor)


def choose_executor(obj):
    index = hash(obj) % len(_threadExecutors)
    return _threadExecutors[index]


def logingame(game: str, addr, account):
    client = gameDict.get(game).get("gameMethod")(addr, account)
    client.game1login()


if __name__ == "__main__":
    init_executor()
    print(_networkExecutor)
    print(_threadExecutors)
    logingame("game1", ("192.168.10.143", 21566), "po001")