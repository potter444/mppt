from game1method import *
from testmethod import *
import os

# 游戏列表

# gameDict = {"game1":{"loginMethod":game1login,"protofile":game1proto,},
#             "game2":{"loginMethod":game2Login,"protofile":game2Proto,}}

TestGameIP = socket.gethostbyname(socket.gethostname())

gameDict = {"game1": {"gameMethod": Game1Proto,
                      "gameServer": ["0dasfdfasdf", "asdf", "33xcv34533"],
                      "filepath": "game1proto/proto",
                      "C2SprotoDict": get_game1c2s_protobuf,
                      "S2CProtoDict": get_game1s2c_protobuf},

            "TestGame": {"gameMethod": Game2Proto,
                         "gameServer": [socket.gethostbyname(socket.gethostname()) + ":21566", "2", "33333"],
                         "filepath": "testproto/proto",
                         "C2SprotoDict": get_testc2s_protobuf,
                         "S2CProtoDict": get_tests2c_protobuf,
                         }
            }



