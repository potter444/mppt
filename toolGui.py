from prototools import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import config
from socketclient import GameSocket
import selectors
from concurrent.futures.thread import ThreadPoolExecutor


QT_APP = QtWidgets.QApplication(sys.argv)
protoData = {}
_selector = selectors.DefaultSelector()
_threadExecutors = []
_networkExecutor = ThreadPoolExecutor(1, 'boss-t')


def init_executor():
    for i in range(2):
        executor = ThreadPoolExecutor(1, 'worker-' + str(i))
        _threadExecutors.append(executor)



class ToolsWindows(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.game = ""
        self.argvlist = []  # 协议参数的列表
        self.loginframe.setVisible(True)
        self.protoframe.setVisible(False)
        self.protofileEdit.setVisible(False)

        gamelist = list(config.gameDict.keys())

        self.gameselect.addItems(gamelist)
        self.gameselect.activated[str].connect(self.get_server)

        self.protofileBox.activated[str].connect(self.select_proto_file)

        self.loginButton.clicked.connect(self.login_game)
        self.quitbutton.clicked.connect(self.relogin)
        self.pushButton.clicked.connect(self.send_proto)
        self.actionstart_testgame_server.triggered.connect(self.start_testgame_server)
        self.sock = GameSocket()

    def get_server(self, game):  # 根据游戏选择服务器地址
        global protoData
        protoData = config.gameDict.get(game).get("getProtoMethod")()

        self.severselect.clear()
        self.severselect.addItems(list(config.gameDict.get(game).get("gameServer")))

    def login_game(self):  # 登陆按钮回调函数，执行登陆逻辑

        self.game = self.gameselect.currentText()
        sever = self.severselect.currentText()
        sever = (sever.split(":")[0], int(sever.split(":")[1]))
        account = self.account.text()
        protoData.get("C2SLogin").get("args")["account"] = account

        self.sock.connect(sever)
        config.gameDict.get(self.game).get("sendMethod")(self.sock, "C2SLogin")

        self.loginframe.setVisible(False)
        self.protoframe.setVisible(True)

        self.proto_name.addItems(list(protoData.keys()))
        self.proto_name.activated[str].connect(self.select_proto)
        filepath = os.listdir(config.gameDict.get(self.game).get("filepath"))
        self.protofileBox.addItems(filepath)


        # self.lineEdit.setText(sever)

    def relogin(self):  # 退出按钮
        self.protofileEdit.clear()
        self.protofileEdit.setVisible(False)
        self.loginframe.setVisible(True)
        self.protoframe.setVisible(False)

    # 选择协议文件，
    def select_proto_file(self, filename):
        # self.protofileBox.clear()
        with open("%s/%s" % (config.gameDict.get(self.game).get("filepath"), filename), "r", encoding="utf-8") as f:
            data = f.read()
            self.protofileEdit.setVisible(True)
            self.protofileEdit.setText(data)

    # 选择协议时，调用的方法。自动生成参数列表
    def select_proto(self, proto):
        self.argvlist.clear()
        self.argvlist = protoData.get(proto).get("args")

        # 先清空form layout
        for i in range(self.argsformLayout.count()):
            self.argsformLayout.itemAt(i).widget().deleteLater()

        if len(self.argvlist) == 0:
            return
        print(self.argvlist)

        # 遍历参数列表，生成QLineEdit
        for i in self.argvlist.keys():
            value_1 = QtWidgets.QLineEdit()

            self.argsformLayout.addRow("%s:" % i, value_1)
        # self.setLayout(self.argsformLayout)

    # 发送协议，获取填写的proto,argv;并将结果输出到文本框
    def send_proto(self):
        argv_value = []
        protoId = self.proto_name.currentText()
        for i in range(self.argsformLayout.count()):
            if self.argsformLayout.itemAt(i).widget().inherits('QLineEdit'):
                argv_value.append(self.argsformLayout.itemAt(i).widget().text())

        print("发送的协议和参数：", protoId, argv_value)



    # 把回包解析，输出在界面上
    def show_result(self, data):
        pass

    # 启动testgame服务器
    def start_testgame_server(self):
        import threading
        p = threading.Thread(target=self.start_process)
        p.start()


    def start_process(self):
        from testserver import SocketServer
        socket_sever = SocketServer()
        socket_sever.start()
        # _networkExecutor.submit(socket_sever.start())

        # _selector.register()


if __name__ == "__main__":
    win = ToolsWindows()
    win.show()
    sys.exit(QT_APP.exec_())