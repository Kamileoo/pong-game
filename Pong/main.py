from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import mylogin
import game
import hub
import config


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

    def keyPressEvent(self, event):
        if game.game_val['is_game']:
            game.keyHandler(event, 'P')
    def keyReleaseEvent(self, event):
        if game.game_val['is_game']:
            game.keyHandler(event, 'R')


if len(sys.argv)<3:
    print("Specify arguments - <serwer_ip_address> <serwer_port>")
    exit(1)
config.glob_params['ip']=sys.argv[1]
config.glob_params['port']=sys.argv[2]
app = QtWidgets.QApplication(sys.argv)
win = MyWindow()
win.setWindowTitle("Pong")
win.setFixedSize(1024, 512)

config.window = win
config.glob_grid = QtWidgets.QGridLayout(config.window)

#hub.hub_ui(win)
mylogin.login_ui()

win.show()
sys.exit(app.exec())