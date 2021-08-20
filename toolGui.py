from prototools import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import config

QT_APP = QtWidgets.QApplication(sys.argv)


class ToolsWindows(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.game = ""
        self.loginframe.setVisible(True)
        self.protoframe.setVisible(False)
        self.protofileEdit.setVisible(False)

        gamelist = list(config.gameDict.keys())

        self.gameselect.addItems(gamelist)
        self.gameselect.activated[str].connect(self.get_server)

        self.protofileBox.activated[str].connect(self.selectprotofile)

        self.loginButton.clicked.connect(self.login_game)
        self.quitbutton.clicked.connect(self.relogin)

    def get_server(self, game):  # 根据游戏选择服务器地址
        self.severselect.clear()
        self.severselect.addItems(list(config.gameDict.get(game).get("gameServer")))

    def login_game(self):  # 登陆按钮回调函数，执行登陆逻辑
        self.game = self.gameselect.currentText()
        sever = self.severselect.currentIndex()

        self.loginframe.setVisible(False)
        self.protoframe.setVisible(True)
        self.c2sproto = config.gameDict.get(self.game).get("C2SprotoDict")()
        self.proto_name.addItems(list(self.c2sproto.keys()))
        self.proto_name.activated[str].connect(self.select_proto)
        filepath = os.listdir(config.gameDict.get(self.game).get("filepath"))
        self.protofileBox.addItems(filepath)


        # self.lineEdit.setText(sever)

    def relogin(self):  # 退出按钮
        self.protofileEdit.clear()
        self.protofileEdit.setVisible(False)
        self.loginframe.setVisible(True)
        self.protoframe.setVisible(False)


    def selectprotofile(self, filename):
        # self.protofileBox.clear()
        with open("%s/%s" % (config.gameDict.get(self.game).get("filepath"), filename), "r", encoding="utf-8") as f:
            data = f.read()
            self.protofileEdit.setVisible(True)
            self.protofileEdit.setText(data)

    # 选择协议时，调用的方法。自动生成参数列表
    def select_proto(self, proto):
        argvlist = self.c2sproto.get(proto)
        if len(argvlist) == 0:
            return
        print(argvlist)
        for i in range(self.argsformLayout.count()):
            self.argsformLayout.itemAt(i).widget().deleteLater()

        for i in argvlist:
            value_1 = QtWidgets.QLineEdit()

            self.argsformLayout.addRow("%s:" % i, value_1)
        # self.setLayout(self.argsformLayout)

    # 发送协议，获取填写的proto,argv;并将结果输出到文本框
    def send_proto(self):
        pass


if __name__ == "__main__":
    win = ToolsWindows()
    win.show()
    sys.exit(QT_APP.exec_())